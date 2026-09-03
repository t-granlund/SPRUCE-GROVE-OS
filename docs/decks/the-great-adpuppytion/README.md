# The Great Adpuppytion — Code-Puppy University deck

A Reveal.js presentation built on Jack Conte's SXSW 2026 talk ("a talk about change"),
extended into the founding charter for **Code-Puppy University**.

## Run it

```bash
cd docs/decks/the-great-adpuppytion
python3 -m http.server 8084
# open http://localhost:8084/
```

Or just open `index.html` directly — Reveal, fonts, and theme all load from CDN/local.

## Structure (45 slides, 8 acts) — DS v2 "Cornerstone+"

| Act | Slides | What happens |
|-----|--------|--------------|
| 0 · Cold open | 1–2 | Title + "who here has felt it?" audience hook |
| I · 1895 | 3–6 | Lumière brothers, Gorky quote, Méliès' cut (FPO still), "not a play" |
| II · The Panic Pattern | 7–9 | Panic rail: 1896 film / 1927 Vitaphone / 1942 Petrillo ban / 1969 Moog ban; fear vs. art |
| III · Chaplin | 10–21 | 13 years of refusal → The Great Dictator speech, **verbatim, one beat per slide (I–VIII)** |
| IV · The Sine Wave | 22–25 | Pomplamoose rebuild cycles; animated stroke-draw SVG wave; "change is not death" |
| V · 2026 | 26–31 | Slop phase, consent/theft, stat wall, **Fireship beat: the moat is gone + asteroid→soil**, permission to feel conflicted |
| VI · Why humans win | 32–34 | Risk / Scarcity / Connection pillars; the 1959 thought experiment |
| VII · The Answer | 35–41 | **Code-Puppy University** — thesis, two personas, the stack (Puppy OS / Code-Puppy / University), founding curriculum (5 schools), self-typing terminal, who it's for |
| VIII · The Ask | 42–45 | Three charter commitments (ledger), Chaplin bookend, thank-you |

Design system: see `DESIGN.md` (four archetypes, act-color discipline, motion budget).
Fact audit: see `FACTCHECK.md` (verified 2026-07-30; v2 text reflects corrections).

## The Chaplin requirement

The Great Dictator final speech appears **verbatim, one beat per slide**, slides 13–20
(numbered I of VIII → VIII of VIII in the eyebrow). Text is set in Source Serif 4 with
gold emphasis beats. Do not paraphrase, truncate, or split differently without sign-off —
this was an explicit, non-negotiable requirement.

## Design tokens (Code-Puppy brand)

Extracted from `docs/field-guide/index.html` CSS variables (the code_puppy field guide):

| Token | Hex | Used for |
|-------|-----|----------|
| `--bg` | `#0b0f14` | canvas |
| `--bg-card` | `#151e28` | cards |
| `--text` | `#e8eef4` | primary ink |
| `--text-soft` | `#9fb0c3` | body |
| `--accent` | `#f5b94d` | gold — creator / brand primary |
| `--accent-2` | `#6cb6ff` | sky — technical / builder |
| `--accent-3` | `#4cc46a` | mint — hope / recovery |
| `--accent-4` | `#b692f6` | violet — creative / weird |
| `--danger` | `#ff7b72` | coral — alarm / disruption |

Type: Space Grotesk (display), Inter (body), JetBrains Mono (eyebrows/labels/terminal),
Source Serif 4 (quotes + Chaplin). Dark mode with luminous accents, per slide-puppy
"Cornerstone" DS conventions (one idea per slide, 8% margins, auto-animate pairs).

## Provenance

- Source transcript: `docs/jack-conte-sxsw.md` (Jack Conte, SXSW 2026). All Conte
  pull-quotes are verbatim from the transcript.
- Chaplin speech text: as delivered in the transcript; trimmed only for stage delivery
  in the original film (this deck uses the transcript's wording exactly).
- Code-Puppy facts: the tool is real and open-source — github.com/mpfaffenberger/code_puppy (MIT).
- Code-Puppy University and Puppy OS are presented as founding concepts — this deck is
  intentionally their charter document. No prior CPU artifacts existed on disk as of
  2026-07-28 (full-machine search performed).
- Historical anchors (Lumière 1895, Gorky 1896, Méliès 1902, Jazz Singer 1927, ~20K
  theater musicians, Petrillo recording ban 1942–44, Moog union ban late 1960s, Baumol
  cost disease, 1992 ASOL/Wolf report, Flanagan 2012) — corrected vs. Conte's compressed
  telling; see FACTCHECK.md.
- Fireship beat (slides 29–30): The Code Report, July 29 2026 — "the moat was coding
  itself"; execution at $20/month; asteroid → soil (distribution, branding, taste).

## Slide-puppy notes

Design system: DS v2 "Cornerstone+" (DESIGN.md), Code-Puppy brand binding.
Reveal.js 5.1.0 via CDN. Auto-animate pairs on title/Chaplin/reveal sequences.
Two sanctioned animations: sine stroke-draw (Act IV), terminal type-in (Act VII).
