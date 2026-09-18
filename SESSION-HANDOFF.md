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

---

# ADDENDUM — 2026-09-16 midday (the branding + orbit close-out)

> Fresh OS session: read the original handoff above, then this. The board in
> `docs/SOVEREIGNTY-EXECUTION.md` still governs.

## What changed since the 9/15 handoff

| Thing | State |
|---|---|
| Repo | clean tree, synced with origin (only this addendum added) |
| **The Disc decision: MADE** | **"Sevardhet" is the Core Disc master** (`f8b8e3c`: Kungsleden + Birch variants, full propagation; plan logged `95a1523`) |
| Site surfaces | every sprucegrove.io page on the current logo kit (`a2bcc6a`), persona tiles + social preview (`6dd3815`) |
| LIVING-UPDATES | the dictation ledger renders into the Release Observatory (`pages-hub/generate-updates.py`) — entries graduate to CHANGELOG when they ship |
| Desktop sibling | inspector/settings/repo-access + Core Disc iconography landed; **`REVIEW.md` holds a 50-finding three-agent audit, top 20 ranked — the fresh desktop session starts there** |
| Stray log | moved out of repo root to `1.MASTER-ORCHESTRATION/LOGS/` |

## Fresh OS session — launch prompt

*"Read SESSION-HANDOFF.md top to bottom, then work the board in
docs/SOVEREIGNTY-EXECUTION.md — start with the post-reboot ritual, then the
highest-priority open item. The Disc is decided (Sevardhet); branding is
propagated everywhere; don't redo it."*

## Still open (unchanged priority order)

1. Post-reboot ritual (~2 min): `colima start`, confirm self-heal, skim the board
2. Council onboarding — Dustin + Anderson (Tyler, this week)
3. Tyler counsel items: COMPAT-EXIT, sovereignty-infra, manifesto naming
4. Harness exit: `load_config` / `make_model_settings` through the seam next
5. Wall-arming after stewards exist

*The orbit/business track lives in `~/dev/SPRUCE-GROVE-OUTREACH` (local-only,
never committed) and `~/dev/1.MASTER-ORCHESTRATION` (its LEVEL-SET.md is the
cross-workstream source of truth). Family-lab stays private by design.*

---

# ADDENDUM — 2026-09-18 morning (manifesto live + barbershop handoff verified)

- **Manifesto rendered for the web — landed** (`b6b53ce`): `pages-hub/manifesto.html`
  ("Believe" hub card, scroll-icon nav entry), published to `_site/manifesto/` by both
  the parity script and the pages workflow; mechanics/updates font-path fix included.
  Parity build verified clean (63 files) before commit.
- **Barbershop P1 (`bmy`) closed.** REVIEW-GUIDE.html + TEXTS-TO-SEND.md verified
  end-to-end: all 10 services match `services.html` line-by-line (name/duration/price),
  hours/address match `location.html`, 6-barber team count confirmed, guide covers every
  memo-1 ask (Square stays, cost comparison, local/secure, monitoring, chairside).
  Remaining Tyler-only: pick delivery method, personalize the two texts, send.
- **Security finding filed as `8l7`:** `t-granlund/bentonville-barber` is PUBLIC and its
  mock-site code already contains real barber names. Handoff deliverables are now
  gitignored local-only in that repo (guard commit `4e0d956`) — deliver by AirDrop/email,
  never push. Decide: make the repo private or scrub.
- Voice memos remain untracked local-only by design (`docs/OFFSITE-*`).

## Addendum 2 — 2026-09-18, the anonymity pivot (policy decided by Tyler)

> **Policy, inherited by every future session:** businesses and their staff
> may be named and detailed publicly. **Nothing about the grove's own people
> (Tyler + family) goes on any public surface** — generalize to the ethos,
> keep the real stories, drop every name/age/relationship.

- **Landed in `bcc846c`:** MANIFESTO.md + manifesto page fully authorless
  (dateline, kids, the inside-the-walls story, the dojo — all generalized;
  Fleckenstein business reference kept); "Tyler's Mac" → "the keeper's Mac",
  TYLER → KEEPER on the dashboard board, granlund spruce → grove spruce
  (copy + asset comments), product footer generalized.
- **Field guide changelog feed now anonymizes at generation time** —
  `_display_author()` in `docs/field_guide_changelog.py` renders the grove's
  own commits as "the grove" (matches observatory provenance chips). Upstream
  contributors keep their names: credit, not exposure.
- Full leak sweep of `_site/` + `pages-hub/` + manifesto + data.js: **clean**.
- Residue filed as `SPRUCE-GROVE-OS-r8c` (Tyler decisions): pyproject author/
  email/homepage on public PyPI, SESSION-HANDOFF.md living in the public
  repo, and the history-rewrite question (one old commit subject says
  "granlund-grove"). Git history itself was NOT rewritten.
- `8l7` closed by policy: barber names on the public mock repo are fine;
  the handoff-deliverable local-only guard stays (they carry Tyler's phone).
