# Changelog

## 2.1.0

- Wired the Alaa skill ecosystem into role agents: security ($alaa-security-review, $alaa-trust-gateway-auth), observability ($alaa-observability-soc), migration ($alaa-data-layer, $alaa-partitioned-table-fk-audit), release ($alaa-docker-production, $alaa-gitlab-ci-cd, $alaa-cicd-laravel-postgres, $alaa-k8s-helm), browser QA ($playwright), performance ($alaa-octane-performance, $golang-performance), test strategy ($golang-testing), architecture ($alaa-services-contract, $alaa-project-constitution).
- Added routing of durable multi-phase plan/state engagements to $alaa-workflow, with single-phase execution through this skill allowed under workflow ownership.
- Corrected the Codex concurrency config key to the documented [agents] max_threads with a freshness caveat.
- Refreshed manifest hashes.

## 2.0.0

- Added mandatory idempotent auto-install/update into `~/.codex/agents` with backups.
- Added repository explorer and split external research from repository mapping.
- Added independent verifier using low-priority resource runners.
- Added failure analyst and pre-implementation test strategist.
- Added architecture, security, migration, browser QA, performance, observability, and release specialist gates.
- Added final documentation validation gate.
- Added current `max_concurrent_threads_per_session` guidance without modifying global config.
- Added Windows and Unix low-priority runners, status checks, validation, routing, failure taxonomy, and complete dispatch templates.
- Reduced Luna documenter effort to medium and preserved `--browser chromium` as a hard user constraint.
