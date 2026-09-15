# GOVERNANCE — The Leather Apron Council & The Approval Wall

How Spruce Grove OS is steered, who decides, and what must be true before
anything ships. The stewards serve anonymously on every public surface —
this project is about the ethos and the work, never about persons or
companies.

---

## The Council

Spruce Grove OS is stewarded by a small council operating in the Leather
Apron tradition — Benjamin Franklin's Junto: a mutual-improvement circle
where decisions start as questions, survive inquiry, and earn their way
into the build. The council is currently **three stewards**. Public
surfaces never name them; the work carries no personal brand.

### How a decision begins

1. **Raise it in council.** Anything worth changing starts as a spoken or
   written question in a council session — same as the dictation ledger:
   real conversation, captured.
2. **Inquiry before opinion.** The Junto rule: understand before judging.
   What exists today? What is it doing for someone right now? What breaks
   if it changes?
3. **Prototype or proposal.** Small proofs beat long debates. A diff, a
   spike, a one-page plan.
4. **The Gate.** Every proposal — ours or upstream's — faces the five
   criteria: *tried & true, secure, honest, grove-fit, counsel sign-off.*
   Manic, insecure, or risky does not pass. No exceptions for shiny.
5. **The Wall.** Approved work queues for release. Published releases
   carry the council's marks (see The Approval Wall).

### Decision rules

| Decision | Threshold |
|---|---|
| Regular feature/fix lands on the release train | **2 of 3 stewards** approve the change |
| Anything touching the Gate surfaces (auth, secrets, tool permissions, the self-updater, the connector) | **3 of 3** — unanimous |
| Removing or recreating a compatibility contract | **3 of 3**, with a written exit plan |
| Infrastructure (where the repos live, domains, CI) | **3 of 3**, plus a rollback plan |
| Emergency security fix | Any **1** steward may ship a hotfix; full council ratifies within 72 hours |

## The Approval Wall

No release reaches the public train without passing the wall:

- The release workflow runs inside a **protected environment** that
  requires named steward review before it can execute.
- Merges to the release branch require council review
  (see `CODEOWNERS`).
- Every published release is recorded on the Release Observatory with its
  provenance chips and gate state — the receipts are public.
- A release that later fails the Gate's judgment is rolled back and the
  rollback is itself published. Honesty survives mistakes; silence
  doesn't.

## The contributor path

1. **Learn the harness.** Desktop and CLI, hands-on — build something for
   yourself with it first.
2. **Work in the open.** Fork, propose, land small things through normal
   review.
3. **Steward invitation.** Contributors the council has worked with are
   invited into review rotation, then into the council itself as seats
   open. The council stays small on purpose; the rotation keeps it honest.
4. **Stewards serve anonymously** on all public surfaces. Contributions
   are judged by the work.

## The connector rule

The upstream line (see the observatory's Upstream Connector and
`PROVENANCE.md`) stays open — it is free leverage and a standing
obligation to learn from what came before. But **nothing auto-merges**:
every signal arrives wearing *awaiting counsel*, and the gate is the only
door.

## What this governance is not

- It is not a corporation, a foundation, or a product board.
- It optimizes for the individual builder — the associate inside the
  walls, the small business, the person with the problem and the voice to
  describe it.
- It will never name persons or companies on public surfaces. The work
  speaks.
