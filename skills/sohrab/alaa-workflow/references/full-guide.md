# Purpose

Provide a durable workflow for long, multi-step repository work so that planning, implementation, validation, review, resume, handoff, delegated execution, and documentation alignment stay coherent even when the task spans many turns, files, agents, worktrees, or context windows.

# Trigger boundaries and ownership

Use this skill when the task needs one or more of these:

- a detailed execution-ready plan grounded in the current repository
- a same-stem implementation/review phase prompt pack
- a multi-phase implementation loop with explicit status tracking
- durable repo-local memory that survives long sessions, compaction, interruption, or agent handoff
- user-authorized subagents, background jobs, parallel lanes, or worktrees
- review mode for production readiness, security, observability, architecture, or clean-code quality
- cross-skill orchestration across Alaa's ecosystem

Do not use this skill as a substitute for domain expertise. Pair it with the correct stack skill when the work touches contracts, frameworks, infrastructure, databases, runtime behavior, UI, security, observability, or docs.

# Instruction precedence

If instructions conflict, follow this order:

1. explicit user constraints for the current task
2. repo-local `AGENTS.md` and closer agent instructions
3. this skill
4. general best practices

If a higher-precedence rule blocks a workflow step, follow the higher-precedence rule and record the deviation in the plan and continuation state.

# Workflow modes

Choose exactly one primary mode at the start. A task can move from one mode to another, but record the transition in state.

## `plan`

Use when the user wants a plan first or the surface is in native plan mode.

Outputs:

- a deep parent plan file unless file creation is forbidden
- a same-stem `__phase-prompts.md` file for GPT implementation and Opus review prompts
- a human continuation state file under `docs/agents/`
- a machine state file under `.codex/state/` when writable

## `execute`

Use when the task already has enough direction and needs implementation.

Outputs:

- code, docs, tests, and validation results
- plan checklist updates as the run advances
- state updates when continuity matters
- review/fix-loop prompts consumed from the phase prompt pack when applicable

## `resume`

Use when continuing a prior task from existing workflow artifacts.

Outputs:

- updated plan/state/continuation files
- refreshed next actions
- explicit reconciliation of old assumptions vs current repo state

Blocking rule: read the main plan before any action. Then read the continuation state, machine state if available, phase prompt pack if implementing or reviewing, and only then open relevant code.

## `delegated`

Use when the user authorizes subagents or parallel work and the work has truly independent lanes.

Outputs:

- parent plan and parent state remain the source of truth
- optional child lane plan and state files
- integrated, validated final result from the parent agent
- clear lane handoffs with files changed, validation evidence, blockers, and suggested commit message

## `review`

Use when the user asks for a code, plan, diff, PR, phase, architecture, security, or production-readiness review.

Outputs:

- verdict and concrete findings
- gate evidence
- blocker/nit separation
- production-readiness, security, observability, high-traffic suitability, clean-code, architecture, and design-pattern assessment
- out-of-scope recommendations where wider refactoring would improve production quality

# Artifact path and naming rules

## Path family selection

Choose the plan directory in this order:

1. the existing task-specific path already in use
2. existing `docs/_agent_plans/`
3. existing `docs/plan/`
4. default `docs/_agent_plans/`

Use `.codex/state/` for machine-readable state whenever state files are needed and the current sandbox can write it.

Use `docs/agents/` for the human-readable continuation state. This file is not a substitute for the plan; it is a compact resumption log.

If `.codex/state` is blocked by sandbox, managed automation permissions, or approval settings:

- do not keep retrying the same blocked write
- do not request escalation only to create workflow state
- keep the plan file in the selected plan directory
- use the continuation state file as the repo-writable fallback
- record the intended `.codex/state/<stem>.json` path and the exact blocker
- keep final output honest that JSON state was blocked and markdown state was used instead

## Naming rules

Parent task stem:

- `<YYYYMMDD-HHMMSS>_<slug>`

Parent artifacts:

- plan: `docs/_agent_plans/<stem>.md` or `docs/plan/<stem>.md`
- phase prompts: `docs/_agent_plans/<stem>__phase-prompts.md` or `docs/plan/<stem>__phase-prompts.md`
- continuation: `docs/agents/<stem>-state.md`
- machine state: `.codex/state/<stem>.json`

Child lane artifacts:

- plan: `<parent-stem>__<lane>.md`
- state: `<parent-stem>__<lane>.json`

Keep parent and child stems stable for the life of the task.

## When to create artifacts

Create a parent plan, phase prompt pack, continuation state, and machine state when:

- the user asks for a plan
- the task is long, risky, or multi-phase
- the task may continue later or transfer to another agent
- the task includes subagents, parallel lanes, background jobs, or worktrees
- the task needs phase-specific implementation/review prompts

Create or update state when:

- a run is likely to span many turns or many hours
- delegated or parallel execution is involved
- meaningful blockers, validation status, or handoff notes should not live only in chat
- another agent should be able to resume from artifacts alone

Skip plan/state files only for truly small tasks with no continuity value or when file creation is explicitly forbidden.

## Constrained mode

If the current task forbids new files or allows only one output file:

- do not create the normal artifact set
- embed the same structure in chat or the single permitted file
- keep the exact plan headings if possible
- explain which normal artifact paths were not created and why

# Plan mode

The plan must be implementation-ready. It must be rooted in the current repository, current task state, user constraints, and real validation surfaces.

## Deep-plan quality bar

A good plan is not a list of vague bullets. It tells the executing agent exactly what to do next and what to avoid. Prefer deterministic recommendations over open-ended option lists unless a decision truly cannot be frozen yet.

Every plan must explicitly separate:

1. what is already good
2. what gaps remain
3. what must change now
4. what is intentionally deferred
5. what must be validated before a phase can close

Do not reopen settled architecture unless the current repository state directly contradicts it.

## Draft-to-final writing rule

Before finalizing a plan, create a working draft mentally or in a safe scratch area. Then rewrite the final plan so it is coherent, polished, and complete.

The final plan must:

- preserve every material detail from the draft
- use simple, fluent English with complete sentences
- have a clear beginning (`## Summary`), structured middle (phases and lanes), and clear finish (docs alignment, validation, handoff)
- avoid filler, contradictions, and orphaned TODOs

## Repository grounding checklist

Before finalizing the plan:

1. read the relevant `AGENTS.md` files
2. find the closest relevant implementation patterns in the repo
3. map the exact surfaces likely to change: code, config, tests, migrations, docs, CI, runtime, infra
4. identify contract boundaries: HTTP, events, jobs, DB schema, CLI, env vars, config files, build pipelines
5. identify rollout, migration, security, privacy, observability, and performance risk
6. identify the real validation commands for this repository
7. decide which phases can be parallelized and which integration phase must serialize convergence
8. identify the mandatory skills for every phase

## Mandatory exact plan headers

The plan must contain these exact top-level headings:

- `## Summary`
- `## Goal`
- `## Assumptions`
- `## Constraints`
- `## Closest existing patterns`
- `## Phases (with dependencies)`
- `## Parallel-safe work split`
- `## Commands to run`
- `## Phase prompt pack`
- `## Files touched (append-only log)`
- `## Done / Remaining`
- `## Draft-to-final rewrite record`

Use `assets/plan-template.md` unless a stronger task-specific structure is already in flight.

## Required content under each heading

### `## Summary`

Write this first. It must explain:

- the topic
- what executing the plan will achieve
- the main idea of the plan
- how tests, parallel lanes, integration, and docs alignment fit together

### `## Goal`

Capture all of these:

- problem statement in repository terms
- in-scope work now
- non-goals and deferrals
- definition of done
- frozen decisions already made
- current repository snapshot relevant to the task
- what is already good
- what gaps remain
- architecture boundaries and contract surfaces

### `## Assumptions`

List only assumptions that materially affect implementation or validation. Mark each assumption as one of:

- `frozen`
- `verify during execution`
- `blocker if false`

Include the impact and verification path.

### `## Constraints`

Include user constraints, repo rules, approval or sandbox limits, environment limits, version constraints, rollout limits, safety/privacy/destructive-action limits, and stack-specific guardrails.

### `## Closest existing patterns`

List concrete paths or modules in the repository and explain:

- why each one is the closest pattern
- what to reuse
- what must stay different

### `## Phases (with dependencies)`

For every phase include:

- status
- objective
- inputs and dependencies
- mandatory skills
- optional skills where useful
- exact files or modules likely to touch
- `Parallel-safe`, `Not parallel-safe`, or `lane-only`
- branch/worktree guidance when useful
- subtask checklist with Markdown checkboxes
- test-first checklist with Markdown checkboxes
- validation checklist with Markdown checkboxes
- acceptance criteria
- risk or drift watchpoints
- completion signal

The final phase must always be documentation alignment and handoff. If no docs need edits, the phase still verifies that fact and records evidence.

### `## Parallel-safe work split`

Define lane ownership even if the task stays single-agent. Include:

- parent-agent responsibilities
- per-lane scope
- mandatory skills per lane
- read scope
- write scope
- dependencies on other lanes
- branch/worktree notes
- merge notes and integration order

If worktrees are recommended, fix branch names but leave worktree directory names to the user.

### `## Commands to run`

Group commands by purpose:

- discovery
- implementation support
- validation
- documentation alignment
- rollback or recovery when relevant

Only include commands that make sense in the current repository.

### `## Phase prompt pack`

Name the required same-stem `__phase-prompts.md` path and include a checklist proving it will contain:

- standing rules
- Codex/GPT implementation `/goal` prompts per phase
- Opus review prompts per phase
- fix-loop prompt
- parallel/worktree run instructions when relevant

### `## Files touched (append-only log)`

Use a timestamped append-only log. Do not rewrite history.

### `## Done / Remaining`

Maintain these subsections:

- Done
- Remaining now
- Deferred intentionally
- Blocked or waiting

### `## Draft-to-final rewrite record`

Record whether a draft was prepared and the final rewrite was completed. The final rewrite must preserve material details and improve coherence.

## Optional extra headings

You may add headings such as `## Risks and drift watchpoints`, `## Contract notes`, or `## Rollout plan` when useful, but do not remove the mandatory exact headings.

# Phase prompt pack mode

Every parent plan created by this skill requires a same-stem `__phase-prompts.md` file. Read `phase-prompts.md` for the complete contract.

Minimum contents:

- summary and cadence
- standing rules copied or tailored from the plan
- one Codex/GPT `/goal` implementation prompt per phase
- one Opus review prompt per phase
- one fix-loop prompt pattern
- clear role split: GPT-5.5/Codex implements by default; Opus 4.8 reviews by default
- explicit permission to use subagents/parallel/background jobs when lanes are independent
- validation and state update requirements

The planning agent must write this as a senior prompt engineer for coding agents, not as a generic checklist.

# Execution mode

The parent plan is the runbook. Execute against it, not against vague memory.

## Standard execution loop

1. read the main plan, active phase, dependencies, continuation state, and machine state if available
2. read the phase prompt pack when running from a phase prompt or producing one
3. re-open the exact files you are about to change
4. write or update tests before or alongside behavior changes
5. make the smallest coherent diff that advances the phase
6. run validation for that phase
7. repair failures before moving on
8. update plan and state artifacts
9. move to the next phase only when acceptance criteria are met or a blocker is recorded

## Update cadence

Update plan/state artifacts at these moments:

- immediately after artifact creation
- when a phase starts
- when a lane or subagent is dispatched
- when a background job or long validation starts
- when a phase finishes
- after any meaningful decision freeze or scope change
- before and after long validation runs
- after review and after fix-loop completion
- before handing off to another agent or another thread
- before closing the task

## Low-noise execution rules

- Do not waste context by dumping whole files or long command output into chat.
- Prefer targeted search, targeted reads, and summarized results.
- Redirect large logs to files when needed and reference the file path.
- Put durable reasoning in plan/state artifacts, not ephemeral terminal chatter.
- Re-read the smallest necessary artifact slices when resuming.

## Resume and handoff protocol

A new agent should be able to resume with these steps:

1. read the closest `AGENTS.md`
2. read the current main plan file
3. read the continuation state file
4. read the machine state file if it exists
5. read the phase prompt pack when implementing or reviewing a phase
6. inspect the append-only touched-file log and current remaining work
7. re-open only the files relevant to the active phase
8. continue execution without hidden chat context

Before leaving a task mid-stream, update:

- active phase
- completed work
- remaining next actions
- blockers
- validation status
- touched files
- lane/subagent status
- background jobs
- review verdicts
- any frozen decisions that changed

# State files

State files are durable memory, not a second copy of the full plan.

## Recommended schema

Use `assets/state-template.json` and `assets/continuation-state-template.md` as starter shapes. Keep keys stable when possible.

State should usually include:

- task identity and mode
- status and timestamps
- main plan path
- phase prompt pack path
- continuation state path
- current phase
- completed and pending phases
- frozen decisions and constraints
- phase checklist status
- lane ownership blocks
- background jobs
- validation status
- review evidence
- touched files
- risk list
- handoff summary and next actions
- resume protocol with the main plan as a required read-first file

## Safe-write protocol

This is mandatory when more than one agent or lane may touch coordination files.

1. Re-open the file immediately before writing.
2. For JSON state files, validate parse before patching.
3. Edit only the smallest owned block or append-only log entry.
4. Do not reformat or reorder unrelated sections.
5. Re-parse JSON after writing.
6. If the file is truncated, invalid, unexpectedly changed by another lane, or otherwise suspicious, stop and record a conflict block in the plan.

## Conflict block format

When coordination artifacts become unsafe, add this block to the plan and stop dependent work:

- `file:` exact path
- `issue:` what failed
- `evidence:` command output, timestamp, or parse error
- `impact:` what can no longer be trusted
- `required_unblock:` what must happen before continuing

# Delegated execution and subagents

Codex subagent workflows require explicit authorization from the user. Treat phrases like `allow to use subagents`, `use subagents`, `parallel tasks`, `parallel jobs`, `background task`, or close equivalents as sufficient authorization.

## Spawn criteria

Use subagents or parallel jobs when all of these are true:

- the task has at least two meaningful low-coupling lanes
- each lane has a crisp scope and validation target
- write scopes are disjoint or shared files are parent-owned
- the parent can integrate the results safely
- state and handoff rules are clear enough for a fresh lane context

Avoid subagents when:

- the task is tiny
- most work is one dependency chain
- multiple lanes would fight over the same files
- the main value is a single debug loop with shared state everywhere

## Parent-agent duties

The parent agent must:

- keep the main plan, phase prompt pack, machine state, and continuation state authoritative
- define each lane before spawning: objective, mandatory skills, read scope, write scope, validation target, branch/worktree notes, merge notes
- decide whether a lane is read-only research, implementation, review, or verification
- tell every subagent to follow the same continuity, testing, validation, and state rules inside its lane
- integrate changes, resolve conflicts, and run the final acceptance pass by re-running the full validation gate against the merged tree yourself. A lane's own isolated test run cannot see fallout in files a sibling lane touched; accepting the union of each lane's self-reported "green" status instead of an independent merged-tree run has let real regressions through in this pattern's field use.
- close or redirect broken lanes instead of letting them drift; see `Handling a stalled or silent lane` below for lanes that go quiet rather than fail outright

## Lane design rules

- One concern per lane.
- Prefer read-heavy explorer or researcher lanes for discovery.
- Prefer disjoint-file implementer lanes for code changes.
- Add a reviewer or verifier lane when independent validation materially helps.
- Child lanes must update only their owned blocks in shared artifacts.
- Parent-owned files are never broad-write targets for children.
- Keep fan-out small by default, usually two to four lanes unless the repository and tooling clearly justify more.
- Avoid deeper delegation trees unless the environment already supports and expects them.

## Role selection guidance

When the environment exposes built-in or custom agent roles, prefer this order:

1. explorer or researcher for read-only discovery
2. worker or implementer for scoped code changes
3. reviewer or verifier for independent checking

Do not assume custom roles exist. Use them only if the current environment already exposes them.

## Worktree guidance

If the surface supports worktrees and the parallel lanes have substantial code changes, prefer separate worktrees to reduce shared-write conflicts.

Plan worktrees like this:

- fix branch names in the plan
- do not fix worktree directory names
- keep shared-file wiring in a later integration phase
- give the user suggested commands and commit messages
- do not commit, push, reset, delete, or force-push without explicit permission

## Handling a stalled or silent lane

Neither Codex's ad hoc subagent delegation nor Claude Code's Agent tool enforces an automatic timeout on an ordinary spawned lane -- only Codex's separate `spawn_agents_on_csv` batch tool has a built-in per-worker timeout (`job_max_runtime_seconds`). For a normal delegated lane, the parent agent decides when a lane has gone silent too long; the harness will not decide it for you.

- Set an explicit patience budget before spawning (a turn count, a wall-clock estimate, or "check back after the next validation checkpoint") and state it in the lane's own instructions, so the lane knows the parent may check on it.
- When a lane goes quiet past that budget, close or stop it rather than waiting indefinitely.
- Do not discard whatever the lane already produced. Inspect its actual output and diff first. Safe, validated partial work should be kept and finished serially by the parent, not thrown away just because the lane itself did not finish.
- Finish the remaining scope of a closed lane serially under the parent, using the same write-scope and validation rules the lane was given.
- Record the stall, what was salvaged, and the serial completion in state, the same way a fallback-to-serial decision is recorded below.

Model-specific tendencies affect how often this comes up, not the recovery procedure itself: Opus 4.8 under-spawns subagents by default and needs explicit delegation guidance to fan out at all, while Fable 5 is documented as more reliable than Opus 4.8 at sustaining parallel subagents once spawned. Read the current tuning for whichever model is running the lane in `$alaa-prompting-guide` (Codex) or `/alaa-prompting-guide` (Claude Code) -- `references/11-codex-runtime-features.md`, `references/20-opus-4-8.md`, `references/30-sonnet-5.md`, or `references/40-fable-5.md` -- instead of assuming one model's subagent behavior applies to another.

## Fallback when subagents are unavailable

If the feature is unavailable, disabled, or inappropriate, do not discard the lane design. Keep the same structure in the plan and execute the lanes serially under the parent agent. Record the fallback.

# Review mode

Use `references/review-mode.md` for complete review rules.

At minimum, review mode checks:

- correctness and regressions
- production readiness for high traffic and high concurrency
- security, privacy, trust boundaries, and data handling
- observability, failure behavior, and operability
- performance, resource usage, and cleanup
- clean code, abstractions, architecture, design patterns, and best practices
- tests and validation evidence
- docs impact

Review may recommend refactors beyond the immediate uncommitted change when they materially affect production quality. Mark wider recommendations as out-of-scope unless they are blockers.

# Surface notes

- Codex app may expose `/goal` and plan-mode surfaces for durable objectives.
- Codex CLI may expose `/plan`, `/status`, `/resume`, `/fork`, and feature flags depending on version.
- Claude Code skills can be invoked directly and may run in subagents depending on frontmatter and environment.
- For difficult long tasks, medium or high reasoning is usually a better baseline than low. Use extra-high reasoning only for hard, long-horizon, or architecture-sensitive work.
- On Windows 11 in the Codex app, prefer native PowerShell-safe commands first.

# Final report

Finish with this order unless the user requests another format:

1. `Touched files:`
2. `Summary:` in simple English, plus a Persian summary only if the user expects Persian
3. `Validation:` commands run and results, or why they could not run
4. `State / handoff:` plan path, phase prompt path, continuation state, machine state, and next action
5. `Suggested commit message:`

If your team already has a legacy report label convention, keep that convention only when the repository or user explicitly requires it.

# Anti-patterns

- Writing a vague plan that could fit any repository.
- Creating a plan without a same-stem `__phase-prompts.md` file.
- Producing phase prompts that are generic instead of phase-specific.
- Failing to read the main plan before resume, review, delegation, or execution.
- Letting progress live only in chat instead of plan/state artifacts.
- Reopening settled architecture without a concrete contradiction.
- Dumping long logs or full file contents into chat.
- Rewriting shared state files end-to-end during delegated work.
- Spawning subagents just because the user allowed it, without a real lane split.
- Letting subagents edit parent-owned plan/state/phase-prompt files broadly.
- Advancing to the next phase before current validation passes or a blocker is recorded.
- Treating the final docs alignment phase as optional.
- Writing reviews that reassure without gate evidence.
- Approving tests that hard-code the implementation or would pass against broken behavior.
