"""Tests for the routing doctor (``verify_model_routing``).

The doctor is the guardrail for the failure mode that actually shipped
silently in September 2026: agent pins lived in a config section no reader
touched, under agent names that no longer existed, while every agent ran
the global default. These tests pin the audit contract: a healthy table
reports clean, and each drift class (stale agent name, rotated model
target, missing global, missing summarizer) is reported as an actionable
problem.
"""

import configparser

import pytest

from spruce_grove.command_line.onboarding_synthetic import verify_model_routing

CATALOG = {
    "syn:large:text": {},
    "syn:small:text": {},
    "hf:zai-org/GLM-5.3-Flash": {},
}

AGENTS = {"spruce-grove": object(), "web-retriever": object()}


@pytest.fixture(autouse=True)
def _patch_environment(monkeypatch):
    monkeypatch.setattr(
        "spruce_grove.model_factory.ModelFactory.load_config",
        staticmethod(lambda: dict(CATALOG)),
    )
    monkeypatch.setattr(
        "spruce_grove.agents.agent_manager.get_available_agents",
        lambda: dict(AGENTS),
    )


def _write_config(**items: str) -> None:
    from spruce_grove import config as cp_config

    parser = configparser.ConfigParser()
    parser["grove"] = items
    with open(cp_config.CONFIG_FILE, "w", encoding="utf-8") as f:
        parser.write(f)


def test_healthy_routing_table_reports_no_problems():
    _write_config(
        model="syn:large:text",
        summarization_model="hf:zai-org/GLM-5.3-Flash",
        **{
            "agent_model_spruce-grove": "syn:large:text",
            "agent_model_web-retriever": "syn:small:text",
        },
    )
    report = verify_model_routing()
    assert report["global"] == "syn:large:text"
    assert report["summarizer"] == "hf:zai-org/GLM-5.3-Flash"
    assert report["pins"] == [
        {"agent": "spruce-grove", "model": "syn:large:text"},
        {"agent": "web-retriever", "model": "syn:small:text"},
    ]
    assert report["problems"] == []


def test_stale_agent_name_is_flagged():
    _write_config(**{"agent_model_junto": "syn:large:text"})
    report = verify_model_routing()
    stale = [p for p in report["problems"] if "agent_model_junto" in p]
    assert stale and "no such agent" in stale[0]


def test_rotated_model_target_is_flagged():
    _write_config(**{"agent_model_web-retriever": "hf:zai-org/GLM-5.2"})
    report = verify_model_routing()
    rotated = [p for p in report["problems"] if "GLM-5.2" in p]
    assert rotated and "not in the catalog" in rotated[0]


def test_missing_global_model_is_flagged(monkeypatch):
    monkeypatch.setattr(
        "spruce_grove.model_factory.ModelFactory.load_config",
        staticmethod(lambda: {}),
    )
    _write_config()
    report = verify_model_routing()
    assert report["global"] is None
    assert any("no global model configured" in p for p in report["problems"])


def test_missing_summarizer_model_is_flagged():
    _write_config(model="syn:large:text", summarization_model="hf:gone/model")
    report = verify_model_routing()
    assert any("summarization_model" in p for p in report["problems"])
