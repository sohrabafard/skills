# Model and Effort Policy

This file owns every model and reasoning-effort decision in the pack. The agent TOMLs carry the pins; this file explains what earns them and how to deviate.

## The two levers are not interchangeable

**Model** selects the tier of judgment available to a lane. **Reasoning effort** selects how much thinking that tier spends before answering. Raising effort on a weaker variant does not buy the judgment of a stronger one, and raising the variant does not compensate for an effort floor too low to explore the problem. Choose the variant from the kind of judgment the lane requires, then choose the effort from how much search that judgment needs.

Effort controls thinking volume, not output length. Output length is prompt-controlled — set `text.verbosity` where the surface exposes it, and rely on each agent's own output contract otherwise.

## Available variants and levels

Three variants are in scope. `sol` is the frontier variant for complex production reasoning. `terra` is the balanced variant. `luna` is the efficient variant for high-volume, bounded work. The bare `gpt-5.6` alias resolves to `sol` and is never used as a pin here, because a pin must be explicit about what it costs.

Reasoning effort accepts `none`, `low`, `medium`, `high`, `xhigh`, and `max`. `medium` is the vendor-recommended balanced starting point, and the documented migration advice is to hold your previous level and then test one level lower, because this generation often holds quality with fewer tokens. This pack takes that advice as policy: **pin one level lower than instinct and raise only on a measured shortfall.**

`none` is never used. A lane with no reasoning budget cannot honor an authority boundary or produce defensible evidence, which is what every role in this pack exists to do.

## The ladder

| Variant | Effort | Lanes |
|---|---|---|
| `sol` | `xhigh` | Adversarial review only |
| `sol` | `high` | Main thread; independent review; security; architecture; escalated implementation |
| `sol` | `medium` | Spec analysis; migration safety; API contract review |
| `terra` | `high` | Routine implementation; failure analysis; performance |
| `terra` | `medium` | Test strategy; research; observability; release; dependency audit; accessibility |
| `luna` | `medium` | Repository exploration; documentation; browser evidence |
| `luna` | `low` | Deterministic command execution and evidence capture |

Three hard rules make the ladder decidable without argument:

1. **Terra's ceiling is `high`.** A lane that needs more thinking than Terra at `high` does not need Terra at `xhigh` — it needs Sol. Change the variant, never the effort, at that boundary. This keeps exactly one escalation axis and prevents the expensive middle ground where a lane burns frontier-scale tokens on a mid-tier judgment.
2. **Luna's ceiling is `medium`.** Luna lanes are bounded by construction: run the given command, capture the given evidence, write the verified sentence. A Luna lane that needs to reason its way out of a problem has been mis-scoped, and the fix is a better dispatch or a different agent, not more effort.
3. **`max` is never a pin.** It is available for a single per-invocation override on a lane that has already failed at `xhigh` for a reason you can name. A `max` pin in an agent TOML is a defect.

## What earns an escalation

Escalation is earned by **decision density**, not by surface sensitivity and not by goal importance.

A lane that mechanically applies an already-ratified decision, an amended contract value, or a precise specification is routine Terra work no matter which surface it touches. Authentication code, payment code, and migration code all receive Sol-tier scrutiny through the reviewer and specialist gates; paying for it a second time inside the implementation lane buys nothing. Importance is handled by gates. Sensitivity is handled by gates. Variant is handled by decision density alone.

Escalate an implementation lane to `alaa-implementer-sol` only when the lane itself must make a non-obvious design decision, and only when at least one named criterion from `routing-matrix.md` applies. Record which criterion earned it, in the dispatch and again in the final agent roster. When you are uncertain whether a lane qualifies, it does not: dispatch Terra and let the review gate catch the rare shortfall. One justified re-dispatch after evidence costs less than habitual escalation across every goal.

## What earns a de-escalation

Step a lane down one level when all of the following hold: the acceptance criteria are fully checkable, the file scope is small and disjoint, no contract or trust boundary is in scope, and a prior lane of the same shape passed its gates at the lower level. Step it back up on the first gate failure attributable to shallow reasoning rather than to a missing fact.

Never step the verifier above `low` to make a failing command pass. A verifier that reasons harder is a verifier that starts debugging, which is a role violation, not an improvement.

## Lean prompts are part of the effort policy

Vendor testing on this generation found that leaner system prompts improved evaluation scores by roughly 10–15% while cutting total tokens by 41–66%. Prompt bloat is therefore not a stylistic problem here; it is a measurable quality regression that also costs money. Three rules follow, and they bind every dispatch this pack writes:

- **State each instruction once.** A rule repeated in the skill body, the agent TOML, and the dispatch text is a rule stated three times and obeyed no better for it.
- **Expose only task-relevant tools, with concise descriptions.** Tool inventory is prompt weight.
- **Keep examples only where they encode a product requirement or close a measured gap.** Decorative examples are pure cost.

Dispatch text carries lane facts — outcome, owned files, exclusions, acceptance criteria, verification commands, dependencies. It does not restate the role: the role lives in the agent TOML, and repeating it there dilutes both.

## Runtime capabilities worth pinning a decision on

**Programmatic Tool Calling** lets the model drive a hosted JavaScript runtime across a bounded, tool-heavy sequence instead of paying a round trip per call. Prefer it for verification and evidence lanes that fan across many small deterministic calls. Enable it deliberately through `allowed_callers` and handle the `program` and `program_output` items; do not leave it on for lanes that make a handful of calls, where it only adds surface.

**Persisted reasoning** via `reasoning.context` carries thinking across turns in a multi-turn lane. Use it for long implementation and diagnosis lanes; it is wasted on single-shot evidence lanes.

**Prompt caching** is explicit on this generation: writes cost 1.25× and reads stay discounted. Long-lived lanes that reuse a stable prefix pay for themselves. Audit `cached_tokens` and `cache_write_tokens` before assuming a caching win.

**Pro mode** aggregates additional model work before returning a single answer, billed at standard rates. Reserve it for genuinely quality-critical passes with clear evaluation criteria — deep review, hard optimization — and benchmark it against standard mode rather than assuming that the highest setting is automatically the best one.

## Deviating from a pin

A per-invocation override is legitimate in exactly three cases: the pinned variant is unavailable; the user explicitly asked for a different tier; or a lane failed at its pin for a reason you can state, and the retry raises exactly one level. Every override is reported in the agent roster alongside the reason. An override that is not reported is indistinguishable from drift.

## Freshness

Variant names, effort level names, defaults, caching multipliers, and the availability of Programmatic Tool Calling, persisted reasoning, and Pro mode are vendor-stated and time-sensitive. Re-read the official model guide before hard-coding any of them somewhere new. Nothing in this file should be quoted as a permanent constant.
