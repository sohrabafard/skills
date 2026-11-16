---
name: alaa-workflow
description: "Planning and continuity workflow for agent work: compact or durable execution plans, Beads task tracking, handoff and resume. Use to plan before implementation, track tasks in Beads, resume after compaction or a restart, or hand work to another agent or PC. Use a compact plan for bounded work and a complete durable plan for multi-phase, resumable, delegated, or handoff-sensitive work. Prefer Beads-native execution plans with exact phase/task skills; keep admitted Markdown families and file consumers. Plan-only authorizes planning only. Respect native Plan Mode and explicit no-file, read-only, or chat-only limits. Short advice and ordinary review need no execution plan. Do not use it to publish durable knowledge, which /alaa-memory-os owns."
---

# Alaa Workflow

Plan before every implementation. Make long work resumable without imposing orchestration on bounded work. Use one plan authority and one task store per task.

## Start

1. Read every artifact that the user names as read-first.
2. Read an existing plan before execution, resume, delegation, review or handoff. After context loss, interruption, compaction, or a branch or worktree change, apply the resume protocol in `references/context-continuity.md` before any other action.
3. When the `/alaa-memory-os` trigger holds, invoke it before you plan from prior context or publish durable knowledge. Memory supplies leads to verify. It never owns this workflow's plan, checkpoint, evidence or handoff.
4. Invoke `/alaa-code-intelligence-routing` once before the first non-trivial repository discovery or code-evidence choice, and reuse its result.
5. Before planning, apply Mandatory Ponytail binding in `references/companion-routing.md`, including its user opt-out. Load `/alaa-low-noise` and the narrowest domain skill for each technical decision. Load `/alaa-testing-strategy` before you design implementation or verification.
6. Before writing, resolve plan kind, approval, admission and profile through `references/artifact-lifecycle.md`. Resolve Beads availability, task authority and evidence through `references/task-tracking.md`. Resolve exact skill bindings through `references/companion-routing.md`.
7. Before the first write, identify the base, the checkout and unrelated changes through `references/workspace-and-integration.md`.

## Execute and resume

This section applies to execution engagements and issue-only implementation.

- Work through the selected task authority and the admitted plan. Apply the hierarchy in `references/task-tracking.md` before dependent work.
- Bring the task and workflow owners and their snapshots current before the next phase, handoff or report.
- Record the engagement's review boundary and final phase, and pass them into nested orchestration. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` schedule phases, reviews and independent observers.
- Record phase test-collection, repair/retest and review barriers in the plan through `references/artifact-lifecycle.md`.
- Before you run, repair or retest a check, apply /alaa-testing-strategy and read its `references/100-test-execution.md`. That skill owns collection, the early-repair exception and the rule against weakening an assertion.
- Record an unresolved blocker with its next safe action, and continue independent safe work.
- At a boundary that carries a curation signal, and before completion, apply `references/context-curation.md`. Curation grants no artifact or publication authority.
- Before handoff and completion, verify a Beads-native record through `references/task-tracking.md`, or run the offline validator in `references/artifact-lifecycle.md` for a Markdown family.
- Complete only when implementation, validation evidence, documentation, artifact status and the final curation outcome agree.
- Report completion as four independent states, `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE` and `PUBLISHED`, each with its own verdict. Never collapse them into one. `references/workspace-and-integration.md` defines what earns each state.

## Delegate selectively

Delegate only independent work with disjoint write scopes, or high-volume exploration whose output should stay isolated. Keep a phase in the main conversation when it needs frequent coordination or low latency.

The parent owns the plan, integration, conflict resolution and final validation. Record lane ownership in the parent plan or the dispatch, and create no lane-plan file. Write each dispatch under `references/context-continuity.md` `## Delegation is a context boundary`. Reconcile the combined evidence through `references/workspace-and-integration.md` before you decide what still needs a run.

A phase that is one bounded goal with parallel role lanes may run through `/alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code. Record the orchestrator's final report as the phase evidence. Never add an orchestrator to work that one agent can finish.

## Generate prompts only on request

Generate a prompt pack only on explicit request, from `assets/phase-prompts-template.md` under `references/phase-prompts.md`. Apply its freshness gate before you resolve a runtime name, model name, effort level, feature syntax or skill-trigger syntax.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence. Create workflow artifacts only on explicit request or for a continuing fix loop. Follow `references/review-mode.md` for the must-check areas, the verdicts and the finding triage that precedes any fix.

## When NOT to use

Advice and ordinary review need no execution plan; `references/artifact-lifecycle.md` decides admission. Activation never authorizes product execution.

## Direct references

| You are about to | Read |
|---|---|
| Begin a long run, hand off (including to another PC), resume, or continue after compaction, interruption or a branch or worktree change, or you cannot name your current position | `references/context-continuity.md` |
| Choose plan size, medium, design or execution authority, or continue an existing family | `references/artifact-lifecycle.md` |
| Resolve the execution hierarchy, test Beads availability, select or migrate a task store, decide where task information, acceptance or evidence lives, write issue fields or a close reason, link a follow-up or cross-project dependency, assign, resume or transfer a Beads identity or issue ownership, resolve readiness, or meet a Beads outage or uncertain update | `references/task-tracking.md` |
| Make the first write of a multi-phase or delegated run, record an evidence snapshot, use authorized Git integration, or state which completion states a run reached | `references/workspace-and-integration.md` |
| Reach an execution phase or decision boundary with a curation signal, or prepare execution completion | `references/context-curation.md` |
| Generate a prompt pack, or resolve a runtime, model or effort value for one | `references/phase-prompts.md` |
| Review a diff, plan or artifact instead of executing one | `references/review-mode.md` |
| Resolve the required Ponytail mode or a user opt-out, or take a companion-owned decision about architecture, security, data, testing depth, frontend, infrastructure or documentation | `references/companion-routing.md` |
