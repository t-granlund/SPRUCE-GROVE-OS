"""The grove's own spinner art -- braille frames that read as growth.

The runtime spinner is owned by a third-party plugin
(``code_puppy_core_plugins.puppy_spinner``) whose default is a bouncing
dog-face emoji. The grove's boot wordmark is braille, dotted, and organic;
the spinner should match it rather than contradict it. This module holds the
art, the grove installs it through the plugin's **supported extension point**
(``~/.spruce_grove/spinners.json``, which loads user spinners and lets them win
on name collision), and the plugin itself is never edited.

Why braille: one braille cell is a 2x4 dot grid, so a single character cell
carries four rows of vertical resolution. Shapes that would need four terminal
rows can therefore live on one line -- which is all a status prefix gets.

Frames are padded to a uniform display width by the plugin, so the following
text never jitters. Keep every frame within ``_MAX_FRAME_LEN`` (40 cells) and
keep the sequences here free of duplicate frames -- a repeated frame is a stall
in the animation, and :func:`validate` rejects it.
"""

from __future__ import annotations

from typing import Dict, List

# --- braille cell construction ------------------------------------------------

#: A braille cell's dots, by (column, row). Rows run downward from the top.
_LEFT_DOTS = (0x01, 0x02, 0x04, 0x40)  # dots 1, 2, 3, 7
_RIGHT_DOTS = (0x08, 0x10, 0x20, 0x80)  # dots 4, 5, 6, 8

#: The blank braille pattern (U+2800). Renders as an empty cell; used for
#: spacing so every frame in a sequence is the same width.
BLANK = "\u2800"

#: The plugin truncates frames to this many display cells; keep art under it.
MAX_FRAME_LEN = 40


def cell(left_row: int | None = None, right_row: int | None = None) -> str:
    """One braille cell with a dot at ``left_row``/``right_row`` (0 = top).

    Either argument may be None to leave that column empty.
    """
    bits = 0
    if left_row is not None:
        bits |= _LEFT_DOTS[left_row]
    if right_row is not None:
        bits |= _RIGHT_DOTS[right_row]
    return chr(0x2800 + bits)


# --- the art ------------------------------------------------------------------

#: A dot rippling along a three-cell diagonal. The literal "no straight lines"
#: read: the dot appears at the top-left, drifts down and right, and leaves.
GROVE_WAVE: List[str] = [
    cell(0) + BLANK + BLANK,
    cell(1) + cell(0) + BLANK,
    cell(2) + cell(1) + cell(0),
    cell(3) + cell(2) + cell(1),
    BLANK + cell(3) + cell(2),
    BLANK + BLANK + cell(3),
]

#: A stem rising from the soil, then a leaf opening beside it. Reads as growth
#: rather than motion, which suits the long waits.
GROVE_GROWTH: List[str] = [
    BLANK + BLANK,
    cell(3) + BLANK,
    cell(2) + BLANK,
    cell(1) + BLANK,
    cell(1) + cell(1),
    cell(0) + cell(0),
    cell(0) + cell(0, 0),
    cell(0, 0) + cell(0, 0),
]

#: name -> (frames, seconds per frame, description). ``groveGrowth`` is the
#: default: growth is what the grove is for, and it holds up at slow speeds
#: better than a ripple.
SPINNERS: Dict[str, Dict[str, object]] = {
    "grove": {
        "frames": GROVE_WAVE,
        "interval": 0.12,
        "description": "a dot rippling through the grove",
    },
    "groveGrowth": {
        "frames": GROVE_GROWTH,
        "interval": 0.14,
        "description": "a fir rising from the soil",
    },
}

#: Which grove spinner the install should default to.
DEFAULT_GROVE_SPINNER = "groveGrowth"


def validate(name: str) -> List[str]:
    """Return the problems with a spinner's art ([] when it is sound).

    Checks the properties the plugin relies on but does not itself police:
    enough frames to animate, no duplicate frame (which would stall the
    animation for one tick), and every frame inside the width cap.
    """
    problems: List[str] = []
    spec = SPINNERS.get(name)
    if spec is None:
        return [f"unknown spinner: {name}"]

    frames = spec["frames"]
    if not isinstance(frames, list) or len(frames) < 2:
        problems.append("needs at least 2 frames to animate")
        return problems

    seen = set()
    for index, frame in enumerate(frames):
        if len(frame) > MAX_FRAME_LEN:
            problems.append(
                f"frame {index} is {len(frame)} cells (max {MAX_FRAME_LEN})"
            )
        if frame in seen:
            problems.append(f"frame {index} duplicates an earlier frame")
        seen.add(frame)

    interval = spec.get("interval")
    if not isinstance(interval, (int, float)) or interval <= 0:
        problems.append(f"interval must be a positive number, got {interval!r}")
    return problems


def validate_all() -> Dict[str, List[str]]:
    """Validate every grove spinner; returns name -> problems (omitting clean)."""
    found = {name: validate(name) for name in SPINNERS}
    return {name: problems for name, problems in found.items() if problems}
