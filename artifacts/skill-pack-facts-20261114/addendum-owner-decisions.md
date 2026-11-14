# Addendum: owner decisions and evidence-settled open items (2026-11-14)

Later the same day than [the report](report.md). Beads issue: `alaa-odfbb`. It closes open items of that report and records the first live runs of the installed roles.

## Owner decisions, implemented at pack version 5.9.0

The pack owner answered the two open decisions.

1. **Lanes commit on a lane branch.** The owner chose lane commits and added that a separate worktree must not be forced: one implementer, or several implementers on files they do not share, work in the checkout the lead runs in, on one branch, and commit; the lead merges with `--no-ff` after acceptance; a fix lands on the same branch first. The owner accepted three conditions: commits by path only, a lane never changes what the shared checkout points at or holds, and a separate worktree only on overlapping files or when the plan requires isolation. `alaa-workflow references/workspace-and-integration.md` section "Lane branches and commits" owns the protocol; both orchestrators point to it and time the merge against the review boundary.
2. **The dispatch carries the admission predicates.** The lead writes the predicates it verified into the dispatch. A lane checks them against the task and reads the routing matrix only when none are recorded or one does not hold.

An evidence follow-up rides with them: the implementer report names the skills loaded before the first edit and each required skill loaded late or not at all.

The independent review found three major gaps before the change was committed, all repaired: a fix after the merge had no branch; removing a merged lane's worktree contradicted four authority sentences; and a commit hook that touches files outside the committed paths can take or lose another lane's work in a shared checkout, so the lead now inspects the hooks and records isolation when one does. Record: `lanes/review-5.9.0.md`. One consequence of a shared lane branch stays by design: an accepted lane cannot merge apart from a rejected one; the fix lands first and the branch merges whole.

## Open items settled by evidence

Executed by the newly installed roles, then reviewed.

- **Kubernetes patch pins.** The project's release channel markers settled the disagreement between the releases page and the repository tags. Each row leads with the marker's patch and dates the older value.
- **The caas capability matrix.** The row sits in a generated block; regenerated with the skill's own update command, and `summarize-openapi.sh --check` now exits `0`.
- **The input-normalization conformance harness.** The Go build disables VCS stamping itself. An independent run observed exit `0` with Python, TypeScript, PHP and Go each matching 290 of 290. The Go implementation is now proven on this host.
- **Six instruction-text items.** One term for the scheduling clause in its five carriers; approval before an install in the Octane drill and before a downloading package runner in the design-system references; a clause the security fast gate could not follow; a false claim about an IndexedDB example; a note that a cited upstream issue was unreachable.

Records: `lanes/L1-infra-open-items.md`, `lanes/L2-instruction-open-items.md`. The independent code review of the infrastructure repairs returned APPROVED-WITH-NITS; its minor finding (two "latest" values in one row) was repaired.

## Live runs of the installed roles

These were real repository tasks, not evaluations.

| Role | Task | First line | Notes |
|---|---|---|---|
| `alaa-implementer-infra` | three infrastructure repairs | `STATUS: COMPLETE` with the outcome | Full report contract. It loaded its surface owner skills after its edits, not before, and said so. |
| `alaa-implementer` | eight instruction-text items | `STATUS: COMPLETE` with the outcome | Applied six, left two with reasons, named files it did not own. |
| `alaa-implementer` | the 5.9.0 change | `STATUS: COMPLETE` with the outcome | Named the skills it loaded before the first edit. |

One run of one stack-bound role is a single observation. It showed the return header and report contract working, and one miss on the load-before-edit rule. The new report item makes that miss visible to the lead in every lane.

## Validation observed

On `main` after the 5.9.0 commit, each exited `0`: the four root checkers, the installer unittest, both orchestrators' render check, pack validator, grants and contracts checkers, the three `alaa-prompting-guide` checkers, the execution-contract checker, the constitution template check and the memory checksum. The Claude Code installer updated 12 files and the Codex installer 15 of 37; a final Claude Code dry run reported 34 unchanged.

## Still open

- **Workflow-tool effort.** The public Claude Code documentation names no effort option on a Workflow `agent()` call.
- **The Kubernetes authoring floor** of 1.34 covers an end-of-life minor; its owner decides.
- **Domain and policy questions** from the report's list that no file or history settles: the keyset-pagination measurement figures; the throttle-hint wait across three provider skills; "below the floor" in the Laravel upgrade triage; the RATIFY word in the constitution workflow (history shows it was never a mode); the PHPantom absolute path that a test asserts; the GitLab parent guides that act as second routers; the IndexedDB threshold policies; the Arvan object-storage default prompt; object keys as secrets in the MinIO skill; a HAProxy source row whose content a past commit removed.
- **`alaa-trust-gateway-auth`**: three reported items, skipped while another session edits that skill.
- **Lua.** No Lua runtime is installed on this host, so the Lua implementation in `alaa-crockford-base32-codecs` stays unproven. Installing one needs the owner's approval.
- **Behaviour under the new commit protocol** has not been observed: the lanes above ran on the previous rule.

No push. No tag.

## Patch 5.9.1, same day

A last check of the commit protocol found two gaps and the release was patched before this record closed.

- **Returned work had no committer.** A lane may return its work uncommitted (no grant, or a failed commit). The lead now commits that work by path on the lane branch when the lane's focused checks passed, and first resolves the cause when the lane's commit failed.
- **Codex cannot write `.git` from its sandbox.** The official Codex page on sandboxing and approvals, read 2026-11-14, lists `.git` among the paths that stay read-only inside a writable root in `workspace-write` mode. The page does not say how `git commit` is handled, so the orchestrator states the consequence as an inference. In Codex the lead records the lane branch, grants no commit authority unless the sandbox allows the write, and commits returned work through the host's approval path. `alaa-prompting-guide references/11-codex-runtime-features.md` holds the fact.
- **Another writer in the checkout.** During this engagement another session committed in the same checkout. Switching that checkout's branch would have put its commits on the lane branch. The lead now checks for new commits since the recorded HEAD and for unowned files that change while it observes them; when it finds one it records isolation and keeps the checkout's branch.
- Both routing matrices say a session started before a role was installed "may not" have it: this session received the four roles without a restart.

The instruction reviewer returned CHANGES-REQUESTED on the first draft of the patch (two major: a sentence that contradicted its neighbour, and no path for a Codex lead under the same sandbox), then APPROVED-WITH-NITS after the repairs; its last wording nit was applied by the parent and not re-read. A search of the whole pack found no other sentence that states the old commit rule. Every gate exits `0` on the patched tree.
