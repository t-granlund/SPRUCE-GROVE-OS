# MASTER-CLASS — The Self-Healing Grove

**A training guide for the lifecycle core of Spruce Grove OS: the breathing
self-update loop, the sovereignty pipeline, and the gates and judges that
keep it honest — rooted in the ethos, taught the way it should be taught.**

Audience: every agent and human who tends this system — including the next
you, six months from now, with no memory of why any of this exists.
Format: seven modules, ~90 minutes, every claim traceable to a source file.
Sources are cited inline; the full source map with fidelity notes is the
appendix.

---

## Module 0 — How to teach this (the 8am rule)

Before the content: the method. This guide is written the way the best
service training is written — the way you'd teach macOS at 8am to someone
older who has never used a trackpad. The rules below apply to every module
and to every conversation an agent has while tending this grove.

1. **Assume zero context, zero shame.** Never open with jargon. Open with
   the thing the learner already knows. (Everyone knows what it feels like
   when an app updates itself in the middle of your work. Start there.)
2. **One concept per breath.** One idea, one sentence, one pause. The loop
   diagram in Module 2 is *one* idea. The contracts are four ideas. Never
   two at once.
3. **Name the fear before the feature.** "Self-updating software" sounds
   like a trojan until someone says out loud: *it cannot break the session
   you're in.* Say that first. Fear named is fear halved.
4. **Celebrate the small win out loud.** The first time a learner reads a
   log line and correctly says "that's the observer, not the actor" — say
   "that's it, exactly." Genuine, specific, brief.
5. **The service-counter cadence** (the classic Apple steps, borrowed with
   respect): **Approach** warmly → **Probe** to understand their actual
   situation → **Present** the fix → **Listen** for what they heard →
   **End** well, leaving them more capable than you found them. Note what
   that is, in grove language: *leave everything better than you found it.*
6. **Troubleshooting is emotional work.** A user reading an error message
   is not reading text; they're reading a verdict on their day. The empathy
   tactics in Module 6 are not soft skills bolted on — they are the
   difference between a fix that lands and a fix that is half a fix.

> Teach-back rule for every module: the learner explains it back in their
> own words, to an imaginary eighth grader. If they can't, the teacher
> re-teaches — never re-tests.

---

## Module 1 — The root system: ethos as mechanism

**By the end you can:** trace any lifecycle mechanism back to the sentence
in `ETHOS.md` that demands it.

The grove's lifecycle design is not an engineering preference that happens
to have a slogan. It is the slogan, executed. `ETHOS.md` carries a section
called **"The grove tends itself"** — "leave everything better than you
found it," applied to the tool itself — and it fixes **three truths** that
hold the whole system honest:

| Ethos truth (ETHOS.md) | Mechanism it becomes | Where to see it |
|---|---|---|
| It verifies against the world before it acts (love truth for truth's sake) | PyPI JSON API is the source of truth for "latest"; fetch failure = observe-only, never act | `docs/SELF-UPDATE.md` — The loop |
| It reports every self-heal in plain words (no silent mutations) | Every actuation reports through the message bus, i18n'd across 3 locales | `docs/SELF-UPDATE.md` — pieces table |
| It can always be told to wait (consent survives autonomy) | `NO_AUTO_UPDATE=1`, `NO_VERSION_UPDATE=1` — opt-outs are first-class features | `docs/SELF-UPDATE.md` — Escape hatches |

Read that middle column bottom-up and you get the ethics of autonomy:
**consent, then honesty, then verification.** Read it top-down and you get
the engineering. Same table. That is the design language of this grove —
every rule is a value with a test attached.

Also load-bearing from `ETHOS.md`: *a living thing does not wait for a
keeper to feed it on schedule; it checks, it acts, it heals, and it says so
plainly while it does.* Three verbs — **checks, acts, heals** — are three
different subsystems (Modules 2, 3, 4). If you can say which verb a given
log line belongs to, you understand this machine.

---

## Module 2 — The breathing core: the self-update loop

**By the end you can:** draw the loop from memory and name the four
contracts that make it safe.

This is `docs/SELF-UPDATE.md` — the cleanest current-state document in the
repo, written the day the feature shipped. The loop, non-blocking, every
startup:

```
launch ─▶ daemon thread ─▶ GET pypi.org/pypi/spruce-grove/json
                        ─▶ compare (installed vs latest)
                        ├─ equal ──────▶ idle
                        └─ newer ──────▶ report status (message bus)
                                        └▶ uv tool upgrade spruce-grove
                                           ├─ exit 0 ─▶ "next launch starts
                                           │             on the new version"
                                           └─ failure ▶ warn + manual command
```

**The design question — and teach it exactly this way:** *how do you swap
the code of a running program without breaking it?*

**Answer: you don't.** You swap the *disk*, and let process boundaries do
the rest. A running session keeps its warm, resolved imports and executes
the version it started with, to the end of its life. The on-disk
environment is replaced atomically. The **next** process boots on the new
code. No restarts, no mid-session import mixing, startup never blocks.

The division of labor is deliberately boring:

| Piece | Role |
|---|---|
| `version_checker.py` | fetch + compare + status; decides *whether* to actuate |
| `self_update.py` | actuation only; guards + reporting; **never decides** |
| startup daemon thread | non-blocking, never joined — a hung network cannot hang a session |

Observer decides, actor acts, and neither can be talked into the other's
job. (Separation of concerns as care ethics: the thing with the power to
change your installation has no power to decide to.)

### The four contracts (the part that must never rot)

1. **`perform_self_update` never raises.** Every path returns and reports;
   the caller wraps it in a last-resort try/except anyway — defense in
   depth.
2. **Never actuate in tests.** `tests/conftest.py` sets `NO_AUTO_UPDATE=1`
   suite-wide. No test can ever mutate a real installation.
3. **Never actuate on source checkouts.** Actuation requires the `uv`
   binary *and* the package to live under `.../uv/tools/...`. Editable
   installs are sacred.
4. **Actuation is a subprocess with a 180s timeout**, never joined.

Contracts 2 and 3 are the 8am-rule turned into code: *the system never
surprises someone who didn't ask.*

### The two release-pipeline races (learned live, 2026-09-15)

`SELF-UPDATE.md` documents two failure modes observed the day this shipped:

- **Hollow releases** — the version-bump commit lands after the build, so
  1.0.37 can ship *with a feature's version number but without the
  feature*. Rule: before trusting a version number, check
  `git rev-list -n1 vX.Y.Z` against the change's commit.
- **CI as the guardrail** — a commit pairing a new test with an unfixed
  implementation fails its run and blocks publish; broken code cannot ride
  the conveyor, it just costs a queued run.

Lab question: *which of the four contracts would have caught a broken
updater at test time, and which catches it at run time?*

---

## Module 3 — The heartbeat: sovereignty and the daily pipeline

**By the end you can:** list what this machine actually owns, and run the
full self-healing pipeline by hand.

`SOVEREIGNTY.md` is the disaster-recovery brief: what you own, where it
mirrors, and how to stay self-sufficient if the upstream public repo ever
disappears. The ownership table: working source clone, public fork,
private insurance mirror, the installed uv tool, an offline wheel, and the
user profile (`~/.spruce_grove/` — plugins, agents, config, kennel memory).

The daily pipeline (runs **ad-hoc** via `/update now`; launchd is
deliberately paused — regressions cannot sneak in unattended):

```
snapshot ─▶ rebase on upstream ─▶ run tests ─▶ reinstall
        ─▶ regen field guide ─▶ push myfork + private
```

Read it as a lifecycle in miniature: **snapshot** (consent — nothing is
mutated un-archived), **rebase** (verify against the world), **tests**
(the gate), **reinstall** (the act), **regen + push** (report plainly).
Five verbs, same ethos table as Module 1.

**Staleness warning (say this out loud when teaching):** `SOVEREIGNTY.md`
predates the 1.0 rebrand — it still references `~/spruce_grove/` paths,
v0.0.768 versions, and the old update script name. The *architecture* it
describes is current; the *paths and numbers* are historical. Verify
against the working tree before quoting it as fact. (Love truth for truth's
sake — including about your own documentation.)

Disaster ladder, if the public repo vanishes: installed binary keeps
running → clone the private mirror → local-source reinstall → nuclear
offline fallback from `dist/` wheel. Nothing breaks immediately. That
sentence — *nothing breaks immediately* — is the whole deliverable.

---

## Module 4 — Gates and judges: how the grove says no

**By the end you can:** explain what a gate is, what a judge is, and why
an abstaining judge is scarier than a failing one.

**Gates** are the hook engine (`spruce_grove/hook_engine/`,
`docs/HOOKS.md`): event-driven checks — PreToolUse, PostToolUse,
SessionStart, Stop — with pattern matching, per-hook timeouts, and
**blocking capability**. The contract is three exit codes:

- `0` — allow
- `1` — **block** (exit code 1 vetoes the tool call; stderr becomes the
  reason)
- `2` — error feedback without blocking

A gate is a rule with a binary answer. *May this tool call proceed?* The
registry normalizes tool names across providers (Claude Code's `Bash` and
the grove's `agent_run_shell_command` are the same gate), so a rule written
once guards every provider.

**Judges** are the evaluation layer: model-backed verdicts on goal
completion (the wiggum goal-judge plugin). A judge votes PASS / FAIL /
**ABSTAIN**. And here is the load-bearing sentence from
`docs/judge-abstain-remediation.md`:

> Abstaining judges do not vote, so goal completion was undecidable and
> the loop remediated forever despite zero repo defects.

A gate that fails is loud. A judge that abstains is *silent* — the system
keeps working, politely, forever, on the wrong premise. That asymmetry is
Module 5.

---

## Module 5 — The war story lab: nine rounds, zero defects

**By the end you can:** run the full troubleshooting method on a live case
where the code was innocent.

This is the master-class case study, verbatim from
`docs/judge-abstain-remediation.md`. Teach it as a story, because it is
one.

### The symptom

Nine consecutive sprint re-verification rounds passed locally, with fresh
evidence (BUILD-LOG.md sections 11–20). Yet every evaluation cycle
returned the identical judge note: `ABSTAIN endpoint error
(UnexpectedModelBehavior): ... metadata.weight_versions Input should be a
valid string (input was a list)`. The loop remediated forever.

### The emotional read (before the technical one)

Nine rounds of "it still fails" reads, to a human, as *nine failures* —
even though every check passed. The first empathy move at the service
counter: **validate the frustration, then reframe the signal.** "You're
not crazy, and the work isn't broken — the referee can't vote. Those are
different problems, and we can prove which one we have." That reframing is
what turned nine rounds of despair into one afternoon of proof.

### The method (troubleshooting theory, five moves)

1. **Reproduce or don't trust.** The failure never reproduced in local
   dev — which is itself evidence: the trigger is *environmental*, not
   code.
2. **Isolate the variable.** The judge harness resolves its own
   pydantic-ai release; the repo pins 2.35.0. Same code, same payload,
   different environments.
3. **Prove it byte-exact.** Isolated uv environments per release built the
   version matrix: under 2.33.0 the stock model raises the byte-exact
   judge error; under the repo's 2.35.0 pin it passes untouched. The
   defect lived in the gap between environments.
4. **Fix minimal, scope tight.** `tolerant_openai.py` —
   `TolerantOpenAIChatModel` overrides the *documented*
   `_validate_completion` hook: strict validation first, one retry that
   JSON-encodes only non-string `metadata` values, and **unrelated
   ValidationErrors propagate unchanged** — no error masking. Wired only
   into the `custom_openai` branch (third-party OpenAI-compatible
   endpoints); first-party OpenAI stays strict. Blast radius, bounded.
5. **Gate the fix.** 9 passing tests (`tests/test_tolerant_openai.py`), a
   strict-env regression proof, and a written validation plan naming what
   the next `/goal` cycle must show: a non-ABSTAIN verdict, no
   `weight_versions` note, a decidable outcome.

### The gap register (the art of the open door)

The remediation doc ends with G1–G5 — each gap owned, statused, and given
a next action. G3 was a *ceremony* (resolving judge-model placeholders via
`/judges` — 4/4 PASS). G4 and G5 are deliberately left open with the
rationale written down: *extend only on observed failure, to keep blast
radius small.* Teach this: **an honest open gap beats a fake closed one.**
The register is the troubleshooting theory made permanent — symptom,
hypothesis, proof, fix, residual risk — in a form the next reader can act
on without re-deriving any of it.

Lab question: *the fix retries once on ValidationError. Why once? What
failure mode does an infinite retry invite, and which ethos truth does it
violate?*

---

## Module 6 — The human layer: empathetic service tactics

**By the end you can:** run a support conversation about a self-healing
system without making the human feel like the failure.

The lifecycle core exists so humans stop babysitting updates. That only
works if the conversation *about* it is as well-engineered as the code.
The tactics (service-counter method, grove dialect):

- **Validate before you verify.** "That would frustrate me too" is not
  filler; it lowers the temperature so the actual signal can be heard.
  (Nine rounds of ABSTAIN felt like failure; saying so out loud came
  *before* the version matrix.)
- **Name the mechanism in plain words.** Not "the daemon thread performs
  non-blocking actuation" — say: "the update happens beside your session,
  never inside it. What you're working on finishes on the version it
  started with; the next time you open the grove, it's current."
- **Show, don't assert.** Every claim in a support conversation should be
  one command away from evidence — a log line, a test name, a doc
  section. "NO_AUTO_UPDATE=1 opts out" lands harder as: "here's the line
  where the system honors your no."
- **The consent script.** Autonomy scares people. Lead with the opt-out:
  "It does this by itself, and you can tell it to wait — `NO_AUTO_UPDATE=1`
  — and it will wait, every startup, until you say otherwise." Consent
  first is both the ethos and the fastest trust-builder.
- **Leave them the ladder.** End every interaction with the next rung:
  the doc to open (`docs/SELF-UPDATE.md`), the command to pin a version
  (`uv tool install spruce-grove==X.Y.Z`), the gap register to read. A
  fix that leaves someone self-sufficient is the only complete fix.
- **Never blame the environment person-shaped.** The judge war story's
  root cause was a *dependency resolution* — nobody's fault. Say that.
  "The code was right, the referee's glasses were wrong" teaches more
  than a postmortem with names redacted ever will.

---

## Module 7 — Teach-backs and graduation

**By the end you can:** teach this system to someone else in 15 minutes,
from memory, with nothing but a whiteboard.

The graduation teach-back (all five, in plain words, 15 minutes):

1. Draw the breathing loop. Say where it can never block a session, and
   why.
2. Recite the four contracts. Explain which two protect *the user* and
   which two protect *the machine*.
3. Explain gates vs. judges, and why an ABSTAIN is scarier than a FAIL.
4. Walk the judge war story in five moves: reproduce, isolate, prove,
   fix minimal, gate.
5. Deliver the consent script and name the one env var that makes the
   system wait.

Passing standard: the eighth-grader in the room could follow it. The
graduation gift is the habit, not the certificate: **write the gap
register, cite the source, leave everything better than you found it.**

---

## Appendix — Source map (what to open, and how much to trust it)

| Artifact | Covers | Fidelity notes |
|---|---|---|
| `docs/SELF-UPDATE.md` | The breathing core: loop, session-safety model, 4 contracts, escape hatches, release-pipeline races | **Cleanest current-state doc**; written 2026-09-15, the day it shipped |
| `docs/judge-abstain-remediation.md` | Gates/judges war story: root cause, version matrix, fix, G1–G5 register, validation plan | Detailed and self-auditing; G2/G4/G5 rows are living — re-check before quoting status |
| `ETHOS.md` | The root system: "the grove tends itself," three truths, the creed | Stable; the why behind every mechanism |
| `SOVEREIGNTY.md` | Ownership map, daily pipeline, disaster ladder | **Architecture current, paths/versions stale** (pre-rebrand); verify against working tree |
| `spruce_grove/hook_engine/README.md` + `docs/HOOKS.md` | Gate mechanics: events, matchers, exit codes, blocking | Current |
| `BUILD-LOG.md` | The ladder: entries 1–29 plus the 5al.x remediation rounds | Append-only history; the receipts |
| `CHANGELOG.md` + `LIVING-UPDATES.md` | What shipped, and the dictation-era decisions behind it | Living; the observatory renders both |

The one-breath version, for the whiteboard:

> The grove checks itself, acts on the world only after verifying it,
> heals without breaking the session that noticed, and says so plainly —
> and it can always be told to wait. Together we are better. Always.
