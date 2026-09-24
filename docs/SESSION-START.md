# Starting a session

A short, name-free entry point. It replaces the old `SESSION-HANDOFF.md`,
which was a private working document that should never have been tracked in a
public repo (see `docs/ANONYMITY-EXIT.md`, item D).

## Do this first

1. **Read the board:** `docs/SOVEREIGNTY-EXECUTION.md` — the current
   priorities and where the work stands.
2. **Find the work:** `bd ready` lists unblocked items; `bd list` shows the
   whole tracker. Beads are the project's durable task store and live outside
   the repo, so they are the right home for operational detail.
3. **Know the rules:** `ETHOS.md` (the creed), `AGENTS.md` (how contributors
   work), `GOVERNANCE.md` (how changes are approved).

## Where operational detail lives now

Working notes — accounts, machine state, launch prompts, breakage narratives —
belong in one of:

- **beads** (`bd create`, `bd remember`) — durable, queryable, not published
  with the repo;
- **`~/.spruce_grove/handoff/`** — a local directory for session handoffs,
  gitignored so a private note cannot become a public one.

If you are an agent reading this: prefer the board and the tracker over any
single long document. Prose handoffs go stale; `bd ready` does not.

## Why there is no `SESSION-HANDOFF.md` here

It was tracked, and it named people and infrastructure. The pivot policy is
*public surfaces show seats, not names*, and a session handoff is not a public
surface at all — it is a working note. Both problems are fixed by keeping it
local. The content was preserved; it simply is not published.
