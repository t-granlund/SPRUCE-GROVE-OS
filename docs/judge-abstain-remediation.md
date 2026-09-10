# Judge ABSTAIN Remediation: Synthetic.new metadata.weight_versions Schema Drift

- Repo: SPRUCE-GROVE-OS
- Sprint beads: SPRUCE-GROVE-OS-5al.1/.3/.2/.4/.5 (nine re-verification rounds)
- Fix bead: SPRUCE-GROVE-OS-5al.9
- Root cause proven: 2026-09-10 17:53Z
- Live confirmation gate: next /goal evaluation cycle

## Background

Nine consecutive sprint re-verification passes of beads SPRUCE-GROVE-OS-5al.1/.3/.2/.4/.5 all passed locally with fresh evidence (BUILD-LOG.md sections 11-20), yet every evaluation cycle returned the identical judge remediation note: `[default] warn ABSTAIN endpoint error (UnexpectedModelBehavior): Invalid response from synthetic chat completions endpoint: 1 validation error for ChatCompletion metadata.weight_versions Input should be a valid string (input was a list)`. Abstaining judges do not vote, so goal completion was undecidable and the loop remediated forever despite zero repo defects. The failure never reproduced in local development because the trigger depends on the pydantic-ai release the judge harness resolves, not on the repo pin. The root cause was proven empirically on 2026-09-10 17:53Z and fixed the same day in bead SPRUCE-GROVE-OS-5al.9.

## Root Cause

Two conditions collided:

1. Synthetic.new chat completions return `metadata.weight_versions` as a LIST of span objects, not a string.
2. pydantic-ai's `OpenAIChatModel._validate_completion` re-validates every response against its strict internal `_ChatCompletion` schema, whose `metadata` field is typed `dict[str, str]` on several releases. A list value fails that validation, pydantic-ai raises `UnexpectedModelBehavior`, and the wiggum goal-judge plugin (`code_puppy_core_plugins/wiggum/judge.py`) catches it and converts it into an ABSTAIN verdict.

Version matrix (verified empirically with isolated uv environments):

| pydantic-ai release | Strict `_ChatCompletion.metadata` (`dict[str, str]`) declared | Behavior on list `weight_versions` |
| ------------------- | ------------------------------------------------------------- | ---------------------------------- |
| 2.33.0 | Yes | ValidationError, judge ABSTAINs |
| 2.35.0 (repo pin) | No | Passes untouched; why local dev never failed |
| 2.36.0 | Yes | ValidationError, judge ABSTAINs |
| 2.40.0 | Yes | ValidationError, judge ABSTAINs |

The judge harness environment resolves a release that declares the strict metadata field; the repo pins 2.35.0, which does not. Same repo code and same Synthetic.new payload, different validation outcome: an environment-only defect with no repo bug behind nine rounds of remediation.

## Fix

Bead SPRUCE-GROVE-OS-5al.9 added `spruce_grove/tolerant_openai.py`:

- `TolerantOpenAIChatModel(OpenAIChatModel)` overrides the documented `_validate_completion` subclass hook.
- Strict validation runs first and its result is returned unchanged on success.
- Only on `ValidationError` does it retry once, JSON-encoding non-string `metadata` values (`_scrub_non_string_metadata`); choices, usage, and tool calls are untouched, only the informational metadata map is normalized.
- If metadata was already conforming, or the pydantic-ai internal validator cannot be located, the original error propagates unchanged, so unrelated failures are never masked.

Wiring in `spruce_grove/model_factory.py`:

- The wrapper is wired ONLY into the `custom_openai` branch (`_CUSTOM_OPENAI_MODEL_TYPES`), which by definition serves third-party OpenAI-compatible endpoints such as Synthetic.new; on the chat-completions return path specifically, since Responses-API models in that branch keep `OpenAIResponsesModel`.
- First-party OpenAI (and Azure) keep the stock strict `OpenAIChatModel`.

Tests and proof:

- `tests/test_tolerant_openai.py`: 9 tests, all passing, covering the scrub path, pass-through of unrelated failures, and factory wiring.
- An isolated strict-environment proof under pydantic-ai 2.33.0 showed the stock model raising the byte-exact judge error on a Synthetic.new-shaped payload while the tolerant model passed the same payload.

## Gap Register

| ID | Gap | Status | Owner | Next Action |
| -- | --- | ------ | ----- | ----------- |
| G1 | Judge-environment pydantic-ai schema drift vs the local 2.35.0 pin made verdicts depend on the environment, not the code | RESOLVED (5al.9) | spruce-grove dev | Closed by TolerantOpenAIChatModel; no further action |
| G2 | No local SYNTHETIC_API_KEY, so no live end-to-end judge re-run could be performed locally | OPEN (attempted 18:12Z: env empty, keychain exits 44 x2, puppy.cfg has no key) | user + next /goal cycle | Live gate remains the next /goal cycle in the keyed harness env; it now finds 4 named judges on tolerant syn:alias models, with the fixed [default] fallback as belt-and-braces |
| G3 | User-level judges.json in ~/.spruce_grove still has placeholder model strings ("REPLACE-WITH-YOUR-JUDGE-MODEL via /judges") for 4 enabled judges | OPEN | user | Ceremony decision: set real judge models (or disable placeholders) via /judges |
| G4 | Streaming-path chunks (`_ChatCompletionChunk`) are not covered by the tolerant wrapper | OPEN | spruce-grove dev | No observed failure; monitor judge logs and extend the wrapper to chunk validation only if one appears |
| G5 | Other third-party branches (cerebras, openrouter, zai_coding) still use stock strict models | OPEN | spruce-grove dev | Intentionally untouched to keep blast radius small; adopt the wrapper only if a failure is observed |

## Validation Plan

1. Evidence that now exists:
   1. `tests/test_tolerant_openai.py`: 9 passing tests.
   2. Isolated strict-env proof (pydantic-ai 2.33.0): stock model raises the byte-exact judge error; tolerant model validates the same payload.
   3. BUILD-LOG.md sections 11-20: nine local re-verification rounds with fresh evidence, plus root-cause and fix entries.
   4. Factory wiring verified: the wrapper appears only in the `custom_openai` branch.
2. What the next /goal cycle must show:
   1. A non-ABSTAIN verdict from the [default] judge (a real vote, not an endpoint error).
   2. No `ABSTAIN endpoint error (UnexpectedModelBehavior)` note mentioning `metadata.weight_versions`.
   3. A decidable goal outcome (PASS or an actionable FAIL), ending the remediation loop.
3. Fallback if a different metadata-shaped error appears:
   1. Capture the exact pydantic message and identify which `_ChatCompletion` (or `_ChatCompletionChunk`) field rejected the payload.
   2. Extend `_scrub_non_string_metadata` (or add a sibling scrub) to cover it and add a byte-exact regression test before re-running the cycle.
   3. If the failure is streaming/chunk-shaped, escalate G4: wrap chunk validation the same way, still scoped to the `custom_openai` branch.

## Final Review Checklist

- [x] `spruce_grove/tolerant_openai.py` uses only the documented `_validate_completion` hook; strict path unchanged on success
- [x] Wrapper wired only into the `custom_openai` branch; first-party OpenAI remains strict
- [x] Unrelated `ValidationError`s still propagate (no error masking)
- [x] `tests/test_tolerant_openai.py` passes (9 tests, plus 101-test regression slice green)
- [x] Strict-env proof recorded: stock model reproduces the byte-exact error under 2.33.0; tolerant model passes
- [ ] G2: next /goal cycle shows a non-ABSTAIN verdict (attempted locally 18:12Z; blocked by missing key, harness env is the gate)
- [x] G3: judges.json placeholders resolved (18:11Z ceremony PASS: 4/4 judges resolve to TolerantOpenAIChatModel on syn: aliases)
- [ ] G4/G5: monitoring owners acknowledged; wrapper extended only on observed failure
- [x] BUILD-LOG.md carries the 5al.9 fix entry and the pending live-confirmation note
