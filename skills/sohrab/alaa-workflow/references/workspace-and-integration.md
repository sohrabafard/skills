# Workspace Evidence and Integration

`references/context-continuity.md` owns artifact contents. This file owns workspace identity, Git authority, and the four completion states. A commit is one durable checkpoint; a scoped worktree snapshot identifies evidence when committing is not authorized.

## Before the first write

1. **Record the base and checkout.** Capture the current branch, HEAD SHA, and worktree path. If integration is requested, also capture the target branch and its base SHA. A resumed agent needs those identities to determine what changed.
2. **Map existing changes.** Treat unowned modified and untracked paths as user or other-lane work. Preserve them and continue on disjoint paths. Resolve overlapping ownership before editing the same file; never stash, stage, overwrite, or commit another owner's change.
3. **Choose an isolated surface when needed.** Use the current checkout when its ownership is clear. Create a branch or worktree for concurrent writes or integration when it materially reduces collision risk, and record the choice. Branch creation never grants commit or merge authority.

## Record the tested state

Before a gate, hold writes to its tested scope. Record the command, result, HEAD SHA, scoped paths, and a SHA-256 digest of a deterministic manifest of those paths and their file contents, including untracked files. Record the manifest method and observation time so a resumed agent can compare the same inputs. A commit SHA may replace the content digest only when the commit contains every tested change. A Git ref alone does not identify uncommitted contents.

When the user explicitly authorizes commits, the parent stages only owned paths and commits after the focused check; lanes never interleave commits into one branch. Use a Conventional Commit subject and no agent attribution. A failed phase remains uncommitted unless the user expressly authorizes a partial checkpoint. When no commit is authorized, the observed snapshot is the phase's evidence identity and the uncommitted tree remains a reported recovery risk.

Do not repeat a passing gate on an unchanged tested snapshot. If a later edit affects its inputs, run that gate again on the new snapshot. `/alaa-testing-strategy` owns any stricter repository proof tier.

## What still needs the user

This skill grants no commit, merge, push, tag, publication, deployment, installation, history-rewrite, or branch-deletion authority. Each requires explicit user authorization for the concrete action. A requested implementation authorizes local edits and validation within scope; activation of this skill grants no additional effect.

## The completion lifecycle

Four states describe what a run has proven, and every run reports all four. Each carries its own verdict — proven, not proven with the blocker named, or not requested — because one word for "done" reads the same over a change that is committed and reviewed as over one that is merely written.

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

- Which tests run at which moment, and when a result may be cited instead of re-run: `/alaa-testing-strategy` (`$alaa-testing-strategy`).
- Which agent may write to which files inside one goal: the orchestrator skills, `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex).
- What is written into the plan, checkpoint, and handoff package: `references/context-continuity.md` and `references/artifact-lifecycle.md`.
