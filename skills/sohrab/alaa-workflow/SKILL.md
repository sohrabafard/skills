---
name: alaa-workflow
description: Use this skill for long-running, multi-phase, plan-mode, review-mode, resume, handoff, or delegated repository work that needs durable plan/state/phase-prompt artifacts, compaction-safe memory, mandatory main-plan re-read, subagent or parallel-lane orchestration, test-first execution, final documentation alignment, or GPT-5.5 Codex implementation plus Opus review prompts. Do not use it for tiny single-file edits, short read-only answers, or narrow domain work that does not need long-horizon coordination.
---

# Alaa Workflow

This skill is the workflow operating system for long tasks. It owns planning discipline, durable memory, orchestration, review cadence, handoff safety, and final reconciliation. It does not replace domain-specific skills.

## Core invariants

- Use simple, fluent English with complete sentences for plans, prompts, state notes, reviews, and final reports.
- For any non-trivial plan, execution, resume, delegated, or review run, keep durable repo-local memory. Do not let critical context live only in chat.
- The main plan is the source of truth. Read it before executing, reviewing, resuming, delegating, or integrating work.
- Draft first, then rewrite the user-facing artifact into a clean final version. Preserve every material detail from the draft; remove scratch wording unless the user asked to see it.
- Treat tests, validation commands, review evidence, and state artifacts as part of the work, not optional follow-up.
- Pair with narrower Alaa skills for stack-specific judgment.

## Use this skill when

- The user asks for a detailed plan, enters plan mode, asks for an implementation prompt pack, or wants work from an existing plan.
- The task is large enough that context drift, compaction, resumability, or phased execution matters.
- The task spans multiple files, contracts, tests, migrations, packages, infrastructure, rollout risk, or documentation.
- The user authorizes subagents, parallel lanes, background jobs, worktrees, or handoff to another agent.
- The user asks for review mode or production-readiness review of a behavior-changing change.

## When NOT to use

- The task is a tiny edit with no coordination cost.
- The task is read-only and does not need durable artifacts.
- A narrower domain skill can handle the task directly without long-horizon workflow overhead.

## Start sequence

1. Read repo-local `AGENTS.md` and any closer agent instructions first.
2. If a main plan already exists or is named by the user, read it as a blocking precondition before planning, execution, review, resume, or delegation.
3. If the user names a Codex goal objective file, phase-prompt file, state file, issue, PR, or ordered "read first" source list, read it as a blocking precondition.
4. Pair with `$alaa-low-noise` for any non-trivial run.
5. Read `references/00-topic-map.md`, then only the smallest relevant reference sections.
6. Decide the workflow mode: `plan`, `execute`, `resume`, `delegated`, or `review`.
7. Route to the correct companion skill before making domain-sensitive decisions.
8. Create or continue workflow artifacts unless the user or environment forbids file creation. If artifacts are blocked, record the blocked path and use the closest writable fallback.

## Required artifact set

For every parent plan created by this skill, create these artifacts with the same stem:

- Main plan: `docs/_agent_plans/<stem>.md` or `docs/plan/<stem>.md`.
- Phase prompt pack: same directory and stem, `<stem>__phase-prompts.md`.
- Human continuation state: `docs/agents/<stem>-state.md`.
- Machine state when writable: `.codex/state/<stem>.json`.

Keep these path families stable:

- `.codex/state/*.json`
- `docs/agents/*`
- `docs/plan/*`
- `docs/_agent_plans/*`

If an in-flight task already uses one of these families, continue that family and stem. Do not migrate it mid-task.

Use `assets/plan-template.md`, `assets/phase-prompts-template.md`, `assets/continuation-state-template.md`, and `assets/state-template.json` unless an in-flight task already has a stronger compatible structure.

## Plan mode contract

When planning, produce an implementation-ready plan, not a conceptual outline. Read `references/full-guide.md#plan-mode` and `assets/plan-template.md`.

A valid plan must include:

- `## Summary` near the top, explaining the topic, target outcome, and main strategy.
- Repository-grounded facts: what is already good, what gaps remain, what must change now, and what is intentionally deferred.
- Phase-by-phase execution with dependencies, safe parallel lanes, and a serial integration phase when lanes converge.
- For every phase: mandatory skills, exact files or surfaces, task checklist, test-first checklist, validation checklist, acceptance criteria, risks, and completion signal.
- For every task that changes behavior: test files or validation fixtures to write or update before or with implementation.
- A final phase that aligns all affected documentation, guides, contracts, runbooks, API docs, and project overview files.
- Worktree and branch guidance when parallel implementation is useful: fix branch names, not worktree directory names; include merge/integration assumptions; provide suggested git commands and commit messages for the user, but do not commit, push, deploy, or run destructive Git commands without explicit permission.
- A same-stem `__phase-prompts.md` companion file with Codex/GPT implementation prompts and Opus review prompts for each phase.

## Phase prompt pack contract

For every plan, create `<stem>__phase-prompts.md`. Read `references/phase-prompts.md` and use `assets/phase-prompts-template.md`.

The pack must assume two agents unless the user says otherwise:

- GPT-5.5/Codex for implementation, optimized for `/goal` or pursue-goal execution.
- Claude Opus 4.8 for expert review.

For every phase, include:

- required read-first files, state files, and mandatory skills
- a Codex `/goal` implementation prompt with one durable objective, a verifiable end state, scope boundaries, validation commands, compact checkpoint reporting, and explicit permission to use subagents/parallel jobs when write scopes are disjoint
- an Opus review prompt using clear XML-style structure, concrete must-check criteria, gate evidence, and a verdict format
- a fix-loop prompt for feeding review findings back into implementation
- notes for parallel worktrees when the plan supports concurrent branches, with branch names fixed and worktree paths left flexible

## Execution and resume contract

Treat the main plan as the runbook. Read it before doing work, after compaction, after interruption, after branch/worktree switch, and before delegating or reviewing a phase.

During execution:

- update `.codex/state/<stem>.json` and `docs/agents/<stem>-state.md` after artifact creation, phase start, lane dispatch, meaningful decision freeze, blocker, before long validation, after validation, phase completion, and handoff
- keep checklists current by ticking completed items in the plan or state file
- run phase validation before moving forward
- repair failures before declaring the phase done
- record exact blockers, attempted fixes, validation evidence, and next actions
- ensure another agent can continue from files alone without hidden chat context

If `.codex/state` is blocked, use `docs/agents/<stem>-state.md` as the writable fallback and record the intended JSON path plus the exact blocker.

## Subagents, parallel lanes, and background jobs

Treat explicit phrases such as `allow subagents`, `use subagents`, `parallelize this`, `background tasks`, `parallel jobs`, or close equivalents as authorization to use them.

Use subagents or parallel jobs when the task has independent lanes with disjoint write scopes, separate validation targets, or isolated review/research value. The parent agent remains the orchestrator and owns:

- the main plan, phase prompt pack, machine state, and continuation state
- lane design, branch/worktree assumptions, read/write scope, and mandatory skills
- integration, conflict resolution, an independent full-gate re-validation of the merged result (not just each lane's own reported status), and final report
- closing, redirecting, marking broken lanes blocked, or recovering a stalled/silent lane by finishing its scope serially without discarding safe in-progress work

Every subagent prompt must be self-contained. It must name the main plan, current state files, phase objective, mandatory skills, read scope, write scope, tests to write, validation commands, checklists to update, and the rule that the subagent must preserve the same state/continuity discipline inside its lane. Subagents must not edit parent-owned plan/state/phase-prompt files unless the parent explicitly assigns a narrow append-only block.

If subagents, background jobs, or worktrees are unavailable or not worth the overhead, keep the same lane design and execute it serially under the parent agent. Record the fallback.

## Review mode contract

Use review mode when the user asks to review code, plans, phases, PRs, diffs, or production readiness. Read `references/review-mode.md`.

A valid review must include the standard review checks plus these Alaa-specific checks:

- bug-free behavior, production readiness, security sensitivity, observability, performance, high-traffic suitability, concurrency safety, reliability, and failure behavior
- clean code, good abstractions, architecture, boundaries, best practices, and design patterns
- tests that prove behavior rather than implementation details; reject hard-coded or test-special-cased solutions
- recommendations beyond the exact diff when architecture or refactor quality materially affects production quality; label out-of-scope recommendations clearly instead of ignoring them
- exact gate evidence: commands run, results, or why the gate could not be run

Return a verdict and concrete findings with file paths and lines when available. Do not reassure without evidence.

## Companion routing

This skill handles workflow, not domain ownership. Read `references/companion-routing.md` and actively pair with the right stack skill before architecture, security, runtime, data, frontend, infrastructure, or documentation decisions.

## Windows and Codex surface notes

This skill should work in Codex app, CLI, and IDE environments. Optimize shell examples for Windows 11 + native PowerShell when the environment is Windows. Use `references/windows-powershell.md` for PowerShell-safe commands and artifact validation.

## Useful bundled files

- `assets/plan-template.md` - parent plan skeleton with required headings and checklists
- `assets/lane-plan-template.md` - child-lane plan skeleton
- `assets/phase-prompts-template.md` - same-stem implementation/review prompt pack skeleton
- `assets/continuation-state-template.md` - human-readable continuation state skeleton
- `assets/state-template.json` - machine-readable state schema starter
- `scripts/init_workflow_files.py` - deterministic artifact bootstrapper
- `scripts/validate_workflow_files.py` - plan/state/phase-prompt validator

## Completion standard

A run is not done when code has changed. It is done when the plan, phase prompts, state files, validations, remaining work, docs, and final report agree.

Before finishing:

- reconcile plan vs. actual work
- tick completed checklist items and mark remaining, deferred, blocked, or cancelled work clearly
- update state files so a fresh agent can resume
- confirm docs alignment was completed or explicitly blocked
- produce the final report in the order defined in `references/full-guide.md`

## Reference navigation

- `references/00-topic-map.md` - smallest useful reading path
- `references/90-source-map.md` - official-first source map, freshness triggers, and model-use notes
- `references/full-guide.md` - detailed operating rules
- `references/phase-prompts.md` - Codex `/goal` and Opus review prompt pack rules
- `references/review-mode.md` - production review rules and output format
- `references/companion-routing.md` - ecosystem pairing map
- `references/windows-powershell.md` - native Windows and PowerShell patterns
