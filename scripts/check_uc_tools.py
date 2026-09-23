"""Report the Universal Constructor tool directory and what lives there.

Useful after moving UC tools or when an agent pins a UC tool that no longer
resolves. Pass tool names as arguments to check them individually.

Usage:
    uv run python scripts/check_uc_tools.py
    uv run python scripts/check_uc_tools.py shell_run jobapp_ledger
"""

from __future__ import annotations

import sys


def uc_tool_names() -> set[str]:
    from spruce_grove.plugins import load_plugin_callbacks

    load_plugin_callbacks()
    from spruce_grove.universal_constructor_provider import (
        get_universal_constructor_provider,
    )

    provider = get_universal_constructor_provider()
    names: set[str] = set()
    if provider is None:
        return names
    for info in provider.list_tools():
        meta = getattr(info, "meta", None)
        names.add(getattr(meta, "name", None) or str(info))
    return names


def main() -> int:
    from spruce_grove.plugins import load_plugin_callbacks

    load_plugin_callbacks()
    from spruce_grove.universal_constructor_provider import (
        get_universal_constructor_provider,
    )

    provider = get_universal_constructor_provider()
    if provider is None:
        print("no Universal Constructor provider registered")
        return 1

    print(f"tools_dir: {provider.tools_dir}")
    names = uc_tool_names()
    print(f"tools: {len(names)}")
    for name in sorted(names):
        print(f"  {name}")

    wanted = sys.argv[1:]
    if not wanted:
        return 0
    missing = [name for name in wanted if name not in names]
    for name in wanted:
        print(f"  {name}: {'FOUND' if name in names else 'MISSING'}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
