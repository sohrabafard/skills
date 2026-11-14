# Workspace Evidence and Integration

`references/context-continuity.md` owns artifact contents. This file owns workspace identity, Git authority, and the four completion states. A commit is one durable checkpoint; a scoped worktree snapshot identifies evidence when committing is not authorized.

## Before the first write

1. **Record the base and checkout.** Capture the current branch, HEAD SHA, and worktree path. If integration is requested, also capture the target branch and its base SHA. A resumed agent needs those identities to determine what changed.
2. **Map existing changes.** Treat unowned modified and untracked paths as user or other-lane work. Preserve them and continue on disjoint paths. Resolve overlapping ownership before editing the same file; never stash, stage, overwrite, or commit another owner's change.
3. **Keep the checkout.** Continue in the same checkout and preserve its diff. Disjoint-file writers may share it. Do not create a branch or worktree automatically; the one exception is the lane branch that `## Lane branches and commits` prescribes for dispatched write lanes. Use a different checkout only when that section routes a lane to a worktree, or when the user or an already authorized explicit plan requires it. Reconcile overlapping ownership before writes through the protocol below.
4. **Honor explicitly authorized isolation.** If a lane worktree is explicitly required, create it from the recorded HEAD SHA, pass its path to the lane and verify `git merge-base --is-ancestor <base-sha> HEAD` before editing. A remote default branch or runtime isolation option is no substitute for the recorded base; a mismatch blocks that lane. Creating a branch or worktree grants no commit or merge authority by itself; `## Lane branches and commits` states the only lane commit grant and the lane merge.

## Lane branches and commits

This section applies when a runtime orchestrator dispatches implementation or documentation lanes that write files. `alaa-cc-orchestrator` and `alaa-codex-orchestrator` `references/verification-and-gates.md` time the merge against the declared review boundary.

1. **Create the lane branch.** Before the first implementation or documentation dispatch of a ready set, the lead creates one lane branch from the recorded HEAD and switches the checkout it runs in to that branch, unless step 2 recorded isolation for a writer the lead does not control. The lead records the branch name in the plan or the compact dispatch. When an accepted lane branch was merged, the next ready set gets a new lane branch; an unmerged one stays the branch for later ready sets. The lead switches branches or merges only while no lane is live in that checkout. When the run stops before a merge, the lead switches back to the work branch once no lane is live, and reports the unmerged lane branch.
2. **Share the checkout.** One implementer, or several implementers whose owned files do not overlap, work in that same checkout on that one branch. They need no separate worktree. Before lanes share the checkout, the lead inspects the repository's commit hooks. When a hook stashes, stages, restores or rewrites files outside the committed paths, the lead records isolation as required in the plan, so that step 3 gives each write lane its own worktree. A lane never bypasses a hook. The lead also checks for a writer it does not control: new commits on the checked-out branch since the recorded HEAD, or unowned files that change while the lead observes them. When it finds one, the lead records isolation as required in the plan and keeps that checkout's branch. Step 3 then gives each write lane its own worktree and branch, and the lead commits its own records on the branch it is on.
3. **Isolate only on overlap or plan.** Use a separate worktree with its own branch only when the owned files of two lanes overlap, or when the plan explicitly requires isolation. Create and verify it under step 4 above. Its branch is that lane's lane branch for the rules below.
4. **Grant commits by naming the branch.** A dispatch grants commit authority only by naming the lane branch. A dispatch that names no lane branch grants no commit authority; the lane then returns its work uncommitted.
5. **Commit owned paths by path.** A lane with the grant commits its own work when its focused checks pass. It stages and commits only its owned paths, named by path: `git add -- <owned paths>`, then `git commit -m "<message>" -- <owned paths>`. It makes one Conventional Commit per topic, with no agent attribution. It never runs `git add -A`, `git add .` or `git commit -a`, and it never stages or commits another owner's path. The reason: the index is shared in one checkout, so a commit without paths takes another lane's staged files. For a rename or a deletion, the owned paths include the old path.
6. **Leave the shared checkout as it is.** A lane never changes what the shared checkout points at or holds. It runs no `switch`, branch `checkout`, `reset` that moves HEAD, `stash`, `rebase`, `commit --amend`, `merge`, `tag` or `push`, and no `checkout`, `reset` or `restore` of a path it does not own. When a commit fails on the index lock, the lane waits and retries the same commit once. When the retry or any other commit fails, the lane leaves its work uncommitted and reports the command and the error.
7. **Treat a lane commit as a checkpoint.** A lane commit is not acceptance. Review follows the declared review boundary. A fix before the merge lands on the same lane branch. A fix after the merge, such as one the final validation requires, gets a new lane branch under step 1 and merges after the gate that required it accepts it.
8. **Merge only accepted branches.** After the independent gates accept the lane branch, the lead merges it into the work branch with `git merge --no-ff` and deletes the lane branch. When the lane used a separate worktree, the lead also removes that worktree after the merge. The lead never merges a branch that the gates did not accept. This lane merge brings accepted work into the work branch. It is not the integration that `MERGE_CANDIDATE` qualifies.
9. **Commit unowned and returned work as the lead.** The lead commits work that no lane owns: integration repairs, and plan and record files. When a lane returns its work uncommitted and its focused checks passed, the lead commits that work by path on the lane branch, one Conventional Commit per topic. When the lane's commit failed under step 6, the lead first resolves the reported cause.
10. **Report the commits.** The lane report names each commit it made, with short hash and subject, and the branch, or says that nothing was committed and why.

The local-commit authority covers the lane commits, the lane merge, the lane-branch deletion and the removal of a merged lane's separate worktree. Push, tag, any other merge, history rewrite and remote sync keep the explicit-permission rule under `## What still needs the user`.

## Shared-file ownership and stopped-writer recovery

Allow one active writer per file, generated output or shared runtime resource, not one writer per worktree. Record ownership and conflicts in the existing plan or dispatch and in the selected task authority. The runtime orchestrator allocates lanes and capacity. Separate files permit concurrent writers only when their generated outputs and runtime resources are also disjoint. A task claim does not lock a file or a resource.

Assign distinct ports, database or tenant test namespaces, queue names and temporary output directories when the repository supports that isolation. Verify each lane's effective configuration before parallel checks. Serialize users of any resource that cannot be isolated.

Before replacing or resuming a stopped writer's overlapping scope:

1. Verify the prior writer process and every descendant have stopped. A returned agent turn, interrupted session or closed terminal alone proves no process termination. Preserve the process identity and the observed liveness evidence; when any descendant's liveness is unknown, ownership is unresolved.
2. Observe that the scoped files, generated outputs and shared resources stay stable after those processes stop. Preserve surviving edits and compare them with the existing progress journal, bound issue and checkpoint; reconcile completed work, remaining scope, ownership and attributable evidence. Create no journal or locking system for this check.
3. Apply `references/task-tracking.md` `## Agent identity and ownership` for any authorized issue transfer and readback. Only then assign the remaining overlapping writes to the replacement. Preserve valid completed work; do not replay it or reset the diff.

If liveness, stability or ownership remains ambiguous, block only overlapping writes and shared-resource use. Continue independently owned disjoint work. Recovery stays in the same checkout. Compaction does not transfer a living writer's ownership; recover the same actor and reconcile its active process before continuing. A replacement never takes over merely because context was lost.

## Record the tested state

The rules for tested state, integration evidence and the completion lifecycle cover execution and issue-only implementation. Design records sources and observed validation in its plan without execution phases, snapshots or implementation verdicts. Authority limits apply to every kind.

Before a gate, hold writes to its tested scope. Record the command, result, HEAD SHA, scoped paths, and a SHA-256 digest of a deterministic manifest of those paths and their file contents, including untracked files. Record the manifest method and observation time so a resumed agent can compare the same inputs. A commit SHA may replace the content digest only when the commit contains every tested change. A Git ref alone does not identify uncommitted contents.

Local commits follow the main instruction file's local-commit rule. Dispatched lanes commit on their lane branch under `## Lane branches and commits`. Other finished, validated work is committed on the current branch as it lands, at any phase, including before final review. Stage only its changes, preserving unrelated work. Use one Conventional Commit per topic or lane without agent attribution; authorized worktree lanes branch from the latest commit. Record authority once; never ask again within its scope. A commit is a checkpoint, not acceptance: record review separately and repair findings through subsequent validated commits, without rewriting history. Record scoped checkpoint validation even while its phase remains in progress. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` own scheduling and the merge timing. Without authority or validation, preserve an identified snapshot and report the gap.

## Reconcile evidence before running checks

Record each required outcome and its evidence at the level owner in `references/task-tracking.md` `## Acceptance and evidence by level`, retaining the tested identity above.

Before integration, resume or final validation, load /alaa-testing-strategy `references/100-test-execution.md` for execution evidence, aggregation and reuse; its `references/120-result-classification.md` decides whether a result is valid. Workflow reconciles those decisions with the current checkout and records which proof remains attributable. The runtime orchestrator owns independent acceptance and commissions missing or invalidated proof at its declared boundary.

## What still needs the user

The main instruction file supplies local-commit authority; skill activation supplies none. Push, merge into another branch, tag, history rewrite, remote sync, publication, deployment, installation and branch deletion require explicit user permission for that action; local-commit authority covers none of them. The one exception is the lane-branch merge, the lane-branch deletion and the removal of a merged lane's worktree under `## Lane branches and commits`. Requested implementation authorizes scoped local edits and validation.

## The completion lifecycle

Every execution run reports all four states of proven work. Each carries its own verdict — proven, not proven with the blocker named, or not requested — because one word for "done" reads the same over a change that is committed and reviewed as over one that is merely written.

| State | Proven when |
|---|---|
| `IMPLEMENTED` | the change's focused proof passed on an identified snapshot. Record an authorized commit when one exists; otherwise record the observed HEAD and scoped content hash and name the uncommitted recovery risk |
| `MERGE_CANDIDATE` | every integration gate the change affects passed, as the run's own pipeline defines them, and the independent review the change required returned its verdict |
| `RELEASE_CANDIDATE` | the user asked for a release, and the release prerequisites the target repository itself defines passed |
| `PUBLISHED` | an authorized immutable publication landed — a push, a tag, a released artifact — and its evidence was observed on the remote rather than inferred from a command that exited zero |

**A blocker in a later state never unproves an earlier one.** A failed release prerequisite leaves `IMPLEMENTED` and `MERGE_CANDIDATE` exactly as they were proven. Collapsing the ladder to its lowest failure hides finished work and buys it a second time, and that is the whole reason a run reports four verdicts instead of one. Only evidence against a state's own condition moves that state — a commit that is gone, a gate that now fails.

**A release is requested, never inferred.** An instruction to implement, fix, or merge authorizes no release step. With no explicit release request from the user, `RELEASE_CANDIDATE` and `PUBLISHED` report not requested, which is a complete outcome and not a gap to close.

**A state is a report, never an authority.** *What still needs the user* governs every action these states describe. Reaching one state never licenses a commit, merge, push, or tag.

## The integration handshake

Run this only when integration was requested and the required Git actions were authorized. Complete the local implementation and its gates first.

1. **Compare the target base.** If it moved, integrate it into the work branch only with the user's authorization. Resolve conflicts against the plan on the work branch; a conflict whose correct resolution is not decidable from the plan needs the user's decision.
2. **Validate the tree that would land.** A base integration changes the tested snapshot even without a conflict. Run the affected integration gates at the required tier on that new tree. Reuse a prior result only when its observed snapshot and inputs are unchanged.
3. **Present the concrete result.** Give the user the branch or checkout, commits or scoped worktree snapshot, diffstat, gate verdicts, and residual risks. If merge authority is still missing, request it after the result is reviewable.
4. **Apply only authorized integration.** Merge only after explicit authorization. Push, tag, publication, and any worktree removal or branch deletion outside `## Lane branches and commits` each remain separate actions under their own authority limits. Verify and report any action actually performed.

If authorization is absent, leave the worktree and base intact and report the verified local state. That is a complete outcome for work whose requested scope was local.

## What this file does not own

- Which tests run at which strength: `/alaa-testing-strategy`.
- Lane allocation and capacity: `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` for the active runtime; this file owns shared-file exclusivity and recovery.
- What is written into the plan, checkpoint, and handoff package: `references/context-continuity.md` and `references/artifact-lifecycle.md`.
