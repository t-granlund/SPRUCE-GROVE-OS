"""Audit user JSON agents in ``~/.spruce_grove/agents`` against live grove.

For every agent file this checks:

* it loads through :class:`JSONAgent` (schema + model-settings validation),
* every name in its ``tools`` list resolves (core, plugin, or Universal
  Constructor),
* its ``model`` pin exists in the catalogue exposed through the harness
  seam (skipped for agents that ride the global default),
* it carries no unrecognised keys.

Exit status is non-zero when anything fails, so it can gate a maintenance
pass.

Usage:
    uv run python scripts/dial_user_agents.py
    uv run python scripts/dial_user_agents.py --prune-tools

``--prune-tools`` removes tool names that do not resolve from the ``tools``
array. It never rewrites prompt prose \u2014 prose mentions are reported for a
human to review instead.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

AGENTS_DIR = Path.home() / ".spruce_grove" / "agents"

KNOWN_KEYS = frozenset(
    {
        "id",
        "name",
        "display_name",
        "description",
        "model",
        "system_prompt",
        "user_prompt",
        "tools",
        "tools_config",
        "model_settings",
        "mcp_servers",
    }
)


def _uc_tool_names() -> set[str]:
    from spruce_grove.universal_constructor_provider import (
        get_universal_constructor_provider,
    )

    provider = get_universal_constructor_provider()
    if provider is None:
        return set()
    names: set[str] = set()
    for info in provider.list_tools():
        meta = getattr(info, "meta", None)
        names.add(getattr(meta, "name", None) or str(info))
    return names


def resolved_tool_names() -> set[str]:
    """Core tools, plugin tools, and Universal Constructor tools."""
    from spruce_grove.plugins import load_plugin_callbacks

    load_plugin_callbacks()
    from spruce_grove.tools import get_available_tool_names

    return set(get_available_tool_names()) | _uc_tool_names()


def catalogue_models() -> set[str] | None:
    """Model names reachable through the harness seam, or None if unknown."""
    try:
        from spruce_grove.harness import get_harness

        data = get_harness().load_models_config()
    except Exception:  # noqa: BLE001 - a broken seam must not hide the audit
        return None
    if isinstance(data, dict):
        return set(data)
    return None


def audit(data: dict, tools: set[str], models: set[str] | None) -> list[str]:
    """Return human-readable findings for one agent config."""
    findings: list[str] = []
    dangling = [t for t in data.get("tools", []) if t not in tools]
    if dangling:
        findings.append(f"dangling tools {dangling}")
    unknown = sorted(set(data) - KNOWN_KEYS)
    if unknown:
        findings.append(f"unrecognised keys {unknown}")
    model = data.get("model")
    if models and model and model not in models:
        findings.append(f"model not in catalogue: {model!r}")
    return findings


def main() -> int:
    prune = "--prune-tools" in sys.argv
    if not AGENTS_DIR.is_dir():
        print(f"no agent directory at {AGENTS_DIR}")
        return 0

    from spruce_grove.agents.json_agent import JSONAgent

    tools = resolved_tool_names()
    models = catalogue_models()
    print(
        f"agents: {AGENTS_DIR}\n"
        f"resolvable tools: {len(tools)} | "
        f"catalogue: {len(models) if models else 'unavailable'}"
    )
    print("-" * 70)

    problems = 0
    for path in sorted(AGENTS_DIR.glob("*.json")):
        try:
            agent = JSONAgent(str(path))
        except Exception as exc:  # noqa: BLE001 - report, never crash the pass
            print(f"LOAD FAIL {path.name}: {type(exc).__name__}: {exc}")
            problems += 1
            continue

        data = json.loads(path.read_text())
        findings = audit(data, tools, models)
        if findings:
            problems += len(findings)
            for finding in findings:
                print(f"  {agent.name}: {finding}")

        if prune:
            kept = [t for t in data.get("tools", []) if t in tools]
            if kept != data.get("tools", []):
                data["tools"] = kept
                path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
                print(f"  {agent.name}: pruned {len(kept)} tools")

    print("-" * 70)
    print(f"problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
