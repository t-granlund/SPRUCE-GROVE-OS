# DECISION LAYER — a plan for System One-style bounded decisions in the grove

> **STATUS: DRAFT — for council review.** This plan adopts a *decision layer*
> alongside the grove's generation layer: instead of asking a model to produce
> text and parsing an answer out of it, we ask for a **bounded decision with a
> confidence and a reason**, and we record it. It is the natural home for the
> "why local / sovereign" argument the room already runs on.
>
> Origin: the Emerging Technology Breakfast Club's *Signal // Tuesday*, Issue
> #15 (Frontier Pulse, 09·15) — **Jev** (TypeSafe "System One", closed paid
> API) and **Laya** (Apache-2.0, 421M params, open weights). Both target one
> job: *return a bounded decision with a usable confidence measure.* This plan
> takes that job seriously without overclaiming the two projects.

---

## 0. What "System One" actually means here

Not Kahneman, and not a vendor slogan. Operationally, a **System One model** is:

- **Input:** a state + one or more **typed questions**.
- **Output:** a **structured choice / score / probability** — *not* generated text.
- **Use:** routing, classification, scoring, and guardrail decisions inside software.

The distinction that matters to us:

| | generation layer (today) | decision layer (this plan) |
|---|---|---|
| ask | "what should I say?" | "which of these, and how sure?" |
| output | free text (parsed) | typed value + confidence |
| cost | prompt + long completion | a short bounded call |
| failure mode | plausible text, no calibration | a wrong label — **so it must be logged and audited** |

The grove already makes thousands of these calls implicitly (is this a steer?
does this need review? which tool? which model?). Today those ride a language
model and a prompt. A decision layer makes them explicit, cheaper, and — this
is the point — **receiptable**.

## 1. Why now (and the honest caveats)

- The club's recurring **`Sovereign AI`** desk is exactly this fork: a closed
  API on someone's rails vs open weights you host. Jev and Laya are the freshest
  concrete example, in one decision layer.
- **Do not present this as a benchmark.** The Issue itself flags Laya's
  comparison tables as **unverified** (different prompts, Jev's own published
  figures). Vendor numbers (70–500 ms, ~$0.042/M input) are **vendor figures**.
- The Issue's own warning is our design brief: *"the hard part arrives after
  release, when outputs meet real failures, escalation paths, and someone
  accountable for the threshold."* That is a **containment + receipts** problem,
  and it is the grove's home turf.

## 2. Where it lands (existing seams — no new spine)

The grove already has the joints this bolts onto:

- `spruce_grove/model_factory.py` / `model_switching.py` — provider + model
  selection. The decision layer is a **second kind of call**, not a second app.
- `spruce_grove/agents/agent_model_judge.py` — already a decision-ish seam
  (judging). The first adapter belongs here.
- `spruce_grove/private_inference.py`, `kennel_provider.py` — the **local**
  lane already exists in embryo.
- `spruce_grove/agents/_history.py` — every part is hashed and recorded; the
  decision layer's outputs must ride the same receipt discipline.
- The desktop shell's **inspector → project / diagnostics** panes (this repo's
  sibling) are where a human reads decisions back.

**Non-goal:** replacing the generation layer. The decision layer is for
*bounded, repeating* calls. Anything needing prose stays on the model.

## 3. Two lanes, one interface

Define one trait; implement it twice:

```text
DecisionRequest  { state, questions[], allowed[] , max_ms? }
DecisionResponse { choice, confidence: 0..1, rationale?, source, latency_ms, cost? }

trait DecisionLayer:
    fn decide(req) -> DecisionResponse
```

- **Lane C — cloud (Jev-class):** a thin HTTP adapter to a System One API.
  Fast, cheap, closed. Behind a provider config key, off by default.
- **Lane L — local (Laya-class / grove-owned):** a local runner for small
  decision models (ONNX/GGUF), or the existing local provider. Sovereign, no
  outside party can switch it off. **Preferred default for the grove's ethos.**

Selection follows the existing model-preference machinery: a `decision` model
per persona/config, with a **local-first fallback**.

## 4. Containment + receipts (the part the room cares about)

Every decision is a **receipt**, and receipts are the desktop's `qp4` ledger:

1. **Log every decision** — input digest, chosen value, confidence, lane,
   latency, and the **threshold** used.
2. **Name the threshold owner.** A decision with no accountable owner is a bug,
   not a feature. Config carries `owner` + `escalation` for each decision class.
3. **Escalate on low confidence.** Below threshold → hand to the generation
   layer or a human, and *record the hand-off*.
4. **Replayable.** Deterministic given (`digest`, model version, threshold) —
   the same discipline as `fixtures/acp/session.jsonl` for the ACP dialect.

This is the same "floor" the desktop pins with `csp_guard` / `cap_guard`, applied
to *decisions* instead of *config*.

## 5. Phased plan

- **Phase 0 — decide (this doc).** Council sign-off on scope + the two-lane
  interface. No code.
- **Phase 1 — one real decision, worst-first.** Pick the **single** highest-value
  bounded call the grove makes today (candidates: steer-vs-new-turn
  classification; tool-permission risk scoring; model routing) and route it
  through a `DecisionLayer` **local-first**, with the generation layer as the
  fallback. Ship behind a flag.
- **Phase 2 — receipts.** Wire decisions into the append-only ledger (desktop
  `qp4`) with the six fields above; surface a tail in the inspector.
- **Phase 3 — the cloud lane.** Add the Jev-class HTTP adapter, off by default,
  with cost/latency metered. A/B against the local lane on real workloads before
  any claim is made.
- **Phase 4 — thresholds & owners.** Config gains `owner` + `escalation` per
  decision class; low-confidence escalations are recorded and reviewed in council.

## 6. Risks / honest limits

- **Calibration is the whole game.** A confident wrong answer is worse than no
  answer. Phase 1 must measure calibration, not just accuracy.
- **Vendor numbers are vendor numbers.** No savings claim ships without a
  workload-level measurement on our own traffic.
- **Small open models may not clear the bar.** Laya is 421M params; it may
  handle classification but not guardrail-risk calls. Lane L may be multi-model.
- **Two lanes = two failure modes.** The interface must make the lane explicit in
  every receipt so a bad decision is traceable to its source.
- **No new dependency by default.** Lane L must degrade to the existing local
  provider if no decision model is configured — never a hard requirement.

## 7. Open questions for the council

1. Which decision is Phase 1's "worst-first" target?
2. Do we ship Lane C (cloud Jev-class) at all, given the sovereignty posture —
   or keep it config-only, never on the default path?
3. What is the escalation threshold policy, and who owns it per decision class?
4. Does the decision ledger merge with the desktop's action ledger, or stay a
   parallel trail with a shared reader?

---

*Provenance: the Jev/Laya framing is sourced from the Emerging Technology
Breakfast Club broadcast (Issue #15, Frontier Pulse), captured in the desktop
repo at `handoff/emtech-breakfast-club-source.md`. Vendor performance figures
are flagged as vendor-supplied; Laya's comparison claims are unverified. Verify
live before any number reaches a slide.*
