# DEPENDENCY-EXIT — the external-dependency census and ladder

> The level-set of everything this project consumes that someone else made.
> Companion to `SOVEREIGNTY.md` (the harness exit), `PROVENANCE.md` (lineage),
> and `docs/SOVEREIGNTY-EXECUTION.md` (the task board). Public mirror: the
> **Dashboard** (`/dashboard.html`) renders this ladder.
>
> The rule of the census, same as the board: **counts are computed, never
> claimed.** Every "unused" verdict below came from a grep, not a guess.

Census date: 2026-09-15 &middot; pyproject 1.0.50 &middot; uv.lock 146 packages

---

## Tier 0 — The harness (the big one)

| Dependency | Used by | Verdict |
|---|---|---|
| `pydantic-ai-slim[openai,anthropic]` | 110 imports across the agent layer | **KEEP behind the seam.** Exit plan = `SOVEREIGNTY.md` Phases 2-4. Call sites migrated: 2 of ~58 (computed by the board). |
| `pydantic-ai-harness` | 4 imports (compaction, output limits, `/truncate`) | Same seam. Phase 3 recreates compaction/limits grove-owned, then this drops. |

## Tier 1 — HTTP clients (consolidate eventually)

| Dependency | Used by | Verdict |
|---|---|---|
| `httpx[http2]` | 11 imports (gemini, health, servers, http_utils) | **KEEP** — primary client. |
| `httpx2` | 5 imports (codex client, claude cache/oauth transports) | **KEEP, documented.** Separate transport used where provider quirks demand it; consolidate onto one client in the ladder below. |
| `requests` | 3 imports (http_utils, universal_constructor) | **DEDUPE candidate** — httpx already here; fold the 3 call sites, drop. |
| `openai`, `anthropic` SDKs | 3 imports (model_factory) + required by pydantic-ai extras | **KEEP** — provider SDKs ride behind the harness seam. |

## Tier 2 — Declared but not imported (verify, then prune)

| Dependency | Grove source | Core plugins | Verdict |
|---|---|---|---|
| `typer` | 0 imports | 0 imports | **REMOVE** — computed unused by both codebases. |
| `agent-client-protocol` | 0 imports | yes (`acp` plugin, `acp.schema`) | **KEEP** — the ACP native-agent surface. |
| `boto3` | 0 imports | yes (bedrock models) | **KEEP** (plugins), consider extra-gating. |
| `azure-identity` | 0 imports | yes (discovery/token) | **KEEP** (plugins), consider extra-gating. |
| `dbos` | 0 imports | yes (durable runtime) | **KEEP as `durable` extra** (already is). |
| `termflow-md` | yes (`tools/display.py`, imports as `termflow`) | - | **KEEP** — tool-output rendering. |
| `ripgrep` (binary, pinned 14.1.0) | yes (grep tool finds executable) | - | **KEEP** — vendoring is a ladder item, not a now item. |

## Tier 3 — Core runtime (grove-owned behavior, third-party parts)

| Dependency | Used by | Verdict |
|---|---|---|
| `rich` | 107 imports | **KEEP** — the entire TUI. Grove-owning this is a multi-year moonshot; not on the ladder. |
| `pydantic` | transitive + direct | **KEEP** with the harness. |
| `pyfiglet` | 2 imports (boot banner, onboarding slides) | **REPLACE candidate** — `splash.py` already bakes the banner constants; render from constants and drop pyfiglet. |
| `rapidfuzz`, `json-repair`, `Pillow`, `keyring`, `python-dotenv`, `packaging`, `mcp`, `anyio`, `logfire` | various | **KEEP** — each earns its keep; `logfire` is opt-in telemetry (self-hostable later). |
| `code-puppy-core-plugins` | the plugin tier | **KEEP** — versioned sibling repo; eventual vendoring decision belongs to the council (see `COMPAT-EXIT.md`). |

## Tier 4 — CI / supply chain

| Item | State | Action |
|---|---|---|
| `actions/checkout@v4`, `setup-python@v5`, `upload-pages-artifact@v3`, `deploy-pages@v4`, `pypa/gh-action-pypi-publish@release/v1` | tag-pinned (mutable) | **PIN BY SHA** — small, do it in one sweep. |
| `actions/github-script`, `alibaba/open-code-review` | already SHA-pinned | keep. |
| npm / node / axios | **absent** (verified: no package.json anywhere in-repo; node removed from CI per board D1) | nothing to do. |

## Tier 5 — Site and assets

| Item | State | Action |
|---|---|---|
| Google Fonts (`fonts.googleapis.com`) | 10 pages-hub pages load Fraunces/Inter/JetBrains Mono from Google's CDN | **SELF-HOST** — download the families into `pages-hub/assets/fonts/`, swap to `@font-face`. Removes an external CDN from a privacy-first product's public face. |
| Favicons/app icons | `pages-hub/assets/` == `logos/` masters (hash-verified); stale solid-mark pair in root `assets/` deleted 2026-09-15 | done; `scripts/sync-brand-assets.sh` + brand-check workflow guard drift. |
| Copy buttons, nav JS | inline, zero dependencies | keep. |

## Tier 6 — Tooling and infrastructure (not shipped, but load-bearing)

| Item | Role | Verdict |
|---|---|---|
| Docker (forgejo 9-rootless, woodpecker v3, caddy 2) | `scripts/sovereignty/forgejo-stack/` — the off-GitHub release rails | **KEEP** — this IS the exit infrastructure; pin image digests at stand-up (board C5). |
| Dolt / beads | issue tracker | **KEEP** — data lives in-repo (`refs/dolt/data` sync); the export is passive JSONL. |
| uv | Python toolchain + publishing | **KEEP** — the rails (PyPI trusted publishing, OIDC). |
| Homebrew | one doc mention (`user-plugins/mockingbird/README.md`) | doc only. |
| Desktop app | separate repo (`spruce-grove-desktop`, Tauri) | out of scope here; same census method applies there. |
| Colima + postgres | local dev containers (machine-level, not repo) | not a product dependency. |

---

## The ladder (ordered, honest)

1. **PIN CI actions by SHA** (Tier 4) — one sweep, zero behavior change. *AUTO.*
2. **Drop `typer`** (Tier 2) — computed unused; run the suite green without it. *AUTO.*
3. **Self-host the site fonts** (Tier 5) — removes Google from the public face. *AUTO.*
4. **Dedupe `requests` onto `httpx`** (Tier 1) — 3 call sites. *AUTO.*
5. **Replace `pyfiglet` with the baked splash constants** (Tier 3) — 2 call sites. *AUTO.*
6. **Harness exit Phases 3-4** (Tier 0) — recreate compaction + agent loop grove-owned behind the seam; then `pydantic-ai-harness` drops, and finally `pydantic-ai-slim` itself. The long march; tracked on the board, rendered on the dashboard.
7. **Extra-gate boto3/azure-identity** (Tier 2) — behind `bedrock`/`azure` extras once plugin lazy-imports allow.
8. **Vendor or formally adopt `code-puppy-core-plugins`** (Tier 3) — council decision, after the compat contracts land (`COMPAT-EXIT.md`).

Rule: a ladder item only flips to *done* with its receipt (tests green, hash
proof, or a diff) — the dashboard says so too.
