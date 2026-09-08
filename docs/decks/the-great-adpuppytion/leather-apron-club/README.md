# The Leather Apron Club — Bentonville 2026

The founding presentation for the first meeting of the Leather Apron Club:
**Friday, September 11, 2026 · Bentonville Barber Company.**

A full visual reimagining of `the-great-adpuppytion` ("Cornerstone+") deck,
re-skinned onto the **Spruce Grove design system** (granlund-grove Nordic
forest dark tokens, Fraunces / Inter / JetBrains Mono) and re-anchored on
Benjamin Franklin's Junto (1727), documented in
`dev/1.MASTER-ORCHESTRATION/Junto-Leather Apron Club.md` and `ETHOS.md`.

## Run it

```bash
cd docs/decks/the-great-adpuppytion/leather-apron-club
python3 -m http.server 8085
# open http://localhost:8085/
```

Reveal.js + fonts load from CDN (same as the parent deck). Presenting offline?
Open with the machine's browser after a warm-up load (fonts cache).

## Structure (33 slides, 6 acts, ~25–30 min with the Chaplin read)

| Act | Slides | What happens |
|-----|--------|--------------|
| 0 · Cold open | 1–2   | Tree-mark stroke-draw (motion slot 1), "What did you build this week?" |
| I · 1727      | 3–8   | The Junto: 4 admission inquiries (verbatim), what 12 tradesmen built, the anti-disputation rule |
| II · Machines | 9–11  | The panic rail (1896/1927/1942/1969), the 2026 moat-is-gone beat |
| III · 1940    | 12–21 | Chaplin's Great Dictator speech — **verbatim, 8 beats**, set in Fraunces |
| IV · Proof    | 22–25 | Why the circle wins; the Sept 3 receipts ledger (tylergranlund.com/progress) |
| V · The club  | 26–30 | Operating code, the pipeline, the self-typing charter terminal (motion slot 2), seed experiments |
| VI · The ask  | 31–33 | Three commitments, the creed, TOGETHER WE ARE BETTER. ALWAYS. |

## Design discipline (inherited, non-negotiable)

1. **Four archetypes only** — STATEMENT / SPLIT / STAGE / LEDGER. Cards and
   tables live in LEDGER. Images were dropped entirely: the deck is pure
   typography, rails, and artifacts (the spruce grove identity needs no FPO).
2. **One accent hue per slide** via `.act-*` scoping; act map in `tokens.css` §4.
3. **Motion budget = 2, total**: tree-mark stroke-draw on the title;
   terminal self-type in Act V. Wow is scarcity.
4. **Chaplin is verbatim** (slides 13–20, I–VIII eyebrows), sourced from
   `docs/jack-conte-sxsw.md` exactly as the parent deck's test suite locks it.
5. **Every fact has a file** — Junto mechanics (`Junto-Leather Apron Club.md`),
   receipts (`granlund-grove/src/routes/progress.tsx`), creed (`ETHOS.md`,
   Ozark Bagels transcript), Fireship beat (Code Report, Jul 29 2026).

## Tokens

Spruce grove oklch palette in `tokens.css`: night canvas 0.18·150,
cedar (founder gold) 0.78·55, grove 0.72·155, frost 0.80·210, ember 0.72·40.
Matches `granlund-grove/src/styles.css` and the OPERATION GRANLUND dashboard —
one design system across site, dashboard, and deck.

## Open to-dos before Friday

- Confirm venue specifics, timing, and invite list with **Victor & Drew** (this week).
- Printable one-pager: the four admission inquiries (hand everyone standing).
- Speaker notes pass (`<aside class="notes">`), 1 rehearsal at full pace.
