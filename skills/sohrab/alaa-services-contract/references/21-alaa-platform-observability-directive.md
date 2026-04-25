# Alaa Platform Observability Directive

Use this file when the task includes telemetry architecture, OpenTelemetry exporter setup, OTLP endpoint ownership, queryable `trace_id`, Collector gateway design, SigNoz, Sentry, exception delivery, Prometheus scrape endpoints, metric catalogs, queue or dependency instrumentation, Vector pipelines, OpenFGA telemetry, or cross-runtime observability alignment between Go, Laravel, HAProxy, Vector, WA, OpenFGA, and future services.

## Contract posture

This directive extends `20-operational-and-observability-contract.md`.

Working rule:
- apply `20-operational-and-observability-contract.md` and this file together for observability work
- `20` owns the exact stable surfaces such as response headers, event names, machine-readable codes, and middleware invariants
- this file owns the larger telemetry design, OTLP path, Collector gateway rules, Prometheus contract, and validation expectations
- pair with `$alaa-observability-soc` for the signal decision model, SOC evidence, alert/runbook rules, Sentry role, and SigNoz/Sentry split
- pair with `$vector-rust-observability-pipelines` when Vector topology, VRL transforms, buffering, acknowledgements, or log-to-OTLP conversion are in scope
- pair with `$alaa-trust-gateway-auth` when trusted headers, request-time authorization, or gateway-derived identity affect telemetry
- pair with `$openfga` when the work changes OpenFGA model, tuple, permission, SDK, or test behavior rather than only observing OpenFGA as a runtime dependency

## Why this directive exists

The Ala platform needs one stable observability shape across services so operators can answer the same questions quickly everywhere:
- what happened
- where it happened
- why it failed or slowed down
- whether the root cause is local, upstream, downstream, or infrastructure-related
- which routes, jobs, queries, and code paths need attention

This directive exists to make that outcome repeatable across:
- Go services
- PHP and Laravel services
- gateway-adjacent components
- queue workers and background consumers
- entitlement control-plane components such as `entitlement-api` and `projector`
- future services such as `notification-core`, `realtime-hub`, and delivery workers
- in-development services such as `assessment` and `notification`

## How this fits the Ala platform

Treat the platform like this:
- public clients call the gateway
- the gateway authenticates requests, strips spoofed internal headers, injects trusted identity and project context, and routes the request
- when a route family needs request-time fine-grained authorization, the gateway calls `authz-sidecar` or `entitlement-spoa`
- backend services still own request normalization, business validation, business authorization, response shaping, and service-local observability
- `entitlement-api` owns normalized authorization business truth
- `projector` writes derived tuples
- OpenFGA stores the derived authorization graph used for fast request-time checks
- `content` is the new macroservice for `course`, `set`, and `content`
- `vod` still exists during migration but is on the deprecation path for learning-content ownership
- `notification` is in development and must converge on the same request correlation, exception, log, metric, and Collector rules before production readiness
- `assessment` is treated as a future Ala service in this contract until a local repository provides stricter source truth
- `wa` is a Vector and ClickHouse ingestion runtime, so apply the same trusted-header, request-id, SOC evidence, and operational visibility goals without forcing Laravel or Go middleware shapes onto it

Observability must respect those boundaries:
- gateway telemetry must explain trust-boundary behavior
- authz-runtime telemetry must explain route-time allow or deny behavior
- service telemetry must explain work done inside the service boundary
- entitlement control-plane telemetry must explain derived-state maintenance, not pretend to be the source of business truth
- WA telemetry must explain ingest acceptance, Vector parsing/routing, drop reasons, ClickHouse sink state, and stored raw analytics rows
- OpenFGA telemetry must be described as native runtime telemetry for the derived authorization graph, not as the business source of truth

## Current Ala service reality

Use this table as a starting point, then re-check the target repository before editing because repo truth wins.

| Service or repo | Current shape to preserve |
|-----------------|---------------------------|
| `auth` | Laravel token-issuer boundary. Uses `X-Request-Id`, `traceparent`, structured logs, OTLP traces/logs, and internal `/metrics`. Do not let observability work reshape token, refresh, session, profile, admin, or TOTP behavior. |
| `ticket` | Laravel service with Sentry present, OTel/Prometheus rollout, root internal `/metrics`, and exact `X-Request-Id` plus `traceparent` response contract. Sentry may remain for exception tracking but does not replace OTel/SigNoz/Prometheus. |
| `comment-service` | Laravel service with canonical `APP_NAME=comment`, OTel traces/logs, Prometheus `/metrics`, and docs that explicitly keep metrics scrape-based. |
| `content` | Laravel macroservice for course, set, and content. Uses manual OTel traces/logs, Prometheus `/metrics`, and outbox rows carrying `request_id` and `traceparent`; AMQP trace headers may require driver extension work. |
| `gateway` | HAProxy gateway. HAProxy owns request serving, trusted-header injection, trace context preservation/generation, and built-in Prometheus metrics at internal `:8404/metrics`. Vector owns optional log parsing, PII guard, buffering, and OTLP log export. Gateway does not currently emit app spans just because it propagates trace context. |
| `entitlement-platform` | Go services `entitlement-api`, `projector`, and `authz-sidecar` use OTel tracing and Prometheus metrics. OpenFGA uses native OTLP/gRPC and native Prometheus metrics. Logs are structured JSON; OTLP log export may be intentionally deferred per repo truth. |
| `wa` | Vector plus ClickHouse ingestion runtime. Canonical routes are `POST /ingest/v1/events` and `GET /health`; trusted headers include `X-Project-Id`, `X-Request-Id`, and optional `X-User-Id`. Apply Vector pipeline reliability and internal metrics rules instead of Laravel middleware rules. |
| `notification` | In-development Laravel service. It already uses `X-Request-Id`, `traceparent`, request observability middleware, and Sentry scaffolding. It must converge on the full OTel/Prometheus/SigNoz contract before production readiness. |
| `assessment` | Future or absent in this local workspace during this rewrite. Apply the generic Ala service contract until repo-local source truth exists. |

Rules:
- never flatten these runtime differences into one implementation template
- keep the outcome consistent even when implementation mechanisms differ
- do not invent a new observability route, header, event, metric family, or backend role for a repo when the platform contract already defines one

## Platform direction

Every long-lived Ala service must:
- produce standard telemetry with official OpenTelemetry and Prometheus libraries
- send traces and logs to an OTLP endpoint
- expose a Prometheus-compatible internal metrics endpoint for scraping
- stay vendor-neutral in application code
- capture exception evidence even when Sentry is not present
- make `trace_id` directly queryable anywhere operators query logs or OTLP log records

The platform direction is:
- application code produces correct telemetry
- Collector tiers receive, process, batch, retry, route, redact, transform, and fan out telemetry
- Prometheus scrapes service metrics from internal endpoints
- backends can change later by configuration without redesigning each service

The current Ala target architecture is:
- application services send OpenTelemetry traces, exception evidence, and structured logs to a gateway OpenTelemetry Collector endpoint
- application services expose Prometheus-compatible metrics endpoints; metrics are first-class and must not be skipped when tracing is added
- the gateway Collector exports to SigNoz or another approved backend through Collector configuration
- SigNoz tokens, endpoints, and exporter-specific headers belong in Collector or deployment secrets, not application code
- Sentry may be added for exception grouping, stack traces, releases, source maps, and developer workflow, but it is not required for exceptions to be observable
- when Sentry is absent, exception spans and structured exception logs must still reach SigNoz through the OTLP Collector path

### What goes where

Use this ownership table to avoid moving platform concerns into application code:

| Data type                           | App code        | OTel Collector          | SigNoz / metrics backend | Sentry |
|-------------------------------------|-----------------|-------------------------|---------------------------|--------|
| traces                              | yes             | receive/process/export  | yes                       | optional, not source of truth |
| exceptions                          | record on spans and logs | receive/process/export | yes, required when Sentry absent | optional specialized grouping |
| structured logs                     | yes             | collect/process/export  | yes                       | optional only if approved |
| Prometheus metrics                  | expose endpoint | scrape/forward optional | yes                       | no |
| retry/compression/fan-out/redaction | no by default   | yes                     | no                        | no |

Rules:
- keep telemetry endpoint configuration in env or deployment config
- do not hard-code backend-specific behavior in service code
- do not build custom multi-backend fan-out, retry queues, compression, or redaction pipelines inside application code unless the platform explicitly approves an exception
- do not replace the Prometheus scrape contract with ad hoc pushing for normal services
- do not use the Pushgateway for normal long-lived service metrics; only use it for explicit service-level batch-job cases when the lifecycle is intentionally decoupled from individual instances
- do not deliver "tracing only" observability; metrics, logs, traces, and exceptions are all part of done
- do not deliver "Sentry only" exception visibility; exceptions must also be visible through the platform OTel/SigNoz path when Sentry is absent or disabled

## OpenTelemetry SDK and OTLP rules

### Resource identity

Use standard OTel resource identity consistently:
- `service.name` must match the Ala service name
- `service.version` should come from the build or release version
- `deployment.environment.name` should come from the deployment environment
- add other resource attributes only when they are stable, useful, and policy-safe

Real resource identifiers belong in the right signal:
- use real identifiers in structured logs and trace attributes when they are needed for debugging and allowed by data-protection policy
- examples include `request_id`, `project_id`, `user_id`, `content_id`, `set_id`, `ticket_id`, or an upstream dependency request id
- real resource identifiers MUST NOT appear as Prometheus metric labels
- use bounded metric labels such as route pattern, operation, dependency, status class, code, queue, job name, and outcome
- `trace_id` is special: it is high-cardinality and must not be a normal metric label, but it must be directly queryable in structured logs and OTLP log records

### Trace queryability

`traceparent` is the propagation contract, not the only query field.

Rules:
- keep `traceparent` as the W3C context carrier across HTTP, RPC, queue, and worker boundaries
- derive `trace_id` from the canonical trace context once at the request or job boundary
- include `trace_id` as a first-class structured log field
- when exporting OTLP logs, populate native trace context fields when supported by the exporter or pipeline
- when building OTLP LogRecord payloads manually or through Vector, set native `traceId`, `spanId`, and trace flags from `traceparent`
- keep `traceparent` as an additional field only when useful for debugging propagation, parent/span id, or sampled flag behavior
- never require operators to parse `traceparent` during normal incident queries
- never add `trace_id` to Prometheus metric labels; use exemplars if the metrics stack supports trace linking

### Configuration rules

Keep OTLP configuration externalized. The common baseline is:
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_EXPORTER_OTLP_PROTOCOL`
- `OTEL_EXPORTER_OTLP_HEADERS`
- `OTEL_EXPORTER_OTLP_TIMEOUT`
- signal-specific overrides only when the platform actually needs different values for traces, metrics, or logs

Rules:
- keep a code-level configuration equivalent for any env-driven behavior
- do not require code edits to move from one backend or collector endpoint to another
- keep OTLP timeouts configurable, not hard-coded
- do not put secrets directly in source code
- default shared Docker Compose or Swarm service containers to the Collector DNS endpoint `http://otel-collector:4318`
- treat `host.docker.internal` as a local developer override only; do not commit it as the service default
- for Laravel or PHP long-lived workers, default to bounded scheduled flushing with `OTEL_SCHEDULED_FLUSH_ENABLED=true`
- keep `OTEL_FLUSH_ON_OPERATION=false` by default; enable it only for controlled full-fidelity verification that intentionally accepts operation-boundary export cost
- allow per-request structured logging to stay unsampled when the service contract requires it
- keep OTLP log and trace export batched, fail-open, circuit-breakered, and bounded so Collector problems do not degrade request latency
- express OTLP/exporter timeout defaults in milliseconds; use `OTEL_EXPORTER_OTLP_TIMEOUT=500`, `OTEL_BSP_EXPORT_TIMEOUT=500`, and `OTEL_BLRP_EXPORT_TIMEOUT=500` for high-traffic Laravel local runtime fallbacks unless production telemetry SLOs justify explicit different values

### Package guidance

Use explicit, vendor-neutral packages:

For Go:
- use official OpenTelemetry Go modules under `go.opentelemetry.io/otel` and `go.opentelemetry.io/contrib/...`
- use official OTLP exporters from the OpenTelemetry Go modules
- expose Prometheus metrics with the official Prometheus Go client `github.com/prometheus/client_golang/...`

For PHP and Laravel:
- the baseline Composer set for Ala PHP and Laravel services is `open-telemetry/api`, `open-telemetry/context`, `open-telemetry/sdk`, and `open-telemetry/exporter-otlp`
- application code and shared internal libraries should depend on classes and interfaces from `open-telemetry/api`; keep SDK, exporter, and provider wiring in bootstrap or infrastructure code
- treat `open-telemetry/context` as effectively baseline for real platform services because queues, workers, downstream HTTP calls, custom middleware, and manual boundaries need explicit context propagation when automatic propagation is not enough
- use the official Laravel auto-instrumentation package `open-telemetry/opentelemetry-auto-laravel` where auto-instrumentation is appropriate
- when using official PHP auto-instrumentation or zero-code instrumentation, install and enable the OpenTelemetry PHP extension, the SDK, and the needed instrumentation libraries; the extension by itself does not generate traces
- for a Laravel manual-instrumentation baseline, the expected Composer starting point is `composer require open-telemetry/api open-telemetry/context open-telemetry/sdk open-telemetry/exporter-otlp`
- for official Laravel auto-instrumentation, add `open-telemetry/opentelemetry-auto-laravel` and satisfy its `ext-opentelemetry` requirement instead of substituting an unrelated package
- because Ala platform observability includes structured logs, use the official `open-telemetry/opentelemetry-logger-monolog` package when sending Laravel Monolog records through the OpenTelemetry logging pipeline
- use only a platform-approved Prometheus-compatible metrics endpoint package for Laravel services
- do not treat third-party Laravel OpenTelemetry helpers as platform defaults; verify the exact package name, maintenance status, Octane behavior, and production readiness before approving one
- a helper such as `keepsuit/laravel-opentelemetry` may be approved as an optional app-level convenience layer for Laravel ergonomics, but it is not the canonical platform package contract
- do not cite `spatie/laravel-opentelemetry` as a canonical package name; as of 2026-04-21 verification, public package evidence points to `spatie/laravel-open-telemetry`, and that package must not be used as the platform default unless the platform explicitly re-approves it despite the maintenance and production-readiness warnings seen during verification

### Propagation rules

Preserve W3C context end-to-end:
- `traceparent`
- `tracestate`
- `baggage` when used

Apply this across:
- incoming HTTP
- outgoing HTTP
- gRPC or RPC calls
- message queues
- background jobs and consumers

Rules:
- preserve valid inbound `traceparent`
- do not fail the request only because an inbound `traceparent` is malformed
- continue the trace in consumers when context exists in message metadata
- when async context is absent, start a new trace and log the boundary clearly
- derive the logged `trace_id` from the canonical trace context
- export or map the same `trace_id` into OTLP logs so SigNoz log search can join with traces without parsing `traceparent`
- prefer OTel semantic conventions for HTTP, DB, messaging, and RPC rather than inventing local attribute names

## OpenTelemetry Collector gateway contract

### Baseline deployment pattern

The default platform pattern is a Collector gateway tier:
- applications or local agents send OTLP telemetry to a stable central endpoint
- one or more gateway collectors receive, process, and export telemetry
- the stable OTLP endpoint can exist per cluster, per region, or per environment
- the approved backend can be SigNoz, but applications must still target the Collector endpoint rather than a SigNoz-specific endpoint

In Kubernetes or OpenShift:
- use a Deployment for a gateway tier by default
- use a DaemonSet or other agent pattern only when host-level collection or a local hop is explicitly needed
- if the platform later adopts an agent-to-gateway design, keep agent configuration small and focused while gateways own heavier processing

For Ala teams that do not own cluster-wide infrastructure:
- target the stable platform-provided OTLP endpoint
- do not invent repo-local collector topologies unless a real blocker is documented

### Collector-owned responsibilities

The Collector tier owns:
- protocol termination for telemetry intake
- batching
- exporter retries
- sending queues
- durable buffering when required
- secure egress, authentication, and TLS
- attribute enrichment
- filtering and dropping
- redaction and masking
- transformation and normalization
- backend routing and fan-out
- SigNoz exporter configuration when SigNoz is the active backend
- centralized sampling policy
- Collector self-telemetry

The application tier does not own those concerns by default.

### Recommended processor placement

Rules:
- place `memory_limiter` first in the pipeline when used
- place `batch` after the work that changes or filters telemetry
- keep redaction, transform, and filter logic in the Collector when the goal is governance, cost control, or backend normalization
- keep tail sampling on gateway collectors only
- if probabilistic sampling is used across multiple collectors, keep the configuration consistent across them
- if tail sampling is used on multiple gateway instances, ensure trace-affinity routing so all spans for one trace reach the same sampling decision point

### Reliability rules

Collector reliability must be designed explicitly:
- use sending queues for exporters that cross a network
- tune queue size and retry windows according to expected data volume and acceptable downtime
- use persistent queue storage such as `file_storage` when losing queued telemetry on Collector restart is not acceptable
- monitor queue depth, queue capacity, and exporter failure metrics
- remember that WAL-style persistence improves resilience but is not a substitute for a dedicated message broker

### Security rules

Rules:
- store Collector secrets and credentials in a secret store, encrypted filesystem, or env expansion sourced from secret management
- use encryption and authentication on non-local network links
- minimize enabled components; do not enable receivers, exporters, or extensions that are not needed
- keep bind addresses private unless exposure is explicitly required
- do not expose OTLP receivers, debug endpoints, or health extensions on public interfaces by default
- treat 0.0.0.0 binds as an explicit choice to justify, not a casual default

### Collector observability

The Collector itself must be observable:
- collect internal Collector metrics
- expose internal metrics for scraping or forward them internally through OTLP according to the platform design
- keep a health endpoint or equivalent extension for operations
- use debug or local exporters only for controlled troubleshooting, not as a normal production sink

## Logging directive

All production service logs must be structured JSON.

Free-form text logs are not acceptable as the main production service log shape.

### Mandatory fields

At minimum, every operational log related to a request, job, readiness check, denial, or failure path must include:
- `timestamp`
- `level`
- `service`
- `service_version`
- `env`
- `event`
- `code`
- `request_id`
- `trace_id`
- `traceparent` when useful for propagation debugging or async handoff evidence
- `project_id` when available
- `user_id` when available and allowed
- `http.method` when request-related
- `http.route` or a stable route name when request-related
- `http.status` when request-related
- `duration_ms` when the log measures work over time

Keep these field names stable.

Trace field rule:
- `trace_id` is mandatory for query speed.
- `traceparent` is the propagation carrier and may also be logged, but it is not a substitute for a separate `trace_id`.
- Vector and other log-pipeline agents must preserve or map `trace_id` into the backend query model.

### Recommended additional fields

Use them when relevant:
- `operation`
- `component`
- `dependency`
- `queue`
- `job_name`
- `attempt`
- `db.system`
- `db.operation`
- `db.statement_fingerprint`
- `error.kind`
- `error.message`
- `error.stack`
- `outcome`

### Data-protection rules

Rules:
- do not log passwords
- do not log secrets
- do not log raw bearer tokens
- do not log full JWTs
- do not log raw `X-Access`
- do not log full request bodies unless a very specific audited flow explicitly allows it
- do not log PII unless an approved operational reason exists and the data is masked, minimized, or reduced

If token-level correlation is needed, prefer:
- token `jti`
- a short fingerprint
- a stable internal code

### Probe-noise rule

Do not emit low-value completion logs for successful:
- `/api/health`
- `/api/ready`

Still log:
- readiness failures
- unexpected health failures
- readiness recovery transitions when tracked

## Error capture and exception handling rules

### Core rule

Handle errors cleanly:
- either return them upward with context
- or handle and log them at the correct boundary

Do not keep logging and returning the same error repeatedly through the same chain.

### What must be observable

At minimum, capture:
- unhandled exceptions
- request-level failures
- queue or job failures
- downstream dependency failures
- database failures
- authorization denials that matter operationally
- validation failures at the correct aggregation level
- business-critical failures even when the user-facing response stays graceful

Exception routing rules:
- if Sentry is installed and enabled, send exception events to Sentry for grouping, release regression, stack-trace workflow, and developer assignment
- regardless of Sentry, record exceptions on active OTel spans when a span exists
- regardless of Sentry, emit structured exception logs with `trace_id`, `request_id`, `service`, `event`, `code`, route or operation, exception type, safe message, and stack trace when policy allows
- if Sentry is absent, the OTLP logs/traces to Collector -> SigNoz path becomes the required exception visibility path
- do not hide handled-but-actionable exceptions only because no Sentry DSN exists

### Required captured context

Whenever possible, include:
- `request_id`
- `trace_id`
- `project_id`
- `user_id` when safe
- route or operation name
- stable machine-readable `code`
- dependency name when a downstream system is involved
- retry attempt when relevant
- job name when relevant

### Runtime-specific rules

For Go services:
- return errors with context
- log structurally
- do not swallow errors
- do not log and return the same error repeatedly
- record the error in the span when work fails
- set span status correctly

For Laravel or PHP services:
- establish request correlation early in middleware
- make the exception handler return `X-Request-Id` and `traceparent` on rendered API error responses
- keep observability state request-scoped
- stay Octane-safe
- for workers and scheduled commands, establish fresh per-job or per-command context and reset any request-like state between units of work

## Trace instrumentation rules

Every service must trace enough work to reveal slow routes, slow dependencies, and expensive internal operations.

At minimum, traces must cover:
- incoming HTTP request
- middleware or request pipeline
- trusted-context normalization
- service-local authorization and validation steps when those are important to diagnosis
- outgoing dependency calls
- significant database operations or query groups
- queue publish
- queue consume
- long-running internal operations
- final response generation

### Route and operation naming

Never use raw paths with live IDs as the primary route identity.

Use:
- a stable route name
- or a templated route pattern

Good example:
- `/api/v2/course/{course_id}/set/{set_id}/content/{content_id}`

Bad example:
- `/api/v2/course/8472/set/99/content/4431`

### Trace attribute rules

Rules:
- prefer OTel semantic conventions for HTTP, DB, messaging, and RPC
- use stable operation names and bounded attributes
- do not use raw SQL text, raw tokens, or raw PII as general span attributes
- use real resource identifiers as span attributes only when they materially help debugging and are policy-safe
- never copy those identifiers into Prometheus labels
- if query-level grouping is needed, use a safe fingerprint
- make retry paths, timeout paths, and cancellation paths visible

### Async boundaries

For messaging and jobs:
- propagate trace context in message headers or metadata
- continue traces in consumers when possible
- include queue name, job name, attempt, and outcome in the span attributes when those values are bounded and policy-safe
- make dead-letter, retry, and nack behavior visible in traces and logs

## Prometheus scrape contract

Every long-lived Ala service must expose a Prometheus-compatible metrics endpoint.

Rules:
- the endpoint is internal, scrapeable, and production-ready
- it is not a public client API
- default to `/metrics` unless a repository already has a different internal path owned by platform contract
- keep exposure behind internal service discovery, internal ingress, or network policy as appropriate
- do not depend on Pushgateway for normal service metrics
- prefer Prometheus pull collection for normal service endpoints

### Metric design rules

Rules:
- use bounded labels only
- use explicit base units
- use counters for totals
- use gauges for values that can go down
- use histograms for latency distributions
- avoid summaries for multi-replica request latency unless there is a very specific justified exception
- if the monitoring stack has explicitly enabled and validated native histograms end-to-end, they may be rolled out deliberately; otherwise keep classic histograms with explicit buckets
- do not use raw user IDs, project IDs, request IDs, raw URLs, query strings, SQL text, exception text, email addresses, or phone numbers as labels
- do not use real resource identifiers such as content ids, set ids, ticket ids, order ids, token ids, or dependency request ids as labels
- prefer service-discovery or target labels for metadata such as service and environment when the platform already injects them, instead of duplicating the same dimensions in every metric

### Allowed label examples

Use these when relevant and bounded:
- `service`
- `env`
- `http_method`
- `http_route`
- `http_status_code`
- `http_status_class`
- `operation`
- `dependency`
- `queue`
- `job_name`
- `db_system`
- `db_operation`
- `outcome`

### Forbidden label examples

Do not use:
- `user_id`
- `project_id`
- `request_id`
- real content, set, ticket, order, token, or dependency request ids
- raw URL
- query string
- email
- phone
- token
- exception text
- SQL text

### Exemplars

If the stack supports exemplars:
- use them on latency histograms where they add real debugging value
- attach trace identifiers as exemplar data, not as normal metric labels
- keep exemplar usage deliberate and bounded

## Mandatory baseline metric catalog

All application metrics must use stable names and must not invent random per-repo naming styles.

### HTTP request metrics

Every HTTP service must expose:
- `alaa_http_requests_total`
  - Counter. Total number of HTTP requests.
- `alaa_http_request_duration_seconds`
  - Histogram. End-to-end request duration.
- `alaa_http_requests_in_flight`
  - Gauge. Current in-flight requests.
- `alaa_http_request_failures_total`
  - Counter. Failed request count.

Recommended labels:
- `http_method`
- `http_route`
- `http_status_code` or `http_status_class`
- `service` and `env` only when those are not already injected elsewhere

### Readiness and health metrics

Every service must expose:
- `alaa_service_ready`
  - Gauge. `1` when ready, `0` when not ready.
- `alaa_service_readiness_failures_total`
  - Counter. Readiness failures.
- `alaa_service_restarts_total`
  - Counter when available from the app boundary or local runtime tracking.

### Authorization and validation metrics

Where relevant, expose:
- `alaa_auth_context_invalid_total`
- `alaa_authz_denied_total`
- `alaa_input_validation_failed_total`
- `alaa_rate_limit_exceeded_total`

Recommended labels:
- `http_route`
- `code`
- `outcome`

### Database metrics

Every service that owns database access must expose enough metrics to show DB pressure and slow queries.

Required baseline:
- `alaa_db_queries_total`
- `alaa_db_query_duration_seconds`
- `alaa_db_query_failures_total`
- `alaa_db_connections_active`
- `alaa_db_pool_in_use`
- `alaa_db_pool_idle`

When supported safely, also expose:
- `alaa_db_transactions_total`
- `alaa_db_transaction_duration_seconds`
- `alaa_db_lock_wait_seconds`
- `alaa_db_deadlocks_total`

Recommended labels:
- `db_system`
- `db_operation`
- `outcome`

Do not use raw SQL text as a label.
If query-level grouping is needed, use a safe fingerprint.

### Downstream dependency metrics

Every service that calls other services or external systems must expose:
- `alaa_dependency_requests_total`
- `alaa_dependency_request_duration_seconds`
- `alaa_dependency_request_failures_total`
- `alaa_dependency_timeouts_total`

Recommended labels:
- `dependency`
- `operation`
- `outcome`

### Queue and async metrics

Any service that publishes or consumes async jobs must expose:
- `alaa_queue_messages_published_total`
- `alaa_queue_messages_consumed_total`
- `alaa_queue_message_failures_total`
- `alaa_queue_message_duration_seconds`
- `alaa_queue_retries_total`
- `alaa_queue_dead_letter_total`

If backlog visibility is owned by the service or safely available, also expose:
- `alaa_queue_backlog`
- `alaa_queue_consumer_lag_seconds`

Recommended labels:
- `queue`
- `job_name`
- `outcome`

### Worker and runtime metrics

For long-lived workers and background consumers, expose runtime health metrics.

Common baseline:
- `alaa_worker_jobs_in_progress`
- `alaa_worker_restarts_total`
- `alaa_worker_memory_bytes`

For Go services, also preserve or expose where relevant:
- goroutine count
- garbage-collection cycles
- garbage-collection pause duration
- heap usage

For Laravel or Octane services, also preserve or expose where relevant:
- Octane worker count
- worker restart count
- queue worker failure count
- queue busy signals
- long job execution time

### Business metrics

Each service must expose a small set of service-owned business metrics beyond the shared baseline.

Examples:
- auth service
  - `alaa_auth_login_attempts_total`
  - `alaa_auth_login_failures_total`
  - `alaa_auth_token_issued_total`
  - `alaa_auth_token_validation_failed_total`
- content or vod service
  - `alaa_content_requests_total`
  - `alaa_content_access_denied_total`
  - `alaa_video_playback_authorizations_total`
- comment service
  - `alaa_comment_created_total`
  - `alaa_comment_deleted_total`
  - `alaa_comment_moderation_actions_total`
- ticket service
  - `alaa_ticket_created_total`
  - `alaa_ticket_reply_created_total`
  - `alaa_ticket_status_changed_total`
- wa service
  - `alaa_watch_events_ingested_total`
  - `alaa_watch_ingest_failures_total`
  - `alaa_watch_pipeline_backpressure_total`

Rules:
- keep business metrics owned by the service that actually owns the behavior
- keep labels bounded
- do not invent large per-feature metric trees without a real operational need

## Runtime-specific implementation notes

### Laravel and PHP

Rules:
- establish request correlation early on `/api/*` traffic
- keep request-scoped observability state request-scoped and Octane-safe
- attach `X-Request-Id` and `traceparent` to success responses and rendered API error responses
- normalize trusted gateway headers once and do not re-parse them in controllers or policies
- treat each queue job, consumer loop unit, or scheduled command as a fresh unit of work with fresh context
- keep the Prometheus endpoint internal and low-noise
- keep logs structured and avoid multiline free-form stack traces as the primary production format
- remember that Octane keeps the Laravel application in memory between requests, so never keep request, user, span, baggage, or trusted-header state in long-lived statics or singletons without an explicit reset path
- do not claim the OpenTelemetry PHP extension is universally required for every possible Octane implementation; require it for official PHP auto-instrumentation or for any chosen package that depends on extension hooks, and evaluate manual instrumentation separately

### Go

Rules:
- apply the same contract through top-level HTTP middleware, router middleware, and gRPC interceptors when those exist
- preserve and propagate `context.Context`
- use a structured logger
- expose a Prometheus metrics endpoint
- record failed operations in spans
- keep error handling clean and non-duplicative
- in long-lived consumers, restore context from message metadata when available and clearly mark retry or dead-letter behavior

## Collector and Prometheus deployment notes for Ala

For Ala environments:
- on Kubernetes or OpenShift, prefer one shared Collector gateway tier per environment or per cluster boundary rather than embedding custom collector topologies into every service repository
- when using the official Collector Helm chart, choose the deployment mode intentionally; gateway tiers usually use `deployment`, while host-level or node-level collection usually points to `daemonset`
- keep metrics endpoints internal and scrape them through platform discovery or explicit scrape configuration
- keep the same contract in Docker Compose and Docker Swarm: OTLP to the shared collector endpoint, Prometheus scraping internal service metrics, and no public metrics endpoint
- when SigNoz is the selected backend, put SigNoz exporter endpoints, access tokens, headers, and TLS options only in the Collector deployment configuration or secrets

## Sentry contract

Sentry is allowed but scoped.

Use Sentry for:
- exception grouping
- stack traces
- first-seen and regression workflow
- releases
- frontend source maps or debug IDs
- developer notifications and ownership
- profiling only when deliberately sampled

Rules:
- Sentry is not the main Ala observability backend.
- Do not send normal service metrics only to Sentry.
- Do not make Sentry traces the only distributed trace path when the service is part of the Ala OTel/SigNoz platform.
- Do not make Sentry the only exception path.
- If Sentry is absent or disabled, exception spans and structured exception logs must still reach SigNoz through OTLP and the Collector.
- Keep `SENTRY_SEND_DEFAULT_PII=false` unless there is an explicit approved data policy.
- Keep Sentry trace and profile sample rates `0` or low until overhead, cost, and duplication with SigNoz are reviewed.
- Put Sentry auth tokens for source-map or release uploads in CI/CD secrets, not source files.

## Service adoption checklist

When applying this skill to a service, finish by checking:
- `/api/health`
- `/api/ready`
- `X-Request-Id`
- `traceparent`
- queryable `trace_id`
- structured JSON logs
- exact event/code naming
- exception evidence through Sentry when present and through SigNoz/OTLP always
- Prometheus endpoint and applicable baseline metric families
- bounded labels
- OTLP exporter endpoint via env
- no vendor-specific backend coupling

## Minimum validation checklist

A service is not considered observability-complete unless all of the following are true:
- it emits structured JSON logs in production
- it returns `X-Request-Id` and `traceparent` on `/api/*` responses
- it preserves valid inbound correlation and generates valid values when missing
- it propagates W3C trace context across HTTP and async boundaries
- it makes `trace_id` directly queryable in structured logs and OTLP log records
- it sends traces and logs through the OTLP path without backend-specific code branches
- it exposes a Prometheus-compatible internal metrics endpoint
- it provides the shared HTTP, readiness, dependency, DB, and queue metrics that apply to it
- it uses bounded labels only
- real resource identifiers appear only in logs or trace attributes when needed, never as metric labels
- OTLP exporter endpoint and protocol are controlled by env or deployment config
- no vendor-specific backend coupling exists in application code
- it captures readiness failures, request failures, queue failures, dependency failures, and important denials with enough context for diagnosis
- it captures exception evidence in SigNoz through OTel spans/logs when Sentry is absent, and in both SigNoz and Sentry when Sentry is deliberately enabled
- it makes slow routes, slow queries, slow dependencies, repeated retries, and repeated denials easy to identify
- its collector path is observable enough to show queue pressure, export failures, or dropped telemetry when those happen

## Anti-patterns

- building custom telemetry fan-out inside application code
- treating telemetry as optional after feature work is done
- treating Sentry as the only exception pipeline
- forcing operators to parse `traceparent` because `trace_id` is missing from logs
- using raw IDs or unbounded text as metric labels
- exposing the metrics endpoint as a public client API
- using Pushgateway for normal long-lived service metrics
- logging raw JWTs, raw `X-Access`, or secret values
- using raw paths with IDs as the primary route dimension
- using summaries for multi-replica HTTP latency when histograms are the correct platform choice
- applying tail sampling in the wrong place or without trace-affinity routing
- hiding collector queue pressure or exporter failures
- duplicating the same error log at every layer
- inventing repo-local event names or metric families that break platform dashboards and alerts
