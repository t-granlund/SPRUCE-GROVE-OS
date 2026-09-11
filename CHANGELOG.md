# Changelog — Spruce Grove OS

An agentic coding CLI grown from Code Puppy (MIT, Michael Pfaffenberger) into
the Granlund Grove. Together we are better. Always.

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
