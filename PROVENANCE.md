# PROVENANCE — Where every trail in this grove came from

SPRUCE GROVE OS is built from **Code Puppy**, MIT licensed, originally
authored by **Michael Pfaffenberger** and contributors:

- Upstream: https://github.com/mpfaffenberger/code_puppy
- Working fork: https://github.com/t-granlund/code_puppy

Lineage of this repository:

1. Fork `t-granlund/code_puppy` synced with upstream `main` (merge commit
   `d819ae4e`, 0 upstream commits behind at sync time).
2. Working tree imported here as commit #1 (pristine copy).
3. Rebrand applied methodically in audited passes (commits #2+).

## The rename map

| Code Puppy | Spruce Grove OS | Notes |
|---|---|---|
| `code_puppy` (python package) | `spruce_grove` | full module rename |
| `code-puppy` (dist/script) | `spruce-grove` | plus `grove` CLI alias |
| `Code Puppy` (display) | `Spruce Grove` | prose/docs |
| `CODE_PUPPY_*` env vars | `SPRUCE_GROVE_*` | NOT auto-aliased; rename on migration |
| `Puppy` (persona, default name) | `Cedar` | the grove guide |
| `puppy` (identifiers) | `grove` | e.g. `puppy_name` -> `grove_name` |
| `puppy.cfg` | `grove.cfg` | config file |
| `~/.code_puppy/` | `~/.spruce_grove/` | config/data dir |
| `agent_code_puppy.py` | `agent_spruce_grove.py` | default agent |
| `CodePuppyAgent` | `SpruceGroveAgent` | class |
| logo assets `code_puppy_logo*` | `spruce_grove_logo*` | imagery refresh pending |

## Contracts intentionally KEPT for compatibility

| Contract | Why |
|---|---|
| `code-puppy-core-plugins` dependency | official external plugin bundle, pinned in pyproject |
| entry-point group `code_puppy.plugins` | the external bundle registers plugins under this group |
| `code_puppy.*` imports | resolved to `spruce_grove.*` by `spruce_grove/_code_puppy_compat.py` (meta-path shim, appended so a real code_puppy install would win) |
| `agent_code_puppy` module | re-exports `SpruceGroveAgent` |
| `CodePuppyAgent` class alias | third-party imports keep working |
| `get_puppy_name()` alias | wraps `get_grove_name()` |
| persisted `puppy_name` config key | `get_grove_name()` falls back to it so upgraded configs keep their pet name |
| `PUPPY_KENNEL_ROOT` env var | consumed by external kennel plugin |
| `PURPLE_PUPPY` / `_PUPPY` in theme/spinner tests | names defined inside the external plugin bundle |

## Known follow-ups (honest ledger)

- Logo/brand imagery still shows the puppy — design refresh pending
  (brand tokens: see BRAND.md).
- Upstream docs under `docs/`, `pages-hub/`, `changelog/` were renamed
  mechanically; prose is ~95% correct but pass-by-pass cleanup is welcome.
- `version_checker` queries PyPI for `spruce-grove` (not yet published);
  it fails soft after a 5s timeout.
- Some user-facing emoji from upstream remain; persona emoji refresh
  planned per project formatting policy (none allowed in source for now).
- i18n non-English catalogs lag the English msgid changes until the next
  catalog regen (`docs/I18N.md` workflow).
