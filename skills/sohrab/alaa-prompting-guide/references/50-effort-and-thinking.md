# Effort and Thinking: A Cross-Model Decision Procedure

This file owns the question "how hard should this model think, and how do I know?" It applies to every model in scope and to both runtimes. Read the target model's own reference for the levels it actually supports; read this file for how to choose among them.

## The two levers do different jobs

**Model** selects the *kind* of judgment available. **Effort** selects *how much search* that judgment performs before it answers.

The two do not substitute for each other, and treating them as one dial is the most common and most expensive mistake in agentic configuration. Raising effort on a weaker tier does not buy the judgment of a stronger tier — it buys a longer, more thorough exploration of a shallower solution space. Raising the tier while leaving effort at a floor too low to explore does not buy depth either — it buys a frontier model answering from its first instinct.

Choose the model from the kind of judgment the task requires. Choose the effort from how much search that judgment needs. Then verify, because both choices are empirical.

## What effort does not control

Effort controls thinking volume. It does not control response length, and on the current Claude flagship the documentation says so explicitly. This matters because the natural reflex when a model's answers run long is to lower effort, and that reflex fails: it produces a shallower answer of roughly the same length. Response length, written-deliverable length, and progress-update cadence are all prompt-controlled and need their own explicit instructions. See `references/20-opus-5.md` for the verbatim calibration snippets.

Effort also does not control scope. A model that widens the task beyond what was asked is not thinking too hard; it is missing a scope constraint. Fix that in the prompt.

## Thinking: keep it on, lower the effort instead

Across the current Claude generation, thinking is on by default in adaptive mode, and on the flagship it cannot be disabled at the top two effort levels at all. Where disabling it is technically possible, it is still the wrong cost lever: it degrades tool-use reliability, it produces artifacts such as tool calls emitted as prose, and it saves less than simply stepping the effort down one level.

**The rule: never disable thinking to save money. Lower the effort.** If you have disabled thinking and are now writing prompt instructions to repair the resulting behavior — nudging the model to actually call its tools, or telling it to suppress internal tags — you are paying twice for a choice that should be reversed.

Manual thinking budgets are no longer the mechanism on this Claude generation; adaptive thinking plus effort replaced them, and passing an explicit budget is an error rather than a tuning knob. Do not carry forward a prompt that sets one. Note also that `adaptive` is a thinking mode, not an effort value, and passing it as one is a mistake.

## Choosing a starting level

Each family has a documented starting point, and the numbers are not the same across models, which is why "use high effort" is meaningless advice across vendors. This file does not restate them — a second copy is the first one to go stale. Read the target model's own reference (`references/20-opus-5.md`, `references/30-sonnet-5.md`, `references/40-fable-5.md`, `references/10-gpt-5-6.md`) for the levels it supports, its default, and its recommended starting point for coding and agentic work.

Every family gives the same meta-instruction and it is the most important sentence in this file: **an effort level inherited from a previous model generation is an untested assumption, not a tuned setting.** Re-run the sweep.

## The decision procedure

1. **Classify the judgment.** Is the decision already made, and the lane applies it? Or must the lane itself decide something non-obvious? The first is mid-tier work; the second is top-tier work. This question, not the sensitivity of the surface, selects the model.
2. **Classify the search.** Does the answer require exploring alternatives, tracing consequences across a system, or holding several constraints simultaneously? That is a high-effort shape. Does it require executing a known procedure and reporting what happened? That is a low-effort shape.
3. **Start at the family's documented starting point** for that shape, not at your habit from a previous generation.
4. **Respect the tier ceiling.** Every tier has a level past which raising effort is worse value than changing the model. When you reach it, change the model.
5. **Sweep before committing.** Run the same representative task at your chosen level and at one level below it. If quality holds, the lower level is the correct pin and you have been overpaying. If it does not, you now have evidence for the higher pin rather than a preference.
6. **Record the reason wherever the pin is raised.** An unexplained high pin is indistinguishable from drift, and it will be copied forward into contexts where it was never justified.

## Escalation is earned by decision density

The single most useful heuristic in this file: **escalate on decision density, not on surface sensitivity and not on goal importance.**

A lane that mechanically applies an already-ratified decision, an amended contract value, or a precise specification is mid-tier work no matter which surface it touches. Authentication code, payment code, and migration code are not automatically top-tier lanes — in a properly gated pipeline those surfaces already receive top-tier scrutiny at the review and specialist gates, and paying for it a second time inside the implementation lane buys nothing measurable.

Importance is handled by gates. Sensitivity is handled by gates. Tier is handled by how much of the decision is still open when the lane starts.

The corollary matters as much: when you are uncertain whether a lane qualifies, it does not. Dispatch the lower tier and let the gate catch the rare shortfall. One justified re-dispatch after evidence costs less than habitual escalation across every task you will ever run.

## Tier ceilings

A ceiling is the level past which raising effort on a given tier is worse value than switching tiers. Ceilings are a policy choice rather than a vendor constraint, but they are what makes a routing decision decidable instead of arguable, and both orchestrator packs in this family enforce them.

The pattern to reproduce in any pack you write: give every tier below the top an explicit ceiling; state that above the ceiling the correct move is to change the model, never to raise the effort; and reserve the absolute maximum level for a named per-invocation retry after a documented failure, never as a standing pin. A `max` pin in an agent definition is a defect, because it removes the escalation path — there is nothing above it to escalate to.

## Effort is not the only cost lever

Before raising effort, check whether the real problem is prompt shape. On the current GPT generation, leaner system prompts measurably improved evaluation scores while substantially cutting tokens, which means prompt bloat degrades quality and costs money at the same time. A padded prompt answered at high effort is strictly worse than a lean prompt answered at medium.

The same applies to context. A model reasoning over a poorly assembled context does not need more thinking; it needs better retrieval. Raising effort to compensate for missing facts is the most expensive way to fail, because the model will explore thoroughly and confidently in the wrong direction.

## Anti-patterns

- Carrying an effort level forward from a previous model generation without re-running the sweep.
- Disabling thinking to control cost instead of lowering effort, then writing repair instructions for the resulting behavior.
- Lowering effort to shorten responses. Effort is not a verbosity control.
- Raising effort because the goal is important or the surface is sensitive rather than because the lane must decide something.
- Pinning the maximum level anywhere, which removes the escalation path.
- Raising effort past a tier ceiling instead of changing the model.
- Setting an explicit thinking budget on a generation that no longer accepts one.
- Passing `adaptive` as an effort value.
- Raising effort to compensate for a bloated prompt or a badly assembled context.
- Benchmarking by effort name across vendors, where the same word denotes different amounts of work.

## Caveats

Thinking-disable constraints and the availability of manual thinking budgets are vendor-stated and time-sensitive; effort level names, per-model defaults, and starting-point recommendations are not restated here — read the target model's own file, which is the current source for its own numbers. The measured lean-prompt figures are from a specific vendor's internal testing on a specific generation and should not be generalized. Re-read the sources below before hard-coding any of these anywhere, and treat the tier ceilings here as this pack's policy rather than as vendor rules.

## Sources

- [Effort parameter reference](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Using the latest model (GPT-5.6)](https://developers.openai.com/api/docs/guides/latest-model)
