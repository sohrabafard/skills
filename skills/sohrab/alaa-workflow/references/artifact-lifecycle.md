# Artifact Admission and Lifecycle

Use the smallest artifact set with a real consumer.

## Admission

An actionable implementation/execution-plan request authorizes a saved plan and checkpoint without a separate request to save them. Authorized multi-phase, resumable, or delegated execution saves them before implementation or write-lane dispatch. A plan-only request authorizes these planning artifacts, never product implementation.

Explicit no-file, read-only, or chat-only limits prevail. Native Plan Mode uses only its host-permitted planning surface until execution is approved; then materialize the admitted artifact family before implementation. Short advisory answers, ordinary review, and small bounded single-phase edits create no workflow files unless requested. A continuing authorized fix loop follows execution admission.

When an admitted family exists, update it instead of creating another. Before execution, fill ordered phases and store-appropriate task mappings, dependencies, ownership, exclusions, phase acceptance, validation, resume context, and skill bindings; task acceptance and results follow `references/task-tracking.md` `## Acceptance and evidence by level`. `references/task-tracking.md` owns task authority; `references/companion-routing.md` owns skill bindings. Report saved plan/checkpoint paths; prose alone does not satisfy admitted durable planning.

## Profiles

| Profile | Plan | Checkpoint | JSON state | Prompt pack | Use for |
|---|---:|---:|---:|---:|---|
| `direct` | required | no | no | opt-in | Genuinely single-phase, bounded work |
| `resumable` | required | required | no | opt-in | **Default.** Anything multi-phase |
| `orchestrated` | required | required | required | opt-in | An automated consumer parses the state |
| `legacy` | required | required | required | required | An old four-file consumer requires it |

Use `resumable` for multi-phase work: event-driven checkpoints preserve position without repeating discovery after interruption. Choose `direct` deliberately for genuinely single-phase bounded work; it accepts rediscovery after interruption. No profile promises a fixed checkpoint size or update count.

Apply admission before selecting a profile; no profile overrides its exceptions. An actionable execution-plan request uses `resumable` unless a real consumer requires a heavier profile.

## Size and consolidate the plan

Classify each phase and delegated lane before execution: missing facts to retrieve or clarify; mechanical work with settled decisions; bounded semantic judgment with a local causal path and decisive acceptance evidence; ordinary engineering judgment; or coupled judgment with interacting unresolved decisions. Record the reason, settled/open decisions and invariants. Assess risk separately: sensitivity determines gates, not reasoning complexity. The runtime orchestrator owns actual task model/effort allocation; `/alaa-prompting-guide` supplies capabilities and runtime mechanics. Planning effort never determines worker effort.

Merge phases or tasks sharing context, ownership and a validation barrier when separation buys no decision or authority boundary. Preserve every acceptance outcome, evidence mapping, dependency, exclusion and required observer. Keep phases separate when a decision, changed tested state, independent authority or integration barrier requires it; record why. `references/workspace-and-integration.md` owns shared-check coverage and evidence reuse.

After finalizing tasks, dependencies and consolidation, route allocation for EVERY role through the active runtime orchestrator.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Workflow records task scope/complexity, priority/reason, role authority identity, explicit model AND effort, source/evidence, invocation surface, requested/effective controls, availability and limits alongside conflict barriers and references to the selected store's readiness; it chooses no role-based pair. Material changes reassess only affected remaining tasks; never replay completed work.

## Dependency and concurrency plan

Use the selected task authority for dependency edges and ready sets through `references/task-tracking.md`. Each lane names disjoint write ownership, shared-resource conflicts (including fixtures, generators, ports and test environments), integration barriers and parallel/serialized rationale. Disjoint files alone do not prove independence. Keep coupled decisions together; serialize overlapping writes and conflicting resources.

Expose independently ready work to the runtime orchestrator; impose no workflow-wide writer limit. It owns observed capacity, dispatch mechanics and resource scheduling. Query/reconcile readiness at completion, scope-change or handoff boundaries; keep no persistent second ready-set cache or scheduler artifact.

## Paths and correlation

- Plan: `docs/_agent_plans/<stem>.md`, or `docs/plan/<stem>.md` when that family already exists.
- Prompt pack: same plan directory, `<stem>__phase-prompts.md`.
- Checkpoint: `docs/agents/<stem>-state.md`.
- JSON state: `.codex/state/<stem>.json`.

Continue an active task's existing family and stem. Resolve companions only from explicit references or this selected stem; never attach an unrelated newest file.

## Permitted contents

`references/context-continuity.md` owns why the artifacts divide the way they do, what each handoff field means, and when a field earns a line. This file owns only where each artifact lives and what it is permitted to contain.

The plan contains outcome/scope, phase design and barriers, phase acceptance, integrated-review evidence, skill associations, and the handoff package; task acceptance and results live per `references/task-tracking.md` `## Acceptance and evidence by level`. Task progress/dependencies follow `references/task-tracking.md`; status and cursor ownership follow `references/context-continuity.md`.

The handoff package is a section inside the plan, not a separate file — knowledge is only useful next to the route it belongs to, and a fourth file is a fourth thing to keep honest. Its six fields are fixed; keep an unused one empty rather than deleting it, because a deleted field reads as a field nobody had anything to put in.

The checkpoint contains only status, current phase, last verified result, blockers, next action, touched surfaces, update time, and, for a cross-PC handoff, the record `references/context-continuity.md` defines.

JSON contains only schema version, task identity, status, plan path, current phase, next actions, blockers, last validation (a pointer to its evidence owner, not a copy), and update time.

## Update events

`references/context-continuity.md` owns all update events, canonical status/cursor ownership and snapshot derivation. Update only the admitted artifact set; keep expensive learning in the handoff package rather than a position snapshot.

Do not maintain duplicate phase checklists, review history, lane definitions, documentation status, or touched-file histories in secondary state.

## Resume and handoff

`references/context-continuity.md` owns the read order, the cold-start test, the post-compaction rules, and what a handoff must contain. Do not restate them here.

## Delegation

`SKILL.md` owns which work may be delegated and what the parent stays responsible for. One artifact rule belongs here: record lane ownership in the parent plan or delegated prompt, never a lane-plan file. A second plan splits the workflow destination in two; task-store ownership remains separate.

## Compatibility

`--with-state`, `--state-only`, `--no-continuation`, `--lane`, `--parent-plan`, and `--mode` remain available for one transition period and emit deprecation warnings when they alter profile behavior. Use `--profile legacy` when an old consumer requires four files.

Completed legacy artifacts remain historical evidence. Validate them with warnings; do not rewrite them unless they become actively executable.
