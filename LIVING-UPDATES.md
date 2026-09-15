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
