# Workflow Integration

## Ownership rule

`/alaa-workflow` owns plan versus execution mode, durable artifact families and naming, resume and handoff continuity, and lane ownership. Follow it for artifact structure, and this skill for how much is read and printed. This skill never decides phases, plans or state layout.

## Artifact routing

- With admitted workflow state: keep durable reasoning in its workflow owner, and cite the canonical plan reference, which is a Beads address for a Beads-native plan. Duplicate nothing in alternate notes. Keep long logs in the repo-local paths that the repository or the workflow run already uses.
- With no active workflow: put a useful bulky artifact where the repository convention says. Without a convention, use a small repo-local path such as `artifacts/` or `reports/`.

## Delegated lanes

The return of a lane enters the parent's context. Keeping discovery out of the parent therefore takes priority over parallelism.

- Give each child an explicit return shape and a length bound in its dispatch: an unbounded return most often floods the parent's context.
- A child returns findings, counts, verdicts or artifact paths. It never returns a transcript, full file contents, a full diff or a raw log.
- A discovery lane reports conclusions and evidence locations, not what it read.
- A writer lane keeps its output inside its owned surfaces and reports changed paths, not diffs.
- The parent owns the concise synthesis and the user-facing report.
- Spawn no summary-only lane when the parent can get that summary in a couple of bounded reads.

Both runtimes share this return contract. Delegation polarity differs by model family and generation: before you assume that a cap or an authorization is the right correction, read `alaa-prompting-guide references/06-invocation-and-composition.md`. That skill also owns runtime-specific delegation authorization and capability.
