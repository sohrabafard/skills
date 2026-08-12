# Workspace, Commits, and Integration

`references/context-continuity.md` owns what gets written into files; this file owns what gets written into Git, because a commit is the only checkpoint that survives a crashed session, a lost conversation, and a wrong edit at the same time.

The whole protocol exists to keep three things true at once: the user's base branch is never the surface being experimented on, every intermediate state is recoverable, and nothing leaves the local repository without the user saying so.

## Before the first write

1. **Record the base.** Capture the current branch name and its commit SHA in the plan header. Everything later is measured against that pair, and a resumed agent that does not know the base cannot compute what this run changed.
2. **Refuse to start on a dirty tree.** Uncommitted changes that this run did not make belong to the user or to another agent. Stop, name the files, and ask. Never stash them, never commit them onto the work branch, and never write on top of them — a mixed diff cannot be reviewed, reverted, or attributed afterwards.
3. **Create the work branch.** Branch from the base and never commit on the base itself. Use the repository's own branch-naming convention when it has one; otherwise `agent/<plan-stem>`. Record the branch in the plan header and the checkpoint.
4. **Decide the tree shape.** One work branch in the existing tree is the default. Add a separate worktree only when the user asks for one, or when two write lanes must run at once and cannot share a tree. Record the worktree path in the plan header when one exists, because every path in every later dispatch is relative to it.

## Commit at the subtask boundary

**One commit per completed subtask or phase, never a single commit at the end.** A run that commits once has no recoverable intermediate state, so a defect found late costs a bisect through work that was never separated. A run that commits every file save has no readable history, which costs the same review twice.

A subtask is committable once its focused-tier check has passed. Commit the change that satisfied it — one commit can close several subtasks, and a subtask found already done produces no commit at all because there is nothing to record. What never happens is a finished change left uncommitted while the next one starts on top of it. `SKILL.md` owns when a plan box may be ticked.

- **The parent commits; lanes do not.** Concurrent lanes committing into one branch interleave into a history that describes no single state. Lanes report changed paths; the parent stages the subtask's owned paths and writes the commit. In worktree-per-lane mode each lane owns its own worktree and its own branch, and the parent still owns every merge.
- **Nothing is committed while a verification pass is in flight.** From dispatch until the pass returns, the tree it is measuring must not move: a commit landing mid-pass silently invalidates every step taken before it and buys a re-run of that gate. Hold the commit until the pass returns, or give the pass its own worktree at the commit under test.
- **Stage the subtask's owned paths only.** Never `git add -A` on a tree where another lane is writing.
- **Conventional Commits, imperative subject, no `Co-Authored-By` trailer.** The subject names the subtask. The body names the acceptance criterion it satisfies and the validation observed, in one line each.
- **A failed subtask is not committed.** Record the blocker in the checkpoint and leave the tree at the last good commit, or commit the partial work on its own branch and say so in the plan.

## What still needs the user

Committing locally on a work branch is the only Git action this protocol authorizes on its own. Every one of these is asked first, each time: push, tag, force-push, history rewrite, branch deletion, merge into the base branch, or any action against a remote. Repository instructions may narrow this further and never widen it.

## The completion lifecycle

Four states describe what a run has proven, and every run reports all four. Each carries its own verdict — proven, not proven with the blocker named, or not requested — because one word for "done" reads the same over a change that is committed and reviewed as over one that is merely written.

| State | Proven when |
|---|---|
| `IMPLEMENTED` | the change's focused-tier proof passed, and the completed change sits in a durable local commit wherever this run holds commit authority. A run that holds none proves the state on the check alone and names the uncommitted tree as a residual risk |
| `MERGE_CANDIDATE` | every integration gate the change affects passed, as the run's own pipeline defines them, and the independent review the change required returned its verdict |
| `RELEASE_CANDIDATE` | the user asked for a release, and the release prerequisites the target repository itself defines passed |
| `PUBLISHED` | an authorized immutable publication landed — a push, a tag, a released artifact — and its evidence was observed on the remote rather than inferred from a command that exited zero |

**A blocker in a later state never unproves an earlier one.** A failed release prerequisite leaves `IMPLEMENTED` and `MERGE_CANDIDATE` exactly as they were proven. Collapsing the ladder to its lowest failure hides finished work and buys it a second time, and that is the whole reason a run reports four verdicts instead of one. Only evidence against a state's own condition moves that state — a commit that is gone, a gate that now fails.

**A release is requested, never inferred.** An instruction to implement, fix, or merge authorizes no release step. With no explicit release request from the user, `RELEASE_CANDIDATE` and `PUBLISHED` report not requested, which is a complete outcome and not a gap to close.

**A state is a report, never an authority.** *What still needs the user* above governs every action these states describe, unchanged: `IMPLEMENTED` records the local commit this protocol already authorizes, while the merge, push, and tag behind `MERGE_CANDIDATE` and `PUBLISHED` each still need the user at the moment they happen. Reaching one state never licenses the action that would reach the next.

## The integration handshake

Run this once, after every phase is complete, every gate has passed, and documentation has landed.

1. **Bring the base in first, on the work branch.** If the base moved while this run was working — another agent, another session, the user — merge or rebase the base into the work branch and resolve the conflicts there. Conflicts are resolved on the branch that is allowed to be wrong, never on the base.
2. **Resolve conflicts against the plan, not against the diff.** The plan's decisions and acceptance criteria are the tie-break. A conflict whose correct resolution is not decidable from the plan is a decision for the user, not a merge choice.
3. **Re-run the exhaustive tier whenever step 1 changed the tree, conflict or no conflict.** A clean merge is the case that gets missed: no conflict means no edit was needed to combine the two sides, not that the combination was observed. `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns the invariant — the exhaustive tier runs on the tree that will land — and the rule that this result is never cited from an earlier run. When the base has not moved since that run, its evidence still describes this tree and nothing is owed.
4. **Present, then wait.** Give the user the work branch, the commit list, the diffstat against the base, the gate verdicts, and the residual risks. Ask for confirmation. Do not merge while waiting.
5. **On confirmation, merge into the base locally.** Merge the work branch into the base with a merge commit, so the run stays visible as a unit. Do not push. Do not delete the work branch without asking — it is the only cheap way back.
6. **Then, and only in worktree mode, detach.** Remove the worktree and prune the administrative entry after the merge is confirmed clean and nothing in it is unmerged. Verify the removal, and report the branch that still holds the work.

If the user declines, or does not answer, the run ends with the work branch intact and the base untouched. That is a complete, reportable outcome, not a failure.

## What this file does not own

- Which tests run at which moment, and when a result may be cited instead of re-run: `/alaa-testing-strategy` (`$alaa-testing-strategy`).
- Which agent may write to which files inside one goal: the orchestrator skills, `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex).
- What is written into the plan, checkpoint, and handoff package: `references/context-continuity.md` and `references/artifact-lifecycle.md`.
