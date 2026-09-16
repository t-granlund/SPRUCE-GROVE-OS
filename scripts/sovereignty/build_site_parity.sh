#!/usr/bin/env bash
# build_site_parity.sh — reproduce the Pages build locally and hash the artifact.
#
# Proof for the migration (SOVEREIGNTY-INFRASTRUCTURE.md Phase C): the new
# rails must serve byte-identical output. Run this before and after any
# rails change; the hashes must match.
#
# Usage: build_site_parity.sh   (repo root; writes dist/_site + SHA256 manifest)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

SITE=_site
rm -rf "$SITE"
mkdir -p "$SITE"

# — same steps as .github/workflows/pages.yml —
cp pages-hub/owners.html "$SITE/index.html"
for f in announce owners product interested share plan; do
  cp "pages-hub/$f.html" "$SITE/$f.html"
done
cp pages-hub/index.html "$SITE/hub.html"
cp pages-hub/desktop-dashboard.html "$SITE/"
cp pages-hub/dashboard.html "$SITE/"
cp -r pages-hub/assets "$SITE/"
cp pages-hub/phases.html "$SITE/phases.html"
cp pages-hub/progress.html "$SITE/progress.html"
for sub in field-guide flat architecture releases council mechanics design; do
  mkdir -p "$SITE/$sub"
done
cp -r docs/field-guide/. "$SITE/field-guide/"
cp pages-hub/updates.html "$SITE/releases/index.html"
cp pages-hub/architecture.html "$SITE/architecture/index.html"
cp pages-hub/design.html "$SITE/design/index.html"
cp pages-hub/mechanics.html "$SITE/mechanics/index.html"
cp pages-hub/council.html "$SITE/council/index.html"
cp docs/field-guide-flat.html "$SITE/flat/index.html"

# stats injection (stdlib python — mirrors the workflow step)
python3 - <<'PY'
import json
text = open("docs/field-guide/data.js", encoding="utf-8").read().strip()
for prefix in ("window.FIELD_GUIDE_DATA = ", "const FIELD_GUIDE_DATA = "):
    if text.startswith(prefix):
        text = text[len(prefix):]
        break
data = json.loads(text.strip().rstrip(";\n"))
stats = data.get("stats", {})
p = "_site/hub.html"
html = open(p, encoding="utf-8").read()
for key, stat in (("s-tools", "tools"), ("s-agents", "agents"),
                  ("s-plugins", "plugins"), ("s-commits", "commitsLast2Months")):
    html = html.replace(f'id="{key}">—<', f'id="{key}">{stats.get(stat, "—")}<')
open(p, "w", encoding="utf-8").write(html)
PY

echo "sprucegrove.io" > "$SITE/CNAME"
touch "$SITE/.nojekyll"

# — seal —
( cd "$SITE" && find . -type f -exec shasum -a 256 {} + | sort > ../_site.sha256 )
echo "== artifact: $SITE ($(find "$SITE" -type f | wc -l | tr -d ' ') files)"
echo "== manifest: _site.sha256"
echo "== diff vs previous run: shasum -a 256 -c _site.sha256 (from the artifact root)"
