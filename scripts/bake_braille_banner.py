#!/usr/bin/env python
"""Bake the grove's braille boot wordmark.

The boot lettering is drawn in **braille** (U+2800 block) rather than a
figlet font. Braille packs a 2x4 dot grid per cell, so a single terminal
row carries four dot rows of vertical resolution -- enough for genuinely
curved, organic letterforms instead of chunky solid blocks.

This script is the *source of truth* for that art. It renders "SPRUCE
GROVE" and "GROVE" from a rounded system font (via Pillow, already a
runtime dependency) and writes the result into the two modules that need
it: ``spruce_grove/banner_art.py`` (the scrollback banner) and
``spruce_grove/splash.py`` (the import-time splash, which cannot import
``spruce_grove`` and so keeps its own copy).

Usage::

    uv run python scripts/bake_braille_banner.py            # report only
    uv run python scripts/bake_braille_banner.py --check    # verify committed art
    uv run python scripts/bake_braille_banner.py --write    # re-bake + rewrite

``--check`` is the drift guard: it re-derives the art and compares it to
what is committed, exiting non-zero if the two have diverged. It needs a
usable font, so it is a local/authoring tool, not a CI gate -- the tests
assert the *contract* (row count, exact width, braille-only) which holds
on every platform without a font.

Override the font with ``SPRUCE_GROVE_BAKE_FONT=/path/to/font.ttf``.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
BANNER_ART = REPO / "spruce_grove" / "banner_art.py"
SPLASH = REPO / "spruce_grove" / "splash.py"

#: The banner contract, pinned by tests/test_splash.py and
#: tests/test_platform_utils.py. ``SPRUCE GROVE`` is exactly 96 columns --
#: ``platform_utils._FULL_BANNER_WIDTH`` pins its label threshold to it.
ROWS = 6
FULL_COLS = 96
PAD_DOTS = 2

#: Rounded faces, best first. macOS has these; other platforms can point
#: SPRUCE_GROVE_BAKE_FONT at any rounded/geometric sans.
FONT_CANDIDATES = (
    "/System/Library/Fonts/SFCompactRounded.ttf",
    "/System/Library/Fonts/SFNSRounded.ttf",
    "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
)

_DOTS = (
    (0, 0, 0x01),
    (0, 1, 0x02),
    (0, 2, 0x04),
    (1, 0, 0x08),
    (1, 1, 0x10),
    (1, 2, 0x20),
    (0, 3, 0x40),
    (1, 3, 0x80),
)
BRAILLE_BASE = 0x2800
BRAILLE_BLANK = "\u2800"


class NoFontError(RuntimeError):
    """No usable rounded font could be found."""


def find_font() -> str:
    override = os.environ.get("SPRUCE_GROVE_BAKE_FONT")
    if override:
        if not Path(override).exists():
            raise NoFontError(f"SPRUCE_GROVE_BAKE_FONT does not exist: {override}")
        return override
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise NoFontError(
        "No rounded font found. Set SPRUCE_GROVE_BAKE_FONT to a .ttf/.ttc path "
        f"(tried: {', '.join(FONT_CANDIDATES)})"
    )


def _fit_font(font_path: str, text: str, max_h: int) -> ImageFont.FreeTypeFont:
    """Largest size whose stroked bbox fits the dot-row budget."""
    for size in range(max_h + 20, 5, -1):
        font = ImageFont.truetype(font_path, size)
        bbox = font.getbbox(text, stroke_width=1)
        if bbox[3] - bbox[1] <= max_h - 2 * PAD_DOTS:
            return font
    return ImageFont.truetype(font_path, 6)


def _draw(font: ImageFont.FreeTypeFont, text: str, track: float, height: int):
    """Draw ``text`` glyph-by-glyph with ``track`` extra dots between them."""
    metrics = [font.getbbox(c, stroke_width=1) for c in text]
    advances = [m[2] - m[0] for m in metrics]
    width = int(round(sum(advances) + track * (len(text) - 1))) + 2 * PAD_DOTS

    img = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(img)
    x = float(PAD_DOTS)
    for ch, m, adv in zip(text, metrics, advances):
        bbox = font.getbbox(ch, stroke_width=1)
        draw.text(
            (x - bbox[0], PAD_DOTS - bbox[1]),
            ch,
            fill=255,
            font=font,
            stroke_width=1,
        )
        x += adv + track
    return img


def _to_braille(grid: list[str]) -> list[str]:
    """Pack a dot grid into braille rows (2 wide x 4 tall per cell)."""
    height = len(grid)
    width = max((len(r) for r in grid), default=0)
    lines: list[str] = []
    for top in range(0, height, 4):
        chars: list[str] = []
        for x in range(0, width, 2):
            bits = 0
            for dx, dy, bit in _DOTS:
                yy, xx = top + dy, x + dx
                if yy < height and xx < len(grid[yy]) and grid[yy][xx] == "1":
                    bits |= bit
            chars.append(chr(BRAILLE_BASE + bits))
        lines.append("".join(chars).rstrip())
    return lines


def _trim(art: list[str]) -> list[str]:
    """Drop blank rows top/bottom and blank columns left/right."""
    while art and not art[0].strip().strip(BRAILLE_BLANK):
        art = art[1:]
    while art and not art[-1].strip().strip(BRAILLE_BLANK):
        art = art[:-1]
    if not art:
        return art
    while all(not line[:1].strip().strip(BRAILLE_BLANK) for line in art):
        art = [line[1:] for line in art]
    while all(not line[-1:].strip().strip(BRAILLE_BLANK) for line in art):
        art = [line[:-1] for line in art]
    return art


def bake(
    text: str, cols: int | None = None, font_path: str | None = None
) -> tuple[str, ...]:
    """Bake ``text`` to six braille rows, padded to exactly ``cols`` cells.

    Splash centers every banner row against one shared block width, so all
    rows come out the same length; ``cols`` also centers the glyphs on that
    canvas. Every row is rstrip-clean.
    """
    font_path = font_path or find_font()
    max_h = ROWS * 4
    font = _fit_font(font_path, text, max_h)

    if cols is None:
        img = _draw(font, text, 0.0, max_h)
    else:
        # Solve tracking so the packed cell count lands on ``cols`` exactly.
        target_dots = cols * 2
        base = _draw(font, text, 0.0, max_h).width
        gaps = max(1, len(text) - 1)
        track = (target_dots - base) / gaps
        img = _draw(font, text, track, max_h)
        while img.width // 2 > cols and track > -4:
            track -= 0.25
            img = _draw(font, text, track, max_h)
        while img.width // 2 < cols:
            track += 0.25
            img = _draw(font, text, track, max_h)

    px = img.load()
    grid = [
        "".join("1" if px[x, y] > 127 else "0" for x in range(img.width))
        for y in range(img.height)
    ]

    art = _trim(_to_braille(grid))
    natural = max((len(line) for line in art), default=0)
    target = cols if cols is not None else natural
    left = max(0, (target - natural) // 2)
    right = max(0, target - natural - left)
    return tuple(
        BRAILLE_BLANK * left + line.ljust(natural) + BRAILLE_BLANK * right
        for line in art
    )


def bake_all(font_path: str | None = None) -> dict[str, tuple[str, ...]]:
    """Both marks, exactly as they belong in the source."""
    font_path = font_path or find_font()
    return {
        "SPRUCE_GROVE_BANNER_LINES": bake(
            "SPRUCE GROVE", cols=FULL_COLS, font_path=font_path
        ),
        "GROVE_BANNER_LINES": bake("GROVE", font_path=font_path),
    }


def as_literal(lines: tuple[str, ...], indent: str = "    ") -> str:
    """Emit the rows as a tuple-of-strings literal, glyphs escape-spelled."""
    rows = []
    for line in lines:
        spelled = "".join(c if ord(c) <= 0x7E else f"\\u{ord(c):04x}" for c in line)
        rows.append(f'{indent}"{spelled}",')
    return "\n".join(rows)


def _committed(path: Path, name: str) -> tuple[str, ...] | None:
    """Read a committed tuple-of-strings constant without importing the module."""
    if not path.exists():
        return None
    source = path.read_text()
    match = re.search(rf"^{name} = \((.*?)^\)$", source, re.M | re.S)
    if not match:
        return None
    return tuple(re.findall(r'"((?:[^"\\]|\\.)*)"', match.group(1)))


def _decoded(rows: tuple[str, ...]) -> tuple[str, ...]:
    """Decode escape-spelled source literals back to real characters."""
    return tuple(row.encode().decode("unicode_escape") for row in rows)


def check() -> int:
    """Verify the committed art matches a fresh bake. 0 = in sync."""
    fresh = bake_all()
    targets = {
        "SPRUCE_GROVE_BANNER_LINES": BANNER_ART,
        "GROVE_BANNER_LINES": BANNER_ART,
        "_BANNER_FULL": SPLASH,
        "_BANNER_COMPACT": SPLASH,
    }
    fresh_for = {
        "SPRUCE_GROVE_BANNER_LINES": fresh["SPRUCE_GROVE_BANNER_LINES"],
        "GROVE_BANNER_LINES": fresh["GROVE_BANNER_LINES"],
        "_BANNER_FULL": fresh["SPRUCE_GROVE_BANNER_LINES"],
        "_BANNER_COMPACT": fresh["GROVE_BANNER_LINES"],
    }

    drifted = []
    for name, path in targets.items():
        committed = _committed(path, name)
        if committed is None:
            print(f"  ?? {path.name}:{name} - not found")
            drifted.append(name)
        elif _decoded(committed) != fresh_for[name]:
            print(f"  DRIFT {path.name}:{name} - committed art != fresh bake")
            drifted.append(name)
        else:
            print(f"  ok  {path.name}:{name}")

    if drifted:
        print(f"\n{len(drifted)} drifted -> run with --write to re-bake.")
        return 1
    print("\nAll committed banner art is in sync with a fresh bake.")
    return 0


def write() -> int:
    """Re-bake and rewrite both modules in place."""
    fresh = bake_all()
    banner = BANNER_ART.read_text()
    for name, lines in fresh.items():
        # No trailing newline: the regex consumes the closing paren, and the
        # blank line that followed it stays put -- a byte-identical round-trip.
        block = f"{name} = (\n{as_literal(lines)}\n)"
        banner, n = re.subn(
            rf"^{name} = \(.*?^\)$", lambda m: block, banner, count=1, flags=re.M | re.S
        )
        if n != 1:
            print(f"  !! could not patch {name} in {BANNER_ART.name}")
            return 1
    BANNER_ART.write_text(banner)

    splash = SPLASH.read_text()
    for name, key in (
        ("_BANNER_FULL", "SPRUCE_GROVE_BANNER_LINES"),
        ("_BANNER_COMPACT", "GROVE_BANNER_LINES"),
    ):
        block = f"{name} = (\n{as_literal(fresh[key])}\n)"
        splash, n = re.subn(
            rf"^{name} = \(.*?^\)$", lambda m: block, splash, count=1, flags=re.M | re.S
        )
        if n != 1:
            print(f"  !! could not patch {name} in {SPLASH.name}")
            return 1
    SPLASH.write_text(splash)

    print("Re-baked banner_art.py and splash.py. Run ruff format, then --check.")
    return 0


def report() -> int:
    fresh = bake_all()
    for name, lines in fresh.items():
        widths = {len(line) for line in lines}
        print(f"{name}: {len(lines)} rows, widths {sorted(widths)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="verify committed art")
    group.add_argument("--write", action="store_true", help="re-bake and rewrite")
    args = parser.parse_args(argv)

    try:
        if args.check:
            return check()
        if args.write:
            return write()
        return report()
    except NoFontError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
