"""Self-update: the grove tends itself.

When startup's version check finds a newer published release, this module
upgrades the on-disk installation in place via ``uv tool upgrade``. The
running session keeps its warm, fully-loaded, internally-consistent code;
the next launch boots the new version. No restart is forced and no
mid-session imports are swapped, so an active chat never breaks under an
upgrade.

Escape hatches:
- ``NO_VERSION_UPDATE`` (existing): disables the whole version check.
- ``NO_AUTO_UPDATE``: keeps the check, but never actuates.
Manual pin-back at any time: ``uv tool install spruce-grove==X.Y.Z``.
"""

import os
import shutil
import subprocess
from pathlib import Path

from spruce_grove.i18n import t
from spruce_grove.messaging import emit_info, emit_success, emit_warning

PACKAGE_NAME = "spruce-grove"
UPGRADE_TIMEOUT_SECONDS = 180.0

_TRUTHY = ("1", "true", "yes", "on")


def auto_update_disabled() -> bool:
    """True when NO_AUTO_UPDATE opts this process out of actuation."""
    return os.getenv("NO_AUTO_UPDATE", "").lower() in _TRUTHY


def _running_from_uv_tool() -> bool:
    """Best-effort check that this installation is a uv-managed tool env.

    Editable/source checkouts must never be ``uv tool upgrade``-d: that
    would silently replace a developer's live dev environment with a PyPI
    wheel. The uv tool env path always contains ``.../uv/tools/<name>/...``.
    """
    try:
        parts = Path(__file__).resolve().parts
    except Exception:  # pragma: no cover - defensive, __file__ always exists
        return False
    return "uv" in parts and "tools" in parts


def self_update_supported() -> bool:
    """Actuation needs the uv binary and a uv-managed installation."""
    return shutil.which("uv") is not None and _running_from_uv_tool()


def perform_self_update(current_version, latest_version) -> bool:
    """Upgrade the on-disk install toward ``latest_version``. Never raises.

    Returns True when the upgrade command succeeded. Designed to run on the
    startup daemon thread: the current process is never restarted, blocked,
    or left waiting on exit (daemon threads are not joined).
    """
    if auto_update_disabled():
        emit_info(t("version.self_update_disabled", current=current_version))
        return False
    if not self_update_supported():
        emit_warning(t("version.self_update_skipped", reason="not a uv-managed install"))
        return False

    emit_info(
        t("version.self_update_started", current=current_version, latest=latest_version)
    )
    try:
        result = subprocess.run(
            ["uv", "tool", "upgrade", PACKAGE_NAME],
            capture_output=True,
            text=True,
            timeout=UPGRADE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        emit_warning(t("version.self_update_failed", error=e))
        return False

    if result.returncode != 0:
        lines = (result.stderr or result.stdout or "").strip().splitlines()
        detail = lines[-1] if lines else f"exit code {result.returncode}"
        emit_warning(t("version.self_update_failed", error=detail))
        return False

    emit_success(
        t("version.self_updated", current=current_version, latest=latest_version)
    )
    return True
