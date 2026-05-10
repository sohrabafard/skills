# Windows Sandbox Recovery

## Pattern

When a read, search, or validation command fails because the Windows sandbox setup or refresh failed:

1. Keep the original task and target paths unchanged.
2. Retry only the failed or essential read/search.
3. Prefer a smaller serial command over another broad parallel command.
4. Use native PowerShell plus `rg`, `Get-Content -TotalCount`, `Select-Object`, or `Get-ChildItem` for read-only inspection.
5. Record the workaround briefly if it affects confidence or validation.

## Do not infer repo state from harness failure

A sandbox setup failure is not evidence that files disappeared, the repo changed, or the user made a mistake.

Confirm with a smaller command before changing assumptions.

## Parallel fallback

If a parallel read batch fails:

- rerun only the failed path or smallest useful subset
- avoid dumping full files as a recovery step
- keep line counts and excerpts bounded
- continue with the evidence gathered from successful lanes

## Escalation

Request escalation when the command is necessary and sandboxing prevents completion. Keep the justification tied to the user's task and the failed capability.
