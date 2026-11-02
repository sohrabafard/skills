# Normative duplicate preservation inventory

The cause-specific repair reconciles the entire previous length-based duplicate guard with the existing explicit short-rule protection. All 54 previously guarded clauses and all 46 shorter protected clauses remain rejected as duplicated policy. No previously guarded clause is excluded. True pointers, topic names and status fragments remain covered by the existing legal-pointer fixtures.

The production map contains 100 owner/clause pairs. A frozen SHA-256 fixture independently identifies that complete inventory; deleting any production entry changes the digest and fails normal checking and self-test, even when generated mutation loops omit the deleted entry. Each entry also has a fresh-map removal fixture against the frozen digest, a canonical-membership fixture and a duplicate-in-consumer fixture.

Manifest method: normalize each clause by whitespace folding and casefold, prefix its owner and TAB, sort all entries, join with LF and append LF, then SHA-256 over UTF-8 bytes. The expected digest is a literal fixture, never computed from the production map as an expected value at runtime.

Parent-authorized caller alignment updates the one runtime-ops route to its declared runtime scope. The obsolete named-pipe invocation remains rejected as a retired contradiction; no prior rejection is lost. The updated route keeps the frozen normative inventory at 100 entries.

Expected fixture SHA-256: `73b16c7c0098cd2d708dddc818f05eca998baa6d48ce7ceccba599eeed851061`.

| Owner | Clause | Previous protection |
|---|---|---|
| execution | Runtime orchestrators own role authority, observer independence, allocation and phase/review scheduling | former >=80 guard |
| execution | required gates, exact commands and scoped inputs, cwd, timeout, environment/resource limits, expected cases, declared case dependencies, aggregate-to-child coverage and eligible citations | former >=80 guard |
| execution | Record each command's machine-readable reporter when available and retain its output | former >=80 guard |
| execution | Record the tested content snapshot, relevant untracked inputs and tool versions | existing shorter clause |
| execution | Keep check inputs stable during the pass | existing shorter clause |
| execution | For a new or changed test command, or one with a recorded harness failure, confirm selection before citing its result | former >=80 guard |
| execution | otherwise compare the first run's selected cases with the recorded expected cases | former >=80 guard |
| execution | Preserve selected and executed counts, case identities and skip/setup reasons, including every covered child of an aggregate | former >=80 guard |
| execution | Non-test lint/type/build/render commands need no case selection check | existing shorter clause |
| execution | Inspect aggregate execution: a name proves no coverage | existing shorter clause |
| execution | Count underlying checks once and run uncovered gates separately | existing shorter clause |
| execution | Run checker self-tests only when checker logic changes | existing shorter clause |
| execution | One failure never cancels independent remaining checks | existing shorter clause |
| execution | Record each command's exit/result and each unrun check's blocker | existing shorter clause |
| execution | A dependent case whose precondition failed is skipped with that precondition named | former >=80 guard |
| execution | use its supported keep-going mode or exact uncovered child commands while preserving failure exits | former >=80 guard |
| execution | A clear owner or cheap fix does not bypass collection | existing shorter clause |
| execution | Only an obstruction blocking all or most remaining checks permits minimal early repair | former >=80 guard |
| execution | record the cause and blocked checks, repair only that obstruction, then resume the full collection, including previously blocked checks | former >=80 guard |
| execution | No review or acceptance precedes complete collection and required retests | existing shorter clause |
| execution | After batch repair, rerun the whole recorded check list on the frozen repaired snapshot, including checks previously discharged by citation | former >=80 guard |
| execution | Invalidate affected evidence | existing shorter clause |
| execution | New failures follow the same collection barrier within existing retry/stop budgets | former >=80 guard |
| execution | Preserve the original failure, repair and retest separately | existing shorter clause |
| execution | Never weaken assertions, suppress findings, lower thresholds, widen tolerances, add assertion retries or alter fixtures to conceal failure | former >=80 guard |
| execution | Environment recovery changes require their own authority and evidence | existing shorter clause |
| execution | Unresolved required checks block acceptance | existing shorter clause |
| resources | Tool/runtime concurrency (`GOMAXPROCS`, package parallelism, test workers, browser workers) | former >=80 guard |
| resources | Lower priority does not limit parallelism. Configure both | existing shorter clause |
| resources | Use `Idle` only for explicitly background-grade benchmark/fuzz/full-profile work | former >=80 guard |
| resources | Do not use `Realtime` or `High` | existing shorter clause |
| resources | Use repository scripts exactly | existing shorter clause |
| resources | Do not run package installation merely because a command is missing | existing shorter clause |
| resources | Preserve explicit `--browser chromium` | existing shorter clause |
| resources | Preserve configured user-data/profile paths | existing shorter clause |
| resources | Do not kill unrelated services, dev servers, containers, or processes | existing shorter clause |
| resources | Do not start duplicate services when a reusable declared service already exists | existing shorter clause |
| resources | Limit browser workers through the repository-supported mechanism only | existing shorter clause |
| resources | Do not kill or reuse another worktree's server without explicit ownership | existing shorter clause |
| resources | Declare one allowed artifact directory in the execution record | existing shorter clause |
| resources | Write run artifacts only there plus unavoidable tool temp directories allowed by the sandbox | former >=80 guard |
| resources | Unexpected tracked file changes contaminate the run | existing shorter clause |
| resources | Run only one CPU-heavy verification or profiling command at a time per host in this workflow | former >=80 guard |
| resources | A gate's supported internal parallel mode counts as that one command | existing shorter clause |
| resources | Priority alone is not a CPU limit | existing shorter clause |
| resources | including container/VM/cgroup quotas, affinity restrictions and reserved capacity | former >=80 guard |
| resources | Their simultaneous allocations must fit effective host capacity with the declared reserve | former >=80 guard |
| resources | Set container `--cpus` limits below the host logical CPU count and within that effective budget | former >=80 guard |
| resources | Record dependency-container allocations as well as the test-container allocation | former >=80 guard |
| resources | Defer work when a safe concurrent budget cannot be established | existing shorter clause |
| resources | read-only source mount, complete copy into the container filesystem (including required Git metadata) | former >=80 guard |
| resources | The container CPU limit replaces the host low-priority wrapper for that run | existing shorter clause |
| resources | make one host fallback under the low-priority wrapper when repository policy and authority permit | former >=80 guard |
| resources | Under Codex, invoke /alaa-codex-runtime-ops for Docker-access permission failures within its declared runtime scope before fallback | former >=80 guard |
| resources | Installation, pulling an undeclared image, permission changes or starting an unowned service require separate authority | former >=80 guard |
| resources | Never substitute another image | existing shorter clause |
| resources | A before/after performance claim requires an idle host: no unrelated CPU-heavy work and no overlapping validation | former >=80 guard |
| resources | Verify and record host load before and during samples | existing shorter clause |
| resources | discard or label contaminated samples rather than presenting them as improvement | former >=80 guard |
| resources | Loaded or slower-host runs remain valid flake diagnosis under `50-flake.md`; they do not support a speed comparison | former >=80 guard |
| resources | Keep CPU allocation/affinity, worker counts, workload/case selection, dependency state, tool versions, image, setup and cache state identical between candidates | former >=80 guard |
| resources | Declare warmup, warm/cold cache policy, sample count and interleaved before/after order before measurement | former >=80 guard |
| resources | Record timer identity, timer resolution, raw samples, units, spread/dispersion and deviations/outliers with their causes | former >=80 guard |
| resources | Retain machine-readable timing output when the tool supports it | existing shorter clause |
| resources | The canonical implementations are `scripts/run-low-priority.sh` and `scripts/Invoke-AlaaLowPriority.ps1` in this skill | former >=80 guard |
| resources | preserve arguments, child stdout/stderr and exit status from any cwd, including paths with spaces | former >=80 guard |
| resources | PowerShell preserves working directory, environment overrides, output files and timeout exit `124` | former >=80 guard |
| classification | Use one primary classification per command and record secondary factors separately | former >=80 guard |
| classification | whose selection is empty or differs from the expected cases recorded for it is `TEST-INFRA-FAILURE`, never `PASS` | former >=80 guard |
| classification | inside a container run, an incomplete copy or mount is instead `ENVIRONMENT-BLOCKED` | former >=80 guard |
| classification | A list or collect selection check executes no case by design: it is `PASS` when it lists exactly the expected cases | former >=80 guard |
| classification | A scoped lint, type-check or build command whose scope matches no file is `TEST-INFRA-FAILURE` | former >=80 guard |
| classification | Do not disguise this as a product failure or install/change the environment without authority | former >=80 guard |
| classification | Preserve partial logs and process/resource evidence | existing shorter clause |
| classification | Do not revert automatically | existing shorter clause |
| classification | Unexecuted checks are never implied passes | existing shorter clause |
| classification | A container runtime is not running, an image is absent, a mount failed, or the daemon refused the socket | former >=80 guard |
| classification | A file, directory, port, or device was refused, locked, or held open by another process | former >=80 guard |
| classification | A required executable, service, credential, browser, or platform capability is absent | former >=80 guard |
| classification | A build, dependency, module, or test cache served an artifact from before the change | former >=80 guard |
| classification | The harness, fixture, factory, seed, or generated setup broke independently of the behaviour under test | former >=80 guard |
| classification | Never repair the product in response to any row above | existing shorter clause |
| classification | Clearing a cache, installing a tool, changing a permission, or starting a service is a declared and reported action, never a silent retry step | former >=80 guard |
| classification | Identify the first causal error, not the last stack trace | existing shorter clause |
| classification | Confirm command/cwd/environment/resource limits | existing shorter clause |
| classification | Compare initial/final git status and concurrent changes | existing shorter clause |
| classification | Inspect the owning code/test/config path | existing shorter clause |
| classification | Classify owner: product, test infrastructure, environment, or unresolved ownership | former >=80 guard |
| classification | Route the smallest grounded next action | existing shorter clause |
| doctrine | **Focused** \| the smallest test/path/scenario distinguishing the subtask's changed behavior | former >=80 guard |
| doctrine | **Task acceptance** \| bounded acceptance selectors combining that task's subtasks | former >=80 guard |
| doctrine | **Exhaustive** \| the whole suite and only the race, end-to-end and higher-level proofs the claims require | former >=80 guard |
| doctrine | Labels never narrow an actual command's scope | existing shorter clause |
| doctrine | When one of them changes, say which one, and re-run every result downstream of it | former >=80 guard |
| doctrine | any result classified `FLAKY`, `CONTAMINATED`, `TIMEOUT`, or environment-blocked | former >=80 guard |
| doctrine | a check outside the list runs only when the repair changes shared behaviour or proves a new reachable surface | former >=80 guard |
| doctrine | A phase transition, new agent or compaction alone invalidates nothing | existing shorter clause |
| doctrine | A case failing never stops an independent case from running | existing shorter clause |
| doctrine | Classify first, then act | existing shorter clause |
| doctrine | A tier is never made to pass by deleting an assertion, widening a tolerance, adding a retry, skipping a case, or lowering a threshold | former >=80 guard |
