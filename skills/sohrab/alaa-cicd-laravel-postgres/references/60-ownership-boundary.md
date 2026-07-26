# Ownership boundary

Read before stating any rule about test design, timeouts, migrations, secrets, observability or provider YAML inside a pipeline. This skill owns which checks gate a Laravel-on-Postgres release, at what threshold, and how the test database, migration gate and recovery path are wired — almost nothing else. A rule restated here rather than pointed at will drift from its owner.

| Ground | Owner, and what wins on conflict |
|---|---|
| YAML schema, `services:`, `needs:`, `rules:`, runner tags, cache and artifact syntax, protected variables, environments, CI lint | `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) — wins on how a gate is expressed; this skill wins on whether a step is a gate and at what threshold |
| What makes a test a test, layer placement, doubles, proof levels, flake classification, quarantine doctrine, coverage as evidence | `/alaa-testing-strategy` (`$alaa-testing-strategy`) — wins on what a test must prove and whether a retry is permitted; this skill wins on how a check is wired, when it blocks, and how a retry is recorded |
| Timeouts, retries, backoff, idempotency, degraded dependencies, error budgets | `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the reason, `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` every value; this skill states neither |
| Migration lock behaviour, large-table and backfill safety, index and tenancy shape | `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md`, and `/alaa-partitioned-table-fk-audit` (`$alaa-partitioned-table-fk-audit`) for partitioned-table FK hazards — they win on what a safe migration does; this skill wins on the gate proving it reverses |
| Trust boundaries, authn/authz, untrusted input, secret handling, tenant isolation | `/alaa-security-review` (`$alaa-security-review`) — wins outright; `50-ci-secrets-and-supply-chain.md` adds only CI-specific exposure |
| Log, metric and event names, readiness and envelope shapes, deprecation windows | `/alaa-services-contract` (`$alaa-services-contract`) names them; `/alaa-observability-soc` (`$alaa-observability-soc`) sets whether a signal is required. This skill names neither, and contributes only the pipeline's own evidence artifacts |
| SOLID, design patterns, size budgets, Pest and PHPUnit idiom | `/alaa-php-clean-code` (`$alaa-php-clean-code`) |
| Complexity bounds and structure choice | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| The ten quality criteria, and the build/test/migrate/deploy/rollback phases every service shares | `alaa-project-constitution references/quality-bar.md` — never restated here |
| Image build, base image, build-time runtime parity | `/alaa-docker-production` (`$alaa-docker-production`) |
| Any step holding a credential, mutating production infrastructure, or needing an approver; the proof-strength vocabulary | `/alaa-controlled-ops` (`$alaa-controlled-ops`) — owns the stop-and-ask procedure this skill routes into |
| Phasing a pipeline migration across sessions | `/alaa-workflow` (`$alaa-workflow`) |
| Model and effort | `/alaa-prompting-guide` (`$alaa-prompting-guide`) — no model is named anywhere in this skill |

A Laravel repository may also ship upstream skills this repository does not control (`laravel-best-practices`, `octane-development`, `pest-testing`). Route to them for framework mechanics; never let one be the sole place a gate threshold or safety invariant is stated, since they can be re-pulled or reworded between runs. Where an upstream file and this skill disagree on whether something gates a release, this skill wins.
