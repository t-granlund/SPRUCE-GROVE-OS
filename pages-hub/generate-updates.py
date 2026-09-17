#!/usr/bin/env python3
"""Regenerate the auto-managed regions of pages-hub/updates.html.

Reads the field-guide changelog data (docs/field-guide/data.js) and rewrites
only the content between <!-- AUTO-BEGIN:name --> / <!-- AUTO-END:name -->
markers. Hand-curated deep-dive narratives outside the markers are untouched.

Auto-managed regions:
  stats          - hero statline numbers (commits/features/fixes/tools/agents/plugins)
  living-updates - cards from the dictation ledger (LIVING-UPDATES.md)
  toc            - link to the auto-detected section (appears only when needed)
  auto-features  - cards for notable feat commits not yet curated into deep-dives
  minor-list     - recent minor enhancements (feat/refactor/perf/docs buckets)
  fixes-list     - recent bug fixes (fix bucket)

Run by ~/.spruce_grove/scripts/update-code-grove.sh after field-guide regen,
or manually: uv run python pages-hub/generate-updates.py
"""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_JS = REPO_ROOT / "docs" / "field-guide" / "data.js"
UPDATES_HTML = REPO_ROOT / "pages-hub" / "updates.html"
LIVING_MD = REPO_ROOT / "LIVING-UPDATES.md"

MAX_LIST_ITEMS = 18
MAX_AUTO_CARDS = 12
MAX_LIVING_CARDS = 12

LIVING_BEGIN = "<!-- LIVING:BEGIN -->"
LIVING_END = "<!-- LIVING:END -->"

# status -> (chip label, css chip class). Reuses the provenance chip palette.
LIVING_STATUS = {
    "shipped": ("shipped", "gr"),
    "in-flight": ("in flight", "up"),
    "idea": ("idea", ""),
}

# Ordered list (NOT a set) so output is deterministic across runs regardless
# of Python's hash randomization.
MINOR_KINDS = ["feat", "refactor", "perf", "polish", "docs", "style"]

# Authors whose commits count as grove-grown. Everything else arrived by
# proxy of the upstream Code Puppy line (see PROVENANCE.md for the lineage
# and the compatibility contracts that keep the two honest).
GROVE_AUTHORS = {"tyler granlund", "t-granlund", "tyler"}


def _prov_chip(author: str | None) -> str:
    """Provenance chip from commit authorship — the living classification.

    Grove-grown vs upstream-synced is decided by evidence (who authored the
    commit), not by vibes, so the observatory stays accountable to the same
    ledger PROVENANCE.md keeps.
    """
    is_grove = (author or "").strip().lower() in GROVE_AUTHORS
    cls, label = ("gr", "grove") if is_grove else ("up", "upstream")
    title = (
        "Authored in the grove"
        if is_grove
        else "Authored upstream — synced via the Code Puppy line"
    )
    return f'<span class="prov {cls}" title="{title}">{label}</span>'


# Self-referential/maintenance feats that would just spam the auto-detected
# cards (site regen chores, i18n extraction sweeps, etc.).
NOISE_RE = re.compile(r"field-guide|changelog\.py|user-facing strings", re.IGNORECASE)


def _hash_key(c: dict) -> str:
    """Normalize to 7 chars so hand-authored (7-char) and data.js (8-char)
    hashes compare equal."""
    return (c.get("short_hash") or "")[:7]


def _load_data() -> dict:
    text = DATA_JS.read_text(encoding="utf-8").strip()
    for prefix in ("window.FIELD_GUIDE_DATA = ", "const FIELD_GUIDE_DATA = "):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    return json.loads(text.strip().rstrip(";\n"))


def _load_living() -> list[dict]:
    """Parse the dictation ledger between LIVING:BEGIN / LIVING:END markers.

    Entries look like:

        ### 2026-09-15 — Title
        - Source: ...
        - Status: shipped
        - Origin: grove-grown
        - free-form body bullet

    Tolerant by design: unknown fields become body bullets, a missing
    ledger file renders as an empty list (the page just omits the cards),
    and the protocol section outside the markers is ignored.
    """
    if not LIVING_MD.exists():
        return []
    text = LIVING_MD.read_text(encoding="utf-8")
    # rfind: the protocol prose at the top of the ledger mentions the marker
    # literals when describing the format — the real BEGIN is the last one.
    begin = text.rfind(LIVING_BEGIN)
    if begin == -1:
        return []
    end = text.find(LIVING_END, begin + len(LIVING_BEGIN))
    if end == -1:
        return []
    block = text[begin + len(LIVING_BEGIN) : end]

    entries: list[dict] = []
    for chunk in block.split("\n### ")[1:]:
        lines = chunk.strip().splitlines()
        title = lines[0].strip() if lines else ""
        # Fold soft-wrapped markdown bullets: a line that doesn't start with
        # "- " continues the previous bullet (prose wraps mid-sentence).
        items: list[str] = []
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("- "):
                items.append(stripped[2:])
            elif items:
                items[-1] += " " + stripped
        entry: dict = {"title": title, "fields": {}, "body": []}
        for item in items:
            m = re.match(r"^([A-Za-z][A-Za-z ]*?):\s+(.+)$", item)
            if m and m.group(1).lower() not in entry["fields"]:
                entry["fields"][m.group(1).lower()] = m.group(2).strip()
            else:
                entry["body"].append(item)
        entries.append(entry)
    return entries


def _inline_md(text: str) -> str:
    """Escape HTML, then honor `code`, **bold**, and *italic* spans."""
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    return out


def _living_cards(entries: list[dict]) -> str:
    """Render dictation-ledger entries as observatory cards."""
    if not entries:
        return ""
    cards = []
    for e in entries[:MAX_LIVING_CARDS]:
        status_raw = e["fields"].get("status", "idea").lower()
        label, chip_cls = LIVING_STATUS.get(status_raw, (status_raw, ""))
        chip = (
            f'<span class="chip {chip_cls}">{html.escape(label)}</span>'
            if chip_cls
            else f'<span class="chip">{html.escape(label)}</span>'
        )
        meta_bits = [chip]
        if source := e["fields"].get("source"):
            meta_bits.append(_inline_md(source))
        if origin := e["fields"].get("origin"):
            meta_bits.append(
                f'<span class="prov {"gr" if "grove" in origin else "up"}">'
                f"{html.escape(origin)}</span>"
            )
        body = "".join(f"        <dd>{_inline_md(b)}</dd>\n" for b in e["body"])
        if body:
            body = f'      <dl class="qa">\n        <dt class="q-what">What happened</dt>\n{body}      </dl>\n'
        cards.append(
            f'    <article class="deep">\n'
            f'      <div class="head"><h3>{_inline_md(e["title"])}</h3>'
            f'<span class="meta">{" · ".join(meta_bits)}</span></div>\n'
            f"{body}"
            f"    </article>"
        )
    count_note = f'<div class="pcount">{len(entries)} entries · newest first</div>'
    return count_note + "\n" + "\n".join(cards)


def _bucketize(commits: list[dict]) -> dict[str, list[dict]]:
    """Split commits into conventional-commit buckets, newest first."""
    buckets: dict[str, list[dict]] = defaultdict(list)
    for c in commits:
        subject = c.get("subject") or ""
        m = re.match(r"^([a-z]+)(\([^)]*\))?:\s*(.*)", subject)
        kind, msg = (m.group(1), m.group(3)) if m else ("other", subject)
        buckets[kind].append({**c, "kind": kind, "msg": msg})
    return buckets


def _short_date(iso: str) -> str:
    # '2026-08-17' -> '08-17'
    return "-".join((iso or "").split("-")[1:3]) or iso


def _list_items(commits: list[dict], exclude: set[str], limit: int) -> str:
    lines = []
    for c in commits:
        if _hash_key(c) in exclude:
            continue
        h = html.escape(c.get("short_hash", ""))
        d = html.escape(_short_date(c.get("date", "")))
        msg = html.escape(c.get("msg") or c.get("subject") or "")
        lines.append(
            '          <li><span class="h">%s</span>'
            '<span class="d">· %s</span> · %s%s</li>'
            % (h, d, msg, _prov_chip(c.get("author", "")))
        )
        if len(lines) >= limit:
            break
    return "\n".join(lines)


def _statline(data: dict, buckets: dict[str, list[dict]]) -> str:
    stats = data.get("stats", {})
    items = [
        ("commits", stats.get("commitsLast2Months", "?")),
        ("features", len(buckets.get("feat", []))),
        ("bug fixes", len(buckets.get("fix", []))),
        ("tools", stats.get("tools", "?")),
        ("agents", stats.get("agents", "?")),
        ("plugins", stats.get("plugins", "?")),
    ]
    return "\n".join(
        '      <div class="s"><div class="n">%s</div><div class="t">%s</div></div>'
        % (html.escape(str(number)), label)
        for label, number in items
    )


def _auto_cards(buckets: dict[str, list[dict]], curated: set[str]) -> str:
    """Cards for notable feats lacking a curated narrative yet."""
    fresh = [
        c
        for c in buckets.get("feat", [])
        if _hash_key(c) not in curated and not NOISE_RE.search(c.get("msg") or "")
    ]
    if not fresh:
        return ""
    cards = []
    for c in fresh[:MAX_AUTO_CARDS]:
        h = html.escape(c.get("short_hash", ""))
        d = html.escape(c.get("date", ""))
        msg = html.escape(c.get("msg") or "")
        prov = _prov_chip(c.get("author", ""))
        cards.append(f"""    <article class="deep" style="border-style:dashed">
      <div class="head"><h3>{msg}</h3><span class="meta"><span class="hash">{h}</span> · {d} · feat{prov}</span></div>
      <dl class="qa">
        <dt class="q-what">What it is</dt><dd>A feature that landed since the last curation pass.</dd>
        <dt class="q-do">What it does</dt><dd>See commit <code>{h}</code> in the repo for the implementation diff.</dd>
        <dt class="q-why">Why it matters</dt><dd>Auto-detected &mdash; a curated narrative will be added on the next observatory curation pass.</dd>
      </dl>
    </article>""")
    grove_n = sum(
        1
        for c in fresh[:MAX_AUTO_CARDS]
        if (c.get("author") or "").strip().lower() in GROVE_AUTHORS
    )
    up_n = len(fresh[:MAX_AUTO_CARDS]) - grove_n
    prov_count = (
        f' <span class="pcount">{grove_n} grove-grown · {up_n} upstream-synced</span>'
        if fresh
        else ""
    )
    return f"""  <!-- ================= AUTO-DETECTED ================= -->
  <section class="g" id="auto-detected">
    <h2>New Since Last Curation <span class="tag">auto-detected</span>{prov_count}</h2>
    <p class="secintro">Feature commits detected by the pipeline that haven't been
    curated into deep-dives yet. These render straight from the changelog so the page
    never goes stale between curation passes.</p>

{chr(10).join(cards)}
  </section>"""


def _replace_region(html_text: str, name: str, new_content: str) -> str:
    begin = f"<!-- AUTO-BEGIN:{name} -->"
    end = f"<!-- AUTO-END:{name} -->"
    idx_b = html_text.find(begin)
    idx_e = html_text.find(end)
    if idx_b == -1 or idx_e == -1:
        raise SystemExit(f"Missing markers for region '{name}' in updates.html")
    inner = f"\n{new_content}\n      " if new_content else ""
    return html_text[: idx_b + len(begin)] + inner + html_text[idx_e:]


def _strip_auto_regions(page: str) -> str:
    """Remove all AUTO-managed regions so curated-hash extraction only sees
    hand-authored content. Without this the generator would treat its own
    output as curated on the next run and churn the page non-idempotently."""
    return re.sub(
        r"<!-- AUTO-BEGIN:[a-z-]+ -->.*?<!-- AUTO-END:[a-z-]+ -->",
        "",
        page,
        flags=re.S,
    )


def main() -> None:
    data = _load_data()
    commits = data.get("changelog", {}).get("commits", [])
    buckets = _bucketize(commits)

    page = UPDATES_HTML.read_text(encoding="utf-8")

    # All hash citations below come from the page with auto regions stripped,
    # so repeated runs converge to a fixed point instead of rotating cards.
    authored = _strip_auto_regions(page)
    curated = {h[:7] for h in re.findall(r'class="hash">([0-9a-f]{6,10})<', authored)}
    cite_hashes = {
        h[:7] for h in re.findall(r'class="(?:hash|h)">([0-9a-f]{6,10})<', authored)
    }

    auto = _auto_cards(buckets, curated)

    # Lists skip anything already showcased (curated deep-dive, auto-card, or
    # hand-cited in an earlier list) to avoid duplicate coverage.
    excluded_from_lists = (
        cite_hashes
        | {
            _hash_key(c)
            for c in buckets.get("feat", [])
            if _hash_key(c) not in curated and not NOISE_RE.search(c.get("msg") or "")
        }
        | curated
    )

    page = _replace_region(page, "stats", _statline(data, buckets))
    page = _replace_region(page, "living-updates", _living_cards(_load_living()))
    page = _replace_region(page, "auto-features", auto)
    toc_link = (
        '      <li><a href="#auto-detected">New Since Last Curation</a></li>'
        if auto
        else ""
    )
    page = _replace_region(page, "toc", toc_link)

    minor_commits = [c for k in MINOR_KINDS for c in buckets.get(k, [])]
    minor_commits.sort(key=lambda c: c.get("date", ""), reverse=True)
    page = _replace_region(
        page,
        "minor-list",
        _list_items(minor_commits, excluded_from_lists, MAX_LIST_ITEMS),
    )
    page = _replace_region(
        page,
        "fixes-list",
        _list_items(buckets.get("fix", []), cite_hashes, MAX_LIST_ITEMS),
    )

    UPDATES_HTML.write_text(page, encoding="utf-8")
    auto_n = len(
        [
            c
            for c in buckets.get("feat", [])
            if _hash_key(c) not in curated and not NOISE_RE.search(c.get("msg") or "")
        ]
    )
    print(
        f"updates.html regenerated: {len(commits)} commits, "
        f"{len(buckets.get('feat', []))} feats ({auto_n} auto-detected uncurated), "
        f"{len(buckets.get('fix', []))} fixes"
    )


if __name__ == "__main__":
    main()
