#!/usr/bin/env bash
# fresh_history_export.sh — clean-history export for the steward migration.
#
# Produces a copy of this repository whose history is rewritten under the
# steward identity (no personal names, no corporate emails). The original
# repository is untouched; the output is a NEW local repo you review before
# anything is pushed anywhere.
#
# Requirements: git-filter-repo  (uv tool install git-filter-repo)
#
# Usage: fresh_history_export.sh "<Steward Name>" "<steward@email>" [out-dir]
set -euo pipefail

NAME="${1:?usage: fresh_history_export.sh '<Steward Name>' '<steward@email>' [out-dir]}"
EMAIL="${2:?usage: fresh_history_export.sh '<Steward Name>' '<steward@email>' [out-dir]}"
OUT="${3:-$HOME/spruce-grove-sovereignty/fresh-history}"

command -v git-filter-repo >/dev/null 2>&1 || {
  echo "git-filter-repo is required:"
  echo "  uv tool install git-filter-repo"
  exit 1
}

SRC="$(git rev-parse --show-toplevel)"
STAMP="$(date +%Y%m%d-%H%M%S)"
DEST="$OUT/SPRUCE-GROVE-OS-$STAMP"

echo "== Clean-history export -> $DEST"
git clone --no-hardlinks "$SRC" "$DEST"
cd "$DEST"

# Rewrite author/committer identity across all of history.
cat > .mailmap-export <<EOF
$NAME <$EMAIL> <$EMAIL>
EOF
git filter-repo \
  --name-callback 'return "'"$NAME"'"' \
  --email-callback 'return "'"$EMAIL"'"' \
  --force

# Re-point origin at nothing (the steward chooses the new home).
git remote remove origin 2>/dev/null || true

echo "== History rewritten: $(git log --format='%an <%ae>' | sort -u | tr '\n' ' ')"
echo "== REVIEW THIS COPY before pushing anywhere:"
echo "   git -C $DEST log --oneline | head"
echo "   Note: tags carry old identities too — re-tag from the new history if"
echo "   the steward standard requires it (filter-repo rewrote refs by default)."
