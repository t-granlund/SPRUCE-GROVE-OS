# Code Puppy — Field Guide Map

> **Purpose.** This is the single source of truth for *what the "field guide" is,
> where every piece lives, how the pieces relate, and how they are (re)built.
> Read this when you need complete context on the field guide and its
> associated pages — before editing any of them.
>
> **Scope.** Three surfaces, two of them literally titled "Code Puppy Field
> Guide": (A) the home-dir live-inventory guide, (B) the in-repo generated doc
> site, (C) the `pages-hub/` public mirror. Surfaces A and B are **independent
> pipelines** with **different data sources** and **different numbers** — this
> is the #1 thing to understand.

**Status note.** This map was written by inspecting the live files on
2026-08-20. It flags several drift/gap issues at the end; fix those before
trusting any individual number as canonical.

---

## TL;DR — the three surfaces

| | A. Home live guide | B. Repo field guide | C. pages-hub mirror |
|---|---|---|---|
| **Title** | "The Code Puppy Field Guide · Live System Inventory · v4" | "Code Puppy Field Guide" | "Code Puppy, documented." |
| **Path** | `~/agent-venn.html` *(outside repo)* | `code_puppy/docs/field-guide/` | `code_puppy/pages-hub/` |
| **Form** | 1 self-contained HTML, no build, no server, no framework | `index.html` + `app.js` renderer + `data.js` blob | 4 HTML pages + shared `assets/` |
| **Data source** | live runtime via `extract_field_guide.py` | git log + runtime via `generate-field-guide.py` | reads B's `data.js` for `updates.html` |
| **Data var** | `FIELD_GUIDE_DATA` (injected `<script>` block) | `window.FIELD_GUIDE_DATA` (`data.js`) | (B's data, re-rendered) |
| **Snapshot** | 62 tools / 22 agents / 55 plugins / 4 skills / 59 hooks / 16 models / 0 mcp | 59 tools / 22 agents / 61 plugins / 5 skills / 776 commits / 3 releases | derived from B |
| **Tests** | `tests/e2e/run_e2e.py` (8/8 PASS, current) | none | none |

**The two field guides overlap in name but differ in scope:** A is a *live
runtime inventory* (what's actually installed right now) plus a deep-dive on
the two-orchestrator agent pack; B is a *generated doc site* (narrative +
catalogs) produced from the repo. They are not generated from each other.

---

## Surface A — Home live-inventory guide (`~/agent-venn.html`)

**Lives outside the fork**, at the home directory. Single static HTML page;
makes **zero network calls**. The data is injected as a `<script>` block:

```html
<script>
const FIELD_GUIDE_DATA = { ... };
</script>
```

### Page structure (13 sections, 13 nav links — current v4)

Hero: kicker `THE CODE PUPPY FIELD GUIDE · LIVE SYSTEM INVENTORY · v4`,
h1 `One kennel. Every dog in it.`, 6 live stat cards. Sticky nav links to:

1. `#architecture` — "Six layers, plugin-first"
2. `#pack` — "One pack, two missions" (the two-orchestrator agent pack)
3. `#agents` — "Every agent in the kennel"
4. `#anatomy` — "Three minds, one decision loop" — 3-circle SVG Venn (Architect / web-puppy / web-retriever / Shared) with tab + circle-click swap
5. `#orchestration` — "The core workflow: conduct, don't carry"
6. `#routing` — "Who gets the job? Follow the tree"
7. `#pipeline` — "The five-step decision pipeline" (Research First → Analyze Options → Document Decision → STRIDE Security → Fitness Functions)
8. `#tools` — "Every tool in TOOL_REGISTRY" (Toolbelt, filterable)
9. `#plugins` — "55 plugins on 59 hook phases"
10. `#skills` — "Opt-in knowledge, pluggable models"
11. `#plays` — "Four plays it runs"
12. `#guardrails` — "What it is — and what it refuses to be"
13. `#careerplays` — "How the career orchestrator runs the pack"

### Build pipeline (home dir, outside repo)

```
extract_field_guide.py   →  ~/field_guide_data.json        (live runtime inventory)
rebuild_field_guide.py   →  extract → inject into agent-venn.html → run E2E
```

- **`~/extract_field_guide.py`** — imports the live `code_puppy` package
  (`TOOL_REGISTRY`, `agent_manager`, `load_plugin_callbacks`, skill discovery,
  MCP registry, `callbacks.PhaseType`), groups tools heuristically, and writes
  `~/field_guide_data.json`. Run: `uv run --project ~/code_puppy python ~/extract_field_guide.py`
- **`~/rebuild_field_guide.py`** — one-command rebuild: extract → idempotently
  swap the `FIELD_GUIDE_DATA` `<script>` block in `agent-venn.html` (regex
  replace if present, else insert before the main `<script>`) → run the E2E
  suite. `--no-test` skips tests. Prints the `open -na "Google Chrome"` command.

### Tests (`~/tests/e2e/`)

- **`tests/e2e/run_e2e.py`** — **authoritative**. Self-contained Playwright
  (sync_api) runner; serves the HTML over in-process `http.server` on
  `127.0.0.1` (free port), drives it headless Chromium 1280×900, writes
  `tests/e2e_report.json` + a collocated copy. Run: `python3 tests/e2e/run_e2e.py`
- **`tests/e2e/test_agent_venn.py`** — pytest variant for CI (self-contained
  fixtures; does **not** require the pytest-playwright plugin).
- **`tests/e2e_manifest.json`** — feature → source → test mapping.
- **`tests/e2e_report.json`** — execution results (current: **8/8 PASS**).

>  **Drift (see Gaps G1).** `run_e2e.py` + `e2e_report.json` track the current
> v4 page (h1 "One kennel…", 6 stat cards, 13 links, 62 tools). But
> `test_agent_venn.py` and `e2e_manifest.json` still assert the **old** page
> (h1 "Two orchestrators / One specialist pack", 4 stat cards, 7 links, 53
> tools). Running the pytest variant now would **fail F1/F2/F5/F6**.

---

## Surface B — Repo field guide (`code_puppy/docs/field-guide/`)

A generated, launchable local documentation site. Three files do the work:

- **`index.html`** (41 KB) — the shell: nav + 12 section skeletons with empty
  container `div`s (e.g. `#stats-grid`, `#tool-grid`, `#plugins-table`,
  `#skills-grid`) filled at runtime by `app.js` from `data.js`.
- **`app.js`** (24 KB) — the renderer. Reads `FIELD_GUIDE_DATA` /
  `window.FIELD_GUIDE_DATA`, defines `THEME_COLORS` + `TOOL_CATEGORY_COLORS`,
  and has `renderMeta/renderStats/renderOverview/renderCapabilities/render…`
  functions that populate each section. Includes `global-search`.
- **`data.js`** (296 KB) — `window.FIELD_GUIDE_DATA = {…}`. Generated artifact;
  **do not hand-edit** (regenerated by `generate-field-guide.py`). Current
  snapshot: `generatedAt 2026-08-22`, `code-puppy v0.0.768`, head `1fb151bc`,
  59 tools / 22 agents / 62 plugins / 5 skills / 825 commits (2mo) / 3 releases.
- **`changelog.js`** — **removed** (was an empty 0 B placeholder; see Gaps G2).
- **`assets/`** — `code_puppy_logo_noback.png` (nav logo), `favicon.png` (favicon), `puppy.svg`/`puppy-full.svg` (legacy SVG marks).

### Sections (12)

`hero`/stats → `overview` (What is Code Puppy? + philosophy cards) →
`capabilities` (Core Feature Set) → `architecture` (How It Fits Together +
diagram) → `tools` (Tool Catalog + filters) → `agents` (Agent System +
base-agent excerpt) → `agent-creator` → `helios` (The Universal Constructor) →
`plugins` (Plugin Ecosystem table) → `commands` (Slash & Console) →
`skills` (Skills You Can Activate).

### Generators (in `code_puppy/docs/`)

- **`docs/generate-field-guide.py`** (24 KB) — reads the live repo (git log,
  agents, tools, plugins, commands, skills, model config) and emits **both**
  `docs/field-guide/data.js` **and** the portable single-file
  `docs/field-guide-flat.html`. Run: `cd ~/code_puppy && python docs/generate-field-guide.py`
- **`docs/field_guide_changelog.py`** — supplies the `changelog_data` dict
  consumed by the generator: recent ~2-month commits on `main` + monthly
  release buckets (`{total_commits, releases[], commits[]}`).
- **`docs/field-guide-flat.html`** (361 KB) — single-file version of the guide
  that opens without a server (data inlined).

---

## Surface C — pages-hub public mirror (`code_puppy/pages-hub/`)

"Code Puppy, documented." — the public knowledge-base mirror
(`mpfaffenberger/code_puppy` → `t-granlund/code_puppy`), rebuilt daily by an
`update_schedule` pipeline.

### Pages

- **`index.html`** (13 KB) — the hub. Sticky nav: **Hub · Field Guide ·
  Releases · Architecture · Flat Docs · GitHub**, plus 4 hero cards
  (field-guide / releases / architecture / flat).
- **`architecture.html`** (37 KB) — "The machine, explained." Interactive
  inventory explorer: search box (`#q`) over plugins/agents/tools/skills, a
  count + `#inv` grid, and a detail **sheet/popover** (`#sheet`/`#bd`).
- **`updates.html`** (46 KB) — the **release observatory**. Hand-curated
  deep-dive narratives plus **auto-managed regions** regenerated from B's
  `data.js` (see below).
- **`design.html`** (12 KB) — "Design System": tokens, iconography (renders
  the `BB.icon()` set), components, accessibility.  **Orphan** — linked
  from **no** nav across the hub (see Gaps G3).

### `generate-updates.py` (the only pages-hub generator)

Regenerates the auto-managed regions of `updates.html` **only between**
`<!-- AUTO-BEGIN:name -->` / `<!-- AUTO-END:name -->` markers; hand-curated
content outside the markers is untouched. Regions: `stats`, `toc`,
`auto-features`, `minor-list`, `fixes-list`. It reads
`docs/field-guide/data.js`, bucketizes commits by conventional-commit type
(feat/fix/refactor/perf/docs/…), emits hero statline numbers, auto-cards for
notable *uncurated* feats, and minor/fix lists. **Idempotent**: it strips its
own auto regions before reading curated hashes so repeated runs converge to a
fixed point. Run: `uv run python pages-hub/generate-updates.py`

### Shared `assets/`

`icons.js` (`BB.icon(name,size)` — the icon factory used by `design.html`),
`popover.css`/`popover.js` (detail sheet), `shell.js`, `sidebar.css`/`sidebar.js`,
`tokens.css` (design tokens), `code_puppy_logo_noback.png` (brand logo), `favicon.png`, `puppy.svg`/`puppy-full.svg` (legacy SVG marks).

###  Deploy convention (see Gaps G4)

Every nav link uses **directory-pretty-URLs**: `./field-guide/`, `./releases/`,
`./architecture/`, `./flat/`, with `../index.html` back-links. The physical
files do **not** match 1:1 (`architecture.html`, `updates.html`,
`docs/field-guide/`, `docs/field-guide-flat.html`). So a **deploy/build step**
is implied that maps files → `dir/index.html`. No such build script lives in
`pages-hub/` — viewing locally by opening the HTML directly will give broken
nav. Treat the directory hrefs as the deployment contract.

---

## Data flow

```
                          ┌──────── Surface B (repo) ────────┐
   git + live runtime      generate-field-guide.py            │
        │                  ──► docs/field-guide/data.js ──┐   │
        │                  ──► docs/field-guide-flat.html │   │
        │                                                ▼   │
        │                  docs/field-guide/app.js ◄── renders │
        │                                                │   │
        │                  pages-hub/generate-updates.py ◄────┘ (B feeds C)
        │                  ──► pages-hub/updates.html
        │
   live runtime only       ┌──────── Surface A (home) ──────┐
        │                  extract_field_guide.py              │
        │                  ──► ~/field_guide_data.json ──┐    │
        │                  rebuild_field_guide.py        │    │
        │                  ──► ~/agent-venn.html ◄────────┘    │
        │                  ──► tests/e2e/ (validate)          │
```

A and B are **parallel**, not serial: A reads the *installed runtime*;
B reads the *repo* (git + runtime). That is why their counts differ.

### Inventory divergence (why the numbers disagree)

| Metric | A `field_guide_data.json` | B `data.js` |
|---|---|---|
| tools | 62 | 59 |
| agents | 22 | 22 |
| plugins | 55 | 61 |
| skills | 4 | 5 |
| hooks | 59 | — |
| models | 16 | — |
| mcp | 0 | — |
| commits (2mo) | — | 776 |

Different extractors + different snapshot moments + different counting rules
(e.g. A counts plugin dirs with `register_callbacks.py`; B's generator counts
plugins another way). **Do not assume one is "wrong"** — pick the source
appropriate to the surface you're editing.

---

## Full file map

### Surface A — home dir (outside the fork)
| File | Role |
|---|---|
| `~/agent-venn.html` | rendered live-inventory guide (data injected inline) |
| `~/extract_field_guide.py` | live runtime → `field_guide_data.json` |
| `~/rebuild_field_guide.py` | extract → inject → E2E (one command) |
| `~/field_guide_data.json` | extracted inventory blob (A's data) |
| `~/tests/e2e/run_e2e.py` | **authoritative** Playwright runner (current) |
| `~/tests/e2e/test_agent_venn.py` | pytest variant (**stale** vs v4) |
| `~/tests/e2e/e2e_manifest.json` | feature map (**stale** vs v4) |
| `~/tests/e2e/e2e_report.json` | latest results (8/8 PASS) |
| `~/tests/e2e_manifest.json` | duplicate manifest at tests root |

### Surface B — repo field guide
| File | Role |
|---|---|
| `docs/field-guide/index.html` | page shell + section skeletons |
| `docs/field-guide/app.js` | renderer (reads `FIELD_GUIDE_DATA`) |
| `docs/field-guide/data.js` | generated data blob (B's data) — do not hand-edit |
| `docs/field-guide/changelog.js` | **removed** (was empty, unused) |
| `docs/field-guide/assets/*` | puppy svgs |
| `docs/generate-field-guide.py` | generator → `data.js` + flat html |
| `docs/field_guide_changelog.py` | changelog data supplier |
| `docs/field-guide-flat.html` | portable single-file guide |

### Surface C — pages-hub
| File | Role |
|---|---|
| `pages-hub/index.html` | hub (nav + 4 cards) |
| `pages-hub/architecture.html` | inventory explorer (search + sheet) |
| `pages-hub/updates.html` | release observatory (auto + curated) |
| `pages-hub/design.html` | design system (**orphan**) |
| `pages-hub/generate-updates.py` | regenerates `updates.html` auto regions from B |
| `pages-hub/assets/*` | icons/popover/shell/sidebar/tokens/svgs |

---

## Rebuild runbook

Refresh everything from live sources, in dependency order:

1. **B — repo field guide data:**
   `cd ~/code_puppy && python docs/generate-field-guide.py`
   → rewrites `docs/field-guide/data.js` + `docs/field-guide-flat.html`.
2. **C — release observatory (depends on B):**
   `cd ~/code_puppy && uv run python pages-hub/generate-updates.py`
   → rewrites only the auto regions of `pages-hub/updates.html`.
3. **A — home live guide (independent of B/C):**
   `python3 ~/rebuild_field_guide.py`
   → extract → inject `agent-venn.html` → run E2E (8/8).
   Add `--no-test` to skip tests.
4. **View:**
   - A: `open -na "Google Chrome" --args "file://$HOME/agent-venn.html"`
   - B: serve `docs/field-guide/` over HTTP (it loads `data.js` via `<script src>`).
   - C: requires the deploy/build mapping for directory hrefs to resolve.

---

## Gaps & drift to fix

- **G1 -- stale tests (A).** **FIXED.** Synced `tests/e2e/test_agent_venn.py`
  and `tests/e2e/e2e_manifest.json` to page v4: h1 "One kennel. Every dog in it.",
  6 live stat cards (driven by `FIELD_GUIDE_DATA.stats`), 13 nav links, 13 sections,
  dynamic tool counts from live data, new F8 live-explorers test (agents/plugins/
  hooks/skills/models counts + search). Pytest variant now mirrors `run_e2e.py`.
- **G2 -- empty changelog (B).** **FIXED.** Removed the 0 B `changelog.js`,
  its `<script>` tag in `index.html`, and the read+inline code in
  `generate-field-guide.py`. The changelog data it was meant to hold already
  lives in `data.js` under `FIELD_GUIDE_DATA.changelog` and is rendered by
  `app.js`.
- **G3 -- orphan design page (C).** **FALSE ALARM.** `design.html` is NOT an
  orphan. All pages-hub pages load `assets/shell.js`, which auto-generates a
  sidebar with 6 nav items including "Design System" (`key: "design"`). The
  hardcoded `<nav class="nav">` blocks in `index.html`/`architecture.html`/
  `updates.html` are legacy top-navs that predate `shell.js` and are suppressed
  by `sidebar.css` (`.sb-legacy-topnav { display: none !important; }`). They
  lack the Design link but are invisible. Optional cleanup: remove the dead
  legacy `<nav>` markup from those 3 files.
- **G4 -- pages-hub deploy mapping.** **DOCUMENTED.** Confirmed via
  `shell.js` NAV array: each page uses directory-pretty-URLs
  (`base + "field-guide/"`, `base + "architecture/"`, etc.) and `../assets/`
  relative paths, meaning the deploy step copies each `pages-hub/<name>.html`
  to `pages-hub/<name>/index.html`. This is handled by the external
  `update_schedule` pipeline (per `index.html` footer: "rebuilt daily"), not
  by any script in the repo. No code to write -- just document the convention.
- **G5 -- duplicate manifest.** **FIXED.** Removed stale root-level
  `tests/e2e_manifest.json`. Canonical location is `tests/e2e/e2e_manifest.json`
  (the manifest's own `test_artifacts` points there; `run_e2e.py` does not
  reference the manifest at all). The root-level `tests/e2e_report.json` is
  intentionally dual-written by `run_e2e.py` and stays.
- **G6 -- mcp=0 (A).** **FIXED.** The mcp=0 result was correct (no MCP servers
  configured -- `mcp_registry.json` does not exist). But `extract_field_guide.py`
  had a latent import bug: it imported `MCPRegistry` (wrong class name; the real
  class is `ServerRegistry`) and called `list_servers()` (wrong method; the real
  method is `list_all()`). The `except` block caught the ImportError and fell
  back to reading the missing file, so the result was accidentally correct.
  Fixed the import and method calls; result unchanged (still 0 servers).

---

## Related context (not part of the field guide, but adjacent)

- `README.md` (29 KB) — repo overview, badges, sovereignty, install.
- `AGENTS.md` — agent conventions for contributors.
- `BUILD-LOG.md` — build/release log.
- `SOVEREIGNTY.md` — data-sovereignty commitments.
- `docs/HOOKS.md`, `docs/AGENT_SKILLS.md`, `docs/I18N.md`, `docs/FLUX.md`,
  `docs/CEREBRAS.md`, `docs/LEFTHOOK.md` — topical deep-dives.
- `changelog/` — release changelog source.
- `docs/decks/the-great-adpuppytion/` — a separate presentation deck (own
  tests/assets), not part of the field guide.
