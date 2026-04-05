# Companion Skill Routing

`$alaa-workflow` owns orchestration. Use it together with the right domain skill.

## Always consider

- `$alaa-low-noise` for any non-trivial run that risks noisy logs, broad searches, or oversized diffs.

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

## Vue, Quasar, Vite, and frontend delivery

Use these when the task touches Vue or Quasar behavior, rendering, or deployment:

- `$alaa-frontend-developer`
- `$quasar-skill-packe`
- `$alaa-frontend-devops`
- `$alaa-frontend-doc-annotations`
- `$alaa-shaka-player`

Signals:

- `src/`, `quasar.config`, `vite.config`, SSR, hydration, PWA, player integration
- frontend CI, Dockerfile, compose, static delivery, edge caching

## Go, Node, Rust, and package boundaries

Use these when the task is language- or package-centric:

- `$alaa-golang`
- `$alaa-mono-package`
- `$vector-rust-observability-pipelines`

Signals:

- `go.mod`, `cmd/`, `internal/`, `pkg/`
- `package.json`, workspace packages, internal shared packages
- Vector configs, VRL, Rust-based telemetry pipelines

## Data, caching, messaging, and storage

Use these when the task touches data modeling or queue semantics:

- `$alaa-data-layer`
- `$alaa-async-messaging`
- `$alaa-mongodb-patterns`
- `$clickhouse-performance-schema-ops`

Signals:

- PostgreSQL schema or query changes
- Redis cache, lock, invalidation, or dedupe
- RabbitMQ jobs, DLQ, retries, poison-message handling
- ClickHouse ingestion, TTL, MergeTree design
- MongoDB collections, indexes, TTL, document bounds

## Infra, containers, Kubernetes, and delivery

Use these when runtime, packaging, or cluster surfaces change:

- `$alaa-docker-production`
- `$caas-arvan-kuber`
- `$alaa-haproxy`
- `$gitlab-ci-generator` / `$gitlab-ci-validator`
- `$dockerfile-generator` / `$dockerfile-validator`
- `$helm-generator` / `$helm-validator`
- `$k8s-debug`
- `$k8s-yaml-generator` / `$k8s-yaml-validator`
- `$terraform-generator` / `$terraform-validator`
- `$terragrunt-generator` / `$terragrunt-validator`
- `$ansible-generator` / `$ansible-validator`

Signals:

- `Dockerfile`, `compose.yml`, Swarm, rootless container behavior
- Kubernetes, OpenShift, namespace-only access, Helm charts
- HAProxy configs and trust boundaries
- GitLab CI/CD, runners, executors, delivery pipelines

## Observability, logging, and incident evidence

Use these when the task touches telemetry, traces, metrics, or query languages:

- `$alaa-observability-soc`
- `$fluentbit-generator` / `$fluentbit-validator`
- `$loki-config-generator`
- `$logql-generator`
- `$promql-generator` / `$promql-validator`

Signals:

- correlation IDs, alerts, traces, logs, dashboards, incident analysis
- Fluent Bit, Loki, Prometheus, LogQL, PromQL

## Docs, API collections, and user-facing artifacts

Use these when the task changes operational or API-facing documentation:

- `$alaa-docs-farsi`
- `$alaa-postman-collections`

Signals:

- `docs/`, runbooks, user-facing instructions, API summaries, Postman collections

## Routing rule of thumb

- Start with `$alaa-workflow` for long-horizon coordination.
- Add exactly the domain skills that own the changed surfaces.
- If multiple domains are involved, plan the boundaries first, then route each phase or lane to the right skill.
