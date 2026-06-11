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

## Windows excluded port ranges

When Docker or a local server fails with an error like `ports are not available` or `bind: An attempt was made to access a socket in a way forbidden by its access permissions`, do not assume another process owns the port.

On Windows, first check both listeners and excluded TCP ranges:

- `Get-NetTCPConnection -LocalPort <port> -ErrorAction SilentlyContinue`
- `netsh interface ipv4 show excludedportrange protocol=tcp`

If the target port falls inside an excluded range, choose a host port outside the excluded ranges and update only the host-side binding. Keep the container port unchanged unless the application itself must listen on a different port.

## Git Bash and path conversion

Git Bash may rewrite slash-looking argument or environment values when invoking native Windows binaries. For Docker Compose and runtime scripts, route service-runtime env conversion issues to `$service-runtime-kit-governance`.

For one-off shell recovery, prefer native PowerShell. If Bash is required, consider `MSYS_NO_PATHCONV=1` or `MSYS2_ARG_CONV_EXCL=*` only for the affected command.

## Escalated commands

If a needed command fails because of sandbox permissions, rerun it with escalation and a concise task-specific justification. Do not request broad persistent prefixes for arbitrary scripting.

## Windows EPERM during frontend validation

Observed recurring pattern: on Windows, package validation can fail under the sandbox with `EPERM` while Vitest opens `.vite-temp/vitest.config.*.mjs` files or tsup/build cleanup unlinks package `dist` outputs such as `index.mjs` or `index.d.ts`.

Recovery sequence:

1. Treat the first `EPERM` as a runtime/permission failure, not evidence of a code regression.
2. Rerun the exact failed validation or build command once with `sandbox_permissions: "require_escalated"` and a task-specific justification.
3. Prefer the smallest gate that failed, such as `yarn workspace <pkg> test` or `yarn workspace <pkg> build`; if a multi-package loop failed, rerun affected packages serially or rerun the same loop elevated.
4. Keep the retry scoped to validation. Do not edit source, rewrite config, or delete `node_modules`, `.vite-temp`, or `dist` as the first fix.
5. If the exact escalated retry passes, record the runtime workaround and continue with normal validation.
6. If it still fails, then inspect for a real lock holder, antivirus/indexer interference, stale generated output, or a project script issue before proposing cleanup.
