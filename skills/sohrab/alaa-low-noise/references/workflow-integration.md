# Workflow Integration

Read this file only when `$alaa-workflow` / `/alaa-workflow` or delegated execution is active.

## Ownership rule

`$alaa-low-noise` / `/alaa-low-noise` owns context economy and output discipline: what enters the context window, and how much is printed.

`$alaa-workflow` / `/alaa-workflow` owns:

- plan mode versus execution mode
- durable artifact families and naming
- resume and handoff continuity
- parent versus child lane ownership

Where they overlap, follow the workflow skill for artifact structure and this skill for how much is read and how much is printed. This skill never decides phases, plans, or state layout.

## Artifact routing

When workflow artifacts already exist, keep durable reasoning in the existing plan or state artifacts, do not create alternate note files duplicating the same information, and keep long logs in repo-local paths the repository or workflow run already uses.

When workflow is not active but a bulky artifact is still useful, prefer existing repository conventions first, and otherwise a small repo-local path such as `artifacts/` or `reports/`.

## Delegated lanes

Delegation is a context-economy instrument before it is a parallelism instrument: a subagent's discovery burns its own context, and only its return lands in the parent. That makes the return contract the thing that matters.

- The parent owns the concise synthesis and the user-facing report.
- Children return findings, counts, verdicts, or artifact paths — never transcripts, full file contents, full diffs, or raw logs.
- Discovery lanes report what they concluded and where the evidence lives, not what they read to get there.
- Writer lanes keep outputs scoped to their owned surfaces and report changed paths rather than diffs.
- Give each child an explicit return shape and a length bound in its dispatch; an unbounded child return is the most common way a parent's context is flooded.
- Do not spawn a lane whose only product is a summary the parent could have obtained in a couple of bounded reads.

Runtime note: Claude Code fans out readily and needs the cap stated, while Codex does not fan out unprompted and needs delegation authorized positively. The return contract above is identical in both.

## Good pairing pattern

`$alaa-workflow` / `/alaa-workflow` decides whether the task needs durable plan or state artifacts; this skill keeps discovery, validation, and reporting compact; domain skills still own the code, runtime, and architecture decisions.

## Caveats

Delegation polarity differs by model family and changes between generations — see `references/model-output-profiles.md` before assuming a cap or an authorization is the right correction. The artifact paths named here (`artifacts/`, `reports/`) are fallbacks only; repository conventions and any active workflow artifact family outrank them.
