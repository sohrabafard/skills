# Claude Fable 5

**Correct the obvious assumption first: Fable 5 is not a creative-writing or persona model.** It is Anthropic's new top-tier flagship, positioned *above* Claude Opus 4.8 — per the official models overview: "For workloads that need the highest available capability, see Claude Fable 5." It is built for the hardest, longest-running, most ambiguous problems: multi-day autonomous agentic runs, complex coding migrations and large refactors, deep enterprise knowledge work, and heavy vision/document analysis. Opus 4.8 remains "most capable Opus-tier model," Sonnet 5 remains "the best combination of speed and intelligence" — Fable 5 sits a full capability tier above both, at a steep price premium (documented at $10/$50 per MTok versus Opus 4.8's $5/$25 and Sonnet 5's $3/$15).

A sibling model, Mythos 5, shares Fable's underlying capability but without Fable's safety classifiers (which can decline certain offensive-cybersecurity, biology/life-sciences, and reasoning-extraction requests); Mythos 5 is limited-availability, invitation-only. This skill's guidance is for Fable 5.

Compared with Opus 4.8, documented improvements include: long-horizon autonomy (multi-day goal-directed runs), first-shot correctness on complex well-specified problems, vision (dense technical images/screenshots), enterprise workflows (financial analysis, spreadsheets, slides, docs), code review/debugging recall outside cybersecurity, navigating ambiguity, and more dependable dispatch/sustaining of parallel subagents. Reach for Fable 5 when the task is genuinely at the edge of what Opus 4.8 can reliably do, or when the run needs to sustain itself autonomously for many hours — not as a default upgrade for routine work (see `references/90-model-selection.md`).

## Effort and thinking

Fable 5 (and Mythos 5) use **adaptive thinking exclusively** — it is the only thinking mode, always on when `thinking` is unset, and `thinking: {type: "disabled"}` is not supported. Traditional token-budget thinking does not apply; depth and cost are controlled entirely by `effort` (low/medium/high/xhigh), described as the primary trade-off control for intelligence, latency, and cost. The raw chain-of-thought is never returned; `thinking.display` is `"summarized"` or `"omitted"` (default). Recommended default is `high` effort for most tasks, `xhigh` reserved for the most capability-sensitive workloads — lower effort on Fable 5 often still exceeds `xhigh` performance on prior models, so do not reflexively max out effort. Individual hard-task requests can run many minutes at higher effort, and autonomous runs can extend for hours — adjust client timeouts, streaming, and progress UX accordingly before migrating a harness from Opus 4.8.

## Prompting techniques that matter most

- **Prevent overplanning/over-narration**: tell it explicitly to act once it has enough information, rather than re-deriving established facts or narrating options it won't pursue outside thinking blocks.
- **Curb unrequested tidying**: at high effort it can over-scope — add an explicit anti-scope-creep instruction (no refactors/abstractions/error-handling beyond what was asked, no designing for hypothetical future needs, no compatibility shims when the code can just be changed).
- **Steer verbosity with one brevity instruction, not a list**: "lead with the outcome in the first sentence" is enough on its own — Fable 5's strong instruction-following makes one short instruction as effective as many.
- **Define checkpoint/pause behavior explicitly**: pause only for destructive/irreversible actions, real scope changes, or user-only input; otherwise proceed, and never end a turn on an unfulfilled promise ("I'll now run X" with no accompanying tool call).
- **Ground long-run progress claims**: instruct it to audit every progress claim against an actual tool result from the session before reporting, and to state plainly — not hedge — when something is unverified, failed, or skipped. Anthropic found this nearly eliminated fabricated status reports in testing.
- **Bound unrequested side actions**: it can occasionally take actions nobody asked for (drafting an email, creating a defensive git backup) — instruct it to stay assessment-only when the user is thinking out loud, and to verify evidence actually supports a state-changing command before running it.
- **Delegate to subagents proactively**: Fable 5 dispatches subagents more readily and reliably than prior models — give explicit delegation guidance, prefer async orchestration over blocking, and keep long-lived subagents with persistent context to save time/cost via cache reads.
- **Build an explicit cross-session memory system**: give it a place (e.g. a notes file) to record one lesson per entry with a one-line summary, capture both corrections and confirmed approaches, avoid duplicating what the repo/chat already records, and delete disproven notes.
- **State intent, not just the request** — Fable 5 uses stated reasoning to connect a task to relevant context rather than inferring intent alone, which matters most for long-running multi-workstream agents.
- **Never ask it to echo or explain its internal chain-of-thought as response text** — this can trigger a `reasoning_extraction` refusal and elevate fallback to Opus 4.8. Use the structured `thinking` block or an explicit send-to-user tool for visibility instead.
- **When migrating prompts/skills tuned for older models, loosen them**: highly prescriptive instructions written for prior models can degrade Fable 5's output; it also adapts skill guidance on the fly based on what it learns mid-task.
- **For unattended/asynchronous pipelines**: add a system reminder that the user cannot answer mid-task questions and that it should proceed on reversible actions without asking, and should not end a turn on a plan/question/promise without having done the work.
- **In very long sessions, do not surface a raw remaining-context countdown** to the model — if unavoidable, add reassurance language that ample context remains, so it doesn't prematurely suggest a new session or trim its own work.
- **For long verification-heavy tasks, prefer separate fresh-context verifier subagents over self-critique**: e.g. "establish a method for checking your own work at an interval of [X], verifying it with subagents against the specification."

## Ready-to-use autonomy fragment

```text
You are operating autonomously; the user is not watching in real time and cannot answer mid-task questions.
Proceed on reversible actions without asking. Pause only for destructive/irreversible actions, a real scope
change, or input only the user can provide. Before reporting any progress claim, verify it against an actual
tool result from this session - state plainly, not hedged, when something is unverified, failed, or skipped.
End your turn only when the task is complete or genuinely blocked - never on an unfulfilled "I'll now do X."
```

## Tone

Not separately documented as a distinct persona/tone profile — there is no roleplay or creative-writing framing anywhere in the official docs. The one documented tendency is a bias toward being thorough/elaborative when un-steered (surveying options it won't pursue, long root-cause explanations, heavily structured PR descriptions), especially at higher effort. Steer this with the explicit brevity and "write for a reader who wasn't there" instructions above, not with a persona instruction.

## Caveats

Public documentation for Fable 5 is not sparse — this file is built from multiple official, cross-linked, directly-fetched Anthropic pages, all internally consistent (matching model IDs, pricing, dates, cross-references). "Project Glasswing" and the exact Mythos 5 classifier behavior could not be independently corroborated beyond what the docs themselves state. This model postdates a typical training cutoff; treat every claim here as sourced from a live fetch, not memory, and re-verify before hard-coding pricing or capability claims elsewhere.

## Sources

- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Claude Fable — Anthropic](https://www.anthropic.com/claude/fable)

## Companion reference

For Claude Code's shared agentic features (`/loop`, Agent subagents, Workflow tool, plan mode / Ultraplan, Claude Code's own `/goal`), read `references/41-claude-code-runtime-features.md` next.
