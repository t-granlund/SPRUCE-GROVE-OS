"""Version checking utilities for Spruce Grove."""

import threading

import httpx

from spruce_grove.i18n import t
from spruce_grove.messaging import (
    emit_info,
    emit_success,
    emit_warning,
    get_message_bus,
)
from spruce_grove.messaging.messages import VersionCheckMessage


def normalize_version(version_str):
    if not version_str:
        return version_str
    version_str = version_str.lstrip("v")
    return version_str


def _version_tuple(version_str):
    """Convert version string to tuple of ints for proper comparison."""
    try:
        return tuple(int(x) for x in version_str.split("."))
    except (ValueError, AttributeError):
        return None


def version_is_newer(latest, current):
    """Return True if latest version is strictly newer than current."""
    latest_tuple = _version_tuple(normalize_version(latest))
    current_tuple = _version_tuple(normalize_version(current))
    if latest_tuple is None or current_tuple is None:
        return False
    return latest_tuple > current_tuple


def versions_are_equal(current, latest):
    current_norm = normalize_version(current)
    latest_norm = normalize_version(latest)
    # Try numeric tuple comparison first
    current_tuple = _version_tuple(current_norm)
    latest_tuple = _version_tuple(latest_norm)
    if current_tuple is not None and latest_tuple is not None:
        return current_tuple == latest_tuple
    # Fallback to string comparison
    return current_norm == latest_norm


def fetch_latest_version(package_name):
    try:
        response = httpx.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5.0)
        response.raise_for_status()
        data = response.json()
        return data["info"]["version"]
    except Exception as e:
        emit_warning(t("version.fetch_failed", error=e))
        return None


def _maybe_self_update(current_version, latest_version) -> None:
    """Close the self-heal loop: schedule the upgrade, best-effort, never raise.

    Runs on the startup daemon thread after the status messages land, so the
    user sees what is happening and startup is never blocked. Actuation is
    requested with ``defer_to_exit=True``: the upgrade must not touch the disk
    while this process can still lazily import tool modules, which is exactly
    how a session gets broken mid-flight. Any failure is reported and
    swallowed - a broken updater must never break a session.
    """
    try:
        from spruce_grove.self_update import perform_self_update

        perform_self_update(current_version, latest_version, defer_to_exit=True)
    except Exception as e:  # pragma: no cover - absolute last resort
        emit_warning(t("version.self_update_failed", error=e))


def default_version_mismatch_behavior(current_version) -> threading.Thread:
    """Kick off the PyPI version check without blocking startup.

    The fetch is a blocking HTTPS round-trip (up to ``timeout`` seconds on a
    bad network) that used to sit on the critical path before the first
    model request. It now runs on a daemon thread, so the result lands on
    the message bus whenever it arrives and process exit never waits for
    it. Returns the thread so callers (tests) can ``join()`` if they must.
    """
    # Defensive: ensure current_version is never None
    if current_version is None:
        current_version = "0.0.0-unknown"
        emit_warning(t("version.undetected"))

    def _check() -> None:
        latest = fetch_latest_version("spruce-grove")
        report_version_status(current_version, latest)
        if latest and version_is_newer(latest, current_version):
            _maybe_self_update(current_version, latest)

    thread = threading.Thread(target=_check, name="version-check", daemon=True)
    thread.start()
    return thread


def report_version_status(current_version, latest_version) -> None:
    """Emit the version-check messages for an already-fetched ``latest_version``."""
    update_available = bool(
        latest_version and version_is_newer(latest_version, current_version)
    )

    # Emit structured version check message
    version_msg = VersionCheckMessage(
        current_version=current_version,
        latest_version=latest_version or current_version,
        update_available=update_available,
    )
    get_message_bus().emit(version_msg)

    # Also emit plain text for legacy renderer
    emit_info(t("version.current", version=current_version))

    if update_available:
        emit_info(t("version.latest", version=latest_version))
        emit_warning(t("version.update_available", version=latest_version))
        emit_success(t("version.please_update"))
