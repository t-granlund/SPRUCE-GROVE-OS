# Contributing to Spruce Grove

> **Golden rule:** nearly all new functionality should be a **plugin** in the
> `code_puppy_core_plugins` repository that hooks into core via
> `spruce_grove/callbacks.py`. Don't edit `spruce_grove/command_line/`.

## How Plugins Work

Plugins are discovered from three tiers, loaded in order:

| Tier | Location | When to use |
|------|----------|-------------|
| **Builtin** | `code_puppy_core_plugins/<name>/register_callbacks.py` | Official, discovered via entry points |
| **User** | `~/.spruce_grove/plugins/<name>/register_callbacks.py` | Personal; every project |
| **Project** | `<CWD>/.spruce_grove/plugins/<name>/register_callbacks.py` | Repo-specific, shared via git |

All tiers use the same pattern — a `register_callbacks.py` in a named subdir (auto-discovered):

```python
from spruce_grove.callbacks import register_callback
register_callback("startup", lambda: print("my_feature loaded!"))
```

### Project Plugins

Mirrors agent/skill discovery (`.spruce_grove/agents|skills/`). Key details:

- **Created intentionally** — the grove never auto-creates `.spruce_grove/plugins/`.
- **Trust-gated.** None load until the user accepts in the `/plugins` TUI
  (select → Enter → type `trust`); accepted plugins hot-load with no restart.
  Trust is a SHA-256 of the plugin dir, stored in `~/.spruce_grove/trusted_plugins.json`
  scoped to the project path; any file change reverts to untrusted, everything
  else fails closed. `/plugins revoke <name>` removes trust. Model: `spruce_grove/plugins/trust.py`.
- **No runtime state in the plugin dir** — state (SQLite, caches, logs) next to
  the code self-tampers the hash. Use `~/.spruce_grove/` or a dot-path
  (e.g. `.state/`), which is excluded from hashing.
- **Load order builtin → user → project** (project last, highest precedence).
- **Project wins name collisions** with user plugins (user copy skipped), matching
  agent dedup; shadowing a builtin logs a warning.
- **Namespace isolation:** project plugins import as `project_plugins.<name>.register_callbacks`.

## Available Hooks

`register_callback("<hook>", func)` — deduplicated; sync or async functions accepted.

`register_callback("<hook>", func, fail_closed=True)` — for `pre_tool_call` /
`run_shell_command` only: a crashed guard normally reports `None` (read as
approval); `fail_closed=True` reports the exception as a block. Rejected elsewhere.

| Hook | When | Signature |
|------|------|-----------|
| `startup` | App boot | `() -> None` |
| `shutdown` | Graceful exit | `() -> None` |
| `invoke_agent` | Sub-agent invoked | `(*args, **kwargs) -> None` |
| `agent_exception` | Unhandled agent error | `(exception, *args, **kwargs) -> None` |
| `agent_run_start` | Before agent task | `(agent_name, model_name, session_id=None) -> None` |
| `model_select` | Select a model for one run | `(*, agent_name, current_model, prompt, messages, session_id=None) -> str \| None` (first non-empty wins) |
| `agent_run_end` | After agent run | `(agent_name, model_name, session_id=None, success=True, error=None, response_text=None, metadata=None) -> None` |
| `load_prompt` | System prompt assembly | `() -> str \| None` |
| `run_shell_command` | Before shell exec | `(context, command, cwd=None, timeout=60) -> dict \| None` (`{"blocked": True}` / `{"rewrite": cmd}`) |
| `file_permission` | Before file op | `(context, file_path, operation, ...) -> bool` |
| `pre_tool_call` | Before tool executes | `(tool_name, tool_args, context=None) -> Any` |
| `post_tool_call` | After tool finishes | `(tool_name, tool_args, result, duration_ms, context=None) -> Any` |
| `custom_command` | Unknown `/slash` cmd | `(command, name) -> True \| str \| None` |
| `custom_command_help` | `/help` menu | `() -> list[tuple[str, str]]` |
| `register_tools` | Tool registration | `() -> list[{"name", "register_func"}]` |
| `register_agent_tools` | Advertise tools to an agent | `(agent_name: str \| None) -> list[str]` (TOOL_REGISTRY names) |
| `register_agents` | Agent catalogue | `() -> list[{"name", "class"}]` |
| `register_model_type` | Custom model type | `() -> list[{"type", "handler"}]` |
| `register_skills` | Skill catalogue | `() -> list[{"name", "skill_md" \| "skill_md_path" \| "frontmatter"+"body"}]` |
| `register_cli_args` | Before CLI `parse_args()` | `(parser) -> list` (call `parser.add_argument`; namespace flags) |
| `handle_cli_args` | After CLI `parse_args()` | `(args) -> dict \| None` (`{"handled": True, "exit_code": int}` to exit; `None` proceeds) |
| `load_model_config` | Patch model config | `(*args, **kwargs) -> Any` |
| `load_models_config` | Inject models | `() -> dict` |
| `load_model_descriptions` | Inject description overlays | `() -> dict[str, str]` |
| `get_model_system_prompt` | Per-model prompt | `(model_name, default_prompt, user_prompt) -> dict \| None` |
| `provider_credential_flow` | `/add_model` missing credential | `(*, provider_id, env_var) -> bool \| None` (first `True` wins) |
| `stream_event` | Response streaming | `(event_type, event_data, agent_session_id=None) -> None` |
| `transform_model_messages` | Before each model request | `(agent_name, messages) -> None` (mutate `list[ModelMessage]` in place) |
| `pre_mcp_autostart` | Before bound MCP servers auto-start | `(agent_name, server_names) -> None` (refresh tokens here) |

Rare hooks: see `spruce_grove/callbacks.py` source.

## Ctrl+X Chords

`Ctrl+X` is a **chord prefix** (readline-style), never a standalone hotkey. The
line editor arms on `Ctrl+X`, hints registered bindings on the bottom bar, and
resolves the NEXT key against the registry in `spruce_grove/messaging/chords.py`.
`Esc` (or any unbound key) cancels.

| Chord | Action | Registered by | Active when |
|-------|--------|---------------|-------------|
| `Ctrl+X Ctrl+E` | Edit the prompt buffer in `$VISUAL`/`$EDITOR` | `run_ui` | Always (UI lifetime) |
| `Ctrl+X Ctrl+X` | Kill all running shell commands | `command_runner` | While shell commands run |
| `Ctrl+X Ctrl+B` | Background all running shell commands | `command_runner` | While shell commands run |

**Design notes:**

- **No modes** — `Ctrl+X` always flows into the editor; the registry decides the
  follow-up key (the old modal arm/disarm raced keystrokes).
- **Backgrounding is mid-flight detach** — streaming shell calls return
  immediately with `background=True`, `log_file`, `pid`; processes keep running.
- **Headless fallback** — without a line editor, bare `Ctrl+X` keeps its
  historical kill-all-shells meaning.

**Plugins can register chords:**

```python
from spruce_grove.messaging.chords import register_chord, unregister_chord

register_chord("\x14", my_callback, "Ctrl+T do the thing")  # Ctrl+X Ctrl+T
```

Chord callbacks run on the key-listener thread: **never block** (hop to the
asyncio executor like `messaging/external_editor.py`), never raise, register
only while meaningful. Keys are single raw control characters — prefer
`Ctrl+<letter>`; digits/F-keys unsupported.

## Internationalization (i18n)

Localize user-facing strings via `spruce_grove/i18n/` (guide: **`docs/I18N.md`**). Rules (PUP-473):

- **Wrap display strings** in `t("key", **params)` / `ngettext("key", n)`; catalogs in
  `spruce_grove/i18n/locales/<locale>.json`; missing keys echo (never crash).
- **Interpolate with `{name}`** placeholders only — no f-strings, no `str.format`
  on catalog text (untrusted input).
- Single emit point (`messaging/message_queue.py::emit_message`) resolves `i18n.lazy(...)`.
- **Model-facing system prompts are OUT of scope** — translation changes LLM behavior.
- CI gate: `tests/i18n/test_i18n_audit.py` (every key in `en-US`, pseudolocale clean).

## Rules

1. **Plugins over core** — if a hook exists for it, use it
2. **One `register_callbacks.py` per plugin** — register at module scope
3. **600-line hard cap** — split into submodules
4. **Fail gracefully** — never crash the app
5. **Return `None` from commands you don't own**
6. **Always run linters** — `ruff check --fix`, `ruff format .`
7. **NEVER ALLOW A CLAUDE CO-AUTHOR COMMIT**

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
