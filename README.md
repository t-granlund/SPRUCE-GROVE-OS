# SPRUCE GROVE OS

**gran · lund · sv. · spruce grove** — an agentic coding CLI grown in the grove.

> Together we are better. Always.

![License: MIT](https://img.shields.io/badge/license-MIT-2D4F3A)
![Python 3.11–3.14](https://img.shields.io/badge/python-3.11--3.14-588F5E)
![Tests: 7700 passing](https://img.shields.io/badge/tests-7700%20passing-D2A069)
![Inspired by Code Puppy](https://img.shields.io/badge/inspired%20by-Code%20Puppy-F0E1C8)

Spruce Grove OS is a full custom instance of an agentic coding assistant:
the same engine, frameworks, plugins, agents, tools, skills, MCP plumbing,
and TUI as the project it is inspired by — replanted around one grove's
vision, mission, and values.

## Inspired by Code Puppy

Every trail in this grove started as a Code Puppy trail. Spruce Grove OS is
built directly from — and stays import-compatible with — **Code Puppy** by
[Michael Pfaffenberger](https://github.com/mpfaffenberger/code_puppy)
(MIT licensed). Huge respect to the original project and its contributors;
this grove exists because the puppy shared everything. Exact lineage, sync
points, and the full rename/contract map: [PROVENANCE.md](PROVENANCE.md).

## The ethos of the grove

Three sources, one creed — [ETHOS.md](ETHOS.md):

1. **Ozark Bagels — how to carry yourself.** Be first to say hello. Be kinder
   than necessary. Be tough minded, but tender hearted. Leave everything
   better than you found it. Spread joy, love, and cream cheese.
2. **The Junto (1727) — how to think with others.** Love truth for truth's
   sake. No invented facts — ever; cite or flag "NOT VERIFIED". Provisional
   phrasing over contradiction combat. Pragmatism over metaphysics.
3. **gran·lund — who is doing the carrying.** Help people solve problems.
   Remove technology obstacles. Meet people where they are, as humans.

## Meet Cedar

The default agent persona is **Cedar**, the grove guide — same competent
agent core, new disposition: candid about code, gentle with people, allergic
to invented facts. Rename it anytime in `grove.cfg`.

---

## Design system

Nordic forest, dark-first. Charcoal base, deep spruce, warm cedar accents,
mist typography. Tokens shared with
[tylergranlund.com](https://tylergranlund.com) — the same palette that colors
the terminal splash.

### Color tokens

| Token | OKLCH | Role | Chip |
|---|---|---|---|
| charcoal | `oklch(0.18 0.012 150)` | base background | ![#1d211e](https://img.shields.io/badge/-%23001D21-1d211e) |
| spruce-deep | `oklch(0.22 0.03 158)` | deep brand layer | ![#20392b](https://img.shields.io/badge/-%2320392B-20392b) |
| spruce | `oklch(0.32 0.045 158)` | primary brand | ![#2d4f3a](https://img.shields.io/badge/-%232D4F3A-2d4f3a) |
| moss | `oklch(0.45 0.06 155)` | accent green | ![#588f5e](https://img.shields.io/badge/-%23588F5E-588f5e) |
| cedar | `oklch(0.78 0.12 55)` | warm accent, persona | ![#d2a069](https://img.shields.io/badge/-%23D2A069-d2a069) |
| bark | `oklch(0.32 0.025 60)` | earthy neutral | ![#4d4136](https://img.shields.io/badge/-%234D4136-4d4136) |
| stone | `oklch(0.85 0.012 90)` | soft UI text | ![#d6d2c8](https://img.shields.io/badge/-%23D6D2C8-d6d2c8) |
| mist | `oklch(0.94 0.008 100)` | foreground/typography | ![#f0e1c8](https://img.shields.io/badge/-%23F0E1C8-f0e1c8) |

### Typography

- **Fraunces** (variable serif) — wordmarks and display
- **Inter** — body copy
- **JetBrains Mono** — code, CLI output

### Terminal theming

The boot splash renders a shimmering pyramid + figlet lockup
("SPRUCE GROVE", compact "GROVE" on narrow terminals) in a truecolor
canopy-to-cedar gradient: halo `#2D4F3A` → glow `#588F5E` → core `#D2A069`,
with a mist-white crest (`#F0E1C8`) where the sheen passes. ANSI fallbacks
step down through green → bright green → yellow.

### Voice

Plain-spoken, warm, a little playful. First to say hello. Candid, never
roasty. Zero invented facts — "NOT VERIFIED" beats a confident guess.

Full tokens and voice guide: [BRAND.md](BRAND.md).

---

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

Python 3.11–3.14 · pydantic-ai · pluggable models (OpenAI, Anthropic,
Gemini, Bedrock, Z.AI, custom endpoints) · MCP servers · skills with
namespaces · session history + compaction · i18n.

## Install & run

```bash
git clone https://github.com/t-granlund/SPRUCE-GROVE-OS
cd SPRUCE-GROVE-OS
uv sync
uv run spruce-grove        # or: uv run grove
```

Config: `~/.spruce_grove/grove.cfg` · Env vars: `SPRUCE_GROVE_*`.

## Code Puppy compatibility

- `code_puppy.*` imports (e.g. from `code-puppy-core-plugins`) resolve to
  `spruce_grove.*` via an import shim with true module identity.
- The plugin entry-point group `code_puppy.plugins` is intentionally retained.
- Legacy aliases kept: `agent_code_puppy`, `CodePuppyAgent`,
  `get_puppy_name()`, persisted `puppy_name` fallback.
- Full contract ledger: [PROVENANCE.md](PROVENANCE.md).

## License

MIT — inherited from Code Puppy. See [LICENSE](LICENSE) and attribution in
[PROVENANCE.md](PROVENANCE.md).
