#!/usr/bin/env bash
# arm_the_wall.sh — branch protection + release environment for the Approval Wall.
#
# Owner: PAIRED (script is safe to run any time; --enforce-reviews flips on
# the review requirement — run that only when the steward handles exist,
# because until then it would block the current direct-push flow).
#
# Usage:
#   arm_the_wall.sh              # soft mode: protect history, keep direct pushes
#   arm_the_wall.sh --enforce-reviews 1   # require N reviews on every PR to main
#
# Requires: gh CLI authenticated with admin on the repo.
set -euo pipefail

REPO="${REPO:-t-granlund/SPRUCE-GROVE-OS}"
BRANCH="${BRANCH:-main}"
REVIEWS=0
[[ "${1:-}" == "--enforce-reviews" ]] && REVIEWS="${2:-1}"

echo "== Arming the wall on $REPO@$BRANCH (required reviews: $REVIEWS) =="

# 1. Branch protection: no force pushes, no deletions; optional review floor.
#    (allow_force_pushes / allow_deletions false = history integrity.)
gh api -X PUT "repos/$REPO/branches/$BRANCH/protection" \
  --input - <<EOF
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": $( [ "$REVIEWS" -gt 0 ] && \
    printf '{"required_approving_review_count": %s, "require_code_owner_reviews": true}' "$REVIEWS" || \
    echo "null" ),
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
echo "   branch protection applied."

# 2. Release environment (the publish job's gate). NOTE: required reviewers
#    for an environment are UI-only — the script creates it and prints the
#    exact remaining click. See GOVERNANCE.md (The Approval Wall).
gh api -X PUT "repos/$REPO/environments/release" \
  --input - <<'EOF'
{"deployment_branch_policy": {"protected_branches": true, "custom_branch_policies": false}}
EOF
echo "   'release' environment created."
echo "   STEWARD-ONLY step: Repo Settings → Environments → release →"
echo "   'Required reviewers' → add the steward handles. The publish"
echo "   workflow must reference environment: release to be gated by it."

# 3. Add environment gate to the publish workflow if not present.
WF=".github/workflows/publish.yml"
if [[ -f "$WF" ]] && ! grep -q "environment: release" "$WF"; then
  python3 - "$WF" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old = "  build-publish:\n    runs-on: ubuntu-latest\n    needs: test\n"
new = ("  build-publish:\n    runs-on: ubuntu-latest\n    needs: test\n"
       "    environment: release\n")
assert old in s, "publish job anchor not found"
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("   publish.yml now targets environment: release")
PY
else
  echo "   publish workflow already references the release environment (or file missing)."
fi

echo "== Done. The wall state: history protected; review floor: $REVIEWS; =="
echo "== release environment gated at: Settings → Environments → release. =="
