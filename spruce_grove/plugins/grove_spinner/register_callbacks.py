"""Install the grove spinner art into the third-party plugin's extension point."""

from __future__ import annotations

import logging
from pathlib import Path

from spruce_grove import spinner_art
from spruce_grove.callbacks import register_callback

logger = logging.getLogger(__name__)

#: The key the third-party plugin reads to decide the active spinner.
_STYLE_KEY = "spinner_style"


class _NotAnObject(Exception):
    """Sentinel: spinners.json parsed to something other than a JSON object."""


def spinners_file() -> Path:
    """The user-spinner file the third-party plugin loads.

    Owned by grove's config dir (the plugin resolves it through
    ``spruce_grove.config``, which ``code_puppy.config`` aliases to), so this
    is the same file the plugin reads -- not a parallel copy.
    """
    from spruce_grove.config import CONFIG_DIR

    return Path(CONFIG_DIR) / "spinners.json"


def seed_spinner_art() -> bool:
    """Add grove's spinners to the user file. Returns True when it wrote.

    Additive by construction: an entry that already exists is left exactly as
    it is, so a user's edit to ``grove``/``groveGrowth`` survives, and every
    other name in the file is untouched.

    Uses the same locked read-modify-write the plugin does
    (:func:`spruce_grove.atomic_json.mutate_json`), so a concurrent write from
    the picker cannot tear the file.
    """
    from spruce_grove import atomic_json

    path = spinners_file()
    wrote = False

    def _add_missing(current):
        nonlocal wrote
        if not isinstance(current, dict):
            raise _NotAnObject()
        for name, spec in spinner_art.SPINNERS.items():
            if name in current:
                continue  # never overwrite an entry the user may have tuned
            current[name] = dict(spec)
            wrote = True
        return current

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_json.mutate_json(str(path), _add_missing, default={})
    except _NotAnObject:
        logger.warning("not seeding spinner art: %s is not a JSON object", path)
        return False
    except (OSError, atomic_json.JsonFileCorrupt) as exc:
        # A file we cannot parse is a file we must not clobber: the user may be
        # mid-edit, and the plugin will warn about it on its own.
        logger.warning("not seeding spinner art: %s is unreadable (%s)", path, exc)
        return False
    return wrote


def seat_grove_default() -> bool:
    """Make the grove spinner active, but only when nothing is chosen yet.

    A user who has already chosen a spinner has made a decision; re-seating on
    every launch would silently undo it. So this writes only when the key is
    unset or blank, and never calls ``set_value`` otherwise.
    """
    from spruce_grove.config import get_value, set_value

    try:
        current = get_value(_STYLE_KEY)
    except Exception:  # config must never break startup
        return False
    if current and current.strip():
        return False

    try:
        set_value(_STYLE_KEY, spinner_art.DEFAULT_GROVE_SPINNER)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("could not seat the grove spinner: %s", exc)
        return False
    return True


def install() -> None:
    """Seed the art and seat it as the default. Never raises.

    Both halves are independent: seeding can succeed while seating is skipped
    (the user already has a pick), and art that fails to write leaves the
    existing spinner alone.
    """
    try:
        if seed_spinner_art():
            logger.info("grove spinner art seeded into %s", spinners_file())
        seat_grove_default()
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("grove spinner install failed: %s", exc)


def _on_startup() -> None:
    """Run once at boot, before the status bar starts spinning."""
    install()


register_callback("startup", _on_startup)
