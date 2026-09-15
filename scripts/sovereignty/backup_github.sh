#!/usr/bin/env bash
# backup_github.sh — the 3-2-1 insurance snapshot (AUTO, read-only).
#
# Mirror-clones every repo under the steward-origin account, dumps issues
# and releases metadata, and seals the bundle with a hash manifest.
# Output: ~/spruce-grove-sovereignty/backups/<datestamp>/
#
# Usage: backup_github.sh [account]   (default: t-granlund)
set -euo pipefail

ACCOUNT="${1:-t-granlund}"
STAMP="$(date +%Y%m%d-%H%M%S)"
DEST="$HOME/spruce-grove-sovereignty/backups/$STAMP"
mkdir -p "$DEST/repos" "$DEST/meta"

echo "== Insurance snapshot of $ACCOUNT -> $DEST =="

for repo in $(gh repo list "$ACCOUNT" --limit 100 --json name --jq '.[].name'); do
  echo "-- mirror: $repo"
  gh repo clone "$ACCOUNT/$repo" "$DEST/repos/$repo" -- --mirror --quiet 2>/dev/null \
    || echo "   (clone skipped/failed — recorded)"
done

echo "-- issues + releases metadata"
for repo in $(gh repo list "$ACCOUNT" --limit 100 --json name --jq '.[].name'); do
  gh api "repos/$ACCOUNT/$repo/issues?state=all&per_page=100" \
    > "$DEST/meta/$repo.issues.json" 2>/dev/null || echo "[]" > "$DEST/meta/$repo.issues.json"
  gh api "repos/$ACCOUNT/$repo/releases?per_page=100" \
    > "$DEST/meta/$repo.releases.json" 2>/dev/null || echo "[]" > "$DEST/meta/$repo.releases.json"
done

echo "-- sealing manifest"
( cd "$DEST" && find . -type f -exec shasum -a 256 {} + | sort > manifest.sha256 )
tar -czf "$DEST.tar.gz" -C "$(dirname "$DEST")" "$(basename "$DEST")"
shasum -a 256 "$DEST.tar.gz" > "$DEST.tar.gz.sha256"

echo "== Bundle sealed: $DEST.tar.gz"
echo "== Copy it somewhere else NOW (3-2-1): second medium + offsite."
