# Gate register

Read when adding, removing, reordering or weakening a check, when setting a threshold, and whenever a green run is offered as evidence. `SKILL.md` holds the gate-versus-advisory discriminator; this file holds the register, the thresholds, the exit obligations and the output contract. An ordering — format, then static analysis, then tests — is not a register: three correctly ordered steps that cannot fail the pipeline give a green run with hundreds of unaddressed errors.

Every check in a pipeline appears below with a class; one present in the pipeline but missing here is advisory until classified, and a change leaving one unclassified is not done. Invocations are written as they run from the repository root with `php` on `PATH`; where the repository drives PHP through a Makefile target, a Composer script or a container `exec`, that wrapper is used and the report names it.

| Check | Invocation | Class | Threshold |
|---|---|---|---|
| Formatting | `vendor/bin/pint --test` | gate | zero files needing change |
| Static analysis | `vendor/bin/phpstan analyse --no-progress` | gate | zero errors outside the committed baseline |
| Tests, SQLite lane | `php artisan test` with `DB_CONNECTION=sqlite` and `DB_DATABASE=:memory:` | gate | zero failed, zero errored, zero skipped without a reason recorded in the test |
| Tests, Postgres parity lane | a reachability probe, then `php artisan test` against production's Postgres major and minor | gate with one defined non-failure | reachable: the suite's own exit status is final. Unreachable: re-run on SQLite, exit zero, publish the `parity-unproven` artifact — except on a release-gating pipeline, where unreachable fails |
| Coverage measurement | `php artisan test --coverage-clover=<artifact path>` | advisory artifact | none; never a pass/fail number |
| Diff-test obligation | the diff's changed application files against its added or changed test files | gate | every changed application file is named by a test the same diff adds or changes, or carries a recorded exemption |
| Migration reversibility | `30-migration-reversibility.md` | gate | that file's predicate |
| Test-database isolation | `20-test-database-isolation.md` | gate | that file's predicate |
| Determinism | `scripts/check-ci-determinism.sh` | gate | exit 0 |
| Dependency advisories | `composer audit --format=json` | gate | zero advisories at or above the committed severity policy |
| SBOM | the repository's SBOM command | advisory artifact | produced and retained on every release run |
| Boot smoke | the three checks below | gate | all three exit zero |

## Thresholds that need stating

**Static analysis.** Level and baseline live in `phpstan.neon`; the pipeline never passes `--level`, which would let one job disagree with the repository invisibly. A Laravel repository registers the Larastan extension — without it every facade and Eloquent magic call is an error and the level gets lowered to compensate, which is how a repository ends up gating at a level that proves nothing. The baseline may only shrink: a change that adds an entry fails the gate unless that entry is recorded in the deviation register below.

**Coverage.** Measured every run and published as an artifact, never a pass/fail percentage — a percentage rises when code is executed without being asserted on. The mechanical gate over test adequacy is the diff-test obligation row. An existing percentage gate stays and never substitutes for that row; `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns what coverage may evidence.

**Complexity.** Enforced by the static-analysis gate, so it fails a pipeline rather than a comment thread. The per-unit ceiling belongs to `/alaa-php-clean-code` (`$alaa-php-clean-code`), the growth bound to `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).

**Dependency advisories.** The scan runs on every pipeline and is a gate; its failing severity is read from a committed policy file, and **a missing policy file fails the job** rather than skipping the scan, because a scan skipped for want of policy is a scan nobody enables. Commit the policy.

**Boot smoke.** Three checks, because a process that starts is not a service that works:

1. `php artisan route:list --json` exits zero and reports no fewer routes than the merge base — a provider that throws during boot drops routes silently.
2. `php artisan migrate:status` exits zero against the parity database — the shipped configuration reaches Postgres and reads the migration table.
3. The built artifact, started in the form it deploys in, answers its readiness endpoint from outside its own process; that endpoint's shape belongs to `/alaa-services-contract` (`$alaa-services-contract`).

`php artisan about` is not a gate: it proves the container booted, and nothing about routes, queues or the database.

## The deviation register

Three rules have an exit — a test engine that is neither SQLite nor production's Postgres, a baseline that grew, and a diff-test exemption. Each requires all three of the following, and an exit missing one is not an exit, so the gate fails: **the reason**, in one sentence naming what forced it; **the approver**, the name of the human who accepted it — any human on the team may, and **no agent may, ever**: an agent that meets a blocking finding records what it found and stops, then asks a human, because an unsigned exit is indistinguishable from one the agent wrote for itself; and **the location**, which is the repository's committed deviation register (`AGENTS.md` or the file it names) and never a merge-request comment, because a comment is not readable by the next run. A deviation is re-reviewed by the same approver when the engine version, the framework major, or the exempted file changes.

## What each script exit obliges

- **0** — no finding at the lexical level. Report the determinism claim as static proof, nothing stronger.
- **1** — findings, with file and line. Fix each, or record it in the deviation register, before the change is done. A finding is not a warning.
- **2** — usage error. Re-invoke correctly; never report this as a pass.
- **3** — no CI configuration at the given path. Report that the check did not run, not that it passed.
- **4** — the CI file only includes configuration from elsewhere. Run the script in the repository owning the included file and report both results.

## Output contract

```text
Gates changed: check -> gate|advisory before -> after -> threshold -> what a non-zero exit obliges
Evidence: exact invocation per gate, its observed exit status, and the wrapper used if any
Parity: Postgres major.minor used, production's, how production's was read, and — when the parity lane fell back to SQLite — that it fell back, on which pipeline, and the artifact recording it
Migrations: up-down-up result and the schema-comparison output
Isolation: worker count, database-name pattern, teardown step, connection budget
Determinism: script exit code and every finding, or why the script did not run
Flake: intermittent results, their classification, and the artifact recording any retry
Deviations: each exit taken -> reason -> approver -> where recorded
Risks: what remains ungated, and who owns it
```
