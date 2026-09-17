"""Tests for the harness seam (spruce_grove/harness/).

The seam is the sovereignty boundary between grove code and whatever agent
framework executes underneath. These tests prove three things:

1. Selection works and fails soft (unknown names fall back, never crash).
2. Behavior parity: the seam resolves models exactly like the inherited
   ``ModelFactory.get_model`` it delegates to — same raises, same Nones,
   same handle types.
3. The boundary is structurally pure: ``protocol.py`` (the grove-owned
   vocabulary) contains no reference to the external framework, so the
   seam cannot quietly dissolve.
"""

import inspect

import pytest

from spruce_grove import harness
from spruce_grove.harness import get_harness
from spruce_grove.harness.selector import DEFAULT_HARNESS, available_harnesses


class TestSelection:
    def test_default_selection_is_inherited_framework(self):
        h = get_harness()
        assert h.info.name == DEFAULT_HARNESS == "pydantic"

    def test_unknown_selector_falls_back_without_raising(self, monkeypatch):
        monkeypatch.setenv("SPRUCE_GROVE_HARNESS", "does-not-exist")
        h = get_harness()
        assert h.info.name == "pydantic"

    def test_selector_env_is_respected(self, monkeypatch):
        monkeypatch.setenv("SPRUCE_GROVE_HARNESS", "pydantic")
        h = get_harness()
        assert h.info.name == "pydantic"

    def test_available_harnesses_registry(self):
        registry = available_harnesses()
        assert "pydantic" in registry
        assert all(hasattr(info, "description") for info in registry.values())

    def test_satisfies_grove_protocol(self):
        from spruce_grove.harness.protocol import Harness

        assert isinstance(get_harness(), Harness)


class _ParityBase:
    """Shared fixture-ish helpers: a minimal openai-type model config."""

    CONFIG = {"test-model": {"type": "openai", "name": "gpt-test"}}

    @pytest.fixture(autouse=True)
    def _no_api_keys(self, monkeypatch):
        for var in ("OPENAI_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY"):
            monkeypatch.delenv(var, raising=False)


class TestResolveModelParity(_ParityBase):
    def test_unknown_model_raises_valueerror_both_paths(self):
        direct = None
        through_seam = None
        try:
            from spruce_grove.model_factory import ModelFactory

            ModelFactory.get_model("no-such-model", {})
        except ValueError as e:
            direct = str(e)
        try:
            get_harness().resolve_model("no-such-model", {})
        except ValueError as e:
            through_seam = str(e)
        assert direct is not None and through_seam == direct

    def test_missing_credentials_returns_none_both_paths(self):
        from spruce_grove.model_factory import ModelFactory

        direct = ModelFactory.get_model("test-model", self.CONFIG)
        through = get_harness().resolve_model("test-model", self.CONFIG)
        assert direct is None and through is None

    def test_handle_type_parity_with_credentials(self, monkeypatch):
        from spruce_grove import model_factory
        from spruce_grove.model_factory import ModelFactory

        monkeypatch.setattr(model_factory, "get_api_key", lambda name: "test-key-123")
        direct = ModelFactory.get_model("test-model", self.CONFIG)
        through = get_harness().resolve_model("test-model", self.CONFIG)
        assert direct is not None and through is not None
        assert type(direct) is type(through)
        assert through.model_name == direct.model_name == "gpt-test"


class TestBoundaryPurity:
    def test_protocol_has_no_external_framework_imports(self):
        source = inspect.getsource(harness.protocol)
        assert "pydantic_ai" not in source
        assert "from pydantic" not in source

    def test_selector_defers_framework_import(self):
        source = inspect.getsource(harness.selector)
        # The heavy import lives inside the implementation module, not at
        # selector top level — selecting/inspecting stays import-light.
        top_level = source.split("def get_harness")[0]
        assert "pydantic_ai" not in top_level
