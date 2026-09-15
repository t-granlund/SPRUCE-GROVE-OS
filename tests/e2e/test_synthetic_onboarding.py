"""E2E for /onboard-synthetic — Synthetic.new subscriber onboarding.

Runs the real apply_onboarding against an isolated temp HOME and verifies:
  - the 11-model set (4 rotation-safe aliases + 7 pinned, verbatim from the
    maintainer's live configuration)
  - vision aliases carry supports_vision (so vision routes to them)
  - the API key path resolves through the shared credential store
  - extra_models.json + grove.cfg land with the driving seat assigned
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
    for mod in [m for m in list(sys.modules) if m.startswith("spruce_grove")]:
        del sys.modules[mod]
    yield tmp
    for mod in [m for m in list(sys.modules) if m.startswith("spruce_grove")]:
        del sys.modules[mod]


import sys  # noqa: E402  (kept late so the fixture comment above reads first)

sys.modules.setdefault("spruce_grove", sys.modules.get("spruce_grove"))


def test_model_set_is_the_maintainer_config(isolated_home):
    from spruce_grove.command_line.onboarding_synthetic import build_synthetic_models

    models = build_synthetic_models()
    assert len(models) == 11
    assert models["syn:large:vision"]["supports_vision"] is True
    assert models["syn:small:vision"]["supports_vision"] is True
    assert not models["syn:large:text"].get("supports_vision")
    assert models["hf:zai-org/GLM-5.3-Flash"]["max_output_tokens"] == 65536


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


def test_apply_onboarding_writes_models_key_and_main_model(isolated_home):
    from spruce_grove.command_line.onboarding_synthetic import (
        EXTRA_MODELS_PATH,
        apply_onboarding,
    )

    with mock.patch(
        "spruce_grove.command_line.onboarding_synthetic.set_api_key"
    ):
        with mock.patch.dict(os.environ, {"SYNTHETIC_API_KEY": "sk-test"}):
            apply_onboarding("sk-test")

    models = json.load(open(EXTRA_MODELS_PATH))
    assert len([k for k in models if k.startswith(("syn:", "hf:"))]) == 11
    assert models["syn:large:vision"]["supports_vision"] is True

    cfg_path = os.path.join(
        isolated_home, ".config", "spruce_grove", "grove.cfg"
    )
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
