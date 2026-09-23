"""Durability guards for the baked braille boot art.

The wordmark lives in **two** modules: ``banner_art`` (the scrollback
banner) and ``splash`` (the import-time splash, which deliberately cannot
import ``spruce_grove`` and so keeps its own copy). They must never drift
apart.

These tests are cross-platform: they assert the *contract* (row count,
exact width, braille-only glyphs) and the *sync* between the two copies,
never the exact glyph shapes -- those are the baker's ``--check`` job,
which needs a usable font. Where a font *is* available, the last test
closes the loop: a fresh bake must reproduce the committed art byte for
byte. That one test catches both source drift and baker rot.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

from spruce_grove import banner_art, splash

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
BRAILLE_LO = 0x2800
BRAILLE_HI = 0x28FF
EXPECTED_ROWS = 6
EXPECTED_FULL_COLS = 96

REPO_ROOT = Path(__file__).resolve().parent.parent
BAKER_PATH = REPO_ROOT / "scripts" / "bake_braille_banner.py"


def _braille_only(rows) -> bool:
    return all(BRAILLE_LO <= ord(c) <= BRAILLE_HI for line in rows for c in line)


class TestCommittedBannerArt:
    def test_full_mark_contract(self):
        rows = banner_art.SPRUCE_GROVE_BANNER_LINES
        assert len(rows) == EXPECTED_ROWS
        assert {len(line) for line in rows} == {EXPECTED_FULL_COLS}
        assert _braille_only(rows)
        assert all(line == line.rstrip() for line in rows)

    def test_compact_mark_contract(self):
        rows = banner_art.GROVE_BANNER_LINES
        assert len(rows) == EXPECTED_ROWS
        assert _braille_only(rows)
        assert all(line == line.rstrip() for line in rows)
        assert max(len(line) for line in rows) <= EXPECTED_FULL_COLS

    def test_natural_width_is_the_bake_width(self):
        # platform_utils pins its label threshold to this number.
        assert banner_art.SPRUCE_GROVE_NATURAL_WIDTH == EXPECTED_FULL_COLS

    def test_art_for_label_is_a_string_both_ways(self):
        full = banner_art.art_for_label("SPRUCE GROVE")
        compact = banner_art.art_for_label("GROVE")
        assert isinstance(full, str) and isinstance(compact, str)
        assert full == banner_art.SPRUCE_GROVE_BANNER
        assert compact == banner_art.GROVE_BANNER
        assert full != compact

    def test_banner_constants_join_their_lines(self):
        assert banner_art.SPRUCE_GROVE_BANNER.split("\n") == list(
            banner_art.SPRUCE_GROVE_BANNER_LINES
        )
        assert banner_art.GROVE_BANNER.split("\n") == list(
            banner_art.GROVE_BANNER_LINES
        )


class TestDuplicateStaysInSync:
    """splash keeps its own copy; nothing may let the two diverge."""

    def test_splash_full_matches_banner_art(self):
        assert splash._BANNER_FULL == banner_art.SPRUCE_GROVE_BANNER_LINES

    def test_splash_compact_matches_banner_art(self):
        assert splash._BANNER_COMPACT == banner_art.GROVE_BANNER_LINES

    def test_widths_agree_everywhere(self):
        from spruce_grove import platform_utils

        assert splash._BANNER_FULL_WIDTH == banner_art.SPRUCE_GROVE_NATURAL_WIDTH
        assert platform_utils._FULL_BANNER_WIDTH == splash._BANNER_FULL_WIDTH


class TestBrailleTierTable:
    def test_covers_every_bit_pattern(self):
        assert len(splash._BRAILLE_TIER) == 256

    def test_blank_cell_is_empty(self):
        assert splash._BRAILLE_TIER[0] == 0

    def test_entries_are_valid_tiers(self):
        assert set(splash._BRAILLE_TIER) <= {0, 2, 3}

    def test_dense_cell_earns_the_core_tier(self):
        # 0xFF lights every dot -- as dense as a cell gets.
        assert splash._BRAILLE_TIER[0xFF] == 3

    def test_sparse_cell_glows_not_core(self):
        # A single dot is a sparse edge cell: glow, never core.
        assert splash._BRAILLE_TIER[0x01] == 2

    def test_core_requires_at_least_four_dots(self):
        # Density is the rule; this is the exact boundary.
        assert splash._BRAILLE_TIER[0b1111] == 3
        assert splash._BRAILLE_TIER[0b111] == 2

    def test_banner_art_lights_both_tiers(self):
        # A tier table that never fires "core" would leave the wordmark flat.
        tiers = {
            splash._BRAILLE_TIER[ord(c) - 0x2800]
            for line in splash._BANNER_FULL
            for c in line
        }
        assert {2, 3} <= tiers


class TestFrameRendersBraille:
    """The splash frame path must handle braille cells without crashing."""

    def _frame_lines(self, columns: int, lines: int):
        rows = splash._compose_rows(columns, lines)
        frame = splash._build_frame(0, True, rows)
        return [ANSI_RE.sub("", line) for line in frame.splitlines()]

    def test_only_pyramid_and_braille_glyphs(self):
        bleed = set()
        for line in self._frame_lines(120, 50):
            bleed |= {
                c
                for c in line
                if not (
                    BRAILLE_LO <= ord(c) <= BRAILLE_HI or c in " \u2591\u2592\u2588"
                )
            }
        assert bleed == set()

    def test_rows_are_left_padded(self):
        # Empty braille cells and centering both render as spaces, so a row
        # may legitimately carry trailing space -- but the art is centered,
        # so every non-blank row opens on padding.
        lines = [ln for ln in self._frame_lines(120, 50) if ln]
        assert lines
        for line in lines:
            assert line.startswith(" ")

    def test_wordmark_rows_reach_the_banner_width(self):
        # The four 96-column rows flow through the frame without being
        # clipped or widened.
        widths = {len(ln) for ln in self._frame_lines(120, 50)}
        assert splash._BANNER_FULL_WIDTH in widths

    def test_frame_still_animates_and_has_no_erase_codes(self):
        rows = splash._compose_rows(120, 50)
        frame = splash._build_frame(0, True, rows)
        assert splash._build_frame(0, True, rows) != splash._build_frame(20, True, rows)
        assert "\x1b[2K" not in frame
        assert not frame.endswith("\n")


class TestBakerReproduces:
    """The strongest guard: a fresh bake must equal the committed art."""

    def _load_baker(self):
        spec = importlib.util.spec_from_file_location("bake_braille_banner", BAKER_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_fresh_bake_matches_committed_art(self):
        baker = self._load_baker()
        try:
            fresh = baker.bake_all()
        except baker.NoFontError as exc:
            pytest.skip(f"no rounded font available: {exc}")

        assert (
            fresh["SPRUCE_GROVE_BANNER_LINES"] == banner_art.SPRUCE_GROVE_BANNER_LINES
        )
        assert fresh["GROVE_BANNER_LINES"] == banner_art.GROVE_BANNER_LINES

    def test_baker_check_passes(self):
        baker = self._load_baker()
        try:
            baker.find_font()
        except baker.NoFontError as exc:
            pytest.skip(f"no rounded font available: {exc}")
        assert baker.check() == 0
