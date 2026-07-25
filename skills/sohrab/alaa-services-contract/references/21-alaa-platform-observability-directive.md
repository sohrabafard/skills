# Alaa Platform Observability Names And Values

Use this file when the task needs an exact observability **name** or **value**: an `alaa_*` metric family,
an `OTEL_*` environment variable and its Ala default, a trace or route naming rule, an exception field
name, or the current telemetry shape of a specific Ala service.

## Ownership split, and it is binding

This skill owns every observability **name and value**. `$alaa-observability-soc` owns every **requirement
level, gate, threshold, and reason**.

- Here: metric family names, log field names, event and code names, `OTEL_*` variable names and their Ala
  default values, route and operation naming rules, exception field names, and the per-service reality
  table below.
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

## Prometheus endpoint and metric naming

- The metrics endpoint path is `/metrics` unless a repository already has a different internal path fixed
  by platform contract. It is internal and is never routed as a public client API.
- Metrics are scraped. Do not push normal long-lived service metrics, and do not use the Pushgateway for
  them.
- Every application metric name begins `alaa_`, uses lowercase snake_case, and carries the unit or kind
  suffix that matches its type: `_total` for a counter, `_seconds` for a duration, `_bytes` for a size, and
  no suffix for a plain gauge. Base units only — seconds, not milliseconds; bytes, not kilobytes.
- Never invent a repo-local name for a family in the catalog below. A dashboard or alert built on
  `alaa_http_requests_total` breaks silently for the one service that called it something else, which is
  the exact failure this catalog exists to prevent.
- Which labels a metric may carry, and the cardinality budget, belong to `$alaa-observability-soc`. The
  request-middleware label boundary is in `20-operational-and-observability-contract.md`.

## The `alaa_*` metric family catalog

These are the canonical family names. A service exposing the behaviour a family measures uses that exact
name. `$alaa-observability-soc` decides which families a given service is required to expose.

### HTTP request
- `alaa_http_requests_total` — counter, total HTTP requests.
- `alaa_http_request_duration_seconds` — histogram, end-to-end request duration.
- `alaa_http_requests_in_flight` — gauge, current in-flight requests. This is the observable behind the
  ingress admission limit in `22-failure-load-and-deprecation-contract.md`.
- `alaa_http_request_failures_total` — counter, failed requests.

### Readiness and health
- `alaa_service_ready` — gauge, `1` when ready and `0` when not ready.
- `alaa_service_readiness_failures_total` — counter.
- `alaa_service_restarts_total` — counter, when available from the app boundary or local runtime tracking.

### Authorization and validation
- `alaa_auth_context_invalid_total`
- `alaa_authz_denied_total`
- `alaa_input_validation_failed_total`
- `alaa_rate_limit_exceeded_total`

### Database
- `alaa_db_queries_total`
- `alaa_db_query_duration_seconds`
- `alaa_db_query_failures_total`
- `alaa_db_connections_active`
- `alaa_db_pool_in_use` — the observable behind the pool bound in `22-failure-load-and-deprecation-contract.md`.
- `alaa_db_pool_idle`

Where the driver and database support them safely: `alaa_db_transactions_total`,
`alaa_db_transaction_duration_seconds`, `alaa_db_lock_wait_seconds`, `alaa_db_deadlocks_total`.

### Downstream dependency
- `alaa_dependency_requests_total`
- `alaa_dependency_request_duration_seconds`
- `alaa_dependency_request_failures_total`
- `alaa_dependency_timeouts_total` — counts a per-attempt timeout as defined in
  `22-failure-load-and-deprecation-contract.md`.

### Queue and async
- `alaa_queue_messages_published_total`
- `alaa_queue_messages_consumed_total`
- `alaa_queue_message_failures_total`
- `alaa_queue_message_duration_seconds`
- `alaa_queue_retries_total`
- `alaa_queue_dead_letter_total`
- `alaa_queue_backlog` and `alaa_queue_consumer_lag_seconds` where backlog visibility is service-owned or
  safely available.

### Worker and runtime
- `alaa_worker_jobs_in_progress`
- `alaa_worker_restarts_total`
- `alaa_worker_memory_bytes`

Go services also expose goroutine count, garbage-collection cycles, GC pause duration, and heap usage
through the official Prometheus Go collectors rather than hand-rolled gauges. Laravel and Octane services
also expose Octane worker count, worker restart count, queue worker failure count, queue busy signals, and
long job execution time.

### Service-owned business families

Each service exposes a small set of business metrics under the same naming rules, owned by the service
that owns the behaviour. The canonical names in use today:

- `auth` — `alaa_auth_login_attempts_total`, `alaa_auth_login_failures_total`,
  `alaa_auth_token_issued_total`, `alaa_auth_token_validation_failed_total`.
- `content` and `vod` — `alaa_content_requests_total`, `alaa_content_access_denied_total`,
  `alaa_video_playback_authorizations_total`.
- `comment` — `alaa_comment_created_total`, `alaa_comment_deleted_total`,
  `alaa_comment_moderation_actions_total`.
- `ticket` — `alaa_ticket_created_total`, `alaa_ticket_reply_created_total`,
  `alaa_ticket_status_changed_total`.
- `wa` — `alaa_watch_events_ingested_total`, `alaa_watch_ingest_failures_total`,
  `alaa_watch_pipeline_backpressure_total`.

Adding a business family adds it to this list in the same change. A per-feature metric tree that is not
listed here is not part of the contract and will not appear on platform dashboards.

## Collector and Prometheus deployment notes for Ala

These are the Ala-specific placement facts. Collector topology, pipeline design, processor placement, and
sampling policy belong to `$alaa-observability-soc`.

- On Arvan Kubernetes or OpenShift, services target one shared Collector gateway tier per environment or
  cluster boundary. A service repository does not carry its own Collector topology.
- Keep the same contract in Docker Compose and Docker Swarm: OTLP to the shared Collector endpoint above,
  Prometheus scraping internal service metrics, and no publicly routed metrics endpoint.
- When SigNoz is the selected backend, its exporter endpoint, access token, headers, and TLS options live
  only in Collector deployment configuration or secrets, never in a service.
