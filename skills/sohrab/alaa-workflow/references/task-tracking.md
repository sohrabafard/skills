# Task Tracking

This file owns task-store selection, the Beads-first policy, task authority, where each kind of task information lives, issue conventions, Beads capability adoption, readiness and migration. Artifact admission and profiles remain in `references/artifact-lifecycle.md`; resume and handoff remain in `references/context-continuity.md`.

## Select before tracking-dependent work

Resolve the plan kind and admission through `references/artifact-lifecycle.md` first. Then test Beads availability. Beads is available only when all four of these conditions hold:

1. `bd` is installed (`command -v bd`).
2. `bd where` succeeds.
3. The workspace that `bd where` reports matches the project binding.
4. `bd ping` succeeds.

`bd where` only resolves the path. `bd ping` opens the store and runs a trivial query, so it detects a dead database. A CLI, an installed skill, hook context or a local `.beads` directory selects nothing on its own. A reachable hub that is not the bound workspace is unavailable; it is not the configured store. A valid binding can point to an external hub that has no repository-local database. Only the project binding decides whether a missing upstream Beads skill (`.agents/skills/beads/SKILL.md`) makes Beads unavailable. When the binding states no such rule, a missing skill changes nothing.

- **Available:** Beads is the task authority for all new tasks, including issue-only work and tasks added to a local family. For a new eligible plan, follow `## Beads-native execution plan`. For an admitted Markdown plan, follow `## Phase-task-subtask hierarchy`.
- **Unavailable:** An admitted durable plan records `Task store: local` and a `Task store reason` that names the observed failure. Bounded work without a durable trigger keeps its compact plan in the session. Retest availability before the next new task. When Beads is available, migrate through `## Migrating a local family`.

A design plan is always local. It takes no `Task store reason` and sits outside the availability test.

A task lives in exactly one store. Never initialize a replacement database or install hooks. Remote sync, including Dolt auto-push, needs the user's authorization under `## Ready tasks and workflow gates`.

The project binding owns workspace identity, project scope and authority. Record a reference to the binding instead of copying its settings or machine paths. The reference is a nonempty repository-relative path to the instruction or configuration file that holds the binding, optionally with a `#anchor`. It must contain no absolute machine path, no multiline value, no backtick and no unresolved marker. The helpers check only the format of the reference; they do not check that the owner exists or is configured. When the Beads adoption or the binding is conflicting or incomplete, resolve it before you register tasks. Before you read or change issues, verify the active workspace and project through the binding owner.

For Beads mechanics, load the installed upstream Beads skill separately, and reuse fresh hook or `bd prime` guidance. Neither of them owns the current task state. Without that skill, use `## Beads capabilities in use` and the installed `bd --help`. Do not copy a CLI manual, and do not implement another Beads client.

## Division of labor

The selected store owns task registration, status, dependencies, readiness, discoveries, continuation and task evidence. Workflow owns planning, acceptance, continuity and completion rules. Only `Task store: local` tracks mutable task state in Markdown.

## Agent identity and ownership

Before any Beads mutation, give every live agent a distinct actor, including the parent. The actor has the form `<runtime>:<run-id>:<agent-instance-id>`. Use the IDs that the host exposes. When the host exposes no ID for a component, allocate an opaque unique ID for it. Identity coordinates ownership and audit. It authenticates nobody and grants no authority. Pass the literal actor with `--actor` on every mutation. Never rely on the default fallback to the Git `user.name` or `$USER` (installed `bd --help`), and never rely on a shared inherited `BEADS_ACTOR`.

Keep the actor recoverable in the existing dispatch or the admitted handoff. A child dispatch carries the child's actor, the binding reference, the issue IDs and the ownership action. A read-only lane uses the ownership action `none` unless it is separately authorized to mutate issues. A parent never acts as a child. The same live agent keeps its actor through compaction and resume. A replacement agent gets a new actor.

Before dependent implementation, read the issue and compare its actual assignee with your actor. Claim authorized unassigned work with `bd --sandbox update <id> --claim --actor <actor>`. Then read the issue back and confirm that the assignee is your actor and the status is `in_progress`. A repeated claim is idempotent only for the same actor. Each of these blocks dependent work: a claim that another actor holds, a failed claim, or a readback that does not match. Never force a claim, and never take over an issue automatically. During an outage, `## Outage and uncertain writes` allows work on one unclaimed task that the user names.

A claim carries a lease that expires after a TTL. Read the expiry from `bd show <id>`, and hard-code no TTL. While you hold a claim for longer than the TTL, run `bd heartbeat <id>`. After a failed heartbeat, run `bd ping`. Treat the claim as lost until a re-read shows otherwise: stop writing and re-read the issue. When the ping fails, follow `## Outage and uncertain writes`. A lease is local to one node. Across PCs, the issue status and assignee carry ownership. Release your own claim with `bd unclaim <id> --if-assignee <actor>`. `bd unclaim --force`, `bd update --force` and a bare `bd reclaim` take another actor's claim, so never use them. `## Beads capabilities in use` owns the one allowed reclaim.

Every update to an issue you own passes `--if-assignee <actor>`. When the update relies on a status, it also passes `--if-status <expected-status>`. After a guard mismatch (exit 13) or a write whose outcome is uncertain, re-read the issue and reconcile before you retry. `## Beads capabilities in use` owns the guard mechanics.

Before you replace an agent or transfer an issue to another device, apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`. Replacement and transfer still require authorized coordination and reconciled surviving files and evidence. Serialize the transfer against closure and against other ownership changes. The authorized transferring agent runs the update with its own `--actor`, with guards on the old assignee and the expected status, and with `--assignee <new-actor>`. Then it reads the issue back. A refused transfer blocks dependent work; never force it. The new actor acts only after the transfer is verified.

`bd close` has no assignee guard and no status guard. Serialize ownership changes and transfers across the whole close sequence:

1. Read the issue, and verify your assignee and the expected status.
2. After the required acceptance and `bd lint` pass, close the issue with your actor.
3. Read the issue back, and verify the closure and the assignee.

This sequence is not atomic. Uncertain coordination blocks closure. Report it; do not claim race safety.

Verified on 2026-11-02 against installed `bd` 1.3.1 (c1c4b642a) help for `update`, `close`, `unclaim` and `heartbeat`; the 2026-10-18 source check named the same commit ([update.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/update.go), [close.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/close.go)). Recheck after upgrade. These rules override actorless upstream examples; project binding still owns scope and authority.

## One task authority

| Store | Task owner | Plan work entries |
|---|---|---|
| `local` (Beads unavailable at plan creation, or an existing local family) | Plan tasks own progress and prerequisite edges for tasks not yet in Beads | Stable ID, outcome, dependency list and skill mapping |
| `beads` | Beads owns issue identity, status, priority, assignee, issue edges and native readiness | Native issue hierarchy, or unique phase mappings for Markdown consumers |

For local families, write each task as `- [ ] T1: <outcome> [depends: none] [skills: inherit]`. Keep IDs unique and stable across the plan. Use comma-separated local IDs for prerequisites; `none` means no prerequisites. Every prerequisite must exist, the graph must be acyclic, and the prerequisites of a completed task must be completed. Tick a task only after you observe its outcome and evidence, including work verified as already done. The plan's recorded claim coordinates ownership; it proves no exclusivity across agents or PCs.

For an existing flat Beads mapping, or for a local family that gains Beads tasks, write `- Issue: <issue-id> [skills: inherit]` in one phase. A task override is its complete `[skills: name, name]` mapping. Record closure in Beads. A local family keeps checkboxes only for tasks not yet migrated. `references/companion-routing.md` owns skill inheritance.

Workflow plan contents follow `references/context-continuity.md`; task acceptance and evidence follow `## Acceptance and evidence by level`.

## Beads-native execution plan

Use the root epic as the canonical plan, addressed as `beads:<root-id>` in dispatch, evidence and handoff. Use the actual opaque IDs. Register the ordered phase milestones under the root. Then register executable tasks, and any subtasks, under their actual parent. Each phase has at least one task. A task is a leaf, or it has at least two independent subtasks that are separately claimable and verifiable and have distinct acceptance. Containment never substitutes for prerequisite edges.

| Issue and field | Canonical content |
|---|---|
| Root `description` | `Plan kind: execution`, `Plan format: beads-native-v1`, portable `Task binding`, outcome, scope and exclusions, constraints, `Registration: draft\|registered`, `Review boundary: phase\|final`, exact `Final phase` issue ID, `Commit authority`, shared skill bindings, and the owner and allocation record or exact references to the nodes that hold it |
| Root `design`, `acceptance` | In `design`: the settled design and the execution authority under `references/artifact-lifecycle.md`, including the delegation source, scope and decision owner, or the actual approval and its evidence. In `acceptance`: the engagement acceptance |
| Root `notes`, handoff | In `notes`: the aggregate cursor, the last verified evidence address, blockers and the next action. The six-field handoff goes in the root description under `references/context-continuity.md` |
| Phase milestone | In `description`: the phase number, outcome, barrier rationale, required skills, and the test collection and repair/retest plan. In `acceptance`: the phase criteria. In attributable comments: the integrated results, the review verdict and its evidence |
| Task or subtask | In `description`: the plan address and exact phase ID, the outcome, the owned scope and its exclusions, the skill binding or inheritance, ownership and resource conflicts, and focused checks. In `design`: settled causal reasoning, invariants, relevant failures, recovery and decisions. In `acceptance`: observable criteria. Results go in comments and the close reason |

Use the review and commit semantics under `## Phase-task-subtask hierarchy`. A nested invocation uses the same root address and final phase ID, with its own assigned node and cursor. The parent holds root registration and aggregate position. Use native status, assignees, parent relations and prerequisites as task truth. Keep no mirrored graph, task table, Markdown checkpoint or second editable plan.

Register the root as `draft`, and verify its owner claim before you create children. After an interruption, reuse the exact matches that already exist. Read back every node's parent, label, criteria, skill bindings and edges with `bd show <id>` and `bd children <id>`. Check graph integrity through the capability table below. Query `bd ready --label <project-label> --parent <root-id> --limit 0` for the leaves that are eligible for new claims. A descendant never blocks on an ancestor. Add edges for real prerequisites, and confirm that the affected leaves stay blocked until those prerequisites land. Confirm that independently executable leaves stay ready when their own prerequisites are satisfied.

Before you mark the root `registered`, read back the root and phase records. Verify the settled design, the recorded execution authority and its scope, the engagement acceptance, the exact final phase, the review and final gate plan, and the resolved skill mappings. Check that they are consistent with the registered graph and the assigned work. After all checks pass, mark `registered` through a guarded root update and read it back. Missing or inconsistent records block dependent work, and so do uncertain writes. Repeat these checks on resume and after a material change. For a material change to the plan or the graph, pause the affected dispatch and return the registration to `draft`. Reconcile and read back before you restore `registered`. The registration marker proves no authority, no test result and no resource independence; apply `## Ready tasks and workflow gates` before each dispatch. Before handoff and before completion, reconcile the affected issues and the root, including pending review, commit and curation evidence.

## Phase-task-subtask hierarchy

This section owns the Markdown mappings, and the review and commit semantics that native plans share. A new Markdown execution family that uses Beads declares `- Task hierarchy: phase-task-subtask`, `Task store: beads` and its portable `Task binding`. A new local family records `Task store: local`, `Task binding: not applicable` and `Task store reason: <observed failure>`. It uses local checkbox tasks and omits the hierarchy marker. Existing unmarked families keep their original contract. Tasks added later to a local family are flat `Issue:` entries.

Register every phase, task and subtask, with acceptance and parent-child relations, in bound Beads before dependent execution. A phase or milestone contains one or more tasks and maps as `Phase N`. IDs are opaque and unique across the family. Preserve an optional enclosing engagement epic.

A coherent task is an executable leaf with zero subtasks. Use subtasks only for a checklist too broad for one agent to hold in mind: two or more separable parts, each claimable, verifiable and closable on its own evidence, with acceptance different from its siblings. Never create one subtask that restates its parent. The validator accepts zero subtasks and rejects exactly one. Verify distinct scope and acceptance in the bound issues before execution.

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

Use exactly zero, two and four spaces before the respective list markers. A task belongs to that phase, and a subtask belongs to its immediately preceding task. A task inherits the phase skills and a subtask inherits the task skills, unless you supply the complete override. Do not mix flat `Issue:` entries or local checkboxes into a marked hierarchy. Missing, duplicate, orphan or unresolved executing nodes block dependent work. Offline structure proves no live node, no parent-child relation, no binding and no readiness: verify those through the bound owner and read them back.

Containment does not establish ordering. Record genuine prerequisites as separate blocking edges through `## Record task prerequisites`, and preserve independently ready leaves. Register the hierarchy and reconcile barriers before dispatch, not after writes.

The plan header records `Review boundary: phase` or `final`, `Final phase: Phase N`, and `Commit authority`. New plans default to `local commits pre-authorized (main instruction file)`; verify the main instruction rule before acting. Use `explicit user grant: <source and scope>` for a separate grant, or `not granted` when no grant applies. Offline syntax proves no authority. Local-commit authority covers no push, no merge into another branch, no tag and no history rewrite. Each phase records `Review status` and `Review evidence` separately from any commit checkpoint. A pending review is `REVIEW_PENDING`. A completed review uses the verdict from `references/review-mode.md` with attributable evidence. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own when review, independent verification and commits run. The plan passes this whole-engagement contract into nested invocations; it does not reset it.

New nested Markdown plans retain the canonical engagement's `Review boundary` and `Final phase`, reached through `Parent plan`, and record their own last phase as `Local final phase`. Their cursor remains local. Nested final-only phases keep `REVIEW_PENDING`; the canonical engagement owns final acceptance. Resolve ancestry before writing. Malformed, conflicting, cyclic, missing or over-limit ancestry blocks initialization. A parent without a representable cadence requires explicit reconciliation. Never infer legacy defaults, and never migrate the parent's authority.

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

- Phase acceptance and review status: the native phase issue, or the Markdown plan with a reference from its phase issue.
- A task or subtask's acceptance and result: that node's issue; under `local`, the plan's task entry.
- Integrated review across tasks: the native phase's evidence comment or the Markdown phase-evidence section.
- Bulky output: an artifact, meaning a file under the task-artifact directory the repository's instructions name, subject to `references/artifact-lifecycle.md` admission. The evidence owner links to it and records the command, the result and the one line that mattered, per `references/context-continuity.md` `## What not to write`. When those instructions name no such directory, record that no artifact was admitted and keep only the command, the result and the one line that mattered in the evidence owner; never paste the bulky output.

The plan links to task results and never copies them. Evidence is recorded once; every other site links to its owner, because a copy goes stale silently. Work without a plan keeps all of it in its issue. Plan-held task acceptance stays in the plan until its task migrates; the issue then points to it with an exact plan reference.

## Issue fields

Under `beads`:

| Field | Holds |
|---|---|
| `description` | Goal, scope, output, and a link to the plan and phase |
| `spec_id` | A real file spec, as repository name and repository-relative path, e.g. `skills:docs/_agent_plans/<stem>.md` |
| `acceptance` | The task's criterion, or an exact reference into the plan |
| `design` | A decision affecting the task, plus its reference link |
| `notes` | Position, including blockers, and next step |
| comments | Events, including interim validation runs, and learned knowledge and curation outcomes when no plan exists (`references/context-continuity.md`) |
| close reason | A closed task's result (see `## Close reason`) |

For Markdown plans, set `spec_id` to the file reference. For native plans, use the plan address in the description and leave `spec_id` unset unless a real file spec applies. Use custom metadata only for a minimal marker or a named consumer; do not copy native fields into it.

## Close reason

Under `beads`, close with three parts: a short verdict, the tested version, and the evidence address. The tested version is the commit containing every tested change or, when uncommitted, the HEAD SHA plus the scoped content SHA-256 digest from `references/workspace-and-integration.md` `## Record the tested state`. Numbers are optional; label each one "at close".

A tested subtask or task may close after its own acceptance and required tests pass while boundary review remains pending. Say `tested; review pending` and cite its tested snapshot; closure implies no independent review. Under `Review boundary: final`, an intermediate phase issue may close its implementation and test milestone once those criteria pass, while the plan records `REVIEW_PENDING`. This advances dependency readiness without claiming reviewed acceptance or authorizing a commit. A final boundary remains incomplete until its required review, fixes and retests pass.

## Record task prerequisites

At task decomposition and material changes to scope or prerequisites, identify genuine blockers and reconcile the selected task store before starting or dispatching affected work. Keep independent tasks independent.

For Beads, inspect existing issues and edges and verify IDs and project scope through the binding before changing dependencies. Use the upstream skill and installed CLI help to apply only authorized missing or obsolete edge changes. Record each prerequisite as a blocking edge: the dependent issue is blocked by the prerequisite. Descriptions, plan references, hierarchy and related links do not establish that edge. Read back affected dependencies and query native readiness to confirm the intended direction and blocking state before proceeding; text alone cannot keep blocked work out of the ready set. If registration or verification fails, follow the outage and uncertain-write rules below.

## Beads capabilities in use

Verified on 2026-11-02 against installed `bd` 1.3.1 (c1c4b642a): the `--help` of every command named below (for integration and setup commands, the `bd --help` list), plus read-only `bd where`, `ping`, `ready`, `list`, `show`, `config`, `formula list`, `gate list`, `human list`, `orphans`, `dep cycles`, `graph check` and `lint`. Recheck after a Beads upgrade. Use a capability only as its row states. No row grants remote or destructive authority.

| Capability | Decision | Rule and reason |
|---|---|---|
| `bd create` with `--parent`, `--spec-id`, `--acceptance`, `--design`, `--labels`, `--deps`, `--validate`, `--dry-run` | Adopt | Register each phase, task and subtask with its parent, acceptance and plan link (`## Issue fields`). Preview the registration with `--dry-run`. `--validate` checks the required sections of the issue type. |
| `bd create --skills`, `--context`, `--body-file`, `--design-file`; `bd update --body-file`, `--design-file` | Adopt | In [Beads v1.3.2](https://github.com/steveyegge/beads/blob/v1.3.2/cmd/bd/create.go#L114-L148), the `--skills` and `--context` flags of `bd create` append sections to the description. Use those flags or write the same sections in the body, and write each section once. For long content, use the `--body-file` and `--design-file` flags, with `-` for stdin where the command supports it. On `bd update`, these flags replace the corresponding field; pass the ownership guards with them. Recheck the installed help and behavior after an upgrade. |
| `bd search` | Adopt | Search before creating; it includes closed issues by default. |
| Types `decision`, `spike` | Adopt | `decision` records a decision other tasks cite. `spike` records a time-boxed investigation whose output is knowledge. |
| `bd create --graph`, `--file`, `bd batch`, `bd q` | Not adopted | The help prints no schema for the graph file. `bd batch` creates issues with no parent, no acceptance and no guards. `bd q` sets parent, labels, priority and type, but it sets no acceptance and no spec-id, and it takes no guards. |
| `bd dep add`, `bd link` | Adopt | Record each prerequisite as a blocking edge (`## Record task prerequisites`). Create each follow-up with a `discovered-from` edge to its origin (`--deps discovered-from:<origin-id>`). That edge records provenance and does not block. Per Beads v1.3.1 source (`internal/types/types.go` `AffectsReadyWork`, checked 2026-10-13), readiness counts only blocks, parent-child, conditional-blocks and waits-for edges. |
| `bd dep cycles`, `bd graph check`, `bd swarm validate` | Adopt, read-only | Run these checks after you register or change edges, and before the affected dispatch. Reuse graph evidence while the graph is unchanged. `bd swarm create` is not adopted. |
| `bd where`, `bd ping`, `bd prime` | Adopt, read-only | `bd where` and `bd ping` are the availability test (`## Select before tracking-dependent work`). `bd prime` prints workflow context; run it only when hook context is missing or stale. |
| `bd ready`, `bd blocked`, `bd children`, `bd show --children --refs --long`, `bd graph --open`, `bd epic status`, `bd list`, `bd query`, `bd count`, `bd status` | Adopt, read-only | Filter by the project label. Run `bd ready --explain` when readiness is unexpected. `bd show --long` shows the lease. |
| `bd ready --claim`, `bd close --claim-next`, `bd close --continue`, `bd epic close-eligible`, `bd orphans --fix` | Not adopted | Each of them claims or closes an issue that the plan did not designate or that acceptance evidence did not approve. Read-only `bd orphans` is adopted at handoff review. |
| `bd update --claim`, `--if-assignee`, `--if-status` | Adopt | Use them as `## Agent identity and ownership` states. A guard mismatch exits 13 and writes nothing (installed help). The guards check only the local database, and they prove no exclusivity across PCs. A guard requires a field update in the same command. Never combine a guard with `--claim`. On exit 13, re-read the actual state and follow `## Outage and uncertain writes`; never retry blindly. |
| `bd heartbeat`, `bd unclaim --if-assignee` | Adopt | Keep and release your own claim as `## Agent identity and ownership` states. |
| `bd reclaim` | Adopt once | Use it only as `bd reclaim --id <id>`, and only inside stopped-writer recovery. Run it only after `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery` verified that the holder stopped, and after `bd show` displays the expired lease. Never run it bare, never pass `--any-replica`, and never run it against a live lease or a foreign-replica lease. The replacement then claims the issue with its own actor. |
| `bd unclaim --force`, `bd update --force` | Not adopted | They take another actor's claim. |
| `bd close --force`, `bd gate resolve` | Not adopted | The one exception is closing a gate issue after the user's approval is recorded, as the `bd gate create` row states. `--force` closes pinned issues and unsatisfied gates. `bd gate resolve` is equivalent to `bd close`. |
| `bd defer`, `bd undefer`, `bd update --defer` | Adopt | Postpone work that nothing blocks, and record a `--reason`. A deferred issue leaves `bd ready`. |
| `bd supersede <id> --with <new>` | Adopt | Replace an obsolete issue or spec. The command closes the old issue with a reference. |
| `bd gate create --type human --blocks <id> --reason <why>`, `bd human list` | Adopt | Gate a decision that only the user may make. Close a gate issue by any command (`bd gate resolve`, `bd close`, `bd close --force`) only after the user's explicit approval is recorded; never close your own gate. |
| Gate types `timer`, `gh:run`, `gh:pr`, `bead` | Not adopted | `gh:*` waits on an external system. `timer` duplicates `bd defer --until`. `bd gate create` cannot create `bead`, and a blocking edge covers that case. |
| `bd formula list`, `bd formula show`, `bd mol pour` | Adopt when a formula exists | Run `bd mol pour --dry-run` first, then pour persistent work. `bd formula list` showed no formula on 2026-11-02; authoring one is a separate authorized change. Wisps, `bond`, `squash` and `burn` are not adopted, because ephemeral work leaves no evidence. |
| `bd close --suggest-next` | Adopt | Read the issues that the close unblocked. Claim none of them automatically. |
| `bd lint`, `bd stale` | Adopt | `bd lint` reports missing sections per issue type. Run it before closing or handing off an issue; a finding blocks that close or handoff until the section is filled or the gap is recorded in the issue. Run `bd stale` at a handoff or resume review. |
| `bd comments add`, `--append-notes` | Adopt | Record events with `bd comments add` and position with `--append-notes`, as `## Issue fields` states. |
| `--readonly`, `--sandbox` (global flags) | Adopt | A read-only lane (ownership action `none`) passes `--readonly`. Every write-capable agent passes `--sandbox` on each `bd` command that can write, unless the user authorized Dolt sync. Read-only commands need none. The installed help says that `--sandbox` disables Dolt auto-push. |
| `bd remember`, `bd recall`, `bd memories` | Not adopted here | `/alaa-memory-os` `## Beads hub reminders and issue notes` owns them. |
| `bd ship`, `external:` dependencies | Not adopted | Resolving them needs the `external_projects` config, which was unset on 2026-11-02. `## Cross-project delivery` states the rule. |
| `bd preflight`, `bd merge-slot`, `bd set-state`, `bd audit`, `bd provenance`, `bd events`, `bd todo`, `bd edit`, `bd create-form` | Not adopted | They serve Beads contributors, merge queues, operational state, interactive editing or a second evidence log. |
| `bd dolt push`, `bd dolt pull`, `bd dolt remote add`, `bd dolt remote remove`, `bd dolt set`, `bd sync`, `bd vc merge`, `bd bootstrap`, `bd init`, `bd hooks`, `bd federation`, `bd backup`, `bd export`, `bd import`, `bd migrate-personal`, `bd delete`, `bd gc`, `bd compact`, `bd flatten`, `bd prune`, `bd purge`, `bd sql`, `bd rename`, `bd rename-prefix`, and every integration command (`bd github`, `bd gitlab`, `bd jira`, `bd linear`, `bd notion`, `bd ado`, `bd repo`, `bd serve`) | Not adopted | Each has a remote, setup or destructive effect. Each needs the user's explicit authorization for that action. |
| Any `bd` command not listed in this table | Not adopted | Any command that reaches a remote or an external system needs the user's explicit authorization for that action. |

## Cross-project delivery

When one project needs another project's output, create a delivery task in the producer project, carrying the producer project's label, whose outcome is "the output is available to the consumer". The consumer's task depends on the delivery task through a blocking edge, per `## Record task prerequisites`. When the producer and consumer cannot be verified through the same binding or hub, stop the edge registration under the binding rule in `## Select before tracking-dependent work` and report it.

## Ready tasks and workflow gates

Use the selected store's prerequisite graph for task readiness. A ready task still requires registered scope, authority, available deliverables and source, mapped skills, independence of files and environments, and satisfied phase barriers. Closing all issues proves none of the workflow lifecycle states in `references/workspace-and-integration.md`.

A claim does not lock files, fixtures, generators, ports or test environments, and independently synced PC databases do not establish mutual exclusion. Designate task ownership and resolve shared-resource conflicts before parallel work. Before a cross-PC transfer, verify that the designated owner can access the actual source and the attributable evidence. Git source sync and Dolt task sync are separate actions with separate authorization. Run a Dolt remote or sync command (`bd dolt push`, `bd dolt pull`, `bd dolt remote`, `bd sync`) only with the user's explicit authorization for that action. `## Beads capabilities in use` owns the `--sandbox` rule against auto-push. A synced issue does not make another PC's uncommitted code available. `references/context-continuity.md` owns the handoff record for a device transfer.

## Outage and uncertain writes

When Beads is unreachable before plan admission, durable work selects `local`. Apply the Markdown profile rules in `references/artifact-lifecycle.md`. Bounded work without a durable trigger keeps its plan in the session and reports its result. When Beads returns, register previously untracked work only if it is still open.

A Beads-bound family that loses Beads mid-run keeps its store. Preserve evidence. Pause claims, dispatch and closure that need Beads state. Continue only independently authorized work on tasks already claimed and read back, subject to the named-task exception below. Reconcile through Beads when it returns.

When `bd ping` fails after a failed heartbeat, handle the failed heartbeat as an outage under this section. When Beads is available, re-read the issue. If another actor holds it or the lease expired, stop, report and wait for the user's instruction. Never re-claim or take over automatically.

When you hold no claimed task, wait for the hub, unless the user names one unclaimed task and chooses to proceed on it. Record the statement as unverified. On recovery, read the task back. If another actor holds it, stop and report the collision. If it is unassigned, claim it before more work.

Record the outage and a dated `Pending Beads reconciliation` list of evidence, notes and discoveries in the admitted Markdown checkpoint or direct cursor. For a native plan or issue-only work, use the session, or an already authorized evidence-only artifact when one is available. Label unsaved items pending. Keep no offline task mirror. On recovery, register or record each pending entry at its Beads owner and read it back before you clear the list. Pending reconciliation blocks closure and completion. At an outage handoff, transmit the list verbatim and name the blocker.

After a mutation with an uncertain outcome, read the actual task state through the bound owner before you retry. Determine whether the requested effect landed, then perform only the still-required authorized change. Do not retry blindly, and do not report success without evidence. Resume and evidence reconciliation follow `references/context-continuity.md` and `references/workspace-and-integration.md`.

## Helper boundary and compatibility

Markdown helpers receive the selected store and binding arguments from `references/artifact-lifecycle.md`; they never discover or contact Beads. The validator requires the reason for local execution and rejects it for Beads. Review defaults to phase at the root, inherits the canonical parent cadence when nested, and rejects a conflicting override. Profiles and aliases never replace task authority.

For execution and existing compatible families, either a `Task store` or a `Task binding` metadata header marks a family. A marked family requires exactly one of each header, a supported store and a valid pairing under every profile, including legacy. When both headers are absent, the family keeps the old contract. Draft unresolved markers may warn; unresolved executing work fails even when the header says planning. Offline validation checks metadata, mappings, skills and snapshots. It proves no live issue, workspace, project scope or readiness.

Install compatible instructions, templates and helpers together before executing a newly marked family; older consumers cannot safely execute it. On rollback, freeze marked families until compatible consumers return. Preserve task truth; do not convert issues to checkboxes.

## Migrating a local family

Apply this when `## Select before tracking-dependent work` finds Beads available and a family records `Task store: local`. Migration grants no installation, live mutation, sync or publication authority.

1. Replace `Task binding: not applicable` with the adopted portable binding before the first Beads task. Keep `Task store: local` and its reason as history.
2. Register every new task in Beads and map it as `- Issue: <issue-id> [skills: inherit]` in its phase. A Beads task never depends on an open local task; migrate that task first.
3. An open local task may be registered in Beads, read back, then marked migrated: `- [-] T2: <outcome> [depends: T1] [migrated: <issue-id>] [skills: inherit]`, with its `- Issue:` mapping in the same plan. Migrate a task's local dependents with it; the validator rejects a local task that depends on a migrated one. Every prerequisite of a migrated task must already be completed or migrated; the validator rejects any other (`plan.local-dependency`).
4. Completed local tasks stay as history. A migrated task lives only in Beads; never keep both mutable. Never migrate from Beads back to local.
