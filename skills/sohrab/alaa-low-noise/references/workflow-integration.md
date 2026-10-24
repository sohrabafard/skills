# Workflow Integration

## Introduction

This reference keeps context economy and output discipline compatible with workflow ownership. Delegation serves context economy before parallelism. Discovery uses the subagent's context. Only its return enters the parent's context, so the return contract matters.

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

When workflow artifacts exist:

- Keep durable reasoning in the existing plan or state artifacts.
- Do not duplicate that information in alternate notes.
- Keep long logs in repo-local paths already used by the repository or workflow run.

When workflow is inactive but a bulky artifact is useful, prefer existing repository conventions. Otherwise, prefer a small repo-local path such as `artifacts/` or `reports/`.

## Delegated lanes

- The parent owns the concise synthesis and the user-facing report.
- Children return findings, counts, verdicts, or artifact paths. Children never return transcripts, full file contents, full diffs, or raw logs.
- Discovery lanes report conclusions and evidence locations, not what they read.
- Writer lanes keep outputs within their owned surfaces. They report changed paths, not diffs.
- Give each child an explicit return shape and length bound in its dispatch. Unbounded returns most often flood the parent's context.
- Do not spawn a summary-only lane when the parent could obtain that summary in a couple of bounded reads.

Route runtime-specific delegation authorization and capability through `/alaa-prompting-guide`. Both runtimes share the return contract above.

## Good pairing pattern

`/alaa-workflow` decides whether durable plan or state artifacts are needed. This skill keeps discovery, validation, and reporting compact. Domain skills own code, runtime, and architecture decisions.

## Caveats

- Delegation polarity differs by model family and generation. Before assuming a cap or authorization is the right correction, read `references/model-output-profiles.md`.
- The `artifacts/` and `reports/` paths are fallbacks only. Repository conventions and any active workflow artifact family take precedence.
