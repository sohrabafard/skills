# Task Tracking

This file owns task-store selection, the Beads-first policy, task authority, where each kind of task information lives, issue conventions, Beads capability adoption, readiness and migration. Artifact admission and profiles remain in `references/artifact-lifecycle.md`; resume and handoff remain in `references/context-continuity.md`.

## Select before tracking-dependent work

Resolve kind and admission through `references/artifact-lifecycle.md` first. Then test Beads availability. Beads is available only when all four hold: `bd` is installed (`command -v bd`), `bd where` succeeds, the workspace it reports matches the project binding, and `bd ping` succeeds. `bd where` only resolves the path. `bd ping` opens the store and runs a trivial query, so it detects a dead database. A CLI, installed skill, hook context or local `.beads` directory alone selects nothing. A reachable wrong hub is unavailable, not the configured store. A valid binding can point to an external hub without a repository-local database. The project binding alone decides whether a missing upstream Beads skill (`.agents/skills/beads/SKILL.md`) makes Beads unavailable; with no such rule, a missing skill changes nothing.

- **Available:** Beads is the task authority. Register every new execution plan, every new task in any family, including an existing `local` family, and every issue-only task in Beads. A new execution plan follows `## Phase-task-subtask hierarchy`.
- **Unavailable:** the plan records `Task store: local` with a `Task store reason` naming the observed failure, tracks its tasks in the plan, and continues. When Beads returns, retest availability before the next new task; new tasks then go to Beads under `## Migrating a local family`.

A design plan is always local. It takes no `Task store reason` and sits outside the availability test.

A task lives in exactly one store. Never initialize a replacement database or install hooks. Remote sync, including Dolt auto-push, needs the user's authorization under `## Ready tasks and workflow gates`.

The project binding owns workspace identity, project scope, and authority. Record its nonempty repository-relative instruction/configuration reference, optionally with a `#anchor`, rather than copying settings or machine paths. The reference must contain no absolute machine path, multiline value, backtick, or unresolved marker. Helpers check its format, not owner existence/configuration. Resolve conflicting or incomplete adoption/binding before registering tasks; verify active workspace and project through the binding owner before reading/changing issues.

For Beads mechanics, load the installed upstream Beads skill separately and reuse fresh hook/prime guidance; neither owns current task state. Without that skill, use `## Beads capabilities in use` and the installed `bd --help`. Do not copy a CLI manual or implement another client.

## Division of labor

The selected task store owns task registration, status, dependencies, ready and blocked state, discovered work, task continuation context, and the local evidence of new tasks. This skill owns whether a plan is needed and the process size, goal and phases, skill and lane choice, conflict prevention, evidence validity, phase acceptance, the four completion states, resume, handoff, and lesson selection. Only plans with `Task store: local` track tasks in Markdown; their recorded store owns that state.

## Agent identity and ownership

Before Beads mutations, give every live agent, including the parent, a distinct actor: `<runtime>:<run-id>:<agent-instance-id>`. Use exposed host IDs; allocate opaque unique IDs for missing components. Identity coordinates ownership and audit; it authenticates nobody and grants no authority. Pass the literal actor with `--actor` on every mutation; never rely on Git/user fallback or shared inherited `BEADS_ACTOR`.

Keep the actor recoverable in the existing dispatch or admitted handoff. A child dispatch carries its actor, binding reference, issue IDs and ownership action; read-only lanes use action `none` unless separately authorized to mutate issues. Parents never act as children. The same live agent retains its actor through compaction/resume; a replacement gets a new actor.

Before dependent implementation, read the issue and compare its actual assignee with your actor. Claim authorized unassigned work with `bd --actor <actor> update <id> --claim`, then read back that assignee and `in_progress`. Claim repetition is idempotent only for the same actor. Another actor's claim, failed claim or mismatched readback blocks dependent work; never force or take over automatically. `## Outage and uncertain writes` states the only exception.

A claim carries a lease that expires after a TTL; read the expiry from `bd show <id>` and hard-code no TTL. While you hold a claim longer than that, run `bd heartbeat <id>`. After a failed heartbeat, run `bd ping`. When it succeeds, the claim was lost: stop writing and re-read the issue. A failed ping follows `## Outage and uncertain writes`. Leases are node-local; across PCs ownership rides status and assignee. Release your own claim with `bd unclaim <id> --if-assignee <actor>`. `bd unclaim --force`, `bd update --force` and a bare `bd reclaim` take another actor's claim and are never used; `## Beads capabilities in use` owns the one allowed reclaim.

Updates to owned issues use `--if-assignee <actor>` and, when relying on a status, `--if-status <expected-status>`. For guard mismatch/exit 13 or uncertain writes, re-read and reconcile before retrying; `## Beads capabilities in use` owns guard mechanics.

Before replacement or cross-device transfer, apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`; authorized coordination and reconciled surviving files/evidence remain required. Serialize transfer against closure and other ownership changes. The authorized transferring agent uses its own `--actor` with old-assignee/status guards and `--assignee <new-actor>`, then reads back. A refused transfer blocks dependent work; never force it. The new actor acts only after verified transfer.

`bd close` has no assignee/status guard. Serialize ownership changes/transfers across pre-read, close and readback: verify your assignee and expected status, close with your actor after required acceptance/lint, then verify closure and assignee. This sequence is not atomic. Uncertain coordination blocks closure; report it rather than claiming race safety.

Verified on 2026-11-02 against installed `bd` 1.3.1 (c1c4b642a) help for `update`, `close`, `unclaim` and `heartbeat`; the 2026-10-18 source check named the same commit ([update.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/update.go), [close.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/close.go)). Recheck after upgrade. These rules override actorless upstream examples; project binding still owns scope and authority.

## One task authority

| Store | Task owner | Plan work entries |
|---|---|---|
| `local` (Beads unavailable at plan creation, or an existing local family) | Plan tasks own progress and prerequisite edges for tasks not yet in Beads | Stable ID, outcome, dependency list and skill mapping |
| `beads` | Beads owns issue identity, status, priority, assignee, issue edges and native readiness | Unique issue ID mapped to one phase, with its skill mapping |

For local families, write each task as `- [ ] T1: <outcome> [depends: none] [skills: inherit]`. Keep IDs unique and stable across the plan. Use comma-separated local IDs for prerequisites; `none` means no prerequisites. Every prerequisite must exist, the graph must be acyclic, and completed tasks' prerequisites must be completed. Tick only after observing the task's outcome and evidence, including work verified as already done. The plan's recorded claim coordinates ownership; it proves no exclusivity across agents or PCs.

For flat Beads mappings, in an existing flat Beads family or a local family that gained Beads tasks, write `- Issue: <issue-id> [skills: inherit]`, using the actual opaque ID without assuming a prefix. New Beads execution families use `## Phase-task-subtask hierarchy`. Map each issue to one phase; a task override is its complete `[skills: name, name]` mapping. A Beads family keeps no local checkbox list or editable issue register; a local family keeps checkboxes only for tasks not yet migrated. Record issue closure in Beads, never by ticking a plan mirror. `references/companion-routing.md` owns inherited/override skill semantics for both stores.

Workflow plan contents follow `references/context-continuity.md`; task acceptance and evidence follow `## Acceptance and evidence by level`.

## Phase-task-subtask hierarchy

Every new execution family created while Beads is available declares `- Task hierarchy: phase-task-subtask` in the plan header, with `Task store: beads` and its portable `Task binding`; omitting the marker cannot exempt it. A family created while Beads is unavailable has no hierarchy marker: it records `Task store: local`, `Task binding: not applicable` and `Task store reason: <observed failure>`, and uses local checkbox tasks. Existing unmarked families keep their original contract. Tasks added later to a local family are flat `Issue:` entries; the family gains no phase hierarchy.

Register every phase, task and subtask, with acceptance and parent-child relations, in bound Beads before dependent execution. A phase or milestone contains one or more tasks and maps as `Phase N`. IDs are opaque and unique across the family. Preserve an optional enclosing engagement epic.

A coherent task is an executable leaf with zero subtasks. Use subtasks only for a checklist too broad for one agent to hold in mind: two or more separable parts, each claimable, verifiable and closable on its own evidence, with acceptance different from its siblings. Never create one subtask restating its parent. The validator accepts zero subtasks and rejects exactly one. Verify distinct scope and acceptance in the bound issues before execution.

The plan maps containment, never mutable issue status:

```markdown
### Phase 1 - Implement
- Phase issue: opaque-phase-id
- Required skills: exact-owner
- Work:
  - Task issue: opaque-task-id [skills: inherit]
    - Subtask issue: opaque-subtask-a-id [skills: inherit]
    - Subtask issue: opaque-subtask-b-id [skills: inherit]
  - Task issue: opaque-leaf-task-id [skills: inherit]
```

Use exactly zero, two and four spaces before the respective list markers. A task belongs to that phase and a subtask to its immediately preceding task. Inherit phase skills at a task and task skills at a subtask, or supply the complete override. Do not mix flat `Issue:` entries or local checkboxes into a marked hierarchy. Missing, duplicate, orphan or unresolved executing nodes block dependent work. Offline structure proves no live node, parent-child relation, binding or readiness: verify those through the bound owner and read them back.

Containment does not establish ordering. Record genuine prerequisites as separate blocking edges through `## Record task prerequisites`; preserve independently ready leaves. Register the hierarchy and reconcile barriers before dispatch, not after writes.

The plan header records `Review boundary: phase` or `final`, `Final phase: Phase N`, and `Commit authority`. New plans default to `local commits pre-authorized (main instruction file)`; verify the main instruction rule before acting. Use `explicit user grant: <source and scope>` for a separate grant or `not granted` when no grant applies. Offline syntax proves no authority; local-commit authority covers no push, merge into another branch, tag or history rewrite. Each phase records `Review status` and `Review evidence` separately from any commit checkpoint. Pending review is `REVIEW_PENDING`; completed review uses the verdict from `references/review-mode.md` with attributable evidence. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own when review, independent verification and commits run; the plan passes this whole-engagement contract into nested invocations rather than resetting it.

New nested plans retain the canonical engagement's `Review boundary` and `Final phase`, reached through `Parent plan`, and record their own last phase as `Local final phase`. Their cursor remains local. Nested final-only phases keep `REVIEW_PENDING`; the canonical engagement owns final acceptance. Resolve ancestry before writing; malformed, conflicting, cyclic, missing or over-limit ancestry blocks initialization. A parent without representable cadence requires explicit reconciliation; never infer legacy defaults or migrate its authority. Existing families remain readable under their recorded contract.

Completed required review boundaries need resolved `Validation commands` and observed `Evidence observed`; absent or unrun evidence cannot establish acceptance. When validation is inapplicable, record `Validation commands: none (specific reason)` and `Evidence observed: not applicable (specific reason)`. A bare sentinel supplies no justification.

## Where task information lives

For local families, the plan owns the first three rows for tasks not yet in Beads.

| Information | Owner |
|---|---|
| Status, priority, assignee, dependency, follow-up work | Beads issue and its relations |
| Position, next step, blockers | Issue `notes` |
| Historical events | Issue comments |
| Goal, shared constraints, phase acceptance | Plan |
| Durable knowledge, shared hub reminders, binding rules | `/alaa-memory-os` `## Beads hub reminders and issue notes` |

That section owns the policy for the last row and its boundary with issue notes; do not restate it here.

## Acceptance and evidence by level

Every criterion and result has one owner, chosen by level:

- Phase acceptance and review status: the plan; its phase issue references that owner.
- A task or subtask's acceptance and result: that node's issue; under `local`, the plan's task entry.
- An integrated review across several tasks: the plan's phase-evidence section.
- Bulky output: an artifact, meaning a file under the task-artifact directory the repository's instructions name, subject to `references/artifact-lifecycle.md` admission. The evidence owner links to it and records the command, the result and the one line that mattered, per `references/context-continuity.md` `## What not to write`. When those instructions name no such directory, record that no artifact was admitted and keep only the command, the result and the one line that mattered in the evidence owner; never paste the bulky output.

The plan links to task results and never copies them. Evidence is recorded once; every other site links to its owner, because a copy goes stale silently. Work without a plan keeps all of it in its issue. Plan-held task acceptance stays in the plan until its task migrates; the issue then points to it with an exact plan reference.

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

Verified on 2026-11-02 against installed `bd` 1.3.1 (c1c4b642a): the `--help` of every command named below (integration and setup commands: the `bd --help` list), plus read-only `bd where`, `ping`, `ready`, `list`, `show`, `config`, `formula list`, `gate list`, `human list`, `orphans`, `dep cycles`, `graph check` and `lint`. Recheck after a Beads upgrade. Use a capability only as its row states. No row grants remote or destructive authority.

| Capability | Decision | Rule and reason |
|---|---|---|
| `bd create` with `--parent`, `--spec-id`, `--acceptance`, `--design`, `--labels`, `--deps`, `--validate`, `--dry-run` | Adopt | Register each phase, task and subtask with its parent, acceptance and plan link (`## Issue fields`). Preview with `--dry-run`; `--validate` checks the type's required sections. |
| `bd search` | Adopt | Search before creating; it includes closed issues by default. |
| Types `decision`, `spike` | Adopt | `decision` records a decision other tasks cite; `spike` a time-boxed investigation whose output is knowledge. |
| `bd create --graph`, `--file`, `bd batch`, `bd q` | Not adopted | Help prints no graph-file schema. `bd batch` creates with no parent, acceptance or guards. `bd q` sets parent, labels, priority and type, but no acceptance, spec-id or guards. |
| `bd dep add`, `bd link` | Adopt | Record each prerequisite as a blocking edge (`## Record task prerequisites`). Create each follow-up `discovered-from` its origin (`--deps discovered-from:<origin-id>`); that edge records provenance and does not block. Per Beads v1.3.1 source (`internal/types/types.go` `AffectsReadyWork`, checked 2026-10-13), readiness counts only blocks, parent-child, conditional-blocks and waits-for edges. |
| `bd dep cycles`, `bd graph check`, `bd swarm validate` | Adopt, read-only | Run after registering or changing edges and before dispatch. `bd swarm create` is not adopted. |
| `bd where`, `bd ping`, `bd prime` | Adopt, read-only | `bd where` and `bd ping` are the availability test (`## Select before tracking-dependent work`). `bd prime` prints workflow context; run it only when hook context is missing or stale. |
| `bd ready`, `bd blocked`, `bd children`, `bd show --children --refs --long`, `bd graph --open`, `bd epic status`, `bd list`, `bd query`, `bd count`, `bd status` | Adopt, read-only | Filter by the project label. Run `bd ready --explain` when readiness is unexpected. `bd show --long` shows the lease. |
| `bd ready --claim`, `bd close --claim-next`, `bd close --continue`, `bd epic close-eligible`, `bd orphans --fix` | Not adopted | Each claims or closes an issue the plan did not designate or acceptance evidence did not approve. Read-only `bd orphans` is adopted at handoff review. |
| `bd update --claim`, `--if-assignee`, `--if-status` | Adopt | Per `## Agent identity and ownership`. A mismatch exits 13 and writes nothing (installed help). Guards check only the local database, prove no cross-PC exclusivity, require a field update in the same command and never combine with `--claim`. On exit 13, re-read actual state and follow `## Outage and uncertain writes`; never retry blindly. |
| `bd heartbeat`, `bd unclaim --if-assignee` | Adopt | Keep and release your own claim per `## Agent identity and ownership`. |
| `bd reclaim` | Adopt once | Only as `bd reclaim --id <id>` inside stopped-writer recovery, after `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery` verified the holder stopped and `bd show` displays the expired lease. Never bare, never `--any-replica`, never against a live or foreign-replica lease. The replacement claims with its own actor. |
| `bd unclaim --force`, `bd update --force` | Not adopted | They take another actor's claim. |
| `bd close --force`, `bd gate resolve` | Not adopted | Except for a gate with recorded user approval (gate row). `--force` closes pinned issues and unsatisfied gates; `bd gate resolve` equals `bd close`. |
| `bd defer`, `bd undefer`, `bd update --defer` | Adopt | Postpone work nothing blocks; record `--reason`. Deferred issues leave `bd ready`. |
| `bd supersede <id> --with <new>` | Adopt | Replace an obsolete issue or spec; it closes the old one with a reference. |
| `bd gate create --type human --blocks <id> --reason <why>`, `bd human list` | Adopt | Gate a decision only the user may make. Close a gate issue by any command (`bd gate resolve`, `bd close`, `bd close --force`) only after the user's explicit approval is recorded; never close your own gate. |
| Gate types `timer`, `gh:run`, `gh:pr`, `bead` | Not adopted | `gh:*` waits on an external system; `timer` duplicates `bd defer --until`; `bd gate create` cannot create `bead`, and a blocking edge covers it. |
| `bd formula list`, `bd formula show`, `bd mol pour` | Adopt when a formula exists | Run `bd mol pour --dry-run` first, then pour persistent work. `bd formula list` showed no formula on 2026-11-02; authoring one is a separate authorized change. Wisps, `bond`, `squash` and `burn` are not adopted: ephemeral work leaves no evidence. |
| `bd close --suggest-next` | Adopt | Read the newly unblocked issues; claim none automatically. |
| `bd lint`, `bd stale` | Adopt | `bd lint` reports missing sections per issue type. Run it before closing or handing off an issue; a finding blocks that close or handoff until the section is filled or the gap is recorded in the issue. Run `bd stale` at a handoff or resume review. |
| `bd comments add`, `--append-notes` | Adopt | Events and position per `## Issue fields`. |
| `--readonly`, `--sandbox` (global flags) | Adopt | A read-only lane (ownership action `none`) passes `--readonly`. Every write-capable agent passes `--sandbox` on each `bd` command that can write, unless the user authorized Dolt sync. Read-only commands need none. Installed help says it disables Dolt auto-push. |
| `bd remember`, `bd recall`, `bd memories` | Not adopted here | `/alaa-memory-os` `## Beads hub reminders and issue notes` owns them. |
| `bd ship`, `external:` dependencies | Not adopted | Resolution needs the `external_projects` config, unset on 2026-11-02; `## Cross-project delivery` states the rule. |
| `bd preflight`, `bd merge-slot`, `bd set-state`, `bd audit`, `bd provenance`, `bd events`, `bd todo`, `bd edit`, `bd create-form` | Not adopted | They serve Beads contributors, merge queues, operational state, interactive editing or a second evidence log. |
| `bd dolt push`, `bd dolt pull`, `bd dolt remote add`, `bd dolt remote remove`, `bd dolt set`, `bd sync`, `bd vc merge`, `bd bootstrap`, `bd init`, `bd hooks`, `bd federation`, `bd backup`, `bd export`, `bd import`, `bd migrate-personal`, `bd delete`, `bd gc`, `bd compact`, `bd flatten`, `bd prune`, `bd purge`, `bd sql`, `bd rename`, `bd rename-prefix`, and every integration command (`bd github`, `bd gitlab`, `bd jira`, `bd linear`, `bd notion`, `bd ado`, `bd repo`, `bd serve`) | Not adopted | Remote, setup or destructive effect. Each needs the user's explicit authorization for that action. |
| Any `bd` command not listed in this table | Not adopted | Any command that reaches a remote or an external system needs the user's explicit authorization for that action. |

## Cross-project delivery

When one project needs another project's output, create a delivery task in the producer project, carrying the producer project's label, whose outcome is "the output is available to the consumer". The consumer's task depends on the delivery task through a blocking edge, per `## Record task prerequisites`. When the producer and consumer cannot be verified through the same binding or hub, stop the edge registration under the binding rule in `## Select before tracking-dependent work` and report it.

## Ready tasks and workflow gates

Use the selected store's prerequisite graph for task readiness. A ready task still requires scope, authority, available deliverables/source, mapped skills, and file/environment independence before dispatch. Phase dependencies and acceptance barriers stay in the plan; native issue readiness does not satisfy them. Closing all issues proves none of the workflow lifecycle states defined in `references/workspace-and-integration.md`.

A claim does not lock files, fixtures, generators, ports or test environments, and independently synced PC databases do not establish mutual exclusion. Designate task ownership and resolve shared-resource conflicts before parallel work. Before cross-PC transfer, verify that the designated owner can access the actual source and attributable evidence. Git source sync and Dolt task sync are separate actions with separate authorization; run a Dolt remote or sync command (`bd dolt push`, `bd dolt pull`, `bd dolt remote`, `bd sync`) only with the user's explicit authorization for that action. `## Beads capabilities in use` owns the `--sandbox` rule against auto-push. A synced issue does not make another PC's uncommitted code available. `references/context-continuity.md` owns the handoff record for a device transfer.

## Outage and uncertain writes

Beads unreachable before a plan exists selects `local` under `## Select before tracking-dependent work`. Issue-only work needs tracking when it spans more than one session, delegates work or ends in a handoff. Admit such work through `references/artifact-lifecycle.md` as an execution plan with the `direct` profile and `Task store: local`. Other issue-only work proceeds untracked and reports its result. When Beads is available again, register an issue for untracked issue-only work only if the work is still open.

A `beads` family that loses Beads mid-run keeps its store. Preserve existing evidence, record the outage in the checkpoint, create no local copy of a Beads-owned task, never convert issues to checkboxes, and never claim a failed update as saved. Pause claims, dispatch and closure that need Beads state; continue independent authorized work on tasks already claimed and read back, and reconcile through Beads when it returns.

When `bd ping` fails, a failed heartbeat is an outage, not a lost claim. Continue only independent authorized work on a task already claimed and read back. Record the outage in the checkpoint. When Beads is available, re-read the issue. If another actor holds it or the lease expired, stop and follow the claim-lost rule.

With no claimed task, a `beads` family waits for the hub. The user may instead name one task as unclaimed and choose to proceed on it. Record that statement in the checkpoint and create no local copy of the task. When Beads is available, read the issue back. If another actor holds it, stop and report the collision. If it is unassigned, claim it with `--claim` before more work.

Park newly discovered work, evidence and notes in the optional checkpoint field `Pending Beads reconciliation` (the plan cursor under the `direct` profile), a dated list. Write them as plain list entries, never as tasks or checkboxes. When Beads is available, register each entry there, then clear the list. A list that is not cleared blocks closure. A handoff during an open outage copies the list verbatim and names the outage as the blocker.

After a mutation with an uncertain outcome, read actual task state through the bound owner before retrying. Reconcile whether the requested effect landed, then perform only the still-required authorized change. Do not retry blindly or report success without evidence. Resume and evidence reconciliation follow `references/context-continuity.md` and `references/workspace-and-integration.md`.

## Helper boundary and compatibility

For a new execution family the initializer requires `--task-store beads` with `--beads-binding <portable-reference>`, or `--task-store local` with a one-line `--beads-unavailable-reason <observed failure>`. The reason becomes the `Task store reason` header: the validator requires it with local execution and rejects it with Beads. Kind admission belongs to `references/artifact-lifecycle.md`; profiles and aliases never replace task authority. `--review-boundary {phase,final}` defaults to phase at the root, inherits canonical parent cadence when nested, and rejects a conflicting explicit override. Resolve availability first; the helper never discovers a store from PATH, environment or directory existence. Local binding is `not applicable` until the family gains Beads tasks. Beads binding is required; Beads with deprecated standalone `--state-only` is invalid. Helpers invoke no Beads command, service or network operation.

For execution and existing compatible families, either `Task store` or `Task binding` metadata header marks a family. Marked families require exactly one of each, a supported store and valid pairing under every profile, including legacy; both absent retains the old contract. Draft unresolved markers may warn; unresolved executing work fails even when the header says planning. Offline validation checks metadata, mappings, skills and snapshots; it proves no live issue, workspace, project scope or readiness.

Install compatible instructions, templates and helpers together before executing a newly marked family; older consumers cannot safely execute it. On rollback, freeze marked families until compatible consumers return and preserve task truth rather than converting issues to checkboxes.

## Migrating a local family

Apply this when `## Select before tracking-dependent work` finds Beads available and a family records `Task store: local`. Migration grants no installation, live mutation, sync or publication authority.

1. Replace `Task binding: not applicable` with the adopted portable binding before the first Beads task. Keep `Task store: local` and its reason as history.
2. Register every new task in Beads and map it as `- Issue: <issue-id> [skills: inherit]` in its phase. A Beads task never depends on an open local task; migrate that task first.
3. An open local task may be registered in Beads, read back, then marked migrated: `- [-] T2: <outcome> [depends: T1] [migrated: <issue-id>] [skills: inherit]`, with its `- Issue:` mapping in the same plan. Migrate a task's local dependents with it; the validator rejects a local task that depends on a migrated one. Every prerequisite of a migrated task must already be completed or migrated; the validator rejects any other (`plan.local-dependency`).
4. Completed local tasks stay as history. A migrated task lives only in Beads; never keep both mutable. Never migrate from Beads back to local.
