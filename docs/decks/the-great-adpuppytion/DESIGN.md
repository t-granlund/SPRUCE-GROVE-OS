# DESIGN — The Great Adpuppytion DS v2 ("Cornerstone+")

Design system + layout architecture for the Code-Puppy University founding deck.
Supersedes the informal v1 conventions. Locked 2026-07-30.

## Architecture (prompt-addressable)

```
tokens.css      §1 brand primitives → §2 semantic → §3 role accents →
                §4 act map → §5 type families → §6 type scale →
                §7 space/geometry → §8 motion → §9 glow
components.json machine-readable registry + prompt_guide (natural-language
                edits map to a token or class; tests enforce sync)
theme.css       component layer — consumes tokens ONLY (no hardcoded values)
index.html      45 slides; every slide is exactly one archetype
tests/          42-test compliance suite (see STATE.md)
```

Natural-language edit examples: "make Act II sky" → `--act-2: var(--accent-builder)`
in tokens.css §4. "Bigger Chaplin text" → `--type-chaplin`. "Slower sine draw" →
`--motion-draw`. Nothing else needs touching.

## Principles (in priority order)

1. **Simple** — one idea per slide, ruthlessly. If a slide needs a fourth element,
   it's two slides.
2. **Informed** — every claim survives the FACTCHECK.md pass; attribution is part
   of the design, not footnote confetti.
3. **Captivating** — contrast of scale does the work: whisper slides and shout
   slides alternate. Nothing mid-volume.
4. **Wow** — at most ONE animated/live moment per act. Wow is scarcity (thanks,
   Karen X. Cheng).
5. **Show the medium** — this deck argues a new medium is being born. It must
   itself look like it was made *in* the new medium: live terminal, animated
   artifacts, agentic self-reference. Not a filmed play (the Méliès rule).

## The four archetypes

Every slide is EXACTLY ONE of these. No hybrid layouts.

### 1 · STATEMENT
The shout. Megaword act-breaks, the Chaplin beats, the closing.
- Canvas only: eyebrow + one typographic object. Nothing else.
- `min-height: 92vh`, vertically centered.
- Type: Space Grotesk 700, 3.2–4.5em, tracking -0.03em. Chaplin uses Source Serif 4.
- ONE accent color (the act color). No cards, no grids, no images.

### 2 · SPLIT
The whisper. Context + evidence: Gorky, Chaplin backstory, personas, consent.
- Two columns: prose left (max 3 short paragraphs), ONE artifact right
  (quote block OR image, never both).
- Artifact is borderless: a 1px accent rule + whitespace, not a card.
- Images: duotone-treated (ink + act accent), 40–50% column, subtle mask.
- Body text floor: 0.62em @30px base ≈ 19px. No 0.5em body text anywhere.

### 3 · STAGE
The artifact IS the slide. Timeline, sine wave, terminal, stat wall.
- Full-bleed (edge-to-edge inside 8% margins): the SVG/terminal/grid owns
  the canvas. Eyebrow + one-line caption only.
- The timeline is a horizontal STAGE band (year rail +事件 nodes), not four
  cards. The sine wave animates stroke-draw on slide entry.
- Terminal = the deck's meta-wow: types itself via auto-animate/JS, once.

### 4 · LEDGER
Structured data, used twice ONLY: the five-schools table, the three
charter commitments.
- Real table styling (puptable, upgraded): row hover, generous padding,
  0.66em floor, accent row-labels.
- Charter = three columns but ledger-flat: no borders, hairline rules,
  big numerals.

## Act → color discipline (navigation by hue)

| Act | Color | Token |
|-----|-------|-------|
| 0 Cold open | gold | `--accent-creator` |
| I 1895 | sky | `--accent-builder` |
| II Panic | coral | `--accent-alarm` |
| III Chaplin | gold (serif) | `--accent-creator` |
| IV Sine wave | mint | `--accent-hope` |
| V 2026 | coral→violet | alarm into weird |
| VI Humans win | violet | `--accent-weird` |
| VII CPU | gold | `--accent-creator` |
| VIII Ask | all four, sequenced | — |

Rule: within a slide, only the act color + neutral ink. The v1 sin
(five hues on one slide) is banned.

## Type scale (@ 30px Reveal base)

| Name | Size | Use |
|------|------|-----|
| mega | 3.4–4.5em | STATEMENT |
| h2 | 1.9em | SPLIT/STAGE headers |
| body | 0.85em | prose max |
| small | 0.66em | card/ledger floor |
| micro | 0.52em | eyebrows, attributions only |

## Assets (FPO now, licensed stills later)

- `assets/` dir. FPO pattern: `https://placehold.co/1200x800/0b0f14/f5b94d?text=...`
  wrapped in `.duo` (duotone: grayscale + mix-blend + act-color overlay).
- Targets: Méliès moon (Act I), Jazz Singer frame (II), Chaplin silhouette (III),
  Pomplamoose-era YouTube chrome (IV), slop/glitch texture (V), hot-dog fingers
  nod (VI), paw mark (VII–VIII).
- One image max per slide; SPLIT or STAGE only, never STATEMENT.

## Motion budget

- Reveal fade everywhere (current).
- Auto-animate pairs: title sequence, Chaplin beats, CPU reveal (existing).
- TWO custom moments, total: (1) sine-wave stroke-draw Act IV;
  (2) terminal self-type Act VII. Nothing else animates. Wow is scarcity.

## Fireship integration (dedicated beat — locked placement)

New Act V slide pair after "mass disruption" stats:

- **STAGE slide: "The moat is gone."** — big ledger: `Execution: $20/month`
  next to the 20K-musicians echo; copy: "Why pay $29/mo for your SaaS when a
  frontier model builds a better version in 20 minutes? The moat was coding
  itself." (Fireship, Code Report, Jul 29 2026)
- **SPLIT slide: "Asteroid → soil."** — "The ceiling has never been higher.
  The floor has never been more crowded." Left: indie-hacker extinction
  (Peter Levels era ends); right: what survives — distribution, branding,
  taste, proprietary data. Bridge line: "That's not a death notice.
  That's a course catalog." → hands off to Act VI/VII.

Persona line edit (Act VII, Technical): "Their moat is evaporating too" →
"The moat was coding itself. The moat is gone."

## QA protocol (unchanged)

Headless Playwright @1440×810, `/#/<n>`, 1100ms settle, screenshot every
slide; diff against archetype rules. The `.vcenter` specificity fix
(`.reveal .slides section.vcenter`, min-height 92vh) is load-bearing —
keep it.
