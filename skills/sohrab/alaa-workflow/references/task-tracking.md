# Task Tracking

This file owns task-store selection, task authority, readiness and migration. Artifact admission and profiles remain in `references/artifact-lifecycle.md`; execution position remains in `references/context-continuity.md`.

## Select before tracking-dependent work

Task store and artifact profile are independent. Continue an existing family's recorded task store until explicit migration. For new work, select `beads` only when project instructions/configuration explicitly adopt Beads and provide a binding; otherwise select `local`. A CLI, installed skill, hook context or local `.beads` directory alone selects nothing. A valid binding can point to an external hub without a repository-local database.

The project binding owns workspace identity, project scope, and authority. Record its nonempty repository-relative instruction/configuration reference, optionally with a `#anchor`, rather than copying settings or machine paths. The reference must contain no absolute machine path, multiline value, backtick, or unresolved marker. Helpers check its format, not owner existence/configuration. Resolve conflicting or incomplete adoption/binding before tracking-dependent work. Verify active workspace and project through the binding owner before reading/changing issues; a reachable wrong hub is not the configured store.

For Beads mechanics, load the installed upstream Beads skill separately and reuse fresh hook/prime guidance. Neither hooks nor guidance own current task state. If the required binding or upstream owner is unavailable, report the gap and stop its dependent work. Do not copy a CLI manual, implement another client, install hooks, initialize a replacement database or silently fall back to local.

## One task authority

| Store | Task owner | Plan work entries |
|---|---|---|
| `local` | Plan tasks own progress and prerequisite edges | Stable ID, outcome, dependency list and skill mapping |
| `beads` | Beads owns issue identity, status, priority, assignee, issue edges and native readiness | Unique issue ID mapped to one phase, with its skill mapping |

For marked local families, write each task as `- [ ] T1: <outcome> [depends: none] [skills: inherit]`. Keep IDs unique and stable across the plan. Use comma-separated local IDs for prerequisites; `none` means no prerequisites. Every prerequisite must exist, the graph must be acyclic, and completed tasks' prerequisites must be completed. Tick only after observing the task's outcome and evidence, including work verified as already done. The local plan's recorded claim/ownership coordinates; it does not prove exclusivity across agents or PCs.

For Beads, write `- Issue: <issue-id> [skills: inherit]`, using the actual opaque ID without assuming a prefix. Map each issue uniquely to one phase; a task override is its complete `[skills: name, name]` mapping. Keep no authoritative local checkbox/numbered task list or editable issue register alongside these mappings. Issue closure is recorded in Beads, never by ticking a plan mirror. `references/companion-routing.md` owns inherited/override skill semantics for both stores.

Plans own goal/scope, phase design and acceptance, evidence, skill associations, shared-resource conflicts and integration barriers. Existing task acceptance stays in its canonical plan section and the issue links it. New issue-only work may own acceptance in its issue. Never retain editable copies of the same acceptance or evidence. Small Beads-only work can use issue notes for handoff without forcing workflow files; artifact admission still applies.

## Record task prerequisites

At task decomposition and material changes to scope or prerequisites, identify genuine blockers and reconcile the selected task store before starting or dispatching affected work. Keep independent tasks independent.

For Beads, inspect existing issues and edges and verify IDs and project scope through the binding before changing dependencies. Use the upstream skill and installed CLI help to apply only authorized missing or obsolete edge changes. Record each prerequisite as a blocking edge: the dependent issue is blocked by the prerequisite. Descriptions, plan references, hierarchy and related links do not establish that edge. Read back affected dependencies and query native readiness to confirm the intended direction and blocking state before proceeding; text alone cannot keep blocked work out of the ready set. If registration or verification fails, follow the outage and uncertain-write rules below.

## Ready tasks and workflow gates

Use the selected store's prerequisite graph for task readiness. A ready task still requires scope, authority, available deliverables/source, mapped skills, and file/environment independence before dispatch. Phase dependencies and acceptance barriers stay in the plan; native issue readiness does not satisfy them. Closing all issues proves none of the workflow lifecycle states defined in `references/workspace-and-integration.md`.

A claim does not lock files, fixtures, generators, ports or test environments, and independently synced PC databases do not establish mutual exclusion. Designate task ownership and resolve shared-resource conflicts before parallel work. Before cross-PC transfer, verify that the designated owner can access the actual source and attributable evidence. Git source sync and Dolt task sync are separate actions with separate authorization; a synced issue does not make another PC's uncommitted code available.

## Outage and uncertain writes

When configured Beads is unavailable or its workspace/project mismatches, preserve existing evidence and continue only independent authorized analysis. Stop tracking-dependent implementation, dispatch and closure. Report the actual blocker and next safe action; do not create local replacement tasks or claim a failed update was saved.

After a mutation with an uncertain outcome, read actual task state through the bound owner before retrying. Reconcile whether the requested effect landed, then perform only the still-required authorized change. Do not retry blindly or report success without evidence. Resume and evidence reconciliation follow `references/context-continuity.md` and `references/workspace-and-integration.md`.

## Helper boundary and compatibility

The initializer takes `--task-store {local,beads}`, defaulting to local for compatibility, and `--beads-binding <portable-reference>` for Beads. Resolve adoption before invoking it; it never discovers a store from PATH, environment or directory existence. Local binding is `not applicable`. Beads binding is required; Beads with deprecated standalone `--state-only` is invalid. Helpers invoke no Beads command, service or network operation.

Either `Task store` or `Task binding` metadata header marks a family. Marked families require exactly one of each, a supported store and valid pairing under every profile, including legacy. Both absent retains the old compatibility contract. Draft unresolved markers may warn; unresolved executing work fails even when the overall header still says planning. Offline validation checks metadata, graph/mappings, skills and snapshots; it proves no live issue existence, bound workspace, project scope or readiness.

Install compatible instructions, templates, and helpers together before executing a newly marked family. Older consumers may skip mappings or gates and cannot safely execute it. On rollback, freeze marked families until compatible consumers return; preserve task truth/evidence rather than converting issues to checkboxes or selecting local. Existing unmarked families remain under their original compatible contract.

Migration is explicit: identify the old authority, verify the destination binding and issue/task mapping, preserve canonical acceptance/evidence and designate the cutover owner before changing authority. Keep the old task store read-only after cutover so rollback has its evidence; never maintain two mutable task owners. Migration and this skill grant no installation, live mutation, sync or publication authority.
