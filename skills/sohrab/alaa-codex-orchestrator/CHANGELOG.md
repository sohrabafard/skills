# Changelog

## 2.1.3

- Escalation discipline: default down; escalation earned by decision density, never surface sensitivity or goal importance; named criterion required in dispatch and roster; when uncertain, do not escalate.
- Anti-patterns extended for habitual top-tier implementation dispatches.

## 2.1.2

- Bootstrap redesigned: one sentinel-file check per activation (.alaa-codex-orchestrator.version vs VERSION); installer runs only on first install or version change, one attempt, never blocks dispatch.
- Fixed installer empty-path failure when $PSScriptRoot is unset (robust script-root resolution with explicit -SourceDirectory fallback error).
- Both installers now write the version sentinel after installing.

## 2.1.1

- Every agent now begins its final report with a mandatory AGENT | MODEL | EFFORT identity line and flags pin mismatches.
- The orchestrator final report gained an agent roster section listing each dispatched subagent with pinned and self-reported model/effort.

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
