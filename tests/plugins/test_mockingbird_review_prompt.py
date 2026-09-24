"""Regression test for the Mockingbird review menu's Rich escaping.

Reported 2026-09-24: the review prompt after a recording rendered as

    end as prompt  ·  dit  ·  e-record  ·  uit >

The hotkey letters were gone. Cause: the prompt was passed to Rich as markup,
and ``[s]`` is a valid strikethrough TAG -- so Rich consumed the very
characters telling the user what to press. ``[/b]`` then closed the bold,
leaving the fragments behind. The fix escapes the OPENING bracket (``\\[s]``);
only the opening bracket, because ``\\]`` would print a literal backslash and
that leaked into the menu on the first attempt.

These tests pin the rendered result, since the failure is invisible in the
source string and only shows up once Rich parses it.
"""

from __future__ import annotations

import sys
from pathlib import Path

# The plugin lives under user-plugins/; import it the way the loader does.
_PLUGIN_PARENT = Path(__file__).resolve().parents[2] / "user-plugins"
if str(_PLUGIN_PARENT) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_PARENT))

from mockingbird import review  # noqa: E402


def _rendered(prompt: str) -> str:
    """What Rich actually prints for *prompt* (plain text, no ANSI)."""
    from io import StringIO

    from rich.console import Console

    buf = StringIO()
    console = Console(file=buf, width=200, no_color=True, highlight=False)
    console.print(prompt)
    return buf.getvalue().strip()


def test_every_hotkey_is_visible_in_the_review_menu():
    rendered = _rendered(review.REVIEW_PROMPT)
    for key, word in (("s", "end"), ("e", "dit"), ("r", "e-record"), ("q", "uit")):
        assert f"[{key}]{word}" in rendered, (
            f"hotkey [{key}] is missing from the rendered menu: {rendered!r}"
        )


def test_the_menu_is_not_mangled_into_fragments():
    """The exact broken output that confused the user."""
    rendered = _rendered(review.REVIEW_PROMPT)
    assert "end as prompt  ·  dit  ·  e-record  ·  uit" not in rendered


def test_escaping_does_not_leak_a_backslash():
    """`\\]` would render literally -- only the opening bracket is escaped."""
    rendered = _rendered(review.REVIEW_PROMPT)
    assert "\\" not in rendered, f"stray backslash in rendered menu: {rendered!r}"
