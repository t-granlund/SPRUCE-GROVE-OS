# Why Apache-2.0 — the relicense, plainly

*Effective September 2026. Previously MIT, inherited from Code Puppy.*

This is the public rationale, so anyone — a contributor, a downstream user, a
co-maintainer, a lawyer — can see the reasoning without having to trust a
summary of it.

## Start with why

A grove is what you get when spruces grow together: no single tree carries the
forest, but the stand outlasts any one of them. The license should say the same
thing the mark does — this is a shared stand, maintained in the open, and no
one person's name is the point.

## What changed

- `LICENSE` — Apache-2.0, from MIT.
- `NOTICE` — the Grove's attribution plus the Code Puppy lineage. **The MIT
  notice is preserved verbatim**, because that is what MIT requires and because
  the puppy came first.
- `pyproject.toml`, the README badge, and the release notes — all updated.
- The desktop shell and the club site carry the same treatment.

Nothing about the *use* got friendlier-to-hoard. Every freedom MIT granted —
run it, read it, fork it, sell it, embed it — Apache-2.0 grants too. What it
adds are the two things a project steward actually needs as contributors and
users grow:

1. **An explicit patent grant** (§3). MIT is silent on patents, which leaves
   users quietly exposed. Apache-2.0 says the contributors' patents come along
   with the code.
2. **A stated trademark boundary** (§6). The license covers the *code*.
   The names and marks are governed separately, in `TRADEMARKS.md`. That
   separation is what lets the creed spread while the brand stays honest about
   who maintains it.

## The trade, honestly

Apache-2.0 is *more* permissive in patent terms and *more* explicit in
attribution terms — it asks that changes be noted and the NOTICE preserved.
For a project whose whole ethos is "leave it better than you found it, and show
your work," that is not a tax. It is the point. The receipts are part of the
product.

## Council stewardship and the anonymity policy

The repository is stewarded by a council, and the license keeps the granting
entity and the trademark contact *off* any individual: the public surfaces show
seats, not names. This is a deliberate policy, not an accident of drafting,
and it is why the `NOTICE` copyright line and the packaging metadata name a
stewardship rather than a person.

The one name that must stay is **Michael Pfaffenberger's**, as upstream author
of Code Puppy. That is required attribution, not a leak. Any audit that flags
him is wrong, and ours is written not to.

## For a co-maintainer considering the same move

If you forked a MIT project into something with a public story, a mark, and a
group of maintainers instead of one, the Apache-2.0 swap is usually the right
call — for the patent grant and for the trademark boundary, in that order.
Preserve the upstream notice verbatim, say thank you in the NOTICE as loudly as
you say it anywhere else, and write the rationale down where people can read
it. This file is that, for us.

---

See also: `NOTICE`, `TRADEMARKS.md`, `PROVENANCE.md`, `docs/LICENSE-ANALYSIS.md`
(the working analysis), and `GOVERNANCE.md`.
