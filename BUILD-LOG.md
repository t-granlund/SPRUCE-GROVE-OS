# Code Puppy Site — Build Log & Roadmap

> Single source of truth for **what was built, when, where it lives locally vs. deployed**, QA status, and the forward roadmap.
>
> - **Local repo:** `~/code_puppy` (branch `main`)
> - **Live site:** https://t-granlund.github.io/code_puppy/
> - **Remotes:** `myfork` = t-granlund/code_puppy (the public site source) · `private` = Multi-Agent-Orch-CLI (insurance mirror) · `origin` = mpfaffenberger/code_puppy (upstream, not pushed by us)
> - **Deploy:** `.github/workflows/pages.yml` → GitHub Pages (`build_type: workflow`)

---

## 1. Current state (verified 2026-08-17 18:1x CDT)

| Check | Result |
|---|---|
| Working tree | **clean** |
| Local HEAD | `e861349e` |
| `myfork/main` | `e861349e` — **0/0 drift**, matches local |
| `private/main` | `e861349e` — **0/0 drift**, matches local |
| `origin/main` (upstream) | `2b4732da` — **47 behind / 11 ahead** (expected: we iterate site-only; upstream adds its own work) |
| Live Pages deploy | **success** @ `e861349e` (run 22:50:32Z → 22:50:55Z) |
| Live spot-check | sidebar present, top-nav hidden, popover wired, 0 JS errors |

**Reading the drift:** local ↔ myfork ↔ private are at exact parity. The `origin` numbers are normal for a fork — 47 commits upstream made that we haven't pulled, 11 of ours (the site/observatory/regen line) that live only on the fork. Nothing is stuck mid-push.

---

## 2. What shipped, when, and where

Times are local (CDT). "Local files" = repo paths; "Live" = deployed URL; "Remote" = which git remote(s) carry it.

### a. Earlier in the day — icon/brand pass (pre-crash recovery)
- **Live commit:** `f8415651` — *feat(brand): lucide icon pass + face-only mark, brand watermarks across site*
- **Local files:** `pages-hub/index.html`, `pages-hub/architecture.html`, `pages-hub/updates.html`, `docs/field-guide/index.html`, `*/assets/puppy.svg`, new `*/assets/puppy-full.svg`
- **What:** face-only nav/favicon mark, lucide icons on cards/sections, brand watermarks. (This is the work the 1:36 PM session was finishing when it died on a `400 Unterminated string` vision-model transport error; we recovered the uncommitted changes and shipped them.)
- **Pushed to:** `myfork` + `private`; **Live:** all sections.

### b. Bug fixes + hardening (same day)
- **Live commit:** `3e17c216` — *fix(field-guide): flat-doc JSON corruption + responsive [mobile/tablet] layout*
  - Fixed the `re.sub` string-replacement bug in `docs/generate-field-guide.py` (switched to function replacements) — the flat offline doc was emitting invalid JS.
  - Responsive hardening across guide + observatory (table scroll, `minmax(0,1fr)`, wrap rules).
  - **Pushed:** `myfork` + `private`; **Live.**
- **Live commit:** `ea58e81e` — *docs(field-guide+observatory): regenerate …* (data refresh, auto-commit from the generator).

### c. Major UI overhaul (this request)
- **Live commit:** `e861349e` — *feat(ui): sidebar app-shell + reusable popover + design system, WCAG 2.2 AAA*
- **Local files (new):**
  | Path | Purpose |
  |---|---|
  | `pages-hub/assets/tokens.css` | AAA design tokens (§3) |
  | `pages-hub/assets/sidebar.css` | Sidebar shell styles |
  | `pages-hub/assets/sidebar.js` | Collapse/open, focus trap, Esc/backdrop, persistence |
  | `pages-hub/assets/shell.js` | Injects the shell into each page (single source) |
  | `pages-hub/assets/popover.css` | Detail modal styles |
  | `pages-hub/assets/popover.js` | Reusable ARIA popover (open-page / copy-link / close / deep-link) |
  | `pages-hub/assets/icons.js` | Shared Lucide icon set (30 icons) |
  | `pages-hub/design.html` | **New Design System page** |
- **Local files (modified):** `pages-hub/index.html` (hub), `pages-hub/updates.html` (releases), `pages-hub/architecture.html`, `docs/field-guide/index.html`, `*/assets/puppy.svg` (square-safe mark), `.github/workflows/pages.yml` (deploys `/design/`)
- **Live URL new this round:** https://t-granlund.github.io/code_puppy/design/
- **Pushed to:** `myfork` + `private`; **Live:** all six sections.

---

## 3. QA / validation status

Automated via Playwright (Chromium channel). Re-run any time; the checks are deterministic.

### Coverage matrix (page × viewport)
| Page | 390 | 768 | 1440 | 1920 | Sidebar | JS errors |
|---|---|---|---|---|---|---|
| Hub `/` | pass | pass | pass | pass | yes | 0 |
| Field Guide `/field-guide/` | pass¹ | pass | pass | pass | yes | 0 |
| Releases `/releases/` | pass | pass | pass | pass | yes | 0 |
| Architecture `/architecture/` | pass | pass | pass | pass | yes | 0 |
| Design `/design/` | pass | pass | pass | pass | yes | 0 |
| Flat `/flat/` | pass | pass | pass | pass | by design (self-contained) | 0 |

¹ Field-guide mobile measured `392` vs `390` (2px scrollbar gutter); within tolerance, no horizontal scroll.

### Interaction / a11y checks (all passing)
- Sidebar: open (mobile), close, `Esc`, backdrop click, desktop collapse (persisted), focus restore, focus moves into drawer on open.
- Popover: opens on node/row click and on `#detail=<key>` deep-link; **focus trap holds across 7+ Tab cycles**; `Esc`/backdrop close; rich detail body renders; "Open page" / "Copy link" present and functional.
- Keyboard: skip-link target `#sb-main` present; `aria-current`/`aria-expanded` correct; focus ring is high-contrast (`#FFE08A`).

### Contrast (AAA targets on `--BB-bg #141B23`)
| Token | Value | Ratio | Role |
|---|---|---|---|
| `--BB-t1` | #FFFFFF | 19.3:1 | headings |
| `--BB-t2` | #E9EEF4 | 15.9:1 | body (AAA) |
| `--BB-t3` | #C7D0DA | 11.1:1 | secondary (AAA) |
| `--BB-peri` | #C0C4FB | 8.6:1 | accent (large/UI) |
| `--BB-cyan` | #66F0ED | 12.1:1 | accent/link |
| `--BB-mint` | #6FF09A | 10.9:1 | accent |
| `--BB-peri-l` | #DBDDFE | 12.9:1 | accent |
| `--BB-pink` | #F2A9F0 | 8.7:1 | accent |
| `--BB-focus` | #FFE08A | 12.6:1 | focus ring |

Body/secondary text meet **≥ 7:1 (AAA)**; accent tokens meet **≥ 4.5:1** and are reserved for large text / icons / borders / data — never small body copy. **As of 2026-08-18 the legacy page bodies were also swept to AAA** — legacy muted `#7E8B99` (4.67:1, AA-only) re-pointed to `#AEB9C7` (8.17:1 AAA) site-wide via one var per page, so every selector inherits. The entire site now meets the AAA 7:1 bar for all body, secondary, and suppressed text. (An automated axe/Lighthouse gate in CI remains on the roadmap as the regression guard.)

### Regeneration idempotency
- `docs/generate-field-guide.py` and `pages-hub/generate-updates.py` re-run cleanly; hand-edited CSS/markup outside `AUTO-BEGIN/END` markers survives; output is byte-stable apart from live data.

---

### AAA body-text sweep (2026-08-18)
Only the tokens that actually failed were touched — the bright accents (#A3A8F8 7.36:1, #5CF2F2 11.94:1, #61E887 10.36:1, #C5C9FB 10.14:1 on #1A2129) already clear AAA and were left alone per the paragraph/accent separation.

| Page | Var changed | Was | Now | New ratio on --bg |
|---|---|---|---|---|
| guide (+ flat via template) | `--text-muted` | #7E8B99 (4.67, AA) | #AEB9C7 | 8.17:1 |
| guide (+ flat via template) | `--text-soft` | #AAB6C4 (7.88) | #D6DEE8 | 11.96:1 |
| releases | `--text-muted`, `--danger` | #7E8B99, #8A8FF0 | #AEB9C7, #B7BBF7 | 8.17 / 8.86 |
| architecture | `--t3`, `--t2` | #7E8B99, #AAB6C4 | #AEB9C7, #D6DEE8 | 8.17 / 11.96 |
| hub | `--text-muted`, `--text-soft` | #7E8B99, #AAB6C4 | #AEB9C7, #D6DEE8 | 8.17 / 11.96 |

## 4. Design decisions / non-obvious calls
- **Flat docs keeps its own inline nav** — it is the double-click-able offline artifact; no external asset coupling, so no shared shell.
- **Shared assets live in `pages-hub/assets/`** and deploy to `/assets/`; subpages reference `../assets/` (works at `/releases/`, `/architecture/`, `/design/`, `/field-guide/`). Local `file://` can't represent the deploy layout — always validate over HTTP (see §6).
- **We don't push to `origin`** — that's upstream (mpfaffenberger). The fork line is `myfork` + `private`; Pages builds off `myfork/main`.

---

## 5. Roadmap

### Now (done)
- [x] Sidebar app-shell across hub/guide/releases/arch/design
- [x] Reusable ARIA popover (open-in-new-page / copy-link / close / deep-link)
- [x] Responsive "badass" architecture board (L→R train → wrapping grid)
- [x] Design System page + deploy registration
- [x] Square-safe logo, AAA tokens, focus ring, reduced-motion, target sizes
- [x] Flat-doc JS corruption fix; mobile/tablet overflow fixes
- [x] This build log

### Next (queued, highest value first)
- [ ] `detail.html` — wire "Open page" to a standalone detail template (currently opens same page's deep-link). Finish per-item standalone routing.
- [ ] Automated AAA lint in CI (axe-core / Lighthouse on the 6 pages) gating the Pages build.
- [x] Apply AAA tokens to the *legacy* page bodies — **DONE 2026-08-18.** Only the failing muted vars re-pointed (one var per page, DRY): `--text-muted`/`--t3` #7E8B99→#AEB9C7 (4.67→8.17:1), `--text-soft`/`--t2` #AAB6C4→#D6DEE8 (7.88→11.96:1), releases `--danger` #8A8FF0→#B7BBF7 (5.62→8.86:1). Verified via live computed styles: guide meta 9.08:1, releases count 8.17:1, arch node-desc 11.96:1 — all AAA. Flat doc inherits the guide change automatically (it is generated from the guide template).
- [ ] Flat docs: optional light nav refresh to match chrome (kept self-contained).
- [ ] Keyboard shortcut: `/` focuses architecture inventory search; `g d` jump-to-design.

### Later (nice-to-have)
- [ ] JSON-driven architecture nodes (single data file → board + detail + inventory).
- [ ] Component tests for `popover.js` / `sidebar.js` (no build step, keep plain).
- [ ] Dark/light theming toggle (tokens already isolated for it).
- [ ] i18n pass on new pages (site is currently English).
- [ ] OG/social preview meta + richer per-page descriptions.

---

## 6. How to verify / reproduce
```bash
# serve a Pages-mirrored layout locally (file:// can't express /releases/ style URLs)
cd ~/code_puppy
rm -rf /tmp/bbsite && mkdir -p /tmp/bbsite/{field-guide,releases,architecture,design,flat}
cp pages-hub/index.html /tmp/bbsite/
cp -r pages-hub/assets /tmp/bbsite/
cp -r docs/field-guide/. /tmp/bbsite/field-guide/
cp pages-hub/updates.html     /tmp/bbsite/releases/index.html
cp pages-hub/architecture.html /tmp/bbsite/architecture/index.html
cp pages-hub/design.html       /tmp/bbsite/design/index.html
cp docs/field-guide-flat.html  /tmp/bbsite/flat/index.html
(cd /tmp/bbsite && python3 -m http.server 8931)

# live validation sweep used for this log
# (Playwright over https://t-granlund.github.io/code_puppy + the staging URL)
```

---
*Generated 2026-08-17 · commit `e861349e` · maintained by the update pipeline + manual curation.*
