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
| `pydantic-ai-slim[openai,anthropic]` | 47 files / 92 import statements (recomputed 2026-09-22 evening, after the tool-context vocabulary landing; was 61 / 114) | **KEEP behind the seam.** Exit plan = `SOVEREIGNTY.md` Phases 2-4. Call-site files routed through the seam: 34 now import `spruce_grove.harness` — model resolution, the settings surface (`_builder.py` no longer imports `model_factory` at all), and the `ToolContext` tool vocabulary; 18 of them no longer mention `pydantic-ai` at all. |
| `pydantic-ai-harness` | 4 imports (compaction, output limits, `/truncate`) | Same seam. Phase 3 recreates compaction/limits grove-owned, then this drops. |

## Tier 1 — HTTP clients (consolidate eventually)

| Dependency | Used by | Verdict |
|---|---|---|
| `httpx[http2]` | 11 imports (gemini, health, servers, http_utils) | **KEEP** — primary client. |
| `httpx2` | 5 imports (codex client, claude cache/oauth transports) | **KEEP, documented.** Separate transport used where provider quirks demand it; consolidate onto one client in the ladder below. |
| `requests` | 3 imports, but the real surface is the universal constructor: generated tool code imports `requests` (documented examples teach it) and `create_requests_session` feeds that environment | **KEEP — revised 2026-09-16.** This is a generated-code contract surface, not a dedupe target. |
| `openai`, `anthropic` SDKs | 3 imports (model_factory) + required by pydantic-ai extras | **KEEP** — provider SDKs ride behind the harness seam. |

## Tier 2 — Declared but not imported (verify, then prune)

| Dependency | Grove source | Core plugins | Verdict |
|---|---|---|---|
| `typer` | 0 imports | 0 imports | **REMOVED 2026-09-16** — computed unused by both codebases; suite green without it. |
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
| Google Fonts (`fonts.googleapis.com`) | was 10+ pages-hub pages on Google's CDN | **SELF-HOSTED 2026-09-16** — 12 latin woff2 faces (592K) + `fonts.css` + OFL notice; 16 pages swapped; zero third-party CDN calls remain. |
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

1. **Pin CI actions by SHA** (Tier 4) — **DONE 2026-09-16**: 4 workflows, 5 actions pinned to immutable commits (checkout, setup-python, pages artifacts, pypi-publish); yaml-validated.
2. **Drop `typer`** (Tier 2) — **DONE 2026-09-16**: removed from pyproject + lock (typer, shellingham swept); full suite 7,873 passed.
3. **Self-host the site fonts** (Tier 5) — **DONE 2026-09-16**: 12 latin woff2 faces + `fonts.css` + OFL notice; 16 pages swapped off the CDN.
4. ~~**Dedupe `requests` onto `httpx`**~~ — **REVISED 2026-09-16, KEEP**: the real surface is generated-code contracts (the universal constructor's environment), not 3 import sites. The census's import count was true but not the whole truth.
5. **Replace `pyfiglet` with baked art** (Tier 3) — **DONE 2026-09-16**: `spruce_grove/banner_art.py` bakes both renders byte-identically; pyfiglet dropped; suite green. **RE-BAKED 2026-09-23**: the figlet `ansi_shadow` block art read as 8-bit, so the wordmark is now drawn in braille by `scripts/bake_braille_banner.py` — same 6-row / 96-column contract, `--check` guards drift against the copy in `splash.py`.
6. **Supply-chain bumps** (Tier 3/4) — **DONE 2026-09-16**: `pip-audit` found 53 known vulnerabilities across 8 packages (pillow, pyjwt, cryptography, httpx2, mcp, json-repair, h2, pydantic-settings); lock upgraded to fix versions; re-audit clean. Found during the D2 re-run.
7. **Gate-flagged: `mcp` 2.x migration** (Tier 3) — discovered mid-bump when the resolver jumped a major version and broke FastMCP; pinned `<2`, CVE fix taken from the 1.x line (1.30.0). The 2.x rename is its own deliberate landing.
8. **Extra-gate `boto3`/`azure-identity`** (Tier 2) — plugin-consumed; behind extras once lazy imports allow. *PARKED.*
9. **Vendor or formally adopt `code-puppy-core-plugins`** (Tier 3) — council decision after the compat contracts land. *PARKED.*
10. **The harness itself** — the largest dependency of all; tracked as Program A in the dashboard and `SOVEREIGNTY.md`. *IN-FLIGHT (34 files now import the seam; model resolution + settings surface + the tool-context vocabulary landed 2026-09-22).*

Rule: a ladder item only flips to *done* with its receipt (tests green, hash
proof, or a diff) — the dashboard says so too.
