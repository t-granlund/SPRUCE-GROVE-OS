# Multi-Agent-Orch-CLI — Sovereignty Playbook

A living brief on what this is, what's backed up where, and how to stay self-sufficient if the upstream public repo ever disappears.

## What You Actually Own

| Layer | Location | Purpose | Status |
|---|---|---|---|
| **Working source clone** | `~/code_puppy/` | Live development + install source |  main @ v0.0.768 |
| **Public fork** | `github.com/t-granlund/code_puppy` | Backup; mirrors upstream + Tyler's work |  auto-synced by updater; **GitHub Pages site** at t-granlund.github.io/code_puppy/ (hub / field-guide / releases / flat) |
| **Private mirror (insurance)** | `github.com/t-granlund/Multi-Agent-Orch-CLI` | Untouchable fallback if public repo dies |  auto-synced by updater |
| **Installed tool** | `~/.local/share/uv/tools/code-puppy/` | Currently-running CLI (uv tool install) |  v0.0.768 |
| **Offline wheel** | `~/code_puppy/dist/code_puppy-0.0.768-py3-none-any.whl` | Zero-network reinstall artifact |  built Aug 22 (current; rebuild with `uv build` if needed) |
| **User profile** | `~/.code_puppy/` | plugins/, agents/, config, kennel (memory), logs |  not in any repo |
| **Apr-2026 OAuth fix (history)** | tag `snapshot-old-myfork-main` | Tyler's callback/Claude-OAuth sync; since superseded by upstream | archived as tag |

## Remotes on `~/code_puppy`

```
origin   = github.com/mpfaffenberger/code_puppy.git   (PUBLIC upstream, Michael Pfaffenberger)
myfork   = github.com/t-granlund/code_puppy.git       (public fork — backup)
private  = github.com/t-granlund/Multi-Agent-Orch-CLI (private insurance repo)
```

Daily update script (`~/.code_puppy/scripts/update-code-puppy.sh`) is a **full self-healing pipeline**: snapshot → rebase on upstream → run tests (cross-check) → reinstall → regen field guide → push `myfork` + `private` via `gh`. Runs **ad-hoc** via `/update now` (launchd plist is paused; no auto-schedule).

## Running cadence

```bash
cd ~/code_puppy

# 1. Ad-hoc: run `/update now` in any code-puppy session to trigger the
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
git clone git@github.com:t-granlund/code-puppy-profile-backup.git ~/.code_puppy
```

## If the Public Repo Goes Away

**Nothing breaks immediately.** Your installed binary keeps running. Your local clone has the full history. Your two GitHub repos have the full history.

**When you want to update/reinstall:**
```bash
# Fresh machine? Clone your private mirror
git clone https://github.com/t-granlund/Multi-Agent-Orch-CLI.git ~/code_puppy

# Or just use local source
cd ~/code_puppy && /opt/homebrew/bin/uv tool install --reinstall .

# Nuclear offline fallback (no network at all)
/opt/homebrew/bin/uv tool install ~/code_puppy/dist/code_puppy-0.0.768-py3-none-any.whl
```

**Cut the upstream link** (cleanliness):
```bash
cd ~/code_puppy && git remote remove origin
# update_schedule script will error on fetch but won't hurt anything;
# consider editing it to skip the git pull if origin is gone
```

## What's NOT Yet Backed Up

- ~~`~/.code_puppy/`~~ — **Now backed up** to private repo `t-granlund/code-puppy-profile-backup` on every update run (whitelist: agents, plugins, kennel memory, skills, commands, scripts, config + credentials). Note the repo contains API keys — keep it private, restrict collaborators.
- `dist/` wheels older than today's rebuild. Rotate them or keep only the latest.

## Residual Risk

- **Generated field-guide artifacts** (`docs/field-guide/data.js`, `docs/field-guide-flat.html`) are gitignored locally but referenced by upstream code. If upstream ever tracks them, your local untracking will fight on every rebase. Decide once: either commit them somewhere owned by you, or accept the rebase dance.
- **Updates run ad-hoc** (launchd paused). You only ingest upstream changes when you explicitly run `/update now`, so regressions can't sneak in unattended.
