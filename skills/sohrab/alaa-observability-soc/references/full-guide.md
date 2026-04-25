# Purpose

Make services operable under SLA, debuggable during incidents, and defensible when upstream or downstream systems fail.

This skill defines how to design and validate operational signals:
- logs
- metrics
- traces
- exceptions
- profiles
- alerts
- dashboards
- SOC evidence
- runbooks

The deterministic mental model is:

```text
Application services produce telemetry.
OpenTelemetry standardizes telemetry.
The OpenTelemetry Collector receives, processes, batches, retries, redacts, routes, and exports telemetry.
SigNoz is the main observability backend.
Sentry is a focused error, release, source-map, and developer-debugging tool.
Prometheus-compatible metrics support health, SLOs, dashboards, and alerts.
```

# When to use

- Adding or updating logs, metrics, traces, dashboards, or alerts
- Writing or updating runbooks, SOPs, SLA, or SLO guidance
- Integrating with SOC or SIEM workflows and security event catalogs
- Incident or availability analysis and evidence collection
- Deciding between logs, metrics, traces, exceptions, and profiles
- Designing OpenTelemetry, OTLP, Collector, SigNoz, Sentry, or Prometheus behavior
- Enabling or hardening Sentry error tracking, tracing, releases, source maps, or profiling

# Ownership and precedence

This skill owns signal decisions and operator/SOC quality rules.

For Ala service repositories, pair with `$alaa-services-contract`.

Precedence:
- `$alaa-services-contract` owns exact Ala headers, response behavior, route contracts, metric names, event/code names, trusted-ingress behavior, deployment topology, and service-boundary rules.
- This skill owns why each signal exists, what each tool is for, how to avoid noisy or unsafe telemetry, and what evidence operators need.
- If a target repo already has a deployed log schema, do not rename fields casually. Add compatible fields or a documented migration path.

# Step-by-step workflow (deterministic)

1. Identify the operational question.
2. Select the primary signal.
3. Inventory existing signal names, fields, dashboards, alerts, and runbooks.
4. Define the signal contract: schema, semantics, cardinality, privacy, retention, and owner.
5. Decide where the signal flows: stdout, OTLP, Prometheus scrape, Collector, SigNoz, Sentry, SIEM, or another approved backend.
6. Update implementation and docs together.
7. Validate end-to-end: emit -> ship -> receive -> query -> alert/runbook.
8. Report validation evidence and remaining blind spots.

# Signal decision matrix

| Question | Primary signal | Secondary signal |
|----------|----------------|------------------|
| What happened in detail? | logs | trace attributes |
| Is the service healthy? | metrics | readiness logs |
| Should a human be alerted? | metrics and alert rules | logs and runbook |
| Where did one request go? | traces | logs with `trace_id` |
| Which code crashed? | exceptions | logs and traces |
| Which errors are new after deploy? | Sentry issues and releases | SigNoz dashboards |
| Which service or dependency is slow? | traces and latency metrics | logs |
| Is the queue backing up? | queue metrics | worker logs and traces |
| Why is code expensive? | profiles | traces and metrics |

Rules:
- Use logs for detail and forensic context.
- Use metrics for health, trends, SLOs, and alerts.
- Use traces for one request or one job journey.
- Use exceptions for code failures and stack traces.
- Use profiles only when performance evidence is needed and sample rates are controlled.

# Platform tool roles

## OpenTelemetry

OpenTelemetry is the standard and toolkit for telemetry. It is not a dashboard.

Use it for:
- traces
- logs
- metrics when appropriate
- context propagation
- semantic conventions
- vendor-neutral OTLP export

## OpenTelemetry Collector

The Collector is the telemetry router and processing tier.

Use it for:
- receiving OTLP
- batching
- retries
- sending queues
- filtering
- redaction
- enrichment
- sampling
- backend routing
- fan-out
- keeping backend secrets out of application code

## SigNoz

SigNoz is the main observability backend for system behavior.

Use it for:
- traces
- logs
- metrics
- dashboards
- alerts
- service maps
- latency and error analysis
- correlating logs, traces, and metrics

## Sentry

Sentry is a focused application-error and developer-debugging tool.

Use it for:
- exception grouping
- stack traces
- first-seen and regression detection
- release tracking
- frontend source maps and debug IDs
- issue ownership and developer notifications
- profiling only when deliberately enabled

Do not make Sentry a second full observability source of truth when SigNoz and the Collector already own platform observability.

# OpenTelemetry and OTLP contract

Use official OpenTelemetry APIs, SDKs, exporters, and semantic conventions where practical.

Resource identity must be stable:
- `service.name`
- `service.version`
- `deployment.environment.name`
- runtime and host or Kubernetes resource attributes when useful and safe

OTLP endpoint configuration belongs in environment or deployment config, not hard-coded service code.

Recommended baseline:
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_EXPORTER_OTLP_PROTOCOL`
- `OTEL_EXPORTER_OTLP_HEADERS`
- `OTEL_EXPORTER_OTLP_TIMEOUT`
- signal-specific endpoint overrides only when the platform needs them

High-traffic Laravel and PHP services must separate event capture from export flushing:
- keep structured request logging full-fidelity when the service contract requires one log per request
- keep OTLP log and trace export batched, fail-open, circuit-breakered, and bounded by short transport/export timeouts
- use `OTEL_FLUSH_ON_OPERATION=true` only as a controlled full-fidelity verification switch
- never let a slow Collector block or materially slow the request hot path

Trace context rules:
- `traceparent` is the propagation header.
- `tracestate` and `baggage` are propagated when the platform uses them.
- Do not fail a request only because inbound trace context is malformed; generate or start a new context according to the platform contract.

Trace query rule:
- `trace_id` must be queryable without parsing `traceparent`.
- For spans, OTLP carries trace ID natively; do not duplicate it as a high-cardinality metric label.
- For OTLP logs, populate native log-record trace context when the exporter supports it and also keep a stable `trace_id` log attribute or field if the backend query model benefits from it.
- For structured JSON logs, include both `traceparent` when useful for propagation/debugging and `trace_id` for direct filtering.

# OpenTelemetry alignment (mandatory when OTel is used)

If the service uses OpenTelemetry:
- Use W3C Trace Context propagation across HTTP, RPC, queue, and worker boundaries.
- Prefer OpenTelemetry semantic conventions for HTTP, database, messaging, RPC, exceptions, logs, resources, and profiles.
- Do not invent local attribute names when semantic conventions already define one.
- Keep instrumentation fail-open unless the user explicitly requests fail-closed telemetry behavior.
- Never put secrets or unmasked PII into OTel attributes.

# Collector architecture

Default pattern:

```text
Services -> OpenTelemetry Collector Gateway -> SigNoz or approved backend
```

Larger pattern when justified:

```text
Services -> Agent Collector -> Gateway Collector -> SigNoz or approved backend
```

Rules:
- Start with a gateway Collector unless host-local collection or node-level collection is needed.
- Keep redaction, retries, batching, fan-out, and backend credentials in the Collector or deployment layer.
- Use `memory_limiter` and `batch` processors in production Collector pipelines where appropriate.
- Use exporter sending queues for network exporters.
- Monitor Collector self-telemetry, especially exporter queue size, send failures, dropped data, and memory pressure.
- Validate Collector config with the Collector's validation command when a config changes.
- Do not expose OTLP receivers or debug endpoints publicly by default.

# SigNoz and Sentry role split

Clean architecture:

```text
Services -> OTLP -> Collector -> SigNoz
Services -> Sentry SDK -> Sentry
Services -> /metrics -> Prometheus-compatible scraper/backend
```

Rules:
- Use SigNoz as the main operational truth for service health, logs, traces, metrics, dashboards, and alerts.
- Use Sentry for exception grouping, stack traces, releases, source maps, regressions, and developer workflow.
- If Sentry is absent, exceptions must still go to SigNoz through the OpenTelemetry path as span exception events and structured error logs.
- Do not duplicate full tracing, logs, metrics, and alert ownership across both tools without an explicit architecture decision.
- When Sentry tracing is enabled, use conservative sample rates and make sure it does not conflict with the OTel/SigNoz trace strategy.
- Sentry structured logs are beta in some SDKs; do not replace the platform log pipeline with Sentry logs unless the platform explicitly approves it.

# Cardinality budgets (mandatory)

Unbounded cardinality ruins metrics systems and makes alerts noisy.

## Metrics label allowlist (default)

Allowed labels should come from small, bounded sets:
- templated route name or route pattern
- HTTP method
- status code or status class
- service
- environment
- dependency name
- queue name
- job name
- operation
- outcome
- stable machine-readable code when bounded

Disallowed metric labels by default:
- `user_id`
- `project_id`
- tenant IDs
- request IDs
- trace IDs
- raw IPs
- emails
- phone numbers
- device IDs
- raw URLs
- query strings
- headers
- exception messages
- SQL text

Budget rules:
- Each label should be bounded.
- Avoid combining multiple medium-cardinality labels on one metric.
- Prefer logs and traces for per-user or per-request debugging.

## Trace attribute discipline

Traces can carry richer context than metrics, but still avoid secrets and raw PII.

Rules:
- Use semantic attributes when available.
- Use templated routes, not raw paths with IDs, as span names or route attributes.
- Use identifiers as span attributes only when they materially help debugging and policy allows it.
- Use safe query fingerprints instead of raw SQL.

# Mandatory logging standard (structured JSON)

Production operational logs must be structured JSON, not free-form text as the primary signal.

## Required fields (baseline)

Include at minimum:
- `timestamp`
- `level`
- `service`
- `service_version`
- `env`
- `event`
- `code`
- `request_id`
- `trace_id`
- `project_id` when available
- `user_id` when available and allowed
- `http.method` when request-related
- `http.route` or route name when request-related
- `http.status` when request-related
- `duration_ms` when measuring work

## Trace query fields

Logs and OTLP log records must make trace lookup cheap:
- include `trace_id` as its own field
- include `traceparent` when useful for propagation debugging or reconstructing parent/span flags
- map native OTLP LogRecord `traceId`, `spanId`, and flags when the pipeline builds OTLP log payloads directly
- do not put `trace_id` into metric labels

## Authz denials (403) - response + log alignment

When returning 403:
- respond with stable `code` and user-facing `message`
- log the same `code`
- log the ability, route, object type, or policy name only when safe and useful

## PII and secrets

Never log:
- passwords
- secrets
- full tokens
- full JWTs
- raw access bitmaps when sensitive
- full request bodies by default
- PII unless approved, minimized, and masked

Prefer:
- token `jti`
- short fingerprints
- stable internal codes
- aggregate counts

# Metrics guidance (SLA-friendly)

Metrics are for health, trends, dashboards, and alerts.

Recommended signals:
- request rate
- error rate
- latency p50, p95, p99
- database latency and failures
- queue depth or lag
- failed jobs
- worker restarts
- memory usage
- dependency timeouts
- readiness state

Rules:
- Use counters for totals.
- Use gauges for values that go up and down.
- Use histograms for latency.
- Avoid summaries for multi-instance service latency unless explicitly justified.
- Prefer pull-based Prometheus-compatible endpoints for long-lived services.
- Alerts must have thresholds, owners, and runbook links.

# Trace guidance

Traces are for request and job journeys.

Trace at minimum:
- incoming HTTP requests
- outgoing HTTP calls
- database query groups
- Redis/cache calls
- queue publish
- queue consume
- worker jobs
- external dependencies
- authorization or validation decisions when needed for diagnosis

Rules:
- Preserve valid inbound `traceparent`.
- Generate or start a new trace when missing or invalid according to the platform contract.
- Propagate trace context across async boundaries.
- Record exceptions on spans.
- Set span status on failures.
- Keep `trace_id` queryable in logs.

# Exceptions and Sentry

Exceptions are code failures with stack traces.

Exceptions must be observable even when Sentry is not installed.

Default rule:
- record exceptions on the active OpenTelemetry span when one exists
- emit a structured error log with `event`, `code`, `request_id`, `trace_id`, route or operation, exception type, and safe message
- export the span and log through OTLP to the Collector and SigNoz

Sentry is an optional specialized layer and is strongest for:
- grouping similar errors
- stack traces
- first seen and last seen times
- release regressions
- affected users or requests when policy allows
- frontend source maps and debug IDs
- issue assignment and developer workflow

Rules:
- Capture unhandled exceptions.
- Capture selected handled exceptions only when they are actionable.
- Do not make Sentry the only exception path.
- When Sentry is absent, SigNoz must still receive enough exception evidence to query by `trace_id`, `service.name`, `event`, `code`, exception type, and route or operation.
- Do not send secrets or private user data.
- Use `beforeSend` or equivalent SDK hooks to scrub sensitive data when needed.
- Keep `SENTRY_SEND_DEFAULT_PII=false` unless there is an explicit approved policy decision.
- Keep `SENTRY_RELEASE` and `SENTRY_ENVIRONMENT` set by build/deploy when Sentry is enabled.
- Keep Sentry tracing and profiling sample rates low unless explicitly validated.

# Profiling

Profiles answer why code is slow or expensive.

Use profiling when:
- trace and metrics evidence shows a real performance problem
- CPU, memory, or runtime cost needs deeper proof
- overhead and cost are acceptable

Rules:
- Do not enable high production profiling rates by default.
- Start disabled or very low sample rate.
- Document the owner, retention, cost expectation, and rollback switch.
- Pair with runtime-specific performance skills when the task changes hot paths.

# SOC deliverable: Security log catalog

Maintain a security log catalog for security-relevant events.

Each catalog entry should define:
- event name
- severity
- required fields
- detection intent
- dashboard or query owner
- alerting rule when applicable
- runbook link

Minimum recommended events:
- `auth.login.failed`
- `auth.token.invalid`
- `auth.context.invalid`
- `authz.denied`
- `rate_limit.exceeded`
- `input.validation.failed`
- `resource.access.suspicious`
- `service.readiness.failed`

# Evidence-first incident diagnostics

Collect evidence that separates app faults from infrastructure or upstream faults:
- exact time window
- request IDs
- trace IDs
- response status and code
- health and readiness outputs
- database connectivity and timeout evidence
- upstream 502 or 504 patterns
- queue depth and consumer health
- worker restarts and memory
- Collector exporter queue and send-failure metrics
- SigNoz query screenshots or saved query details when requested
- Sentry issue IDs when exception grouping is relevant

# Sentry integration (optional; production-friendly)

Use this section when the task is to standardize Sentry for Laravel, frontend, or other application runtimes.

## 1) Install packages

For Laravel:

```bash
composer require sentry/sentry-laravel
```

Use SDK-level packages only when the repo needs SDK features directly.

## 2) Laravel / Octane configuration

Do not commit real DSNs.

Example baseline:

```dotenv
SENTRY_DSN=https://publicKey@o0.ingest.sentry.io/0
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=app@1.2.3
SENTRY_SEND_DEFAULT_PII=false
SENTRY_TRACES_SAMPLE_RATE=0
SENTRY_PROFILES_SAMPLE_RATE=0
```

Octane and long-lived workers:
- Ensure Sentry scope/state does not leak between requests or jobs.
- Avoid request-scoped state in singletons or statics.
- Reset per-request or per-job context.

## 3) Tracing (distributed tracing)

Enable Sentry tracing only deliberately.

For high-throughput services:
- start at `0`
- move to a low sample rate only after overhead and duplication risks are reviewed
- prefer OTel/SigNoz as the platform tracing source of truth unless the platform explicitly chooses otherwise

## 4) Release tracking (CI-driven)

Inject release at build/deploy time:

```bash
export SENTRY_RELEASE="app@${GIT_SHA}"
```

Upload frontend source maps or debug IDs through CI when frontend Sentry is enabled. Keep upload tokens in CI secrets.

## 5) Profiling (cost-controlled)

Enable profiling only with a low sample rate and a rollback switch:

```dotenv
SENTRY_PROFILES_SAMPLE_RATE=0.01
```

Profiling usually depends on tracing being enabled first.

## 6) Compatibility with OpenTelemetry / W3C Trace Context

Preserve W3C trace context headers:
- `traceparent`
- `tracestate`
- `baggage`

Make `trace_id` queryable in logs even when `traceparent` is available.

## 7) Validation (minimum)

- Confirm outbound connectivity to Sentry when Sentry is enabled.
- Send one controlled test exception in a non-production-safe way.
- Confirm the event appears with the expected environment and release.
- Confirm sensitive fields are absent.
- Confirm Sentry traces/profiles are disabled or sampled at the intended rate.
- Confirm OTel/SigNoz remains the main observability path when both are present.

# Laravel 13 observability audit points

When the repository targets Laravel 13, explicitly review:
- queue-event listeners or alerts that still expect `JobAttempted::$exceptionOccurred` instead of `JobAttempted::$exception`
- queue saturation listeners that still read `QueueBusy::$connection` instead of `QueueBusy::$connectionName`
- CSRF deny logs, tests, or middleware exclusions that still reference `VerifyCsrfToken` or `ValidateCsrfToken` instead of `PreventRequestForgery`
- cache-related operational assumptions when object caching now requires explicit `cache.serializable_classes` allow-lists
- route-level telemetry or alert rules when domain route precedence changes could alter which handler or middleware now wins

# Output contract

When applying this skill, output:

1. What changed and why
2. Signal contract fields and semantics
3. Where signals are emitted and shipped
4. Runbook or SOP changes: detect -> mitigate -> verify -> rollback
5. Validation steps and expected outcomes
6. Operational risks and follow-ups

For reviews, lead with findings and classify them by severity.

# Anti-patterns

- Unstructured production logs
- Logging secrets, full tokens, or raw PII
- Debug spam in hot paths
- High-cardinality metric labels
- Alerts without thresholds, owners, or runbooks
- Dashboards without alert or incident use
- Sentry as a replacement for platform metrics and traces
- SigNoz as a replacement for exception grouping and release debugging
- Direct app-to-vendor fan-out when the Collector should own routing
- Hard-coded backend secrets in application code
- Parsing `traceparent` in every incident query because `trace_id` was not emitted separately
- Enabling high Sentry trace/profile sample rates in production without cost and overhead validation
