# STATE — pick up here

**Last saved:** 2026-07-30 (evening) by code-puppy-8aaf0e
**Status:** v2.1 — DS "Cornerstone+" refactored into token/component architecture,
42-test compliance suite green, headless QA re-verified post-refactor.

## How to resume

```bash
cd /Users/tygranlund/code_puppy/docs/decks/the-great-adpuppytion
python3 -m http.server 8084   # then open http://localhost:8084/
```

## Docs map

- `DESIGN.md` — DS v2 spec: four archetypes (STATEMENT/SPLIT/STAGE/LEDGER),
  act→color discipline, type scale, motion budget, asset pipeline. **Read first
  before editing slides.**
- `components.json` — machine-readable DS registry. Natural-language prompts
  map to tokens/classes via its `prompt_guide`. Keep in sync with deck edits
  (test_registry.py enforces).
- `FACTCHECK.md` — web-puppy verified claims table; corrections applied.
- `tokens.css` — SINGLE SOURCE OF TRUTH for every color/size/motion value.
  Prompt-driven edits land here (e.g. "recolor Act II" → edit `--act-2`).
- `theme.css` — component layer. Consumes tokens only; zero hardcoded hex
  (test_tokens.py enforces).
- `README.md` — structure + provenance.
- `index.html` — all 45 slides, 8 acts.
- `tests/` — 42-test compliance suite. Run: `/opt/homebrew/bin/pytest tests/ -q`

## Hard requirements (do not break)

1. **Chaplin's Great Dictator speech = verbatim, one beat per slide, 8 slides**
   (eyebrow I–VIII, slides 13–20). Text exactly from `docs/jack-conte-sxsw.md`.
   Bookended on slide 44.
2. Code-Puppy brand tokens (gold #f5b94d / sky #6cb6ff / mint #4cc46a /
   violet #b692f6 / coral #ff7b72 on ink #0b0f14). One accent hue per act/slide
   (`.act-*` scoping) — the v1 five-hues-per-slide sin is banned.
3. Archetype discipline: every slide is STATEMENT, SPLIT, STAGE, or LEDGER.
   Cards/tables ONLY in LEDGER. Images ONLY in SPLIT/STAGE (`.duo` duotone).
4. Motion budget: exactly two animated moments — sine stroke-draw (slide 23)
   and terminal type-in (slide 40). Wow is scarcity.

## Narrative arc (locked, v2)

Cold open → 1895 film (Méliès) → panic rail (1896/1927/1942/1969) → Chaplin
refusal + speech → sine wave (Pomplamoose) → 2026 dip (slop + consent +
**Fireship: the moat is gone / asteroid→soil, slides 29–30**) → why humans win
(risk/scarcity/connection) → **CPU answer (Act VII)** → charter + ask.

## CPU framing (locked concept)

Two halves of one future: creative-non-technical + technical-non-creative.
Stack: **Puppy OS** (front door) → **Code-Puppy** (engine, real, MIT) →
**University** (bridge; this deck is its charter).
5 schools: New Medium / Agentic Craft for Creatives / Creative Direction for
Engineers / The Rebuild Practice / Ethics, Consent & Credit.

## Test suite (tests/ — 42 tests, all green)

| Module | Guards |
|--------|--------|
| `test_structure.py` | 45-slide count, registry coverage, archetype legality (no tables outside LEDGER, images only in SPLIT/STAGE with .duo), single-hue rule with sanctioned exceptions, motion budget = exactly 2 |
| `test_chaplin.py` | Speech verbatim vs transcript (word-level), one beat per slide, I–VIII eyebrows, slide-44 bookend, serif treatment |
| `test_content.py` | Fact-check locks (1942 Petrillo, Moog-not-Novachord, ~20K, 1992 Wolf, Flanagan, Karen X. Cheng), Fireship beat + attribution, CPU framing phrases, act markers |
| `test_tokens.py` | Brand palette exact hex, semantic→primitive wiring, act map completeness, zero hardcoded hex in theme.css, type floors (0.52em micro), WCAG contrast ≥4.5 body / ≥3.0 accents+muted |
| `test_registry.py` | components.json schema, 4 archetypes, component categories, registry↔deck consistency, per-slide act classes (slide_classes map), motion slots = 2 |

## QA tooling

Playwright at /tmp/pwqa (ephemeral — `npm i playwright@1.62.0` to reinstall):

```js
// shoot.js — all 45 slides @1440×810, 1100ms settle
// reshoot.js — slides 23 & 40 (animations need 3.2s / 6s settle)
// audit.js — overflow sweep (note: full-width block elements are false
//            positives; only text ending past x≈1415 is a real clip)
```

v2 QA findings fixed: sine SVG label overlap (labels repositioned to top/bottom
rows), terminal animation fill-mode (`both`), 2020+ label clip (x=960).

## Open ideas (not yet done)

- Real licensed stills to replace placehold.co FPOs (Méliès moon is the only
  FPO placed so far — slide 5)
- PDF export (`?print-pdf` + decktape) for a shareable artifact
- Light-mode fork for projector-hostile rooms
- Speaker notes (`<aside class="notes">`) for live delivery
- The Karen X. Cheng quote is only sourced via Conte's talk — fine as
  attributed, but a primary link would be better
