# Changelog — Spruce Grove OS

An agentic coding CLI grown from Code Puppy (MIT, Michael Pfaffenberger) into
the Granlund Grove. Together we are better. Always.

## How to read this page

Every component and entry carries its origin — no mistaking what we built for
what we inherited:

- **grove-grown** — designed and built in this grove, for this grove.
- **inherited** — arrived with the Code Puppy line; hardened and extended here.
- **transient** — inherited *and* scheduled for replacement; the exit plan
  lives in [PROVENANCE.md](PROVENANCE.md).
- **voice-led** — born in a dictation session with the agent and captured in
  [LIVING-UPDATES.md](LIVING-UPDATES.md), the living ledger this changelog
  promotes from.

## Core components atlas

| Component | Layer | Origin | Status |
|---|---|---|---|
| Voice loop (`/rec` plugin, `--transcribe`, desktop dictation) | voice-first | grove-grown | the reason the fork exists |
| Self-update daemon (`self_update.py`) | platform | grove-grown | shipped (Unreleased) |
| Cohort bricks + `user-plugins/` (Junto, barber, backoffice, creative scaffold) | plugins | grove-grown | versioned in-repo |
| Desktop shell ([spruce-grove-desktop](https://github.com/t-granlund/spruce-grove-desktop)) | surfaces | grove-grown | v0.1.0 |
| Release observatory + field-guide pipeline (`pages-hub/`) | surfaces | grove-grown | auto-regenerating |
| Cedar persona + agent configs (`agents/`) | agent layer | grove-grown persona, inherited engine | stable |
| TUI / CLI (`command_line/`, `cli_runner.py`) | interface | inherited | hardened here |
| Tool layer + `TOOL_REGISTRY` (`tools/`) | tools | inherited | extended here |
| Plugin architecture (3 tiers, SHA-256 trust gate, 30+ hooks) | plugins | inherited | extended here |
| Model layer, multi-provider (`model_factory.py`) | models | inherited | extended here |
| Session storage, migration, compaction | durability | inherited | extended here |
| i18n catalogs (`i18n/`) | platform | inherited | catalog regen cadence |
| pydantic-ai + MCP plumbing | foundation | external | pinned |
| Compat shim (`_code_puppy_compat.py`) + `code-puppy-core-plugins` bundle | compatibility | inherited | **transient** — vendoring planned |

Deep rename/contract map: [PROVENANCE.md](PROVENANCE.md). Organic
dictation-era decisions: [LIVING-UPDATES.md](LIVING-UPDATES.md).

## Unreleased — 2026-09-15 — "the receipt travels"

### License: MIT -> Apache-2.0

The Grove relicenses to Apache-2.0. What changes and why:

- **NOTICE file added** — carries the Grove attribution and preserves the
  Code Puppy lineage verbatim (Pfaffenberger's MIT notice). The receipt now
  travels with every copy, through every rebrand.
- **Patent grant** — contributors grant users an explicit patent license,
  with defensive termination. The builders of the grove are shielded.
- **Modified-file markers** — derivatives must state what they changed;
  stripping the names becomes evidence of the strip, not just a loss.
- **Trademarks withheld** — the names and marks ride outside the license
  (see TRADEMARKS.md).

Code Puppy remains MIT, upstream untouched — its notice lives in our NOTICE,
verbatim, because the puppy came first. Full reasoning:
[docs/LICENSE-ANALYSIS.md](docs/LICENSE-ANALYSIS.md).

### The grove tends itself — self-healing auto-updates

The version checker always *watched* PyPI and nagged; now it *acts*. When a
newer release is live, the on-disk install upgrades in place via
`uv tool upgrade` on the startup daemon thread:

- **Running sessions never break.** The active process keeps its warm,
  fully-loaded code; the next launch boots the new version. No restarts, no
  mid-session import swaps, startup never blocks.
- **A broken updater can never break a session.** Best-effort, never raises;
  any failure degrades to the old nag with the manual command attached.
- **Guards.** `NO_AUTO_UPDATE=1` opts out of actuation (`NO_VERSION_UPDATE=1`
  still silences the whole check). Source/editable checkouts are never
  upgraded. 180s subprocess timeout. Tests default to `NO_AUTO_UPDATE=1` so
  no test can ever mutate a real installation.
- **i18n.** Five new `version.self_update_*` keys across en-US, es, fr-CA.
- **Reference:** `docs/SELF-UPDATE.md`.

## 1.0.0 — 2026-09-10 — "the grove speaks"

First full release. The voice-first pillar — the reason the fork exists — is
live, validated, and shipped.

### The voice loop (the headline)

- **`/rec` Mockingbird plugin**: mic → local whisper (whisper-cli,
  large-v3-turbo q5_0, Metal) → review / edit in `$EDITOR` / re-record against
  your draft → send as the prompt. Zero cloud transcription.
- **`--transcribe <file>` headless verb**: the same rig as a CLI service for
  scripts and other surfaces — accepts any ffmpeg-readable container.
- **Desktop dictation** (spruce-grove-desktop v0.1.0): mic → MediaRecorder →
  the CLI's `--transcribe` → transcript lands in the editable prompt box.
  macOS mic permission declared in the bundle.
- **Live dogfood evidence**: the TUI heard "Thank you.", sent it, and Cedar
  answered on GLM-5.3-Flash (build-log 29).

### The platform

- Full namespace rebrand (`spruce_grove`, `spruce-grove`/`grove` CLI, Cedar,
  `~/.spruce_grove`) with a compatibility shim for upstream contracts.
- Three-tier plugin architecture (builtin / user / project) with SHA-256
  trust gate and 30+ hooks; the golden rule — plugins over core — held
  through every feature in this release.
- Cohort bricks: `/junto`, barber scaffold, `/backoffice`,
  `/creative-scaffold` + shared `grove_site_core`, all versioned in-repo
  (`user-plugins/` is the canonical copy; `scripts/install-user-plugins.sh`
  deploys).
- Zero-tolerance namespace ratchet (5al.8); judge ABSTAIN root cause fixed
  (5al.9); keyring-backed provider credentials.
- Standalone install: `uv tool install --from <repo> spruce-grove`;
  publish pipeline wired (`.github/workflows/publish.yml`).
- Desktop shell v0: spawns the CLI headless, streams output, `--quick-resume`
  continuity, cancel, single-active-run guard.
  https://github.com/t-granlund/spruce-grove-desktop

### Known gaps

- PyPI name unclaimed (owner errand: `docs/PYPI-CLAIM.md`).
- Desktop .app unsigned (first launch: right-click → Open).
- Packaged-app microphone prompt needs one human confirmation click.

---

Older history: the fork's build-log ladder lives in `BUILD-LOG.md` (entries
1–29 predate this file; the dashboard is `pages-hub/phases.html`).
