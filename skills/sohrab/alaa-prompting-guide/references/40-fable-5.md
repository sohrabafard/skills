# Claude Fable 5

**Correct the obvious assumption first: Fable 5 is not a creative-writing or persona model.** It is Anthropic's top capability tier, positioned above Claude Opus 4.8 for the hardest, longest-running, and most ambiguous work. Use it for multi-day autonomous agentic runs, complex migrations, large refactors, deep enterprise knowledge work, heavy vision/document analysis, and problems that have already exceeded Opus 4.8's reliable range. Do not use it as a routine upgrade for ordinary coding when Sonnet 5 or Opus 4.8 is enough.

Mythos 5 shares Fable's underlying capability but is a separate limited-availability model without Fable's safety classifiers. This pack's guidance is for Fable 5 unless a task explicitly names Mythos 5.

## Capability improvements

Compared with Opus 4.8, Fable 5 is documented as stronger at long-horizon autonomy, first-shot correctness on complex well-specified problems, dense vision/screenshot interpretation, enterprise workflows across spreadsheets/slides/docs, code review and debugging outside covered safety domains, ambiguity navigation, and dispatching/sustaining parallel subagents. Testing it only on easy tasks undersells it; pick a task near the top of the difficulty range when evaluating the model.

Fable 5 is not intended for offensive cybersecurity or biology/life-sciences work. Safety classifiers can also catch benign cybersecurity, beneficial life sciences, and reasoning-extraction-adjacent requests. Harnesses that need continuity should configure fallback to Opus 4.8 for `stop_reason: "refusal"` where appropriate.

## Effort, thinking, and long turns

Fable 5 and Mythos 5 use adaptive thinking only. Traditional extended-thinking token budgets do not apply; `effort` (low / medium / high / xhigh) controls the trade-off among intelligence, latency, and cost. Use `high` as the default for most tasks, `xhigh` for the most capability-sensitive workloads, and `medium` or `low` for routine work. Lower effort on Fable 5 can still exceed high-effort results on prior models, so reduce effort if a task is correct but slower or more deliberative than needed.

The raw chain-of-thought is never returned; `thinking.display` is summarized or omitted. Do not ask Fable 5 to echo, transcribe, or explain internal reasoning in user-facing text; this can trigger reasoning-extraction refusals. Use structured thinking outputs where supported and a user-message tool for progress visibility.

Hard individual requests can run for many minutes at higher effort, and autonomous runs can extend for hours. Adjust client timeouts, streaming, user-facing progress indicators, and async check-in mechanisms before migrating an Opus 4.8 harness.

## Prompting techniques that matter most

- **Prevent overplanning**: tell it to act once it has enough information, not to re-derive established facts, and to recommend a path rather than survey options it will not pursue.
- **Curb unrequested tidying**: tell it not to add features, refactor, introduce abstractions, add defensive branches, or create compatibility shims beyond the task.
- **Lead with the outcome**: one concise brevity instruction is usually enough; the first sentence should answer what happened or what was found.
- **Pause only for real blockers**: destructive or irreversible actions, real scope changes, or input only the user can provide.
- **Ground progress claims**: before reporting progress, audit each claim against an actual tool result from the session; state failed, skipped, unverified, and verified work plainly.
- **Bound unrequested side actions**: when the user is asking a question or thinking aloud, report the assessment and stop; do not apply a fix until asked.
- **Delegate actively**: use subagents for independent subtasks, keep working while they run, and intervene when a subagent lacks context or drifts.
- **State intent, not just the request**: explain the larger outcome and audience so Fable can connect the task to relevant context.
- **Loosen old skills and prompts**: highly prescriptive prompts tuned for prior models can degrade Fable 5; remove scaffolding that default capability makes unnecessary.

## Ready-to-use autonomy fragment

```text
You are operating autonomously; the user is not watching in real time and cannot answer mid-task questions.
Proceed on reversible actions that follow from the request. Pause only for destructive or irreversible actions,
a real scope change, or input only the user can provide. Before reporting progress, verify every claim against
an actual tool result from this session. End only when the task is complete or genuinely blocked.
```

## Long-run memory

Fable 5 performs well when it can record lessons from prior runs. Provide a simple memory location and rules:

- Store one lesson per file or entry with a one-line summary at the top.
- Record corrections and confirmed approaches, including why they mattered.
- Do not save what the repo, tests, or chat history already records.
- Update an existing note instead of creating duplicates.
- Delete notes that later prove wrong.

To bootstrap memory from history, ask Fable 5 to review prior sessions with subagents, extract recurring lessons, store them in the chosen location, and explicitly reference that location in future runs.

## Early stopping and context-budget concerns

Deep into a long session, Fable 5 can occasionally end with a promise such as "I'll now run X" without actually calling the tool, or ask permission when it already has enough authority to proceed. A direct "continue end to end" usually recovers it, but autonomous pipelines should include the autonomy fragment above.

Avoid surfacing raw remaining-context countdowns to the model. If the harness must show them, add:

```text
You have ample context remaining. Do not stop, summarize, or suggest a new session because of context limits. Continue the work.
```

## Readability for user communication

Fable 5 can produce dense shorthand after long tool-heavy sessions. The final answer should be written for a reader who did not watch the run:

- Open with the outcome in one complete sentence.
- Reintroduce project-specific terms before relying on them.
- Use complete sentences instead of arrow chains or compressed labels.
- Spell out what files, commits, flags, or identifiers mean in plain language.
- Choose clarity over maximum brevity when summarizing long work.

## Send-to-user tool

Long asynchronous agents sometimes need to surface user-visible content without ending the turn: a partial deliverable, a specific progress update, or a direct reply to a question asked mid-loop. Provide a tool like:

```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The content to display to the user."
      }
    },
    "required": ["message"]
  }
}
```

Defining the tool is not enough. Pair it with an instruction:

```text
Between tool calls, when you have user-facing content that must be shown verbatim, call send_to_user with that content. Use it only for user-facing content, not narration or internal reasoning.
```

Do not route routine narration or reasoning through `send_to_user`; over-calling it defeats its purpose.

## Recommended scaffolding changes

- Start evaluation with a hard, realistic task, not only a simple workload.
- Make self-verification explicit in long runs; prefer separate fresh-context verifier subagents over self-critique.
- Refactor older prompts and skills by removing excess scaffolding when Fable 5 performs better with less prescription.
- Audit prompts for chain-of-thought extraction requests and replace them with structured thinking/progress surfaces.
- Add send-to-user only when the UX requires verbatim mid-task user-visible content.

## Caveats

Pricing, exact availability, safety-classifier behavior, fallback policy, and any API limits are time-sensitive Anthropic-stated details. Re-check the live docs before hard-coding them elsewhere. This model postdates a typical training cutoff; treat every claim here as sourced from the live-docs research pass, not memory.

## Sources

- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)
- [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [Claude Fable - Anthropic](https://www.anthropic.com/claude/fable)

## Companion reference

For Claude Code's shared agentic features (`/loop`, Agent subagents, Workflow tool, plan mode / Ultraplan, Claude Code's own `/goal`), read `references/41-claude-code-runtime-features.md` next.
