# BRAND — Spruce Grove OS

Visual and verbal identity. Dark-first. Nordic forest. No glitter, just
grain.

Public surfaces show seats, not names: this document describes the design
system by what it *is*, not by whose family it came from. The heritage is
told as etymology and ethos, never as a personal brand.

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

`spruce · grove · os`

### Start with why — the name and the mark

A grove is what you get when spruces grow together: no single tree carries
the forest, but the stand outlasts any one of them. That is the whole thesis.

The name has Scandinavian roots: *gran* is spruce, *lund* is grove — so the
word we build under literally means **spruce grove**. We say that plainly,
nothing fancier. The visual language follows from it: Nordic, dark-first,
grain over glitter, a forest (not a tree) as the mark, and a single ground
line the way a stand shares one forest floor.

Everything else — the council, the Leather Apron ethos, the receipts in
public — is downstream of that one belief: **together we are better,
always.**

## The logo pack — one geometry, four jobs

Source of truth for the glyph: `logos/spruce-core-disc.svg` — stepped
canopy, trunk notch, rounded joins, one shared ground line. Every file in
the pack is that one geometry, composed and dressed per job. Masters live
in `logos/`; site-chrome copies in `pages-hub/assets/`, kept identical by
`scripts/sync-brand-assets.sh` (run `--check` to prove it).

| Piece | Files | Job |
|---|---|---|
| **The Core Disc** | `logos/spruce-core-disc.svg` · `-512.png` · `-256.png` | The statement piece that stands on its own — stickers, laptops, app icons, favicons. Cedar gradient roundel, inset keyline, trio inset: deep-forest sides, mist center (the light-bringer), ink ground line. |
| **The Grove Mark** | `logos/spruce-grove-mark.svg` (dark surfaces) · `spruce-grove-mark-on-light.svg` | The application logo — nav chrome, sidebars, docs. Stone sides recessed, gold center, one ground line. |
| **The Ghost** | `logos/spruce-grove-ghost.svg` | Watermarks, era-ghosts, print line art. Pure strokes, no fill; presenting surfaces dim it with CSS opacity. |
| **The Lockups** | `logos/spruce-grove-lockup-horizontal.svg` · `-stacked.svg` | Website headers, READMEs, decks. Mark + Fraunces wordmark (Georgia fallback) + mono motto line. |

Favicon/app-icon duties ride the Disc: `pages-hub/assets/favicon-64.png`
(64px) and `apple-touch-icon.png` (180px) are Disc renders.

Legacy (kept for old embeds, not for new work): `spruce_grove_official.*`,
`spruce_grove_badge_*`, `spruce_grove_logo_noback.png`.

Rules that carry forward: geometry is the identity — never decorate it;
one ground line; the center tree is the light-bringer; below 20px only the
Disc survives.

## Color tokens (source of truth: `pages-hub/assets/tokens.css`)

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

- [x] Sprite/wordmark logo: Ghost Grove (three trees, golden center, one ground line)
- [x] Retired the pre-Grove placeholder marks (noback/withback/mark/north) — superseded by the official grove
- [ ] TUI splash accent color: cedar on spruce-deep
