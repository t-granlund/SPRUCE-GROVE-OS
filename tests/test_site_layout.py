"""Static layout guards for the published site's CSS.

These came out of a real incident: sprucegrove.io/releases/ rendered each
Living Log entry into a 110px-wide column of single words, and /field-guide/
silently clipped ~630px of content on phones. Both were CSS bugs that static
analysis catches cheaply and a browser sweep only finds if it happens to look.

The browser-level audit is the authority (20 pages x 12 widths, 240 checks).
These tests are the fast tripwire that runs with the normal suite, so a
regression fails in seconds rather than at deploy time.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_HUB = REPO_ROOT / "pages-hub"
FIELD_GUIDE = REPO_ROOT / "docs" / "field-guide" / "index.html"

STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S)


def _style_blocks(path: Path) -> list[str]:
    return STYLE_RE.findall(path.read_text(encoding="utf-8"))


def _brace_depth(css: str) -> int:
    """Net { minus } outside comments and strings.

    An unmatched brace is not a cosmetic problem: a stray `.nav {` swallowed
    every rule after it in the field guide, which is why `.tool-item`'s
    `display:flex` never applied and long tool names ran off the page.
    """
    depth = 0
    i = 0
    in_comment = False
    in_string: str | None = None
    while i < len(css):
        ch = css[i]
        if in_comment:
            if ch == "*" and css[i : i + 2] == "*/":
                in_comment = False
                i += 1
        elif in_string:
            if ch == in_string:
                in_string = None
        elif ch == "/" and css[i : i + 2] == "/*":
            in_comment = True
            i += 1
        elif ch in "\"'":
            in_string = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        i += 1
    return depth


def _all_pages() -> list[Path]:
    return sorted(PAGES_HUB.glob("*.html"))


@pytest.mark.parametrize("page", _all_pages(), ids=lambda p: p.name)
def test_pages_hub_stylesheets_have_balanced_braces(page: Path):
    for css in _style_blocks(page):
        assert _brace_depth(css) == 0, f"{page.name}: unbalanced {{ }} in <style>"


def test_field_guide_stylesheet_has_balanced_braces():
    for css in _style_blocks(FIELD_GUIDE):
        assert _brace_depth(css) == 0, "docs/field-guide/index.html: unbalanced { }"


@pytest.mark.parametrize("page", _all_pages(), ids=lambda p: p.name)
def test_no_grid_track_with_a_fixed_minimum(page: Path):
    """`minmax(300px, 1fr)` cannot shrink below 300px.

    On a 320px screen that alone forces horizontal overflow. Every such track
    must clamp its minimum with min(<px>, 100%).
    """
    for css in _style_blocks(page):
        for m in re.finditer(r"minmax\(\s*(\d+)px\s*,\s*1fr\s*\)", css):
            raise AssertionError(
                f"{page.name}: minmax({m.group(1)}px, 1fr) has a fixed minimum; "
                f"use minmax(min({m.group(1)}px, 100%), 1fr)"
            )


@pytest.mark.parametrize("page", _all_pages(), ids=lambda p: p.name)
def test_wrap_sets_width_100(page: Path):
    """A .wrap with only max-width does not shrink inside a flex/grid parent.

    `.wrap` is a flex item in the shell's .sb-main. With max-width alone it
    resolved to its cap (860px) even in a 390px viewport, so the whole page ran
    off-screen while overflow-x:clip hid the evidence.
    """
    for css in _style_blocks(page):
        for m in re.finditer(r"\.wrap\s*\{([^}]*)\}", css):
            body = m.group(1)
            if "max-width" not in body:
                continue
            assert re.search(r"(^|;)\s*width\s*:", body), (
                f"{page.name}: a .wrap rule sets max-width without width:100%"
            )


def _strip_media_blocks(css: str) -> str:
    """Remove every @media block, so only unconditional rules remain.

    Needed because the bug this guards against was a table scroller gated
    behind `@media (max-width:820px)` -- which reads as "present" to a naive
    search but does nothing at a 1024px window.
    """
    out: list[str] = []
    i = 0
    while i < len(css):
        m = re.compile(r"@media\b").search(css, i)
        if not m:
            out.append(css[i:])
            break
        out.append(css[i : m.start()])
        brace = css.find("{", m.end())
        if brace < 0:
            break
        depth = 0
        j = brace
        while j < len(css):
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        i = j + 1
    return "".join(out)


@pytest.mark.parametrize("page", _all_pages(), ids=lambda p: p.name)
def test_pages_with_tables_contain_them(page: Path):
    """A wide data table must scroll inside its own box, at EVERY width.

    The rule must be unconditional. Keying it to a viewport media query cannot
    work: the sidebar and page padding make the content box narrower than the
    viewport, so a rule gated at max-width:820px missed a 1090px table at a
    1024px window and the document scrolled 90px.
    """
    source = page.read_text(encoding="utf-8")
    if "<table" not in source:
        return
    for css in _style_blocks(page):
        if re.search(r"table\s*\{[^}]*overflow-x\s*:\s*auto", _strip_media_blocks(css)):
            return
    raise AssertionError(
        f"{page.name}: contains a <table> but no unconditional table scroller"
    )


def _right_side_escapes(value: str) -> str | None:
    """Return the offending fragment when an inset pushes content past the RIGHT.

    `inset` shorthand is top/right/bottom/left. Only the right component (2nd of
    2 or 4 values) can extend the document's scrollable overflow region in LTR;
    a negative bottom is vertical and harmless, and a negative left is the
    off-screen technique (e.g. `.skip-link{left:-999px}`), which does not create
    a scrollbar in an LTR document.
    """
    parts = value.split()
    if not parts:
        return None
    # inset shorthand: top / right / bottom / left. Right is the 2nd of 2-4
    # values, or the only value when there is one.
    right = parts[0] if len(parts) == 1 else parts[1]
    return right if right.startswith("-") else None


def _containing_rule(css: str, index: int) -> tuple[str, str]:
    """(selector, body) of the declaration block containing `index`."""
    open_brace = css.rfind("{", 0, index)
    close_brace = css.find("}", index)
    if open_brace < 0 or close_brace < 0:
        return "", ""
    selector_start = max(css.rfind("}", 0, open_brace), css.rfind(";", 0, open_brace)) + 1
    selector = css[selector_start:open_brace].strip()
    return selector, css[open_brace : close_brace + 1]


def _is_clipped(css: str, index: int) -> bool:
    """True when the decorated element, or its base element, clips overflow.

    Two real cases drove this:
      `.arrow::after { left:-40% }` clipped by `.arrow { overflow:hidden }`
        -- the clip lives on the PARENT selector; and
      `.watermark { right:-60px }` clipped by `.hero { overflow:hidden }`
        -- the clip is declared LATER in the file, so a search limited to text
        before the offset misses it.
    Search the whole stylesheet for a clipping rule on the element or any
    container-type ancestor selector.
    """
    import re as _re

    selector, body = _containing_rule(css, index)
    if "overflow:hidden" in body.replace(" ", "") or "overflow:clip" in body.replace(" ", ""):
        return True
    base = _re.split(r"::?(?:before|after)", selector)[0].strip()
    if not base:
        return False
    # The element's own base rule anywhere in the sheet.
    if _re.search(rf"(?<![\w-]){_re.escape(base)}\s*\{{[^}}]*overflow\s*:\s*(hidden|clip)", css):
        return True
    # Known container ancestors used by these page templates.
    for anc in (".hero", ".wrap", "header", "body", "section"):
        if _re.search(rf"{_re.escape(anc)}\s*\{{[^}}]*overflow\s*:\s*(hidden|clip)", css):
            return True
    return False


def _is_viewport_fixed(css: str, index: int) -> bool:
    """True when the element is position:fixed.

    A fixed element is laid out against the viewport and, per CSS Overflow, does
    not contribute to the document's scrollable overflow region -- so a negative
    offset there cannot widen the page. (The browser audit agrees.)
    """
    _, body = _containing_rule(css, index)
    return "position:fixed" in body.replace(" ", "")


def test_no_horizontally_negative_inset_decorations():
    """Full-bleed decorations must not exceed their clip.

    `inset:-40% -20% auto` (right:-20%) put an absolutely-positioned layer past
    the right edge and grew the document on every page that used it. A negative
    horizontal offset is fine ONLY when the element's own rule clips it, as an
    animation sweep inside `overflow:hidden` does.
    """
    for page in _all_pages():
        for css in _style_blocks(page):
            for m in re.finditer(r"(?<![\w-])(?:inset|right)\s*:\s*([^;}]+)", css):
                value = m.group(1).strip()
                is_right = m.group(0).lstrip().startswith("right")
                offending = value.startswith("-") if is_right else _right_side_escapes(value)
                if not offending:
                    continue
                if _is_clipped(css, m.start()):
                    continue  # its element (or parent) clips it; cannot widen the page
                if _is_viewport_fixed(css, m.start()):
                    continue  # position:fixed is viewport-anchored; it does not
                    # extend the document's scrollable overflow region
                raise AssertionError(
                    f"{page.name}: negative horizontal offset {m.group(0).strip()!r} "
                    f"is not clipped by its own rule"
                )
