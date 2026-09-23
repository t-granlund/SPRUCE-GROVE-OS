"""Port JSON agents from a legacy code_puppy install into grove.

Reads agent definitions from ``~/.code_puppy/agents`` (override with
``--source``) and writes grove-native copies to ``~/.spruce_grove/agents``
(override with ``--dest``). Dry run by default; pass ``--apply`` to write.

Rewrites only ties to code_puppy *the product*:

* ``~/<dot>code_puppy`` paths and ``<dot>code_puppy/`` path segments,
* references to the generalist agent (``code-puppy`` -> ``spruce-grove``),
* references to the web agent (``web-puppy`` -> ``web-retriever``),
* trailing whitespace in ``display_name``.

A rule is skipped for any file whose own agent name it would rewrite, so an
agent keeps its identity (``web-puppy.json`` is not renamed to itself's
twin). Trailing ``.bak`` files are ignored.

Usage:
    uv run python scripts/port_code_puppy_agents.py
    uv run python scripts/port_code_puppy_agents.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DEFAULT_SOURCE = Path.home() / ".code_puppy" / "agents"
DEFAULT_DEST = Path.home() / ".spruce_grove" / "agents"

# Order matters: path rules must run before the bare agent-name rules, or
# ``~/.code_puppy/x`` would become ``~/.spruce-grove/x``.
RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"~/\.code_puppy"), "~/.spruce_grove"),
    (re.compile(r"\.code_puppy/"), ".spruce_grove/"),
    (re.compile(r"\bcode[-_ ]puppy\b", re.I), "spruce-grove"),
    (re.compile(r"\bweb[-_ ]puppy\b", re.I), "web-retriever"),
]


def own_rule_indices(agent_name: str) -> set[int]:
    """Rules that would rewrite the agent's own name, and so are skipped."""
    return {i for i, (pattern, _) in enumerate(RULES) if pattern.search(agent_name)}


def rewrite(text: str, log: list[str], where: str, skip: set[int]) -> str:
    for index, (pattern, replacement) in enumerate(RULES):
        if index in skip:
            continue
        for match in sorted(set(pattern.findall(text))):
            log.append(f"      {where}: {match!r} -> {replacement!r}")
        text = pattern.sub(replacement, text)
    return text


def walk(value: object, path: str, log: list[str], skip: set[int]) -> object:
    if isinstance(value, str):
        return rewrite(value, log, path, skip)
    if isinstance(value, list):
        return [walk(v, f"{path}[{i}]", log, skip) for i, v in enumerate(value)]
    if isinstance(value, dict):
        return {k: walk(v, f"{path}.{k}", log, skip) for k, v in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write migrated agents (default is a dry run)",
    )
    args = parser.parse_args()

    files = sorted(p for p in args.source.glob("*.json") if ".bak" not in p.name)
    if not files:
        print(f"no agent JSON files under {args.source}")
        return 1

    print(
        f"source: {args.source}\n"
        f"dest:   {args.dest}\n"
        f"mode:   {'APPLY' if args.apply else 'DRY RUN'}\n"
    )
    if args.apply:
        args.dest.mkdir(parents=True, exist_ok=True)

    for path in files:
        data = json.loads(path.read_text())
        log: list[str] = []
        skip = own_rule_indices(str(data.get("name", "")))
        migrated = walk(data, path="", log=log, skip=skip)
        assert isinstance(migrated, dict)

        display_name = migrated.get("display_name")
        if isinstance(display_name, str) and display_name != display_name.strip():
            migrated["display_name"] = display_name.strip()
            log.append("      .display_name: stripped trailing whitespace")

        print(f"[{migrated.get('name', path.stem)}]  ({path.name})")
        if skip:
            print("      own-name rules skipped (agent keeps its identity)")
        for line in log or ["      (no changes)"]:
            print(line)

        if args.apply:
            (args.dest / path.name).write_text(
                json.dumps(migrated, indent=2, ensure_ascii=True) + "\n"
            )

    if args.apply:
        print(f"\nwrote {len(files)} agent file(s) to {args.dest}")
    else:
        print("\ndry run — re-run with --apply to write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
