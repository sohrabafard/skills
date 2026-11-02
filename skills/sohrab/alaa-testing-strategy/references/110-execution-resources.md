# Execution Resources

Read before CPU-heavy checks, dependency-container setup or comparative timing. This policy applies to direct work and either runtime; repository-specific constraints remain binding.

Resource controls have separate layers:

1. OS process priority (`BelowNormal` by default on Windows, `nice 10` on Unix).
2. Optional CPU affinity/count.
3. Tool/runtime concurrency (`GOMAXPROCS`, package parallelism, test workers, browser workers).
4. Timeout and one-heavy-command-at-a-time policy.

Lower priority does not limit parallelism. Configure both.

## Windows runner

Resolve the absolute script path from this testing-strategy skill; do not install or update anything automatically:

```powershell
$runner = "<TESTING_SKILL_ROOT>\scripts\Invoke-AlaaLowPriority.ps1"

& $runner `
  -Priority BelowNormal `
  -CpuCount 2 `
  -WorkingDirectory "<REPOSITORY_ROOT>" `
  -Environment @{ GOMAXPROCS = "2" } `
  -TimeoutSeconds 900 `
  -FilePath "go" `
  -ArgumentList @("test", "-p", "1", "-parallel", "2", "-count=1", "./...")
```

The wrapper returns the child exit code and emits stdout/stderr. It sets the parent test process priority immediately after start; normal child processes inherit process scheduling constraints unless they explicitly override them.

Use `Idle` only for explicitly background-grade benchmark/fuzz/full-profile work. Do not use `Realtime` or `High`.

## Unix/WSL runner

```bash
bash "<TESTING_SKILL_ROOT>/scripts/run-low-priority.sh" \
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

Test-result caching is separate from build caching. Reuse test results only while the four validity conditions in `SKILL.md` hold. When a condition changes or a check requires fresh proof, bypass result reuse for its selected packages or topics, including affected-tier checks against external dependency state (Go: `-count=1`); retain the build cache. The exhaustive tier runs once, fresh, on the final candidate; `./...` is exhaustive-only, and `-count=1` may be used at any tier that needs a fresh result.

## Node/Vue/Quasar

Use repository scripts exactly. Apply worker limits only when the test/build tool supports them and the repository does not define a conflicting policy. Examples vary by Vitest/Jest/Playwright/Vite and must not be guessed.

Do not run package installation merely because a command is missing. Report `ENVIRONMENT-BLOCKED`.

## PHP/Laravel

PHPUnit is commonly single-process unless a parallel runner is configured. Use repository commands and do not introduce ParaTest or process isolation during verification. Lower the OS priority for broad suites or static analysis when declared CPU-heavy.

## Service safety and reuse

- Do not kill unrelated services, dev servers, containers, or processes.
- Do not start duplicate services when a reusable declared service already exists.

## Browser QA

- Preserve explicit `--browser chromium`.
- Preserve configured user-data/profile paths.
- Limit browser workers through the repository-supported mechanism only.
- Do not kill or reuse another worktree's server without explicit ownership.

## Artifacts

Declare one allowed artifact directory in the execution record. Write run artifacts only there plus unavoidable tool temp directories allowed by the sandbox. Unexpected tracked file changes contaminate the run.

## Host and container budgets

Run only one CPU-heavy verification or profiling command at a time per host in this workflow. A gate's supported internal parallel mode counts as that one command. Priority alone is not a CPU limit. Record effective host capacity, including container/VM/cgroup quotas, affinity restrictions and reserved capacity; an unavailable capacity observation is unknown, never unlimited.

Before starting test or dependency containers, allocate explicit CPU budgets across every concurrent container and host worker. Their simultaneous allocations must fit effective host capacity with the declared reserve. Set container `--cpus` limits below the host logical CPU count and within that effective budget; align each gate's worker/package/runtime counts with its container allocation. Record dependency-container allocations as well as the test-container allocation; limiting only the test container leaves an unbudgeted dependency load. Defer work when a safe concurrent budget cannot be established.

For a CI-image gate, record the image reference, read-only source mount, complete copy into the container filesystem (including required Git metadata), setup/services and CPU/worker limits. Verify copied inputs and expected selection before accepting coverage. The container CPU limit replaces the host low-priority wrapper for that run. Share one container and one CI setup per pass under `90-test-economy.md`.

If Docker, the image, mount, copy, setup or required service blocks a container run, record `ENVIRONMENT-BLOCKED` and make one host fallback under the low-priority wrapper when repository policy and authority permit. Record why, the changed environment and any lost coverage; never call it container proof. Under Codex, invoke /alaa-codex-runtime-ops for Docker-access permission failures within its declared runtime scope before fallback. Installation, pulling an undeclared image, permission changes or starting an unowned service require separate authority.

## On a Windows host, a long process-heavy gate runs in the CI job image

When the host is Windows and an affected- or exhaustive-tier gate is long (its last host run, or the repository's documentation, exceeds ten minutes) and process-heavy — shell suites, or many short CLI invocations — run it in a container of the Linux image the repository's CI runs that gate in, as named by its CI configuration or documentation. Process creation under Git Bash or MSYS makes such a gate several times slower, and the CI image's tool variants (for example BusyBox instead of GNU utilities) expose defects a Windows run hides.

- Mount the worktree read-only and run the gate on a copy inside the container's filesystem that includes the git metadata the gate reads: a bind mount is slow, and a writable one lets the gate change the tree.
- Run the CI job's own setup steps and services once per pass, and run every gate of that pass in the same container.
- Use the gate's own parallel mode when it has one, otherwise run it sequentially; never parallelize its steps yourself.
- Report the image reference and that the result is container evidence. Host and container are different environments under `SKILL.md` result validity, so neither result is cited for the other.
- A tool the gate invokes that behaves differently in the CI image is a product or harness defect, because CI runs that image; a setup, mount, copy, or missing-service failure stays a host-environment block.
- Run on the host instead, and report why, when Docker is unavailable, when the image is neither present locally nor pullable as a declared action from a registry the repository allows, or when repository policy places the gate on the host. Never substitute another image.


## Comparative timing

A before/after performance claim requires an idle host: no unrelated CPU-heavy work and no overlapping validation. Verify and record host load before and during samples; discard or label contaminated samples rather than presenting them as improvement. Loaded or slower-host runs remain valid flake diagnosis under `50-flake.md`; they do not support a speed comparison.

Keep CPU allocation/affinity, worker counts, workload/case selection, dependency state, tool versions, image, setup and cache state identical between candidates. Declare warmup, warm/cold cache policy, sample count and interleaved before/after order before measurement; do not measure every baseline first and every candidate second. Record timer identity, timer resolution, raw samples, units, spread/dispersion and deviations/outliers with their causes, plus candidate snapshots and exact commands. Retain machine-readable timing output when the tool supports it. Uncontrolled load, changed workload, incomparable caches or inadequate timer resolution leaves the performance claim unverified; report the limit without inventing an improvement.

## Runner compatibility

The canonical implementations are `scripts/run-low-priority.sh` and `scripts/Invoke-AlaaLowPriority.ps1` in this skill. Legacy paths in both orchestrators are thin forwarders to these siblings: they preserve arguments, child stdout/stderr and exit status from any cwd, including paths with spaces. A missing canonical runner fails clearly and requests a compatible testing-strategy package; it never triggers installation or falls back to copied logic. PowerShell preserves working directory, environment overrides, output files and timeout exit `124`. Unix uses Bash and `nice`, with optional `taskset`; CPU affinity availability must be recorded, never assumed.
