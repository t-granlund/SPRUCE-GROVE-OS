# user-plugins — the grove's personal-tier plugins, versioned

The CLI discovers user-tier plugins from `~/.spruce_grove/plugins/` (loads for
every project, no trust ceremony — this tier is "the person's plugins", vs.
builtin tier in `code_puppy_core_plugins` and project tier in
`<repo>/.spruce_grove/plugins/`).

Until Sept 10 that directory was the only copy of these plugins — one dead
disk from gone. This tree is now the **canonical copy**; `~/.spruce_grove/`
is a deploy target.

## The ritual

Edit here, then:

```bash
scripts/install-user-plugins.sh
```

and restart any running grove session (plugins load at startup).

## What's here

| Dir | Command | What it does | Bead |
|-----|---------|--------------|------|
| `mockingbird/` | `/rec` (`/r`) | Voice prompts: mic → whisper-cli → review/edit → send-as-prompt | SPRUCE-GROVE-OS-0ub |
| `junto/` | `/junto` (`/grove`) | Leather Apron Club credo plaque | 5al.1 |
| `backoffice/` | `/backoffice` | Small-business checklist, sourced IRS/AR/Bentonville gates | 5al.4 |
| `creative_scaffold/` | `/creative-scaffold` | Cohort site starters (FPV, artisans) over shared core | 5al.5 |
| `_lib/grove_site_core/` | (import) | Shared scaffold renderer the cohort plugins ride | 5al.3+ |

`_lib/` installs to `~/.spruce_grove/lib/` (the plugin-lib contract that
`creative_scaffold` bootstraps onto `sys.path`). The `_` prefix matches the
loader's own skip-convention: underscore dirs are support, not plugins.

## Notes

- Mockingbird's env-var config (`SPRUCE_MOCKINGBIRD_*`) is documented in
  `mockingbird/README.md`.
- The install is copy-only and never deletes; remove a plugin by deleting it
  from both here and `~/.spruce_grove/plugins/` in the same sitting.
