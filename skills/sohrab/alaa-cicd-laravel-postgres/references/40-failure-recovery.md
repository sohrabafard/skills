# Failure recovery

Read when a pipeline is red or intermittent, when a retry is proposed, and when a test is quarantined. Start from the symptom, not from the job that is red: in a Laravel-on-Postgres pipeline the failing job is often not the causing one.

## By symptom

| Symptom | Class | First diagnosis | Smallest safe retry | Escalate to |
|---|---|---|---|---|
| Migrate job exits non-zero; log names a SQL error, `already exists`, or a lock wait | migration failure | `php artisan migrate:status` on the same database; read the last migration that ran, not the first error line | none — re-running a partly applied set applies it twice. Reset the test database, then the gate in `30-migration-reversibility.md` | that file's owners for lock and partitioned-table behaviour |
| `connection refused`, `too many clients`, or auth failure on an arbitrary test | connection failure | the wait-for-database output first, then the arithmetic in `20-test-database-isolation.md` | re-run the wait step only, never the suite; `too many clients` is a budget defect and a re-run hides it | the connection budget in that file |
| Assertions fail on rows the test did not create; a different test fails each run; passes at one worker | cross-worker collision | run at one worker; if it passes, the databases are not isolated | none — a retry is a coin flip | the naming and teardown rules in `20-test-database-isolation.md` |
| Fails after a dependency or runtime bump with a missing class or version mismatch that does not reproduce locally | cache poisoning | compare the cache key against the lockfile hash and the runtime version in the image | one re-run with the dependency cache bypassed; if that passes, the key is wrong | fix the key so it cannot recur; `scripts/check-ci-determinism.sh` catches this class |
| Passes alone, fails in the suite, or fails only under one shuffle seed | order-dependent failure | re-run with the recorded seed, then alone | none | `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/50-flake.md` |

## Waiting for the database

The wait-for-database step has a bounded attempt count and a deadline, both read from CI variables and validated at job start. On exhaustion it fails the job with the last connection error and the elapsed time, and the suite does not run — a suite started against an unready database produces failures that read as product defects. Those values belong to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; why a bound exists at all to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Retry mechanics

Classification comes first and belongs to `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/50-flake.md`, which also names the only legitimate retry — one keyed to a named infrastructure failure class. This file owns only how CI expresses and records it.

- A retry declared as a bare count retries assertion failures and is forbidden. The replacement is the runner's failure-class-scoped form listing the classes that file names; the syntax belongs to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`). `scripts/check-ci-determinism.sh` reports a bare count as a finding.
- Every retried attempt appends a line to a retained artifact: job, attempt number, failure class matched, commit. A retry leaving no artifact is indistinguishable from a clean pass, which is how a retried pipeline becomes the normal pipeline.
- The count of retried attempts, and the runner's shuffle seed, are printed with every suite result — the seed so an order-dependent failure is reproducible without waiting for it to recur.
- **Quarantine's exit is mechanical and CI owns it**: the quarantined suite runs as a separate non-gating job on the same cadence, its result and count are reported by the gating job, and the gating job **fails** when the quarantine list holds an entry past its deadline. CI is the only place a date is checked without a human remembering.

## Artifacts

Every gate run — passing, failing, cancelled or timed out — leaves the machine-readable test report, the shuffle seed, the static-analysis error list, the migration output and the determinism-script output on the artifact path.

- Written as the job runs, not assembled at the end, and declared to upload on failure and cancellation as well as success: the run that needs an artifact is the run that did not finish.
- The path carries the attempt, `<job>/<attempt>/<artifact>`. An attempt overwriting the one it replaced destroys the evidence that a retry happened.
- Retention outlives the rollback window of the release the artifact gates. That window's value belongs to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
