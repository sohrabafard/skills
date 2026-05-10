# Command And Path Discipline

## Command length

For `CreateProcessAsUserW failed: 206` or similar command-length errors:

- split the operation into smaller batches
- store long target lists in a repo-local artifact only when that artifact is useful and allowed
- prefer `rg --files` plus focused follow-up reads instead of one giant command
- avoid changing repo files merely to shorten a command

## PowerShell first on Windows

Use PowerShell-native paths and commands for Windows-local inspection unless the task specifically requires Bash.

Prefer:

- `Get-ChildItem -LiteralPath`
- `Get-Content -LiteralPath -TotalCount`
- `Select-String`
- `Resolve-Path`

Use `rg` for search when available.

## Git Bash and path conversion

Git Bash may rewrite slash-looking argument or environment values when invoking native Windows binaries. For Docker Compose and runtime scripts, route service-runtime env conversion issues to `$service-runtime-kit-governance`.

For one-off shell recovery, prefer native PowerShell. If Bash is required, consider `MSYS_NO_PATHCONV=1` or `MSYS2_ARG_CONV_EXCL=*` only for the affected command.

## Escalated commands

If a needed command fails because of sandbox permissions, rerun it with escalation and a concise task-specific justification. Do not request broad persistent prefixes for arbitrary scripting.
