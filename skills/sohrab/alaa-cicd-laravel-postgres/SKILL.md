---
name: alaa-cicd-laravel-postgres
description: "Release gates for Laravel services on Postgres: which checks are gates and which advisory, static-analysis and coverage thresholds, the migration up-down-up reversibility gate, per-worker test-database isolation, Postgres production-version parity with a defined SQLite fallback, image-tag and cache-key determinism, flaky-test and retry mechanics, and CI secret exposure. Use when a pipeline, release gate, test database, migration job, cache key, service image, or CI credential changes; when a pipeline is green against broken code; and when CI fails or flakes around Postgres or migrations. Do not use for GitLab or GitHub Actions YAML syntax, runners, or protected variables (/alaa-gitlab-ci-cd); test design and flake doctrine (/alaa-testing-strategy); migration lock and large-table safety (/alaa-data-layer); security controls (/alaa-security-review); or application edits with no pipeline effect."
---

# Alaa CI/CD Laravel Postgres

Decide which checks may block a Laravel-on-Postgres release, and at what threshold. State each decision as commands and predicates for any runner. This skill emits no provider YAML. `/alaa-gitlab-ci-cd` owns how a provider expresses a gate.

**A step that cannot fail the pipeline is advisory, whatever its name.** A step is a gate only if a non-zero exit from its command stops the pipeline and leaves no deployable artifact. Each of these turns a gate into an advisory step: `allow_failure`, `continue-on-error`, a trailing `|| true`, a pipe without `pipefail`, a wrapper that discards the status, and a rule that skips the step on the deploying branch. The result is a green run that proves only that the runner started. Classify every check the change touches in `references/10-gate-register.md`. Report by the output contract there.

## Always true

- **One test run, on production's Postgres, with SQLite only as its fallback.**
  - Run the suite once per pipeline, on the Postgres major **and** minor of the running production instance. Read that version from the instance with `SELECT version()`.
  - Probe reachability in a step separate from the suite.
  - Reachable: run the suite on Postgres and make its exit status final. A Postgres-only failure then fails the pipeline.
  - Unreachable: run the suite on SQLite in-memory instead and make that run's exit status final. Write a `parity-unproven` artifact naming the pipeline.
  - Never run the suite on both engines in one pipeline, because once Postgres has answered, a SQLite run repeats the whole suite and proves nothing more.
  - **Only unreachability may trigger the fallback.** A `|| true` around the whole job converts a real Postgres-only defect into a warning and makes the lane worthless.
  - On a pipeline that gates a release, the fallback is not permitted. An unreachable parity database fails that pipeline.
  - A third engine, neither SQLite nor production's Postgres, is a deviation and needs the register entry below.
  - Never run migration reversibility on SQLite. See `references/30-migration-reversibility.md`.
- **Version coherence.** Change repo-pinned PHP, Composer and Node versions, Docker images, CI matrices and cache keys in one change. Bumping `composer.json` alone leaves the toolchain split-brained, and the pipeline then proves a combination that never ships.
- **No value lives here.** Take timeout, retry, pool and worker-budget numbers from `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. Take the reason from `/alaa-reliability-sla`.

Before you finish any CI-file change, run `scripts/check-ci-determinism.sh`. Its `--help` states each exit code.

## When NOT to use

- The change touches application code only. It alters no pipeline stage, no gate threshold, no test database, no migration job, no image tag, no cache key, and no CI credential.
- The question is provider YAML syntax, runner configuration, or how a protected variable is declared, rather than what the pipeline must gate on and at what threshold.
- The question is what makes a test a test, or whether a migration is lock-safe on a large table. The routing section below names each owner.

## Read next

| You are about to | Read |
|---|---|
| add, weaken or reorder a check, set a threshold, or judge a green run | `references/10-gate-register.md` |
| enable parallel tests, change the test database, or fix a collision | `references/20-test-database-isolation.md` |
| add, edit or reorder a migration, or wire the job that migrates | `references/30-migration-reversibility.md` |
| triage a red or flaky pipeline, propose a retry, or quarantine a test | `references/40-failure-recovery.md` |
| put a credential, registry token, OIDC role or scan in a job | `references/50-ci-secrets-and-supply-chain.md` |
| state a rule about tests, timeouts, secrets, observability or YAML | `references/60-ownership-boundary.md` |
| rely on a version, image tag or constraint that may have moved | `references/90-source-map.md` |
