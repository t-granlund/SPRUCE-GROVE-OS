"""Self-update: the grove tends itself.

When the version check finds a newer published release, this module upgrades
the on-disk installation via ``uv tool upgrade``. **Actuation is deferred to
process exit** so a running session never has its code swapped underneath it.

Why the deferral matters: the grove imports tool modules *lazily*, at the
moment an agent first needs them (``spruce_grove/tools/_lazy.py``). Upgrading
mid-session replaces those files on disk while the process still holds the old
module table, so the next lazy import half-mixes two versions — the failure
mode behind the 2026-09 stale-module incident. Deferring to exit removes the
hazard entirely: the code on disk only changes once nothing is importing from
it. The disk is still fresh for the next launch, so the self-heal holds.

Escape hatches:
- ``NO_VERSION_UPDATE`` (existing): disables the whole version check.
- ``NO_AUTO_UPDATE``: keeps the check, but never actuates.
- ``SPRUCE_GROVE_UPDATE_AT_EXIT``: ``0`` disables the exit-time actuation.
Manual pin-back at any time: ``uv tool install spruce-grove==X.Y.Z``.
"""

import logging
import os
import shutil
import subprocess
from pathlib import Path

from spruce_grove.i18n import t
from spruce_grove.messaging import emit_info, emit_success, emit_warning

logger = logging.getLogger(__name__)

PACKAGE_NAME = "spruce-grove"
UPGRADE_TIMEOUT_SECONDS = 180.0

#: Exit-time budget for actuation. The process is on its way out, so the wait
#: is user-visible: a publish is seconds, and a miss just defers to next launch.
EXIT_UPGRADE_TIMEOUT_SECONDS = 60.0

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


def update_at_exit_disabled() -> bool:
    """True when SPRUCE_GROVE_UPDATE_AT_EXIT opts out of exit-time actuation."""
    return os.getenv("SPRUCE_GROVE_UPDATE_AT_EXIT", "").lower() in (
        "0",
        "false",
        "no",
        "off",
    )


def _run_upgrade(timeout: float) -> tuple[bool, str]:
    """Run ``uv tool upgrade``. Returns (ok, detail). Never raises."""
    try:
        result = subprocess.run(
            ["uv", "tool", "upgrade", PACKAGE_NAME],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout:.0f}s"
    except OSError as e:
        return False, str(e)

    if result.returncode != 0:
        lines = (result.stderr or result.stdout or "").strip().splitlines()
        return False, (lines[-1] if lines else f"exit code {result.returncode}")
    return True, ""


def perform_self_update(
    current_version, latest_version, *, defer_to_exit: bool = False
) -> bool:
    """Upgrade the on-disk install toward ``latest_version``. Never raises.

    Returns True when the upgrade command succeeded. Guards (disabled,
    unsupported install) are checked here regardless of mode, so a caller
    never schedules an upgrade that could not run.

    ``defer_to_exit=False`` (default) runs the upgrade inline -- the shape the
    tests exercise.

    ``defer_to_exit=True`` runs it now *only when this process owns the
    console*. That is the load-bearing detail: when the grove drives a TUI
    (the desktop shell) stdin is a pipe, so the process is a child and cannot
    modify its own live installation safely or without the parent seeing the
    console change. In that mode we report and let the owning process do the
    upgrade; a bare interactive session owns the console and defers the work
    to exit via :func:`run_deferred_update`.
    """
    if auto_update_disabled():
        emit_info(t("version.self_update_disabled", current=current_version))
        return False
    try:
        supported = self_update_supported()
    except Exception as e:
        emit_warning(t("version.self_update_failed", error=e))
        return False
    if not supported:
        emit_warning(
            t("version.self_update_skipped", reason="not a uv-managed install")
        )
        return False

    if defer_to_exit:
        import sys

        owns_console = sys.stdin is not None and sys.stdin.isatty()
        if not owns_console:
            # A parent (the desktop shell) owns this process. It can upgrade
            # the install cleanly after we exit; we only report.
            emit_info(
                t(
                    "version.self_update_deferred_parent",
                    current=current_version,
                    latest=latest_version,
                )
            )
            return False
        mark_pending_update(
            current_version, latest_version, timeout=EXIT_UPGRADE_TIMEOUT_SECONDS
        )
        emit_info(
            t(
                "version.self_update_deferred_exit",
                current=current_version,
                latest=latest_version,
            )
        )
        return True

    emit_info(
        t("version.self_update_started", current=current_version, latest=latest_version)
    )
    ok, detail = _run_upgrade(UPGRADE_TIMEOUT_SECONDS)
    if not ok:
        emit_warning(t("version.self_update_failed", error=detail))
        return False

    emit_success(
        t("version.self_updated", current=current_version, latest=latest_version)
    )
    return True


# --- Deferred (exit-time) actuation -----------------------------------------
# A pending upgrade is stashed in the process environment rather than a file:
# it is per-process by nature, needs no cleanup, and cannot leave stale state
# on disk for the NEXT launch to trip over.

_PENDING_KEY = "_SPRUCE_GROVE_PENDING_UPDATE"
_PENDING_TIMEOUT_KEY = "_SPRUCE_GROVE_PENDING_UPDATE_TIMEOUT"

#: Separator for the two versions. Environment values may not contain NUL, and
#: a version string is digits and dots, so a pipe can never collide.
_PENDING_SEP = "|"


def mark_pending_update(
    current_version: str, latest_version: str, timeout: float
) -> None:
    """Record an upgrade to run at exit. Safe to call more than once."""
    os.environ[_PENDING_KEY] = f"{current_version}{_PENDING_SEP}{latest_version}"
    os.environ[_PENDING_TIMEOUT_KEY] = str(timeout)


def pending_update() -> tuple[str, str] | None:
    """The (current, latest) pair stashed for exit, or None."""
    raw = os.environ.get(_PENDING_KEY)
    if not raw or _PENDING_SEP not in raw:
        return None
    current, latest = raw.split(_PENDING_SEP, 1)
    return current, latest


def run_deferred_update() -> bool:
    """Run any stashed upgrade. Never raises; a no-op when nothing is pending.

    Called on the exit path, where a failure must never turn a clean shutdown
    into a noisy one -- so every branch reports and returns.
    """
    pending = pending_update()
    if pending is None:
        return False
    current_version, latest_version = pending
    # Clear first: a second entry point must not double-run the upgrade.
    os.environ.pop(_PENDING_KEY, None)
    raw_timeout = os.environ.pop(_PENDING_TIMEOUT_KEY, None)

    try:
        timeout = float(raw_timeout) if raw_timeout else EXIT_UPGRADE_TIMEOUT_SECONDS
    except ValueError:
        timeout = EXIT_UPGRADE_TIMEOUT_SECONDS

    if auto_update_disabled() or update_at_exit_disabled():
        logger.info("deferred self-update skipped by environment")
        return False
    try:
        if not self_update_supported():
            return False
    except Exception:  # pragma: no cover - defensive
        return False

    ok, detail = _run_upgrade(timeout)
    if not ok:
        # Robustness valve: land the message in the log, which always exists
        # on disk, rather than the message bus, which may already be torn down.
        logger.warning(
            "deferred self-update failed (%s); update manually with: "
            "uv tool upgrade %s",
            detail,
            PACKAGE_NAME,
        )
        return False

    logger.info(
        "deferred self-update complete: %s -> %s (%s)",
        current_version,
        latest_version,
        PACKAGE_NAME,
    )
    return True
