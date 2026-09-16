# LIVING-UPDATES — the dictation ledger

Release notes record what landed. This ledger records what *happened* — the
decisions, pivots, and additions made organically in voice-dictation sessions
while Tyler works through the harness with Cedar. Everything here is real
conversation-turned-work; entries graduate into `CHANGELOG.md` when they ship.

## The protocol (how entries get added)

- **Who appends:** the agent (Cedar/Junto), live, during or right after a
  voice-dictation session. No ceremony — an entry per organic decision.
- **Where:** between the `LIVING:BEGIN` / `LIVING:END` HTML-comment
  markers below. Newest entry first.
- **Format:** `### YYYY-MM-DD — Title`, then bullets `Source:` / `Status:` /
  `Origin:`, then plain bullets for the story. Status is one of
  `idea` · `in-flight` · `shipped`. Origin is `grove-grown` or
  `upstream-synced`.
- **Promotion:** when an entry ships, its substance moves into
  `CHANGELOG.md` and the status flips to `shipped` — the ledger keeps the
  narrative, the changelog keeps the receipt.
- **No invented facts.** If a date or number isn't known, say so. The pages
  pipeline (`pages-hub/generate-updates.py`) renders this ledger into the
  Release Observatory on every regen — malformed entries will be visible to
  everyone, which is the point.

## The acceleration path (the working thesis)

The harness wins by running three moves in parallel, not sequentially:

1. **Keep the upstream connector honest.** Code Puppy is the steady feed of
   proven work; port what helps, log what differs, stay import-compatible
   until it no longer pays (see `PROVENANCE.md`). Free leverage is still
   leverage.
2. **Retire the transient, deliberately.** Every inherited piece carries a
   status. When vendoring beats syncing — the external plugin bundle, the
   compat shim — vendor it and flip the badge. Debt with a name and a date
   is a plan; debt without is drift.
3. **Deepen the voice-first wedge.** The fork exists because the voice loop
   is the moat: dictate while building, capture the organic stream in this
   ledger, and let the observatory render it. Every other agentic CLI takes
   typed tickets; this one takes dictation and keeps a public memory.

---

<!-- LIVING:BEGIN -->

### 2026-09-16 — The validation ladder: desktop onboarding, traceability, the living directory
- Source: dictation session (the "biggest validations" question)
- Status: in-flight
- Origin: grove-grown
- Three validations now name the next phase, captured in
  `docs/VALIDATION-LADDER.md`: (1) the desktop OS onboarding — persona-driven
  first runs that tune token economy and context utilization from minute one
  and make the synthetic-subscription path seamless; (2) the traceability
  program — generated matrices mapping every button, command, and feature to
  the test and the build-log receipt that proves it; (3) the living directory
  — opening a folder loads it as an organism with pulses, hooks, telemetry,
  and an audit trail, all voice-driven through mockingbird.
- The small-business portfolio wedge opened with two Benton-Drones-style
  studies (private lab, local-only): one business books jobs by `mailto:`
  with no online booking at all; the other runs a commercial gym portal with
  no public schedule — both are exactly the gap the grove's small-business
  kit exists to fill.
- The family-lab wedge (voice-first computing for the smallest builders) is
  captured privately and locally by design — the public repo never carries
  the people, only the product ideas.

### 2026-09-15 — The dashboard lands: release rail + dependency census go public
- Source: build session (the "level-set everything we borrow" question)
- Status: shipped
- Origin: grove-grown
- The rebrand finished its sweep: the last dog-era copy and paw prints left the
  CLI and all three locales. Compat aliases (`puppy_name`, `get_puppy_name`,
  the `agent_code_puppy` session bridge) stay by contract — the receipt is the
  contract, not the vibe.
- The stale solid-mark favicon pair left the repo root; the site serves the
  Disc, hash-verified against `logos/`.
- `docs/DEPENDENCY-EXIT.md`: the full census of everything borrowed — six
  tiers, verdicts computed by import scans of grove source and the plugin
  package. npm/axios: zero in-repo. `typer`: computed unused, removal queued.
  CI action pinning and site-font self-hosting queued. `httpx2` documented
  (codex/claude transports), `requests` dedupe queued, `pyfiglet` replacement
  queued.
- `/dashboard.html` live on the public site: every release on the rail with
  what landed in it, and the dependency-exit ladder rendered from the in-repo
  board. Wired into pages.yml + the parity harness.
- GitHub releases with real notes now exist for the rail (the tag was the only
  receipt since v1.0.1 — now the notes travel with it).
- AGENTS.md back under the 10k cap so the agent rules load whole.

### 2026-09-15 — The execution board: the sovereignty work becomes runnable
- Source: build session (the "what can be automated" question)
- Status: in-flight
- Origin: grove-grown
- The infrastructure runbook became a task board
  (`docs/SOVEREIGNTY-EXECUTION.md`) with one owner per task: the human
  for identity, payment, ceremony, and approval; scripts for everything
  that can be verified.
- Automation kit landed in `scripts/sovereignty/`: the wall
  (`arm_the_wall.sh`), the insurance snapshot (`backup_github.sh`), the
  site-parity harness (`build_site_parity.sh` — byte-identical artifact
  proof for the rails migration), the clean-history export
  (`fresh_history_export.sh`), and the Forgejo/Woodpecker/Caddy stack
  templates.
- Live inventories taken: domains (the project domain was already
  privacy-shielded at purchase — Porkbun, private registrant) and the
  full account surface (repos, collaborators, secrets, protection state).
- First supply-chain audit ran against the actual ship set: one finding
  (a file-upload parser with a known advisory), fixed and re-audited to
  zero. The audit command is now part of the board.

### 2026-09-15 — The Council & The Wall: governance made public
- Source: council session (governance design)
- Status: in-flight
- Origin: grove-grown
- The steering model is now public: three anonymous stewards, decisions
  starting as questions in Leather Apron sessions, the five-criteria Gate,
  and an Approval Wall no release climbs without the council's marks.
- Contributor path codified: learn the desktop and CLI, work in the open,
  earn into review rotation and steward seats.
- New public page: `sprucegrove.io/council/` — the story told in
  iconography only. No persons, no companies: seats, seals, and rules.
- Emergency lane defined: any steward may ship a security hotfix; the
  full council ratifies within 72 hours.

### 2026-09-15 — The harness seam lands: the grove starts owning its own engine
- Source: birthday dictation + build session (the sovereignty push)
- Status: in-flight
- Origin: grove-grown
- Decision taken on the birthday: the grove stops renting its core. The
  inherited agent framework is now behind a grove-owned seam
  (`spruce_grove/harness/`) — a protocol in grove vocabulary, an adapter
  that delegates verbatim, and a soft-failing selector
  (`SPRUCE_GROVE_HARNESS`).
- First two call sites migrated with behavior parity proven by tests
  (same raises, same fallbacks, same handle types). 56 remain; each lands
  one at a time, tests green, no big-bang rewrite — the Gate applies to
  our own work too.
- Roadmap adopted into SOVEREIGNTY.md: inventory (done) → seam (landed) →
  grove implementation behind the seam → flip per model → prune. The north
  star beyond: a core so lean and standard it could wake on real hardware,
  agnostic and self-owned — the destination, not the next step.
- Public phrasing rule adopted: the pages speak of "the inherited
  framework" and the ethos — never of companies or people. The work speaks
  for itself.

### 2026-09-15 — The logo pack: one geometry, four jobs
- Source: voice dictation session with Junto (this one)
- Status: shipped
- Origin: grove-grown
- The flat green trio read clip-art against the granlund look. Built the
  pack from the tylergranlund.com glyph DNA — stepped canopy, trunk notch,
  rounded joins, low-opacity fill wash: the **Core Disc** (statement
  roundel — stickers, laptops, app icons, favicons), the **Grove Mark**
  (app/nav logo, dark + light variants), the **Ghost** (watermark line
  art), and the **Lockups** (Fraunces wordmark). Wired across the board:
  shell chrome, every era-ghost, favicons, README badge, and the design
  system itself — BRAND.md now carries "The logo pack" and design.html a
  live Logo Pack section.

### 2026-09-15 — The Mechanics page: one page, ethos to evidence
- Source: voice dictation session with Junto (this one)
- Status: shipped
- Origin: grove-grown
- `pages-hub/mechanics.html` — the lifecycle core as a single-page explainer
  on the sprucegrove.io site: breathing core, four contracts, heartbeat,
  gates and judges, the nine-rounds war story, the human layer. Full GRAN
  design language (Fraunces/mono/EB Garamond, rune lines, one stamp, grain
  veil, era-ghost). Registered in the site sidebar and the hub, linked to
  the Release Observatory. The master class, made public.

### 2026-09-15 — The master class: teaching the lifecycle the way we teach people
- Source: voice dictation session with Junto (this one)
- Status: shipped
- Origin: grove-grown
- "The full enchilada": `MASTER-CLASS.md` now carries the training
  methodology — the 8am rule (zero context, zero shame, one concept per
  breath), the service-counter cadence, and troubleshooting theory run on
  the judge ABSTAIN war story as the lab. Seven modules: ethos-as-mechanism
  → breathing core → sovereignty heartbeat → gates & judges → the war
  story → empathetic service tactics → teach-backs. Graduation standard:
  the eighth-grader in the room could follow it.

### 2026-09-15 — The Living Log itself: release notes that breathe
- Source: voice dictation session with Junto (this one)
- Status: shipped
- Origin: grove-grown
- The release observatory covered the last two months of commits, but the
  *organic* work — decided out loud, mid-session — had no home. This ledger
  was born, the pipeline grew a `living-updates` region, and the observatory
  now renders the dictation stream on every regen. The page stopped being a
  snapshot and became a heartbeat.

### 2026-09-15 — The grove tends itself: self-healing auto-updates
- Source: voice dictation session (see `CHANGELOG.md`, Unreleased)
- Status: shipped
- Origin: grove-grown
- The version checker always *watched* PyPI and nagged; the decision to make
  it *act* came out of a spoken working session. It now upgrades the on-disk
  install via `uv tool upgrade` on the startup daemon thread — running
  sessions never break, failures degrade to the old nag, `NO_AUTO_UPDATE=1`
  opts out. Reference: `docs/SELF-UPDATE.md`.

### 2026-09-14 — The receipt travels: MIT → Apache-2.0
- Source: voice dictation session (see `CHANGELOG.md`, Unreleased)
- Status: shipped
- Origin: grove-grown
- Relicensing decision made out loud, reasons logged in
  `docs/LICENSE-ANALYSIS.md`: NOTICE carries the Code Puppy lineage verbatim,
  contributors grant a patent license with defensive termination, modified
  files must state what changed. Upstream stays MIT, untouched — the puppy
  came first.

### 2026-09 (undated draft) — TASK-001: Synthetic.new 90x plan re-pinning
- Source: drafted in a working session (`Sythentic-spruce-grove-updates.md`)
- Status: in-flight
- Origin: grove-grown
- Heavyweight model pins (Kimi-K3 at 3.0×) were exhausting the weekly quota
  in minutes under multi-agent execution. The plan: shift main-reasoning
  agents to `syn:large:text` (1.0×), fan-out agents to Flash-class (0.1×),
  embeddings to 0.0× — tracked through the Beads task DB, config changes
  staged in `grove.cfg` and agent JSON overrides.

### 2026-09-10 — The voice loop ships: "the grove speaks"
- Source: the founding dictation sessions (see `CHANGELOG.md`, 1.0.0)
- Status: shipped
- Origin: grove-grown
- The reason the fork exists, validated and released: `/rec` mic-to-whisper
  plugin, headless `--transcribe`, desktop dictation wired through the CLI.
  Zero cloud transcription. The TUI heard "Thank you.", sent it, and Cedar
  answered — dogfood evidence in build-log 29.

<!-- LIVING:END -->

---

Older organic decisions live in the build-log ladder: `BUILD-LOG.md`
(entries 1–29) and the release receipts: `CHANGELOG.md`.
