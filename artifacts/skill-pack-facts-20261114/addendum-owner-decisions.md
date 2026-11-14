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
- **Lua.** Closed later the same day; see the last section of this file.
- **Behaviour under the new commit protocol** was observed once, in the last section of this file; shared-checkout concurrency, a rejected lane and the Codex path remain unobserved. The laravel, frontend and go roles have not run: this repository holds no real task for them, and an invented one would be the evaluation the pack owner excludes.

No push. No tag.

## Patch 5.9.1, same day

A last check of the commit protocol found two gaps and the release was patched before this record closed.

- **Returned work had no committer.** A lane may return its work uncommitted (no grant, or a failed commit). The lead now commits that work by path on the lane branch when the lane's focused checks passed, and first resolves the cause when the lane's commit failed.
- **Codex cannot write `.git` from its sandbox.** The official Codex page on sandboxing and approvals, read 2026-11-14, lists `.git` among the paths that stay read-only inside a writable root in `workspace-write` mode. The page does not say how `git commit` is handled, so the orchestrator states the consequence as an inference. In Codex the lead records the lane branch, grants no commit authority unless the sandbox allows the write, and commits returned work through the host's approval path. `alaa-prompting-guide references/11-codex-runtime-features.md` holds the fact.
- **Another writer in the checkout.** During this engagement another session committed in the same checkout. Switching that checkout's branch would have put its commits on the lane branch. The lead now checks for new commits since the recorded HEAD and for unowned files that change while it observes them; when it finds one it records isolation and keeps the checkout's branch.
- Both routing matrices say a session started before a role was installed "may not" have it: this session received the four roles without a restart.

The instruction reviewer returned CHANGES-REQUESTED on the first draft of the patch (two major: a sentence that contradicted its neighbour, and no path for a Codex lead under the same sandbox), then APPROVED-WITH-NITS after the repairs; its last wording nit was applied by the parent and not re-read. A search of the whole pack found no other sentence that states the old commit rule. Every gate exits `0` on the patched tree.

## First run of the lane-branch commit protocol, same day

The protocol of pack version 5.9.1 was then used once on real work (Beads issue `alaa-szivq`): clearing four ShellCheck findings in the input-normalization conformance harness, findings that an earlier lane had reported and left.

| Step of the protocol | Observed |
|---|---|
| The lead inspects hooks and other writers, records HEAD, creates the lane branch and switches the checkout | No commit hook, no other writer, HEAD `38dc9e0d`, branch `lane/normalization-harness-shellcheck` |
| The dispatch names the branch and carries the verified admission predicates | Yes |
| The lane loads its surface owner skill before the first edit | Yes (`/alaa-bash-shell`); it said it did not load the skill of the harness itself |
| The lane commits its owned path by path when its focused checks pass | One commit, `8ac5e7bf`, one path, a Conventional Commit subject, no attribution; the checkout was left on the branch and clean |
| The lane report names the commit and the branch | Yes |
| Independent review before the merge | `alaa-reviewer`: APPROVED-WITH-NITS; it ran ShellCheck (exit 0) and the harness (exit 0, four runtimes at 290 of 290) |
| The lead switches back while no lane is live, merges with `--no-ff` and deletes the branch | Merge commit `b84e60ed`; branch deleted; every gate exits 0 on `main` |

The role was `alaa-implementer-infra`, requested opus/medium. One nit from the review could not be applied to the lane's commit without rewriting history, so the merge message carries it: a failed resolution of the script's own directory now stops the script at once.

This is one run of one role with one lane. It shows that the protocol can be followed as written in Claude Code. It does not show two lanes sharing a checkout, a rejected lane, a fix on the same branch, or the Codex path.

## Second run: two lanes in one checkout, and a fix before the merge

A second real task (Beads issue `alaa-t2qxm`) exercised the parts the first run did not. Five version and link checkers sent a User-Agent that named the pack or called the client a skill tool; a request to an outside service must not carry the owner's project identity.

- **Two lanes, one checkout, one branch.** Two `alaa-implementer` lanes (requested opus/medium) ran at the same time on `lane/generic-client-name` with files they did not share. Each saw the other's modified files in the working tree, left them alone, and committed only its own paths by path: `f77311e4` (one file) and `fe957a27` (two files). Neither met the index lock.
- **Review, then a fix on the same branch.** `alaa-reviewer` returned APPROVED-WITH-NITS and found two more checkers of the same kind. The lead committed that fix on the same lane branch (`459a9ee2`, files no lane owned) before the merge.
- **Merge.** The lead switched back while no lane was live and merged with `--no-ff` (`2ba9ef0f`), then deleted the branch. Every gate exits `0` on `main`.

Still unobserved: a lane that hits the index lock, a rejected lane, a lane in a separate worktree, and the Codex path.

One lane loaded no skill before its edit and said why (two literal swaps); the report item made that visible.

## Scratch cleanup

The two files of transcript excerpts and one intermediate file that held hand-back openings were removed from the session scratchpad after the evidence summary was archived. They were throwaway output of this engagement and can be rebuilt by rerunning the extractors, which remain with their aggregate counts.

## Owner answers of the same day, and what they closed

The pack owner answered three questions.

- **Lua.** The owner installed Lua 5.4.8 on the host. The Crockford codec conformance harness then compared four of four runtimes (PHP 8.5.4, Node 26.12.1, the shell implementation and Lua 5.4.8) over 109 cases with no disagreement and exited `0`. The Lua implementation is proven on this host; the item under "Still open" above is closed.
- **Three low-risk domain repairs** (Beads issue `alaa-2xe14`), run under the lane-branch protocol: the constitution workflow reference names only modes that exist; the HAProxy source row says that a past commit removed the content it described (the file has no historical table, so the row stays and its cell carries the note); every site that quotes the keyset-pagination buffer measurements carries "not re-measured as of 2026-11-14", with no number changed. The lane returned `STATUS: INCOMPLETE` because one site sat outside its scope; the lead labelled it on the same branch. The instruction review returned APPROVED-WITH-NITS and its nit landed before the merge (`a19f3776`).
- **Push.** The owner authorized pushing `main` to `origin`.

The other domain and policy questions stay with the owner: the throttle-hint wait across three provider skills, the IndexedDB threshold policies, the Kubernetes authoring floor, "below the floor" in the Laravel upgrade triage, the PHPantom absolute path, the GitLab parent guides, the Arvan object-storage default prompt, object keys as secrets in the MinIO skill, and three items in `alaa-trust-gateway-auth`.

## The trust-boundary skill, after the parallel session went idle

Beads issue `alaa-2y7li`. The parallel session's six commits to `alaa-trust-gateway-auth` and `alaa-services-contract` had been pushed without a review by this engagement, and three wording-pass items in the trust-boundary skill had been deferred while that session was active. Both were handled once it had been idle for hours.

- **Review of the parallel session's commits.** The instruction review found two major defects in already-published text: two sentences of `references/40-downstream-normalization.md` could be read as fail-open. One read as if a body field may override trusted tenant context on WA; the other as if a malformed trusted `X-Project-Id` may fall back to the client envelope. The owner file of that rule says the opposite. Both now state that a body or envelope value never replaces a present trusted header and that a malformed one never falls back.
- **The deferred items.** An empty or blank `X-Access` is reported as `AUTH_ACCESS_HEADER_MISSING` in the case text, the router row and the checker script, as the skill's own deny-code table states; the script's unit test passes. The "four layers" sentence no longer states a count that its three-row table contradicts. The dangling "that positive-integer parser" names what it means.
- **Process.** One lane on a lane branch committed by path; the review returned CHANGES-REQUESTED, the lane applied twelve repairs on the same branch, the confirmation returned APPROVED-WITH-NITS, its last clause landed before the merge (`6629b88b`). Record: `lanes/review-trust-gateway.md`.
- **Left for the owner, in `alaa-services-contract`:** a router row states a who-may-set rule that the trust-boundary skill owns, and two references restate the optional-bearer rule. They agree with their owner today.
- **Not verified:** the contract values themselves against the gateway, wa and client repositories.

These commits are local. The owner's push authorization covered the state at that time; pushing these needs the owner's word again.
