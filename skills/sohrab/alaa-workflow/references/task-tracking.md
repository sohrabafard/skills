# Task Tracking

## Select before tracking-dependent work

First resolve the plan kind and admission through `references/artifact-lifecycle.md`. Then test Beads availability. Beads is available only when all four conditions hold:

1. `bd` is installed (`command -v bd`).
2. `bd where` succeeds.
3. The workspace that `bd where` reports matches the project binding.
4. `bd ping` succeeds. It opens the store, so it detects a dead database that `bd where` does not.

A CLI, an installed skill, hook context or a local `.beads` directory selects nothing. A reachable hub that is not the bound workspace is unavailable. A binding may point to an external hub with no repository-local database. A missing upstream Beads skill (`.agents/skills/beads/SKILL.md`) makes Beads unavailable only when the project binding says so.

- **Available:** Beads is the task authority for every new task, including issue-only work and tasks added to a local family. A new eligible plan follows `## Beads-native execution plan`. An admitted Markdown plan follows `## Phase-task-subtask hierarchy`.
- **Unavailable:** An admitted durable plan records `Task store: local` and a `Task store reason` that names the observed failure. Bounded work without a durable trigger keeps its compact plan in the session. Retest availability before the next new task. When Beads is available, migrate through `## Migrating a local family`.

A design plan is always local, takes no `Task store reason` and skips the availability test.

A task lives in exactly one store. Never initialize a replacement database or install hooks.

The project binding owns workspace identity, project scope and authority. Record a reference to it, never a copy of its settings: a nonempty repository-relative path to the file that holds the binding, optionally with a `#anchor`, with no absolute machine path, multiline value, backtick or unresolved marker. The helpers check only this format. Resolve a conflicting or incomplete binding before you register tasks. When an authorized task writes or refreshes a repository's binding block, start from `assets/beads-binding-template.md`.

For Beads mechanics, load the installed upstream Beads skill. Without it, use `## Beads capabilities in use` and the installed `bd --help`. Hook guidance and `bd prime` never state the current task state, and their unfiltered output never widens the project scope.

## Agent identity and ownership

Before any Beads mutation, give every live agent, the parent included, a distinct actor of the form `<runtime>:<run-id>:<agent-instance-id>`, built from the IDs that the host exposes or from an opaque unique ID. Use the session identifier that the host exposes as the run ID, so that the same session derives the same actor after a compaction. An actor coordinates ownership and audit; it authenticates nobody and grants no authority. Pass the literal actor with `--actor` on every mutation. Never rely on the fallback to the Git `user.name` or `$USER` (installed `bd create --help`, bd 1.3.2, observed 2026-11-14), or on an inherited `BEADS_ACTOR`.

Keep the actor recoverable in the dispatch or the admitted handoff. A child dispatch carries the child's actor, the binding reference, the issue ID of its leaf and the ownership action. The action of a write lane is `claim`: the lane claims its leaf with its own actor, so that the issue names the agent that does the work. The action of a read-only lane is `none`, unless it is separately authorized to mutate issues. The lead keeps one `Lane: <leaf id> <actor>` line per live leaf in the root `notes`. A parent never acts as a child. An agent keeps its actor through compaction and resume; a replacement agent gets a new actor.

Before dependent implementation, read the issue and compare its assignee with your actor. Claim only authorized, unassigned work, with `bd --sandbox update <id> --claim --actor <actor>`, then read the issue back once: the assignee is your actor and the status is `in_progress`. A repeated claim is idempotent only for the same actor. Never claim an in-progress issue that another actor holds, whatever its lease. A claim that another actor holds, a failed claim or a mismatched readback blocks dependent work. Never force a claim, and never take another actor's issue except through the transfer or the takeover below. `## Outage and uncertain writes` states the one outage exception.

Send no heartbeat, and read no lease TTL. Reason: in Beads 1.3.2 a claim by another actor on an in-progress issue fails whatever the lease, `bd ready` lists open issues only, and only `bd reclaim` reads the lease (source read on 2026-11-17 at tag v1.3.2: `internal/storage/issueops/claim.go`, `internal/workapi/ready.go`, `lease.go`). Recheck this after a Beads upgrade. The issue status and assignee carry ownership, on one node and across PCs. Release your own claim with `bd unclaim <id> --if-assignee <actor>`. Never take another actor's claim: `## Beads capabilities in use` rejects the force flags and limits `bd reclaim`.

Every update to an issue you own passes `--if-assignee <actor>`, and also `--if-status <expected-status>` when the update relies on a status. After a guard mismatch (exit 13) or a write with an uncertain outcome, re-read the issue and reconcile under `## Outage and uncertain writes` before any retry. When the re-read shows that another actor holds the issue, stop writing, report it and wait for the user.

**Transfer.** Before you replace an agent or transfer an issue to another device, apply `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`. The authorized transferring agent runs one update with its own `--actor`, with guards on the old assignee and the expected status, and with `--assignee <new-actor>`, then reads the issue back. For a stopped lane, the lead is the transferring agent, and it updates the `Lane:` line in the same pass. Run no closure or other ownership change during the transfer. A refused transfer blocks dependent work; never force it. The new actor acts only after that readback.

**Takeover of your own earlier claim.** A new session has a new actor, so the claim of the session that it continues names the earlier actor. Take that claim over only when all three conditions hold:

1. The user, the dispatch or the admitted handoff gives this session that plan or issue.
2. `bd show <id>` names the earlier actor as the assignee, with the status `in_progress`.
3. Stopped-writer recovery, under the section named above, proved that the earlier writer stopped.

Then run one guarded transfer with your new actor, `bd --sandbox update <id> --if-assignee <old-actor> --if-status in_progress --assignee <new-actor> --actor <new-actor>`, and read the issue back. Continue from the last checkpoint block (`references/context-continuity.md` `## Status and position`). The guards refuse the transfer when the holder changed, and the transfer needs no force flag and no lease. When a condition fails, the issue belongs to another agent that can still be live: leave it, and report it. After a compaction the session keeps its actor and runs no transfer.

**Close.** `bd close` has no assignee guard and no status guard. After the required acceptance passes, run `bd lint <id>`, then close with your actor; the command's result confirms the closure. Before the close, read the issue and verify the assignee and the expected status only after a resume, an outage or a transfer, because only those change them without your knowledge. The lead closes the leaf of a dispatched write lane with the lead's own actor, after three facts hold: the lane returned, the leaf's assignee matches its `Lane:` line, and the lead reconciled the lane's diff. The lead then removes that `Lane:` line. A lane never closes its leaf, so that a dependent leaf becomes ready only after the lead accepts. Run no ownership change or transfer during the close. The sequence is not atomic: uncertain coordination blocks closure, and you report it.

Verified on 2026-11-02 against installed `bd` 1.3.1 (c1c4b642a) help for `update`, `close`, `unclaim` and `heartbeat`; the 2026-10-18 source check named the same commit ([update.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/update.go), [close.go](https://github.com/steveyegge/beads/blob/c1c4b642ac1c/cmd/bd/close.go)). The guarded transfer was read on 2026-11-17 at tag v1.3.2 (`cmd/bd/update.go`, `cmd/bd/assign.go`): its guard compares the assignee name and never the lease. Recheck after upgrade. These rules override actorless upstream examples; the project binding still owns scope and authority.

## One task authority

Under `beads`, Beads owns issue identity, status, priority, assignee, edges and readiness, and the plan holds only the native hierarchy or the phase mappings. Only `Task store: local` tracks mutable task state in Markdown, and only for tasks not yet in Beads.

In a local family, write each task as `- [ ] T1: <outcome> [depends: none] [skills: inherit]`. Keep IDs unique and stable. List prerequisites as comma-separated local IDs, or `none`. Every prerequisite exists, the graph is acyclic, and a completed task's prerequisites are completed. Tick a task only after you observe its outcome and evidence, also for work found already done. The plan's recorded claim proves no exclusivity across agents or PCs.

For an existing flat Beads mapping, or a local family that gains Beads tasks, write `- Issue: <issue-id> [skills: inherit]` in one phase. A task override is its complete `[skills: name, name]` mapping. Record closure in Beads. A local family keeps checkboxes only for tasks not yet migrated. `references/companion-routing.md` owns skill inheritance.

## Beads-native execution plan

Size the plan to the work, because each extra node costs commands and adds no safety:

- One bounded task is one issue, with no root.
- Several tasks are a root epic with the leaf tasks directly under it.
- Register a phase milestone under the root only where a recorded barrier separates two groups of tasks: a collection, review or approval gate that the earlier group passes before the later group starts. Each phase has at least one task.

The root epic is the canonical plan, addressed as `beads:<root-id>` with the actual opaque ID in dispatch, evidence and handoff. Register tasks and subtasks under their actual parent. A task is a leaf, or it has at least two subtasks that are separately claimable and verifiable and have distinct acceptance. Containment never replaces a prerequisite edge. In a plan with no phase, the root takes the place of the phase in every rule of this skill that names a native phase.

Each leaf states its owned paths. Two leaves that can be ready together never own the same file: add a blocking edge between two leaves that must change one file. Reason: disjoint owned paths let several agents work in one checkout with no worktree.

| Issue and field | Canonical content |
|---|---|
| Root `description` | `Plan kind: execution`, `Plan format: beads-native-v1`, portable `Task binding`, outcome, scope and exclusions, constraints, `Registration: draft\|registered`, `Review boundary: phase\|final`, `Final phase` (the exact issue ID of the last phase, or of the root when the plan has no phase), `Commit authority`, shared skill bindings, and the allocation record or exact references to the nodes that hold it |
| Root `design`, `acceptance` | `design`: the settled design and the execution authority under `references/artifact-lifecycle.md`, which is the execution source, scope and decision owner, or the approval and its evidence. `acceptance`: the engagement acceptance |
| Root `notes`, comments | `notes`: the engagement checkpoint block, with one `Lane: <leaf id> <actor>` line per live leaf (`references/context-continuity.md` `## Status and position`). Comments: engagement-wide knowledge, as tagged comments (`references/context-continuity.md` `## Task resume and phase resume`) |
| Phase milestone, where one exists | `description`: the phase number, outcome, barrier rationale, required skills, and the test collection and repair/retest plan. `acceptance`: the phase criteria. Comments: the integrated results, the review verdict and its evidence |
| Task or subtask | `description`: the plan address, the exact phase ID where a phase exists, the outcome, the owned paths and their exclusions, the skill binding or inheritance, ownership and resource conflicts, and focused checks. `design`: settled reasoning, invariants, relevant failures, recovery and decisions. `acceptance`: observable criteria. `notes`: the leaf checkpoint block. Comments: task-local knowledge as tagged comments, and results. The close reason holds the result |

A dispatched write lane owns its leaf, and the lead accepts it. The lane claims the leaf with its own actor, and appends a checkpoint block to the leaf `notes` before it returns or stops, so that a stopped lane leaves its position in Beads. The lead keeps the root checkpoint block with its `Lane:` lines, reconciles the lane's diff, and closes the leaf under `## Agent identity and ownership`. When the lead rejects the result, the leaf stays unclosed, and the lead registers the repair as a follow-up task with a `discovered-from` edge to that leaf.

Review and commit semantics follow `## Phase-task-subtask hierarchy`. A nested invocation uses the same root address and final phase ID, with its own node and checkpoint block; the parent holds root registration and the engagement position. Native status, assignees, parent relations and prerequisites are task truth: keep no mirrored graph, task table, Markdown checkpoint or second editable plan.

Register the root with `Registration: draft`, and claim it before you create children. After an interruption, reuse the nodes that already exist. Add an edge for each real prerequisite; a descendant never blocks on an ancestor. Then run two checks. Run `bd dep cycles`: it must report no cycle. Query `bd ready --label <project-label> --parent <root-id> --limit 0`: a leaf with an open prerequisite must be absent, and an independent leaf must be present.

Mark the root `registered`, through a guarded update, only when both checks pass and the root and phase records hold the settled design, the execution authority and its scope, the engagement acceptance, the exact final phase, the review and final gate plan, and the resolved skill mappings. Reason: other agents claim from `bd ready`, so a draft graph must not look ready. A missing or inconsistent record blocks dependent work. A material change to the plan or the graph pauses the affected dispatch and returns the root to `draft` until you reconcile it. The marker proves no authority, test result or resource independence; apply `## Ready tasks and workflow gates` before each dispatch. Before handoff and completion, reconcile the affected issues and the root, including pending review, commit and curation evidence.

## Phase-task-subtask hierarchy

This section owns the Markdown mappings, and the review and commit semantics that native plans share.

| Markdown execution family | Plan header and work entries |
|---|---|
| New family on Beads | `- Task hierarchy: phase-task-subtask`, `Task store: beads` and its portable `Task binding` |
| New local family | `Task store: local`, `Task binding: not applicable` and `Task store reason: <observed failure>`; local checkbox tasks; no hierarchy marker. Tasks added later are flat `Issue:` entries |
| Existing unmarked family | Its original contract |

Register every phase, task and subtask in bound Beads, with acceptance and parent-child relations, before dependent execution. A phase or milestone maps as `Phase N` and contains one or more tasks. IDs are opaque and unique across the family. Preserve an optional enclosing engagement epic.

A task is an executable leaf with zero subtasks. Use subtasks only when the work has two or more separable parts, each claimable, verifiable and closable on its own evidence, with acceptance that differs from its siblings. The validator rejects exactly one subtask.

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

Use exactly zero, two and four spaces before the phase, task and subtask list markers. A task inherits the phase skills and a subtask the task skills, unless it carries a complete override. Never mix flat `Issue:` entries or local checkboxes into a marked hierarchy. A missing, duplicate, orphan or unresolved executing node blocks dependent work. Offline structure proves no live node, parent-child relation, binding or readiness; verify those through the bound owner.

Containment sets no order: record each real prerequisite as a blocking edge through `## Record task prerequisites` before dispatch.

The plan header records `Review boundary: phase` or `final`, `Final phase: Phase N` and `Commit authority`:

| `Commit authority` value | Use |
|---|---|
| `local commits pre-authorized (main instruction file)` | The default for a new plan. Verify the main instruction rule before you act on it |
| `explicit user grant: <source and scope>` | A separate grant |
| `not granted` | No grant applies |

Local-commit authority covers no push, no tag, no history rewrite and no merge into another branch, except the lane-branch merge under `references/workspace-and-integration.md` `## Lane branches and commits`. Each phase records `Review status` and `Review evidence` apart from any commit checkpoint. A pending review is `REVIEW_PENDING`. A completed review uses the verdict from `references/review-mode.md` with attributable evidence. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` decide when review, independent verification and commits run. A nested invocation inherits this whole-engagement contract and never resets it.

A nested Markdown plan keeps the canonical engagement's `Review boundary` and `Final phase`, reached through `Parent plan`, and records its own last phase as `Local final phase`. Its cursor stays local. Under final-only review its phases keep `REVIEW_PENDING`, because the canonical engagement owns final acceptance. Malformed, conflicting, cyclic, missing or over-limit ancestry blocks initialization. A parent without a representable cadence needs explicit reconciliation: never infer a legacy default, and never migrate the parent's authority.

A completed required review boundary needs resolved `Validation commands` and observed `Evidence observed`. When validation does not apply, record `Validation commands: none (specific reason)` and `Evidence observed: not applicable (specific reason)`.

## Acceptance and evidence by level

Every criterion and result has one owner, chosen by level:

- Phase acceptance and review status: the native phase issue, or the Markdown plan with a reference from its phase issue.
- A task's or subtask's acceptance and result: that node's issue. Under `local`: the plan's task entry.
- Integrated review across tasks: the native phase's evidence comment, or the Markdown phase-evidence section.
- Bulky output: an artifact file under the task-artifact directory that the repository's instructions name, subject to `references/artifact-lifecycle.md` admission. The evidence owner links to it and records the command, the result and the one line that mattered. When the instructions name no such directory, record that no artifact was admitted and keep only those three items; never paste the bulky output.

Record evidence once and link to its owner from every other site, because a copy goes stale silently. Work without a plan keeps all of it in its issue. Plan-held task acceptance stays in the plan until its task migrates; the issue then points to it with an exact plan reference.

## Issue fields

Under `beads`:

| Field | Holds |
|---|---|
| `description` | Goal, scope, output, and a link to the plan and phase |
| `spec_id` | A real file spec, as repository name and repository-relative path, e.g. `skills:docs/_agent_plans/<stem>.md` |
| `acceptance` | The task's criterion, or an exact reference into the plan |
| `design` | A decision affecting the task, plus its reference link |
| `notes` | Position, including blockers, and next step, as the checkpoint block of `references/context-continuity.md` `## Status and position` |
| comments | Learned knowledge as tagged comments (`references/context-continuity.md` `## Task resume and phase resume`); events, including interim validation runs; and curation outcomes when no plan exists |
| close reason | A closed task's result (see `## Close reason`) |

For a Markdown plan, set `spec_id` to the file reference. For a native plan, put the plan address in the description and leave `spec_id` unset unless a real file spec applies. Use custom metadata only for a minimal marker or a named consumer; never copy native fields into it. The plan holds the goal, the shared constraints and phase acceptance.
Durable knowledge, shared hub reminders and binding rules go through `/alaa-memory-os` `## Beads hub reminders and issue notes`, never into an issue field.

## Close reason

Under `beads`, close with three parts: a short verdict, the tested version and the evidence address. The tested version is the commit that contains every tested change. For an uncommitted change, it is the HEAD SHA plus the scoped content SHA-256 digest from `references/workspace-and-integration.md` `## Record the tested state`. Numbers are optional; label each one "at close".

A task or subtask may close after its own acceptance and required tests pass while the boundary review is pending. Say `tested; review pending` and cite its tested snapshot; the closure implies no independent review. Under `Review boundary: final`, an intermediate phase issue may close its implementation and test milestone once those criteria pass, while the plan records `REVIEW_PENDING`. Such a closure advances dependency readiness. It claims no reviewed acceptance and authorizes no commit. A final boundary stays incomplete until its required review, fixes and retests pass.

## Record task prerequisites

At task decomposition, and at a material change to scope or prerequisites, identify the real blockers and reconcile the task store before you start or dispatch affected work. Add no edge between independent tasks.

In Beads, verify the issue IDs and the project scope through the binding, then add or remove only authorized edges. Record each prerequisite as a blocking edge: the dependent issue is blocked by the prerequisite. A description, plan reference, hierarchy or related link establishes no edge. After the change, query native readiness to confirm the direction and the blocking state, because text alone cannot keep blocked work out of the ready set. When registration or verification fails, follow `## Outage and uncertain writes`.

## Beads capabilities in use

Verified on 2026-11-02 against installed `bd` 1.3.1 (c1c4b642a): the `--help` of every command named below (for integration and setup commands, the `bd --help` list), plus read-only `bd where`, `ping`, `ready`, `list`, `show`, `config`, `formula list`, `gate list`, `human list`, `orphans`, `dep cycles`, `graph check` and `lint`. Recheck after a Beads upgrade. Rechecked 2026-11-14 against installed `bd` 1.3.2 (9b65b9e19): the `--help` of every adopted command named below still lists each flag this table names; no behaviour was re-tested. The claim, ready and lease behaviour was read from the v1.3.2 source on 2026-11-17 (`## Agent identity and ownership`). Use a command only as its row states. The last row rejects every command and flag that no other row names. No row grants remote or destructive authority.

| Adopted command | Rule and reason |
|---|---|
| `bd create` with `--parent`, `--spec-id`, `--acceptance`, `--design`, `--labels`, `--deps`, `--validate`, `--dry-run` | Register each node with its parent, acceptance and plan link (`## Issue fields`). `--dry-run` previews. `--validate` checks the issue type's required sections. |
| `bd create --skills`, `--context`, `--body-file`, `--design-file`; `bd update --body-file`, `--design-file` | `--skills` and `--context` append sections to the description ([Beads v1.3.2](https://github.com/steveyegge/beads/blob/v1.3.2/cmd/bd/create.go#L114-L148)); write each section once. Use the file flags for long content, with `-` for stdin where supported. On `bd update` they replace the field; pass the ownership guards. Recheck the installed help and behavior after an upgrade. |
| `bd search` | Search before you create. Closed issues are included by default. |
| Types `decision`, `spike` | `decision`: a decision that other tasks cite. `spike`: a time-boxed investigation whose output is knowledge. |
| `bd dep add`, `bd link` | Record each prerequisite as a blocking edge (`## Record task prerequisites`). Create each follow-up with `--deps discovered-from:<origin-id>`; that edge records provenance and does not block. Per Beads v1.3.1 source (`internal/types/types.go` `AffectsReadyWork`, checked 2026-10-13), readiness counts only blocks, parent-child, conditional-blocks and waits-for edges. |
| `bd dep cycles`, `bd graph check`, `bd swarm validate` | Read-only. Run `bd dep cycles` after you register or change edges, before the affected dispatch. The other two are optional second views of the same graph. Reuse the result while the graph is unchanged. |
| `bd where`, `bd ping`, `bd prime` | Read-only. `bd where` and `bd ping` are the availability test. Run `bd prime` only when hook context is missing or stale. |
| `bd ready`, `bd blocked`, `bd children`, `bd show --children --refs --long`, `bd graph --open`, `bd epic status`, `bd list`, `bd query`, `bd count`, `bd status`, `bd orphans` | Read-only. Filter by the project label. `bd show <id>` prints the description, design, acceptance, notes and comments in one call, and `bd list --assignee <actor>` lists the issues that one actor holds: these two are the resume read. Run `bd ready --explain` when readiness is unexpected. `bd show --long` shows the lease. Run `bd orphans` at a handoff review. |
| `bd update --claim`, `--if-assignee`, `--if-status`, `--assignee`, `bd unclaim --if-assignee` | Use them as `## Agent identity and ownership` states. A guard mismatch exits 13 and writes nothing (installed help). A guard checks only the local database and proves no exclusivity across PCs. A guard requires a field update in the same command. Never combine a guard with `--claim`. |
| `bd reclaim` | Use only `bd reclaim --id <id>` inside stopped-writer recovery, after `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery` verified that the holder stopped and `bd show` displays the expired lease. Never run it bare, with `--any-replica`, or against a live or foreign-replica lease. The replacement then claims the issue with its own actor. |
| `bd defer`, `bd undefer`, `bd update --defer` | Postpone work that nothing blocks, with a `--reason`. A deferred issue leaves `bd ready`. |
| `bd supersede <id> --with <new>` | Replace an obsolete issue or spec. It closes the old issue with a reference. |
| `bd gate create --type human --blocks <id> --reason <why>`, `bd human list` | Gate a decision that only the user may make. Close a gate issue, by any command, only after the user's explicit approval is recorded. Never close your own gate. |
| `bd formula list`, `bd formula show`, `bd mol pour` | Use them only when a formula exists. Run `bd mol pour --dry-run` first, then pour persistent work. `bd formula list` showed no formula on 2026-11-02; authoring one is a separate authorized change. |
| `bd close`, `bd close --suggest-next` | Close as `## Agent identity and ownership` and `## Close reason` state. With `--suggest-next`, read the issues that the close unblocked, and claim none of them automatically. |
| `bd lint`, `bd stale` | Run `bd lint` before you close or hand off an issue. A finding blocks that close or handoff until the section is filled or the gap is recorded in the issue. Run `bd stale` at a handoff or resume review. |
| `bd comments add`, `bd update --append-notes`, `--notes` | Knowledge and events go in `bd comments add`. The checkpoint block goes in `--append-notes`; `--notes` replaces the whole field (`## Issue fields`). |
| `--readonly`, `--sandbox` (global flags) | A read-only lane (ownership action `none`) passes `--readonly`. Every write-capable agent passes `--sandbox` on each `bd` command that can write, unless the user authorized Dolt sync. Read-only commands need none. The installed help says that `--sandbox` disables Dolt auto-push. Batch `bd` writes in one script only when every command passes `--actor` and the script runs with `set -euo pipefail`, prints each command's result and stops at the first failure; read the changed issues back afterwards. Add no per-command environment override. |
| Every other `bd` command and flag | Not adopted: do not run it. The classes with a rule of their own follow. **Takes another actor's claim:** `bd update --force`, `bd unclaim --force`, `bd assign --force`. **Closes without acceptance:** `bd close --force` closes pinned issues and unsatisfied gates, and `bd gate resolve` equals `bd close`. **Claims or closes work that the plan did not designate:** `bd ready --claim`, `bd close --claim-next`, `bd close --continue`, `bd epic close-eligible`, `bd orphans --fix`. **Renews a lease that no rule reads:** `bd heartbeat`. **Owned elsewhere:** `bd remember`, `bd recall` and `bd memories` belong to `/alaa-memory-os` `## Beads hub reminders and issue notes`; `bd ship` and `external:` dependencies need the `external_projects` config, which was unset on 2026-11-02, and `## Cross-project delivery` states their rule. **Remote, setup, destructive or external effect:** every `bd dolt` subcommand, `bd sync`, `bd vc merge`, `bd bootstrap`, `bd init`, `bd hooks`, `bd federation`, `bd backup`, `bd export`, `bd import`, `bd migrate-personal`, `bd delete`, `bd gc`, `bd compact`, `bd flatten`, `bd prune`, `bd purge`, `bd sql`, `bd rename`, `bd rename-prefix` and every integration command (`bd github`, `bd gitlab`, `bd jira`, `bd linear`, `bd notion`, `bd ado`, `bd repo`, `bd serve`). Such a command needs the user's explicit authorization for that action. |

## Cross-project delivery

When one project needs another project's output, create a delivery task in the producer project, with the producer's label and the outcome "the output is available to the consumer". The consumer's task depends on it through a blocking edge (`## Record task prerequisites`). When you cannot verify the producer and the consumer through the same binding or hub, stop the edge registration and report it.

## Ready tasks and workflow gates

Use the selected store's prerequisite graph for task readiness. A ready task still requires registered scope, authority, available deliverables and source, mapped skills, independent files and environments, and satisfied phase barriers. Closing all issues proves none of the workflow lifecycle states in `references/workspace-and-integration.md`.

A claim locks no file or resource, and independently synced PC databases give no mutual exclusion. Resolve shared-resource conflicts before parallel work under `references/workspace-and-integration.md` `## Shared-file ownership and stopped-writer recovery`. Before a cross-PC transfer, verify that the designated owner can reach the actual source and the attributable evidence; a synced issue does not make another PC's uncommitted code available. Git source sync and Dolt task sync are separate actions with separate authorization. Run a Dolt remote or sync command (`bd dolt push`, `bd dolt pull`, `bd dolt remote`, `bd sync`) only with the user's explicit authorization for that action. Report a sync as complete only after you observed its result. `references/context-continuity.md` `## Cross-PC handoff record` owns the handoff record.

## Outage and uncertain writes

When Beads is unreachable before plan admission, apply the Unavailable rule in `## Select before tracking-dependent work`. When Beads returns, register previously untracked work only if it is still open.

A Beads-bound family that loses Beads mid-run keeps its store. Preserve evidence. Pause every claim, dispatch and closure that needs Beads state. Continue only independently authorized work on tasks that you already claimed and read back. Reconcile through Beads when it returns.

When you hold no claimed task, wait for the hub, unless the user names one unclaimed task and chooses to proceed on it. On recovery, read the task back. If another actor holds it, stop and report the collision. If it is unassigned, claim it before more work.

Record the outage and a dated `Pending Beads reconciliation` list of evidence, notes and discoveries in the admitted Markdown checkpoint or direct cursor. For a native plan or issue-only work, use the session, or an already authorized evidence-only artifact. Keep no offline task mirror. Label unsaved items pending. On recovery, record each entry at its Beads owner and read it back before you clear the list. Pending reconciliation blocks closure and completion. At an outage handoff, transmit the list verbatim and name the blocker.

After a mutation with an uncertain outcome, read the actual task state through the bound owner, then perform only the authorized change that is still required. Never retry blindly, and never report success without evidence.

## Helper boundary and compatibility

The Markdown helpers take the store and binding as arguments (`references/artifact-lifecycle.md`) and never contact Beads. The validator requires the reason for local execution and rejects it for Beads. Review defaults to `phase` at the root, inherits the canonical parent cadence when nested, and rejects a conflicting override. A profile or alias never replaces task authority.

For execution and existing compatible families, a `Task store` or a `Task binding` header marks a family. A marked family requires exactly one of each header, a supported store and a valid pairing under every profile, `legacy` included. A family with neither header keeps the old contract. An unresolved marker in a draft may warn; unresolved executing work fails even when the header says planning.

Install compatible instructions, templates and helpers together before you execute a newly marked family, because an older consumer cannot execute it safely. On rollback, freeze marked families until compatible consumers return, and never convert issues to checkboxes.

## Migrating a local family

Apply this when `## Select before tracking-dependent work` finds Beads available and a family records `Task store: local`. Migration grants no installation, live mutation, sync or publication authority.

1. Before the first Beads task, replace `Task binding: not applicable` with the adopted portable binding. Keep `Task store: local` and its reason as history.
2. Register every new task in Beads and map it as `- Issue: <issue-id> [skills: inherit]` in its phase. A Beads task never depends on an open local task; migrate that task first.
3. To migrate an open local task, register it in Beads and read it back, then mark it `- [-] T2: <outcome> [depends: T1] [migrated: <issue-id>] [skills: inherit]`, with its `- Issue:` mapping in the same plan. Migrate its local dependents with it. Every prerequisite of a migrated task must already be completed or migrated. The validator rejects a local task that depends on a migrated one, and a migrated task with any other prerequisite (`plan.local-dependency`).
4. Completed local tasks stay as history. A migrated task lives only in Beads. Never migrate from Beads back to local.
