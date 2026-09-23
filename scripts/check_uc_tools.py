"""Report and repair the Universal Constructor tools location.

The third-party UC plugin hard-codes ``USER_UC_DIR`` at
``~/.code_puppy/plugins/universal_constructor``. Grove cannot edit that
constant (it is dependency code; vendoring is tracked as ladder item 9), so
grove owns the data and bridges the legacy path with a symlink:

    canonical: ~/.spruce_grove/lib/universal_constructor
    bridge:    ~/.code_puppy/plugins/universal_constructor -> canonical

This script reports the relationship and, with ``--repair``, moves tools
into grove and re-creates the bridge. Repair never deletes tools: it refuses
when both paths hold real files and leaves a backup directory on any move.

Usage:
    uv run python scripts/check_uc_tools.py
    uv run python scripts/check_uc_tools.py shell_run
    uv run python scripts/check_uc_tools.py --repair
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

CANONICAL_DIR = Path.home() / ".spruce_grove" / "lib" / "universal_constructor"
LEGACY_DIR = Path.home() / ".code_puppy" / "plugins" / "universal_constructor"
BACKUP_DIR = LEGACY_DIR.with_name(LEGACY_DIR.name + ".bak-pre-grove-migration")


def tools_in(directory: Path) -> list[Path]:
    """Tool modules directly inside ``directory`` (following symlinks)."""
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.glob("*.py") if p.name != "__init__.py")


def bridge_state() -> tuple[str, str]:
    """Return a (state, detail) pair describing the two paths."""
    canonical = tools_in(CANONICAL_DIR)
    if LEGACY_DIR.is_symlink():
        target = LEGACY_DIR.resolve()
        if target == CANONICAL_DIR.resolve():
            return "owned", "legacy path is a symlink into grove"
        return "wrong-link", f"legacy path points at {target}"
    legacy = tools_in(LEGACY_DIR)
    if not legacy and not canonical:
        return "absent", "no UC tools in either location"
    if legacy and not canonical:
        return "drifted", f"{len(legacy)} tool(s) still only in the code_puppy path"
    if legacy and canonical:
        return "split", "both paths hold tools; merge manually first"
    return "canonical-only", f"{len(canonical)} tool(s) in grove; legacy not bridged"


def repair() -> int:
    state, detail = bridge_state()
    print(f"state: {state} ({detail})")
    if state in {"owned", "absent"}:
        return 0
    if state == "split":
        print(f"refusing: merge {LEGACY_DIR} into {CANONICAL_DIR} first")
        return 1
    if state == "drifted":
        CANONICAL_DIR.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(LEGACY_DIR, CANONICAL_DIR)
        print(f"copied tools to {CANONICAL_DIR}")
        if BACKUP_DIR.exists():
            print(f"backup already present: {BACKUP_DIR}")
        else:
            LEGACY_DIR.rename(BACKUP_DIR)
            print(f"legacy directory moved to {BACKUP_DIR}")
        shutil.rmtree(LEGACY_DIR, ignore_errors=True)
    if not LEGACY_DIR.parent.is_dir():
        print(f"{LEGACY_DIR.parent} absent; no bridge needed")
        return 0
    if LEGACY_DIR.is_symlink():
        LEGACY_DIR.unlink()
    elif LEGACY_DIR.exists():
        print(f"unexpected real directory at {LEGACY_DIR}; not touching it")
        return 1
    LEGACY_DIR.symlink_to(CANONICAL_DIR)
    print(f"bridged {LEGACY_DIR} -> {CANONICAL_DIR}")
    return 0


def provider_tools() -> tuple[Path | None, set[str]]:
    from spruce_grove.plugins import load_plugin_callbacks

    load_plugin_callbacks()
    from spruce_grove.universal_constructor_provider import (
        get_universal_constructor_provider,
    )

    provider = get_universal_constructor_provider()
    if provider is None:
        return None, set()
    names = set()
    for info in provider.list_tools():
        meta = getattr(info, "meta", None)
        names.add(getattr(meta, "name", None) or str(info))
    return provider.tools_dir, names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="tool names to verify")
    parser.add_argument("--repair", action="store_true", help="relocate + bridge")
    args = parser.parse_args()

    print(f"canonical: {CANONICAL_DIR}")
    print(f"legacy:    {LEGACY_DIR}")
    state, detail = bridge_state()
    print(f"state:     {state} ({detail})")
    if args.repair:
        return repair()

    tools_dir, names = provider_tools()
    if tools_dir is None:
        print("no Universal Constructor provider registered")
        return 1
    print(f"plugin tools_dir: {tools_dir}")
    print(f"tools ({len(names)}):")
    for name in sorted(names):
        print(f"  {name}")
    if not args.names:
        return 0 if state in {"owned", "canonical-only"} else 1
    missing = [n for n in args.names if n not in names]
    for name in args.names:
        print(f"  {name}: {'FOUND' if name in names else 'MISSING'}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
