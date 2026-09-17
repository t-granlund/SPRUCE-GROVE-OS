"""E2E smoke suite for every Spruce Grove surface.

The staple surfaces, each verified for the things that must never break:
  - deck      http://localhost:8086   (the presentation: GRAN chrome + Chaplin live transcription)
  - product   http://localhost:8087   (sprucegrove.io: lockup, club band, stamps)
  - club      http://localhost:8088   (the Leather Apron Club hall: mark, stamp, countdown)
  - works     http://localhost:8088   (the homecoming page: chairs, booking truth)

Run:  boot the three static servers, then  uv run pytest tests/e2e/test_surfaces.py
Servers are expected on 8086 (deck dir), 8087 (pages-hub), 8088 (club repo root).
Every test skips cleanly when its server is not reachable, so the suite is
safe to run anywhere.
"""

import os

import pytest
from playwright.sync_api import sync_playwright

DECK = os.environ.get("SURFACE_DECK", "http://localhost:8086")
PRODUCT = os.environ.get("SURFACE_PRODUCT", "http://localhost:8087")
CLUB = os.environ.get("SURFACE_CLUB", "http://localhost:8088")


def _reachable(url: str) -> bool:
    import urllib.request

    try:
        return urllib.request.urlopen(url, timeout=2).status == 200
    except Exception:
        return False


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        yield b
        b.close()


def _page(browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on(
        "console",
        lambda m: errors.append(m.text) if m.type == "error" else None,
    )
    page.errors = errors  # type: ignore[attr-defined]
    return page


# ── the deck ────────────────────────────────────────────────────────────


@pytest.mark.skipif(not _reachable("http://localhost:8086"), reason="deck server down")
class TestDeck:
    def test_gran_chrome_present(self, browser):
        page = _page(browser)
        page.goto(f"{DECK}/", wait_until="networkidle")
        page.wait_for_timeout(1500)
        assert page.evaluate("!!document.getElementById('grove-grain')")
        slides = page.evaluate(
            "Reveal.getSlides().filter(s => s.querySelector('.stamp')).length"
        )
        assert slides >= 2, "the stamps went missing"
        assert page.evaluate(
            "Reveal.getSlides().filter(s => s.querySelector('.rune-line')).length >= 2"
        )

    def test_chaplin_live_transcription_armed(self, browser):
        page = _page(browser)
        page.goto(f"{DECK}/", wait_until="networkidle")
        idx = page.evaluate(
            "Reveal.getSlides().findIndex(s => !!s.querySelector('#bank-caps'))"
        )
        page.evaluate(f"Reveal.slide({idx})")
        page.wait_for_timeout(800)
        assert page.evaluate("!!document.getElementById('chaplin-video')"), (
            "the film is gone"
        )
        caps = page.evaluate("document.getElementById('bank-caps').textContent")
        assert caps is not None

    def test_no_console_errors_or_broken_images(self, browser):
        page = _page(browser)
        page.goto(f"{DECK}/", wait_until="networkidle")
        page.wait_for_timeout(1200)
        broken = page.evaluate(
            "[...document.querySelectorAll('img')].filter(i => !i.complete || i.naturalWidth === 0).length"
        )
        assert broken == 0
        assert not page.errors, f"console errors: {page.errors[:3]}"


# ── sprucegrove.io (product) ────────────────────────────────────────────


@pytest.mark.skipif(
    not _reachable("http://localhost:8087"), reason="product server down"
)
class TestProduct:
    def test_lockup_and_brandmark(self, browser):
        page = _page(browser)
        page.goto(f"{PRODUCT}/product.html", wait_until="networkidle")
        wm = page.locator(".wordmark")
        assert wm.count() == 1
        assert page.locator(".wordmark .brandmark").count() == 1
        assert page.locator(".wordmark .leaf").count() == 1, "the orange dot"

    def test_club_message_and_stamp(self, browser):
        page = _page(browser)
        page.goto(f"{PRODUCT}/product.html", wait_until="networkidle")
        assert page.locator(".club-line").count() == 1
        assert page.locator(".club-band").count() == 1
        assert page.locator(".club-band .rune").count() == 1
        stamp = page.locator(".sec-h .stamp").first.text_content()
        assert stamp and "live today" in stamp.lower()

    def test_no_stale_brand_refs(self, browser):
        page = _page(browser)
        page.goto(f"{PRODUCT}/product.html", wait_until="networkidle")
        assert "candm" not in page.content().lower()


# ── the club hall ───────────────────────────────────────────────────────


@pytest.mark.skipif(not _reachable("http://localhost:8088"), reason="club server down")
class TestClub:
    def test_hall_staples(self, browser):
        page = _page(browser)
        page.goto(f"{CLUB}/", wait_until="networkidle")
        page.wait_for_timeout(900)
        assert page.evaluate(
            "(function(){var m=document.querySelector('.mark-hero');return m&&m.naturalWidth>0})()"
        )
        assert page.locator(".notice .stamp").count() == 1
        assert page.evaluate("!!document.querySelector('header .rune-line')")
        assert page.evaluate("!!document.getElementById('grove-grain')")

    def test_countdown_and_reachability(self, browser):
        page = _page(browser)
        page.goto(f"{CLUB}/", wait_until="networkidle")
        cd = page.locator("#countdown").text_content() or ""
        assert "convene" in cd.lower() or "council" in cd.lower()
        hrefs = page.evaluate(
            "Array.from(document.querySelectorAll('a')).map(a => a.getAttribute('href'))"
        )
        assert "guide.html" in hrefs, "the explainer guide is an orphan again"
        assert any(h and "sprucegrove.io" in h for h in hrefs)

    def test_barbershop_truth(self, browser):
        page = _page(browser)
        page.goto(f"{CLUB}/", wait_until="networkidle")
        assert "candm" not in page.content().lower()
        works = page.evaluate(
            "Array.from(document.querySelectorAll('a')).filter(a => (a.getAttribute('href')||'').includes('works/')).length"
        )
        assert works >= 1
