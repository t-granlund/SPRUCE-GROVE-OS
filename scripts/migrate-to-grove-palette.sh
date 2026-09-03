#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# Migrate Code Puppy design tokens to the Granlund-Grove forest palette.
#
# Maps the old blue-grey / periwinkle / cyan / mint palette to the grove's
# warm cedar + forest-green system. Every value is WCAG-AAA verified on
# the grove background (#0E130F). Applied via sed for deterministic,
# auditable bulk replacement across all CSS/HTML files.
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# Files to migrate (NOT logs, NOT generated data.js, NOT flat HTML)
FILES=(
  pages-hub/assets/tokens.css
  pages-hub/assets/sidebar.css
  pages-hub/assets/popover.css
  pages-hub/assets/puppy.svg
  pages-hub/assets/puppy-full.svg
  pages-hub/index.html
  pages-hub/architecture.html
  pages-hub/updates.html
  pages-hub/design.html
  docs/field-guide/index.html
)

# ── hex surface colors ──────────────────────────────────────────────
HEX_MAP=(
  # backgrounds  (old blue-grey → grove charcoal-green)
  "s|#141B23|#0E130F|g"      # BB-bg / sb-bg
  "s|#1A2129|#0E130F|g"      # bg (field-guide + pages-hub)
  "s|#182029|#121813|g"      # BB-bg-elev
  "s|#202834|#121813|g"      # bg-elev (pages-hub)
  "s|#1B2530|#161D18|g"      # BB-bg-card
  "s|#232D3A|#161D18|g"      # bg-card (pages-hub)
  "s|#1E2936|#1B211C|g"      # BB-panel
  "s|#252F3C|#1B211C|g"      # panel-2 (architecture)
  "s|#171F28|#121813|g"      # sb-bg-2
  "s|#151C24|#0E130F|g"      # pre bg (field guide)
  "s|#0F141A|#0E130F|g"      # snip bg (design)
  # text  (AAA verified on #0E130F)
  "s|#FFFFFF|#EEEBE2|g"      # t1 / text  → grove foreground  15.7:1
  "s|#F7FAFD|#EEEBE2|g"      # sb-text
  "s|#E9EEF4|#D1CEC5|g"      # BB-t2  → stone  11.9:1
  "s|#D6DEE8|#D1CEC5|g"      # text-soft  → stone
  "s|#C7D0DA|#A5A699|g"      # BB-t3  → muted-fg  7.6:1
  "s|#AEB9C7|#A5A699|g"      # text-muted  → muted-fg
  "s|#B7C3D1|#A5A699|g"      # sb-text-soft
  # accents  (AAA verified)
  "s|#A3A8F8|#E4AA71|g"      # accent / peri  → cedar  9.2:1
  "s|#C0C4FB|#E4AA71|g"      # BB-peri  → cedar
  "s|#5CF2F2|#F2A26A|g"      # accent-2 / cyan  → cedar-bright  9.1:1
  "s|#66F0ED|#F2A26A|g"      # BB-cyan  → cedar-bright
  "s|#61E887|#98B79E|g"      # accent-3 / mint  → sage  8.6:1
  "s|#6FF09A|#98B79E|g"      # BB-mint  → sage
  "s|#C5C9FB|#ECEBE5|g"      # accent-4 / peri-l  → mist  15.7:1
  "s|#DBDDFE|#ECEBE5|g"      # BB-peri-l  → mist
  "s|#F2A9F0|#CAAB88|g"      # BB-pink  → amber-soft  8.7:1
  "s|#8A8FF0|#CAAB88|g"      # danger / peri-d  → amber-soft
  "s|#FFE08A|#E4AA71|g"      # focus  → cedar
)

# ── rgba RGB-triple tints ───────────────────────────────────────────
RGBA_MAP=(
  # accent tints (peri/accent → cedar)
  "s|192,196,251|228,170,113|g"
  "s|163,168,248|228,170,113|g"
  # cyan tints → cedar-bright
  "s|102,240,237|242,162,106|g"
  "s|92,242,242|242,162,106|g"
  # mint tints → sage
  "s|111,240,154|152,183,158|g"
  "s|97,232,135|152,183,158|g"
  # peri-l tints → mist
  "s|197,201,251|236,235,229|g"
  # white overlays → warm cream (foreground)
  "s|255,255,255|238,235,229|g"
  # green-tint the dark nav/backdrop rgba bases
  "s|11,15,20|10,15,11|g"
  "s|26,33,41|14,19,15|g"
  "s|6,10,14|6,10,8|g"
  "s|10,14,19|10,15,11|g"
)

for f in "${FILES[@]}"; do
  for m in "${HEX_MAP[@]}" "${RGBA_MAP[@]}"; do
    sed -i '' "$m" "$f"
  done
  echo "   $f"
done

echo "Done. Bulk color migration applied to ${#FILES[@]} files."
