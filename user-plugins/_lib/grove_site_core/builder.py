"""grove_site_core.builder -- content-driven static site scaffolder.

One function that matters: ``build_site(profile, outdir)``. A profile is a
plain dict (see SCHEMATIC below); nothing reaches the network, nothing writes
outside ``outdir``. Reuse rule of the grove: cohort plugins ship profile DATA;
this builder is the shared >=60%% of every scaffold (sg-5al.3 / sg-5al.5).

Profile keys (all optional except brand_name):
    brand_name (str), tagline (str), hero_copy (str),
    services: list[dict(title, desc)],
    sections: list[dict(title, cards=list[dict(title, desc)])]  # extra grids
    booking_url (str), booking_label (str),
    checklist: list[dict(item, source)],   # source = official URL or note
    footer_note (str), theme_overrides: dict  # reserved, palette stays grove
    media: dict                             # showcase block (sg-5al.5)
        video_url (str), video_label (str),  # https embed only; iframe
        gallery: list[dict(src, alt)]        # thumbs + pure-JS lightbox
"""

from __future__ import annotations

import html
from pathlib import Path

from grove_site_core import tokens


def _esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def _card(text_title: str, text_body: str) -> str:
    return (
        f'<div class="card"><div class="t">{_esc(text_title)}</div>'
        f"<p>{_esc(text_body)}</p></div>"
    )


_LIGHTBOX_CSS = (
    "section.media .embed{aspect-ratio:16/9;width:100%;max-width:860px;border:1px solid rgba(238,235,229,.10);"
    "border-radius:14px;background:#121813;display:block}"
    "section.media img[data-lb]{width:100%;border:1px solid rgba(238,235,229,.10);border-radius:10px;display:block}"
    "#lb{position:fixed;inset:0;background:rgba(10,14,11,.92);display:none;align-items:center;"
    "justify-content:center;z-index:50;cursor:zoom-out}"
    "#lb img{max-width:92vw;max-height:88vh;border:1px solid rgba(238,235,229,.10);border-radius:14px}"
    "#lb .cap{position:fixed;bottom:20px;left:0;right:0;text-align:center;font-size:13px;color:#A5A699}"
)

_LIGHTBOX_JS = """(function () {
  var ov = document.getElementById('lb');
  if (!ov) return;
  var img = ov.querySelector('img');
  var cap = ov.querySelector('.cap');
  document.querySelectorAll('img[data-lb]').forEach(function (el) {
    el.addEventListener('click', function () {
      img.src = el.getAttribute('data-full') || el.src;
      cap.textContent = el.alt || '';
      ov.style.display = 'flex';
    });
    el.style.cursor = 'zoom-in';
  });
  ov.addEventListener('click', function () { ov.style.display = 'none'; img.removeAttribute('src'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') ov.style.display = 'none'; });
})();
"""


def _media_section(profile: dict) -> str:
    """Optional showcase block: embeddable video + click-to-zoom gallery.

    Video URLs must be https (never guess-scheme); gallery images are dropped
    into a native-feeling lightbox with focus-visible support. Pure vanilla JS.
    """
    media = profile.get("media") or {}
    chunks = []
    video = str(media.get("video_url", ""))
    if video:
        if not video.startswith("https://"):
            raise ValueError("media.video_url must be an https embed URL")
        chunks.append(
            f'<iframe class="embed" src="{_esc(video)}" title="{_esc(media.get("video_label", "Showreel"))}" '
            'loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
            "allowfullscreen></iframe>"
        )
    gallery = media.get("gallery", [])
    if gallery:
        thumbs = "".join(
            f'<img src="{_esc(g["src"])}" alt="{_esc(g.get("alt", ""))}" loading="lazy" '
            f'data-lb data-full="{_esc(g.get("full", g["src"]))}" />'
            for g in gallery
        )
        chunks.append(f'<div class="grid">{thumbs}</div>')
    if not chunks:
        return ""
    return (
        '<section class="media" aria-label="Media showcase"><h2>Work</h2>'
        + "".join(chunks)
        + '<div id="lb" role="dialog" aria-label="Image viewer"><img alt="" /><div class="cap"></div></div>'
        + "</section>"
    )


def render_index(profile: dict) -> str:
    """Render the marketing landing page for a cohort profile."""
    brand = _esc(profile["brand_name"])
    tagline = _esc(profile.get("tagline", ""))
    hero = _esc(profile.get("hero_copy", ""))
    booking_url = _esc(profile.get("booking_url", ""))
    booking_label = _esc(profile.get("booking_label", "Book an appointment"))

    service_cards = "".join(
        _card(s["title"], s.get("desc", "")) for s in profile.get("services", [])
    )
    extra_sections = "".join(
        f'<section aria-label="{_esc(sec["title"])}"><h2>{_esc(sec["title"])}</h2>'
        f'<div class="grid">'
        + "".join(_card(c["title"], c.get("desc", "")) for c in sec.get("cards", []))
        + "</div></section>"
        for sec in profile.get("sections", [])
    )
    cta = (
        f'<a class="cta" href="{booking_url}">{booking_label} &rarr;</a>'
        if booking_url
        else ""
    )
    media_html = _media_section(profile)
    if media_html:
        extra_style = f"<style>{_LIGHTBOX_CSS}</style>"
        lightbox_js = f"<script>{_LIGHTBOX_JS}</script>"
    else:
        extra_style = lightbox_js = ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="theme-color" content="{tokens.TOKENS["bg"]}" />
<title>{brand}</title>
<meta name="description" content="{tagline}" />
<style>{tokens.base_css()}</style>
{extra_style}
</head>
<body>
<div class="wrap">
  <div class="hero">
    <span class="kicker">{tagline}</span>
    <h1><em>{brand}</em></h1>
    <p class="lede">{hero}</p>
    {cta}
  </div>
  <section aria-label="Services">
    <h2>Services</h2>
    <div class="grid">{service_cards}</div>
  </section>
  {extra_sections}
  {media_html}
  <footer>
    <p>{_esc(profile.get("footer_note", ""))}</p>
    <span class="wordmark">site scaffold by {tokens.wordmark()} &middot; grove site core</span>
  </footer>
</div>
{lightbox_js}
</body>
</html>
"""


def render_checklist(profile: dict) -> str:
    """Render the launch checklist page (booking, media, and ship-gates)."""
    brand = _esc(profile["brand_name"])
    items = "".join(
        f"<li>{_esc(entry['item'])}"
        + (
            f' <span class="src">source: {html.escape(str(entry["source"]), quote=True)}</span>'
            if entry.get("source")
            else ""
        )
        + "</li>"
        for entry in profile.get("checklist", [])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="theme-color" content="{tokens.TOKENS["bg"]}" />
<title>{brand} &mdash; Launch checklist</title>
<style>{tokens.base_css()}</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <span class="kicker">launch gates</span>
    <h1><em>{brand}</em> checklist</h1>
    <p class="lede">Every gate must pass before this site goes live. Sources are official
      or explicit placeholders &mdash; never guesswork.</p>
  </div>
  <section aria-label="Checklist">
    <ul class="check-list">{items}</ul>
  </section>
  <footer><span class="wordmark">site scaffold by {tokens.wordmark()} &middot; grove site core</span></footer>
</div>
</body>
</html>
"""


def build_site(profile: dict, outdir: Path) -> dict:
    """Write the full scaffold to ``outdir`` and report what landed.

    Returns {written: [Path, ...], outdir: Path}. No network. No writes
    outside outdir. Idempotent: re-running overwrites generated files only.
    """
    if "brand_name" not in profile:
        raise ValueError("profile requires 'brand_name'")
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    pages = {
        "index.html": render_index(profile),
        "checklist.html": render_checklist(profile),
    }
    written = []
    for name, content in pages.items():
        target = outdir / name
        target.write_text(content, encoding="utf-8")
        written.append(target)
    return {"written": written, "outdir": outdir}
