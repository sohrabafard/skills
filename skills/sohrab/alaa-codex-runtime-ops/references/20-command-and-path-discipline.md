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

## Shell syntax mismatch

Recurring Windows failure modes:

- PowerShell `ParserError` from complex regex, brace expansion, `awk`, or Bash quoting pasted into a PowerShell command.
- `The term 'NAME=value' is not recognized` when Bash-style environment assignment is run in PowerShell.
- Inline `python -c` commands fail because `\n`, quotes, or list literals were flattened into one PowerShell string.

Recovery sequence:

1. Do not retry the identical command string.
2. If the command is conceptually PowerShell-native, rewrite it using PowerShell syntax: `$env:NAME = 'value'`, `Get-Content`, `Select-String`, arrays, and explicit path lists instead of Bash brace expansion.
3. If the command is Bash-native, run it as Bash explicitly, for example `bash -lc 'cd /d/path && NAME=value command ...'`.
4. For inline Python on PowerShell, prefer a here-string assigned to `$code`, then `python -c $code`; set `$env:PYTHONIOENCODING = 'utf-8'` when transcript text may contain non-ASCII.
5. Keep the retry bounded to the failed command or smallest useful subset.

## Escalated commands

If a needed command fails because of sandbox permissions, rerun it with escalation and a concise task-specific justification. Do not request broad persistent prefixes for arbitrary scripting.

## Windows EPERM during frontend validation

Observed recurring pattern: on Windows, package validation can fail under the sandbox with `EPERM` while Vitest opens `.vite-temp/vitest.config.*.mjs` files or tsup/build cleanup unlinks package `dist` outputs such as `index.mjs` or `index.d.ts`.

Recovery sequence:

1. Treat the first `EPERM` as a runtime/permission failure, not evidence of a code regression.
2. Rerun the exact failed validation or build command once with `sandbox_permissions: "require_escalated"` and a task-specific justification.
3. Prefer the smallest gate that failed, such as `yarn test`, `yarn test:new`, `yarn build`, `yarn build:ssr`, `yarn workspace <pkg> test`, `yarn workspace <pkg> build`, or the exact Quasar build/dev command needed for app verification; if a multi-package loop failed, rerun affected packages serially or rerun the same loop elevated.
4. Keep the retry scoped to validation. Do not edit source, rewrite config, or delete `node_modules`, `.vite-temp`, or `dist` as the first fix.
5. If the exact escalated retry passes, record the runtime workaround and continue with normal validation.
6. If it still fails, then inspect for a real lock holder, antivirus/indexer interference, stale generated output, or a project script issue before proposing cleanup.

## Docker Desktop named-pipe permissions

On Windows, Docker commands may fail with `permission denied while trying to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`.

Recovery sequence:

1. Decide whether live Docker state is required for the user's task.
2. If it is required, rerun the exact Docker command with escalation and a concise justification.
3. If the task can proceed from source/config inspection, use that fallback and report that Docker runtime validation was blocked.
4. Do not treat the named-pipe permission error as evidence that containers, Compose files, or application code are broken.
5. If Docker access works after escalation, continue with the original validation path and keep any follow-up Docker reads scoped.
