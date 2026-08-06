# Claude Code Runtime Features (shared by Opus 5, Sonnet 5, and Fable 5)

These are harness-level features of Claude Code itself, not model APIs. They work the same way regardless of which Claude model powers the session, because the orchestration logic — scheduler, subagent spawner, workflow runtime, plan-mode gate, goal evaluator — lives in Claude Code, not in the model weights. The one place the model matters is the effort ladder that some features sit on, and all three in-scope models now support the full ladder (`low`, `medium`, `high`, `xhigh`, `max`), so ultracode's automatic workflow orchestration is available on all three. Default effort is `high` on every model that supports effort. Read the matching model file (`references/20-opus-5.md`, `references/30-sonnet-5.md`, `references/40-fable-5.md`) for model-level tuning before writing a feature prompt from this file.

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

Model resolution order for a subagent: `CLAUDE_CODE_SUBAGENT_MODEL` (when set to a model alias or ID), then the per-invocation `model` parameter, then the definition's `model` frontmatter, then the main conversation's model. Setting the environment variable to `inherit` is equivalent to leaving it unset. Subagents also inherit the main conversation's extended-thinking configuration; there is no per-subagent thinking setting.

```text
Explicit authorization: you may use subagents, and you may run independent lanes of this task in parallel or
in the background, without asking again. Research the authentication, database, and API modules in parallel
using separate subagents, then summarize the risk each one found before you touch any code.
```

This wording is authored for Codex's reticent bias — before reusing it on Opus 5 or Fable 5, read `references/06-invocation-and-composition.md` for the delegation-polarity rule those models need instead.

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

**Not the same mechanism as Codex's `/goal`** — same name, different implementation. Claude Code's `/goal` is a wrapper around a session-scoped prompt-based Stop hook: after every turn, the condition plus the conversation so far go to your configured small fast model (defaults to Haiku), which returns a yes/no decision plus a short reason. On "no," Claude starts another turn using that reason as guidance; on "yes," the goal clears and records an achieved entry. Setting a goal immediately starts a turn with the condition as the directive. One goal is active per session; a new one replaces it. Requires Claude Code v2.1.139 or later.

Codex's `/goal` instead runs a durable thread-scoped objective loop with its own budget accounting, not a Stop-hook evaluator — the two differ in what proves completion, how they're enabled, and what they cost. Never carry a `/goal` block between the runtimes unedited; read `references/11-codex-runtime-features.md` for Codex's mechanism.

```text
/goal migrate every call site off the deprecated `useLegacyAuth` composable to `useAuth`, all TypeScript
compiles clean, and the full test suite passes, or stop after 25 turns
```

The condition can be up to **4,000 characters**. The evaluator calls no tools and reads no files — it judges only what Claude has surfaced in the transcript — so write the condition as something the session's own output demonstrates, name the check explicitly (`npm test` exits 0, `git status` is clean), and include a turn or time clause, since the evaluator can only judge a bound that is stated in the condition itself.

Bare `/goal` shows status: the condition, elapsed time, turns evaluated, token spend, and the evaluator's latest reason. `/goal clear` removes it early (aliases `stop`, `off`, `reset`, `none`, `cancel`), and `/clear` also removes it. An active goal is restored on `--resume`/`--continue`, but the turn count, timer, and token baseline reset. It works in non-interactive mode (`claude -p "/goal …"` runs the loop to completion in one invocation; add `--output-format stream-json --verbose` or nothing prints until it finishes), in the desktop app, and through Remote Control.

A goal does **not** change permissions. In the default mode Claude still asks before tool calls your settings do not already allow, so an unattended goal run needs auto mode alongside it. `/goal` requires an accepted workspace trust dialog and is unavailable when `disableAllHooks` is set at any settings level or `allowManagedHooksOnly` is set in managed settings; in each case the command says why.

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

Verified against live documentation on 24 July 2026. Every version gate and hard limit above is time-sensitive and several changed within the current release line — re-check `code.claude.com/docs` before depending on an exact number. Specifically volatile: `/goal` at v2.1.139+ and its 4,000-character cap; dynamic workflows at v2.1.154+ with 16 concurrent and 1,000 total agents; `/effort ultracode` at v2.1.203+; the subagent caps (nesting off by default, 20 concurrent from v2.1.217, 200 per session from v2.1.212); the workflow size guideline at v2.1.202+ and the large-run warning thresholds at v2.1.203+; and the `/loop` figures (1-minute minimum, 50 tasks, 7-day expiry, 25,000-byte `loop.md`).

Ultraplan is documented as a research preview with no stated minimum version; do not carry forward a version gate for it. Model aliases resolve differently per provider — `opus` resolves to Opus 5 on the Anthropic API but to older versions on some others, and Opus 5 itself requires Claude Code v2.1.219 or later — so a generated prompt that assumes a model from an alias is unsafe across providers. Auto mode, which unattended `/goal` and workflow runs generally need, has its own plan, owner, model, and provider requirements.

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
- [Model configuration](https://code.claude.com/docs/en/model-config)
