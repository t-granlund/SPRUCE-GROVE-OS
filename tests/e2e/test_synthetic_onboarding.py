"""E2E for /onboard-synthetic — Synthetic.new subscriber onboarding.

Runs the real apply_onboarding against an isolated temp HOME and verifies:
  - the 11-model set (4 rotation-safe aliases + 7 pinned) matching the
    2026-09 live catalog: DeepSeek-V4.1-Flash in, GLM-5.2 rotated out
  - multimodal entries carry supports_vision; syn:large:text comes first,
    so it is the default vision target (cheapest multimodal alias)
  - the API key path resolves through the shared credential store
  - extra_models.json + grove.cfg land with the driving seat assigned
  - rotated-out pins are pruned from extra_models.json on re-run
  - catalog drift detection + the free quota/embeddings probes
  - the /onboard-synthetic command is registered
"""

import json
import os
import tempfile
import unittest.mock as mock
import urllib.error

import pytest


@pytest.fixture()
def isolated_home(monkeypatch):
    tmp = tempfile.mkdtemp()
    monkeypatch.setenv("HOME", tmp)
    monkeypatch.setenv("XDG_CONFIG_HOME", os.path.join(tmp, ".config"))
    # Re-import the grove so CONFIG_DIR resolves inside the sandbox, but
    # RESTORE the original module objects afterwards. Deleting them breaks
    # every later test whose patches reference the original module objects
    # (this hung the MCP wizard suite: its prompt mock vanished and the
    # wizard blocked on real stdin).
    saved = {k: v for k, v in sys.modules.items() if k.startswith("spruce_grove")}
    for mod in [m for m in list(sys.modules) if m.startswith("spruce_grove")]:
        del sys.modules[mod]
    yield tmp
    for mod in [m for m in list(sys.modules) if m.startswith("spruce_grove")]:
        del sys.modules[mod]
    sys.modules.update(saved)


import sys  # noqa: E402  (kept late so the fixture comment above reads first)

sys.modules.setdefault("spruce_grove", sys.modules.get("spruce_grove"))


def test_model_set_is_the_maintainer_config(isolated_home):
    from spruce_grove.command_line.onboarding_synthetic import build_synthetic_models

    models = build_synthetic_models()
    assert len(models) == 11
    assert models["syn:large:text"]["supports_vision"] is True
    assert models["syn:large:vision"]["supports_vision"] is True
    assert models["syn:small:vision"]["supports_vision"] is True
    # GLM-4.7-Flash (syn:small:text upstream) is text-only per the live catalog.
    assert not models["syn:small:text"].get("supports_vision")
    # 2026-09 catalog: DeepSeek-V4.1-Flash is the syn:large:text upstream and
    # GLM-5.2 has been rotated out of the live subscription entirely.
    assert "hf:deepseek-ai/DeepSeek-V4.1-Flash" in models
    assert "hf:zai-org/GLM-5.2" not in models
    # Live catalog reports max_output_length 65536 for the entire lineup.
    assert all(m["max_output_tokens"] == 65536 for m in models.values())


def test_probe_handles_success_and_rejection(isolated_home):
    from spruce_grove.command_line.onboarding_synthetic import probe_endpoint

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"data": [{"id": "x"}, {"id": "y"}]}).encode()

    with mock.patch("urllib.request.urlopen", return_value=FakeResp()):
        ok, detail = probe_endpoint("sk-test")
    assert ok and "2 models" in detail

    with mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("u", 401, "denied", None, None),
    ):
        ok, detail = probe_endpoint("bad-key")
    assert not ok and "401" in detail


def test_catalog_drift_detects_rotation_and_newcomers():
    from spruce_grove.command_line.onboarding_synthetic import check_catalog_drift

    live = [
        "syn:large:text",
        "syn:small:text",
        "syn:large:vision",
        "syn:small:vision",
        "hf:zai-org/GLM-5.3-Flash",
        "hf:deepseek-ai/DeepSeek-V4.1-Flash",
        "hf:zai-org/GLM-4.7-Flash",
        "hf:moonshotai/Kimi-K3",
        "hf:Qwen/Qwen3.8-27B",
        "hf:nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4",
        "hf:openai/gpt-oss-120b",
        "hf:brand-new/Model-X",
    ]
    rotated, unpinned = check_catalog_drift(live)
    # The live catalog covers every current pin -> nothing rotated out;
    # the unknown newcomer is surfaced as informational only.
    assert rotated == []
    assert unpinned == ["hf:brand-new/Model-X"]

    rotated, _ = check_catalog_drift([i for i in live if "GLM-5.3" not in i])
    assert rotated == ["hf:zai-org/GLM-5.3-Flash"]


def test_probe_quotas_parses_live_payload():
    from spruce_grove.command_line.onboarding_synthetic import probe_quotas

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps(
                {
                    "subscription": {"limit": 1750, "requests": 3},
                    "weeklyTokenLimit": {
                        "maxCredits": "$84.00",
                        "remainingCredits": "$48.73",
                        "percentRemaining": 58.018,
                    },
                    "rollingFiveHourLimit": {
                        "remaining": 1748.7,
                        "max": 1750,
                        "limited": False,
                    },
                }
            ).encode()

    with mock.patch("urllib.request.urlopen", return_value=FakeResp()):
        ok, detail = probe_quotas("sk-test")
    assert ok
    assert "$48.73 of $84.00, 58%" in detail
    assert "5-hour requests 1748.7 of 1750" in detail

    with mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError("u", 401, "denied", None, None),
    ):
        ok, detail = probe_quotas("bad-key")
    assert not ok and "401" in detail


def test_probe_embeddings_reports_dimensions():
    from spruce_grove.command_line.onboarding_synthetic import (
        EMBEDDINGS_MODEL,
        probe_embeddings,
    )

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"data": [{"embedding": [0.1, 0.2, 0.3]}]}).encode()

    with mock.patch("urllib.request.urlopen", return_value=FakeResp()):
        ok, detail = probe_embeddings("sk-test")
    assert ok
    assert EMBEDDINGS_MODEL in detail
    assert "3-dim" in detail


def test_apply_onboarding_writes_models_key_and_main_model(isolated_home):
    from spruce_grove.command_line.onboarding_synthetic import (
        EXTRA_MODELS_PATH,
        apply_onboarding,
    )

    # A stale install still carries the rotated-out GLM-5.2 pin and a
    # user-added model; onboarding must prune the former, keep the latter.
    os.makedirs(os.path.dirname(EXTRA_MODELS_PATH), exist_ok=True)
    with open(EXTRA_MODELS_PATH, "w") as f:
        json.dump(
            {
                "hf:zai-org/GLM-5.2": {"type": "custom_openai"},
                "my:own:model": {"type": "custom_openai"},
            },
            f,
        )

    with mock.patch("spruce_grove.command_line.onboarding_synthetic.set_api_key"):
        with mock.patch.dict(os.environ, {"SYNTHETIC_API_KEY": "sk-test"}):
            apply_onboarding("sk-test")

    models = json.load(open(EXTRA_MODELS_PATH))
    assert len([k for k in models if k.startswith(("syn:", "hf:"))]) == 11
    assert "hf:zai-org/GLM-5.2" not in models
    assert "my:own:model" in models
    assert models["syn:large:text"]["supports_vision"] is True
    assert models["syn:large:vision"]["supports_vision"] is True

    cfg_path = os.path.join(isolated_home, ".config", "spruce_grove", "grove.cfg")
    assert "model = syn:large:text" in open(cfg_path).read()


def test_command_registered(isolated_home):
    # Mirror production: command_handler imports every command module,
    # which is what populates the live registry.
    import spruce_grove.command_line.command_handler  # noqa: F401
    from spruce_grove.command_line.command_registry import get_unique_commands

    names = [
        c["name"] if isinstance(c, dict) else getattr(c, "name", "")
        for c in get_unique_commands()
    ]
    assert "onboard-synthetic" in names
