# Execution Resources

Repository-specific constraints stay binding. Four separate layers control resources:

1. OS process priority (`BelowNormal` by default, which is `nice 10`).
2. Optional CPU affinity/count.
3. Tool and runtime concurrency (`GOMAXPROCS`, package parallelism, test workers, browser workers).
4. Timeout and one-heavy-command-at-a-time policy.

Lower priority does not limit parallelism. Configure both.

## Low-priority runner

Resolve the absolute script path from this skill. Install or update nothing automatically.

```bash
bash "<TESTING_SKILL_ROOT>/scripts/run-low-priority.sh" \
  --priority BelowNormal \
  --cpu-count 2 \
  -- env GOMAXPROCS=2 go test -p 1 -parallel 2 -count=1 ./...
```

The runner returns the child exit code and emits stdout/stderr. The runner uses Bash and `nice`, with optional `taskset`: when `--cpu-count` is set and `taskset` is available, it also limits CPU affinity. Record whether affinity was applied; never assume it. Use `Idle` only for benchmark, fuzz or full-profile work that is explicitly background-grade.

The canonical implementation is `scripts/run-low-priority.sh` in this skill. The legacy paths in both orchestrators are thin forwarders: they preserve arguments, child stdout/stderr and exit status from any cwd, including paths with spaces. When the canonical runner is missing, a forwarder fails clearly and requests a compatible testing-strategy package; it never triggers installation or falls back to copied logic.

## Go verification profiles

Derive final commands from repository guidance. A conservative race check uses one package worker and one parallel test:

```bash
GOMAXPROCS=2 go test -race -p 1 -parallel 1 -count=1 ./...
```

`-p` controls package and build concurrency. `-parallel` controls tests using `t.Parallel` inside a test binary. `GOMAXPROCS` controls runtime CPU parallelism. They are not interchangeable.

Test-result caching is separate from build caching. When a validity condition in `SKILL.md` changes, or a check requires fresh proof, bypass result reuse for its selected packages or topics, including affected-tier checks against external dependency state (Go: `-count=1`, at any tier), and retain the build cache. `./...` is exhaustive-only.

## Node/Vue/Quasar

Use repository scripts exactly. Apply a worker limit only through a mechanism that the tool supports and that repository policy does not contradict. The mechanism differs between Vitest, Jest, Playwright and Vite; never guess it.

Do not run package installation merely because a command is missing. Report `ENVIRONMENT-BLOCKED`.

## PHP/Laravel

Use repository commands, and do not introduce ParaTest or process isolation during verification. Lower the OS priority for a broad suite or static analysis that is declared CPU-heavy.

## Service safety and reuse

- Do not kill unrelated services, dev servers, containers, or processes.
- Do not start duplicate services when a reusable declared service already exists.
- Before you return, stop each background process, container and service that this run started, and remove each temporary file that it created outside the allowed artifact directory. Keep what a declared reuse or a later step of the same engagement needs. Reason: agents that share a machine leave CPU and memory to the other work ([Prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra), 18 November 2026).

## Browser QA

- Preserve explicit `--browser chromium`.
- Preserve configured user-data and profile paths.
- Limit browser workers through the repository-supported mechanism only.
- Do not kill or reuse another worktree's server without explicit ownership.

## Artifacts

Declare one allowed artifact directory in the execution record. Write run artifacts only to that directory and to the unavoidable tool temporary directories that the sandbox allows. Unexpected tracked file changes contaminate the run.

## Host and container budgets

Run only one CPU-heavy verification or profiling command at a time per host in this workflow. A gate's supported internal parallel mode counts as that one command. Record effective host capacity, including container, VM and cgroup quotas, affinity restrictions and reserved capacity; an unavailable capacity observation is unknown, never unlimited.

Before you start test or dependency containers, allocate explicit CPU budgets across every concurrent container and host worker. Their simultaneous allocations must fit effective host capacity with the declared reserve. Set container `--cpus` limits below the host logical CPU count and within that effective budget; align each gate's worker, package and runtime counts with its container allocation. Record dependency-container allocations as well as the test-container allocation. Defer work when a safe concurrent budget cannot be established.

For a CI-image gate, use the image that the repository's CI configuration or documentation names. Never substitute another image. Record the image reference, read-only source mount, complete copy into the container filesystem (including required Git metadata), setup and services, and CPU and worker limits. Verify copied inputs and expected selection before you accept coverage. The container CPU limit replaces the host low-priority wrapper for that run. A tool that the gate invokes and that behaves differently in the CI image is a product or harness defect, because CI runs that image.

If Docker, the image, mount, copy, setup or required service blocks a container run, record `ENVIRONMENT-BLOCKED` and make one host fallback under the low-priority wrapper when repository policy and authority permit. Record why, the changed environment and any lost coverage; never call it container proof. Under Codex, invoke /alaa-codex-runtime-ops for Docker-access permission failures within its declared runtime scope before fallback. Installation, pulling an undeclared image, permission changes or starting an unowned service require separate authority.

## Comparative timing

Measure performance only for a named question with a comparable baseline and a declared budget. Use the smallest workload that answers it, and widen it only when that workload leaves required proof uncovered.

A before/after performance claim requires an idle host: no unrelated CPU-heavy work and no overlapping validation. Verify and record host load before and during samples; discard or label contaminated samples rather than presenting them as improvement. Loaded or slower-host runs remain valid flake diagnosis under `50-flake.md`; they do not support a speed comparison.

Keep CPU allocation and affinity, worker counts, workload and case selection, dependency state, tool versions, image, setup and cache state identical between candidates. Before measurement, declare the warmup, the warm or cold cache policy, the sample count and the interleaved order of before and after samples; do not measure every baseline first and every candidate second. Record the timer identity, timer resolution, raw samples, units, spread or dispersion, and every deviation or outlier with its cause, plus candidate snapshots and exact commands. Retain machine-readable timing output when the tool supports it. Uncontrolled load, changed workload, incomparable caches or inadequate timer resolution leaves the performance claim unverified: report the limit, and claim no improvement.
