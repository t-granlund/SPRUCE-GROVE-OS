#!/usr/bin/env bash
# sync-brand-assets.sh — single source of truth for the brand.
# Masters live in SPRUCE-GROVE-OS/logos/. Every other surface CONSUMES copies.
# Run without args to sync; run with --check in CI to fail on drift.
#
#   ./scripts/sync-brand-assets.sh          # promote masters -> all surfaces
#   ./scripts/sync-brand-assets.sh --check  # exit 1 if any consumer drifted
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGOS="$ROOT/logos"
CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

# consumer: relative-to-root label  master  ->  dest
PAIRS=(
  "pages-hub assets/favicon-64.png               favicon-64.png"
  "pages-hub assets/apple-touch-icon.png         apple-touch-icon.png"
  "pages-hub assets/spruce_grove_official.png    spruce_grove_official.png"
  "code_puppy docs/decks/the-great-adpuppytion/leather-apron-club/assets/favicon-64.png        favicon-64.png"
  "code_puppy docs/decks/the-great-adpuppytion/leather-apron-club/assets/apple-touch-icon.png  apple-touch-icon.png"
  "code_puppy docs/decks/the-great-adpuppytion/leather-apron-club/assets/spruce_grove_official.png   spruce_grove_official.png"
  "code_puppy docs/decks/the-great-adpuppytion/leather-apron-club/assets/spruce_grove_official.svg   spruce_grove_official.svg"
  "code_puppy docs/decks/the-great-adpuppytion/leather-apron-club/assets/spruce_grove_official_line.svg spruce_grove_official_line.svg"
  "leather-apron-club works/assets/favicon-64.png          favicon-64.png"
  "leather-apron-club works/assets/apple-touch-icon.png    apple-touch-icon.png"
  "leather-apron-club works/assets/spruce_grove_official.png spruce_grove_official.png"
)

declare -A REPO_OF=( [pages-hub]="$ROOT" [code_puppy]="$HOME/code_puppy" [leather-apron-club]="$HOME/leather-apron-club" )

drift=0
for entry in "${PAIRS[@]}"; do
  read -r repo dest master <<< "$entry"
  src="$LOGOS/$master"
  dst="${REPO_OF[$repo]}/$dest"
  if [[ ! -f "$src" ]]; then echo "MISSING MASTER: $src"; drift=1; continue; fi
  if [[ ! -f "$dst" ]]; then
    echo "MISSING CONSUMER: $dst"; drift=1
    [[ $CHECK -eq 0 ]] && { mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"; echo "  -> copied"; }
    continue
  fi
  if ! cmp -s "$src" "$dst"; then
    if [[ $CHECK -eq 1 ]]; then
      echo "DRIFT: $dst != logos/$master"
      drift=1
    else
      cp "$src" "$dst"
      echo "synced: $dst"
    fi
  fi
done

if [[ $CHECK -eq 1 ]]; then
  if [[ $drift -eq 1 ]]; then
    echo "brand assets have drifted — run scripts/sync-brand-assets.sh and commit"
    exit 1
  fi
  echo "brand assets: all consumers in sync with logos/ masters"
else
  [[ $drift -eq 0 ]] && echo "brand assets: nothing to do"
fi
