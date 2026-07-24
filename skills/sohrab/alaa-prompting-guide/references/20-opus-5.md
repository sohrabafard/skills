# Claude Opus 5

API model id `claude-opus-5`. Anthropic's model for complex agentic coding and enterprise work, with its documented strength in long-horizon agentic tasks. 1M-token context window as both default and maximum, 128k max output, $5/$25 per MTok — the same price as Opus 4.8. Anthropic positions it as "a thoughtful and proactive model that comes close to the frontier intelligence of Claude Fable 5 at half the price." In this pack it is the default Claude tier for architecture-sensitive review, subtle bug finding, complex agentic coding, and long-horizon work (see `references/90-model-selection.md`).

The docs say existing Opus 4.8 prompts "perform well" on Opus 5. That is true of the prompt body and false of the scaffolding. Several behaviors invert relative to Opus 4.8, so the parts of a 4.8-tuned prompt that compensated for 4.8's weaknesses are now actively counterproductive.

## Behaviors that inverted relative to Opus 4.8

**Delegation.** Opus 4.8 under-spawned subagents, so 4.8 prompts encouraged delegation. Opus 5 "delegates more readily than prior models," and delegation multiplies cost and time on small tasks. Delegation guidance must now cap rather than encourage — see `## Subagents`.

**Self-verification.** Opus 5 verifies its own work without being told. The doc is explicit: **remove explicit verification instructions** — "include a final verification step," "use a subagent to verify" — because they cause over-verification and waste tokens for no quality gain. Draw the distinction carefully before deleting anything:

- A *redundant self-check* is the same agent re-reading its own output against the same criteria it just applied. Delete these.
- An *authority boundary* is a structurally independent verifier that exists so that no lane approves its own change: a fresh-context reviewer, a separate review lane, a gate another role owns. This is a governance property, not a quality patch, and it survives the model upgrade. Keep it. The doc itself notes writer-verifier patterns work well on Opus 5.

The test: if the verifier disappeared and the only loss would be a second look, remove it. If the loss would be that an implementer now signs off on its own work, keep it.

**Self-correction.** Opus 5 "catches and fixes mistakes well without prompting." Avoid re-check instructions such as "double-check your answer" or "re-verify before responding"; they compound with the model's own behavior and add cost without adding quality. It also narrates corrections more than prior models, which needs its own control:

```
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

**Run length and narration.** Opus 5 runs longer, narrates readily during agentic work, and writes longer files than prior models. Response length, deliverable length, and progress-update cadence each need explicit calibration — see `## Response length, tone, and progress updates`. Note that `effort` controls thinking volume, not response length; lowering effort will not shorten the answer.

## Migration and API notes

Migration checklist from Opus 4.8, per the live migration guide:

- Update the model name from `claude-opus-4-8` to `claude-opus-5`.
- Review workloads that ran without a `thinking` field: on Opus 4.8 they ran without thinking, on Opus 5 they run with adaptive thinking.
- Revisit `max_tokens`, which remains a hard limit on total output (thinking plus response text), or pass `thinking: {type: "disabled"}` at effort `high` or below to preserve the old behavior.
- Audit requests that disable thinking: `thinking: {type: "disabled"}` with effort `xhigh` or `max` returns a 400 error, enforced per request. Opus 4.8 accepted that combination.
- Re-baseline cost on your own workloads, and re-run an effort sweep rather than carrying over 4.8 effort defaults.

Neither the Opus 5 prompting page nor the migration guide states a restriction on `temperature`/`top_p`/`top_k` (unlike Sonnet 5, where they error). Verify against the API reference before relying on that either way.

## Effort and thinking

`effort` (`low` / `medium` / `high` / `xhigh` / `max`) is the primary control for token cost and response time. The effort reference marks `high` as the default level, and recommends for Opus 5: start at `xhigh` for coding and agentic work, use `high` for most intelligence-sensitive workloads, and treat `low` and `medium` as genuinely usable — they are stronger on Opus 5 than on earlier Opus models and produce strong quality at a fraction of the tokens and latency. Use effort liberally as the cost lever wherever your own evals show quality holds. Set a large `max_tokens` at higher effort, starting around 64k.

Thinking is on by default and **disabling it is capped at `high` effort or below**. That cap, plus two documented failure artifacts, is why lowering effort while leaving thinking on is the better cost lever than disabling thinking:

- **Tool calls as text.** With thinking disabled, the model occasionally writes a tool call into visible text instead of emitting a structured `tool_use` block. Mitigation: `You may say a brief sentence before using a tool.`
- **Internal XML tags in output.** The model can emit `<thinking>` tags into the visible response. Remove any rules instructing the model not to think, and use the general form rather than naming specific tags: `Do not include internal or system XML tags in your response.`

Changing effort between requests invalidates cached prefixes; hold effort constant within a cached conversation and vary it across workloads. For the cross-model decision procedure, read `references/50-effort-and-thinking.md`.

## Response length, tone, and progress updates

Default responses run longer than on prior Opus models. For conciseness:

```
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

For long system prompts, add a late reminder:

```
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

Files Opus 5 writes — reports, Markdown, summaries — are often longer than on prior models. Calibrate deliverable length separately from response length:

```
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

For agentic narration, set the cadence rather than a counter:

```
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

## Prompting techniques that matter most

- Give the complete task specification upfront. Opus 5 performs best on multi-file features, larger refactors, and end-to-end work when the whole spec arrives at once, and it completes full tasks rather than leaving stubs.
- Constrain scope explicitly on narrow tasks:

```
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

- Use XML tags to separate role, instructions, context, examples, and input documents; use 3–5 `<example>` blocks for format-sensitive work.
- For long-context work, put long documents near the top and the query/instructions at the end — the family guidance cites up to ~30% quality improvement from that ordering alone.
- Use direct action verbs (`change`, `implement`, `verify`, `report only`); state when an instruction applies to every section, file, or item.
- Drop "avoid overthinking," "double-check," and "verify before responding" boilerplate — 4.6/4.8-era patches. Keep confirm-before-destructive-action guidance for shared systems and irreversible operations: that is an authority rule, not a quality patch.

## Subagents

Opus 5 coordinates subagent teams well — writer-verifier patterns work, and agents rarely overwrite each other's work. The problem is volume, not coordination. Cap it:

```
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

Read that last clause against the authority-boundary distinction above: it forbids spawning a subagent to re-check *your own* output, not a review lane that exists because implementers do not approve their own changes. Multi-agent writer-verifier remains a supported pattern where the verifier is a distinct role with its own context and criteria.

For Claude Code's actual Agent tool, `/loop`, Workflow tool, plan mode, and `/goal`, read `references/41-claude-code-runtime-features.md`.

## Code review harnesses

Opus 5 reviews with high precision and recall: it finds real bugs at a high rate per pass, and its additional findings are mostly real issues rather than false positives. Accuracy holds at lower effort, which supports a fast pass at review time and a more thorough pass later. The failure mode is instruction-literal filtering — a harness that says "only report high-severity issues" or "be conservative" will report less. Report everything, filter downstream. Anthropic's documented coverage-stage language (stated verbatim on the Sonnet 5 page and applicable here):

```
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

If a single pass must self-filter, define the bar concretely: report any bug that could cause incorrect behavior, a test failure, or a misleading result; omit only nits such as pure style or naming preferences.

## Vision, office, and document tasks

Vision is strong on charts, documents, diagrams, UI, and frontend visual replication. Re-validate any prompt-side vision workarounds tuned for prior models — they may no longer be needed. Performance is strongest when the model has tools to iteratively analyze, crop, and visually verify its work; tool use is a more cost-effective lever here than thinking alone. For office work, Opus 5 generates and edits complex multi-sheet spreadsheets with non-trivial formulas and produces well-structured slide decks; supply any required styles or templates explicitly.

## Caveats

Pricing ($5/$25 per MTok), the 1M context window, 128k max output, the 64k `max_tokens` starting point, effort level names and defaults, and the 400-error conditions are time-sensitive Anthropic-stated figures — re-check the live docs before hard-coding them elsewhere. The Opus 5 prompting page states no default effort value for the model specifically; `high` as the default comes from the shared effort reference table. This model postdates a typical training cutoff; every claim here came from a live fetch, not memory.

## Sources

- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
- [Effort (parameter reference)](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)

## Companion reference

For Claude Code's shared agentic features (Agent subagents, `/loop`, Workflow tool, plan mode, `/goal`), read `references/41-claude-code-runtime-features.md`. For the cross-model effort decision procedure, read `references/50-effort-and-thinking.md`.
