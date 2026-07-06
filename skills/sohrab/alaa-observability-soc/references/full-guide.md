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

For Ala service repositories, pair with `/sohrab-skills:alaa-services-contract`.

Precedence:
- `/sohrab-skills:alaa-services-contract` owns exact Ala headers, response behavior, route contracts, metric names, event/code names, trusted-ingress behavior, deployment topology, and service-boundary rules.
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

# OpenTelemetry alignment (mandatory for every Alaa service)

Full, standard OpenTelemetry is a platform requirement, not an option. Every Alaa service emits all three signals - traces, metrics, and logs - over OTLP. A service that cannot emit standard OpenTelemetry is not production-ready. The older "only when OTel is used" reading is retired: OTel is always used.

Required of every service:
- Emit traces, metrics, and logs; do not ship a service with a missing signal.
- Use W3C Trace Context propagation across HTTP, RPC, queue, and worker boundaries.
- Carry stable resource identity on every signal: `service.name`, `service.version`, `deployment.environment.name`.
- Prefer OpenTelemetry semantic conventions for HTTP, database, messaging, RPC, exceptions, logs, resources, and profiles.
- Do not invent local attribute names when semantic conventions already define one.
- Emit latency histograms that carry exemplars (see "Exemplars and metric-to-trace correlation"), so an aggregate percentile can be traced to a concrete request.
- Keep instrumentation fail-open unless the user explicitly requests fail-closed telemetry behavior, so mandatory telemetry never becomes a mandatory outage.
- Never put secrets or unmasked PII into OTel attributes.

Definition of done (audit a service against this):
- all three signals leave the service over OTLP;
- `traceparent` is propagated across every HTTP/RPC/queue/worker hop;
- `/metrics` is exposed and its latency histograms carry exemplars;
- `trace_id` is queryable in logs without parsing `traceparent`;
- resource attributes are stable and correct per service and per customer environment.

# Collector architecture

Default pattern:

```text
Services -> OpenTelemetry Collector Gateway -> SigNoz or approved backend
```

Larger pattern when justified:

```text
Services -> Agent Collector -> Gateway Collector -> SigNoz or approved backend
```

Alaa platform default (per-application Vector sidecar, agent tier):

```text
application -> local Vector sidecar (localhost, one per pod/replica) -> central OpenTelemetry Collector (gateway, scaled) -> SigNoz / SOC
```

The application emits OTLP only to a Vector running beside it and knows nothing about where the central Collector lives. See "Per-application Vector sidecar collection" for the full rationale and deployment shapes.

Rules:
- Start with a gateway Collector; use the per-application Vector sidecar as the agent tier so applications are decoupled from backend location and central back-pressure never reaches the request hot path.
- Keep redaction, retries, batching, fan-out, and backend credentials in the Collector or deployment layer.
- Use `memory_limiter` and `batch` processors in production Collector pipelines where appropriate.
- Use exporter sending queues for network exporters, and disk buffering at the sidecar so a central-Collector outage is absorbed locally.
- Run the central gateway Collector horizontally scaled behind a load balancer so it is never a single bottleneck (see "The central Collector must never become a bottleneck").
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

Can Sentry become "just an OTLP destination" behind the Collector? (dated: 2026-07; version-sensitive - recheck the source map)
- Sentry now ingests OTLP for traces and logs, via the Collector's `otlphttp`/Sentry exporter. This is open beta and single-project by default; multi-project routing (per customer/service) needs the Collector routing connector.
- OTLP does NOT carry errors to Sentry. Sentry's own docs state that only the Sentry SDK captures backend exceptions and links them to the trace. Error grouping, first-seen/regression, source maps/debug IDs, and release health also require the SDK.
- Therefore do not delete the Sentry SDK to make Sentry a pure OTLP sink. Keep the split: OTel/Collector/SigNoz own traces/metrics/logs; the Sentry SDK owns exception grouping and developer workflow where its value is real (backend services with meaningful regressions, plus the frontend source maps/replay).
- Reason the errors caveat matters: an unhandled exception is by definition unhandled. If it occurs inside an active span, the platform records a span exception event and a structured error log over OTLP, so SigNoz has evidence even with Sentry off. But a failure with no active span (boot, a worker crash, a panic outside a request) may never reach the Collector - which is exactly why a dedicated capture path (the SDK, or an explicit crash hook) still matters.

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
- Use histograms for latency, never averages - averages hide the tail. Define latency SLOs and alerts on percentiles (p95/p99); see "Latency percentiles".
- Latency histograms must carry exemplars so a slow percentile bucket links to a concrete `trace_id`; see "Exemplars and metric-to-trace correlation". This is mandatory, not optional.
- Avoid summaries for multi-instance service latency unless explicitly justified - summary quantiles cannot be aggregated across instances, histograms can.
- Prefer pull-based Prometheus-compatible endpoints for long-lived services, exposed as OpenMetrics so exemplars survive the scrape.
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
- Putting `trace_id` or `span_id` on a metric as a label instead of as an exemplar
- Latency histograms without exemplars, so a red percentile cannot be traced to a request
- Reasoning about latency with averages instead of percentiles
- Alerts without thresholds, owners, or runbooks
- Dashboards without alert or incident use
- Sentry as a replacement for platform metrics and traces
- SigNoz as a replacement for exception grouping and release debugging
- Deleting the Sentry SDK and expecting OTLP-to-Sentry to carry errors (it does not)
- Direct app-to-vendor fan-out when the Collector should own routing
- Application code that knows the central Collector address instead of emitting to its local sidecar
- Heavy trace processing (tail-sampling) at the per-app sidecar instead of the central Collector
- A single unscaled central Collector on the path of a high-concurrency site
- SOC egress wired as an inline dependency instead of a fan-out branch
- Hard-coded backend secrets in application code
- Parsing `traceparent` in every incident query because `trace_id` was not emitted separately
- Enabling high Sentry trace/profile sample rates in production without cost and overhead validation

# Latency percentiles

Reason about latency in percentiles, not averages. A percentile latency answers "what latency were the slowest X% of requests at or below?" p99 = 500 ms means 99% of requests finished within 500 ms and the slowest 1% were worse. Averages hide this: a service can look healthy on average while its p99 times out for one request in a hundred - which at high traffic is thousands of users. Define latency SLOs and alerts on percentiles (usually p95 and p99), and use histograms as the instrument because percentiles can be computed from them at query time and histograms are what carry exemplars.

| Percentile | Reading | What it tells you | Typical use |
|---|---|---|---|
| p50 (median) | half of requests are faster than this | the typical experience | baseline health, capacity trend |
| p90 | 90% faster than this | start of the slow tail | early warning on degradation |
| p95 | 95% faster than this | common SLO target | user-facing latency SLOs and alerts |
| p99 | 99% faster; slowest 1% worse | the tail your unlucky users feel | strict SLOs, bottleneck hunting |
| p99.9 | 99.9% faster than this | rare but real worst case | high-traffic services where 0.1% is still many requests |

Rules:
- Do not aggregate averages or summary quantiles across instances; aggregate histograms and compute the percentile at query time.
- When a percentile alert fires, do not stop at the number - follow the histogram bucket's exemplar to the trace (next section).

# Exemplars and metric-to-trace correlation

This is the mechanism that answers the platform's core operational question: "the p99 latency panel is red - which exact request caused it, and where did the time go?" Metrics are pulled by Prometheus on their own schedule and traces are pushed over OTLP, so they look disconnected. An exemplar is what connects them.

What an exemplar is: a small sample attached to a metric point - most usefully to one bucket of a latency histogram - that carries the `trace_id` (and often `span_id`) of a representative request that landed in that bucket. So when a bucket goes slow, its exemplar hands you a concrete `trace_id` you open directly in SigNoz. Crucially, the `trace_id` rides *inside* the metric as an exemplar, not as a metric label. This is the only cardinality-safe bridge: a `trace_id` label would create a new time series per request and destroy the metrics system, which is why the cardinality rules forbid it. Exemplars give you the same navigation without the cardinality cost.

Enabling requirements:
- Instrument latency as histograms and record exemplars on them.
- Expose metrics as OpenMetrics with exemplar storage enabled on the scrape path, or emit OTLP metrics that carry exemplars on the push path.
- This is mandatory for every service (see the OpenTelemetry alignment definition of done).

The complementary path (SigNoz span-metrics): the Collector's `spanmetrics` connector derives rate/error/duration (RED) metrics directly from traces, so those metrics and the traces share the same service and operation identity. This gives a service-map RED view you can pivot from a metric straight into the underlying traces, without hand-linking anything.

Bottleneck workflow (teach this explicitly):
1. Open the latency panel and find the slow percentile bucket (p95/p99).
2. Follow that bucket's exemplar `trace_id`.
3. Open the trace in SigNoz.
4. Read the span tree - the slow span (DB, Redis, provider, downstream service) is the bottleneck.
5. Fix at the source, then confirm the percentile recovers.

Rule of thumb: traces are the primary bottleneck tool; exemplars and span-metrics are how you get from an aggregate chart down to the one trace. Keep high-cardinality identifiers in traces and logs, keep metric labels bounded, and link the two through exemplars. To actually write the SigNoz ClickHouse query for a percentile panel or the metric-to-trace lookup, hand off to `$alaa-signoz-clickhouse-docs`.

# Per-application Vector sidecar collection

Platform default topology: every application emits its OTLP data only to a lightweight Vector running beside it (one per pod/replica, reached over localhost), and the application knows nothing about where the central OpenTelemetry Collector lives or how delivery happens. The local Vector owns the forward to the central Collector.

```text
application -> local Vector sidecar (localhost) -> central OpenTelemetry Collector (gateway, scaled) -> SigNoz / SOC
```

Why this is the right design:
- It fully decouples the application from backend location and availability; the app's only responsibility is "fire OTLP at localhost and forget."
- Each replica has its own buffer, so a slow or restarting central Collector cannot back-pressure the request hot path.
- It scales naturally: every new pod brings its own sidecar, with no shared contention between pods.
- It gives a natural per-application place to pre-filter or shape data, including SOC pre-filtering (see "SOC / SIEM egress").
- It is the concrete realization of the Agent Collector to Gateway Collector two-tier pattern, with Vector as the agent tier.

Deployment shapes:
- Kubernetes / OpenShift: a sidecar container in the same pod, sharing the network namespace; the app targets `localhost:4318`.
- Docker Swarm / Compose: a co-located Vector service on the shared network, or a baked binary - but a baked binary means two processes in one container, which requires a proper process supervisor and carries the documented trade-offs of that pattern.

Rules:
- The sidecar buffers to disk and forwards with retry so it absorbs central-Collector outages.
- Heavy trace processing such as tail-sampling belongs at the central Collector, not the sidecar; Vector's trace handling is forward/shape-oriented.
- The application never carries the central Collector address.

# The central Collector must never become a bottleneck

Because every service and every sidecar forwards into the central Collector, treat "the Collector is not a single point of congestion" as a first-class design rule. Defend it on four layers:

1. Application export is always asynchronous, batched, fail-open, and bounded by short timeouts - a slow Collector must never slow a request.
2. The per-application Vector sidecar buffers locally, so the app never feels central back-pressure.
3. The central Collector runs horizontally scaled behind a load balancer with `memory_limiter`, `batch`, sending-queue, and retry processors, plus sampling to bound trace volume.
4. The Collector's own self-telemetry (exporter queue size, send failures, dropped spans, memory pressure) is monitored and alerted.

The Collector is a deployed, sized runtime component included in the per-customer deploy artifacts, not a build-time step. Review its capacity as part of onboarding a high-traffic customer.

# SOC / SIEM egress

Some customers run a SOC/SIEM server and want specific rule-matched security events forwarded to it. Make this a standard pipeline branch, not a per-customer improvisation. (Note: a Vector that converts syslog to OTLP and ships it to the Collector is a telemetry-ingest adapter, not a SOC sink - SOC egress must be an explicit, dedicated branch.)

How it works:
- SOC forwarding is a filtered fan-out branch (a Vector sink or a Collector exporter) that selects only the rule-matched security events from the security log catalog and forwards them.
- Common SOC ingestion formats/protocols: syslog RFC5424, CEF, LEEF over TCP/TLS, OTLP, or Kafka/HTTP.
- From the customer, request only three things: the SOC endpoint, the required format/protocol, and the rule/event set. Their "rules" become filter conditions in the pipeline config.
- SOC egress must never block or degrade the primary SigNoz path; it is a fan-out branch, not an inline dependency.

# Collector selection (OTel Collector vs Vector vs Grafana Alloy)

| Tier | Tool | Why |
|---|---|---|
| Central gateway | OpenTelemetry Collector (contrib) | CNCF reference; most flexible; hundreds of receivers/processors/exporters; best trace processing; vendor-neutral |
| Edge sidecar, log-shaping, SOC egress | Vector | Rust, fast, low memory, strong transforms (VRL); already used in gateway and wa |
| - | Grafana Alloy | Only for a Grafana-native stack (Prometheus remote-write, Loki, Pyroscope); not our fit since the platform standardizes on SigNoz |

Default: central = OpenTelemetry Collector, edge = Vector, Alloy not used unless a customer mandates Grafana. This choice is version-sensitive; recheck the source map when a customer has an unusual constraint.

# Working with the SigNoz execution skill

This skill owns the design and reasoning: the signal model, exemplars, latency percentiles, SOC evidence, cardinality budgets, the Sentry role, and the Collector mental model. `$alaa-signoz-clickhouse-docs` owns execution against SigNoz: picking the right SigNoz docs page and writing or repairing the ClickHouse queries for dashboard panels (the p99 latency panel, the metric-to-trace exemplar lookup, the service-map RED view) and the missing-spans anti-join.

Hand off to `$alaa-signoz-clickhouse-docs` when the task becomes writing an actual SigNoz query or choosing a SigNoz docs page. Expect that skill to defer back here when a query task raises a design question (why exemplars, cardinality budgets, signal choice, SOC evidence). Keep the shared vocabulary aligned: `trace_id`/`span_id`, exemplars, and the percentile fields are described the same way in both skills.

# 2026 security-sensitive additions

Use these additions alongside the earlier guidance when the target system is production, customer-facing, regulated, or incident/security sensitive.

## Profiles signal positioning

OpenTelemetry semantic conventions include profiles, but Alaa does not treat continuous profiling as a universal minimum for every service in every environment. Use profiling when runtime cost, sampling policy, data sensitivity, and backend support are acceptable and the task involves CPU/memory contention, tail latency, allocator pressure, long-lived workers, or Sentry/SigNoz profiling workflows.

Profiles must follow the same privacy and operational rules as other signals: no secrets, no customer-private content, bounded retention, clear owner, cost controls, and a documented disable path.

## Service readiness evidence

A service is observability-ready only when the evidence exists in the repo, tests, or live telemetry:

- Traces: inbound server spans, outbound dependency spans, error status, operation names based on route templates, and propagated `traceparent`.
- Metrics: request rate, error rate, latency histogram, p50/p90/p95/p99 panels or equivalent queries, and resource/saturation metrics where relevant.
- Logs: structured JSON, UTC timestamps, `service.name`, environment, request ID, `trace_id`, bounded event names, result/error codes, and no secrets/PII.
- Exemplars: latency histograms that let an operator move from a percentile spike to representative traces, or a documented equivalent trace-linking workflow.
- Alerts: owner, severity, threshold, evaluation window, no-data behavior, runbook, and dashboard/log/trace links.
- Pipeline: Collector/Vector config validates, self-telemetry is visible, queues/retries are monitored, and critical remote hops have persistent buffering or an explicitly accepted loss profile.
- Drill: one controlled failure produces correlated metric, trace, log, alert, and SOC evidence when the event is security relevant.

## Collector and Vector resilience validation

For local sidecar/agent and central Collector patterns, validate each network hop separately:

- application to local endpoint: short timeouts, bounded memory, fail-open behavior, and no synchronous dependency on backend availability
- local Vector/Collector to central Collector: queue size, retry policy, disk buffer or persistent queue where needed, TLS, authentication, and self-telemetry
- central Collector to SigNoz/Sentry/SOC: bounded fan-out, isolated exporter queues, retry/drop/dead-letter behavior, and alerting on export failures

When a Collector branch is for SOC/SIEM export, failure of that branch must not block SigNoz observability or application traffic. Prefer independent exporters/queues and explicit loss/replay behavior.

## Safe SOC/SIEM forwarding model

Do not forward raw application logs wholesale to a customer SOC endpoint by default. Build a curated security-event catalog with a schema version, event category/action, decision, reason code, actor reference, resource reference, customer/tenant routing rule, trace/request correlation, and redaction policy.

A SOC/SIEM egress design is blocked until it defines transport security, endpoint authentication, credential rotation, retry/replay/dead-letter behavior, delivery-failure alerting, and a test event that the customer can verify safely.

## Source freshness and model-runtime note

When this skill itself is edited, use `references/95-model-runtime-compatibility.md`. Keep skill instructions portable across Codex/GPT-5.5 and Claude Opus/Sonnet/Fable runtimes. Do not hardcode model-specific API parameters or data-retention assumptions into ordinary observability guidance; put those in runtime/harness configuration or the compatibility reference.
