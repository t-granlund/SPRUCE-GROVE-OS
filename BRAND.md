# BRAND — Spruce Grove OS

Visual and verbal identity, shared with the granlund-grove design system
(tylergranlund.com). Dark-first. Nordic forest. No glitter, just grain.

## The design language — GRAN

Dark-forest punk with Scandinavian discipline. Immersive, rebellious, clean —
in that order, held together by contrast. Every surface inherits these rules;
nothing improvises.

1. **The canvas is never flat black.** Near-black forest base, always carrying
   two radials: moss glow high, ember warmth low-corner. Depth before content.
2. **Grain on everything dark.** A fixed SVG-noise veil at 3–6% opacity over
   every immersive surface — the xerox soul, executed modern. No glitter.
3. **Four type voices, no more:**
   - **Fraunces** — the monumental statement (heroes, megawords)
   - **IM Fell English SC** — the 1727 council voice (club pages, ceremony)
   - **JetBrains Mono**, uppercase, wide-tracked — the machine voice
     (kickers, stamps, captions, data)
   - **EB Garamond** — long-form reading (stories, guides)
4. **Three symbols only:** the spruce-trio mark, the North Star, and the
   algiz rune (drawn as SVG strokes — protection, the raised branch, "leave
   everything better"). No emoji. Ever.
5. **The stamp** — punk's rubber stamp: mono uppercase, double-offset border,
   rotated −2° to −4°, cedar or ember ink. One per view, on the line that must
   not be missed. If everything is stamped, nothing is.
6. **The rune line** — section divider: hairline, algiz glyph centered, 40%
   opacity. Restraint is the rebellion.
7. **Opposition is the punk:** monumental serif against machine mono; warm
   cedar against cold frost; 7rem statements against 12.5px whispers. Soft
   gradients are atmosphere; edges are edges.
8. **Motion is scarce:** glow, fade, the Chaplin ignition. Nothing bounces.
9. **The era-ghost** — a corner watermark on every immersive page. The room
   should always know what century it is standing in.

## Wordmark

`gran·lund · sv. · spruce grove`

Name derivation, per truth-for-truth's-sake: "granlund" maps to "spruce
grove" in Swedish. Say that, nothing fancier.

## Color tokens (source of truth: granlund-grove `src/styles.css`)

| Token | OKLCH | Role |
|---|---|---|
| charcoal | `oklch(0.18 0.012 150)` | base background |
| spruce-deep | `oklch(0.22 0.03 158)` | deep brand layer |
| spruce | `oklch(0.32 0.045 158)` | primary brand |
| moss | `oklch(0.45 0.06 155)` | accent green |
| cedar | `oklch(0.78 0.12 55)` | warm accent, persona markers |
| bark | `oklch(0.32 0.025 60)` | earthy neutral |
| stone | `oklch(0.85 0.012 90)` | soft UI text |
| mist | `oklch(0.94 0.008 100)` | foreground/typography |

Terminal splash truecolor mapping: halo `#2D4F3A` (45/79/58) -> glow
`#588F5E` (88/143/94) -> cedar core `#D2A069` (210/160/105), mist crest
`#F0E1C8` (240/225/200). ANSI fallback: 32 -> 92 -> 93.

## Typography

- **Fraunces** (variable) — display wordmarks
- **Inter** — body
- **JetBrains Mono** — code, CLI output

## Voice

- Plain-spoken, warm, a little playful. First to say hello.
- Candid, never roasty. Tough minded, tender hearted.
- Zero invented facts; "NOT VERIFIED" beats a confident guess.
- Closers that fit the grove: "leave it better than we found it",
  "together we are better, always", (when earned) "joy, love, and cream cheese".

## Imagery roadmap

- [ ] Sprite/wordmark logo: spruce cone + canopy mark (vector)
- [ ] Replace `logos/spruce_grove_logo_noback.png` and field-guide/pages-hub assets
- [ ] TUI splash accent color: cedar on spruce-deep
