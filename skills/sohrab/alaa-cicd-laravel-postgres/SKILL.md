---
name: alaa-cicd-laravel-postgres
description: "Release gates for Laravel services on Postgres: which checks are gates and which advisory, static-analysis and coverage thresholds, the migration up-down-up reversibility gate, per-worker test-database isolation, Postgres production-version parity with a defined SQLite fallback, image-tag and cache-key determinism, flaky-test and retry mechanics, and CI secret exposure. Use when a pipeline, release gate, test database, migration job, cache key, service image, or CI credential changes; when a pipeline is green against broken code; and when CI fails or flakes around Postgres or migrations. Do not use for GitLab or GitHub Actions YAML syntax, runners, or protected variables (/alaa-gitlab-ci-cd); test design and flake doctrine (/alaa-testing-strategy); migration lock and large-table safety (/alaa-data-layer); security controls (/alaa-security-review); or application edits with no pipeline effect."
---

# Alaa CI/CD Laravel Postgres

Decide which checks may block a Laravel-on-Postgres release and at what threshold, as commands and predicates for any runner. This skill emits no provider YAML; `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how a gate is expressed on one.

**A step that cannot fail the pipeline is advisory, whatever it is named.** A step is a gate only if a non-zero exit from its command stops the pipeline and leaves no deployable artifact. `allow_failure`, `continue-on-error`, a trailing `|| true`, a pipe without `pipefail`, a wrapper that discards the status, and a rule skipping the step on the deploying branch each turn a gate into an advisory step, leaving a green run that proves only that the runner started. Classify every check the change touches in `references/10-gate-register.md`; report by the output contract there.

## Always true

- **Two test lanes, both gates.** The suite runs twice: on SQLite in-memory, and on the Postgres major **and** minor of the running production instance, read from it with `SELECT version()`. The SQLite lane has no fallback. The Postgres lane probes reachability in a step separate from the suite: unreachable re-runs the suite on SQLite, exits zero, and writes a `parity-unproven` artifact naming the pipeline; reachable makes the suite's own exit status final, so a Postgres-only failure fails the pipeline. **Only unreachability may trigger the fallback** — a `|| true` around the whole job converts a real Postgres-only defect into a warning and makes the lane worthless. On a pipeline that gates a release the fallback is not permitted: an unreachable parity database fails that pipeline. A third engine, neither SQLite nor production's Postgres, is a deviation and needs the register entry below. Migration reversibility never runs on SQLite — see `references/30-migration-reversibility.md`.
- **Version coherence.** Repo-pinned PHP, Composer and Node versions, Docker images, CI matrices and cache keys move in one change; bumping `composer.json` alone leaves the toolchain split-brained and the pipeline proving a combination that never ships.
- **No value lives here.** Timeout, retry, pool and worker-budget numbers come from `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; the reason from `/alaa-reliability-sla` (`$alaa-reliability-sla`).

Run `scripts/check-ci-determinism.sh` before finishing any CI-file change; `--help` states each exit code.

## When NOT to use

- The change touches application code only and alters no pipeline stage, no gate threshold, no test
  database, no migration job, no image tag, no cache key, and no CI credential.
- The question is provider YAML syntax, runner configuration, or how a protected variable is declared,
  rather than what the pipeline must gate on and at what threshold.
- The question is what makes a test a test, or whether a migration is lock-safe on a large table. The
  routing section below names each owner.

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
