# Claude Code Runtime Features (shared by Opus 4.8, Sonnet 5, and Fable 5)

These are harness-level features of Claude Code itself, not model APIs — they work the same way regardless of which of the three Claude models is powering the session, because the orchestration logic (scheduler, subagent spawner, workflow runtime, plan-mode gate) lives in Claude Code, not in the model weights. One exception: automatic per-turn workflow orchestration ("ultracode" mode) requires a model that supports `xhigh` effort (Opus 4.7+/4.8, Fable 5) — on models without `xhigh` the `/effort` menu simply omits that option, though manually requesting a workflow still works on any model. Read the matching model file (`20-opus-4-8.md`, `30-sonnet-5.md`, or `40-fable-5.md`) for model-level tuning before writing a feature prompt from this file.

## `/loop` — recurring or self-paced interval execution

A bundled, prompt-based skill that re-runs a prompt inside the current session on Claude Code's session-scoped cron scheduler. Give an interval and it fires on that cadence (Claude converts it to a cron expression; odd intervals round to the nearest clean step). Omit the interval and it self-paces: after each iteration Claude picks a 1-minute-to-1-hour delay based on what it observed (short waits while something is running, long waits when idle). Omit the prompt entirely and it runs a built-in maintenance prompt, or a project `.claude/loop.md` / user `~/.claude/loop.md` default if one exists.

```text
/loop 5m check if the deployment finished and tell me what happened
```

Limits worth knowing: minimum interval is 1 minute; up to 50 scheduled tasks per session; recurring tasks auto-expire after 7 days; tasks are session-scoped (restored on `--resume`/`--continue` if not expired); on Bedrock/Vertex/Foundry an interval-less prompt falls back to a fixed 10-minute schedule instead of dynamic self-pacing and `loop.md` is not read there.

## Agent tool / subagents — foreground, background, and nested delegation

Delegates a task to a subagent with its own fresh context, system prompt, restricted tools, and independent permissions. Built-in: `Explore` (fast, Haiku-powered read-only search), `Plan`, `general-purpose`. Custom subagents live as Markdown files under `.claude/agents/` (project) or `~/.claude/agents/` (user). Subagents run in the foreground (blocking, permission prompts pass through to you) or background (concurrent, permission prompts surface in your main session naming the subagent); Claude picks based on the task, or you can explicitly say "run this in the background." A subagent can itself spawn nested subagents up to a fixed depth of 5. `/fork` spawns a background subagent that inherits the full conversation history instead of starting fresh — useful for trying several approaches in parallel from the same starting point.

```text
Explicit authorization: you may use subagents, and you may run independent lanes of this task in parallel or
in the background, without asking again. Research the authentication, database, and API modules in parallel
using separate subagents, then summarize the risk each one found before you touch any code.
```

Model per subagent resolves in this order: `CLAUDE_CODE_SUBAGENT_MODEL` env var > per-invocation model param > subagent frontmatter `model` > the main conversation's model — so a Sonnet-5-driven session gets Sonnet-5-powered subagents by default (except `Explore`, which defaults to Haiku).

## Workflow tool — deterministic multi-agent orchestration scripts

A dynamic workflow is a JavaScript script (written by Claude, or authored/edited by you) that a separate runtime executes in the background while your session stays responsive. Control flow (loops, branching, fan-out/fan-in) is plain deterministic code; only the individual `agent(...)` calls inside it are model-powered, so a run can scale to hundreds of agents without flooding the conversation. This is the right tool for patterns like independent agents adversarially cross-checking each other's findings, or a judge panel scoring several drafted approaches.

```text
ultracode: sweep the entire codebase for SQL injection risk in raw query builders, cross-check each finding
with a second independent agent, and report only confirmed issues.
```

Include the keyword `ultracode` anywhere in a prompt (or ask in your own words, "use a workflow") for a one-off workflow without changing session effort; `/effort ultracode` (requires an `xhigh`-capable model) makes Claude plan a workflow automatically for every substantive task in the session. Watch/manage runs with `/workflows`. Hard limits: no mid-run user input (only agent permission prompts pause a run), up to 16 concurrent agents, 1,000 agents total per run.

## Plan mode / Ultraplan — structured checkpoint before autonomous work

Plan mode lets Claude read and reason but not edit or run mutating commands; it produces a plan you explicitly approve before any change happens. Ultraplan extends this to the cloud — drafts the plan on Claude Code on the web (freeing your local terminal), gives you a browser review surface with inline comments, and lets you execute on the web (opens a PR) or "teleport" the approved plan back to your local terminal.

```text
/ultraplan migrate the auth service from sessions to JWTs
```

Local plan mode: `Shift+Tab` to cycle permission modes, or prefix a prompt with `/plan`. This is the closest thing to a launch gate for a large or risky autonomous run — it composes with `/goal` (condition-based continuation) and `/loop` (interval-based continuation) for the actual multi-turn autonomy after the plan is approved.

## `/goal` — condition-based multi-turn autonomy (Claude Code's own mechanism)

**Not the same mechanism as Codex's `/goal`** (see `references/11-codex-runtime-features.md`) — same name, different implementation. Claude Code's `/goal` sets a natural-language completion condition (up to 4,000 characters) as a session-scoped Stop hook: after every turn, the condition plus the conversation so far go to a small fast evaluator model (defaults to Haiku, no tool calls, judges only what's already in the transcript), which returns yes/no plus a short reason. On "no," Claude automatically starts another turn using that reason as guidance — no re-prompting needed. Only one goal is active per session; setting a new one replaces the old one and immediately starts a turn using the condition as the directive.

```text
/goal migrate every call site off the deprecated `useLegacyAuth` composable to `useAuth`, all TypeScript
compiles clean, and the full test suite passes, or stop after 25 turns
```

Bare `/goal` checks status (condition, elapsed time, turns evaluated, token spend, latest evaluator reason); `/goal clear` (aliases: `stop`, `off`, `reset`, `none`, `cancel`) removes it early. Since the evaluator only judges what's in the transcript, always include an explicit turn or time bound in the condition itself for long-running goals.

## Choosing between `/loop`, `/goal`, Agent subagents, and the Workflow tool

- **`/loop`** — recurring check-ins on an interval, or "keep tending this" maintenance work. Use when the natural cadence is time-based.
- **`/goal`** — "don't stop until this condition is true," evaluated after every turn without you re-prompting. Use when the natural cadence is condition-based, not time-based.
- **Agent subagents** — independent lanes that can run concurrently, each with its own fresh context. Use when the task decomposes into disjoint pieces of work.
- **Workflow tool** — deterministic, scriptable orchestration across many agents, with adversarial cross-checking, judge panels, or loop-until-dry patterns. Use for the highest-stakes or highest-scale fan-out, where the control flow itself needs to be reliable and reviewable, not just the individual agent calls.

These compose: a Workflow's individual `agent()` calls are themselves subagents; a `/goal` can supervise a session that also uses `/loop` for periodic status checks; a plan approved via `/ultraplan` is often what a subsequent `/goal` or `/loop` then executes toward.

## Caveats

Version gates and hard limits documented above (Claude Code v2.1.139+ for `/goal`, v2.1.154+ for Workflow, v2.1.91+ for Ultraplan, subagent nesting fixed at 5 levels, 50 scheduled tasks per session, etc.) are time-sensitive — re-check `code.claude.com/docs` before depending on an exact version or limit. `/goal` requires the workspace trust dialog to have been accepted and is unavailable when hooks are disabled at the settings level.

## Sources

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Run prompts on a schedule (/loop)](https://code.claude.com/docs/en/scheduled-tasks)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Plan in the cloud with ultraplan](https://code.claude.com/docs/en/ultraplan)
- [Keep Claude working toward a goal (/goal)](https://code.claude.com/docs/en/goal)
