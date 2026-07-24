# Claude Fable 5

API model id `claude-fable-5`. Correct the obvious assumption first: Fable 5 is not a creative-writing or persona model. It is Anthropic's most capable widely released tier, built for complex, long-running, end-to-end work that previously took hours, days, or weeks. 1M-token context, 128k max output, $10/$50 per MTok, adaptive thinking always on, training and knowledge cutoff January 2026. Mythos 5 shares Fable's specs and pricing but is invitation-only and lacks Fable's safety classifiers; this file is about Fable 5 unless a task names Mythos 5 explicitly.

**As of this revision the orchestrator packs no longer pin Fable 5 at all.** Opus 5 reaches comparable quality on coding and agentic benchmarks at substantially lower cost — Anthropic's own figures put Opus 5 within 0.5% of Fable 5's peak CursorBench 3.2 score at half the cost, and above Fable 5 on OSWorld 2.0 at just over a third of the cost — and Opus 5 carries a May 2026 knowledge cutoff against Fable's January 2026. Fable 5 is now an **opt-in specialist**: name it deliberately for a specific lane, do not inherit it as a default.

## When Fable 5 is still the right call

Three things it is still uniquely good at:

- **Genuinely multi-day autonomous runs.** Sustained productive output over extended periods with strong instruction retention across the whole run — not "a long session," but work measured in days where early instructions must still bind at the end.
- **The heaviest sustained subagent fan-out.** It dispatches and manages parallel subagents and peer agents reliably over long horizons.
- **The hardest first-shot single-pass implementations.** Complex, well-specified problems where one correct pass beats several cheaper iterations.

Secondary documented strengths: dense technical images and detailed screenshots, enterprise workflows over spreadsheets/slides/documents, bug-finding recall outside restricted domains, and navigating complex multithreaded requests. If the task is not one of the three above, the cost case does not close — run the comparison in `references/90-model-selection.md` before pinning it.

## Costs and constraints

- **Price.** $10/$50 per MTok, double Opus 5. On long autonomous runs that multiplier lands on a very large token count.
- **Latency.** Individual requests can run for many minutes at higher effort; autonomous runs can extend for hours. Adjust client timeouts, streaming, and progress indicators before migrating a harness onto it.
- **Staleness.** January 2026 cutoff. Any version-sensitive claim needs a live check.
- **Refusal domains.** Safety classifiers decline offensive cybersecurity (exploits, malware, attack tooling), biology and life sciences (lab methods, molecular mechanisms), and thinking extraction (prompts asking it to reproduce internal reasoning as response text). Benign security work and beneficial life-sciences work can also trigger the safeguards. **This makes Fable 5 a poor fit for a security-review lane** — the exact work such a lane does is what the classifiers are tuned to catch, and a refusal mid-run is worse than a slightly weaker model.
- **Fallback is mandatory, not optional.** Any harness that needs continuity must configure fallback handling for `stop_reason: "refusal"`. Note that the live docs still name Claude Opus 4.8 as the fallback target; re-check whether that has been updated to Opus 5 before wiring it.

Audit prompts for chain-of-thought extraction requests and replace them with structured thinking or progress surfaces — raw chain-of-thought is never returned, and asking for it trips the `reasoning_extraction` refusal category.

## Migration and API notes, effort and thinking

Fable 5 and Mythos 5 use adaptive thinking only; manual extended-thinking token budgets do not apply. Verify sampling-parameter and error behavior against the live API reference rather than assuming the Sonnet 5 rules carry over.

`effort` is the primary control for the intelligence/latency/cost trade-off. **`high` is the default**; use `xhigh` for the most capability-sensitive workloads and step down to `medium` or `low` for routine work. The docs state that lower effort settings on Fable 5 still exceed `xhigh` performance on prior models, so if a task comes out correct but slower or more deliberative than needed, drop effort before changing anything else. Set a large `max_tokens` at `high` and `xhigh`. See `references/50-effort-and-thinking.md`.

## Response length, tone, and progress updates

For elaboration at higher effort:
```
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

For checkpoint behavior in long workflows:
```
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

After a long tool-heavy run the final message is the user's first look at the work, and Fable 5 carries its working shorthand into it. Instruct it to re-ground: outcome first, complete sentences, no arrow chains or invented labels, project terms reintroduced, each file/commit/flag given its own plain-language clause.

## Prompting techniques that matter most

- **Prevent overplanning on ambiguous tasks:**

```
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

- **Ground progress claims** — the fix for fabricated status in long runs:

```
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

- **State the boundaries** — bound unrequested side actions:

```
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

- **Curb premature refactoring** — test whether default behavior is already better before adding this, and remove it if so:

```
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

- **Give the reason, not only the request:** `I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].`
- **Loosen prompts tuned for prior models.** Highly prescriptive scaffolding can degrade Fable 5; strip what default capability makes unnecessary. Evaluate at the top of your difficulty range — testing it on easy tasks undersells it and will not justify the price.

## Autonomous operation

For unattended pipelines, the full documented fragment:

```
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

Rarely, deep into a long session, Fable 5 ends on a text-only intent statement without issuing the tool call; a plain "continue" recovers it. Avoid surfacing raw remaining-context countdowns; if the harness must show them:

```
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

## Subagents

Fable 5 dispatches parallel subagents readily. Give explicit guidance and prefer asynchronous communication: `Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.`

Unlike Opus 5, self-verification here should be **explicit**, and separate fresh-context verifier subagents outperform self-critique: `Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.` For Claude Code's Agent tool and related runtime features, read `references/41-claude-code-runtime-features.md`.

## Memory system

Fable 5 performs well when it can record lessons from previous runs. Give it a location and these rules —

```
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

To bootstrap from existing history: `Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.`

## Send-to-user tool

Long asynchronous agents need a way to surface verbatim content without ending the turn:

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

Defining the tool is not enough; pair it with elicitation language. Add it only when the UX genuinely needs verbatim mid-task output — over-calling it defeats the purpose.

```
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

## Caveats

Pricing ($10/$50 per MTok), the 1M/128k limits, the January 2026 cutoff, the Opus 5 comparison figures, availability, safety-classifier behavior, and the documented fallback target are time-sensitive Anthropic-stated details — re-check the live docs before hard-coding them. The benchmark comparisons come from Anthropic's own Opus 5 announcement, not independent evaluation. The "no longer pinned by default" decision is this pack's policy driven by that cost comparison, not an Anthropic recommendation. This model postdates a typical training cutoff; every claim here came from a live fetch.

## Sources

- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Effort (parameter reference)](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)

## Companion reference

For Claude Code's shared agentic features, read `references/41-claude-code-runtime-features.md`. For the cross-model effort decision procedure, read `references/50-effort-and-thinking.md`. For whether Fable 5 is warranted at all, read `references/90-model-selection.md`.
