# VALIDATION-LADDER — the three validations that prove the grove

> Dictated 2026-09-16; the master plan behind the next phase. Companion to
> `SOVEREIGNTY.md` (infrastructure), `docs/DEPENDENCY-EXIT.md` (the census),
> and the family-lab wedge (private, local-only — never in this repo).

---

## 1. The desktop OS — onboarding as the product

The CLI is grown; the **desktop OS implementation** is the validation that
turns a tool into a home. Every person who downloads the grove should walk a
full onboarding that adapts to **who they are and why they came**:

- **Persona-driven first run:** the onboarding wizard asks use-case questions
  and configures the grove to fit — the builder, the small-business owner,
  the tinkerer, the curious kid (with a guardian). Persona decides: default
  agents, plugin set, voice on/off, telemetry posture, model tier.
- **Subscription onboarding, seamless:** the path from download to a working
  synthetic-model subscription should be one flow — credential entry, model
  selection, a cost ceiling, and a first successful run inside five minutes.
- **Optimized from minute one:** the onboarding should tune token economy and
  context utilization per persona — model tier, context window policy,
  compaction aggressiveness, tool allowlists. The grove should feel fast and
  cheap because it was *configured* to be, not lucky.

Landed already: the onboarding wizard skeleton, `/add_model`, keyring
credentials, cohort plugins. The ladder: persona survey -> tuned defaults ->
subscription flow -> a measured "time-to-first-successful-run" metric.

## 2. The traceability program — every button has a receipt

A test suite that matches the surface, not just the functions:

- **Traceability matrices** mapping every feature, button, command, flag,
  history/view-queue behavior, and optimization to: the test that proves it,
  the build-log entry that birthed it, and the observatory narrative that
  explains it. If a thing exists and has no row, that is a bug in the matrix.
- Generated, not hand-kept: matrices computed from the command registry,
  tool registry, and hook registry (the same "counts are computed" rule the
  dashboard lives by).
- Usability passes ride on top: scripted user journeys per persona, run
  against the real TUI (the pexpect harness already exists for this).

## 3. The living directory — a repo as an organism

Opening an existing directory should load it as a **living system**, not a
file listing:

- **Pulses:** what changed here recently, what's hot (git + mtime + test
  activity), rendered as a heartbeat, not a tree.
- **Hooks:** the project's own extension points discovered and surfaced
  (`.spruce_grove/`, plugins, CI, make/test entry points).
- **Telemetry & audit:** every agent action against the directory lands in
  the audit log — what happened, how, why (which prompt/run), with the
  observatory treatment for humans.
- All voice-driven through **mockingbird** and the cohort plugins; the
  directory view is where small-business users (a locksmith's job folder, a
  gym's season plan) will live, so it must feel like walking into a place,
  not opening a drawer.

---

**The rule the ladder inherits from the sovereignty work:** every rung ships
with its receipt — a test, a metric, or a matrix row — never a claim.
