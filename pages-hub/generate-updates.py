#!/usr/bin/env python3
"""Regenerate the auto-managed regions of pages-hub/updates.html.

Reads the field-guide changelog data (docs/field-guide/data.js) and rewrites
only the content between <!-- AUTO-BEGIN:name --> / <!-- AUTO-END:name -->
markers. Hand-curated deep-dive narratives outside the markers are untouched.

Auto-managed regions:
  stats          - hero statline numbers (commits/features/fixes/tools/agents/plugins)
  toc            - link to the auto-detected section (appears only when needed)
  auto-features  - cards for notable feat commits not yet curated into deep-dives
  minor-list     - recent minor enhancements (feat/refactor/perf/docs buckets)
  fixes-list     - recent bug fixes (fix bucket)

Run by ~/.code_puppy/scripts/update-code-puppy.sh after field-guide regen,
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

MAX_LIST_ITEMS = 18
MAX_AUTO_CARDS = 12

# Ordered list (NOT a set) so output is deterministic across runs regardless
# of Python's hash randomization.
MINOR_KINDS = ["feat", "refactor", "perf", "polish", "docs", "style"]

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
            text = text[len(prefix):]
            break
    return json.loads(text.strip().rstrip(";\n"))


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
            '<span class="d">· %s</span> · %s</li>' % (h, d, msg)
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
        cards.append(f"""    <article class="deep" style="border-style:dashed">
      <div class="head"><h3>{msg}</h3><span class="meta"><span class="hash">{h}</span> · {d} · feat</span></div>
      <dl class="qa">
        <dt class="q-what">What it is</dt><dd>A feature that landed since the last curation pass.</dd>
        <dt class="q-do">What it does</dt><dd>See commit <code>{h}</code> in the repo for the implementation diff.</dd>
        <dt class="q-why">Why it matters</dt><dd>Auto-detected &mdash; a curated narrative will be added on the next observatory curation pass.</dd>
      </dl>
    </article>""")
    return f"""  <!-- ================= AUTO-DETECTED ================= -->
  <section class="g" id="auto-detected">
    <h2>New Since Last Curation <span class="tag">auto-detected</span></h2>
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
        "", page, flags=re.S,
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
        h[:7]
        for h in re.findall(r'class="(?:hash|h)">([0-9a-f]{6,10})<', authored)
    }

    auto = _auto_cards(buckets, curated)

    # Lists skip anything already showcased (curated deep-dive, auto-card, or
    # hand-cited in an earlier list) to avoid duplicate coverage.
    excluded_from_lists = cite_hashes | {
        _hash_key(c)
        for c in buckets.get("feat", [])
        if _hash_key(c) not in curated and not NOISE_RE.search(c.get("msg") or "")
    } | curated

    page = _replace_region(page, "stats", _statline(data, buckets))
    page = _replace_region(page, "auto-features", auto)
    toc_link = ('      <li><a href="#auto-detected">New Since Last Curation</a></li>'
                if auto else "")
    page = _replace_region(page, "toc", toc_link)

    minor_commits = [c for k in MINOR_KINDS for c in buckets.get(k, [])]
    minor_commits.sort(key=lambda c: c.get("date", ""), reverse=True)
    page = _replace_region(page, "minor-list",
                           _list_items(minor_commits, excluded_from_lists, MAX_LIST_ITEMS))
    page = _replace_region(page, "fixes-list",
                           _list_items(buckets.get("fix", []), cite_hashes, MAX_LIST_ITEMS))

    UPDATES_HTML.write_text(page, encoding="utf-8")
    auto_n = len(
        [c for c in buckets.get("feat", [])
         if _hash_key(c) not in curated and not NOISE_RE.search(c.get("msg") or "")]
    )
    print(f"updates.html regenerated: {len(commits)} commits, "
          f"{len(buckets.get('feat', []))} feats ({auto_n} auto-detected uncurated), "
          f"{len(buckets.get('fix', []))} fixes")


if __name__ == "__main__":
    main()
