# Resource and Low-Priority Execution Policy

Resource controls have separate layers:

1. OS process priority (`BelowNormal` by default on Windows, `nice 10` on Unix).
2. Optional CPU affinity/count.
3. Tool/runtime concurrency (`GOMAXPROCS`, package parallelism, test workers, browser workers).
4. Timeout and one-heavy-command-at-a-time policy.

Lower priority does not limit parallelism. Configure both.

## Windows runner

Use the absolute script path from the installed skill:

```powershell
$runner = "<SKILL_ROOT>\scripts\Invoke-AlaaLowPriority.ps1"

& $runner `
  -Priority BelowNormal `
  -CpuCount 2 `
  -WorkingDirectory "D:\path\to\repo" `
  -Environment @{ GOMAXPROCS = "2" } `
  -TimeoutSeconds 900 `
  -FilePath "go" `
  -ArgumentList @("test", "-p", "1", "-parallel", "2", "-count=1", "./...")
```

The wrapper returns the child exit code and emits stdout/stderr. It sets the parent test process priority immediately after start; normal child processes inherit process scheduling constraints unless they explicitly override them.

Use `Idle` only for explicitly background-grade benchmark/fuzz/full-profile work. Do not use `Realtime` or `High`.

## Unix/WSL runner

```bash
"<SKILL_ROOT>/scripts/run-low-priority.sh" \
  --priority BelowNormal \
  --cpu-count 2 \
  -- go test -p 1 -parallel 2 -count=1 ./...
```

It uses `nice`; when `taskset` is available and `--cpu-count` is set, it also limits CPU affinity.

## Go verification profiles

Derive final commands from repository guidance. Common conservative examples:

```powershell
# Targeted unit package
-Environment @{ GOMAXPROCS = "2" }
-ArgumentList @("test", "-p", "1", "-parallel", "2", "-count=1", "./path/to/package")

# Race check: expensive, one package worker and one parallel test
-Environment @{ GOMAXPROCS = "2" }
-ArgumentList @("test", "-race", "-p", "1", "-parallel", "1", "-count=1", "./...")
```

`-p` controls package/build concurrency. `-parallel` controls tests using `t.Parallel` inside a test binary. `GOMAXPROCS` controls runtime CPU parallelism. They are not interchangeable.

## Node/Vue/Quasar

Use repository scripts exactly. Apply worker limits only when the test/build tool supports them and the repository does not define a conflicting policy. Examples vary by Vitest/Jest/Playwright/Vite and must not be guessed.

Do not run package installation merely because a command is missing. Report `ENVIRONMENT-BLOCKED`.

## PHP/Laravel

PHPUnit is commonly single-process unless a parallel runner is configured. Use repository commands and do not introduce ParaTest or process isolation during verification. Lower the OS priority for broad suites or static analysis when declared CPU-heavy.

## Browser QA

- Preserve explicit `--browser chromium`.
- Preserve configured user-data/profile paths.
- Reuse an existing declared dev server.
- Limit browser workers through the repository-supported mechanism only.
- Do not kill or reuse another worktree's server without explicit ownership.

## Artifacts

Each dispatch declares one artifact directory. Verifiers/profilers/browser QA may write only there plus unavoidable tool temp directories allowed by the sandbox. Unexpected tracked file changes contaminate the run.
