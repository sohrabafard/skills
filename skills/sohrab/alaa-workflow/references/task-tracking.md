# Task Tracking

This file owns task-store selection, task authority, where each kind of task information lives, issue conventions, readiness and migration. Artifact admission and profiles remain in `references/artifact-lifecycle.md`; resume and handoff remain in `references/context-continuity.md`.

## Select before tracking-dependent work

Resolve kind and admission through `references/artifact-lifecycle.md` before tracking-dependent work. Continue an existing family's recorded task store until explicit migration. Every new execution plan, including direct single-phase work, requires explicitly adopted, verified Beads and the hierarchy below; a missing binding blocks dependent execution and dispatch. A CLI, installed skill, hook context or local `.beads` directory alone selects nothing. A valid binding can point to an external hub without a repository-local database.

The project binding owns workspace identity, project scope, and authority. Record its nonempty repository-relative instruction/configuration reference, optionally with a `#anchor`, rather than copying settings or machine paths. The reference must contain no absolute machine path, multiline value, backtick, or unresolved marker. Helpers check its format, not owner existence/configuration. Resolve conflicting or incomplete adoption/binding before tracking-dependent work. Verify active workspace and project through the binding owner before reading/changing issues; a reachable wrong hub is not the configured store.

For Beads mechanics, load the installed upstream Beads skill separately and reuse fresh hook/prime guidance. Neither hooks nor guidance own current task state. If the required binding or upstream owner is unavailable, report the gap and stop its dependent work. Do not copy a CLI manual, implement another client, install hooks, initialize a replacement database or silently fall back to local.

## Division of labor

The selected task store owns task registration, status, dependencies, ready and blocked state, discovered work, task continuation context, and the local evidence of new tasks. This skill owns whether a plan is needed and the process size, goal and phases, skill and lane choice, conflict prevention, evidence validity, phase acceptance, the four completion states, resume, handoff, and lesson selection. Only existing `local` execution plans track tasks in Markdown; their recorded store owns that state.

## Agent identity and ownership

Before Beads mutations, give every live agent, including the parent, a distinct actor: `<runtime>:<run-id>:<agent-instance-id>`. Use exposed host IDs; allocate opaque unique IDs for missing components. Identity coordinates ownership and audit; it authenticates nobody and grants no authority. Pass the literal actor with `--actor` on every mutation; never rely on Git/user fallback or shared inherited `BEADS_ACTOR`.

Keep the actor recoverable in the existing dispatch or admitted handoff. A child dispatch carries its actor, binding reference, issue IDs and ownership action; read-only lanes use action `none` unless separately authorized to mutate issues. Parents never act as children. The same live agent retains its actor through compaction/resume; a replacement gets a new actor.

Before dependent implementation, read the issue and compare its actual assignee with your actor. Claim authorized unassigned work with `bd --actor <actor> update <id> --claim`, then read back that assignee and `in_progress`. Claim repetition is idempotent only for the same actor. Another actor's claim, failed claim or mismatched readback blocks dependent work; never force or take over automatically.

Updates to owned issues use `--if-assignee <actor>` and, when relying on a status, `--if-status <expected-status>`. For guard mismatch/exit 13 or uncertain writes, re-read and reconcile before retrying; `## Beads capabilities in use` owns guard mechanics.

Before replacement or cross-device transfer, apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`; authorized coordination and reconciled surviving files/evidence remain required. Serialize transfer against closure and other ownership changes. The authorized transferring agent uses its own `--actor` with old-assignee/status guards and `--assignee <new-actor>`, then reads back. A refused transfer blocks dependent work; never force it. The new actor acts only after verified transfer.

`bd close` has no assignee/status guard. Serialize ownership changes/transfers across pre-read, close and readback: verify your assignee and expected status, close with your actor after required acceptance/lint, then verify closure and assignee. This sequence is not atomic. Uncertain coordination blocks closure; report it rather than claiming race safety.

Verified on 2026-10-18 against installed `bd` 1.3.1 help and matching upstream [update.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/update.go) and [close.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/close.go). Recheck after upgrade. These rules override actorless upstream examples; project binding still owns scope and authority.

## One task authority

| Store | Task owner | Plan work entries |
|---|---|---|
| `local` in an existing execution family | Plan tasks own progress and prerequisite edges | Stable ID, outcome, dependency list and skill mapping |
| `beads` | Beads owns issue identity, status, priority, assignee, issue edges and native readiness | Unique issue ID mapped to one phase, with its skill mapping |

For existing marked local execution families, write each task as `- [ ] T1: <outcome> [depends: none] [skills: inherit]`. Keep IDs unique and stable across the plan. Use comma-separated local IDs for prerequisites; `none` means no prerequisites. Every prerequisite must exist, the graph must be acyclic, and completed tasks' prerequisites must be completed. Tick only after observing the task's outcome and evidence, including work verified as already done. The local plan's recorded claim/ownership coordinates; it does not prove exclusivity across agents or PCs.

For existing flat Beads families, write `- Issue: <issue-id> [skills: inherit]`, using the actual opaque ID without assuming a prefix. New execution families use `## Phase-task-subtask hierarchy`. Map each issue uniquely to one phase; a task override is its complete `[skills: name, name]` mapping. Keep no authoritative local checkbox/numbered task list or editable issue register alongside these mappings. Issue closure is recorded in Beads, never by ticking a plan mirror. `references/companion-routing.md` owns inherited/override skill semantics for both stores.

Workflow plan contents follow `references/context-continuity.md`; task acceptance and evidence follow `## Acceptance and evidence by level`.

## Phase-task-subtask hierarchy

Every new execution family declares `- Task hierarchy: phase-task-subtask` in the plan header, with `Task store: beads` and its portable `Task binding`. Existing unmarked or local families keep their original contract until explicit migration; omitting the marker cannot exempt a new execution plan.

Register every phase, task and subtask, its acceptance and parent-child relation in bound Beads before dependent execution. A phase or milestone contains one or more tasks; each task contains one or more executable subtasks. Map milestones as `Phase N` in the plan. IDs are opaque and unique across the family. Preserve an optional enclosing engagement epic. The plan maps containment, never mutable issue status:

```markdown
### Phase 1 - Implement
- Phase issue: opaque-phase-id
- Required skills: exact-owner
- Work:
  - Task issue: opaque-task-id [skills: inherit]
    - Subtask issue: opaque-subtask-id [skills: inherit]
```

Use exactly zero, two and four spaces before the respective list markers. A task belongs to that phase and a subtask to its immediately preceding task. Inherit phase skills at a task and task skills at a subtask, or supply the complete override. Do not mix flat `Issue:` entries or local checkboxes into a marked hierarchy. Missing, duplicate, orphan or unresolved executing nodes block dependent work. Offline structure proves no live node, parent-child relation, binding or readiness: verify those through the bound owner and read them back.

Containment does not establish ordering. Record genuine prerequisites as separate blocking edges through `## Record task prerequisites`; preserve independently ready leaves. Register the hierarchy and reconcile barriers before dispatch, not after writes.

The plan header records `Review boundary: phase` or `final`, `Final phase: Phase N`, and `Commit authority: explicit user grant: <source and scope>` or `Commit authority: not granted`. Offline syntax never proves that the user actually granted authority. Each phase records `Review status` and `Review evidence`. Pending review is `REVIEW_PENDING`; completed review uses the verdict from `references/review-mode.md` with attributable evidence. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own when review, independent verification and commits run; the plan passes this whole-engagement contract into nested invocations rather than resetting it.

New nested plans retain the canonical engagement's `Review boundary` and `Final phase`, reached through `Parent plan`, and record their own last phase as `Local final phase`. Their cursor remains local. Nested final-only phases keep `REVIEW_PENDING`; the canonical engagement owns final acceptance. Resolve ancestry before writing; malformed, conflicting, cyclic, missing or over-limit ancestry blocks initialization. A parent without representable cadence requires explicit reconciliation; never infer legacy defaults or migrate its authority. Existing families remain readable under their recorded contract.

Completed required review boundaries need resolved `Validation commands` and observed `Evidence observed`; absent or unrun evidence cannot establish acceptance. When validation is inapplicable, record `Validation commands: none (specific reason)` and `Evidence observed: not applicable (specific reason)`. A bare sentinel supplies no justification.

## Where task information lives

For existing local execution families, the plan owns the first three rows.

| Information | Owner |
|---|---|
| Status, priority, assignee, dependency, follow-up work | Beads issue and its relations |
| Position, next step, blockers | Issue `notes` |
| Historical events | Issue comments |
| Goal, shared constraints, phase acceptance | Plan |
| Durable knowledge, shared hub reminders, binding rules | `/alaa-memory-os` `## Beads hub reminders and issue notes` |

That section owns the policy for the last row and its boundary with issue notes; do not restate it here.

## Acceptance and evidence by level

Every criterion and every result has one owner, chosen by level:

- Phase acceptance and review status: the plan; its phase issue references that owner.
- A task or subtask's acceptance and result: that node's issue. Under existing `local`, the plan's task entry.
- An integrated review across several tasks: the plan's phase-evidence section.
- Bulky output: an artifact, meaning a file under the task-artifact directory the repository's instructions name, subject to `references/artifact-lifecycle.md` admission. The evidence owner links to it and records the command, the result and the one line that mattered, per `references/context-continuity.md` `## What not to write`. When those instructions name no such directory, record that no artifact was admitted and keep only the command, the result and the one line that mattered in the evidence owner; never paste the bulky output.

The plan links to task results and never copies them. Evidence is recorded once; every other site links to its owner, because a copy goes stale silently. Work without a plan keeps all of it in its issue. Existing work is not migrated automatically: plan-held task acceptance stays where it is, and its issue points to it with an exact plan reference until an explicit migration.

## Issue fields

Under `beads`:

| Field | Holds |
|---|---|
| `description` | Goal, scope, output, and a link to the plan and phase |
| `spec_id` | The repository name, a colon, then the plan's repository-relative path, e.g. `skills:docs/_agent_plans/<stem>.md` |
| `acceptance` | The task's criterion, or an exact reference into the plan |
| `design` | A decision affecting the task, plus its reference link |
| `notes` | Position, including blockers, and next step |
| comments | Events, including interim validation runs, and learned knowledge and curation outcomes when no plan exists (`references/context-continuity.md`) |
| close reason | A closed task's result (see `## Close reason`) |

When a plan exists, put its path in `spec_id` in that form; a path inside `description` prose alone does not count. The repository prefix keeps the path unambiguous on a hub shared by several projects.

## Close reason

Under `beads`, close with three parts: a short verdict, the tested version, and the evidence address. The tested version is the commit containing every tested change or, when uncommitted, the HEAD SHA plus the scoped content SHA-256 digest from `references/workspace-and-integration.md` `## Record the tested state`. Numbers are optional; label each one "at close".

A tested subtask or task may close after its own acceptance and required tests pass while boundary review remains pending. Say `tested; review pending` and cite its tested snapshot; closure implies no independent review. Under `Review boundary: final`, an intermediate phase issue may close its implementation/test milestone once those criteria pass, while the plan records `REVIEW_PENDING`. This advances dependency readiness without claiming reviewed acceptance or authorizing a commit. A final boundary remains incomplete until its required review, fixes and retests pass.

## Record task prerequisites

At task decomposition and material changes to scope or prerequisites, identify genuine blockers and reconcile the selected task store before starting or dispatching affected work. Keep independent tasks independent.

For Beads, inspect existing issues and edges and verify IDs and project scope through the binding before changing dependencies. Use the upstream skill and installed CLI help to apply only authorized missing or obsolete edge changes. Record each prerequisite as a blocking edge: the dependent issue is blocked by the prerequisite. Descriptions, plan references, hierarchy and related links do not establish that edge. Read back affected dependencies and query native readiness to confirm the intended direction and blocking state before proceeding; text alone cannot keep blocked work out of the ready set. If registration or verification fails, follow the outage and uncertain-write rules below.

## Beads capabilities in use

The `bd` behavior stated below was verified on 2026-10-13 against installed `bd` help (1.3.1) and Beads v1.3.1 source (`internal/types/types.go` `AffectsReadyWork`); recheck after a Beads upgrade.

- `--spec-id` carries the plan link (see `## Issue fields`).
- Use issue type `decision` to record a decision that other tasks cite, and `spike` for a time-boxed investigation whose output is knowledge.
- Create each follow-up `discovered-from` its origin (`--deps discovered-from:<origin-id>` on `bd create`). The edge records provenance only and does not block, because readiness counts only blocks, parent-child, conditional-blocks and waits-for edges. Record a real prerequisite as a separate blocking edge.
- `--if-assignee` and `--if-status` check only the local database state and prove no cross-PC exclusivity. A mismatch exits 13 (installed help: nothing is written). They require a field update in the same command and are never combined with `--claim`. On exit 13, re-read actual state and follow `## Outage and uncertain writes`; never retry blindly.
- `bd lint` reports missing recommended sections per issue type (installed `bd lint --help`). Run it before closing or handing off an issue; a finding blocks that close or handoff until the missing section is filled or the gap is recorded in the issue. Run `bd stale` at a handoff or resume review, and `bd ready --explain` when readiness is unexpected.
- Formulas, molecules and automatic gates are not adopted by this workflow. The verified `bd gate --help` already lists `human`, `timer`, `gh:run`, `gh:pr` and `bead`; capability availability does not change this policy. Reconsider adoption through a separately authorized workflow-policy change.

## Cross-project delivery

When one project needs another project's output, create a delivery task in the producer project, carrying the producer project's label, whose outcome is "the output is available to the consumer". The consumer's task depends on the delivery task through a blocking edge, per `## Record task prerequisites`. When the producer and consumer cannot be verified through the same binding or hub, stop the edge registration under the binding rule in `## Select before tracking-dependent work` and report it.

## Ready tasks and workflow gates

Use the selected store's prerequisite graph for task readiness. A ready task still requires scope, authority, available deliverables/source, mapped skills, and file/environment independence before dispatch. Phase dependencies and acceptance barriers stay in the plan; native issue readiness does not satisfy them. Closing all issues proves none of the workflow lifecycle states defined in `references/workspace-and-integration.md`.

A claim does not lock files, fixtures, generators, ports or test environments, and independently synced PC databases do not establish mutual exclusion. Designate task ownership and resolve shared-resource conflicts before parallel work. Before cross-PC transfer, verify that the designated owner can access the actual source and attributable evidence. Git source sync and Dolt task sync are separate actions with separate authorization; run `bd dolt push` and `bd dolt pull` only with the user's explicit authorization for that action. A synced issue does not make another PC's uncommitted code available. `references/context-continuity.md` owns the handoff record for a device transfer.

## Outage and uncertain writes

When configured Beads is unavailable or its workspace/project mismatches, preserve existing evidence and continue only independent authorized analysis. Stop tracking-dependent implementation, dispatch and closure. Report the actual blocker and next safe action; do not create local replacement tasks or claim a failed update was saved.

After a mutation with an uncertain outcome, read actual task state through the bound owner before retrying. Reconcile whether the requested effect landed, then perform only the still-required authorized change. Do not retry blindly or report success without evidence. Resume and evidence reconciliation follow `references/context-continuity.md` and `references/workspace-and-integration.md`.

## Helper boundary and compatibility

For a new execution family, the initializer requires `--task-store beads` and `--beads-binding <portable-reference>`. Kind admission belongs to `references/artifact-lifecycle.md`; profiles and aliases never replace task authority. `--review-boundary {phase,final}` defaults to phase at the root, inherits canonical parent cadence when nested, and rejects a conflicting explicit override. Resolve and verify adoption before invoking it; it never discovers a store from PATH, environment or directory existence. Local binding is `not applicable`. Beads binding is required; Beads with deprecated standalone `--state-only` is invalid. Helpers invoke no Beads command, service or network operation.

For execution and existing compatible families, either `Task store` or `Task binding` metadata header marks a family. Marked families require exactly one of each, a supported store and valid pairing under every profile, including legacy. Both absent retains the old compatibility contract. Draft unresolved markers may warn; unresolved executing work fails even when the overall header still says planning. Offline validation checks metadata, graph/mappings, skills and snapshots; it proves no live issue existence, bound workspace, project scope or readiness.

Install compatible instructions, templates, and helpers together before executing a newly marked family. Older consumers may skip mappings or gates and cannot safely execute it. On rollback, freeze marked families until compatible consumers return; preserve task truth/evidence rather than converting issues to checkboxes or selecting local. Existing unmarked families remain under their original compatible contract.

Migration is explicit: identify the old authority, verify the destination binding and issue/task mapping, preserve canonical acceptance/evidence and designate the cutover owner before changing authority. Keep the old task store read-only after cutover so rollback has its evidence; never maintain two mutable task owners. Migration and this skill grant no installation, live mutation, sync or publication authority.
