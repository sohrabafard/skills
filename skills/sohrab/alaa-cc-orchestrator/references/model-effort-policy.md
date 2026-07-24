# Model and Effort Policy

This file owns every model and effort decision in the pack. The agent files carry the pins; this file explains what earns them and how to deviate.

## The two levers are not interchangeable

**Model** selects the tier of judgment available to a lane. **Effort** selects how much thinking that tier spends before answering. Raising effort on a weaker tier does not buy the judgment of a stronger tier, and raising the tier does not compensate for an effort floor too low to explore the problem. Choose the model from the kind of judgment the lane requires, then choose the effort from how much search that judgment needs.

Effort controls thinking volume. It does not control response length — that is prompt-controlled, and every agent file in this pack carries its own output contract for exactly that reason.

## Available levels

Effort accepts `low`, `medium`, `high`, `xhigh`, and `max`; `high` is the default when the parameter is unset. Thinking is on by default and must stay on: at `xhigh` and above it cannot be disabled at all, and below that, disabling it degrades tool-use reliability for no saving that a lower effort level would not deliver more cleanly. **Never disable thinking in this pack. Lower the effort instead.**

## The ladder

| Tier | Effort | Lanes |
|---|---|---|
| Opus | `xhigh` | Lead session; independent review; adversarial review; security; architecture; escalated implementation |
| Opus | `high` | Spec analysis; migration safety; failure analysis; API contract review |
| Sonnet | `high` | Routine implementation; test strategy; performance; observability; release; dependency audit; accessibility |
| Sonnet | `medium` | Repository exploration; external research; documentation; browser evidence |
| Sonnet | `low` | Deterministic command execution and evidence capture |

Two hard rules make the ladder decidable without argument:

1. **Sonnet's ceiling is `high`.** A lane that needs more thinking than Sonnet at `high` does not need Sonnet at `xhigh` — it needs Opus. Change the model, never the effort, at that boundary. This keeps exactly one escalation axis and prevents the expensive middle ground where a lane burns frontier-scale tokens on a mid-tier judgment.
2. **`max` is never a pin.** It is available for a single per-invocation override on a lane that has already failed at `xhigh` for a reason you can name. A `max` pin in an agent file is a defect.

## What earns an escalation

Escalation is earned by **decision density**, not by surface sensitivity and not by goal importance.

A lane that mechanically applies an already-ratified decision, an amended contract value, or a precise specification is routine Sonnet work no matter which surface it touches. Authentication code, payment code, and migration code all receive Opus-tier scrutiny through the reviewer and specialist gates; paying for it a second time inside the implementation lane buys nothing. Importance is handled by gates. Sensitivity is handled by gates. Tier is handled by decision density alone.

Escalate an implementation lane to Opus only when the lane itself must make a non-obvious design decision, and only when at least one named criterion from `routing-matrix.md` applies. Record which criterion earned it, in the dispatch and again in the final agent roster. When you are uncertain whether a lane qualifies, it does not: dispatch Sonnet and let the review gate catch the rare shortfall. One justified re-dispatch after evidence costs less than habitual escalation across every goal.

## What earns a de-escalation

Step a lane down one level when all of the following hold: the acceptance criteria are fully checkable, the file scope is small and disjoint, no contract or trust boundary is in scope, and a prior lane of the same shape passed its gates at the lower level. Step it back up on the first gate failure attributable to shallow reasoning rather than to a missing fact.

Never step the verifier above `low` to make a failing command pass. A verifier that reasons harder is a verifier that starts debugging, which is a role violation, not an improvement.

## Lead-session behavior the pins do not cover

The lead runs Opus at `xhigh`, and that tier brings four behaviors this pack must actively counter-tune. Each of these is a deliberate inversion of guidance that was correct for the previous Opus generation.

**It delegates readily.** Earlier orchestration prompts had to push the lead to fan out. This one must do the opposite: one agent per lane, never several agents per lane, and no subagent for work the lead can finish in a handful of tool calls. Breadth in the catalog is free because gates are conditional; breadth in a single dispatch is not.

**It verifies without being told.** Remove every "add a final verification step" and "double-check your work" instruction. Independent verification survives in this pack for a different reason: `alaa-verifier` and `alaa-reviewer` exist as **authority boundaries**, not as redundancy. No lane may approve its own change. That is a structural property of the pipeline and it is not the same thing as asking a model to re-check itself — do not let the model collapse the two and skip a gate on the grounds that it already checked.

**It self-corrects without narration.** Do not instruct it to re-verify before responding. Correct an earlier statement only when the error would change the user's code, conclusions, or decisions; state the correction plainly and move on.

**It runs long and narrates freely.** Final reports and written deliverables need explicit length calibration, or they arrive padded. Cover the substance and stop; no filler sections, no redundant summaries, no boilerplate.

## Deviating from a pin

A per-invocation override is legitimate in exactly three cases: the pinned model is unavailable; the user explicitly asked for a different tier; or a lane failed at its pin for a reason you can state, and the retry raises exactly one level. Every override is reported in the agent roster alongside the reason. An override that is not reported is indistinguishable from drift.

## Freshness

Effort level names, defaults, thinking-disable constraints, context limits, and relative model pricing are vendor-stated and time-sensitive. Re-read the official effort reference and the model-specific prompting page before hard-coding any of them somewhere new. Nothing in this file should be quoted as a permanent constant.
