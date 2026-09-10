"""Tests for the tolerant custom_openai chat-completions model.

Reproduces the exact Synthetic.new failure that sent the wiggum /goal
judges into a permanent ABSTAIN loop: the gateway returns
``metadata.weight_versions`` as a *list*, and pydantic-ai's strict
``_ChatCompletion`` re-validation (``metadata: dict[str, str]``) rejects
the whole response. The tolerant subclass must scrub and succeed; the
stock model must keep failing (proving the repro is real).
"""

from typing import Any, Dict, Optional

import pytest
from openai.types.chat import ChatCompletion
from pydantic import ValidationError
from pydantic_ai.models import openai as _openai_models
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from spruce_grove.tolerant_openai import (
    TolerantOpenAIChatModel,
    _scrub_non_string_metadata,
)

WEIGHT_VERSIONS = [{"version": "default", "start": 0, "end": 313}]


# pydantic-ai's strict ``_ChatCompletion`` copy declares
# ``metadata: dict[str, str]`` on some release lines (verified empirically:
# declared on 2.33.0 / 2.36.0 / 2.40.0, absent on 2.35.0 pinned here). The
# judge harness environment runs a declaring line, which is where
# Synthetic.new's list-typed ``weight_versions`` aborts validation. Patch a
# declaring variant in so the repro holds on ANY installed version.
class _StrictChatCompletion(_openai_models._ChatCompletion):
    metadata: Optional[Dict[str, str]] = None


@pytest.fixture
def strict_metadata_env(monkeypatch):
    """Simulate the judge env: strict ``metadata: dict[str, str]``."""
    monkeypatch.setattr(_openai_models, "_ChatCompletion", _StrictChatCompletion)
    return _StrictChatCompletion


def _payload(metadata: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1_757_000_000,
        "model": "hf:zai-org/GLM-4.7-Flash",
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": "complete: yes"},
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        },
    }
    if metadata is not None:
        payload["metadata"] = metadata
    return payload


def _replay(metadata: Any = None) -> ChatCompletion:
    # model_construct skips validation, mirroring what the SDK effectively
    # hands pydantic-ai when the upstream payload is schema-nonconforming.
    return ChatCompletion.model_construct(**_payload(metadata))


def _strict_model() -> OpenAIChatModel:
    provider = OpenAIProvider(
        base_url="https://api.synthetic.new/openai/v1", api_key="sk-test"
    )
    return OpenAIChatModel(model_name="hf:zai-org/GLM-4.7-Flash", provider=provider)


def _tolerant_model() -> TolerantOpenAIChatModel:
    provider = OpenAIProvider(
        base_url="https://api.synthetic.new/openai/v1", api_key="sk-test"
    )
    return TolerantOpenAIChatModel(
        model_name="hf:zai-org/GLM-4.7-Flash", provider=provider
    )


class TestReproduction:
    """The bug, replayed offline, byte-for-byte on the observed field."""

    def test_stock_model_rejects_weight_versions_list(self, strict_metadata_env):
        with pytest.raises(ValidationError) as exc_info:
            _strict_model()._validate_completion(
                _replay(metadata={"weight_versions": WEIGHT_VERSIONS})
            )
        assert "weight_versions" in str(exc_info.value)

    def test_tolerant_model_accepts_and_preserves_content(self, strict_metadata_env):
        validated = _tolerant_model()._validate_completion(
            _replay(metadata={"weight_versions": WEIGHT_VERSIONS})
        )
        assert validated.choices[0].message.content == "complete: yes"
        # Lossy-by-design only in the informational metadata map.
        assert isinstance(validated.metadata["weight_versions"], str)

    def test_tolerant_is_passthrough_on_lenient_versions(self):
        # Without the strict-metadata patch (as pinned in this repo), the
        # wrapper must behave exactly like the stock model: no raising, no
        # alteration of the happy path.
        validated = _tolerant_model()._validate_completion(
            _replay(metadata={"weight_versions": WEIGHT_VERSIONS})
        )
        assert validated.choices[0].message.content == "complete: yes"


class TestScrubbing:
    def test_scrub_encodes_non_string_values(self):
        scrubbed = _scrub_non_string_metadata(
            {"metadata": {"a": 1, "b": "ok", "c": None, "d": [1, 2]}}
        )
        assert scrubbed is not None
        assert scrubbed["metadata"] == {"a": "1", "b": "ok", "c": "null", "d": "[1, 2]"}

    def test_scrub_noop_when_conforming(self):
        assert _scrub_non_string_metadata({"metadata": {"a": "ok"}}) is None
        assert _scrub_non_string_metadata({}) is None
        assert _scrub_non_string_metadata({"metadata": None}) is None

    def test_tolerant_still_clean_when_metadata_conforming(self, strict_metadata_env):
        validated = _tolerant_model()._validate_completion(
            _replay(metadata={"region": "iad"})
        )
        assert validated.metadata == {"region": "iad"}

    def test_tolerant_does_not_mask_unrelated_failures(self, strict_metadata_env):
        # Missing 'choices' entirely: scrub finds nothing to fix and the
        # original ValidationError must propagate unchanged.
        broken = ChatCompletion.model_construct(
            id="chatcmpl-x",
            created=1,
            model="m",
            object="chat.completion",
            metadata={"weight_versions": "fine"},
        )
        with pytest.raises(ValidationError):
            _tolerant_model()._validate_completion(broken)


class TestFactoryWiring:
    def test_custom_openai_branch_returns_tolerant_model(self):
        from spruce_grove.model_factory import ModelFactory

        config = {
            "hf:zai-org/GLM-4.7-Flash": {
                "type": "custom_openai",
                "provider": "synthetic",
                "name": "hf:zai-org/GLM-4.7-Flash",
                "custom_endpoint": {
                    "url": "https://api.synthetic.new/openai/v1",
                    "api_key": "sk-test",
                },
            }
        }
        model = ModelFactory.get_model("hf:zai-org/GLM-4.7-Flash", config)
        assert isinstance(model, TolerantOpenAIChatModel)

    def test_first_party_openai_stays_strict(self):
        # The 'openai' type is untouched: no env key -> get_model warns and
        # returns None rather than secretly using the tolerant class.
        from spruce_grove.model_factory import ModelFactory

        model = ModelFactory.get_model(
            "gpt-4", {"gpt-4": {"type": "openai", "name": "gpt-4"}}
        )
        assert model is None or type(model) is OpenAIChatModel
