#!/usr/bin/env bash
# build-site.sh -- compose the GitHub Pages artifact from repo sources.
#
# Single source of truth for the PUBLISHED LAYOUT. CI calls this, and the
# site tests build through it too, so "what deploys" and "what we verify"
# cannot drift apart. `_site/` is a BUILD OUTPUT (gitignored) -- never edit
# it by hand, and never commit it: a tracked copy that goes stale is how the
# repo once published a page the sources no longer agreed with.
#
#   ./scripts/build-site.sh            # -> <repo>/_site
#   ./scripts/build-site.sh /tmp/site  # -> an explicit directory (tests)
#
# The relative asset prefixes (`./assets/` vs `../assets/`) are decided HERE,
# by where each page lands -- not in the page sources. A page copied to
# `_site/mechanics/index.html` needs `../assets/`, and that is why the source
# already carries it. When you add a page, add its copy line below and put it
# where its existing prefixes already resolve.
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/_site}"

# Normalize to an absolute path FIRST: CI passes the relative `_site`, which
# the guard below would otherwise reject because it checks the literal string.
case "$OUT" in
  /*) ;;
  *) OUT="$ROOT/$OUT" ;;
esac

case "$OUT" in
  "$ROOT"/* | /tmp/*) ;;
  *) echo "build-site: refusing to build into $OUT (must be under $ROOT or /tmp)" >&2; exit 2 ;;
esac

cd "$ROOT"
rm -rf "$OUT"
mkdir -p "$OUT"

# 1. Landing hub at the root + shared assets (logo, favicon)
cp pages-hub/owners.html    "$OUT/index.html"
cp pages-hub/announce.html  "$OUT/announce.html"
cp pages-hub/owners.html    "$OUT/owners.html"
cp pages-hub/product.html   "$OUT/product.html"
cp pages-hub/interested.html "$OUT/interested.html"
cp pages-hub/share.html     "$OUT/share.html"
cp pages-hub/plan.html      "$OUT/plan.html"
cp pages-hub/index.html     "$OUT/hub.html"
cp pages-hub/desktop-dashboard.html "$OUT/"
cp pages-hub/dashboard.html "$OUT/"
cp -r pages-hub/assets "$OUT/"

# Inject live platform stats from the field guide data into the hub.
# stdlib Python only -- no node/npm anywhere in the build.
python3 - "$OUT" <<'PYEOF'
import json, sys
from pathlib import Path

out = Path(sys.argv[1])
text = (Path("docs/field-guide/data.js")).read_text(encoding="utf-8").strip()
for prefix in ("window.FIELD_GUIDE_DATA = ", "const FIELD_GUIDE_DATA = "):
    if text.startswith(prefix):
        text = text[len(prefix):]
        break
stats = json.loads(text.strip().rstrip(";\n")).get("stats", {})

hub = out / "hub.html"
html = hub.read_text(encoding="utf-8")
for key, stat in (
    ("s-tools", "tools"),
    ("s-agents", "agents"),
    ("s-plugins", "plugins"),
    ("s-commits", "commitsLast2Months"),
):
    html = html.replace(f'id="{key}">—<', f'id="{key}">{stats.get(stat, "—")}<')
hub.write_text(html, encoding="utf-8")
PYEOF

# 2. Interactive field guide explorer (a self-contained sub-site: own assets/)
mkdir -p "$OUT/field-guide"
cp -r docs/field-guide/. "$OUT/field-guide/"

# 3. Nested pages: copied to <dir>/index.html, so they use ../assets/
mkdir -p "$OUT/releases"
cp pages-hub/updates.html "$OUT/releases/index.html"
mkdir -p "$OUT/architecture"
cp pages-hub/architecture.html "$OUT/architecture/index.html"
mkdir -p "$OUT/design"
cp pages-hub/design.html "$OUT/design/index.html"
mkdir -p "$OUT/mechanics"
cp pages-hub/mechanics.html "$OUT/mechanics/index.html"
mkdir -p "$OUT/council"
cp pages-hub/council.html "$OUT/council/index.html"
mkdir -p "$OUT/manifesto"
cp pages-hub/manifesto.html "$OUT/manifesto/index.html"

# 4. Fully-offline flat file
mkdir -p "$OUT/flat"
cp docs/field-guide-flat.html "$OUT/flat/index.html"

# 5. Roadmap boards at the site root (same ./assets/ resolution as the hub)
cp pages-hub/phases.html   "$OUT/phases.html"
cp pages-hub/progress.html "$OUT/progress.html"

# 6. Custom domain (sprucegrove.io, purchased 2026-09-11 at Porkbun).
#    Matches the Pages settings cname so an Actions build always carries the
#    domain, even after settings drift.
echo "sprucegrove.io" > "$OUT/CNAME"

# 7. Stop GitHub Pages from Jekyll-transforming anything
touch "$OUT/.nojekyll"

echo "build-site: composed $(find "$OUT" -type f | wc -l | tr -d ' ') files into $OUT"
