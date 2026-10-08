# Claude Code Runtime Features

Model/API capabilities do not establish harness support. This file owns Claude Code selection
and activation mechanics; the structured policy owns executable role pins. Refresh official
runtime documentation against the actual CLI version before depending on a feature.

## Current model, effort and identity resolution

Verified 25 September 2026 against model-config and sub-agents. Full API IDs pin versions;
family aliases roll and can resolve differently by provider, parent model or gateway.
Provider deployment mappings are separate runtime evidence, not aliases accepted by the policy.
The policy records sourced minimum versions for assigned profiles. Haiku 5.5 requires Claude Code 2.1.293; unlike its API disabled-thinking exception, Code prevents switching thinking off for it (verified 8 October 2026 against model-config). A newer installed CLI alone proves neither account entitlement nor activation.

For session selection, inspect explicit /model choice, startup --model, ANTHROPIC_MODEL,
settings and ANTHROPIC_DEFAULT_MODEL, plus managed allowlists and host overrides. /model can
persist a selection; inspection does not authorize changing settings or credit consent.

Since 2.1.251, subagent model precedence is invocation, definition frontmatter, subagent
model environment variable, then parent. Earlier versions prioritize that environment
variable. Since 2.1.257, CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 forces the subagent
model environment target, or the parent when no target is set. Forks and skills with
model: inherit retain documented exceptions; inspect them before claiming a pin won. Resolve inherit and family aliases on the target provider.
Allowlists may substitute a different model. Requested selection is not observed identity.

Frontmatter effort overrides session effort but remains subject to environment override,
model support and effective caps. Unsupported levels may step down. Opus 5.5's default differs
from older models, and legacy top-level user effortLevel has a documented exception; inspect
per-model settings and effective effort instead of extrapolating a saved value.

Record requested profile/model/effort and resolved controls separately from observed serving
model/effort. Use unknown where the host exposes no observation. Session/subagent status and
response modelUsage, when available, contribute evidence; an agent's self-description does
not prove identity. Runtime activation checks require authorized execution and must preserve
provider/account context, control evidence and any observed mismatch.

## Fallback and safeguards

Provider safety fallback and configured overload fallback are different events. Both can
change the serving model after selection. Preserve safeguards, disclose fallback/unknown
identity, and exclude affected runs from claims about the requested pair. Never weaken a
safeguard, silently substitute a model or introduce a local fallback to complete a gate.
Fable noninteractive use may spend credits without prompting; obtain the applicable execution
authority before a live comparison. No source checker grants installation, settings mutation
or paid execution authority.

## Historical harness mechanics

The remaining loop, workflow, scheduling and nesting details retain their original
24 July 2026 verification. The goal section has its own refresh date below. Historical
details are lookup leads, not current capability promises; re-fetch the named feature's
official page before use. Unverified limits receive no new date.

## `/loop` — recurring or self-paced interval execution

A bundled skill that re-runs a prompt inside the current session on Claude Code's session-scoped cron scheduler. What you supply determines the behavior:

| You provide | Behavior |
|---|---|
| Interval and prompt | Runs on a fixed cron schedule |
| Prompt only | Claude picks a delay between 1 minute and 1 hour after each iteration, based on what it observed, and prints the delay and its reason |
| Interval only, or nothing | Runs the built-in maintenance prompt, or your `loop.md` if one exists |

```text
/loop 5m check if the deployment finished and tell me what happened
```

Units are `s`, `m`, `h`, `d`; the interval can lead as a bare token or trail as a clause. Seconds round up to the nearest minute, and intervals that do not map to a clean cron step (`7m`, `90m`) round to one that does, with Claude reporting what it picked. A skill can be the prompt (`/loop 20m /review-pr 1234`), but a scheduled fire runs only skills Claude is allowed to invoke on its own — built-in commands, skills marked `disable-model-invocation: true`, skills withheld by settings, and MCP prompts arrive as plain text instead of executing.

Limits and behaviors worth knowing: minimum interval 1 minute; up to 50 scheduled tasks per session, each with an 8-character ID; recurring tasks expire 7 days after creation, firing once more and deleting themselves; tasks are session-scoped and restored on `--resume`/`--continue` only if unexpired; a fresh conversation clears them. The scheduler adds deterministic jitter — recurring tasks fire up to 30 minutes late, or up to half the interval for sub-hourly tasks, and one-shots scheduled for `:00` or `:30` fire up to 90 seconds early — so pick an off-round minute when exact timing matters. There is no catch-up for fires missed while Claude was busy. `Esc` stops a loop that is waiting; in self-paced mode Claude can also end it itself. `loop.md` lives at `.claude/loop.md` (project, takes precedence) or `~/.claude/loop.md` (user), is re-read each iteration, and is truncated beyond 25,000 bytes. Underlying tools: `CronCreate`, `CronList`, `CronDelete`; `CLAUDE_CODE_DISABLE_CRON=1` turns the whole scheduler off.

On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry, an interval-less prompt falls back to a fixed 10-minute schedule instead of self-pacing, `loop.md` is not read, and a bare `/loop` prints the usage message.

When the natural pattern is "watch a process and react" rather than "re-ask a question," the `Monitor` tool is usually the better instrument: it runs a background script and streams output lines back, avoiding polling entirely.

## Agent tool / subagents — foreground, background, and nested delegation

Delegates a task to a subagent with its own fresh context window, system prompt, restricted tools, and independent permissions. Built-ins: `Explore` (read-only codebase search, invoked with a thoroughness level of quick, medium, or very thorough), `Plan`, and `general-purpose`. `Explore` and `Plan` skip CLAUDE.md and the parent session's git status to stay fast and cheap; every other subagent loads both. `Explore` inherits the main conversation's model, capped at Opus on the Claude API — define a user or project subagent named `Explore` with `model: haiku` if you want exploration held on a cheaper model.

Custom subagents are Markdown files with YAML frontmatter under `.claude/agents/` (project, discovered by walking up to the repository root) or `~/.claude/agents/` (user), both scanned recursively; identity comes from the `name` field, not the path. Only `name` and `description` are required. Frontmatter of interest for orchestration prompts: `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`. `isolation: worktree` gives the subagent an isolated copy of the repository in a temporary git worktree, branched from your default branch rather than the parent's `HEAD`, and cleaned up automatically if the subagent changes nothing — this is the mechanism to reach for when lanes would otherwise contend on the same files.

Three separate caps govern subagent use, each with its own environment variable:

| Cap | Default | Variable |
|---|---|---|
| Nesting depth | Off — a subagent cannot spawn subagents | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` |
| Concurrent subagents | 20 running at once | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` |
| Total spawned per session | 200 | `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` |

Nesting being off by default is the item most likely to break a carried-forward orchestration prompt: while nesting is off, the `Agent` tool is withheld from every subagent except a fork, so a lane instructed to delegate will quietly do the work itself and return one summary. If your lane design depends on a second layer, set the depth variable explicitly and say so in the prompt. Sessions with ultracode active are exempt from the concurrency cap.

Subagents run in the background by default; Claude runs one in the foreground when it needs the result before continuing. Background subagents surface permission prompts in your main session, naming the asking subagent, and their results reach Claude as a completion notification in a later turn. `/subtask` starts a fork — a subagent that inherits the full conversation instead of starting fresh — which is the right shape for trying several approaches from the same starting point. `/fork` now copies the whole session into a separate background session instead.

For current model and effort precedence, read the current-resolution section above. The historical environment-first order must not be applied to newer CLIs. Refresh thinking inheritance against the actual runtime; model/API thinking controls are not per-agent settings by inference.

```text
Explicit authorization: you may use subagents, and you may run independent lanes of this task in parallel or
in the background, without asking again. Research the authentication, database, and API modules in parallel
using separate subagents, then summarize the risk each one found before you touch any code.
```

This wording requires current host delegation authority — before reusing it on current Opus or Fable, read `references/06-invocation-and-composition.md` for the delegation-polarity rule those models need instead.

## Workflow tool — deterministic multi-agent orchestration scripts

A dynamic workflow is a JavaScript script that orchestrates subagents at scale. Claude writes the script for the task you describe, and a separate runtime executes it in the background while your session stays responsive. Control flow — loops, branching, fan-out, fan-in — is plain deterministic code; only the `agent(...)` calls inside it are model-powered, and `pipeline(...)` runs one agent per item in a list. Intermediate results stay in script variables rather than in Claude's context, which is what lets a run scale to hundreds of agents without flooding the conversation. The script for every run is written under your session's directory in `~/.claude/projects/`, so you can read, diff, or edit it.

This is the right instrument when a job outgrows a handful of subagents, or when findings need verifying against each other: a codebase-wide audit, a 500-file migration, adversarial cross-checking, a judge panel over several drafted approaches. `/deep-research` ships as a bundled workflow and runs only when you invoke it.

```text
ultracode: sweep the entire codebase for SQL injection risk in raw query builders, cross-check each finding
with a second independent agent, and report only confirmed issues.
```

Include `ultracode` anywhere in a prompt, or ask in your own words ("use a workflow"), for a one-off workflow without changing session effort. `/effort ultracode` makes Claude plan a workflow automatically for every substantive task in the session; it combines `xhigh` effort with automatic orchestration, applies to the current session only, and is a Claude Code setting rather than a model effort level. The keyword is an opt-in only from human-typed input — it does not fire from a `-p` prompt, an unstamped SDK prompt, a scheduled-task prompt, or a relayed webhook or PR comment. Manage runs with `/workflows`, and press `s` there to save a run's script as a reusable `/<name>` command in `.claude/workflows/` (project) or `~/.claude/workflows/` (personal); saved workflows accept input through an `args` global.

Runtime constraints: no mid-run user input (only agent permission prompts pause a run); no direct filesystem or shell access from the script itself, since agents do the work and the script coordinates; up to **16 concurrent agents**, fewer on machines with limited CPU cores; **1,000 agents total per run**. The subagents a workflow spawns always run in `acceptEdits` mode and inherit your tool allowlist regardless of the session's permission mode, so pre-approve the commands the agents will need before a long run. A run is resumable within the same session — completed agents return cached results — but exiting Claude Code loses the progress.

Cost controls worth naming in a generated prompt: the Dynamic workflow size setting in `/config` sends Claude an advisory agent-count target (`small` fewer than 5, `medium` fewer than 15, `large` fewer than 50, `unrestricted` by default), and Claude Code flags a run that schedules more than 25 agents or projects past 1.5 million tokens with a `Large workflow` warning — advisory only, and suppressed when ultracode is on. Workflows can be turned off entirely with `disableWorkflows` in settings or `CLAUDE_CODE_DISABLE_WORKFLOWS=1`, which also removes `ultracode` from the `/effort` menu.

## Plan mode / Ultraplan — structured checkpoint before autonomous work

Plan mode lets Claude read and explore but not edit; it produces a plan you explicitly approve before any change happens. Enter it with `Shift+Tab` (the CLI cycles `default` → `acceptEdits` → `plan`), by prefixing a single prompt with `/plan`, or with `claude --permission-mode plan`. Shell commands outside the built-in read-only set still prompt during planning. The approval dialog offers approve-with-auto-mode, approve-with-manual-edits, refine with Ultraplan, or keep planning; `Ctrl+G` opens the plan in your editor first. Approving switches the session into the permission mode the chosen option describes. Note the mode names when generating prompts: the CLI labels `default` as **Manual** and accepts `manual` as an alias, and the full set is `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`.

Ultraplan hands the planning task to a Claude Code on the web session running in plan mode: Claude drafts the plan in the cloud while your terminal stays free, and you review it in the browser with inline comments on individual sections, emoji reactions, and an outline sidebar.

```text
/ultraplan migrate the auth service from sessions to JWTs
```

Three launch paths: the `/ultraplan` command, the bare keyword `ultraplan` in a prompt, or choosing "refine with Ultraplan" from a local plan's approval dialog. Status shows in the CLI prompt input (`◇ ultraplan`, `◇ ultraplan needs your input`, `◆ ultraplan ready`), and `/tasks` opens a detail view with the session link and a stop action. When the plan is ready you either approve it to execute in the same cloud session and open a pull request, or teleport it back to the terminal, where you choose **Implement here**, **Start new session**, or **Cancel** (which saves the plan to a file and prints the path). Ultraplan is in research preview, requires a Claude Code on the web account and a GitHub repository, and is unavailable on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. `/ultrareview` is its review-side counterpart.

Plan mode is the closest thing to a launch gate for a large or risky autonomous run — it composes with `/goal` (condition-based continuation) and `/loop` (interval-based continuation) for the multi-turn autonomy that follows approval.

## `/goal` — condition-based multi-turn autonomy (Claude Code's own mechanism)

Verified 4 October 2026 against the official goal, desktop and skills pages. Claude Code's `/goal <condition>` starts execution immediately and evaluates the condition after each turn using the transcript. Its evaluator returns **Not yet met** (continue with its reason), **Met** (clear as achieved), or **Impossible** (stop without achievement). One goal is active per session; a new one replaces it. These are evaluator verdicts, not evidence that repository gates passed.

Codex's `/goal` instead runs a durable thread-scoped objective loop with its own budget accounting, not a Stop-hook evaluator — the two differ in what proves completion, how they're enabled, and what they cost. Never carry a `/goal` block between the runtimes unedited; read `references/11-codex-runtime-features.md` for Codex's mechanism.

The condition limit is **4,000 characters**, excluding the leading command. The evaluator calls no tools and reads no files; the executing session must surface acceptance evidence and check outcomes in the transcript. A saved report's path alone cannot prove its contents. Composition, the soft authoring target, examples and stop clauses belong to `references/06-invocation-and-composition.md`; do not put an operating manual in the condition.

Measure the final text actually sent, after substitutions. `scripts/check_goal_condition.py` checks a declared surface and counts conservatively in UTF-16 code units against this dated cap. The documentation does not specify Unicode counting semantics; this assumption avoids undercounting astral characters relative to code points. A static pass is neither parser parity nor live Desktop acceptance, and a runtime rejection remains authoritative.

Bare `/goal` reports status and `/goal clear` ends it early. Other aliases, resume accounting and noninteractive flags retain their historical verification; re-fetch the goal page before generating those commands.

A goal preserves the current permission mode; it grants no installation, commit, deployment or other side-effect authority. Workspace trust must be accepted, and `/goal` is unavailable when `disableAllHooks` is set at any level or `allowManagedHooksOnly` is set in managed settings. Report the restriction; never change trust, hooks or permissions to make a prompt run without authorization.

### Surface preflight and rejected commands

Claude Desktop's **Code tab** is the documented desktop Claude Code surface. Do not infer Chat or Cowork command support from the app name; their `/goal` support is not established by these sources. Resolve the actual surface, installed runtime version, registered skill command, goal availability and relevant trust/hook restrictions before issuing a runnable kickoff. Inspection does not authorize installation or settings changes.

The user observed this Code-tab rejection on 4 October 2026 (Desktop version unprovided):

> A command takes file @-mentions but no other @-mentions, slash commands, links, or inline formatting, so nothing was sent. Remove them.

This is Desktop composer evidence, not an officially documented universal CLI grammar. It applies to **command arguments**, including a skill-led kickoff: use one leading registered command and plain arguments without secondary slash commands, non-file @mentions, links, backticks, bold or other inline formatting. Name companion skills without sigils and use plain paths. Generate the goal condition as plain text with no skill activation or file references by default; keep them in the kickoff or plan. The diagnostic permits file @mentions, but generated text cannot manufacture or validate their composer chips. A static text pass proves no structured-composer acceptance.

For a rejection, record the supplied prompt, error, app/runtime version and tab; obtain only missing facts needed for diagnosis. Check composer tokens and rendered length, then classify command/surface availability, skill resolution, trust/hooks or remaining unknowns. Without the rejected payload, repair established defects but do not claim reproduction, a parser/cap change or incident closure. Provide a verified plain kickoff or report missing capability; never guess a fallback on another surface.

## Choosing between `/loop`, `/goal`, subagents, workflows, and the rest

- **`/loop`** — recurring check-ins on an interval, or "keep tending this" maintenance. Use when the natural cadence is time-based. For watching a process rather than re-asking a question, prefer the `Monitor` tool.
- **`/goal`** — "don't stop until this condition is true," evaluated after every turn without re-prompting. Use when the cadence is condition-based, and only when the condition is demonstrable from the transcript.
- **Subagents** — independent lanes inside one session, each with a fresh context, reporting back to the conversation that spawned them. Use when the task decomposes into disjoint pieces and only the results matter. Add `isolation: worktree` when lanes would otherwise touch the same files.
- **Workflow tool** — deterministic, scriptable orchestration across many agents, with adversarial cross-checking, judge panels, or loop-until-dry patterns. Use for the highest-stakes or highest-scale fan-out, where the control flow itself must be reliable and reviewable, and where the orchestration is worth saving and rerunning.
- **Agent teams** — multiple coordinated sessions with a shared task list and direct teammate-to-teammate messaging, managed by a lead. Use when the workers need to talk to each other rather than only report back. Experimental and disabled by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), materially more expensive than subagents, no worktree isolation, and no nested teams.
- **Agent view** (`claude agents`) — one screen to dispatch and monitor independent sessions running in the background, each in its own worktree. Research preview. Use when you want to hand tasks off and step in only when one needs you.
- **`/batch`** — a bundled skill that splits one large change into 5 to 30 worktree-isolated subagents, each opening a pull request. A packaged use of subagents and worktrees, not a separate coordination style.

These compose: a workflow's `agent()` calls are themselves subagents; a `/goal` can supervise a session that also uses `/loop` for periodic status checks; a plan approved via `/ultraplan` is often what a subsequent `/goal` or `/loop` then executes toward. For durable multi-phase work that outgrows any single one of them, route to `/alaa-workflow`.

## Caveats

Goal condition, evaluator, permissions, restrictions and Desktop Code guidance refreshed 4 October 2026. No live Desktop command was exercised and no parser/cap change is established. Other historical harness sections retain their 24 July 2026 verification. Re-check every version gate and exact limit before use: dynamic workflow concurrency and total caps, `ultracode`, nesting and subagent caps, workflow warnings, and loop limits are especially volatile.

Ultraplan is documented as a research preview with no stated minimum version; do not carry forward a version gate for it. Current alias and selection rules are in the current-resolution section above; historical defaults are not activation evidence. A chosen autonomous permission mode has separate account, model and provider requirements; a goal prompt cannot enable it.

## Sources

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Run prompts on a schedule (`/loop`)](https://code.claude.com/docs/en/scheduled-tasks)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Run agents in parallel](https://code.claude.com/docs/en/agents)
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Plan in the cloud with ultraplan](https://code.claude.com/docs/en/ultraplan)
- [Keep Claude working toward a goal (`/goal`)](https://code.claude.com/docs/en/goal)
- [Claude Code on desktop](https://code.claude.com/docs/en/desktop)
- [Model configuration](https://code.claude.com/docs/en/model-config)

- [Model configuration](https://code.claude.com/docs/en/model-config)

## Managed direct-selection profiles

The runtime orchestrator renders standalone implementation and planner variants from one editable contract per role family. `scripts/render_agents.py --write` supplies pins only from this skill's canonical policy; `--check` rejects drift. Select the exact registered variant, not a caller effort override that custom metadata ignores. Planning inline requires verified compatible configured controls; a planner draft remains advisory and the parent owns the durable plan. Subagent YAML model and effort realize the selected pair; environment settings and effort caps may override them. No per-call Agent effort override is assumed without current supported-interface evidence. Static agreement proves source configuration, not runtime identity or model obedience.
