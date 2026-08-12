# Alaa Platform Observability Names And Values

Use this file when the task needs an exact observability **name** or **value**: an `OTEL_*` environment
variable and its Ala default, a trace or route naming rule, an exception field name, the `/metrics` endpoint
facts, or the current telemetry shape of a specific Ala service. For a metric name, read
`24-metric-registry.md` instead; it owns every one.

## Ownership split, and it is binding

This skill owns every observability **name and value**. `$alaa-observability-soc` owns every **requirement
level, gate, threshold, and reason**.

- Here: log field names, `OTEL_*` variable names and their Ala default values, route and operation naming
  rules, exception field names, the `/metrics` endpoint facts, and the per-service reality table below.
  Metric family names moved to `24-metric-registry.md`; event and code names are owned by
  `20-operational-and-observability-contract.md`.
- There: whether a signal is required, which alert or SLO gate it feeds, Collector topology and processor
  placement, sampling policy, metric label allow and deny lists, resource-identity policy, exemplar
  requirement level, Sentry policy, and the data-retention and cardinality budgets.

When this file and `$alaa-observability-soc` appear to disagree about whether something is required, that
skill wins. When they appear to disagree about what something is called or what its default value is, this
file wins. Do not resolve such a disagreement by inventing a third answer.

Two more boundaries inside this skill:
- `20-operational-and-observability-contract.md` owns `X-Request-Id`, `traceparent`, `trace_id`, the
  structured log field list, event and code naming, the probe-noise rule, the metrics label boundary at the
  request middleware layer, and `RequestObservabilityMiddleware` including its middleware order. Read it
  there; it is not repeated here.
- `40-apply-checklist-and-anti-patterns.md` owns the adoption checklist, the validation checklist, and the
  anti-pattern list for this whole skill.

Also pair with `$vector-rust-observability-pipelines` for Vector topology, VRL transforms, buffering,
acknowledgements, and log-to-OTLP conversion; `$alaa-trust-gateway-auth` when trusted headers or
gateway-derived identity affect telemetry; `$openfga` when the work changes the OpenFGA model or tuples
rather than only observing OpenFGA as a dependency; and `$alaa-laravel-architecture` plus
`$alaa-php-clean-code` for which PHP or Composer observability packages to install, which this skill does
not decide.

## Current Ala service reality

Use this table as the starting point, then re-check the target repository before editing, because repo
truth wins over this table.

| Service or repo | Current shape to preserve |
|-----------------|---------------------------|
| `auth` | Laravel token-issuer boundary. Uses `X-Request-Id`, `traceparent`, structured logs, OTLP traces/logs, and internal `/metrics`. Do not let observability work reshape token, refresh, session, profile, admin, or TOTP behavior. |
| `ticket` | Laravel service with Sentry present, OTel/Prometheus rollout, root internal `/metrics`, and the exact `X-Request-Id` plus `traceparent` response contract. |
| `comment-service` | Laravel service with canonical `APP_NAME=comment`, OTel traces/logs, Prometheus `/metrics`, and docs that explicitly keep metrics scrape-based. |
| `content` | Laravel macroservice for course, set, and content. Uses manual OTel traces/logs, Prometheus `/metrics`, and outbox rows carrying `request_id` and `traceparent`; AMQP trace headers may require driver extension work. |
| `gateway` | HAProxy gateway. HAProxy owns request serving, trusted-header injection, trace context preservation and generation, and built-in Prometheus metrics at internal `:8404/metrics`. Vector owns optional log parsing, PII guard, buffering, and OTLP log export. The gateway does not emit app spans just because it propagates trace context. |
| `entitlement-platform` | Go services `entitlement-api`, `projector`, and `authz-sidecar` use OTel tracing and Prometheus metrics. OpenFGA uses native OTLP/gRPC and native Prometheus metrics. Logs are structured JSON; OTLP log export may be intentionally deferred per repo truth. |
| `wa` | Vector plus ClickHouse ingestion runtime. Canonical routes are `POST /ingest/v1/events` and `GET /health`; trusted headers include `X-Project-Id`, `X-Request-Id`, and optional `X-User-Id`. Apply Vector pipeline rules, not Laravel middleware rules. |
| `notification` | In-development Laravel service. It already uses `X-Request-Id`, `traceparent`, request observability middleware, and Sentry scaffolding, and must converge on the full contract before production readiness. |
| `assessment` | Future or absent in this workspace. Apply the generic Ala service contract until repo-local source truth exists. |

Rules:
- Never flatten these runtime differences into one implementation template.
- Never invent a new observability route, header, event, metric family, or backend role for a repo when
  this contract already names one.
- When a repo's shape changes, update this table in the same change, so the next agent does not plan
  against a stale reality.

## OTLP configuration: variable names and Ala default values

Keep every value below in environment or deployment config. A code edit must never be required to move a
service from one Collector endpoint or backend to another, and a secret must never appear in source.

| Variable | Ala default | Note |
|---|---|---|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://otel-collector:4318` | The shared Collector DNS endpoint on `alaa-shared-network`. `host.docker.internal` is a local developer override and must not be committed as a service default. |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | Matches the `:4318` endpoint above. |
| `OTEL_EXPORTER_OTLP_HEADERS` | unset | Backend-specific headers belong in Collector or deployment secrets, not in a service. |
| `OTEL_EXPORTER_OTLP_TIMEOUT` | `500` | Milliseconds. |
| `OTEL_BSP_EXPORT_TIMEOUT` | `500` | Milliseconds. Span batch processor. |
| `OTEL_BLRP_EXPORT_TIMEOUT` | `500` | Milliseconds. Log record batch processor. |
| `OTEL_SCHEDULED_FLUSH_ENABLED` | `true` | For Laravel and PHP long-lived workers: bounded scheduled flushing. |
| `OTEL_FLUSH_ON_OPERATION` | `false` | Enable only for a controlled full-fidelity verification that accepts operation-boundary export cost. |

Rules:
- Every value above is expressed in these exact key names. A repo-local synonym is contract drift.
- Express every exporter timeout in milliseconds, so the three timeout values above are comparable.
- Signal-specific overrides exist only when the platform genuinely needs different values for traces,
  metrics, or logs; a signal-specific key set that duplicates the common one is removed.
- Keep OTLP log and trace export batched and bounded so a Collector problem cannot add latency to a
  request. `$alaa-observability-soc` owns how much loss is acceptable when it does.
- Keep a code-level configuration equivalent for every env-driven value, so a service still boots with a
  valid configuration when the env is incomplete, and validate the values at startup rather than at first
  export.

## Resource, propagation, and naming

- Resource identity uses the standard OTel keys `service.name`, `service.version`, and
  `deployment.environment.name`. `service.name` equals the canonical Ala service identity from
  `10-core-service-contract.md`. Which additional resource attributes are permitted is
  `$alaa-observability-soc`'s decision, not this file's.
- Propagate W3C context across incoming HTTP, outgoing HTTP, gRPC or RPC, message queues, and background
  jobs, using the exact names `traceparent`, `tracestate`, and `baggage`.
- Carry trace context in message headers or metadata for async work, and continue the trace in the
  consumer when context is present. When async context is absent, start a new trace and log the boundary
  as a distinct event rather than silently starting a detached trace.
- Never use a raw path containing a live id as the primary route identity. Use a stable route name or a
  templated pattern: `/api/v2/course/{course_id}/set/{set_id}/content/{content_id}`, never
  `/api/v2/course/8472/set/99/content/4431`.
- Use OTel semantic-convention attribute names for HTTP, DB, messaging, and RPC. Inventing a local
  attribute name for a concept the semantic conventions already name is contract drift.
- Use a query fingerprint, never raw SQL text, when query-level grouping is needed. The fingerprint field
  name is `db.statement_fingerprint`.

## Field names beyond the log contract

`20-operational-and-observability-contract.md` owns the mandatory structured log field list. These
additional field names are the canonical spellings when the value applies; do not coin a synonym:

`operation`, `component`, `dependency`, `queue`, `job_name`, `attempt`, `outcome`, `db.system`,
`db.operation`, `db.statement_fingerprint`, `error.kind`, `error.message`, `error.stack`.

An exception record carries `request_id`, `trace_id`, `project_id`, `user_id` when policy allows, the route
or operation name, the stable machine-readable `code`, `error.kind`, `error.message`, and — when the
failure involves a downstream system, a retry, or a job — `dependency`, `attempt`, and `job_name`.

Never write these values into any log, span, or metric: a password, a secret, a raw bearer token, a full
JWT, a raw `X-Access` value, a TOTP secret, `otpauth_uri`, a TOTP code, or a recovery code. For
token-level correlation use the token `jti`, a short fingerprint, or a stable internal code. Full request
bodies and PII appear only where an approved, audited flow allows it, masked or minimized; whether a given
flow is approved is `$alaa-security-review`'s and `$alaa-observability-soc`'s call, not a per-service one.

## Prometheus endpoint

- The metrics endpoint path is `/metrics` unless a repository already has a different internal path fixed
  by platform contract. It is internal and is never routed as a public client API.
- Metrics are scraped. Do not push normal long-lived service metrics, and do not use the Pushgateway for
  them.
- Whether a histogram carries exemplars is a requirement level, and `$alaa-observability-soc` owns it.
- Which labels a metric may carry, and the cardinality budget, belong to `$alaa-observability-soc`. The
  request-middleware label boundary is in `20-operational-and-observability-contract.md`.

### Metrics scraper admission

- The central Collector or Prometheus scraper calls each service's `GET /metrics` endpoint directly. The
  public API gateway never proxies, aggregates, authenticates, or discovers service metrics.
- Admission is the deployment's private network boundary only. When the endpoint is enabled, the
  application accepts the scrape without a gateway proof, bearer token, API key, session, cookie, client
  certificate, custom authentication header, or application-owned source-IP allowlist.
- Do not add a metrics credential, secret-file path, authentication bypass, or trusted-gateway environment
  variable. A service that currently guards `/metrics` with one removes that guard when adopting this
  contract.
- The deployment keeps `/metrics` absent from public gateway routes and public Ingress rules, and does not
  publish its listener or metrics port outside the approved private network. If that boundary cannot be
  demonstrated in rendered deployment artifacts and a negative reachability check, the deployment does
  not expose the endpoint.
- A private network is the accepted admission boundary for this non-sensitive operational surface; it is
  not cryptographic service authentication. Internal mTLS remains governed by
  `25-end-to-end-flow-and-boundaries.md` and is not introduced service by service for metrics.
- The endpoint exposes only registered metric families and bounded labels. A secret, credential, token,
  session value, raw PII, request or trace identifier, raw URL, query string, or customer payload in its
  output is a contract violation, because every workload admitted to the private metrics network may read
  it.

## Metric names

`24-metric-registry.md` owns every one: the `alaa_` prefix rule, the naming grammar and unit suffixes, the
complete registered family list, the baseline set every service emits, the rule that a metric is registered
before it is emitted, and the names in the fleet that are non-conforming today together with what each
becomes. Do not restate a metric name here; add it there.

Per-service metric-name conformance is recorded in `95-fleet-conformance.md`.

## Collector and Prometheus deployment notes for Ala

These are the Ala-specific placement facts. Collector topology, pipeline design, processor placement, and
sampling policy belong to `$alaa-observability-soc`.

- On Arvan Kubernetes or OpenShift, services target one shared Collector gateway tier per environment or
  cluster boundary. A service repository does not carry its own Collector topology.
- Keep the same contract in Docker Compose and Docker Swarm: OTLP to the shared Collector endpoint above,
  Prometheus scraping internal service metrics, and no publicly routed metrics endpoint.
- When SigNoz is the selected backend, its exporter endpoint, access token, headers, and TLS options live
  only in Collector deployment configuration or secrets, never in a service.
