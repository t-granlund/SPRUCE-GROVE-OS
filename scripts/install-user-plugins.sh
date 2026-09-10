#!/usr/bin/env bash
# Install the grove's user-tier plugins (and their shared lib) from this repo
# into ~/.spruce_grove/, where the CLI discovers them at startup.
#
# The copies in user-plugins/ are canonical: edit there, then re-run this.
# Copy-only by design -- never deletes, so a stale repo copy can never clobber
# a newer live plugin.
#
# Usage: scripts/install-user-plugins.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/user-plugins"
DEST_PLUGINS="${SPRUCE_PLUGINS_DIR:-$HOME/.spruce_grove/plugins}"
DEST_LIB="${SPRUCE_LIB_DIR:-$HOME/.spruce_grove/lib}"

if [[ ! -d "$SRC" ]]; then
  echo "error: $SRC not found (run from a full checkout)" >&2
  exit 1
fi

mkdir -p "$DEST_PLUGINS" "$DEST_LIB"

shopt -s nullglob
installed=()
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  # underscore-prefixed dirs are support trees (e.g. _lib), not plugins --
  # same convention the plugin loader uses to skip them.
  [[ "$name" == _* ]] && continue
  rsync -a --exclude='__pycache__' --exclude='*.pyc' "$d" "$DEST_PLUGINS/$name"
  installed+=("$name")
done

if [[ -d "$SRC/_lib" ]]; then
  rsync -a --exclude='__pycache__' --exclude='*.pyc' "$SRC/_lib/" "$DEST_LIB/"
fi

if [[ ${#installed[@]} -eq 0 ]]; then
  echo "error: no plugins found in $SRC" >&2
  exit 1
fi

echo "installed ${#installed[@]} plugin(s) to $DEST_PLUGINS: ${installed[*]}"
echo "shared lib synced to $DEST_LIB (if present)"
echo "note: restart any running grove session -- plugins load at startup."
