# Claude Code Runtime Features

A model or API capability does not establish harness support. This file owns Claude Code selection and activation mechanics. The structured policy registers model-neutral role identities and capabilities. Before you depend on a feature, refresh its official runtime page against the actual CLI version.

## Current model, effort and identity resolution

Verified 25 September 2026 against model-config and sub-agents. A full API ID pins a version. A family alias rolls, and it can resolve differently by provider, parent model or gateway. A provider deployment mapping is separate runtime evidence; the policy does not accept it as an alias.
The policy records sourced model minimum versions. When you need a model's minimum Claude Code version, alias behaviour, default effort per surface or thinking control in Code, read that model's current reference. A newer installed CLI alone proves neither account entitlement nor activation.

To resolve the session model, inspect an explicit /model choice, the startup --model flag, ANTHROPIC_MODEL, settings and ANTHROPIC_DEFAULT_MODEL, managed allowlists, and host overrides. /model can persist a selection. Inspection authorizes neither a settings change nor credit consent.

Since 2.1.251, subagent model precedence runs from the invocation, to the definition frontmatter, to the subagent model environment variable, to the parent. Earlier versions give that environment variable priority, so never apply that order to a newer CLI. Since 2.1.257, CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 forces the model that the subagent model environment variable targets, or the parent model when the variable sets no target. Forks and skills with model: inherit keep documented exceptions; inspect them before you claim that a pin won. Resolve inherit and family aliases on the target provider.
An allowlist may substitute a different model. A requested selection is not an observed identity.

Verified 14 November 2026 against sub-agents and the active Agent tool schema: the per-invocation `model` parameter accepts a family alias only (`sonnet`, `opus`, `haiku`, `fable`). It accepts no full ID and no `inherit`. To realize a selected full ID at dispatch, pass its family alias and verify that the alias resolves to that ID on the target provider. When it does not, the definition's `model` field is the only pin, and the lane of a managed model-neutral role is blocked. A nested subagent with no model runs on its parent subagent's model, not on the main conversation's model.

Verified 9 October 2026: since 2.1.292, an effort given at a non-fork invocation overrides the frontmatter effort and the session effort, and it persists on resume. Verified 14 November 2026: when neither an effort field nor an effort parameter is set, a subagent on the main model uses the session level; on a different model that level does not apply. `CLAUDE_CODE_EFFORT_LEVEL` supersedes the invocation and the frontmatter; model support and effective caps can step an unsupported level down. Managed roles omit model and effort, so on that verified surface the dispatch must provide BOTH controls explicitly. Inspect how force settings, environment variables, hooks and the provider resolve the controls; omitted pins alone prove neither pair. On an older, forked or unsupported surface, use an available exact verified realization or block the affected lane. Never treat inheritance as selection. Main-session configuration stays external. Refresh thinking inheritance against the actual runtime; a model or API thinking control does not become a per-agent setting by inference.

Verified 14 November 2026 against [workflows](https://code.claude.com/docs/en/workflows): a Workflow-tool `agent()` call takes its model in the same order as a subagent. A model the script names counts as the per-invocation model. When nothing else assigns one, the agent runs on the session's model. The workflows page names no effort option for `agent()`.

When you report identity, follow `references/80-subagent-authoring.md` *Configuration and observed identity*, and record the resolved controls as well. In Claude Code, session status, subagent status and the response's modelUsage contribute evidence when they are available. An agent's self-description does not prove its identity. A runtime activation check requires authorized execution, and it must preserve the provider and account context, the control evidence and any observed mismatch.

## Fallback and safeguards

A provider safety fallback and a configured overload fallback are different events. Either can change the serving model after selection. Preserve safeguards. Disclose a fallback or an unknown identity. Exclude the affected runs from claims about the requested pair. Never weaken a safeguard, silently substitute a model or introduce a local fallback to complete a gate.
Noninteractive Fable use may spend credits without prompting; obtain the applicable execution authority before a live run. No source checker grants authority to install, to change settings or to pay for execution.

## Native Advisor

Use Claude Code's native Advisor for executor consultations. The orchestrator's read-only Advisor mode is a separate role. In a supported Code session, use `/advisor <model>`. At launch, `--advisor <model>` overrides the `advisorModel` setting. Use a supported `sonnet`, `opus` or `fable` alias or a full model ID. Verified 14 November 2026: the advisor is experimental and needs the Anthropic API or Claude Platform on AWS. Before you depend on Advisor, resolve the alias and verify support on the actual Code version, provider, account, managed allowlist and entitlement. Inspection grants neither configuration authority nor paid execution authority.

Claude Code ranks models for the advisor role and accepts only the pairs in its advisor table. These are its rows for the active set. Verify the exact resolved pair on the target Code surface.

| Main model | Accepted advisors |
|---|---|
| Haiku 5.5 | Fable, Opus 4.7 or later, Sonnet 5 or later, Haiku 5.5 |
| Sonnet 5.5 | Fable, Opus 5 or later, Sonnet 5.5 |
| Opus 5.5 | Fable, Opus 5 or later |
| Fable 5.2 | Fable 5.2 only; the API also accepts Mythos 5.2, which stays excluded from selection |

Claude Code attaches no lower-ranked advisor: an Opus or Sonnet advisor on a Fable 5.2 main model runs no consultation and raises no error.

The executor decides when to consult and owns the resulting action. The advisor receives the model-request transcript, including system context, tool interactions and partial output, as quoted context. The advisor has no tools or context management of its own. Account for added latency and model usage. Advice grants no authority and cannot satisfy independent review.

Subagents inherit the configured advisor and apply the same pairing check against their own model. The checked Code sources establish no Advisor subagent frontmatter and no per-advisor effort control. Keep Advisor out of generated role definitions and dispatch controls unless the target runtime documents and verifies those controls.

Pair table and subagent inheritance verified 14 November 2026 against [Code advisor](https://code.claude.com/docs/en/advisor). Other mechanics verified 3 November 2026 against [Advisor API mechanics and compatibility](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool), [Code CLI flags](https://code.claude.com/docs/en/cli-reference#cli-flags), [Code release notes](https://code.claude.com/docs/en/changelog#21260), [model configuration](https://code.claude.com/docs/en/model-config) and [subagents](https://code.claude.com/docs/en/sub-agents).

### Prompts for a session that may have an advisor

Apply this when you write a prompt, a system prompt or a dispatch for a Claude model. The advisor is a session setting and a subagent inherits it, so you usually cannot know whether it is on. Write the prompt so that it works in both cases.

**What the prompt can rely on.** The executor decides when to call. The call takes no parameters. The advisor reads the whole transcript: your prompt, the tool definitions, earlier turns, tool results and the text written so far. When a call fails, the executor continues without advice. The platform page disagrees with itself on whether the executor's reasoning reaches the advisor, so do not rely on it.

1. **State the goal, the constraints and the acceptance criteria in the prompt text.** The advisor judges the work against what it can read. Tell the executor to write a decision down in visible text before it acts on it. Never tell it to "send" or "summarize for" the advisor: nothing written into the call reaches the advisor.
2. **Never make the task depend on the advisor.** It can be off, refused or failing. Advice grants no authority and replaces no review.
3. **Name the points where a consultation pays, and only on a long multi-step task:** before the approach is fixed, on a recurring error, and before the executor declares the work done. For a short or reactive task, write nothing about the advisor: the first call carries most of the value and a short task is a weak fit.
4. **Ask for a durable result before the completion consultation.** The executor saves or writes its deliverable, within its authority, and then consults. A call takes time, and a saved result survives a session that ends during it.
5. **Do not write restraint and a nudge together.** "Reserve the advisor for real uncertainty" beside "consult the advisor before you continue" conflict; the platform page says to drop the nudge when restraint language is present. Choose one.
6. **Fit the executor model.** Opus calls at an appropriate rate without prompting: add no nudge and no checkpoint by default. A nudge had no measurable effect on Sonnet. For a Haiku coding executor the platform page gives a hard-rule block and a second-turn nudge; its stated evidence is Haiku 4.5. For Fable the pages state no prompting guidance.
7. **Do not ask for a forced call through `tool_choice`.** Fable 5.2, Opus 5.5 and Sonnet 5.5 executors reject the `tool` and `any` types. Use one sentence in the prompt.
8. **Do not ask for a consultation at every step.** Each call bills at the advisor model's rates and, in Claude Code, processes the full transcript again. Claude Code has no setting that caps or forces calls.
9. **Shorten the advice only when you must.** The tested placement is one line in the user message, such as "(Advisor: please keep your guidance under 80 words.)". It is a soft limit, so name about 80% of the real ceiling. The hard cap is the tool's `max_tokens`, which only an API caller sets.

**Claude Code session or subagent.** Add no timing block and no block about how much weight advice gets. The Code page says only that a prompt can ask for a consultation and can say that Claude should consult more or less often. In one observed Claude Code 2.1.307 subagent the harness had already supplied the platform's timing and weight text; no page states this, so treat it as observed, not guaranteed, and never contradict it.

**API or Agent SDK caller who writes the executor's system prompt.** The platform page gives a timing block and a weight block for coding executors. Put the timing block before any other sentence that mentions the advisor, and the weight block directly after it. Copy both from the page; do not paraphrase them. They tell the executor to consult before substantive work, when stuck, on a change of approach and before it declares completion; to give advice serious weight; to adapt when a step fails or a primary source contradicts a claim; and to raise a conflict in one more call instead of switching silently.

**A dispatch to a subagent.** The pages state no prompt guidance for delegated lanes beyond inheritance. Apply rules 1 to 9, and name a consultation point only for a lane that carries long multi-step work.

Verified 14 November 2026 against [Code advisor](https://code.claude.com/docs/en/advisor) and [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool). Before you copy a block, a model rule or a number from this section into a prompt, read the page again.

## Historical harness mechanics

The loop, workflow and scheduling details below keep their 24 July 2026 verification unless a sentence carries a later date. They are lookup leads, not current capability promises: re-fetch the feature's official page before use. An unverified limit receives no new date.

## `/loop` — recurring or self-paced interval execution

A bundled skill that re-runs a prompt inside the current session. An interval and a prompt run on a fixed schedule. A prompt alone self-paces: Claude picks a delay between 1 minute and 1 hour after each iteration. An interval alone, or nothing, runs the built-in maintenance prompt or your `loop.md`. A scheduled fire runs only skills Claude may invoke on its own; a built-in command, a skill marked `disable-model-invocation: true`, a skill withheld by settings and an MCP prompt arrive as plain text instead.

Write a loop prompt with these limits in mind. The minimum interval is 1 minute. Tasks are session-scoped: a fresh conversation clears them, and recurring tasks expire after 7 days. Fires carry deterministic jitter, so pick an off-round minute when timing matters. A fire missed while Claude was busy is not caught up. On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform and Microsoft Foundry, a prompt-only loop runs every 10 minutes instead of self-pacing and `loop.md` is not read. To watch a process rather than re-ask a question, use the `Monitor` tool instead.

## Agent tool / subagents — foreground, background, and nested delegation

A subagent gets its own fresh context window, system prompt, restricted tools and independent permissions. The built-ins are `Explore`, `Plan` and `general-purpose`. `Explore` and `Plan` skip CLAUDE.md and the parent session's git status; every other subagent loads both. `Explore` inherits the main conversation's model, capped at Opus on the Claude API; to hold exploration on a cheaper model, define a user or project subagent named `Explore` with `model: haiku`.

Custom subagents are Markdown files with YAML frontmatter under `.claude/agents/` (project, discovered by walking up to the repository root) or `~/.claude/agents/` (user), both scanned recursively; identity comes from the `name` field, not the path. Only `name` and `description` are required. Frontmatter of interest for orchestration prompts: `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`. `isolation: worktree` gives the subagent an isolated repository copy in a temporary git worktree, removed automatically when the subagent changes nothing; use it when lanes would otherwise contend on the same files. Verified 21 October 2026 against worktrees: the default `worktree.baseRef: "fresh"` branches from `origin/HEAD`, so a local base ahead of its remote starts lanes behind it, `"head"` branches from the current local `HEAD`, and no value names a commit; `alaa-workflow references/workspace-and-integration.md` owns the lane base rule.

Two separate caps govern subagent use, each with its own environment variable:

| Cap | Default | Variable |
|---|---|---|
| Nesting depth | On — up to three layers below the main conversation | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`; `1` disables nesting |
| Concurrent subagents | 20 running at once | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` |

At the concurrency cap, a spawn with the Agent tool fails with `Concurrent subagent limit reached`, and the error tells Claude not to retry. Spawning succeeds again when the running count drops below the cap. No cap limits the total number of subagents spawned in a session; `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` has been a no-op since v2.1.224. Verified 14 November 2026 against [sub-agents](https://code.claude.com/docs/en/sub-agents) and [environment variables](https://code.claude.com/docs/en/env-vars).

Verified 14 November 2026 against sub-agents: nesting is on by default, so a carried-forward prompt that assumed it was off now permits nested layers. A subagent whose definition omits `tools` inherits `Agent` and can spawn subagents of its own. To stop a role from spawning, omit `Agent` from its `tools` or list it in `disallowedTools`; an `Agent(type, type)` allowlist is ignored in a subagent definition. At the depth limit the `Agent` tool is withheld from subagents, and a fork keeps the tool but gets an error. Sessions with ultracode active are exempt from the concurrency cap.

Subagents run in the background by default; Claude runs one in the foreground when it needs the result before continuing. A background subagent surfaces its permission prompts in the main session, and its result arrives as a completion notification in a later turn. `/subtask` starts a fork, a subagent that inherits the full conversation; use it to try several approaches from one starting point. `/fork` copies the whole session into a separate background session.

An authorization to run subagents or parallel lanes requires current host delegation authority. Before you write one for current Opus or Fable, read `references/06-invocation-and-composition.md` for the delegation polarity those models need.

## Workflow tool — deterministic multi-agent orchestration scripts

A dynamic workflow is a JavaScript script that orchestrates subagents. Claude writes it, and a separate runtime runs it in the background. Control flow is deterministic code; only `agent(...)` calls are model-powered, and `pipeline(...)` runs one agent per list item. Intermediate results stay in script variables, not in Claude's context. The script for every run is saved under the session's directory in `~/.claude/projects/`. Use a workflow when a job outgrows a handful of subagents or when findings must be cross-checked: a codebase-wide audit, a large migration, adversarial cross-checking, a judge panel. `/deep-research` is a bundled workflow that runs only when invoked.

`ultracode` anywhere in a prompt, or a request in your own words, starts a one-off workflow without changing session effort. The keyword opts in only from human-typed input: it does not fire from a `-p` prompt, an unstamped SDK prompt, a scheduled-task prompt, or a relayed webhook or PR comment. `/effort ultracode` makes Claude plan a workflow for every substantive task in the current session; it combines `xhigh` effort with automatic orchestration and is a Claude Code setting, not a model effort level. `/workflows` manages runs, and `s` there saves a run's script as a `/<name>` command in `.claude/workflows/` or `~/.claude/workflows/`; a saved workflow takes input through an `args` global.

Runtime constraints that change a generated prompt:

- No mid-run user input; agent permission prompts and the usage-limit pause are the only pauses. The script has no direct filesystem or shell access.
- Up to **16 concurrent agents**, fewer on machines with limited CPU cores, and **1,000 agents total per run**.
- Workflow subagents always run in `acceptEdits` mode and inherit your tool allowlist whatever the session's permission mode, so pre-approve the commands they need before a long run.
- A run resumes within the same session, and completed agents return cached results. After you exit, the run stops, but its saved results stay under the session's directory; resume with `claude --resume` and ask Claude to relaunch it. A fresh session starts the workflow over.
- When an agent hits the claude.ai usage limit, the run pauses, starts no new agents, and continues shortly after the reset. It pauses only under the conditions the page lists, among them a claude.ai subscription session without usage-based billing, `autoContinueAtUsageLimit` on, a reset within 24 hours and no more than two earlier waits; otherwise the affected agent fails. The pause requires Claude Code v2.1.271 or later.
- The Dynamic workflow size setting in `/config` sends an advisory agent-count target: `small` fewer than 5, `medium` fewer than 10, `large` fewer than 50, `unrestricted` none. The default is `medium`, or `small` on a Pro plan, from v2.1.271. A run that schedules more than 25 agents or projects past 1.5 million tokens raises an advisory `Large workflow` warning, suppressed when ultracode is on.
- `disableWorkflows` in settings or `CLAUDE_CODE_DISABLE_WORKFLOWS=1` turns workflows off and removes `ultracode` from the `/effort` menu.

The exit, relaunch, usage-limit pause and size-setting statements were verified 14 November 2026 against [workflows](https://code.claude.com/docs/en/workflows).

## Plan mode / Ultraplan — structured checkpoint before autonomous work

Plan mode lets Claude read and explore but not edit, and it produces a plan you approve before any change. Enter it with `Shift+Tab`, a `/plan` prefix on one prompt, or `claude --permission-mode plan`. Shell commands outside the built-in read-only set still prompt during planning. Approving switches the session into the permission mode the chosen option describes. When you name modes in a prompt, the full set is `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`; the CLI labels `default` as **Manual** and accepts `manual` as an alias.

Ultraplan drafts the plan in a Claude Code on the web session in plan mode, for review in the browser. Launch it with `/ultraplan <task>`, the bare keyword `ultraplan` in a prompt, or "refine with Ultraplan" in a local plan's approval dialog. It is a research preview with no stated minimum version, so carry forward no version gate for it. It requires a Claude Code on the web account and a GitHub repository, and is unavailable on Amazon Bedrock, Google Cloud's Agent Platform and Microsoft Foundry. `/ultrareview` is its review-side counterpart.

Plan mode is the closest thing to a launch gate for a large or risky autonomous run. It composes with `/goal` and `/loop` for the autonomy that follows approval.

## `/goal` — condition-based multi-turn autonomy (Claude Code's own mechanism)

Verified 4 October 2026 against the official goal, desktop and skills pages. Claude Code's `/goal <condition>` starts execution immediately and evaluates the condition after each turn using the transcript. Its evaluator returns **Not yet met** (continue with its reason), **Met** (clear as achieved), or **Impossible** (stop without achievement). One goal is active per session; a new one replaces it. These are evaluator verdicts, not evidence that repository gates passed.

Codex's `/goal` instead runs a durable thread-scoped objective loop with its own budget accounting, not a Stop-hook evaluator. The two differ in what proves completion, how they are enabled and what they cost. Never carry a `/goal` block between the runtimes unedited; read `references/11-codex-runtime-features.md` for Codex's mechanism.

The condition limit is **4,000 characters**, excluding the leading command. The evaluator calls no tools and reads no files; the executing session must surface acceptance evidence and check outcomes in the transcript. A saved report's path alone cannot prove its contents. Composition, the soft authoring target, examples and stop clauses belong to `references/06-invocation-and-composition.md`; do not put an operating manual in the condition.

Measure the final text actually sent, after substitutions. `scripts/check_goal_condition.py` checks a declared surface and counts conservatively in UTF-16 code units against this dated cap. The documentation does not specify Unicode counting semantics; this assumption avoids undercounting astral characters relative to code points. A static pass is neither parser parity nor live Desktop acceptance, and a runtime rejection remains authoritative.

Bare `/goal` reports status and `/goal clear` ends it early. Other aliases, resume accounting and noninteractive flags keep their historical verification; re-fetch the goal page before you generate those commands.

A goal preserves the current permission mode; it grants no installation, commit, deployment or other side-effect authority. Workspace trust must be accepted, and `/goal` is unavailable when `disableAllHooks` is set at any level or `allowManagedHooksOnly` is set in managed settings. Report the restriction; never change trust, hooks or permissions to make a prompt run without authorization.

### Surface preflight and rejected commands

Claude Desktop's **Code tab** is the documented desktop Claude Code surface. Do not infer Chat or Cowork command support from the app name; these sources do not establish their `/goal` support. Before you issue a runnable kickoff, resolve the actual surface, the installed runtime version, the registered skill command, goal availability, and the relevant trust and hook restrictions. Inspection does not authorize installation or settings changes.

The user observed this Code-tab rejection on 4 October 2026 (Desktop version unprovided):

> A command takes file @-mentions but no other @-mentions, slash commands, links, or inline formatting, so nothing was sent. Remove them.

This is Desktop composer evidence, not an officially documented universal CLI grammar. It applies to **command arguments**, including a skill-led kickoff: use one leading registered command and plain arguments without secondary slash commands, non-file @mentions, links, backticks, bold or other inline formatting. Name companion skills without sigils and use plain paths. Generate the goal condition as plain text with no skill activation or file references by default; keep them in the kickoff or plan. The diagnostic permits file @mentions, but generated text cannot manufacture or validate their composer chips. A static text pass proves no structured-composer acceptance.

When a command is rejected:

1. Record the supplied prompt, the error, the app and runtime version, and the tab. Obtain only the missing facts that the diagnosis needs.
2. Check the composer tokens and the rendered length.
3. Classify the cause as command or surface availability, skill resolution, trust or hooks, or a remaining unknown.
4. Without the rejected payload, repair established defects, but do not claim a reproduction, a parser or cap change, or incident closure.
5. Provide a verified plain kickoff, or report the missing capability. Never guess a fallback on another surface.

## Choosing between `/loop`, `/goal`, subagents, workflows, and the rest

- **`/loop`**: a time-based cadence, or "keep tending this" maintenance.
- **`/goal`**: "do not stop until this condition is true", only when the condition is demonstrable from the transcript.
- **Subagents**: disjoint lanes inside one session whose results alone matter. Add `isolation: worktree` when lanes would touch the same files.
- **Workflow tool**: the highest-stakes or highest-scale fan-out, where the control flow must be reliable, reviewable and worth rerunning.
- **Agent teams**: coordinated sessions with a shared task list whose workers must message each other. They are experimental and off by default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), cost materially more than subagents, and have no worktree isolation and no nested teams.
- **Agent view** (`claude agents`): dispatch and monitor independent background sessions, each in its own worktree. Research preview.
- **`/batch`**: a bundled skill that splits one large change into 5 to 30 worktree-isolated subagents, each opening a pull request.

These compose: a workflow's `agent()` calls are subagents, a `/goal` can supervise a session that uses `/loop`, and an approved `/ultraplan` plan is often what a later `/goal` or `/loop` executes. For durable multi-phase work, route to `/alaa-workflow`.

## Caveats

Goal condition, evaluator, permissions, restrictions and Desktop Code guidance were refreshed 4 October 2026. No live Desktop command was exercised and no parser or cap change is established. Re-check every version gate and exact limit before use; the most volatile are dynamic workflow concurrency and total caps, `ultracode`, nesting and subagent caps, workflow warnings and loop limits. Historical defaults are not activation evidence. A chosen autonomous permission mode has separate account, model and provider requirements; a goal prompt cannot enable it.

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

The runtime orchestrator renders a model-neutral definition for every managed authority role. Its `scripts/render_agents.py --check` rejects source drift and does not claim activation. The capability policy registers the roles and their supported pairs. The orchestrator chooses the actual model AND effort for each task and checks the effective overrides. An existing ID that names a model or an effort is a compatibility name only. Source consistency cannot prove loaded registration, account access or serving identity. A planner draft remains advisory. Main-session controls remain externally configured.
