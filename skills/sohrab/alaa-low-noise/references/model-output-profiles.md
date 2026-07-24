# Model Output Profiles

Noise is not a constant. Each model family has documented defaults for how long it talks, how often it narrates, how literally it reads a concision instruction, and how eagerly it calls tools — and tool eagerness is a context cost, not merely a latency cost. Read only the section for the model in play, plus `## Cross-model rules`.

Two facts govern every section below. Effort and thinking parameters control *thinking volume*, not answer length, so lowering effort never shortens a response. And naming the content that must appear is a more reliable length control than asking for brevity, because a bare "be concise" trims caveats, validation results, and blockers before it trims filler.

## Claude Opus 5

Opus 5 runs longer, narrates readily during agentic work, and writes longer files to disk than prior models. Response length, written-deliverable length, and progress-update cadence are controlled independently, so a single concision instruction fixes at most one of them. Calibrate all three explicitly.

Response length:

```
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

Behind a long system prompt, add a late reminder:

```
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

Written deliverables — reports, Markdown, summaries — run long independently of the response, and need their own rule:

```
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

Agentic narration is set by cadence rather than by a counter:

```
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

Opus 5 also narrates its own corrections more than prior models, which is pure output noise when the correction changes nothing for the user:

```
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

Two behaviors matter for context economy specifically. Opus 5 delegates more readily than prior models, and every unnecessary subagent adds a return to the parent's context; cap volume with the documented language:

```
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

And it self-verifies without being told, so explicit "double-check your answer" or "include a final verification step" instructions cause over-verification — extra tool calls and extra tokens for no quality gain. Remove them. Do not confuse this with an authority boundary: a structurally independent reviewer that exists so no lane approves its own change survives, because it is a governance property rather than a quality patch.

## Claude Sonnet 5

Sonnet 5 follows instructions literally and explicitly, especially at lower effort, and does not silently generalize a rule to cases the rule did not name. A concision instruction must therefore state its own scope, or it will be applied to the first section and nowhere else. Write `Apply this to every section, not just the first one` rather than trusting the rule to spread on its own; the same applies to "summarize each file," "bound every log," and "trim each report."

Verbosity:

```
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Prefer positive statements of the style you want over negative instructions about what to avoid; negatives tend to move Sonnet 5 to a different fixed default rather than to genuine variety.

For context economy, the operative fact is that Sonnet 5 reaches for tools more readily than the prior generation, and higher effort produces substantially more tool calls. On this model the dominant context cost is usually tool results rather than prose, so steer tool use explicitly — say when to search rather than read, and when one call suffices. With thinking disabled the behavior inverts and it is *less* likely to call tools, so triggering rules must be explicit in that configuration.

Progress updates during long agentic traces are regular and higher quality than on the prior generation. Remove scaffolding that forces interim status messages on a counter; describe what an update should contain instead.

One trap: because Sonnet 5 honors a stated bar faithfully, a brevity instruction can silently become a reporting filter in review or audit work, suppressing real findings rather than words. Separate coverage from filtering when both matter.

## Claude Fable 5

Fable 5 carries documented brevity and user-facing-communication guidance that is directly on-topic for this skill.

```
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

The key distinction: terse shorthand *between* tool calls is fine and appropriately cheap, but after a long tool-heavy run the final message is the user's first look at the work, and Fable 5 carries its working shorthand into it. Instruct it to re-ground — outcome first, complete sentences, no arrow chains or invented labels, project terms reintroduced, and each file, commit, or flag given its own plain-language clause.

To suppress deliberation printed as prose:

```
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

Quiet is not the same as unverified. On long runs, ground every progress claim against an observed result:

```
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

Where a harness needs verbatim mid-run content without ending the turn, a `send_to_user`-style tool is the documented mechanism; use it only for user-facing content, never for narration or reasoning, since over-calling it defeats its purpose. Avoid surfacing raw remaining-context countdowns to the model, which prompt premature wrap-up.

## GPT-5.6 and Codex

On this family, leanness is a measured quality property. OpenAI's internal testing on this generation found that trimming prompts improved evaluation scores by roughly **10–15%** while cutting total tokens by **41–66%** and cost by **33–67%**. Both directions moved at once, so prompt bloat here is a quality regression and not merely an expense — a padded instruction set competes with itself for compliance.

The three operative rules:

- State each instruction once. A rule repeated in the system prompt, the developer message, and a tool description does not reinforce itself; give every rule exactly one owning location.
- Expose only task-relevant tools, with concise descriptions confined to the contract — inputs, outputs, errors, routing constraints.
- Keep only examples that encode a real requirement or close a measured gap. An example demonstrating a format the schema already enforces is dead weight.

For output length, `text.verbosity` (`low`, `medium`, `high`) sets a task default, and concrete content requirements go in the prompt on top of it; verbosity is independent of reasoning effort. For long tool runs, require exactly one short preamble before the first call rather than running narration.

Programmatic Tool Calling is the strongest context-economy lever available on this family: the model writes code that calls tools and filters, joins, ranks, or aggregates results in a hosted runtime, so the intermediate volume never enters the model's context. It pays on bounded, tool-heavy stages with predictable data flow. Use direct calls instead when one call suffices, intermediate results are already small, each result could change the next decision, or the action needs approval.

Note the polarity difference on delegation: unlike Opus 5, GPT-5.6 and Codex do not fan out unprompted, so parallel work must be authorized positively — but the context-economy rule is unchanged, because only a subagent's return lands in the parent.

## Cross-model rules

- Effort and thinking parameters govern thinking volume, not answer length. Length, deliverable size, and narration cadence each need their own instruction.
- Name the required content instead of asking for brevity; generic concision instructions suppress caveats, validation evidence, and blockers first.
- State each rule once, in one owning file or message. Repetition costs context and does not raise compliance.
- Fewer tokens, calls, or turns count as an improvement only when the final output still clears its quality bar.
- Never let a brevity rule act as a reporting filter in review, audit, or coverage work. Separate what is reported from how compactly it is written.
- Re-verify per-model behavior when models change; these profiles describe current generations, not permanent properties.

## Caveats

Every per-model claim here is restated from this pack's prompting-guide references (`20-opus-5.md`, `30-sonnet-5.md`, `40-fable-5.md`, `10-gpt-5-6.md` in the `alaa-prompting-guide` skill), which were verified against live vendor documentation on 24 July 2026. The fenced snippets are vendor-documented language quoted verbatim; treat any paraphrase around them as this pack's interpretation. The 10–15% / 41–66% / 33–67% figures are OpenAI's own measurement on their evaluation set for this generation, not a general law. Model names, defaults, parameter surfaces, and effort levels are time-sensitive — re-check the live docs before quoting them elsewhere. Some of these models postdate a typical training cutoff, so do not substitute recalled behavior for the sources below.

## Sources

- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Effort (parameter reference)](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Using GPT-5.6 | OpenAI API](https://developers.openai.com/api/docs/guides/latest-model)
- [Programmatic Tool Calling | OpenAI API](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)
- [Prompting – Codex](https://developers.openai.com/codex/prompting)
