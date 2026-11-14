# Artifact Admission and Lifecycle

Choose the smallest plan that preserves authority, acceptance and recovery.

## Admission

Before any implementation, record the outcome, scope, settled approach, prerequisites, exact skill bindings, acceptance and focused checks. For bounded single-phase work, keep this compact plan in the bound task issue when Beads is available, or in the session if durable tracking is unnecessary. See `references/task-tracking.md` for availability and tracking triggers. Advice and ordinary review require no execution plan.

Authorized multi-phase, resumable, delegated or handoff-sensitive work, including a continuing fix loop, requires a complete durable execution plan before dependent implementation or write-lane dispatch. Continue an existing family's contract. For a new eligible execution with available bound Beads, use the native family in `references/task-tracking.md`. Use a Markdown family when Beads is unavailable at admission or an explicit file request or file-consuming tool requires one. Record the file consumer. Use one canonical plan.

A design-plan or execution-plan request authorizes saving the admitted planning deliverable. Plan-only uses the admitted Markdown or host planning surface and authorizes no implementation. Explicit no-file, read-only or chat-only limits prevail. Native Plan Mode uses only its host-permitted planning surface until execution is approved. A native plan file opens with a Persian decision summary (overall picture, goals, open questions), then a line containing only `<!-- design-body -->`, then the complete English design. Use that file as the approved design source after approval. If a higher-priority limit prevents a required durable record, report the gap and pause dependent work.

Report the saved `beads:<root-id>` or plan/checkpoint paths. A session outline cannot satisfy durable admission.

## Plan kinds and approval

Every durable plan declares `Plan kind: design` or `Plan kind: execution`. Existing unmarked families retain their recorded authority and kind.

A **design** plan discusses ideas, alternatives and algorithms before implementation. It always uses `Task store: local` and `Profile: resumable`, with no Beads binding, issue registration, phase, task or subtask hierarchy, executable checklist, prompt pack or machine state. Keep outcome, scope, proposed design, acceptance criteria, `## Decisions` with `Date | Owner | Decision | Reason`, and `## Open Questions`. Date and attribute each decision and its reason. `references/context-continuity.md` owns its required handoff package and checkpoint. Stop design work by presenting the design for explicit user approval; do not dispatch implementation from it.

The design header records `Approval status: pending|approved`, `Approval by`, `Approval on`, and `Approval evidence`. Pending values remain explicit. Approval requires an identifiable approver, a valid ISO date and evidence of the user's approval of this design and scope. Do not infer approval from file creation, schema success or a request to discuss the design. A material change to an approved design returns affected decisions to pending approval before dependent execution.

An **execution** plan admits implementation only with execution authority and settled design. Record actual design approval with its source and scope when required or obtained. Where the implementation request delegates design decisions, record that request, authorized scope, and decision owner separately. Resolve and record those decisions before dependent work. Delegation is no evidence of human design approval. Unresolved human-only decisions, pending required approval, or changes outside the approved scope block dependent work. Neither an issue nor offline validation authenticates authority.

For Markdown execution with an approved separate design, set `Approved design` to its readable portable path and resolve its approval before execution. For a design approved in the current session, use a **single plan**. Set `Approved design: embedded` and the four approval fields. Keep `## Approved Design` last. After its `<!-- approved-design:start -->` line, copy the source after `<!-- design-body -->`, or the whole source when it has no marker, byte-for-byte. A material change returns the affected approval to pending.

For Markdown execution with delegated decisions, use `Execution authority: delegated` with `Execution source`, `Execution scope` and `Decision owner`. Record the settled design in `## Execution Design`. Approval and delegated headers are mutually exclusive in this file. Preserve existing approval evidence when continuing an approved family.

Before execution, populate ordered phases, acceptance, dependencies, ownership, exclusions, validation, resume context and skill bindings through their owners. `references/task-tracking.md` owns task authority and hierarchy. `references/companion-routing.md` owns exact skill bindings.

## Markdown profiles

Select a file profile only after admitting a Markdown family. Design uses the profile specified above. For execution and existing compatible families:

| Profile | Plan | Checkpoint | JSON state | Prompt pack | Use for |
|---|---:|---:|---:|---:|---|
| `direct` | required | no | no | opt-in | Genuinely single-phase, bounded work |
| `resumable` | required | required | no | opt-in | **Default.** Anything multi-phase |
| `orchestrated` | required | required | required | opt-in | An automated consumer parses the state |
| `legacy` | required | required | required | required | An old four-file consumer requires it |

Use `resumable` for multi-phase work: event-driven checkpoints preserve position without repeating discovery after interruption. Choose `direct` deliberately for genuinely single-phase bounded work; it accepts rediscovery after interruption. No profile promises a fixed checkpoint size or update count.

Apply admission before selecting a profile; no profile overrides its exceptions. An actionable execution-plan request uses `resumable` unless a real consumer requires a heavier profile.

For execution task authority and hierarchy, apply `references/task-tracking.md` `## Select before tracking-dependent work` regardless of profile.

## Markdown helpers

Set `SKILL_DIR` to the installed skill directory. From the target repository root, run `python3 "$SKILL_DIR/scripts/init_workflow_files.py" --task <title> --plan-kind design` for design. For execution use `--plan-kind execution` and one authority route:

- `--approved-design <path>` for linked approval.
- `--approved-design embedded --design-source <path> --approval-by <approver> --approval-on <YYYY-MM-DD> --approval-evidence <evidence>` for embedded approval.
- `--execution-source <request-reference> --execution-scope <authorized-scope> --decision-owner <owner>` for delegated design. Fill the generated design before execution.

Supply either `--task-store beads --beads-binding <portable-reference>` or `--task-store local --beads-unavailable-reason <observed failure>` through `references/task-tracking.md`. Use `--profile <profile>`, `--review-boundary phase|final` or `--with-prompts` when admitted. Exit `0` creates files (or prints paths on dry run), `1` means collision without writes, and `2` means the invocation could not run. Continue an existing family instead of forcing over it.

Before handoff and completion, run `python3 "$SKILL_DIR/scripts/validate_workflow_files.py" --plan <path>`. It checks kind, explicit companion references or selected stem, and legacy compatibility offline. Exit `0` means no blocking errors, `1` blocks advancement until repaired, and `2` means validation could not run. Warnings alone do not fail it. Live Beads checks still apply when the file family binds Beads.

## Size and consolidate the plan

This section and the dependency/concurrency plan below apply to execution.

Classify each phase and delegated lane before execution: missing facts to retrieve or clarify; mechanical work with settled decisions; bounded semantic judgment with a local causal path and decisive acceptance evidence; ordinary engineering judgment; or coupled judgment with interacting unresolved decisions. Record the reason, settled/open decisions and invariants. Assess risk separately: sensitivity determines gates, not reasoning complexity. The runtime orchestrator owns actual task model/effort allocation; `/alaa-prompting-guide` supplies capabilities and runtime mechanics. Planning effort never determines worker effort.

Merge phases or tasks sharing context, ownership and a validation barrier when separation buys no decision or authority boundary. Preserve every acceptance outcome, evidence mapping, dependency, exclusion and required observer. Keep phases separate when a decision, changed tested state, independent authority or integration barrier requires it; record why. `references/workspace-and-integration.md` owns shared-check coverage and evidence reuse.

After finalizing tasks, dependencies and consolidation, route allocation for EVERY role through the active runtime orchestrator.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Workflow records task scope/complexity, priority/reason, role authority identity, explicit model AND effort, source/evidence, invocation surface, requested/effective controls, availability and limits alongside conflict barriers and references to the selected store's readiness; it chooses no role-based pair. Material changes reassess only affected remaining tasks; never replay completed work.

## Dependency and concurrency plan

Use the selected task authority for dependency edges and ready sets through `references/task-tracking.md`. Each lane names disjoint write ownership, shared-resource conflicts (including fixtures, generators, ports and test environments), integration barriers and parallel/serialized rationale. Apply `references/workspace-and-integration.md` for shared-file ownership and stopped-writer recovery. Disjoint files alone do not prove independence. Keep coupled decisions together; serialize overlapping writes and conflicting resources. Record a dependency edge only where a lane or phase consumes another's output; an edge added for ordering convenience makes unrelated work wait. `alaa-codex-orchestrator` or `alaa-cc-orchestrator` Dispatch discipline owns when each lane starts.

Record each phase's post-reconciliation test collection, combined repair/retest and declared review barriers, with responsible owners, exact check coverage, failure/blocker evidence and resume position. Route generic execution and the early-repair exception to /alaa-testing-strategy `references/100-test-execution.md`; `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own phase/review scheduling and independent observers. Workflow records barriers without redefining them. Final-only review keeps phase test evidence separate from pending review.

Expose independently ready work to the runtime orchestrator; impose no workflow-wide writer limit. It owns observed capacity, dispatch mechanics and resource scheduling. Query/reconcile readiness at completion, scope-change or handoff boundaries; keep no persistent second ready-set cache or scheduler artifact.

## Markdown paths and correlation

- Plan: `docs/_agent_plans/<stem>.md`, or `docs/plan/<stem>.md` when that family already exists.
- Prompt pack: same plan directory, `<stem>__phase-prompts.md`.
- Checkpoint: `docs/agents/<stem>-state.md`.
- JSON state: `.codex/state/<stem>.json`.

Continue an active task's existing family and stem. Resolve companions only from explicit references or this selected stem; never attach an unrelated newest file.

## Permitted contents

`references/context-continuity.md` owns why the artifacts divide the way they do, what each handoff field means, and when a field earns a line. This file owns only where each artifact lives and what it is permitted to contain.

Kind-specific contents follow `## Plan kinds and approval`; task acceptance/results follow `references/task-tracking.md` `## Acceptance and evidence by level`. For handoff contents, checkpoint fields, status/cursor ownership and JSON projection, read `references/context-continuity.md`.

## Update events

`references/context-continuity.md` owns all update events, canonical status/cursor ownership and snapshot derivation. Update only the admitted artifact set; keep expensive learning in the handoff package rather than a position snapshot.

Do not maintain duplicate phase checklists, review history, lane definitions, documentation status, or touched-file histories in secondary state.

## Resume and handoff

`references/context-continuity.md` owns the read order, the cold-start test, the post-compaction rules, and what a handoff must contain. Do not restate them here.

## Delegation

`SKILL.md` `## Delegate selectively` owns which work may be delegated, what the parent stays responsible for, and where lane ownership is recorded. It forbids a lane-plan file because a second plan splits the workflow destination in two; task-store ownership remains separate.

## Compatibility

Execution compatibility aliases `--with-state`, `--state-only`, `--no-continuation`, `--lane`, `--parent-plan`, and `--mode` remain subject to the initializer's kind checks and emit deprecation warnings when they alter profile behavior. They never bypass kind admission. New initialization rejects `--state-only`: it cannot represent an execution plan and hierarchy. Continue historical standalone snapshots in place. Use `--profile legacy` when an old execution consumer requires four files.

Completed legacy artifacts remain historical evidence. Validate them with warnings; do not rewrite them unless they become actively executable.
