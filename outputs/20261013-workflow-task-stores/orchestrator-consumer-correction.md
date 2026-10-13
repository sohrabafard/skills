# Orchestrator consumer correction

Status: pre-edit baseline excerpts. Parent-approved scope: only A9, B2, B6, E6 and the final-success item in each listed reference.

Compression decision: rule-writer examined all five replacements; parent accepted A9/B6/E6/final-success and retained the B2 draft because its proposed rewrite muddled phase-barrier ownership and the capacity-observation condition. No new task-selection, resource, role or permission policy.

Required reading: both skill bodies, all references and scripts read; identical mirrored references/runners reused after hash equality, related script parity checked by native diff. CodeGraph was reached first for all scripts in this same worktree; elided code and unindexed PowerShell/shell source used bounded native continuation. No embedded commands executed.

## Before: skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md

9. Write the plan down through `/alaa-workflow` at the `resumable` profile, or adopt the parent plan when a workflow parent already exists. That plan is the run's single checklist — ordered phases, one checkbox per subtask, acceptance criteria, per-phase validation commands, and the handoff package — and it is where the main thread reads its own position back after compaction. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Tick a box once its outcome has been observed and never ahead of the evidence — several at once when one change satisfied several, and at the start for a subtask that turns out to be already done and was verified rather than assumed. `/alaa-workflow` owns the plan and state machinery; this skill consumes it and does not recreate it.

2. Consume the workflow plan's dependency, ownership, resource-conflict and integration-barrier fields. A lane is ready only after required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit; increase parallel writers when capacity and ready work justify it. Record an unavailable capacity observation and use the smallest supported batch until capacity is established; do not invent a ceiling or assume unlimited capacity.

6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record each completed subtask and tick its box in the plan. Commit it only with explicit user permission.

6. Re-check final git status and diff against declared scopes, confirm every plan checkbox matches what actually landed, and record the last authorized commit timestamp when available; otherwise record unavailable.

- every plan checkbox matches what actually landed, and every changed subtask carries a reviewed diff and evidence, plus a commit only when authorized;


## Before: skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md

9. Write the plan down through `/alaa-workflow` at the `resumable` profile, or adopt the parent plan when a workflow parent already exists. That plan is the run's single checklist — ordered phases, one checkbox per subtask, acceptance criteria, per-phase validation commands, and the handoff package — and it is where the lead reads its own position back after compaction. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Tick a box once its outcome has been observed and never ahead of the evidence — several at once when one change satisfied several, and at the start for a subtask that turns out to be already done and was verified rather than assumed. `/alaa-workflow` owns the plan and state machinery; this skill consumes it and does not recreate it.

2. Consume the workflow plan's dependency, ownership, resource-conflict and integration-barrier fields. A lane is ready only after required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit; increase parallel writers when capacity and ready work justify it. Record an unavailable capacity observation and use the smallest supported batch until capacity is established; do not invent a ceiling or assume unlimited capacity.

6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record each completed subtask and tick its box in the plan. Commit it only with explicit user permission.

6. Re-check final git status and diff against declared scopes, confirm every plan checkbox matches what actually landed, and record the last authorized commit timestamp when available; otherwise record unavailable.

- every plan checkbox matches what actually landed, and every changed subtask carries a reviewed diff and evidence, plus a commit only when authorized;


## After: skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md

9. Write the plan through `/alaa-workflow` at the `resumable` profile or adopt the existing parent plan. It records ordered phases, acceptance, per-phase validation, and handoff knowledge. Follow `alaa-workflow references/task-tracking.md` for selected-store task records and evidence-based progress; use `alaa-workflow references/context-continuity.md` for canonical position and resume. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Workflow owns this machinery; the orchestrator consumes it without duplicating task state.

2. Consume dependencies/readiness from the selected task authority and phase barriers, write ownership and shared-resource conflicts from the workflow plan. A lane is ready only after required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit; increase parallel writers when capacity and ready work justify it. Record an unavailable capacity observation and use the smallest supported batch until capacity is established; do not invent a ceiling or assume unlimited capacity.

6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record observed task progress, with evidence, through the authority selected by `alaa-workflow references/task-tracking.md`. Commit only with explicit user permission.

6. Re-check final Git status and diff against declared scopes; confirm canonical task progress and workflow status match what landed; record the last authorized commit timestamp when available, otherwise record it as unavailable.

- canonical task progress and workflow status match what landed; every changed subtask has a reviewed diff and evidence; commit only when authorized;


## After: skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md

9. Write the plan through `/alaa-workflow` at the `resumable` profile or adopt the existing parent plan. It records ordered phases, acceptance, per-phase validation, and handoff knowledge. Follow `alaa-workflow references/task-tracking.md` for selected-store task records and evidence-based progress; use `alaa-workflow references/context-continuity.md` for canonical position and resume. Apply `alaa-workflow references/companion-routing.md` for executable phase/task skill bindings before implementation or write-lane dispatch. Workflow owns this machinery; the orchestrator consumes it without duplicating task state.

2. Consume dependencies/readiness from the selected task authority and phase barriers, write ownership and shared-resource conflicts from the workflow plan. A lane is ready only after required dependency contracts are reconciled. Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit; increase parallel writers when capacity and ready work justify it. Record an unavailable capacity observation and use the smallest supported batch until capacity is established; do not invent a ceiling or assume unlimited capacity.

6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Record observed task progress, with evidence, through the authority selected by `alaa-workflow references/task-tracking.md`. Commit only with explicit user permission.

6. Re-check final Git status and diff against declared scopes; confirm canonical task progress and workflow status match what landed; record the last authorized commit timestamp when available, otherwise record it as unavailable.

- canonical task progress and workflow status match what landed; every changed subtask has a reviewed diff and evidence; commit only when authorized;

