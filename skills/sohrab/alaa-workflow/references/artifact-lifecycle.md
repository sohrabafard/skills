# Artifact Admission and Lifecycle

Choose the smallest plan that preserves authority, acceptance and recovery.

## Admission

Before any implementation, record the outcome, scope, settled approach, prerequisites, exact skill bindings, acceptance and focused checks. That record is the compact plan.

| Work | Plan |
|---|---|
| Advice or ordinary review | No execution plan |
| Bounded single-phase work | The compact plan, in the bound task issue when Beads is available, or in the session when durable tracking is unnecessary |
| Authorized multi-phase, resumable, delegated or handoff-sensitive work, including a continuing fix loop | A complete durable execution plan, before dependent implementation or write-lane dispatch |

For a durable plan, continue an existing family's contract. For a new eligible execution with available bound Beads, use the native family in `references/task-tracking.md`. Use a Markdown family when Beads is unavailable at admission, or when an explicit file request or a file-consuming tool requires one; record that file consumer. Use one canonical plan.

A design-plan or execution-plan request authorizes saving that planning deliverable. Plan-only authorizes no implementation. An explicit no-file, read-only or chat-only limit prevails. Native Plan Mode uses only its host-permitted planning surface until execution is approved. A native plan file opens with a Persian decision summary (overall picture, goals, open questions), then a line that contains only `<!-- design-body -->`, then the complete English design. After approval, use that file as the approved design source. When a higher-priority limit prevents a required durable record, report the gap and pause dependent work.

Report the saved `beads:<root-id>`, or the plan and checkpoint paths. A session outline never satisfies durable admission.

## Plan kinds and approval

Every durable plan declares `Plan kind: design` or `Plan kind: execution`. An existing unmarked family keeps its recorded authority and kind.

A **design** plan discusses ideas, alternatives and algorithms before implementation. It always uses `Task store: local` and `Profile: resumable`. It has no Beads binding, issue registration, phase, task or subtask hierarchy, executable checklist, prompt pack or machine state. It keeps the outcome, scope, proposed design, acceptance criteria, `## Decisions` with `Date | Owner | Decision | Reason`, `## Open Questions`, and the handoff package and checkpoint that `references/context-continuity.md` defines. Date and attribute each decision and its reason. Design work ends when you present the design for explicit user approval; dispatch no implementation from it.

The design header records `Approval status: pending|approved`, `Approval by`, `Approval on` and `Approval evidence`. Approval needs an identifiable approver, a valid ISO date and evidence that the user approved this design and scope. Never infer approval from file creation, schema success or a request to discuss the design. A material change to an approved design returns the affected decisions to pending before dependent execution.

An **execution** plan admits implementation only with execution authority and a settled design. Record the authority by its actual route:

- **Approved design:** the actual approval, with its source and scope.
- **Delegated decisions:** the implementation request that delegates design decisions, its authorized scope and the decision owner. Resolve and record those decisions before dependent work. Delegation is no evidence of human design approval.

An unresolved human-only decision, a pending required approval or a change outside the approved scope blocks dependent work. Neither an issue nor offline validation authenticates authority.

A Markdown execution plan records the route in its header:

- **Separate approved design:** set `Approved design` to its readable portable path, and resolve its approval before execution.
- **Design approved in the current session:** use a single plan. Set `Approved design: embedded` and the four approval fields. Keep `## Approved Design` last. After its `<!-- approved-design:start -->` line, copy the source after `<!-- design-body -->`, or the whole source when it has no marker, byte-for-byte.
- **Delegated decisions:** set `Execution authority: delegated` with `Execution source`, `Execution scope` and `Decision owner`, and record the settled design in `## Execution Design`. One plan never carries both the approval headers and the delegated headers.

Preserve existing approval evidence when you continue an approved family.

Before execution, populate the ordered phases, acceptance, dependencies, ownership, exclusions, validation, resume context and skill bindings.

## Markdown profiles

Select a file profile only after you admit a Markdown family; no profile overrides an admission exception. Design uses `resumable`. For execution and existing compatible families:

| Profile | Plan | Checkpoint | JSON state | Prompt pack | Use for |
|---|---:|---:|---:|---:|---|
| `direct` | required | no | no | opt-in | Genuinely single-phase, bounded work |
| `resumable` | required | required | no | opt-in | **Default.** Anything multi-phase |
| `orchestrated` | required | required | required | opt-in | An automated consumer parses the state |
| `legacy` | required | required | required | required | An old four-file consumer requires it |

An actionable execution-plan request uses `resumable` unless a real consumer requires a heavier profile. Choose `direct` deliberately: it accepts rediscovery after an interruption. No profile promises a fixed checkpoint size or update count. Under every profile, task authority and hierarchy follow `references/task-tracking.md` `## Select before tracking-dependent work`.

## Markdown helpers

Set `SKILL_DIR` to the installed skill directory, and run both helpers from the target repository root.

**Initializer.** For design, run `python3 "$SKILL_DIR/scripts/init_workflow_files.py" --task <title> --plan-kind design`. For execution, use `--plan-kind execution` and one authority route:

- `--approved-design <path>` for linked approval.
- `--approved-design embedded --design-source <path> --approval-by <approver> --approval-on <YYYY-MM-DD> --approval-evidence <evidence>` for embedded approval.
- `--execution-source <request-reference> --execution-scope <authorized-scope> --decision-owner <owner>` for delegated design. Fill the generated design before execution.

Supply either `--task-store beads --beads-binding <portable-reference>` or `--task-store local --beads-unavailable-reason <observed failure>` through `references/task-tracking.md`. Use `--profile <profile>`, `--review-boundary phase|final` or `--with-prompts` when admitted. Exit `0` creates the files, or prints their paths on a dry run. Exit `1` means a collision and no write; continue the existing family instead of forcing over it. Exit `2` means that the invocation could not run.

**Validator.** Before handoff and completion, run `python3 "$SKILL_DIR/scripts/validate_workflow_files.py" --plan <path>`. It checks kind, explicit companion references or the selected stem, and legacy compatibility, all offline. Exit `0` means no blocking errors; warnings alone do not fail it. Exit `1` blocks advancement until repaired. Exit `2` means that validation could not run, which is never a pass. Live Beads checks still apply when the family binds Beads.

## Size and consolidate the plan

This section and the dependency and concurrency plan below apply to execution.

For each phase and each delegated lane, record the settled and open decisions and the invariants. Assess risk apart from reasoning complexity: sensitivity sets the gates. Planning effort never sets worker effort.

Merge phases or tasks that share context, ownership and a validation barrier when the split buys no decision boundary and no authority boundary. Keep every acceptance outcome, evidence mapping, dependency, exclusion and required observer. Keep phases separate, and record why, when a decision, a changed tested state, an independent authority or an integration barrier requires it.

After you finalize tasks, dependencies and consolidation, route allocation for EVERY role through the active runtime orchestrator.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Workflow chooses no pair. It stores the orchestrator's allocation record, with the explicit model AND effort for each task, beside the conflict barriers and the references to the store's readiness. A material change reassesses only the affected remaining tasks; never replay completed work.

## Dependency and concurrency plan

Take dependency edges and ready sets from the selected task authority through `references/task-tracking.md`. Each lane names its disjoint write ownership, its shared-resource conflicts (fixtures, generators, ports and test environments included), its integration barriers, and the reason it runs in parallel or serialized. Disjoint files alone prove no independence: apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`. Keep coupled decisions together. Serialize overlapping writes and conflicting resources. Record a dependency edge only where a lane or phase consumes another's output, because an edge added for ordering convenience makes unrelated work wait. `alaa-codex-orchestrator` or `alaa-cc-orchestrator` Dispatch discipline owns when each lane starts.

Record each phase's post-reconciliation test collection, combined repair/retest and declared review barriers, with their owners, exact check coverage, failure and blocker evidence, and resume position. Workflow records barriers without redefining them. /alaa-testing-strategy `references/100-test-execution.md` owns generic execution and the early-repair exception. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` schedule phases, reviews and independent observers. Final-only review keeps phase test evidence apart from pending review.

Expose independently ready work to the runtime orchestrator, and impose no workflow-wide writer limit. Query and reconcile readiness at completion, scope-change and handoff boundaries. Keep no persistent ready-set cache and no scheduler artifact.

## Markdown paths and correlation

- Plan: `docs/_agent_plans/<stem>.md`, or `docs/plan/<stem>.md` when that family already exists.
- Prompt pack: same plan directory, `<stem>__phase-prompts.md`.
- Checkpoint: `docs/agents/<stem>-state.md`.
- JSON state: `.codex/state/<stem>.json`.

Continue an active task's existing family and stem. Resolve companions only from explicit references or this selected stem; never attach an unrelated newest file.

## Artifact contents

Update only the admitted artifact set. `references/context-continuity.md` defines what each artifact holds and when to update it. Keep expensive learning in the handoff package, not in a position snapshot. Keep no duplicate phase checklists, review history, lane definitions, documentation status or touched-file histories in secondary state.

## Compatibility

The execution aliases `--with-state`, `--state-only`, `--no-continuation`, `--lane`, `--parent-plan` and `--mode` stay subject to the initializer's kind checks. They warn when they alter profile behavior, and they never bypass kind admission. New initialization rejects `--state-only`, because it cannot represent an execution plan and its hierarchy; continue a historical standalone snapshot in place. Use `--profile legacy` when an old execution consumer requires four files.

A completed legacy artifact is historical evidence. Validate it with warnings, and rewrite it only when it becomes actively executable.
