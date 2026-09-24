#!/usr/bin/env bash
# sync-brand-assets.sh - single source of truth for the brand.
# Masters live in SPRUCE-GROVE-OS/logos/. Every other surface CONSUMES copies.
#   ./scripts/sync-brand-assets.sh          promote masters -> all surfaces
#   ./scripts/sync-brand-assets.sh --check  exit 1 if any consumer drifted
# Portable: no associative arrays (macOS ships bash 3.2).
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGOS="$ROOT/logos"
CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

repo_path() {
  case "$1" in
    pages-hub)          echo "$ROOT/pages-hub" ;;
    docs/field-guide)   echo "$ROOT/docs/field-guide" ;;
    spruce-grove-desktop) echo "$HOME/spruce-grove-desktop" ;;
    code_puppy)         echo "$HOME/code_puppy" ;;
    leather-apron-club) echo "$HOME/leather-apron-club" ;;
    *)                  echo "" ;;
  esac
}

PAIRS="pages-hub|assets/favicon-64.png|favicon-64.png
pages-hub|assets/apple-touch-icon.png|apple-touch-icon.png
pages-hub|assets/spruce_grove_official.png|spruce_grove_official.png
pages-hub|assets/grove-mark.svg|spruce-grove-mark.svg
pages-hub|assets/spruce-core-disc.svg|spruce-core-disc.svg
docs/field-guide|assets/favicon-64.png|favicon-64.png
docs/field-guide|assets/apple-touch-icon.png|apple-touch-icon.png
docs/field-guide|assets/spruce-grove-mark.svg|spruce-grove-mark.svg
spruce-grove-desktop|assets/grove-mark.svg|spruce-grove-mark.svg
spruce-grove-desktop|assets/spruce-grove-lockup-stacked.svg|spruce-grove-lockup-stacked.svg
spruce-grove-desktop|assets/spruce-core-disc.svg|spruce-core-disc.svg
code_puppy|docs/decks/the-great-adpuppytion/leather-apron-club/assets/favicon-64.png|favicon-64.png
code_puppy|docs/decks/the-great-adpuppytion/leather-apron-club/assets/apple-touch-icon.png|apple-touch-icon.png
code_puppy|docs/decks/the-great-adpuppytion/leather-apron-club/assets/spruce_grove_official.png|spruce_grove_official.png
code_puppy|docs/decks/the-great-adpuppytion/leather-apron-club/assets/spruce_grove_official.svg|spruce_grove_official.svg
code_puppy|docs/decks/the-great-adpuppytion/leather-apron-club/assets/spruce_grove_official_line.svg|spruce_grove_official_line.svg
leather-apron-club|works/assets/favicon-64.png|favicon-64.png
leather-apron-club|works/assets/apple-touch-icon.png|apple-touch-icon.png
leather-apron-club|works/assets/spruce_grove_official.png|spruce_grove_official.png"

echo "$PAIRS" | while IFS='|' read -r repo dest master; do
  [ -z "$repo" ] && continue
  base=$(repo_path "$repo")
  if [ -z "$base" ]; then echo "UNKNOWN REPO: $repo"; continue; fi
  src="$LOGOS/$master"
  dst="$base/$dest"
  if [ ! -f "$src" ]; then echo "MISSING MASTER: $src"; continue; fi
  if [ ! -f "$dst" ]; then
    echo "MISSING CONSUMER: $dst"
    if [ $CHECK -eq 0 ]; then mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"; echo "  -> copied"; fi
    continue
  fi
  if ! cmp -s "$src" "$dst"; then
    if [ $CHECK -eq 1 ]; then
      echo "DRIFT: $dst != logos/$master"
    else
      cp "$src" "$dst"
      echo "synced: $dst"
    fi
  fi
done

if [ "$CHECK" -eq 1 ]; then
  if echo "$PAIRS" | while IFS='|' read -r repo dest master; do
    [ -z "$repo" ] && continue
    base=$(repo_path "$repo"); [ -z "$base" ] && continue
    src="$LOGOS/$master"; dst="$base/$dest"
    if [ -f "$src" ] && [ ! -f "$dst" ]; then echo "DRIFT"; fi
    if [ -f "$src" ] && [ -f "$dst" ] && ! cmp -s "$src" "$dst"; then echo "DRIFT"; fi
  done | grep -q DRIFT; then
    echo "brand assets have drifted - run scripts/sync-brand-assets.sh and commit"
    exit 1
  fi
  echo "brand assets: all consumers in sync with logos/ masters"
else
  echo "brand assets: sync pass complete"
fi
