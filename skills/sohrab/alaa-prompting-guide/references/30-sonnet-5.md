# Claude Sonnet 5

API model id `claude-sonnet-5`. The balanced tier: 1M-token context (default and maximum), 128k max output, $3/$15 per MTok, with introductory pricing of $2/$10 through 31 August 2026. Adaptive thinking, vision, and the `computer_20251124` computer-use tool. Anthropic calls it the most agentic Sonnet yet — the largest gains over Sonnet 4.6 are in sustained multi-step tool use, unprompted self-verification, and finishing tasks that previously stalled halfway.

Frame its place honestly. Sonnet 5 is the right default for ordinary implementation, extraction, high-volume, and latency-sensitive work. It is not a cheaper Opus 5. This pack caps Sonnet 5 at `high` effort: a lane that needs more than `high` should change model, not raise effort, because `xhigh`/`max` on Sonnet buys less per token than moving to Opus 5 for the same work (see `references/90-model-selection.md`).

## Migration and API notes

From Sonnet 4.6, three breaking changes:

- **Adaptive thinking is on by default.** Requests without a `thinking` field ran without thinking on 4.6; on Sonnet 5 they run with adaptive thinking. Turn it off with `thinking: {type: "disabled"}`. Manual extended thinking — `thinking: {type: "enabled", budget_tokens: N}` — is **not supported and returns a 400 error**.
- **Sampling parameters error.** `temperature`, `top_p`, and `top_k` set to any non-default value return a 400. Remove them on migration and steer tone through the system prompt instead. This also removes temperature as a lever for stylistic variation.
- **New tokenizer.** The same input text produces approximately 30% more tokens than on Sonnet 4.6. Re-run token counting and revisit every `max_tokens` limit tuned on the older model.

Also add handling for `stop_reason: "refusal"` if the workload touches cybersecurity topics, and re-baseline cost.

## Effort and thinking

`effort` is the primary lever. **Sonnet 5 defaults to `high`.**

`max` is absolute maximum capability with no token constraint; `xhigh` is for the hardest coding and agentic tasks; `high` is the default and balances token usage against intelligence for most use cases; `medium` suits cost-sensitive workloads; `low` is for short, scoped tasks and latency-sensitive workloads.

Cross-model mapping against the prior generation, stated verbatim in the docs: **Sonnet 5 at `medium` ≈ Sonnet 4.6 at `high`; Sonnet 5 at `high` ≈ Sonnet 4.6 at `max`.** A pipeline ported from 4.6 can usually step down one level and keep quality. If reasoning looks shallow on a complex problem, raise effort rather than prompting around it. For latency-critical low-effort tasks that still need multi-step reasoning:

```
This task involves multistep reasoning. Think carefully through the problem before responding.
```

If adaptive thinking triggers too often behind a large system prompt:

```
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

Because thinking counts against the same `max_tokens` output cap, leave headroom at `high`, `xhigh`, or `max` — a tight cap yields a response that is mostly thinking and then truncates. Read `references/50-effort-and-thinking.md` for the cross-model decision procedure.

## Response length, tone, and progress updates

Sonnet 5 calibrates response length to task complexity rather than a fixed verbosity: shorter on simple queries, longer on open-ended analysis. To reduce verbosity:

```
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Prefer positive examples of the style you want over negative instructions about what to avoid. Long-form prose style may shift versus 4.6; if the product needs a specific voice, state it — for example, `Use a warm, collaborative tone. Acknowledge the user's framing before answering.`

Progress updates during long agentic traces are regular and higher quality than on 4.6. Remove scaffolding that forces interim status messages on a counter. If the updates do not fit the product, describe what they should contain, with examples.

## Prompting techniques that matter most

- **Literal, explicit instruction following, especially at lower effort.** Sonnet 5 does not silently generalize an instruction or infer an unstated request. This is a benefit for structured extraction and API use, and a trap for loosely scoped prompts. State scope in full: `Apply this formatting to every section, not just the first one.` Anywhere a prompt says "fix the bug" and means "fix every instance of this class of bug," say the second thing.
- **Be explicit about action versus suggestion.** "Suggest some changes" will produce suggestions, not edits.
- **Tool use is more aggressive by default** than on 4.6, and higher effort produces substantially more tool calls. With thinking disabled it is *less* likely to reach for tools — add explicit triggering rules if tool calls are critical in that configuration. It also runs independent tool calls in parallel readily; steer up or down explicitly.
- Use XML tags to separate instructions, context, and input; 3–5 `<example>` blocks for format-sensitive work.
- For long-context work (20k+ tokens), put documents at the top and the query at the end — cited as up to ~30% quality improvement from ordering alone.
- Ask it to confirm before hard-to-reverse or shared-system actions (force-push, `rm -rf`, dropping tables, posting externally) unless autonomous action on those is intended.

## Subagents and agentic notes

Sonnet 5 tracks its remaining context budget through a conversation. For long-running or multi-context-window work, tell it explicitly that context will be auto-compacted so it should not wrap up early; use structured state files and commits as checkpoints; and give it verification tools (Playwright, computer use) so it can self-check without human round-trips. Family guidance for delegation:

```
Use subagents when tasks can run in parallel, require isolated context, or involve 
independent workstreams. For simple tasks, sequential operations, or single-file edits, 
work directly rather than delegating.
```

Sonnet 5 is a good subagent model at `low` or `medium` effort under an Opus 5 orchestrator. For Claude Code's Agent tool, `/loop`, Workflow tool, and plan mode, read `references/41-claude-code-runtime-features.md`.

## Frontend and design defaults

Sonnet 5 defaults to a consistent visual style on open-ended design briefs, and negative instructions ("don't use that color") tend to shift it to a different fixed default rather than produce variety. Temperature is no longer available as a variation lever. Two remedies are documented as reliable. First, **specify a concrete visual system** — palette hexes, typeface direction, layout structure, corner radius, spacing rhythm, motion timing, section-by-section content; the doc's worked example runs to a full paragraph-level brief, and that level of specificity is the point. Second, **have the model propose options first**:

```
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

Where generic AI aesthetics are a risk, add to the system prompt:

```
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Interactive coding products

Use `xhigh` or `high` effort, add autonomous features such as an auto mode, and front-load a well-specified task description with intent and constraints in the first human turn. Minimize required user interactions: ambiguous prompts revealed progressively across many turns reduce token efficiency and sometimes performance.

## Code review harnesses

Expect an apparent recall drop when porting a review harness from an older model. Sonnet 5 follows a stated importance bar faithfully — it may investigate just as thoroughly and then not report findings below the bar. Fix it by separating coverage from filtering:

```
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

For a single pass that must self-filter: `Report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences.`

## Computer use

Sonnet 5 supports tool version `computer_20251124` with support up to 2576px / 3.75MP. Internal testing shows 1080p gives a good performance/cost balance; 720p or 1366×768 are viable for cost-sensitive workloads. Tune effort alongside resolution.

## Caveats

Pricing ($3/$15 per MTok, introductory $2/$10 through 31 August 2026), the ~30% tokenizer increase, the 1M/128k limits, the computer-use resolution caps, and the 400-error conditions are time-sensitive Anthropic-stated figures — re-check before quoting them elsewhere. "Defaults to `high` effort" is stated for the Claude API; do not assume every third-party surface matches. The `high` effort cap is this pack's policy, not an Anthropic recommendation — the docs recommend `xhigh` for Sonnet 5's hardest coding and agentic tasks.

## Sources

- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Effort (parameter reference)](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)

## Companion reference

For Claude Code's shared agentic features, read `references/41-claude-code-runtime-features.md`. For the cross-model effort decision procedure, read `references/50-effort-and-thinking.md`. For model choice, read `references/90-model-selection.md`.
