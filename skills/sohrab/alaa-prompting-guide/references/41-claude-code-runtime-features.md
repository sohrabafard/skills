# Claude Code Runtime Features

This file owns Claude Code selection and activation mechanics. A model or API capability establishes no harness support: before you depend on a feature, refresh its official page against the actual CLI version.

## Model, effort and identity resolution

**IDs and aliases** (model-config and sub-agents, 25 September 2026). A full API ID pins a version. A family alias rolls, and it can resolve differently by provider, parent model or gateway; resolve `inherit` and family aliases on the target provider. A provider deployment mapping is separate runtime evidence, and the policy does not accept it as an alias. An allowlist can substitute a different model, so a requested selection is not an observed identity. For a model's minimum Claude Code version, alias behaviour, default effort per surface and thinking control in Code, read that model's reference. A newer installed CLI alone proves neither account entitlement nor activation.

**Session model** (25 September 2026). Inspect an explicit `/model` choice, the startup `--model` flag, `ANTHROPIC_MODEL`, settings and `ANTHROPIC_DEFAULT_MODEL`, managed allowlists, and host overrides. `/model` can persist a selection. Inspection authorizes neither a settings change nor credit consent.

**Subagent model precedence** (25 September 2026).

- Since 2.1.251: the invocation, then the definition frontmatter, then the subagent model environment variable, then the parent. Earlier versions give the environment variable priority; never apply that order to a newer CLI.
- Since 2.1.257: `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` forces the model that the environment variable targets, or the parent model when the variable sets no target.
- Forks and skills with `model: inherit` keep documented exceptions; inspect them before you claim that a pin won.
- A nested subagent with no model runs on its parent subagent's model, not on the main conversation's model (14 November 2026).

**The Agent tool's `model` parameter** (sub-agents and the active tool schema, 14 November 2026) accepts a family alias only: `sonnet`, `opus`, `haiku`, `fable`. It accepts no full ID and no `inherit`. To realize a selected full ID at dispatch, pass its family alias and verify that the alias resolves to that ID on the target provider. When it does not, the definition's `model` field is the only pin, and the lane of a managed model-neutral role is blocked.

**Effort.**

- Since 2.1.292 an effort given at a non-fork invocation overrides the frontmatter effort and the session effort, and it persists on resume (9 October 2026).
- With neither an effort field nor an effort parameter, a subagent on the main model uses the session level; on a different model that level does not apply (14 November 2026).
- `CLAUDE_CODE_EFFORT_LEVEL` supersedes the invocation and the frontmatter. Model support and effective caps can step an unsupported level down.
- Managed roles omit model and effort, so on that verified surface the dispatch provides BOTH controls explicitly. Inspect how force settings, environment variables, hooks and the provider resolve them; omitted pins alone prove neither pair.
- On an older, forked or unsupported surface, use an available exact verified realization or block the affected lane. Never treat inheritance as selection. Main-session configuration stays external.
- A model or API thinking control is no per-agent setting by inference. Refresh thinking inheritance against the actual runtime.

**Workflow `agent()`** ([workflows](https://code.claude.com/docs/en/workflows), 14 November 2026) takes its model in the same order as a subagent. A model the script names counts as the per-invocation model; when nothing assigns one, the agent runs on the session's model. The page names no effort option for `agent()`.

**Identity.** Report identity through `references/80-subagent-authoring.md` *Configuration and observed identity*, and record the resolved controls too. Session status, subagent status and the response's `modelUsage` are evidence when available; an agent's self-description is not. A runtime activation check needs authorized execution, and it preserves the provider and account context, the control evidence and any observed mismatch.

## Fallback and safeguards

- A provider safety fallback and a configured overload fallback are different events. Either can change the serving model after selection.
- Preserve safeguards. Disclose a fallback or an unknown identity, and exclude the affected runs from claims about the requested pair.
- Never weaken a safeguard, silently substitute a model or introduce a local fallback to complete a gate.
- Noninteractive Fable use can spend credits without a prompt; get the applicable execution authority before a live run. No source checker grants authority to install, to change settings or to pay for execution.

## Native Advisor

Use Claude Code's native Advisor for executor consultations. The orchestrator's read-only Advisor mode is a separate role.

**Start.** Use `/advisor <model>` in a supported Code session. At launch, `--advisor <model>` overrides the `advisorModel` setting. Give a supported `sonnet`, `opus` or `fable` alias or a full model ID.

**Preflight.** The advisor is experimental and needs the Anthropic API or Claude Platform on AWS (14 November 2026). Before you depend on it, resolve the alias and verify support on the actual Code version, provider, account, managed allowlist and entitlement. Inspection grants neither configuration authority nor paid execution authority.

**Pairs.** Claude Code ranks models for the advisor role and accepts only the pairs in its table. These are its rows for the active set; verify the exact resolved pair on the target surface.

| Main model | Accepted advisors |
|---|---|
| Haiku 5.5 | Fable, Opus 4.7 or later, Sonnet 5 or later, Haiku 5.5 |
| Sonnet 5.5 | Fable, Opus 5 or later, Sonnet 5.5 |
| Opus 5.5 | Fable, Opus 5 or later |
| Fable 5.2 | Fable 5.2 only; the API also accepts Mythos 5.2, which stays excluded from selection |

Claude Code attaches no lower-ranked advisor: an Opus or Sonnet advisor on a Fable 5.2 main model runs no consultation and raises no error.

**What the advisor receives.** The model-request transcript, including system context, tool interactions and partial output, as quoted context. It has no tools and no context management of its own.

**Limits.** The executor decides when to consult and owns the resulting action. Account for the added latency and model usage. Advice grants no authority and cannot satisfy independent review.

**Subagents** inherit the configured advisor and apply the same pairing check against their own model. The checked sources establish no Advisor subagent frontmatter and no per-advisor effort control. Keep Advisor out of generated role definitions and dispatch controls unless the target runtime documents and verifies those controls.

Pair table and subagent inheritance: [Code advisor](https://code.claude.com/docs/en/advisor), 14 November 2026. Other mechanics, 3 November 2026: [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool), [Code CLI flags](https://code.claude.com/docs/en/cli-reference#cli-flags), [Code release notes](https://code.claude.com/docs/en/changelog#21260), [model configuration](https://code.claude.com/docs/en/model-config) and [subagents](https://code.claude.com/docs/en/sub-agents).

### Prompts for a session that may have an advisor

Apply this to a prompt, a system prompt or a dispatch for a Claude model. The advisor is a session setting that a subagent inherits, so you usually cannot know whether it is on: write the prompt to work in both cases. Verified 14 November 2026 against the Code advisor and Advisor tool pages; before you copy a block, a model rule or a number from this section into a prompt, read the page again.

**What the prompt can rely on.** The call takes no parameters. The advisor reads the whole transcript: the prompt, the tool definitions, earlier turns, tool results and the text written so far. When a call fails, the executor continues without advice. The platform page disagrees with itself on whether the executor's reasoning reaches the advisor, so do not rely on that.

1. **State the goal, the constraints and the acceptance criteria in the prompt text.** The advisor judges the work against what it can read. Tell the executor to write a decision in visible text before it acts on it. Never tell it to "send" or "summarize for" the advisor: nothing written into the call reaches the advisor.
2. **Never make the task depend on the advisor.** It can be off, refused or failing.
3. **Name consultation points only on a long multi-step task:** before the approach is fixed, on a recurring error, and before the executor declares the work done. For a short or reactive task, write nothing about the advisor.
4. **Ask for a durable result before the completion consultation.** The executor saves its deliverable, within its authority, and then consults: a call takes time, and a saved result survives a session that ends during it.
5. **Never write restraint and a nudge together.** "Reserve the advisor for real uncertainty" conflicts with "consult the advisor before you continue"; the platform page says to drop the nudge when restraint language is present.
6. **Fit the executor model.** Opus calls at an appropriate rate unprompted: add no nudge and no checkpoint by default. A nudge had no measurable effect on Sonnet. For a Haiku coding executor the platform page gives a hard-rule block and a second-turn nudge; its stated evidence is Haiku 4.5. For Fable the pages state no prompting guidance.
7. **Never ask for a forced call through `tool_choice`.** Fable 5.2, Opus 5.5 and Sonnet 5.5 executors reject the `tool` and `any` types. Use one sentence in the prompt.
8. **Never ask for a consultation at every step.** Each call bills at the advisor model's rates and, in Claude Code, processes the full transcript again. Claude Code has no setting that caps or forces calls.
9. **Shorten the advice only when you must.** The tested placement is one line in the user message, such as "(Advisor: please keep your guidance under 80 words.)". It is a soft limit, so name about 80% of the real ceiling. The hard cap is the tool's `max_tokens`, which only an API caller sets.

**Claude Code session or subagent.** Add no timing block and no block about the weight of advice. The Code page says only that a prompt can ask for a consultation and can say that Claude should consult more or less often. In one observed Claude Code 2.1.307 subagent the harness had already supplied the platform's timing and weight text. No page states this: treat it as observed, not guaranteed, and never contradict it.

**API or Agent SDK caller who writes the executor's system prompt.** The platform page gives a timing block and a weight block for coding executors. Put the timing block before any other sentence that mentions the advisor, and the weight block directly after it. Copy both from the page; never paraphrase them.

**A dispatch to a subagent.** The pages state no guidance for delegated lanes beyond inheritance. Apply rules 1 to 9.

## Historical harness mechanics

The loop, workflow and scheduling details below keep their 24 July 2026 verification unless a sentence carries a later date. They are lookup leads, not capability promises: re-fetch the feature's official page before use. An unverified limit receives no new date.

## `/loop`

A bundled skill that re-runs a prompt inside the current session. Limits that change a loop prompt:

- An interval and a prompt run on a fixed schedule; the minimum interval is 1 minute.
- A prompt alone self-paces: Claude picks a delay between 1 minute and 1 hour after each iteration. On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform and Microsoft Foundry it runs every 10 minutes instead, and `loop.md` is not read.
- An interval alone, or nothing, runs the built-in maintenance prompt or your `loop.md`.
- Tasks are session-scoped: a fresh conversation clears them, and recurring tasks expire after 7 days. `--resume` or `--continue` restores only unexpired tasks.
- Limits: up to 50 scheduled tasks per session; `loop.md` is truncated beyond 25,000 bytes; a recurring task fires up to 30 minutes late (up to half the interval when sub-hourly), and a one-shot task set for `:00` or `:30` fires up to 90 seconds early; seconds round up to a minute, and an interval with no clean cron step rounds to one; `CLAUDE_CODE_DISABLE_CRON=1` disables the scheduler.
- Fires carry deterministic jitter, so pick an off-round minute when timing matters. A fire missed while Claude was busy is not caught up.
- A scheduled fire runs only skills Claude may invoke on its own. A built-in command, a skill marked `disable-model-invocation: true`, a skill withheld by settings and an MCP prompt arrive as plain text.
- To watch a process, use the `Monitor` tool, not a loop.

## Agent tool and subagents

For definition files, their directories and the frontmatter field list, read `references/80-subagent-authoring.md`; it holds the one list.

- `Explore` and `Plan` skip CLAUDE.md and the parent session's git status; every other subagent loads both. `Explore` inherits the main conversation's model, capped at Opus on the Claude API. To hold exploration on a cheaper model, define a user or project subagent named `Explore` with `model: haiku`.
- `isolation: worktree` gives the subagent a repository copy in a temporary git worktree, removed automatically when the subagent changes nothing. Use it when lanes would contend on the same files.
- Worktree base (worktrees, 21 October 2026): the default `worktree.baseRef: "fresh"` branches from `origin/HEAD`, so a local base ahead of its remote starts lanes behind it. `"head"` branches from the current local `HEAD`. No value names a commit. `alaa-workflow references/workspace-and-integration.md` owns the lane base rule.
- An authorization to run subagents or parallel lanes requires current host delegation authority. Before you write one for current Opus or Fable, read `references/06-invocation-and-composition.md`.

Two caps govern subagent use ([sub-agents](https://code.claude.com/docs/en/sub-agents) and [environment variables](https://code.claude.com/docs/en/env-vars), 14 November 2026):

| Cap | Default | Variable |
|---|---|---|
| Nesting depth | On — up to three layers below the main conversation | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` disables nesting |
| Concurrent subagents | 20 running at once | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` |

- At the concurrency cap a spawn with the Agent tool fails with `Concurrent subagent limit reached`, and the error tells Claude not to retry. Spawning succeeds again when the running count drops below the cap. Sessions with ultracode active are exempt.
- No cap limits the total number of subagents spawned in a session; `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` has been a no-op since v2.1.224.
- Nesting is on by default, so a carried-forward prompt that assumed it was off now permits nested layers. A subagent whose definition omits `tools` inherits `Agent` and can spawn subagents of its own.
- To stop a role from spawning, omit `Agent` from its `tools` or list it in `disallowedTools`. An `Agent(type, type)` allowlist is ignored in a subagent definition.
- At the depth limit the `Agent` tool is withheld from subagents, and a fork keeps the tool but gets an error.

## Workflow tool

A dynamic workflow is a JavaScript script that orchestrates subagents; a separate runtime runs it in the background. Control flow is deterministic code. Only `agent(...)` calls are model-powered, and `pipeline(...)` runs one agent per list item. Intermediate results stay in script variables, outside Claude's context.

- `ultracode` anywhere in a prompt, or a request in your own words, starts a one-off workflow without changing session effort. The keyword opts in only from human-typed input: not from a `-p` prompt, an unstamped SDK prompt, a scheduled-task prompt, or a relayed webhook or PR comment.
- `/effort ultracode` makes Claude plan a workflow for every substantive task in the session. It combines `xhigh` effort with automatic orchestration and is a Claude Code setting, not a model effort level.

Runtime constraints that change a generated prompt. The exit, relaunch, usage-limit pause and size-setting statements were verified 14 November 2026 against [workflows](https://code.claude.com/docs/en/workflows).

- No mid-run user input: agent permission prompts and the usage-limit pause are the only pauses. The script has no direct filesystem or shell access.
- Up to **16 concurrent agents**, fewer on machines with limited CPU cores, and **1,000 agents total per run**.
- Workflow subagents always run in `acceptEdits` mode and inherit your tool allowlist whatever the session's permission mode, so pre-approve the commands they need before a long run.
- A run resumes within the same session, and completed agents return cached results. After you exit, the run stops, but its saved results stay under the session's directory; resume with `claude --resume` and ask Claude to relaunch it. A fresh session starts the workflow over.
- When an agent hits the claude.ai usage limit, the run pauses, starts no new agents, and continues shortly after the reset. It pauses only under the conditions the page lists, among them a claude.ai subscription session without usage-based billing, `autoContinueAtUsageLimit` on, a reset within 24 hours and no more than two earlier waits; otherwise the affected agent fails. The pause requires Claude Code v2.1.271 or later.
- The Dynamic workflow size setting in `/config` sends an advisory agent-count target: `small` fewer than 5, `medium` fewer than 10, `large` fewer than 50, `unrestricted` none. The default is `medium`, or `small` on a Pro plan, from v2.1.271. A run that schedules more than 25 agents or projects past 1.5 million tokens raises an advisory `Large workflow` warning, suppressed when ultracode is on.
- `disableWorkflows` in settings or `CLAUDE_CODE_DISABLE_WORKFLOWS=1` turns workflows off and removes `ultracode` from the `/effort` menu.

## Plan mode and Ultraplan

- Permission mode names for a prompt: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. The CLI labels `default` as **Manual** and accepts `manual` as an alias.
- Plan mode is the closest thing to a launch gate for a large or risky autonomous run. It composes with `/goal` and `/loop` for the autonomy that follows approval.
- Ultraplan is a research preview with no stated minimum version, so carry forward no version gate for it. It requires a Claude Code on the web account and a GitHub repository, and is unavailable on Amazon Bedrock, Google Cloud's Agent Platform and Microsoft Foundry.

## `/goal`

Verified 4 October 2026 against the goal, desktop and skills pages.

- `/goal <condition>` starts execution immediately and evaluates the condition after each turn from the transcript. One goal is active per session; a new one replaces it.
- The evaluator returns **Not yet met** (continue with its reason), **Met** (clear as achieved) or **Impossible** (stop without achievement). These are evaluator verdicts, not evidence that repository gates passed.
- The evaluator calls no tools and reads no files. The executing session must surface acceptance evidence and check outcomes in the transcript. A saved report's path alone cannot prove its contents.
- The condition limit is **4,000 characters**, excluding the leading command. Put no operating manual in the condition; `references/06-invocation-and-composition.md` owns composition, the soft authoring target, examples and stop clauses.
- Measure the final text actually sent, after substitutions. `scripts/check_goal_condition.py` checks a declared surface and counts in UTF-16 code units against this dated cap. The documentation specifies no Unicode counting semantics; UTF-16 units avoid undercounting astral characters. A static pass is neither parser parity nor live Desktop acceptance, and a runtime rejection stays authoritative.
- Bare `/goal` reports status and `/goal clear` ends it early. Other aliases, resume accounting and noninteractive flags keep their historical verification; re-fetch the goal page before you generate those commands.
- A goal preserves the current permission mode and grants no installation, commit, deployment or other side-effect authority. A chosen autonomous permission mode has separate account, model and provider requirements; a goal prompt cannot enable it.
- Workspace trust must be accepted. `/goal` is unavailable when `disableAllHooks` is set at any level or `allowManagedHooksOnly` is set in managed settings. Report the restriction; never change trust, hooks or permissions to make a prompt run without authorization.
- This is not Codex's `/goal`. Codex runs a durable thread-scoped objective loop with its own budget accounting, not a Stop-hook evaluator. The two differ in what proves completion, how they are enabled and what they cost. Never carry a `/goal` block between the runtimes unedited; read `references/11-codex-runtime-features.md` for Codex.

### Surface preflight and rejected commands

Claude Desktop's **Code tab** is the documented desktop Claude Code surface. Infer no Chat or Cowork command support from the app name; these sources do not establish their `/goal` support. Before you issue a runnable kickoff, resolve the actual surface, the installed runtime version, the registered skill command, goal availability, and the relevant trust and hook restrictions. Inspection authorizes no installation and no settings change.

The user observed this Code-tab rejection on 4 October 2026 (Desktop version unprovided):

> A command takes file @-mentions but no other @-mentions, slash commands, links, or inline formatting, so nothing was sent. Remove them.

This is Desktop composer evidence, not a documented universal CLI grammar. No live Desktop command was exercised, and no parser or cap change is established. The rule applies to **command arguments**, including a skill-led kickoff:

- Use one leading registered command and plain arguments: no secondary slash command, non-file @mention, link, backtick, bold or other inline formatting.
- Name companion skills without sigils and use plain paths.
- Write the goal condition as plain text with no skill activation and no file reference by default; keep those in the kickoff or the plan.
- The diagnostic permits file @mentions, but generated text can neither create nor validate their composer chips. A static text pass proves no structured-composer acceptance.

When a command is rejected:

1. Record the supplied prompt, the error, the app and runtime version, and the tab. Get only the missing facts that the diagnosis needs.
2. Check the composer tokens and the rendered length.
3. Classify the cause: command or surface availability, skill resolution, trust or hooks, or a remaining unknown.
4. Without the rejected payload, repair established defects, but claim no reproduction, no parser or cap change and no incident closure.
5. Provide a verified plain kickoff, or report the missing capability. Never guess a fallback on another surface.

## Choosing a mechanism

- `/loop`: a time-based cadence, or "keep tending this" maintenance.
- `/goal`: "do not stop until this condition is true", only when the transcript can demonstrate the condition.
- Subagents: disjoint lanes inside one session whose results alone matter. Add `isolation: worktree` when lanes would touch the same files.
- Workflow tool: a job that outgrows a handful of subagents, or findings that must be cross-checked, where the control flow must be reliable, reviewable and worth rerunning: a codebase-wide audit, a large migration, a judge panel.
- Agent teams: coordinated sessions with a shared task list whose workers must message each other. They are experimental and off by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), cost materially more than subagents, and have no worktree isolation and no nested teams.
- Agent view (`claude agents`): independent background sessions, each in its own worktree. Research preview.
- `/batch`: a bundled skill that splits one large change into 5 to 30 worktree-isolated subagents, each opening a pull request.
- `/alaa-workflow`: durable multi-phase work.

## Caveats

Re-check every version gate and exact limit before use. The most volatile are the dynamic workflow concurrency and total caps, `ultracode`, the nesting and subagent caps, the workflow warnings and the loop limits. A historical default is not activation evidence.

## Sources

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Run prompts on a schedule (`/loop`)](https://code.claude.com/docs/en/scheduled-tasks)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Run agents in parallel](https://code.claude.com/docs/en/agents)
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Plan in the cloud with ultraplan](https://code.claude.com/docs/en/ultraplan)
- [Keep Claude working toward a goal (`/goal`)](https://code.claude.com/docs/en/goal)
- [Claude Code on desktop](https://code.claude.com/docs/en/desktop)
- [Model configuration](https://code.claude.com/docs/en/model-config)

## Managed task-selected authority roles

- The runtime orchestrator renders a model-neutral definition for every managed authority role. Its `scripts/render_agents.py --check` rejects source drift and claims no activation.
- The capability policy registers the roles and their supported pairs. An existing ID that names a model or an effort is a compatibility name only.
- The orchestrator chooses the model AND effort for each task and checks the effective overrides. Main-session controls stay externally configured.
- A planner draft stays advisory.
- Source consistency proves no loaded registration, account access or serving identity.
