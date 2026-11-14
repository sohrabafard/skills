# Workflow Integration

Read this file only when `/alaa-workflow` or delegated execution is active.

## Ownership rule

`/alaa-low-noise` owns context input and printed output.

`/alaa-workflow` owns:

- plan mode versus execution mode
- durable artifact families and naming
- resume and handoff continuity
- parent versus child lane ownership

Where they overlap, follow `/alaa-workflow` for artifact structure. Follow `/alaa-low-noise` for how much is read and printed. This skill never decides phases, plans, or state layout.

## Artifact routing

When workflow has admitted durable state:

- Keep durable reasoning in its existing workflow owner. Use the canonical plan reference, including
  a Beads address for a Beads-native plan.
- Do not duplicate that information in alternate notes.
- Keep long logs in repo-local paths already used by the repository or workflow run.

When workflow is inactive but a bulky artifact is useful, prefer existing repository conventions. Otherwise, prefer a small repo-local path such as `artifacts/` or `reports/`.

## Delegated lanes

When delegating, prioritize keeping discovery out of the parent context over parallelism.
The return enters the parent's context.

- The parent owns the concise synthesis and the user-facing report.
- Children return findings, counts, verdicts, or artifact paths. Children never return transcripts, full file contents, full diffs, or raw logs.
- Discovery lanes report conclusions and evidence locations, not what they read.
- Writer lanes keep outputs within their owned surfaces. They report changed paths, not diffs.
- Give each child an explicit return shape and length bound in its dispatch. Unbounded returns most often flood the parent's context.
- Do not spawn a summary-only lane when the parent could obtain that summary in a couple of bounded reads.

Route runtime-specific delegation authorization and capability through `/alaa-prompting-guide`. Both runtimes share the return contract above.

## Caveats

- Delegation polarity differs by model family and generation. Before assuming a cap or authorization is the right correction, read `alaa-prompting-guide references/06-invocation-and-composition.md`; it owns the polarity rule.
- The `artifacts/` and `reports/` paths are fallbacks only. Repository conventions and any active workflow artifact family take precedence.
