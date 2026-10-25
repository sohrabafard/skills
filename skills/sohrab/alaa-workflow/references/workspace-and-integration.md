# Workspace Evidence and Integration

`references/context-continuity.md` owns artifact contents. This file owns workspace identity, Git authority, and the four completion states. A commit is one durable checkpoint; a scoped worktree snapshot identifies evidence when committing is not authorized.

## Before the first write

1. **Record the base and checkout.** Capture the current branch, HEAD SHA, and worktree path. If integration is requested, also capture the target branch and its base SHA. A resumed agent needs those identities to determine what changed.
2. **Map existing changes.** Treat unowned modified and untracked paths as user or other-lane work. Preserve them and continue on disjoint paths. Resolve overlapping ownership before editing the same file; never stash, stage, overwrite, or commit another owner's change.
3. **Keep the checkout.** Continue in the same checkout and preserve its diff. Disjoint-file writers may share it. Do not create a branch or worktree automatically; use a different checkout only when the user or an already authorized explicit plan requires it. Reconcile overlapping ownership before writes through the protocol below.
4. **Honor explicitly authorized isolation.** If a lane worktree is explicitly required, create it from the recorded HEAD SHA, pass its path to the lane and verify `git merge-base --is-ancestor <base-sha> HEAD` before editing. A remote default branch or runtime isolation option is no substitute for the recorded base; a mismatch blocks that lane. Branch/worktree authority grants no commit or merge authority.

## Shared-file ownership and stopped-writer recovery

Allow one active writer per file, generated output or shared runtime resource, not one writer per worktree. Record ownership and conflicts in the existing plan/dispatch and selected task authority. The runtime orchestrator allocates lanes and capacity; separate files permit concurrent writers only when their generated outputs and runtime resources are also disjoint. A task claim is no file or resource lock.

Before replacing or resuming a stopped writer's overlapping scope:

1. Verify the prior writer process and every descendant have stopped. A returned agent turn, interrupted session or closed terminal alone proves no process termination. Preserve process identity and observed liveness evidence; unknown descendant liveness is unresolved ownership.
2. Observe the scoped files and generated/shared resources are stable after those processes stop. Preserve surviving edits and compare them with the existing progress journal, bound issue and checkpoint; reconcile completed work, remaining scope, ownership and attributable evidence. Create no journal or locking system for this check.
3. Apply `references/task-tracking.md` `## Agent identity and ownership` for any authorized issue transfer and readback. Only then assign the remaining overlapping writes to the replacement. Preserve valid completed work; do not replay it or reset the diff.

If liveness, stability or ownership remains ambiguous, block only overlapping writes and shared-resource use. Continue independently owned disjoint work. Recovery stays in the same checkout. Compaction does not transfer a living writer's ownership; recover the same actor and reconcile its active process before continuing. A replacement never takes over merely because context was lost.

## Record the tested state

Tested-state, integration-evidence and completion-lifecycle rules cover execution and issue-only implementation. Design records sources and observed validation in its plan without execution phases, snapshots or implementation verdicts. Authority limits apply to every kind.

Before a gate, hold writes to its tested scope. Record the command, result, HEAD SHA, scoped paths, and a SHA-256 digest of a deterministic manifest of those paths and their file contents, including untracked files. Record the manifest method and observation time so a resumed agent can compare the same inputs. A commit SHA may replace the content digest only when the commit contains every tested change. A Git ref alone does not identify uncommitted contents.

Record explicit user commit authority and its scope once; a standing grant remains valid within that scope and does not require repeated approval. After successful declared boundary review, accepted fixes and required retests, the parent stages only owned paths and commits on the current branch with a Conventional Commit subject and no agent attribution. No task/subtask commit is implied. Under final-only review, intermediate phases remain uncommitted; a failed boundary remains uncommitted unless the user expressly authorizes a partial checkpoint. `alaa-codex-orchestrator` and `alaa-cc-orchestrator` `references/verification-and-gates.md` schedule the action. Without commit authority, the observed snapshot identifies evidence and the uncommitted tree remains a reported recovery risk.

## Reconcile evidence before running checks

Record each required outcome and its evidence at the level owner in `references/task-tracking.md` `## Acceptance and evidence by level`, retaining the tested identity above.

Before integration, resume or final validation, load /alaa-testing-strategy `references/100-test-execution.md` for execution evidence, aggregation and reuse; its `references/120-result-classification.md` decides whether a result is valid. Workflow reconciles those decisions with the current checkout and records which proof remains attributable. The runtime orchestrator owns independent acceptance and commissions missing or invalidated proof at its declared boundary.

## What still needs the user

This skill grants no commit, merge, push, tag, publication, deployment, installation, history-rewrite, or branch-deletion authority. Each requires explicit user authorization covering the action; a recorded standing grant counts within its scope. A requested implementation authorizes local edits and validation within scope; activation of this skill grants no additional effect.

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
4. **Apply only authorized integration.** Merge only after explicit authorization. Push, tag, publication, worktree removal, and branch deletion each remain separate actions under their own authority limits. Verify and report any action actually performed.

If authorization is absent, leave the worktree and base intact and report the verified local state. That is a complete outcome for work whose requested scope was local.

## What this file does not own

- Which tests run at which strength: `/alaa-testing-strategy`.
- Lane allocation and capacity: `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` for the active runtime; this file owns shared-file exclusivity and recovery.
- What is written into the plan, checkpoint, and handoff package: `references/context-continuity.md` and `references/artifact-lifecycle.md`.
