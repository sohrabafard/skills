# Workflow Integration

Read this file only when `/alaa-workflow` or delegated execution is active.

## Ownership rule

`SKILL.md` states the split: this skill owns context input and printed output, and `/alaa-workflow` owns durable planning and state. Within that state, workflow owns plan versus execution mode, durable artifact families and naming, resume and handoff continuity, and parent versus child lane ownership. Where they overlap, follow `/alaa-workflow` for artifact structure and this skill for how much is read and printed. This skill never decides phases, plans or state layout.

## Artifact routing

When workflow has admitted durable state:

- Keep durable reasoning in its existing workflow owner. Use the canonical plan reference, including
  a Beads address for a Beads-native plan.
- Do not duplicate that information in alternate notes.
- Keep long logs in repo-local paths already used by the repository or workflow run.

When workflow is inactive but a bulky artifact is useful, follow existing repository conventions. Without one, use a small repo-local path such as `artifacts/` or `reports/`; these are fallbacks only, and repository conventions and any active workflow artifact family take precedence.

## Delegated lanes

When delegating, keeping discovery out of the parent context takes priority over parallelism, because the return enters the parent's context.

- The parent owns the concise synthesis and the user-facing report.
- Children return findings, counts, verdicts or artifact paths. Children never return transcripts, full file contents, full diffs or raw logs.
- Discovery lanes report conclusions and evidence locations, not what they read.
- Writer lanes keep outputs within their owned surfaces and report changed paths, not diffs.
- Give each child an explicit return shape and length bound in its dispatch, because unbounded returns most often flood the parent's context.
- Do not spawn a summary-only lane when the parent could obtain that summary in a couple of bounded reads.

Both runtimes share this return contract. Route runtime-specific delegation authorization and capability through `/alaa-prompting-guide`. Delegation polarity differs by model family and generation: before assuming a cap or an authorization is the right correction, read `alaa-prompting-guide references/06-invocation-and-composition.md`, which owns the polarity rule.
