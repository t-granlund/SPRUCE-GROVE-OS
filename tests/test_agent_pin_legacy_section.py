"""Tests for agent model pins and the legacy ``[agents]`` section dual-read.

Pins live in ``[grove]`` — that is where every setter writes them. Hand-edited
configs have historically placed ``agent_model_*`` keys under an ``[agents]``
section that nothing read, so those pins silently fell through to the global
default (one subscription model for every task — exactly the drift the
TASK-001 routing plan was written to prevent). These tests pin the dual-load
contract: legacy pins are honored, ``[grove]`` wins conflicts, warnings fire
once, and clearing a pin removes it from BOTH sections.
"""

import configparser
import logging

import pytest

from spruce_grove import config as cp_config


def _write_config(sections: dict[str, dict[str, str]]) -> None:
    parser = configparser.ConfigParser()
    for section, items in sections.items():
        parser[section] = items
    with open(cp_config.CONFIG_FILE, "w", encoding="utf-8") as f:
        parser.write(f)


@pytest.fixture(autouse=True)
def _reset_legacy_warnings():
    cp_config._legacy_pin_warnings.clear()
    yield
    cp_config._legacy_pin_warnings.clear()


class TestGroveSectionPins:
    def test_pin_in_grove_section_is_read(self):
        _write_config({"grove": {"agent_model_spruce-grove": "syn:large:text"}})
        assert cp_config.get_agent_pinned_model("spruce-grove") == "syn:large:text"

    def test_missing_pin_returns_none(self):
        _write_config({"grove": {}})
        assert cp_config.get_agent_pinned_model("helios") is None


class TestLegacyAgentsSection:
    def test_legacy_pin_is_honored_with_warning(self, caplog):
        _write_config({"agents": {"agent_model_web-retriever": "syn:small:text"}})
        with caplog.at_level(logging.WARNING, logger="spruce_grove.config"):
            assert cp_config.get_agent_pinned_model("web-retriever") == "syn:small:text"
        assert any("[agents]" in r.message for r in caplog.records)

    def test_legacy_warning_fires_once_per_agent(self, caplog):
        _write_config({"agents": {"agent_model_web-retriever": "syn:small:text"}})
        with caplog.at_level(logging.WARNING, logger="spruce_grove.config"):
            cp_config.get_agent_pinned_model("web-retriever")
            cp_config.get_agent_pinned_model("web-retriever")
        warnings = [r for r in caplog.records if "[agents]" in r.message]
        assert len(warnings) == 1

    def test_grove_section_wins_on_conflict(self, caplog):
        _write_config(
            {
                "grove": {"agent_model_helios": "syn:large:text"},
                "agents": {"agent_model_helios": "syn:small:text"},
            }
        )
        with caplog.at_level(logging.WARNING, logger="spruce_grove.config"):
            assert cp_config.get_agent_pinned_model("helios") == "syn:large:text"
        # No warning when the canonical location already answers.
        assert not [r for r in caplog.records if "[agents]" in r.message]

    def test_empty_legacy_value_is_not_a_pin(self):
        _write_config({"agents": {"agent_model_helios": ""}})
        assert cp_config.get_agent_pinned_model("helios") is None


class TestListingAndClearing:
    def test_listing_merges_both_sections_grove_wins(self):
        _write_config(
            {
                "grove": {"agent_model_helios": "syn:large:text"},
                "agents": {
                    "agent_model_helios": "syn:small:text",
                    "agent_model_web-retriever": "syn:small:text",
                },
            }
        )
        pins = cp_config.get_all_agent_pinned_models()
        assert pins == {
            "helios": "syn:large:text",
            "web-retriever": "syn:small:text",
        }

    def test_clear_removes_legacy_pin_no_resurrection(self):
        _write_config(
            {"grove": {}, "agents": {"agent_model_qa-kitten": "syn:large:text"}}
        )
        cp_config.clear_agent_pinned_model("qa-kitten")
        assert cp_config.get_agent_pinned_model("qa-kitten") is None
        # And the legacy section no longer carries the pin at all.
        parser = configparser.ConfigParser()
        parser.read(cp_config.CONFIG_FILE)
        assert "agent_model_qa-kitten" not in parser["agents"]

    def test_clear_on_missing_pin_is_a_noop(self):
        _write_config({"grove": {}})
        cp_config.clear_agent_pinned_model("nobody")
        assert cp_config.get_agent_pinned_model("nobody") is None
