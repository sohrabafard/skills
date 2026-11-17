# Workspace Evidence and Integration

This file owns workspace identity, Git authority and the four completion states. A commit is one durable checkpoint. A scoped worktree snapshot identifies evidence when committing is not authorized.

## Before the first write

1. **Record the base and checkout.** Capture the current branch, the HEAD SHA and the worktree path. When integration is requested, also capture the target branch and its base SHA. A resumed agent needs them to see what changed.
2. **Map existing changes.** Treat unowned modified and untracked paths as user or other-lane work: preserve them and work on disjoint paths. Resolve overlapping ownership before you edit the same file. Never stash, stage, overwrite or commit another owner's change.
3. **Keep the checkout.** Continue in the same checkout and preserve its diff. Writers of disjoint files may share it. Do not create a branch or worktree automatically. The exceptions are the lane branch and the lane worktree that `## Lane branches and commits` prescribes, and a checkout that the user or an already authorized plan requires.
4. **Honor required isolation.** Create a required lane worktree from the recorded HEAD SHA, pass its path to the lane, and verify `git merge-base --is-ancestor <base-sha> HEAD` before editing. A remote default branch or a runtime isolation option is no substitute for the recorded base; a mismatch blocks that lane. Restore the lane worktree's dependencies from the committed lockfile with the repository's own command; that restore is part of creating the worktree, not an installation that needs permission. A branch or a worktree grants no commit or merge authority.

## Lane branches and commits

This section applies when a runtime orchestrator dispatches file-writing implementation or documentation lanes. `alaa-cc-orchestrator` and `alaa-codex-orchestrator` `references/verification-and-gates.md` time the merge against the declared review boundary.

1. **Create the lane branch.** Before the first implementation or documentation dispatch of a ready set, the lead creates one lane branch from the recorded HEAD, switches its checkout to that branch, and records the branch name in the plan or the compact dispatch. The lead does not switch when step 2 recorded isolation for a writer that it does not control. After an accepted lane branch is merged, the next ready set gets a new lane branch; an unmerged one stays the branch for later ready sets. The lead switches branches or merges only while no lane is live in that checkout. When the run stops before a merge, the lead switches back to the work branch once no lane is live, and reports the unmerged lane branch.
2. **Share the checkout.** One implementer, or several implementers whose owned files do not overlap, work in that checkout on that one branch, with no separate worktree. Before lanes share the checkout, the lead checks for two conditions that require isolation:
   - a commit hook that stashes, stages, restores or rewrites files outside the committed paths. A lane never bypasses a hook.
   - a writer that the lead does not control: new commits on the checked-out branch since the recorded HEAD, or unowned files that change while the lead observes them. In this case the lead keeps that checkout's branch and commits its own records on it.

   When isolation is required, the lead records it in the plan, and step 3 gives each write lane its own worktree and branch.
3. **Isolate only on overlap or plan.** Use a separate worktree with its own branch only when the owned files of two lanes overlap, or when the plan requires isolation. Create and verify it under `## Before the first write` step 4. Its branch is that lane's lane branch for the rules below.
4. **Grant commits by naming the branch.** A dispatch grants commit authority only by naming the lane branch. A lane whose dispatch names no lane branch returns its work uncommitted.
5. **Commit owned paths by path.** A lane with the grant commits its own work when its focused checks pass: `git add -- <owned paths>`, then `git commit -m "<message>" -- <owned paths>`. It makes one Conventional Commit per topic, with no agent attribution. It never runs `git add -A`, `git add .` or `git commit -a`, and never stages or commits another owner's path, because one checkout has one index and a commit without paths takes another lane's staged files. For a rename or a deletion, the owned paths include the old path.
6. **Leave the shared checkout as it is.** A lane runs no `switch`, branch `checkout`, `reset` that moves HEAD, `stash`, `rebase`, `commit --amend`, `merge`, `tag` or `push`, and no `checkout`, `reset` or `restore` of a path it does not own. When a commit fails on the index lock, the lane waits and retries the same commit once. When the retry or any other commit fails, the lane leaves its work uncommitted and reports the command and the error.
7. **Treat a lane commit as a checkpoint.** A lane commit is not acceptance. A review runs at the declared review boundary when the runtime orchestrator's verification decision or a floor calls for one. A fix before the merge lands on the same lane branch. A fix after the merge gets a new lane branch under step 1, and merges after the gate that required it accepts it.
8. **Merge only accepted branches.** After the required verification accepts the lane branch, the lead merges it into the work branch with `git merge --no-ff`, deletes the lane branch, and removes the lane's separate worktree when it had one. The required verification is what the runtime orchestrator's verification decision and its floors set: the lead's recorded verdict, or an independent gate where one is required. The lead never merges a branch that this verification did not accept. This lane merge is not the integration that `MERGE_CANDIDATE` qualifies.
9. **Commit unowned and returned work as the lead.** The lead commits work that no lane owns: integration repairs, and plan and record files. When a lane returns uncommitted work whose focused checks passed, the lead commits it by path on the lane branch, one Conventional Commit per topic. The lead first resolves a commit failure that the lane reported under step 6.
10. **Report the commits.** The lane report names each commit with its short hash and subject, and the branch, or says that nothing was committed and why.

The local-commit authority covers the lane commits, the lane merge, the lane-branch deletion and the removal of a merged lane's separate worktree. Push, tag, any other merge, history rewrite and remote sync keep the explicit-permission rule under `## What still needs the user`.

## Shared-file ownership and stopped-writer recovery

Allow one active writer per file, generated output or shared runtime resource, not one writer per worktree. Separate files permit concurrent writers only when their generated outputs and runtime resources are also disjoint. A task claim does not lock a file or a resource. Record ownership and conflicts in the plan or the dispatch, and in the selected task authority.

Give each lane distinct ports, database or tenant test namespaces, queue names and temporary output directories where the repository supports that isolation, and verify each lane's effective configuration before parallel checks. Serialize the users of a resource that cannot be isolated.

Before you replace or resume a stopped writer's overlapping scope:

1. Verify the prior writer process and every descendant have stopped. A returned agent turn, interrupted session or closed terminal alone proves no process termination; when any descendant's liveness is unknown, ownership is unresolved.
2. Observe that the scoped files, generated outputs and shared resources stay stable after those processes stop. Preserve surviving edits and compare them with the existing progress journal, bound issue and checkpoint. Create no journal or locking system for this check.
3. Apply `references/task-tracking.md` `## Agent identity and ownership` for an authorized issue transfer. Only then assign the remaining overlapping writes to the replacement. Keep valid completed work; do not replay it or reset the diff.

If liveness, stability or ownership remains ambiguous, block only overlapping writes and shared-resource use. Continue independently owned disjoint work. Recovery stays in the same checkout. Compaction does not transfer a living writer's ownership; recover the same actor and reconcile its active process before continuing (actor recovery: `references/task-tracking.md` `## Agent identity and ownership`).

## Record the tested state

The rules for tested state, integration evidence and the completion lifecycle cover execution and issue-only implementation. A design plan records its sources and observed validation, with no snapshots and no implementation verdicts. Authority limits apply to every kind.

Before a gate, hold writes to its tested scope. Record the command, the result and the tested identity. The identity is the commit SHA when that commit contains every tested change. Otherwise it is the HEAD SHA, the scoped paths, and a SHA-256 digest of a deterministic manifest of those paths and their file contents, untracked files included, with the manifest method and the observation time, so that a resumed agent can compare the same inputs. A Git ref alone does not identify uncommitted contents.

Local commits follow the main instruction file's local-commit rule. A dispatched lane commits on its lane branch under `## Lane branches and commits`. Commit other finished, validated work on the current branch as it lands, at any phase, including before final review. Stage only its changes. Use one Conventional Commit per topic, with no agent attribution. An authorized worktree lane branches from the latest commit. Record the authority once, and never ask again within its scope. A commit is a checkpoint, not acceptance: record review separately, and repair findings through later validated commits without rewriting history. Record a scoped checkpoint's validation even while its phase is in progress. Without authority or validation, preserve an identified snapshot and report the gap.

## Reconcile evidence before running checks

Record each required outcome and its evidence at the level owner in `references/task-tracking.md` `## Acceptance and evidence by level`, with the tested identity above.

Before integration, resume or final validation, load /alaa-testing-strategy `references/100-test-execution.md` for execution evidence, aggregation and reuse. Its `references/120-result-classification.md` decides whether a result is valid. Workflow reconciles those decisions with the current checkout and records which proof remains attributable. The runtime orchestrator commissions missing or invalidated proof at its declared boundary.

## What still needs the user

The main instruction file supplies local-commit authority; skill activation supplies none. Push, merge into another branch, tag, history rewrite, remote sync, publication, deployment, installation and branch deletion each need the user's explicit permission for that action. The one exception is the lane-branch merge, the lane-branch deletion and the removal of a merged lane's worktree under `## Lane branches and commits`. A request to implement authorizes scoped local edits and validation.

## The completion lifecycle

Every execution run reports all four states. Each state carries its own verdict: proven, not proven with the blocker named, or not requested.

| State | Proven when |
|---|---|
| `IMPLEMENTED` | the change's focused proof passed on an identified snapshot. Record an authorized commit when one exists; otherwise record the observed HEAD and scoped content hash and name the uncommitted recovery risk |
| `MERGE_CANDIDATE` | every integration gate the change affects passed, as the run's own pipeline defines them, and the independent review the change required returned its verdict |
| `RELEASE_CANDIDATE` | the user asked for a release, and the release prerequisites the target repository itself defines passed |
| `PUBLISHED` | an authorized immutable publication landed — a push, a tag, a released artifact — and its evidence was observed on the remote rather than inferred from a command that exited zero |

- **A blocker in a later state never unproves an earlier one.** A failed release prerequisite leaves `IMPLEMENTED` and `MERGE_CANDIDATE` as they were proven. Only evidence against a state's own condition moves that state: a commit that is gone, a gate that now fails.
- **A release is requested, never inferred.** An instruction to implement, fix or merge authorizes no release step. Without an explicit release request from the user, `RELEASE_CANDIDATE` and `PUBLISHED` report not requested, which is a complete outcome.
- **A state is a report, never an authority.** `## What still needs the user` governs every action that these states describe. Reaching a state licenses no commit, merge, push or tag.

## The integration handshake

Run this only when integration was requested and the required Git actions were authorized. Complete the local implementation and its gates first.

1. **Compare the target base.** If it moved, integrate it into the work branch only with the user's authorization. Resolve conflicts against the plan; a conflict that the plan cannot decide needs the user's decision.
2. **Validate the tree that would land.** A base integration changes the tested snapshot even without a conflict. Run the affected integration gates at the required tier on the new tree. Reuse a prior result only when its observed snapshot and inputs are unchanged.
3. **Present the concrete result.** Give the user the branch or checkout, the commits or the scoped worktree snapshot, the diffstat, the gate verdicts and the residual risks. Request missing merge authority only after the result is reviewable.
4. **Apply only authorized integration.** Merge only after explicit authorization. Push, tag, publication, and any worktree removal or branch deletion outside `## Lane branches and commits`, each stay a separate action under its own authority limit. Verify and report each action that you performed.

Without authorization, leave the worktree and the base intact and report the verified local state. That is a complete outcome for work whose requested scope was local.
