# Multi-Agent-Orch-CLI — Sovereignty Playbook

> **REALITY UPDATE — 2026-09-15.** The brief below was written in the
> `~/spruce_grove` fork era (v0.0.768). The grove has since moved into
> `SPRUCE-GROVE-OS` (this repo, origin), self-healing releases train
> directly from PyPI, the site lives at https://sprucegrove.io/, and the
> upstream relationship is now a managed connector (see
> `docs/SELF-UPDATE.md` + the observatory's Upstream Connector). The
> historical tables below are kept for the insurance lineage they document.

## The harness exit — pydantic-ai, honestly

**Where we stand:** 61 files under `spruce_grove/` import pydantic-ai
(114 import statements; recomputed 2026-09-22). It owns the agent loop,
streaming, tool calling, model resolution, and the retry/refresh seams.
The boot banner no longer advertises it (this was branding; the dependency
is still real).

**The honest assessment:** a big-bang removal is a rewrite masquerading as
a cleanup, and the Leather Apron Gate exists precisely to stop manic,
insecure moves like that. The exit is a staged seam, judged by the same
five criteria as any upstream signal:

1. **Inventory & freeze (done).** Touchpoints mapped: `pydantic_patches`,
   `model_factory`, `agents/base_agent`, `event_stream_handler`,
   `round_robin_model`, `cli_runner` bootstrap, MCP toolset bridges.
2. **The seam — LANDED 2026-09-15.** `spruce_grove/harness/` is live:
   grove-owned `Harness` protocol (`protocol.py`, zero external imports —
   structurally tested), the delegating adapter (`pydantic_harness.py`,
   pass-through to `ModelFactory` — parity proven by tests), and the
   soft-failing selector (`selector.py`, `SPRUCE_GROVE_HARNESS` env,
   unknown names fall back loudly and safely). First two call sites
   migrated: `tools/subagent_invocation.py` and `private_inference.py`.
   **Settings surface — LANDED 2026-09-22:** the protocol grew
   `load_models_config` / `make_model_settings` (parity-tested against the
   inherited functions), and three call-site files now route model
   resolution plus settings through the seam — `agents/_builder.py` (the
   agent construction path, which no longer imports `model_factory` at
   all), `tools/subagent_invocation.py`, and `private_inference.py`.
   Remaining: 58 of 61 files (computed 2026-09-22) — each migrates one
   landing at a time, tests green, next the `RunContext` tool vocabulary
   (the long tail), then the agent loop and streaming.
3. **The replacement.** Behind the protocol, grow (or vendor) the grove's
   own loop: stdlib + httpx streaming, the tolerant OpenAI client we
   already carry, our own retry/token logic (much of it already exists —
   `http_retry.py`, `claude_oauth_transport.py`, `tolerant_openai.py`).
   Gate criterion: it must be *tried & true* in production before the
   flag flips — the seam lets both implementations run side by side.
4. **The flip & the prune.** Flip per-model/per-agent behind config,
   then delete. The exit ends with `pydantic-ai` gone from pyproject and
   the compat story updated in `PROVENANCE.md`.
5. **The north star — grove on metal.** When the core is grove-owned end
   to end and stdlib-lean, the long-horizon track opens: a runtime small
   enough to wake on real hardware, agnostic across Linux/macOS/Windows
   first, bare-metal eventually. That is the destination, not the next
   step — it inherits every gate and every test the seam lands along the
   way.

**Estimate:** multiple focused sprints, not a session. The seam work can
start any session and pays off immediately (one vocabulary instead of 58
import sites), which is exactly why it is the sovereignty play.

---

# Multi-Agent-Orch-CLI — Sovereignty Playbook

A living brief on what this is, what's backed up where, and how to stay self-sufficient if the upstream public repo ever disappears.

## What You Actually Own

| Layer | Location | Purpose | Status |
|---|---|---|---|
| **Working source clone** | `~/spruce_grove/` | Live development + install source |  main @ v0.0.768 |
| **Public fork** | `github.com/t-granlund/code_puppy` | Backup; mirrors upstream + Tyler's work |  auto-synced by updater; **GitHub Pages site** at t-granlund.github.io/spruce_grove/ (hub / field-guide / releases / flat) |
| **Private mirror (insurance)** | `github.com/t-granlund/Multi-Agent-Orch-CLI` | Untouchable fallback if public repo dies |  auto-synced by updater |
| **Installed tool** | `~/.local/share/uv/tools/spruce-grove/` | Currently-running CLI (uv tool install) |  v0.0.768 |
| **Offline wheel** | `~/spruce_grove/dist/spruce_grove-0.0.768-py3-none-any.whl` | Zero-network reinstall artifact |  built Aug 22 (current; rebuild with `uv build` if needed) |
| **User profile** | `~/.spruce_grove/` | plugins/, agents/, config, kennel (memory), logs |  not in any repo |
| **Apr-2026 OAuth fix (history)** | tag `snapshot-old-myfork-main` | Tyler's callback/Claude-OAuth sync; since superseded by upstream | archived as tag |

## Remotes on `~/spruce_grove`

```
origin   = github.com/mpfaffenberger/code_puppy.git   (PUBLIC upstream, Michael Pfaffenberger)
myfork   = github.com/t-granlund/code_puppy.git       (public fork — backup)
private  = github.com/t-granlund/Multi-Agent-Orch-CLI (private insurance repo)
```

Daily update script (`~/.spruce_grove/scripts/update-code-grove.sh`) is a **full self-healing pipeline**: snapshot → rebase on upstream → run tests (cross-check) → reinstall → regen field guide → push `myfork` + `private` via `gh`. Runs **ad-hoc** via `/update now` (launchd plist is paused; no auto-schedule).

## Running cadence

```bash
cd ~/spruce_grove

# 1. Ad-hoc: run `/update now` in any spruce-grove session to trigger the
#    full pipeline (rebase -> tests -> reinstall -> regen field guide ->
#    push myfork + private). No auto-schedule; launchd plist is paused.

# 2. Each push to main rebuilds the field guide on GitHub Pages via
#    .github/workflows/pages.yml

# 3. Quarterly (or when version bumps): rebuild offline insurance
/opt/homebrew/bin/uv build --out-dir dist/

# 4. Every few weeks: Release Observatory curation pass.
#    Auto-detected 'narrative pending' cards accumulate on the Pages site;
#    promote the good ones into curated deep-dives in pages-hub/updates.html.
    
# 5. On machine replacement: restore profile from
git clone git@github.com:t-granlund/spruce-grove-profile-backup.git ~/.spruce_grove
```

## If the Public Repo Goes Away

**Nothing breaks immediately.** Your installed binary keeps running. Your local clone has the full history. Your two GitHub repos have the full history.

**When you want to update/reinstall:**
```bash
# Fresh machine? Clone your private mirror
git clone https://github.com/t-granlund/Multi-Agent-Orch-CLI.git ~/spruce_grove

# Or just use local source
cd ~/spruce_grove && /opt/homebrew/bin/uv tool install --reinstall .

# Nuclear offline fallback (no network at all)
/opt/homebrew/bin/uv tool install ~/spruce_grove/dist/spruce_grove-0.0.768-py3-none-any.whl
```

**Cut the upstream link** (cleanliness):
```bash
cd ~/spruce_grove && git remote remove origin
# update_schedule script will error on fetch but won't hurt anything;
# consider editing it to skip the git pull if origin is gone
```

## What's NOT Yet Backed Up

- ~~`~/.spruce_grove/`~~ — **Now backed up** to private repo `t-granlund/spruce-grove-profile-backup` on every update run (whitelist: agents, plugins, kennel memory, skills, commands, scripts, config + credentials). Note the repo contains API keys — keep it private, restrict collaborators.
- `dist/` wheels older than today's rebuild. Rotate them or keep only the latest.

## Residual Risk

- **Generated field-guide artifacts** (`docs/field-guide/data.js`, `docs/field-guide-flat.html`) are gitignored locally but referenced by upstream code. If upstream ever tracks them, your local untracking will fight on every rebase. Decide once: either commit them somewhere owned by you, or accept the rebase dance.
- **Updates run ad-hoc** (launchd paused). You only ingest upstream changes when you explicitly run `/update now`, so regressions can't sneak in unattended.
