---
name: alaa-workflow
description: "Plan before implementation. Use a compact plan for bounded work and a complete durable plan for multi-phase, resumable, delegated, or handoff-sensitive work. Prefer Beads-native execution plans with exact phase/task skills; keep admitted Markdown families and file consumers. Plan-only authorizes planning only. Respect native Plan Mode and explicit no-file, read-only, or chat-only limits. Short advice and ordinary review need no execution plan."
---

# Alaa Workflow

Plan before every implementation. Make long work resumable without imposing orchestration on bounded work. Use one plan authority and one task store per task.

## Start

1. Read repository instructions and every user-named read-first artifact.
2. If a plan already exists, read it before execution, resume, delegation, review, or handoff. Follow the resume protocol in `references/context-continuity.md`.
3. When `/alaa-memory-os` says its trigger holds, invoke it before planning from prior context or publishing durable knowledge. Memory may contribute verified leads. It never owns this workflow's plan, checkpoint, evidence, or handoff.
4. Before the first non-trivial repository discovery or code-evidence choice, invoke `/alaa-code-intelligence-routing` once. Reuse its routed result instead of retrieving the same fact through a second surface.
5. Pair with `/alaa-low-noise` and the narrowest domain skill needed for technical decisions. Before designing implementation or verification, load `/alaa-testing-strategy`.
6. Before writing, resolve plan kind, approval and artifact/profile admission through `references/artifact-lifecycle.md`. Resolve Beads availability, execution task authority and evidence through `references/task-tracking.md`. Resolve exact skill bindings through `references/companion-routing.md`.

## Select the planning route

Select kind, authority, medium and plan size through `references/artifact-lifecycle.md`. Use its initializer only for an admitted Markdown family. For a Beads-native plan, register and verify the issue graph through `references/task-tracking.md` before dependent execution.

## Survive compaction and handoff

`references/context-continuity.md` owns position, handoff, event-driven updates and the cold-start test. Follow its resume protocol after context loss.

## Execute and resume

This section applies to execution engagements and issue-only implementation.

- Work through the selected task authority and any admitted plan; apply the resume protocol after interruption, compaction, or a branch or worktree change.
- Apply the execution hierarchy and task authority in `references/task-tracking.md` before dependent work.
- Bring canonical workflow/task owners and derived snapshots current before the next phase, handoff, or report.
- Record the engagement's review boundary and final phase. Pass them into nested orchestration. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own cadence scheduling.
- Record phase test-collection, repair/retest and inherited review barriers in the plan through `references/artifact-lifecycle.md`.
  Route generic execution and the early-repair exception to /alaa-testing-strategy `references/100-test-execution.md`. The runtime orchestrators own phase/review scheduling and independent observers through the cadence owner above.
- Fix defects and retest the failing path within the active retry budget. Never weaken assertions, hard-code expected results, suppress findings or lower review standards. Record an unresolved blocker and next safe action. Continue independent safe work.
- On resume, follow the read order in `references/context-continuity.md` before taking any action.
- Complete only when implementation, validation evidence, documentation, artifact status, and the final reusable-context curation outcome agree.
- Report completion as four independent states — `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` — each with its own verdict, never collapsed into a single one. This skill owns that lifecycle for execution runs. `references/workspace-and-integration.md` owns what earns each state.

## Preserve workspace evidence

Before writing, identify the base, checkout and unrelated changes through `references/workspace-and-integration.md`. It owns write isolation, execution evidence snapshots and authorized Git integration.

## Curate reusable context

For execution completion and signal-bearing boundaries, apply `/alaa-extract-agent-lessons` through `references/context-curation.md`. It owns intermediate signal triggers, the mandatory final full-engagement gate, recording locations and pipeline reopening. Curation grants no additional artifact or publication authority.

## Delegate selectively

Delegate only genuinely independent work with disjoint write scopes, or high-volume exploration whose output should stay isolated. Keep shared-context phases in the main conversation when they need frequent coordination or latency matters.

A dispatch is a one-way context wall. `references/context-continuity.md` covers what that requires of the dispatch text and the return.

The parent owns the plan, integration, conflict resolution and final validation. Reconcile combined evidence through `references/workspace-and-integration.md` before deciding what still needs a run. Put lane ownership inside the parent plan or dispatch. Do not create a separate lane-plan artifact.

A phase that is itself one bounded goal with parallel role lanes may be executed by invoking `/alaa-codex-orchestrator` in Codex or `/alaa-cc-orchestrator` in Claude Code for that phase. The workflow parent still owns the plan, integration, and evidence recording. It records the orchestrator's final report as the phase evidence. Keep simple phases direct. Do not stack both orchestration layers on work one agent can finish.

## Generate prompts only on request

Start from `assets/phase-prompts-template.md`. `references/phase-prompts.md` owns roles, six-field shape, word target and its exceptions. Review prompts inherit the declared engagement boundary.

Before resolving any runtime name, model name, effort level, feature syntax, or skill-trigger syntax, load `/alaa-prompting-guide` and verify current official documentation. `references/phase-prompts.md` owns the freshness gate, the role definitions, and where a resolved value is allowed to live.

## Review

Review the requested surface directly. Lead with actionable findings and exact evidence. Create workflow artifacts only when explicitly requested or when a continuing fix loop needs them. `references/review-mode.md` owns the evidence order, the must-check areas, the verdict vocabulary a phase can hand across a lane boundary, and finding triage before any fix.

## Validate the workflow record

For Beads-native work, verify the bound record through `references/task-tracking.md`. For Markdown, use the offline validator in `references/artifact-lifecycle.md`. An issue-only or session plan needs no workflow file to validate. Record required behavior evidence at its task owner.

## When NOT to use

`references/artifact-lifecycle.md` owns artifact admission and its exceptions; activation alone never authorizes product execution.

## Direct references

This skill owns coordination and continuity, not architecture, security, data, runtime, frontend, infrastructure, or documentation rules. This table selects references. Their named sections own the detailed procedures.

| You are about to | Read |
|---|---|
| Begin a long run, hand off (including to another PC), resume, or find you cannot name your own current position | `references/context-continuity.md` |
| Choose plan size, medium, design or execution authority, or continue an existing family | `references/artifact-lifecycle.md` |
| Resolve execution hierarchy, test Beads availability, select or migrate a task store, decide where task information, acceptance or evidence lives, write issue fields or a close reason, link a follow-up or cross-project dependency, assign/resume/transfer an agent's Beads identity or issue ownership, resolve readiness, or encounter a Beads outage or uncertain update | `references/task-tracking.md` |
| Make the first write of a multi-phase or delegated run, record an evidence snapshot, exercise authorized Git integration, or state which completion states a finished run reached | `references/workspace-and-integration.md` |
| Reach an execution phase or decision boundary with a curation signal, or prepare execution completion | `references/context-curation.md` |
| Generate a prompt pack, or resolve a runtime, model, or effort value for one | `references/phase-prompts.md` |
| Review a diff, plan, or artifact instead of executing one | `references/review-mode.md` |
| Take a technical decision this skill does not own — architecture, security, data, testing depth, frontend, infrastructure, or documentation | `references/companion-routing.md` |
