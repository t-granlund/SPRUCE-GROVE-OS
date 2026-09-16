# SESSION HANDOFF — 2026-09-15 (the sovereignty birthday session)

> **NEXT SESSION: read this file first, then work the board in
> `docs/SOVEREIGNTY-EXECUTION.md`.** Suggested launch prompt:
> *"Read SESSION-HANDOFF.md and pick up the sovereignty board where it
> stands — start with the post-reboot ritual and the highest-priority
> open item."*

---

## State of the world at handoff

| Thing | State |
|---|---|
| Repo | `t-granlund/SPRUCE-GROVE-OS` @ `6229060`, tree clean, pushed |
| CLI on PyPI | **1.0.49** (self-heal target — first launch after reboot upgrades in-place) |
| CLI installed locally | 1.0.40 → self-heals to 1.0.49 on next launch (expected) |
| Site | https://sprucegrove.io — releases/, council/, mechanics/, hub, observatory all live |
| Colima | **stopped cleanly** for the macOS golden-master restart; `colima start` resumes `tenantfleet-postgres-1` with data intact |
| Workflows | publish + pages: completed/success; Wall of approval NOT yet armed (see W-phase) |
| Beads | epic `SPRUCE-GROVE-OS-5al` "Grove execution ladder" tracks the ladder incl. `5al.7` bootable-OS north star |

## What shipped today (eight+ landings, all pushed)

1. **Self-healing auto-updates** — detect → upgrade on disk → next chat
   runs new version; running sessions never break. Guarded
   (`NO_AUTO_UPDATE`, source-checkout immunity), i18n ×3, tested.
2. **The observatory (sprucegrove.io/releases)** — provenance chips on
   every entry (grove-grown vs upstream-synced, computed from commit
   authorship at generation time), hero ledger, sticky nav bar with
   working Grove/Upstream filter, Upstream Connector with a LIVE feed of
   upstream commits, scroll-spy sidebar TOC on all viewports.
3. **The Leather Apron Gate** — five criteria (tried & true · secure ·
   honest · grove-fit · counsel sign-off); every upstream row arrives
   "awaiting counsel"; connector is read-only metadata, the gate is the
   only door.
4. **MANIFESTO.md** — the birthday dictation as founding document.
5. **Bootloader de-Pydantic'd** — splash docstring + banner tagline +
   boot link now grove-owned; es/fr keys added.
6. **Harness seam (Phase 2 LANDED)** — `spruce_grove/harness/`:
   grove-owned protocol (structurally pure), delegating adapter (parity
   proven), soft-failing selector. Two call sites migrated; 56 remain.
7. **Governance** — `GOVERNANCE.md` (3 stewards, 2/3 + 3/3 thresholds,
   emergency lane), `CODEOWNERS` (the wall in repo form),
   `docs/COMPAT-EXIT.md` (all eight compat contracts get proper
   recreation plans — DRAFT awaiting approval), council page live at
   `/council/`.
8. **Sovereignty execution** — `docs/SOVEREIGNTY-EXECUTION.md` board +
   `scripts/sovereignty/` kit (arm_the_wall, backup_github,
   build_site_parity, fresh_history_export, forgejo-stack) + live
   inventories (domains already privacy-shielded; account surface mapped)
   + first supply-chain audit (python-multipart fixed, ship set clean).

## NEXT STEPS — in priority order

### 0. Post-reboot ritual (next session, ~2 min)
- [ ] `colima start` (postgres container resumes with data)
- [ ] `grove` → confirm self-heal to 1.0.49 (the loop across a reboot)
- [ ] Skim this file + `docs/SOVEREIGNTY-EXECUTION.md`

### 1. Council onboarding — Dustin + Anderson (TYLER, by end of week)
- [ ] Train them on the desktop + CLI (the entrance exam is hands-on)
- [ ] Provision pseudonymous steward accounts (see Phase A of
      `docs/SOVEREIGNTY-INFRASTRUCTURE.md`: steward email, vault,
      hardware keys ×2 each)
- [ ] Add their handles to `.github/CODEOWNERS` (gate paths = 3/3)
- [ ] Settings → Environments → `release` → Required reviewers = three
      stewards
- [ ] `scripts/sovereignty/arm_the_wall.sh --enforce-reviews 2` → the
      wall is fully armed

### 2. Decisions waiting on Tyler (counsel items)
- [ ] Approve/reject `docs/COMPAT-EXIT.md` (all eight compat contracts
      have proper recreation plans; nothing executes without sign-off)
- [ ] Approve/reject `docs/SOVEREIGNTY-INFRASTRUCTURE.md` (the off-GitHub
      migration runbook)
- [ ] **Manifesto naming**: public MANIFESTO.md currently carries
      Tyler's name (written before the anonymity pivot). Council decision:
      keep the named original, or publish the authorless variant.
- [ ] `tylergranlund.com`: keep personal (never project infra) or drop —
      it cannot be made anonymous.

### 3. Harness exit — next landings (AUTO, any session)
- [ ] Migrate `load_config` / `make_model_settings` through the seam
      (settings surface)
- [ ] Then the `RunContext` tool vocabulary (the long tail, ~40 modules)
- [ ] Then the agent loop + streaming events
- [ ] Then Phase 3: the grove implementation behind the protocol
      (see `SOVEREIGNTY.md` — the plan and the honesty are already there)

### 4. Infrastructure execution (per the runbook + board)
- [ ] Phase A steward identity → Phase B sprucegrove.io transfer →
      Phase C dual-home proof → Phase D tooling policy (W-phase interleaves
      with council onboarding)

### 5. Long horizon (adopted, parked)
- Grove-on-metal (bead `5al.7`), privacy-first telemetry (`r2j`), and the
  rest of the ladder epic.

## Rules the next session inherits

- Public pages: **never persons, never companies — only the ethos.**
- The Gate applies to everything, including our own refactors and the
  infrastructure.
- Compatibility contracts: recreate properly, dual-load, exit on
  evidence (`docs/COMPAT-EXIT.md`).
- Counts are computed, never claimed. If it can drift, make it live.
- Together we are better. Always.

---

*Handoff written 2026-09-15 evening, after the macOS golden-master restart
prep. All work pushed. Nothing left dangling.*
