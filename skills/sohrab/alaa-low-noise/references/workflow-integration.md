# Workflow Integration

Use this reference only when `$alaa-workflow` or delegated execution is active.

## Ownership rule

`$alaa-low-noise` owns output discipline.

`$alaa-workflow` owns:

- plan mode versus execution mode
- durable artifact families and naming
- resume and handoff continuity
- parent versus child lane ownership

If they overlap, follow `$alaa-workflow` for artifact structure and follow `$alaa-low-noise` for how much to print.

## Artifact routing

When workflow artifacts already exist:

- keep durable reasoning in the existing plan or state artifacts
- do not create alternate note files that duplicate the same information
- keep long logs in repo-local paths already used by the repository or workflow run

When workflow is not active but a bulky artifact is still useful:

- prefer existing repo conventions first
- otherwise use a small repo-local path such as `artifacts/` or `reports/`

## Delegated lanes

In delegated work:

- the parent agent owns the concise synthesis
- child lanes should avoid raw-log chatter in the parent thread
- discovery lanes should return counts, tight findings, or artifact paths
- writer lanes should keep outputs scoped to their owned surfaces

## Good pairing pattern

- `$alaa-workflow` decides whether the task needs durable plan or state artifacts
- `$alaa-low-noise` keeps discovery, validation, and reporting compact
- domain skills still own the actual code, runtime, or architecture decisions
