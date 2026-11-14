# Independent instruction review of pack version 5.9.0: VERDICT: CHANGES-REQUESTED
## Findings to repair (use each replacement text exactly unless a file forces a difference; report every deviation)

1. major. Owner file step 7, and the `<commit>` field in both `references/delegation-prompts/90-completion/20-review-followup.md`.
   Why: a fix needed after the merge has no lane branch. Under a final boundary the lead merges and deletes the lane branch after the final review; a final-validation failure then goes through Gate economics to the existing implementer, and the fix template says "the same lane branch name", which is gone. The documenter branch has the same gap.
   Replace step 7's last sentence with: "A fix before the merge lands on the same lane branch. A fix after the merge, such as one the final validation requires, gets a new lane branch under step 1 and merges after the gate that required it accepts it."
   Template field: `<commit><the lane branch the fix lands on: the unmerged lane branch, or a new one after the merge> | <none: return the work uncommitted></commit>`.

2. major. The clause in step 8 that the lead removes a merged lane's separate worktree contradicts four places. The owner's global rule pre-authorizes that removal, so correct the authority text:
   - Owner file, the closing paragraph of the section: "The local-commit authority covers the lane commits, the lane merge, the lane-branch deletion and the removal of a merged lane's separate worktree." (keep the sentence that follows it)
   - Owner file, the exception sentence near line 59: "The one exception is the lane-branch merge, the lane-branch deletion and the removal of a merged lane's worktree under `## Lane branches and commits`."
   - Owner file, handshake step 4 near line 85: "Push, tag, publication, and any worktree removal or branch deletion outside `## Lane branches and commits` each remain separate actions under their own authority limits."
   - Stage F in both `references/verification-and-gates.md`: "Push, tag, branch deletion other than the lane-branch deletion, worktree removal other than a merged lane's worktree, and remote effects each require explicit authority."

3. major. Owner file step 5 (commit hooks in a shared checkout).
   Why: a pre-commit hook that stashes, re-stages, restores or rewrites the working tree can take another lane's uncommitted edits into a commit or lose them. The pathspec rule does not protect against this.
   Append to step 2: "Before lanes share the checkout, the lead inspects the repository's commit hooks. When a hook stashes, stages, restores or rewrites files outside the committed paths, the lead records isolation as required in the plan, so that step 3 gives each write lane its own worktree. A lane never bypasses a hook."

4. minor. Owner file step 1. Append: "The lead switches branches or merges only while no lane is live in that checkout. When the run stops before a merge, the lead switches back to the work branch once no lane is live, and reports the unmerged lane branch."

5. minor. Owner file step 5. Append: "For a rename or a deletion, the owned paths include the old path."

6. minor. Owner file step 6. Replace the last sentence with: "When a commit fails on the index lock, the lane waits and retries the same commit once. When the retry or any other commit fails, the lane leaves its work uncommitted and reports the command and the error."

7. minor. Both `references/verification-and-gates.md`, the documenter merge-timing sentence (about line 40): "created after that merge" can point at a phase merge. Replace with: "The documenter's lane branch is created after the last implementation merge. It merges after the Stage E documentation gate accepts it and before the Stage E final validation."

8. minor. Owner file step 8. Append: "This lane merge brings accepted work into the work branch. It is not the integration that `MERGE_CANDIDATE` qualifies."

9. minor. Both `references/delegation-prompts.md`, the read-back paragraph. Append: "For an implementation or fix dispatch, also confirm that `<task_controls>` records the admission predicates of the selected route." (If the template records the predicates in a different field, name that field.)

10. nit. `alaa-cc-orchestrator/references/delegation-prompts/30-implementation.md`, the new paragraph: Claude Code has no bug route. In the Claude Code file write "For a mechanical or bounded route".

11. nit. Both `assets/implementation-contract.md`, output item 3: write "each skill the dispatch or your stack binding required, under a condition that held, that you loaded late or not at all, with the reason."

## Accepted by the reviewer
No surviving sentence says a lane never commits or that the lead makes every commit; only read-only roles keep their ban. Decision 1 behaviours map to owner steps 1 to 10. The documenter coverage, the lead's commits landing on the checked-out lane branch, and path-mode checkout, reset and restore on owned paths only are accepted. Merge timing is stated once and agrees with the stages and Gate economics apart from finding 1. Push, tag, history rewrite, remote sync and any other merge still need explicit permission; no read-only role gained commit authority. The mechanical, bounded and bug predicate lists are unchanged and both runtimes behave the same. All seven new checker literals appear verbatim; nothing was weakened.

## Dispositions
The implementer lane applied all eleven findings with the reviewer's text. The confirmation pass returned APPROVED-WITH-NITS: all eleven confirmed, no new conflict among the appended sentences and the two gates files. Its one nit (a pointer from the final-boundary merge bullet to the post-merge fix rule) was applied by the parent in both runtimes; the gates passed after it and no reviewer re-read that one sentence.
