# Metric Registry

This file owns every Ala application metric **name**, the grammar those names follow, and the rule that a
metric is registered here before it is emitted. It is the complete list: a service building a dashboard,
an alert, or a new metric reads this file and nothing else to learn what the fleet already calls things.

What this file does not own:
- **Whether a signal is required**, which alert or SLO gate it feeds, the label allow and deny lists beyond
  the request-middleware boundary, the cardinality budget, histogram bucket policy, and exemplar
  requirement level — `/alaa-observability-soc` (`$alaa-observability-soc` in Codex) owns all of it, and it
  wins whenever the two appear to disagree about whether something is required.
- The **`/metrics` endpoint, scraping, and Collector placement** — `21-alaa-platform-observability-directive.md`.
- The **request-middleware label boundary** — `20-operational-and-observability-contract.md`.
- **Log field names, `OTEL_*` variables, and trace naming** — `21-alaa-platform-observability-directive.md`.

## Naming grammar

Every application metric name matches `^alaa_[a-z0-9]+(_[a-z0-9]+)*$` and carries the suffix its type
requires:

| Type | Suffix | Example |
|---|---|---|
| Counter | `_total` | `alaa_http_requests_total` |
| Duration histogram | `_seconds` | `alaa_http_request_duration_seconds` |
| Size | `_bytes` | `alaa_worker_memory_bytes` |
| Gauge | none | `alaa_http_requests_in_flight` |

Rules, each with the failure it prevents:
- The `alaa_` prefix is unconditional for every metric a service's own code registers. A dashboard or alert
  written against `alaa_http_requests_total` breaks silently for the one service that called it
  `http_requests_total`, and the breakage looks like an outage in the panel rather than a naming defect.
- Base units only: seconds, not milliseconds; bytes, not kilobytes. Two services reporting the same quantity
  in different units cannot share one alert threshold, and the mismatch is invisible in the metric name.
- A metric that a shared kit or base library registers is prefixed **at the kit**, and its consumers
  re-generate. Fixing it per service leaves the next service built on that kit non-conforming on its first
  day, so the defect reproduces faster than it is repaired.
- Metrics emitted by an infrastructure component the fleet did not write — HAProxy's own Prometheus
  endpoint, RabbitMQ's, OpenFGA's, Postgres exporters, Vector's `internal_metrics` — keep their upstream
  names and are out of scope for the prefix rule. Renaming them breaks the upstream dashboards that ship
  with them. Only names a repository's own code chooses are governed here.

## Registering a metric before emitting it

A service may define a metric the registry does not have. It adds the row **before** the code that emits it
merges. Adding a row is a normal change and needs no approval; emitting an unregistered name is a contract
violation on the day it merges.

1. Add the row to the correct table below with every column filled.
2. Reuse an existing family name whenever the new metric measures the same thing. A second spelling of one
   measurement is worse than no metric, because two panels then disagree and an operator must learn which
   service uses which.
3. Renaming or removing a registered name follows the deprecation procedure in
   `22-failure-load-and-deprecation-contract.md`; a metric name is a contract surface there.

Why the registry exists rather than a per-service catalogue: an agent building a new service reads this file
and emits at least what its neighbours emit, and an agent adding something new makes every other service
aware of it in the same change. A per-service catalogue gives neither property.

Observable that decides compliance: every metric-name constant in a repository appears as a row below, and
every row marked `platform-wide` appears in the repository's metric-name constants for any service that has
the behaviour the row measures.

## Baseline: what every long-lived Ala service emits

These seven are the floor. A service serving HTTP traffic emits all of them, with no per-service exception.

| Metric | Type | Labels | Owner | Measures |
|---|---|---|---|---|
| `alaa_http_requests_total` | counter | `http_route`, `method`, `status_class`, `service`, `env` | platform-wide | every HTTP request the service serves |
| `alaa_http_request_duration_seconds` | histogram | `http_route`, `method`, `status_class`, `service`, `env` | platform-wide | end-to-end request duration |
| `alaa_http_request_failures_total` | counter | `http_route`, `method`, `status_class`, `service`, `env` | platform-wide | requests that failed |
| `alaa_http_requests_in_flight` | gauge | `http_route`, `method` | platform-wide | concurrent in-flight requests; the observable behind the ingress admission limit in `22-failure-load-and-deprecation-contract.md` |
| `alaa_service_ready` | gauge | `service`, `env` | platform-wide | `1` when `/api/ready` answers ready, `0` when not |
| `alaa_service_readiness_failures_total` | counter | `service`, `env`, `check` | platform-wide | readiness check failures |
| `alaa_requests_deadline_exhausted_total` | counter | `http_route`, `service`, `env` | platform-wide | requests refused without calling anything because the inherited deadline had no remaining budget; the observable behind the request deadline in `22-failure-load-and-deprecation-contract.md` |

## Conditional families: emitted when the service has the behaviour

A service that has the behaviour uses these exact names. A service that does not have the behaviour emits
nothing rather than inventing a near-miss name.

### Authorization and validation
| Metric | Type | Owner | Measures |
|---|---|---|---|
| `alaa_auth_context_invalid_total` | counter | platform-wide | trusted-context parse or validation failures at ingress |
| `alaa_authz_denied_total` | counter | platform-wide | authorization denials |
| `alaa_input_validation_failed_total` | counter | platform-wide | request validation failures |
| `alaa_rate_limit_exceeded_total` | counter | platform-wide | requests rejected by a rate limit |

### Pagination
| Metric | Type | Labels | Owner | Measures |
|---|---|---|---|---|
| `alaa_pagination_client_failures_total` | counter | `http_route`, `purpose`, `code` | any service with keyset pagination | client-recoverable pagination failures by bounded route, code-owned purpose, and stable error code |
| `alaa_pagination_server_failures_total` | counter | `http_route`, `purpose`, `category` | any service with keyset pagination | pagination server failures by bounded route, code-owned purpose, and bounded failure category |
| `alaa_pagination_reply_hydration_nodes` | gauge | `purpose`, `truncated` | any service with bounded reply hydration | reply nodes materialized for a keyset page, split only by code-owned purpose and bounded truncation state |
| `alaa_pagination_requests_total` | counter | `http_route`, `purpose`, `mode` | any service running dual-mode pagination during a keyset migration | successfully served list responses split by the pagination mode actually used, so a legacy-selector removal gate has a server-side observable instead of a point-in-time client survey. `mode` is bounded to `legacy` and `keyset` |

### Database
| Metric | Type | Owner | Measures |
|---|---|---|---|
| `alaa_db_queries_total` | counter | any service with a database | executed queries |
| `alaa_db_query_duration_seconds` | histogram | any service with a database | query duration |
| `alaa_db_query_failures_total` | counter | any service with a database | failed queries |
| `alaa_db_connections_active` | gauge | any service with a database | active connections |
| `alaa_db_pool_in_use` | gauge | any service with a database | the observable behind the pool bound in `22-failure-load-and-deprecation-contract.md` |
| `alaa_db_pool_idle` | gauge | any service with a database | idle pooled connections |
| `alaa_db_pool_wait_seconds` | histogram | any service with a database | time spent waiting to acquire a pooled connection |
| `alaa_db_session_guard_seconds` | gauge | any service on the `alaa-go-chi` kit with a database | the effective server-side session guard in seconds, as the server reports it on the connection sampled; `0` is PostgreSQL's own encoding for disabled |
| `alaa_db_session_guard_observed` | gauge | same | `1` when the guard was read successfully, `0` when the read failed, so a disabled guard is distinguishable from an unread one |

Where the driver and database support them safely: `alaa_db_transactions_total`,
`alaa_db_transaction_duration_seconds`, `alaa_db_lock_wait_seconds`, `alaa_db_deadlocks_total`.

### The two `alaa_db_session_guard_*` families: their labels, and why there are two

Registered 2026-08-11 on the registry owner's approval, ahead of emission, for
`alaa-go-chi`'s `docs/change-requests/2026-08-11-pgkit-session-guard-runtime-verification.md`. They
exist because that kit's ratified pooled/direct boundary hands `statement_timeout`, `lock_timeout` and
`idle_in_transaction_session_timeout` to the pooler and the database on a pooled lane, leaving no way
to answer "is this service actually guarded" without a manual session.

- **Labels: `guard`, `lane`.** `guard` is closed to `statement_timeout`, `lock_timeout`,
  `idle_in_transaction_session_timeout`; `lane` is closed to `runtime`, `admin`. Both are
  compile-time constants in the kit, so nothing in a request, tenant, host, or connection can extend
  either set. Add no per-connection, per-host, per-database or per-tenant label: the question these
  answer is per-service, and the connection-level detail belongs in a log reached through `trace_id`.
- **Worst-case series: 3 `guard` x 2 `lane` = 6 per family, 12 across both, per service per
  environment**, with `service` and `env` arriving as const labels. Invariant under attack traffic
  because no request path reaches either label.
- **Two families, not one, and this is not a second spelling of one measurement.** The value alone
  cannot distinguish *disabled on purpose* from *never configured* from *the read failed*, because `0`
  is PostgreSQL's own encoding for disabled. With the companion, the first two are `observed=1,
  value=0` and the third is `observed=0`, and series absence means only that the service is not
  reporting.
- **A gauge carrying `_seconds` is deliberate**, matching `alaa_queue_consumer_lag_seconds` and
  `alaa_outbox_oldest_age_seconds`: the base-unit rule governs, and the type-suffix table's "gauge:
  none" applies to gauges that measure no unit.
- **`{guard="statement_timeout", lane="admin"}` is `0` on a correctly configured service**, because
  that kit's `PG_MIGRATE_STATEMENT_TIMEOUT` defaults to `0` by ratified design. Measured against a real
  stack on 2026-08-11. An alert that does not exclude it fires on correct configuration from its first
  day. Alert authorship and severity remain `$alaa-observability-soc`'s.

### Downstream dependency
| Metric | Type | Owner | Measures |
|---|---|---|---|
| `alaa_dependency_requests_total` | counter | any service with an outbound call | outbound dependency calls |
| `alaa_dependency_request_duration_seconds` | histogram | any service with an outbound call | dependency call duration |
| `alaa_dependency_request_failures_total` | counter | any service with an outbound call | failed dependency calls |
| `alaa_dependency_timeouts_total` | counter | any service with an outbound call | per-attempt timeouts as defined in `22-failure-load-and-deprecation-contract.md` |
| `alaa_dependency_checks_total` | counter | `content` today; adoptable | readiness dependency probes executed |
| `alaa_dependency_check_duration_seconds` | histogram | `content` today; adoptable | readiness dependency probe duration |

### Queue and async
| Metric | Type | Owner | Measures |
|---|---|---|---|
| `alaa_queue_messages_published_total` | counter | any publisher | messages published to the broker |
| `alaa_queue_messages_consumed_total` | counter | any consumer | messages consumed |
| `alaa_queue_message_failures_total` | counter | any consumer | handler failures |
| `alaa_queue_message_duration_seconds` | histogram | any consumer | handler duration |
| `alaa_queue_retries_total` | counter | any consumer | redeliveries and retries |
| `alaa_queue_dead_letter_total` | counter | any consumer | messages dead-lettered |
| `alaa_queue_backlog` | gauge | any consumer with backlog visibility | messages awaiting consumption; the observable behind the queued path in `22-failure-load-and-deprecation-contract.md` |
| `alaa_queue_consumer_lag_seconds` | gauge | any consumer with backlog visibility | age of the oldest unconsumed message |

### Outbox
One family, because three spellings exist today and no panel can read all three.

| Metric | Type | Owner | Measures |
|---|---|---|---|
| `alaa_outbox_depth` | gauge | any service with an outbox | rows awaiting publish |
| `alaa_outbox_oldest_age_seconds` | gauge | any service with an outbox | age of the oldest unpublished row |
| `alaa_outbox_published_total` | counter | any service with an outbox | rows successfully published |
| `alaa_outbox_publish_failures_total` | counter | any service with an outbox | publish attempts that failed |

### Worker and runtime
| Metric | Type | Owner | Measures |
|---|---|---|---|
| `alaa_worker_jobs_in_progress` | gauge | any service with workers | jobs currently executing |
| `alaa_worker_restarts_total` | counter | any service with workers | worker restarts |
| `alaa_worker_memory_bytes` | gauge | any service with workers | worker resident memory |
| `alaa_service_restarts_total` | counter | any service that can observe it | process restarts, when available from the app boundary or local runtime tracking |
| `alaa_job_lane_depth` | gauge | any service with a lane-partitioned job queue | jobs waiting per lane |
| `alaa_job_lane_oldest_age_seconds` | gauge | same | age of the oldest waiting job per lane |
| `alaa_job_dead_depth` | gauge | same | jobs in the terminal dead state |
| `alaa_seed_runs_total` | counter | any service with a seed runner | seed executions by outcome |
| `alaa_http_server_error_total` | counter | any Go service on the kit | server-level faults bridged from the HTTP server's own error log: TLS handshake failures, header-read timeouts, malformed `Content-Length` |

Go services also expose goroutine count, GC cycles, GC pause duration, and heap usage through the official
Prometheus Go collectors rather than hand-rolled gauges; those keep their upstream names. Laravel and Octane
services also expose Octane worker count, worker restart count, queue worker failure count, queue busy
signals, and long job execution time under the `alaa_worker_*` names above.

## Service-owned business families

Each row belongs to the service that owns the behaviour. Adding a business family adds it here in the same
change; a per-feature metric tree that is not listed here is not part of the contract and will not appear on
platform dashboards.

| Metric | Type | Owner | Measures | Evidence |
|---|---|---|---|---|
| `alaa_auth_login_attempts_total` | counter | `auth` | login attempts | `app/Support/Observability/MetricsRegistry.php:230` |
| `alaa_auth_login_failures_total` | counter | `auth` | failed logins | `MetricsRegistry.php:231` |
| `alaa_auth_token_issued_total` | counter | `auth` | access tokens issued | `MetricsRegistry.php:232` |
| `alaa_auth_token_refreshed_total` | counter | `auth` | successful refreshes | `MetricsRegistry.php:233` |
| `alaa_auth_token_refresh_failures_total` | counter | `auth` | failed refreshes | `MetricsRegistry.php:234` |
| `alaa_auth_totp_step_up_total` | counter | `auth` | TOTP step-up challenges completed | `MetricsRegistry.php:235` |
| `alaa_auth_totp_step_up_failures_total` | counter | `auth` | failed TOTP step-ups | `MetricsRegistry.php:236` |
| `alaa_gateway_totp_proof_verifications_total` | counter | `gateway` | TOTP step-up proof verifications, by outcome | registered ahead of emission; labels and production path below |
| `alaa_content_requests_total` | counter | `content` | content requests served | emitted in `content` |
| `alaa_content_access_denied_total` | counter | `content` | content access denials | emitted in `content` |
| `alaa_content_filter_executions_total` | counter | `content` | filter-pipeline executions | emitted in `content` |
| `alaa_video_playback_authorizations_total` | counter | `content`, `vod` | playback authorization decisions | emitted in `content` |
| `alaa_controlled_operations_total` | counter | `content`, via the shared controlled-ops package | controlled operations started | emitted in `content` |
| `alaa_controlled_operation` | gauge | same | controlled operations currently running | emitted in `content` |
| `alaa_controlled_operation_duration_seconds` | histogram | same | controlled-operation duration | emitted in `content` |
| `alaa_controlled_operation_items_total` | counter | same | items processed | emitted in `content` |
| `alaa_controlled_operation_progress_updates_total` | counter | same | progress updates emitted | emitted in `content` |
| `alaa_controlled_operation_retries_total` | counter | same | controlled-operation retries | emitted in `content` |
| `alaa_controlled_operation_totp_bypass_total` | counter | same | TOTP bypasses taken on a controlled operation | emitted in `content` |
| `alaa_comment_created_total` | counter | `comment` | comments created | `app/Support/Observability/MetricCatalog.php:112` |
| `alaa_comment_deleted_total` | counter | `comment` | comments deleted | `MetricCatalog.php:117` |
| `alaa_comment_moderation_actions_total` | counter | `comment` | moderation actions | `MetricCatalog.php:122` |
| `alaa_ticket_created_total` | counter | `ticket` | tickets created | contract-declared |
| `alaa_ticket_reply_created_total` | counter | `ticket` | ticket replies created | contract-declared |
| `alaa_ticket_status_changed_total` | counter | `ticket` | ticket status transitions | contract-declared |
| `alaa_watch_events_ingested_total` | counter | `wa` | watch events ingested | contract-declared |
| `alaa_watch_ingest_failures_total` | counter | `wa` | ingest failures | contract-declared |
| `alaa_watch_pipeline_backpressure_total` | counter | `wa` | pipeline backpressure events | contract-declared |
| `alaa_entitlement_grant_mutations_total` | counter | `entitlement-api` | grant create, update, revoke | owed rename of `entitlement_grant_mutations_total` |
| `alaa_entitlement_access_queries_total` | counter | `entitlement-api` | access queries served | owed rename of `entitlement_access_queries_total` |
| `alaa_entitlement_expansion_duration_seconds` | histogram | `entitlement-api` | audience-expansion duration | owed rename of `entitlement_expansion_duration_seconds` |
| `alaa_entitlement_worker_batches_total` | counter | `entitlement-api` | worker batches claimed | owed rename of `entitlement_worker_batches_total` |
| `alaa_entitlement_worker_attempts_total` | counter | `entitlement-api` | worker attempts | owed rename of `entitlement_worker_attempts_total` |
| `alaa_authz_decisions_total` | counter | `authz-sidecar` | allow/deny decisions | owed rename of `authz_sidecar_decisions_total` |
| `alaa_authz_decision_duration_seconds` | histogram | `authz-sidecar` | decision duration | owed rename of `authz_sidecar_decision_duration_seconds` |
| `alaa_authz_openfga_requests_total` | counter | `authz-sidecar` | OpenFGA check calls | owed rename of `authz_sidecar_openfga_requests_total` |
| `alaa_authz_openfga_request_duration_seconds` | histogram | `authz-sidecar` | OpenFGA check duration | owed rename of `authz_sidecar_openfga_request_duration_seconds` |
| `alaa_authz_cache_requests_total` | counter | `authz-sidecar` | decision-cache hits and misses | owed rename of `authz_sidecar_cache_requests_total` |

### `alaa_gateway_totp_proof_verifications_total`: its label, and where it is produced

The two `auth` TOTP rows above cover the half of step-up that `auth` runs. The gateway half —
verifying the proof a client retries with — had no counter at all, so a signing-key rotation showed as a
rising counter on `auth` only if codes were also failing there, while the gateway's `invalid_signature`
spike was reachable by log search alone. This row is the gateway half.

- **Labels: `status`, `service`, `env`.** `status` is the proof-verification outcome; its value set is the
  status vocabulary owned by `32-auth-totp-and-step-up-contract.md`, closed there and chosen by gateway
  configuration. Add no `route`, `user`, `project`, `purpose`, or proof-id label: the question this counter
  answers is fleet-wide, and the gateway log already carries `route`, `path`, `user_id`, `project_id`,
  `request_id`, and `trace_id` on the same line for the attribution half.
- **Increment rule: once per request that carried `X-TOTP-Proof`.** A request with no proof increments
  nothing, because counting those would restate `alaa_http_requests_total` under a second name.
- **Worst-case series: 19 status values x 1 `service` x 1 `env` = 19 per environment.** That is the
  eighteen rejection values closed in `32-auth-totp-and-step-up-contract.md` plus `validated`, and it
  excludes only `absent`, which the increment rule above never counts. It holds under attack traffic
  because nothing in the request can add a value to the label: every value is a `str()` literal in the
  gateway's own configuration. Recount it against that configuration whenever a status is added — the
  figure was 18 until `issued_in_future` shipped. Ceilings are `$alaa-observability-soc`,
  `references/30-quantitative-budgets.md`.
- **One counter, not two.** A separate failures counter would be `status != "validated"` on this one, and a
  second spelling of one measurement is what the registering rule above forbids. Keeping `validated` in the
  label is also what gives a rejection rate its denominator.
- **Produced by the Vector pipeline, not by HAProxy.** The path is a `log_to_metric` transform in the
  gateway repository's `observability/vector/gateway-vector.yaml` over the `totp_proof_status` field of the
  gateway request log, exported through a `prometheus_exporter` sink. HAProxy's own Prometheus endpoint
  cannot produce it — `totp_proof_status` is a per-transaction variable, not a stats counter — and the
  metrics that endpoint does emit keep their upstream names under the prefix rule above.

## Reserved and owed names

A name here is registered and is not emitted by any service today. Registered means no other service may
reuse the name for a different measurement; it does not mean the metric exists.

| Metric | State | Note |
|---|---|---|
| `alaa_auth_token_validation_failed_total` | reserved | Named by this contract before the registry existed; `auth` does not emit it. Either `auth` emits it or the row is removed through the deprecation procedure. Do not build an alert on it. |
| `alaa_requests_deadline_exhausted_total` | owed by every service | No service computes the request deadline yet, so no service emits this counter. A permanent zero on it means one of two things and the operator must distinguish them: nobody honours the deadline, or the budget is so generous nothing ever reaches it. |
| `alaa_gateway_totp_proof_verifications_total` | owed by `gateway` | Registered ahead of emission, which is the order this file requires. On 2026-07-29 the gateway's `observability/vector/gateway-vector.yaml` carries no `log_to_metric` transform and its only `prometheus_exporter` sink exports Vector's own internal metrics, so the series does not exist. A missing series means "the transform is not built", not "no proof was rejected"; build no alert on it until the transform lands. |

## Names that exist today and are non-conforming

Each row names what the metric becomes. These are the fleet's current drift, recorded here so an agent
reading a neighbour's code does not copy the wrong spelling.

| Current name | Repository | Becomes |
|---|---|---|
| `http_requests_total`, `http_request_duration_seconds`, `http_requests_in_flight` | `alaa-go-chi` kit, `obskit/metricnames.go:4-6` | the `alaa_`-prefixed baseline names above |
| `outbox_depth`, `outbox_oldest_age_seconds`, `outbox_publish_failures_total` | kit, `obskit/metricnames.go:7-9` | `alaa_outbox_depth`, `alaa_outbox_oldest_age_seconds`, `alaa_outbox_publish_failures_total` |
| `job_lane_depth`, `job_lane_oldest_age_seconds`, `job_dead_depth` | kit, `obskit/metricnames.go:10-12` | the `alaa_job_*` names above |
| `consumer_lag` | kit, `obskit/metricnames.go:13` | `alaa_queue_consumer_lag_seconds`, which also fixes the missing unit suffix |
| `pg_pool_wait_seconds` | kit, `obskit/metricnames.go:14` | `alaa_db_pool_wait_seconds` |
| `seed_runs_total` | kit, `obskit/metricnames.go:15` | `alaa_seed_runs_total` |
| `service_readiness`, `service_readiness_transitions_total` | kit, `obskit/metricnames.go:16-17` | `alaa_service_ready`, `alaa_service_readiness_failures_total` |
| `http_server_error_total` | kit, `obskit/metricnames.go:25` | `alaa_http_server_error_total` |
| `entitlement_http_requests_total`, `entitlement_http_request_duration_seconds` | `entitlement-api`, `internal/observability/metrics.go:93,100` | the `alaa_http_*` baseline names above |
| `entitlement_grpc_requests_total`, `entitlement_grpc_request_duration_seconds` | `entitlement-api`, `metrics.go:108,115` | `alaa_dependency_requests_total` and `alaa_dependency_request_duration_seconds` with a `dependency` label, or registered `alaa_grpc_*` rows if the gRPC surface needs its own family |
| `entitlement_mq_publish_total`, `entitlement_mq_publish_duration_seconds`, `entitlement_mq_consume_total`, `entitlement_mq_retry_total` | `entitlement-api`, `metrics.go:137-159` | `alaa_queue_messages_published_total`, `alaa_queue_message_duration_seconds`, `alaa_queue_messages_consumed_total`, `alaa_queue_retries_total` |
| `entitlement_outbox_events_total`, `entitlement_outbox_retry_delay_seconds` | `entitlement-api`, `metrics.go:166,173` | `alaa_outbox_published_total`; the retry-delay histogram registers its own `alaa_outbox_retry_delay_seconds` row when it is kept |
| `authz_sidecar_authz_requests_total`, `authz_sidecar_authz_request_duration_seconds`, `authz_sidecar_authz_requests_in_flight` | `authz-sidecar` | the `alaa_http_*` baseline names above |
| `alaa_http_request_errors_total` | `comment`, `MetricCatalog.php:29` | `alaa_http_request_failures_total` |
| `alaa_queue_jobs_total`, `alaa_queue_job_duration_seconds` | `comment`, `MetricCatalog.php:60,65` | `alaa_queue_messages_consumed_total`, `alaa_queue_message_duration_seconds` |
| `alaa_outbox_events_total`, `alaa_outbox_pending_total`, `alaa_outbox_failed_total`, `alaa_outbox_lag_seconds` | `comment`, `MetricCatalog.php:71-89` | `alaa_outbox_published_total`, `alaa_outbox_depth`, `alaa_outbox_publish_failures_total`, `alaa_outbox_oldest_age_seconds` |
| `alaa_content_outbox_events_published_total`, `alaa_content_outbox_publish_failures_total` | `content` | `alaa_outbox_published_total`, `alaa_outbox_publish_failures_total` |

## The mechanical check, and what it cannot reach

A registry nothing checks goes stale, so one exists. `scripts/validate_sohrab_skill_pack.py` in the skills
repository fails when a metric name matching `alaa_[a-z0-9_]+` appears anywhere in this skill's reference
files and has no row in this file, and fails when a broker exchange or queue name appears in a reference
file and has no row in `23-queue-and-exchange-registry.md`. Run it from the skills repository root with `python3 scripts/validate_sohrab_skill_pack.py` and read the
lines containing `no row in`; those are the registry failures. The pack carries unrelated pre-existing
failures from other skills, so a non-zero exit alone does not mean a registry failure, and an empty
`no row in` set is the passing condition for this check.

What that check proves: this skill cannot name a metric or a queue it did not register. What it cannot
prove: that a **service repository** emits only registered names, because the skill repository cannot read
the service repositories. Closing that half needs a check inside each repository, and the shape it takes per
runtime is already available:

- Go services on the `alaa-go-chi` kit have `contracttest.AssertMetricNamesStable`, which gathers from the
  live Prometheus registry and fails on an unexpected or missing family. Extending it with the registered
  name set is the smallest change that closes the Go half of the fleet at once, and it belongs in the kit
  rather than in each service, per the kit-prefix rule above.
- Laravel services with a metric-name catalogue class — `comment`'s `MetricCatalog.php`, `auth`'s
  `MetricsRegistry.php` — can assert in a test that every name the catalogue declares matches
  `^alaa_[a-z0-9]+(_[a-z0-9]+)*$` and appears in a committed copy of the registered set. `content` and
  `entitlement-api` have no single catalogue file, so they need one before the check can be written; that is
  a prerequisite, not an excuse.

Until those land, the fleet half of this registry is enforced by review, and review is why the drift table
above exists.
