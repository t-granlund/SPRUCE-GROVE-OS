#!/usr/bin/env bash
# brand_personal_guard.sh -- merge-discipline + privacy pre-commit guard (sg-5al.1)
#
# Two hard fails, kept deliberately dumb and greppable:
#   1. PUPPY NAMESPACE LEAK: a bare `import code_puppy` / `from code_puppy ...`
#      statement inside spruce_grove/ core. The L4 rebrand is prepaid; the only
#      legal sponsor of the legacy namespace is spruce_grove/_code_puppy_compat.py
#      (core-plugin packages in the venv may import it -- they are out of scope).
#   2. PRIVATE FILE TRACKING: anything matching the MASTER-MASTER-PROMPT family
#      (voice memo, transcript, captions) or raw .m4a voice memos. The fork is
#      PUBLIC -- staged files are publishable. Local-only means local-only.
#
# Usage:
#   scripts/brand_personal_guard.sh [staged_files...]   # from lefthook / hook shim
#   scripts/brand_personal_guard.sh --all                # whole-tree audit (CI/manual)

set -u

# Import statements only. Matches `import code_puppy`, `import code_puppy.config`,
# `from code_puppy import x`; deliberately does NOT match `code_puppy_core_plugins`
# (underscore continuation is a legal package name).
PUPPY_RE='^[[:space:]]*(import|from)[[:space:]]+code_puppy([[:space:]]|\.|$)'
SHIM='spruce_grove/_code_puppy_compat.py'

fail=0

block() {
    printf 'brand-personal-guard: BLOCKED: %s\n' "$1" >&2
    printf '  reason: %s\n' "$2" >&2
    fail=1
}

check_path() {
    local f="$1"
    case "$f" in
        *MASTER-MASTER-PROMPT* | *.m4a | *.M4A)
            block "$f" "private voice-memo family file; the fork is public (keep local, keep gitignored)"
            ;;
    esac
}

# Grandfathered at guard install (sg-5al.1): files that ALREADY imported the
# legacy namespace before the guard existed. The guard's job is ratchet, not
# retroactive execution: these must shrink over time, never grow. New files
# get no mercy; new imports in these files get no mercy either.
# Emptied by sg-5al.8 (all four rerouted to spruce_grove.*); keep this EMPTY.
GRANDFATHERED=''


check_imports() {
    local f="$1"
    case "$f" in
        "$SHIM") return ;; # the shim is the legal sponsor -- but keep path hygiene above
        spruce_grove/*.py) ;;
        *) return ;;
    esac
    local hits
    hits="$(grep -nE "$PUPPY_RE" "$f" 2>/dev/null || true)"
    [[ -z "$hits" ]] && return
    if printf '%s\n' "$GRANDFATHERED" | grep -qx -- "$f"; then
        # Ratchet: only the legacy import lines already present at HEAD survive.
        # Any ADDITIONAL bare-legacy import line in a grandfathered file fails.
        base_hits="$(git show "HEAD:$f" 2>/dev/null | grep -E "$PUPPY_RE" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g' || true)"
        while IFS= read -r raw; do
            norm="$(printf '%s' "$raw" | sed -E 's/^[0-9]+://; s/^[[:space:]]+|[[:space:]]+$//g')"
            [[ -z "$norm" ]] && continue
            if ! printf '%s\n' "$base_hits" | grep -qxF -- "$norm"; then
                block "$f" "new bare legacy import in grandfathered file: $norm"
            fi
        done <<< "$hits"
        return
    fi
    block "$f" "bare legacy-namespace import (grep: $PUPPY_RE); route via spruce_grove._code_puppy_compat instead"
}

all_mode=0
if [[ "${1:-}" == "--all" ]]; then
    all_mode=1
    shift
    while IFS= read -r f; do
        check_path "$f"
        check_imports "$f"
    done < <(git ls-files)
else
    for f in "$@"; do
        check_path "$f"
        [[ -f "$f" ]] && check_imports "$f"
    done
fi

if [[ "$fail" -ne 0 ]]; then
    printf 'brand-personal-guard: commit blocked. Fix the files above and stage again.\n' >&2
    exit 1
fi
if [[ "$all_mode" -eq 1 ]]; then
    printf '\033[32mbrand-personal-guard: OK -- no legacy-namespace leaks, no private files tracked (GRANDFATHERED empty)\033[0m\n'
fi
exit 0
