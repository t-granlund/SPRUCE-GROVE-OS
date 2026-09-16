# SOVEREIGNTY EXECUTION — the task board

> The scaffold for `docs/SOVEREIGNTY-INFRASTRUCTURE.md` and the
> governance adoption (`GOVERNANCE.md`). Every task has exactly one owner:
> **TYLER** (identity, payment, ceremony, approval) · **AUTO** (a script —
> run any time, verified) · **PAIRED** (script prepares, Tyler executes
> the ceremony). Status lives in the checkboxes; this board is updated in
> every council session.
>
> Local steward workspace: `~/spruce-grove-sovereignty/` (never committed).

---

## Phase A — Steward identity (all TYLER; nothing here can be automated)

- [ ] **A1** Choose the steward name (no ties to any person/place/employer).
- [ ] **A2** Create the steward email; enroll it in the shared vault.
- [ ] **A3** Password manager with two-person steward vault access.
- [ ] **A4** Order hardware keys (2 per steward). Enroll on: email, vault,
      registrar, git host, CI.
- [ ] **A5** Write the sealed recovery kit (both stewards, separate places).

## Phase B — Domains

- [x] **B1** Domain/DNS inventory — **AUTO, done 2026-09-15**
      (`~/spruce-grove-sovereignty/inventory/dns_sprucegrove_io.txt`):
      sprucegrove.io @ Porkbun, WHOIS privacy already ON ("Private by
      Design"), expires 2027-09-11, DNS on Porkbun NS, A records → GitHub
      Pages. tylergranlund.com @ Cloudflare (personal — council decision:
      keep personal, never project infra).
- [ ] **B2** **TYLER**: create the steward registrar account (privacy-first
      registrar or Porkbun sub-account) + bind hardware keys.
- [ ] **B3** **TYLER**: transfer sprucegrove.io into the steward account;
      re-delegate DNS to the steward nameservers at cutover.
- [ ] **B4** **PAIRED**: DNSSEC on; every record documented in the vault
      (script will export records: `inventory_domains.sh`).

## Phase C — Source control & release rails

- [x] **C1** GitHub asset inventory — **AUTO, done 2026-09-15**
      (`~/spruce-grove-sovereignty/inventory/github_inventory.txt`):
      28 repos under the legacy identity; SPRUCE-GROVE-OS has Pages ON,
      zero external collaborators, zero Action secrets (publishing is
      OIDC — nothing to rotate), and **no branch protection on main**
      (the wall is not armed yet — see W1).
- [x] **C2** Full backup bundle — **AUTO**:
      `scripts/sovereignty/backup_github.sh` (mirror-clone every repo +
      issues/releases JSON + SHA256 manifest). Run now, then weekly.
- [x] **C3** Site-build parity harness — **AUTO**:
      `scripts/sovereignty/build_site_parity.sh` reproduces the Pages
      artifact locally and seals a hash manifest — the new rails must
      match byte-for-byte before cutover.
- [x] **C4** Forgejo + Woodpecker + Caddy stack — **AUTO (templates)**:
      `scripts/sovereignty/forgejo-stack/` (compose + Caddyfile +
      `.env.example`). Fill `.env` from the vault, `docker compose up -d`.
- [ ] **C5** **PAIRED**: stand the stack up on the chosen box; run
      `build_site_parity.sh` against it; prove a full release + deploy.
- [ ] **C6** **PAIRED**: clean-history export
      (`scripts/sovereignty/fresh_history_export.sh`) — review the copy
      BEFORE any push; council decides fresh-history vs. preserved-history.
- [ ] **C7** **TYLER**: push the reviewed export to the Forgejo instance;
      GitHub flips to frozen read-only mirror at cutover.

## Phase W — The Approval Wall (by end of week, per council)

- [x] **W1** Wall scripts — **AUTO**:
      `scripts/sovereignty/arm_the_wall.sh` (branch protection: no force
      pushes, no deletions; `--enforce-reviews N` flips the review floor
      when steward handles exist; creates the `release` environment).
- [ ] **W2** **TYLER**: train Dustin + Anderson on desktop + CLI
      (contributor entrance exam, hands-on).
- [ ] **W3** **TYLER**: provision their steward accounts; add handles to
      `CODEOWNERS`; enroll their hardware keys.
- [ ] **W4** **TYLER**: Settings → Environments → `release` → Required
      reviewers = the three stewards (UI-only step; script prepares the
      environment and prints this reminder).
- [ ] **W5** **AUTO**: run `arm_the_wall.sh --enforce-reviews 2` after W3
      — the wall is live: no release climbs without the marks.

## Phase D — Dependency & tooling ownership

- [x] **D1** node/npm removed from CI (stdlib Python stats injection) —
      **done 2026-09-15**.
- [x] **D2** Supply-chain audit — **AUTO**: `pip-audit` against the
      runtime environment (run now, then quarterly in council).
- [ ] **D3** **AUTO**: wheel index on the steward rails
      (`releases.sprucegrove.io`, Caddyfile already routes it) + document
      the `--index` install flag beside the PyPI instructions.
- [ ] **D4** **COUNCIL**: quarterly audit + allowlist review in session.

## The long horizon (adopted, not scheduled)

- Grove-on-metal: stdlib-lean core → minimal runtime → bare hardware.
  Inherits every gate and test the seam lands. See `SOVEREIGNTY.md`
  Phase 5 and `docs/SELF-UPDATE.md`.

---

## What ran today (AUTO, evidence in `~/spruce-grove-sovereignty/`)

| Task | Result |
|---|---|
| B1 domain/DNS inventory | sprucegrove.io: Porkbun + privacy ON; NS on Porkbun |
| C2 weekly backup (2026-09-16) | bundle sealed: `~/spruce-grove-sovereignty/backups/20260915-235647.tar.gz` + sha256 |
| D2 quarterly audit (2026-09-16) | pip-audit: 53 known CVEs found &rarr; lock upgraded to fix versions &rarr; re-audit clean |
| C1 GitHub inventory | 28 repos; no collaborators beyond owner; no branch protection; OIDC publish (no secrets to rotate) |
| C2 backup bundle | run `scripts/sovereignty/backup_github.sh` (see output dir) |
| C3 parity build | `build_site_parity.sh` — artifact + `_site.sha256` |
| D2 dependency audit | `pip-audit` — see report |

The rule of the board: **if a task has a script, the script runs; if it
has a ceremony, the human performs it.** The council decides which is
which — and only the council can change that.
