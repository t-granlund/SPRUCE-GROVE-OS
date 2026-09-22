"""Tests for the one-time ``puppy.cfg`` -> ``grove.cfg`` migration.

The rebrand renamed the config file in code but never moved the file on
disk: users upgraded from the Code Puppy era kept their whole curated
config in ``puppy.cfg`` while every supported version read a ``grove.cfg``
that did not exist. These tests pin the migration contract: copy once when
``grove.cfg`` is absent, never overwrite an existing ``grove.cfg``, keep
the legacy file as a backup, and never re-prompt when the migrated config
already carries the required keys.
"""

import configparser
import os


from spruce_grove import config as cp_config

PUPPY_CONTENT = """[grove]
grove_name = Junto
owner_name = Tyler
model = syn:large:text
agent_model_web-retriever = syn:small:text

[agents]
# legacy section kept for structure
"""


def _write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _read_parser(path: str) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    parser.read(path)
    return parser


def _forbid_prompts(monkeypatch) -> None:
    def _boom(*_args, **_kwargs):
        raise AssertionError("ensure_config_exists prompted — migration failed")

    monkeypatch.setattr("builtins.input", _boom)


def test_missing_grove_cfg_with_legacy_puppy_cfg_migrates(monkeypatch):
    _forbid_prompts(monkeypatch)
    _write(os.path.join(cp_config.CONFIG_DIR, "puppy.cfg"), PUPPY_CONTENT)

    config = cp_config.ensure_config_exists()

    assert os.path.isfile(cp_config.CONFIG_FILE)
    migrated = _read_parser(cp_config.CONFIG_FILE)
    assert migrated["grove"]["grove_name"] == "Junto"
    assert migrated["grove"]["model"] == "syn:large:text"
    assert config["grove"]["grove_name"] == "Junto"
    # The legacy file stays on disk untouched as a backup.
    assert os.path.isfile(os.path.join(cp_config.CONFIG_DIR, "puppy.cfg"))
    # And the migrated pin resolves through the real reader.
    assert cp_config.get_agent_pinned_model("web-retriever") == "syn:small:text"


def test_existing_grove_cfg_is_never_overwritten(monkeypatch):
    _forbid_prompts(monkeypatch)
    grove_path = cp_config.CONFIG_FILE
    _write(grove_path, "[grove]\ngrove_name = Existing\nowner_name = Keeper\n")
    _write(os.path.join(cp_config.CONFIG_DIR, "puppy.cfg"), PUPPY_CONTENT)
    before = open(grove_path, encoding="utf-8").read()

    cp_config.ensure_config_exists()

    assert open(grove_path, encoding="utf-8").read() == before


def test_fresh_install_without_legacy_file_still_prompts(monkeypatch):
    answers = iter(["FreshGrove", "Keeper"])

    def _fake_input(_prompt: str = "") -> str:
        return next(answers)

    monkeypatch.setattr("builtins.input", _fake_input)

    config = cp_config.ensure_config_exists()

    assert config["grove"]["grove_name"] == "FreshGrove"
    assert os.path.isfile(cp_config.CONFIG_FILE)
