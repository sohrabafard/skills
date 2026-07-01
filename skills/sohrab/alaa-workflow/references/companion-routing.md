# Companion Skill Routing

`$alaa-workflow` owns orchestration. Use it together with the right domain skill.

## Always consider

- `$alaa-prompting-guide` for writing, tuning, or repairing any prompt this skill produces for another model or itself -- phase-prompt implementation/review prompts, `/goal` objectives, subagent lane instructions, and skill-trigger syntax (`$` vs `/`) all depend on getting the target model and runtime right.
- `$alaa-low-noise` for any non-trivial run that risks noisy logs, broad searches, long command output, large diffs, or oversized status chatter.
- `$alaa-security-review` for review mode, auth, tenant isolation, trust boundaries, untrusted input, secrets, permissions, public APIs, or deployment exposure.
- `$alaa-observability-soc` for review mode or implementation that touches logs, metrics, traces, alerts, incident evidence, queues, analytics, high-traffic production behavior, or failure visibility.
- `$alaa-docs-farsi` for repository documentation alignment, Persian docs, user-facing docs, or docs consistency checks.

## Laravel, PHP, services, and backend contracts

Use these when the task touches Laravel structure, service boundaries, contracts, or trust:

- `$alaa-laravel-architecture`
- `$alaa-php-clean-code`
- `$alaa-services-contract`
- `$alaa-security-review`
- `$alaa-trust-gateway-auth`
- `$alaa-laravel-job-rabbitmq`
- `$alaa-octane-performance`

Signals:

- `app/`, `routes/`, `bootstrap/`, `config/`, `database/`, `artisan`
- controllers, requests, resources, DTOs, jobs, listeners, middleware, policies
- response envelopes, tenant propagation, trusted headers, authN/authZ
- Octane, Swoole, RoadRunner, static state, worker lifecycle, high-concurrency behavior

## Vue, Quasar, Vite, and frontend delivery

Use these when the task touches Vue or Quasar behavior, rendering, design-system components, or deployment:

- `$alaa-frontend-developer`
- `$quasar-skill-packe`
- `$alaa-frontend-devops`
- `$alaa-frontend-doc-annotations`
- `$alaa-shaka-player`
- `$alaa-mono-package` when `packages/*` or workspace package consumption changes

Signals:

- `src/`, `packages/*`, `quasar.config`, `vite.config`, SSR, hydration, PWA, player integration
- frontend CI, Dockerfile, compose, static delivery, edge caching
- UI review, a11y, responsive behavior, RTL/dark mode, browser-only APIs

## Go, Node, Rust, and package boundaries

Use these when the task is language- or package-centric:

- `$alaa-golang`
- `$alaa-golang-fiber`
- `$alaa-mono-package`
- `$vector-rust-observability-pipelines`

Signals:

- `go.mod`, `cmd/`, `internal/`, `pkg/`
- `package.json`, workspace packages, internal shared packages
- Vector configs, VRL, Rust-based telemetry pipelines

## Data, caching, messaging, and storage

Use these when the task touches data modeling, persistence, queue semantics, cache behavior, or high-volume storage:

- `$alaa-data-layer`
- `$alaa-async-messaging`
- `$alaa-mongodb-patterns`
- `$clickhouse-performance-schema-ops`

Signals:

- PostgreSQL schema or query changes
- Redis cache, lock, invalidation, dedupe, or Horizon behavior
- RabbitMQ jobs, DLQ, retries, poison-message handling
- ClickHouse ingestion, TTL, MergeTree design
- MongoDB collections, indexes, TTL, bounded document design

## Infra, containers, Kubernetes, and delivery

Use these when runtime, packaging, or cluster surfaces change:

- `$alaa-docker-production`
- `$alaa-makefile`
- `$caas-arvan-kuber`
- `$alaa-haproxy`
- `$alaa-gitlab-ci-cd`
- `$alaa-k8s-helm`
- `$terraform-generator` / `$terraform-validator`
- `$terragrunt-generator` / `$terragrunt-validator`
- `$ansible-generator` / `$ansible-validator`

Signals:

- `Dockerfile`, `compose.yml`, Swarm, rootless container behavior
- `Makefile`, `.mk`, local automation, install/test/build wrappers
- Kubernetes, OpenShift, namespace-only access, Helm charts
- HAProxy configs and trust boundaries
- GitLab CI/CD, runners, executors, delivery pipelines

## Observability, logging, and incident evidence

Use these when the task touches telemetry, traces, metrics, logs, alerts, profiling, or operational evidence:

- `$alaa-observability-soc`
- `$fluentbit-generator` / `$fluentbit-validator`
- `$loki-config-generator`
- `$logql-generator`
- `$promql-generator` / `$promql-validator`

Signals:

- correlation IDs, alerts, traces, logs, dashboards, incident analysis
- Fluent Bit, Loki, Prometheus, LogQL, PromQL, OpenTelemetry, SigNoz, Sentry

## Docs, API collections, and user-facing artifacts

Use these when the task changes operational, API-facing, or user-facing documentation:

- `$alaa-docs-farsi`
- `$alaa-postman-collections`
- `$alaa-laravel-public-api-contract-pack`

Signals:

- `docs/`, `README.md`, `BIG_PICTURE.md`, runbooks, user-facing instructions
- API summaries, OpenAPI, Postman collections, public SDK docs

## Review-mode routing

For production review, include `$alaa-security-review` and `$alaa-observability-soc` by default unless the change is purely textual and has no runtime, trust, or operational surface. Add the domain skills that own the touched code. Review findings may recommend wider refactors or design changes when they materially affect production quality, but mark them as out-of-scope unless they are blockers.

## Routing rule of thumb

- Start with `$alaa-workflow` for long-horizon coordination.
- Add exactly the domain skills that own the changed surfaces.
- If multiple domains are involved, plan the boundaries first, then route each phase or lane to the right skill.
- In the phase prompt pack, list mandatory skills per phase explicitly; optional skills may be added during execution when evidence requires them.
