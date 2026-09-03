# SPRUCE GROVE OS

**gran·lund · sv. · spruce grove** — an agentic coding CLI grown in the grove.

> Together we are better. Always.

Spruce Grove OS is a full custom instance of an agentic coding assistant: the
same engine, frameworks, plugins, agents, tools, skills, MCP plumbing, and
TUI as the project it is inspired by — replanted around one grove's vision,
mission, and values.

## Inspired by Code Puppy

Every trail in this grove started as a Code Puppy trail. Spruce Grove OS is
built directly from — and stays compatible with — **Code Puppy** by
[Michael Pfaffenberger](https://github.com/mpfaffenberger/code_puppy)
(MIT licensed). Huge respect and gratitude to the original project and its
contributors; this grove exists because the puppy shared everything.

See [PROVENANCE.md](PROVENANCE.md) for exact lineage, sync points, and the
complete rename/contract mapping.

## The ethos of the grove

Three sources, one creed — adapted from Tyler Granlund's master orchestration
docs ([ETHOS.md](ETHOS.md)):

1. **Ozark Bagels — how to carry yourself.** Be first to say hello. Be kinder
   than necessary. Be tough minded, but tender hearted. Leave everything
   better than you found it. Spread joy, love, and cream cheese.
2. **The Junto (1727) — how to think with others.** Love truth for truth's
   sake. No invented facts — ever; cite or flag. Provisional phrasing over
   contradiction combat. Pragmatism over metaphysics: build things that WORK.
   Mutual aid: "How can the Junto assist you in any of your honorable designs?"
3. **gran·lund — who is doing the carrying.** Help people solve problems.
   Remove technology obstacles. Meet people where they are, as humans.

## Meet Cedar

The default agent persona is **Cedar**, the grove guide — same competent
agent core, new disposition: candid about code, gentle with people, allergic
to invented facts. Rename it anytime; the config keys live in `grove.cfg`.

## What's inside (same bones as Code Puppy)

```
┌──────────────────────────────────────────────────┐
│  TUI / CLI  (command_line/)                      │
├──────────────────────────────────────────────────┤
│  Agent Layer  (agents/)  — Cedar default + JSON  │
├──────────────────────────────────────────────────┤
│  Tool Layer  (tools/)    — TOOL_REGISTRY         │
├──────────────────────────────────────────────────┤
│  Plugin Layer  (plugins/, callbacks.py)          │
├──────────────────────────────────────────────────┤
│  Model Layer  (model_factory.py)                 │
├──────────────────────────────────────────────────┤
│  pydantic-ai + MCP (external)                    │
└──────────────────────────────────────────────────┘
```

Python 3.11–3.14, pydantic-ai, pluggable models (OpenAI, Anthropic, Gemini,
Bedrock, Z.AI, custom endpoints), MCP servers, skills with namespaces,
session history + compaction, i18n — the whole kennel... er, grove.

## Install & run

```bash
# from source, with uv (recommended)
git clone https://github.com/t-granlund/SPRUCE-GROVE-OS
cd SPRUCE-GROVE-OS
uv sync
uv run spruce-grove        # or: uv run grove
```

Config directory: `~/.spruce_grove/` (config file `grove.cfg`).
Environment variables are `SPRUCE_GROVE_*` (see PROVENANCE.md for the
`CODE_PUPPY_*` mapping).

## Code Puppy compatibility

- Imports of `code_puppy.*` (e.g. from `code-puppy-core-plugins`) resolve to
  `spruce_grove.*` via an import shim (`spruce_grove/_code_puppy_compat.py`).
- The plugin entry-point group `code_puppy.plugins` is intentionally retained
  so the official core-plugin bundle keeps loading.
- Legacy aliases kept: `agent_code_puppy` module, `CodePuppyAgent`,
  `get_puppy_name()`, and the persisted `puppy_name` config key fallback.
- Legacy `CODE_PUPPY_*` env vars are NOT auto-read — rename them to
  `SPRUCE_GROVE_*` when migrating.

## Brand

Nordic forest, dark-first: charcoal base, deep spruce, warm cedar accents,
mist typography. Display font Fraunces, body Inter, mono JetBrains Mono —
shared with [tylergranlund.com](https://tylergranlund.com). Tokens live in
[BRAND.md](BRAND.md).

## License

MIT — inherited from Code Puppy. See [LICENSE](LICENSE) and the attribution
in [PROVENANCE.md](PROVENANCE.md).
