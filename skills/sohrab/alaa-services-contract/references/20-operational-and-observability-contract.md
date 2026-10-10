# Operational And Observability Contract

This file owns the exact stable observability surfaces that must not drift across Ala services, and the broker message envelope and broker names that carry the same correlation across an async hop.

Use `21-alaa-platform-observability-directive.md` together with this file when the task needs an `OTEL_*` variable and its Ala default, a trace or route naming rule, or the current telemetry shape of a specific service, and `24-metric-registry.md` when it needs a metric name. If these two files appear to conflict, this file owns the exact header, log field, event, code, probe-noise, and middleware invariants.

Requirement levels, gates, thresholds, alerts, Collector topology, sampling policy, metric label budgets, and Sentry policy are in neither file. `$alaa-observability-soc` owns them, and it wins on whether a signal is required.

## Exact response headers

The target Ala response-header contract is:
- `X-Request-Id`
- `traceparent`

Rules:
- Do not make `X-Correlation-Id` part of the final contract.
- Do not make `X-Trace-Id` part of the final contract.
- If a service still emits, parses, forwards, tests, or documents `X-Correlation-Id`, migrate it to `X-Request-Id` plus `traceparent` and remove the stale code in the same effort.
- After applying this skill, `X-Correlation-Id` must not appear anywhere in the service: not in code, config, docs, tests, fixtures, Postman artifacts, or emitted response headers.

## Exact `X-Request-Id` rules

Rules:
- Preserve an inbound `X-Request-Id` only when, after trimming leading and trailing whitespace, it matches
  `^[A-Za-z0-9._~-]{8,128}$`. That is one token of URL-safe unreserved characters, at least 8 and at most
  128 of them, with no whitespace, no comma, and no control character.
- Treat any other inbound value as absent, including an empty value, a value with an inner space, a
  multi-value header, and a value outside the length bounds. Do not sanitize it into a passing value,
  because a rewritten id no longer joins to the caller's own logs.
- When the value is absent or was treated as absent, generate a new lowercase UUIDv7.
- Emit `input.validation.failed` at debug level with a stable validation code when an inbound value is
  rejected, so a misbehaving caller is diagnosable without failing its request.
- Keep it stable for the lifetime of the request.
- Return it on every `/api/*` response including `/api/health`, `/api/ready`, and rendered API error responses.
- Include it in every structured request log and relevant denial or failure log.

## Exact `traceparent` rules

Canonical format:
- `00-{trace_id}-{parent_id}-01`

`trace_id` rules:
- 32 lowercase hexadecimal characters
- non-zero
- generated from secure random 16 bytes when absent or invalid

`parent_id` rules:
- 16 lowercase hexadecimal characters
- non-zero
- generated from secure random 8 bytes when absent or invalid

Incoming `traceparent` rules:
- if valid, preserve it as the canonical trace context for the request
- derive logged `trace_id` from it
- if invalid, do not fail the request only because of this
- treat it as absent and generate a fresh canonical `traceparent`

Response rules:
- always return the canonical `traceparent`
- always return `X-Request-Id`

Logging rules:
- log `trace_id`
- make `trace_id` queryable as its own field in structured logs and OTLP log records
- include `traceparent` in structured logs when it helps propagation debugging, but never force operators to parse it for normal trace lookup
- do not require a separate `X-Trace-Id` response header

## Structured log field contract

For logs emitted by middleware or operational flows owned by this skill, include at minimum:
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
- `project_id` when available, always in the canonical UUIDv7 form bound by `25-end-to-end-flow-and-boundaries.md`
- `user_id` when available and safe
- `http.method`
- `http.route` or route name
- `http.status`
- `duration_ms`

Keep the field names stable so SOC queries and runbooks remain reusable.

## Event and code naming contract

For request and operational flows owned by this skill, use these exact event names:
- `http.request.completed`
- `http.request.failed`
- `service.readiness.failed`
- `service.readiness.recovered` when a repository explicitly tracks readiness transitions
- `auth.context.invalid`
- `authz.denied`
- `input.validation.failed`
- `dependency.call.failed` for one failed attempt against a downstream dependency
- `dependency.unavailable` when the retry budget for that dependency is exhausted, or when the request
  deadline no longer covers another attempt
- `queue.publish.failed` when a broker publish or its outbox write fails
- `request.shed` when ingress refuses a request because in-flight requests are at the configured maximum
- `panic.recovered` when a request, handler or worker recovers a panic and turns it into an error response or a failed delivery

Use these exact code expectations:
- `HTTP_REQUEST_COMPLETED` with `http.request.completed`
- `HTTP_REQUEST_FAILED` with `http.request.failed`
- `SERVICE_NOT_READY` with `service.readiness.failed`
- `SERVICE_READY` with `service.readiness.recovered` when used
- `AUTH_*` and `TENANT_CONTEXT_*` codes from `$alaa-trust-gateway-auth` (`references/50-deny-codes.md` owns each name and status) with `auth.context.invalid`, or with the event of the route that refuses them
- stable domain denial codes with `authz.denied`
- stable validation codes with `input.validation.failed`
- `DEPENDENCY_CALL_FAILED` with `dependency.call.failed`
- `DEPENDENCY_UNAVAILABLE` with `dependency.unavailable`
- `QUEUE_PUBLISH_FAILED` with `queue.publish.failed`
- `REQUEST_SHED` with `request.shed`
- `PANIC_RECOVERED` with `panic.recovered`
- `INTERNAL_ERROR` as the response `code` of an unexpected `500` (a response that cannot be rendered, or a recovered panic); the log line keeps `HTTP_REQUEST_FAILED` or `PANIC_RECOVERED`

The behaviour these four names describe is defined in `22-failure-load-and-deprecation-contract.md`. This
file owns the names; that file owns when they are emitted.

Rules:
- Do not invent alternate names for the same event type.
- Keep `event` and `code` aligned.
- Keep user-facing messages separate from these machine-readable names.

## Service-specific event names (authorization mesh)

A record, not a rule: the `event` values each mesh service emits, verified 2026-10-10. Each owning
repository's `docs/handoffs/mesh-145d79be-registry-inventory.md` cites every name at `file:line`.

| Owner | `event` values | Emitted when |
|---|---|---|
| `entitlement-api` | `panic.recovered` | recovered panic in a handler, worker, consumer, or operator mode (`internal/observability/recovery.go:21-26`) |
| `entitlement-api` | `security.audit.attempt`, `security.audit.outcome` | start and end of an audited access route (`internal/httpserver/access_observability.go:43-62`) |
| `entitlement-api` | `entitlement.projection_replay.started`, `entitlement.projection_replay.completed` | legacy `projection-replay` operator mode (`internal/app/projection_replay.go:73-100`) |
| `entitlement-api` | `projection_operator_started`, `projection_task_reopened`, `projection_write_fence_applied`, `projection_generation_created`, `projection_bootstrap_applied`, `projection_bootstrap_completed`, `projection_switch_check`, `projection_generation_abandoned_retired`, `projection_generation_retire_applied`, `projection_hydration_live_recheck`, `projection_hydration_verified`, `projection_hydration_refused`, `projection_marker_incident_operator_failed`, `projection_rule_inspection`, `projection_rule_inspection_revision`, `projection_minimum_generation`, `projection_minimum_generation_refused`, `projection_rule_repair_applied`, `projection_snapshot_exported`, `projection_snapshot_verified` | one audited `projection-*` operator mode started, applied, verified, refused, or reported (`internal/app/projection_operator*.go`, `projection_reopen.go`) |
| `entitlement-api` | `projection_rule_blocked`, `projection_outcome_conflict`, `projection_task_dead_lettered`, `projection_deny_retire_exhausted`, `projection_incident_repeat`, `projection_marker_incident`, `projection_marker_incident_failed`, `projection_marker_incident_closed`, `projection_marker_incident_awaiting_verification`, `projection_marker_incident_fenced_successor`, `projection_deny_not_effective`, `projection_deny_retire_success_after_refusal` | projection-worker receipt processing blocked a rule, opened, repeated, or closed an incident, or saw a dead-letter, conflict, or ineffective deny (`internal/projectionreceipts/transition.go`, `incident.go`) |
| `entitlement-projector` | `panic.recovered`, `telemetry_shutdown_incomplete` | recovered panic; incomplete exporter shutdown; all modes (`internal/observability/recovery.go:22-23`, `shutdown.go:64`) |
| `entitlement-projector` | `executor_task_rejected`, `executor_task_disposed`, `executor_task_defect`, `executor_task_held`, `executor_task_hold_repeated`, `executor_task_hold_reclassified`, `executor_task_retry`, `executor_task_final_attempt_dead_lettered`, `executor_task_final_attempt_notice` | rule-executor task attempt rejected, applied, held, retried, or dead-lettered (`internal/execruntime/handler.go`, `runtime.go`) |
| `entitlement-projector` | `executor_generation_verify_failed`, `executor_engine_tls_unverified`, `executor_intake_paused`, `executor_intake_channel_lost`, `executor_intake_return_unproven`, `executor_intake_channel_closed_at_ceiling`, `executor_intake_probe_failed`, `executor_intake_probe_passed`, `executor_intake_resume_failed`, `executor_intake_return_mode`, `executor_shutdown_drain_expired`, `executor_shutdown_deliveries_returned` | rule-executor startup verification, intake pause, probe, resume, and shutdown drain (`internal/execruntime/readiness.go`, `app.go`, `runtime.go`) |
| `entitlement-projector` | `audit_config_invalid`, `audit_engine_tls_unverified`, `audit_finished`, `audit_engine_failed`, `audit_refused`, `audit_output_failed` | read-only `audit` mode (`internal/audit/run.go`) |
| `entitlement-projector` | `hydration_evidence_config_invalid`, `hydration_evidence_engine_tls_unverified`, `hydration_evidence_digest_mismatch`, `hydration_evidence_written`, `hydration_evidence_markers_read`, `hydration_evidence_refused`, `hydration_evidence_engine_failed`, `hydration_evidence_output_failed` | read-only `hydration-evidence` mode (`internal/hydrationevidence/run.go`) |
| `authz-sidecar` | `panic.recovered` | recovered panic in the HTTP or geography path (`internal/observability/recovery.go:18-21`) |
| `authz-sidecar` | `authz.model_fence.opened`, `authz.model_fence.recovered`, `authz.model_fence.unverified`, `authz.model_fence.closed` | model fence transition (`internal/health/model_fence.go:133-149`) |
| `authz-sidecar` | `sentry.configuration`, `sentry.spotlight.unsupported`, `sentry.flush` | Sentry boot configuration, unsupported Spotlight setting, exit flush (`internal/observability/sentry.go:38,159`; `cmd/authz-sidecar/main.go:101-103`) |
| `authz-sidecar` | `authz.cache.cleared`, `authz.cache.clear_refused` | emitted (CACHE-1 P5, `authz-sidecar` `ac89ce0`: `internal/observability/cache_clear.go:18-20`; `internal/httpserver/clear_audit.go:84,94` (at `6135113`)): one terminal audit event per `POST /internal/authz/cache/clear` attempt, `authz.cache.cleared` at info (warn when `outcome` is `partial`) and `authz.cache.clear_refused` at warn, sampled to at most one line per second per `reason` per replica with `suppressed_since_last_log` (the counter stays unsampled). Fields: `actor_user_id`, `actor_project_id`, `scope`, `project_id`, `user_id` (subject and decision scopes), `requested_items`, `cleared`, `mechanism`, `outcome` (`partial` after a partial `UNLINK`), `code`, `reason` (`disabled`, `cidr`, `gateway_credential`, `identity`, `permission`, `tenant`, `rate_limited`, `shed`, `validation`, `unavailable`; `clear_audit.go:15-26`), `peer_ip`, `request_id`, trace and span ids. Never logged: object ids, locations, keys, tokens, secrets (`authz-sidecar: docs/integrations/gateway/authz-sidecar-contract.md:654`) |
| `authz-sidecar` | `authz.cache.clear_started` | info; the audit record of an accepted clear, written after the body is validated and the actor bucket admits it, and before the fleet cooldown and any Redis mutation; the record shape is that of `authz.cache.cleared`. It fails closed: when it cannot be written, the clear returns `503` `DEPENDENCY_UNAVAILABLE` and mutates nothing (`authz-sidecar` `dd02250`: `internal/observability/cache_clear.go:18-20`; `internal/httpserver/clear_audit.go:84,94` (at `6135113`); `internal/httpserver/clear.go:30,213-220`) |
| `authz-sidecar` | `authz.cache.clear_route.enabled` | info at startup when the clear route is mounted; fields `allowed_cidrs` and `gateway_keys` are counts, never values (`authz-sidecar: cmd/authz-sidecar/main.go:161-162`) |
| `authz-sidecar` | `authz.decision_cache.armed`, `authz.decision_cache.disarmed` | decision cache (mode `redis`) armed at info once the redis-mode lease is held; disarmed at warn when the lease cannot be renewed for its 30 s TTL and decisions go to the engine (`authz-sidecar: internal/decisioncache/cache.go:507-530`) |
| `authz-sidecar` | `authz.decision_cache.global_token_rotated` | info when a replica finds no redis-mode lease and rotates the global token before creating the lease (`authz-sidecar: internal/decisioncache/cache.go:566-567`) |
| `authz-sidecar` | `authz.decision_cache.mac_mismatch` | warn when a cached entry fails MAC verification and is served from the engine; at most one line per second with `mismatches_since_last_log`; no key, token, user or object (`authz-sidecar: internal/decisioncache/cache.go:43,592-605`) |
| `authz-sidecar` | `authz.decision_cache.breaker_open` | warn once per opening of the decision-cache Redis breaker; fields `consecutive_failures`, `cooldown_ms` (`authz-sidecar: internal/decisioncache/guard.go:68-88`) |
| `authz-sidecar` | `authz.decision_cache.arm_failed` | warn when an arm or lease-renewal attempt of the redis-mode lease fails, the first attempt included; at most one line per lease TTL (30 s); fields `error_class`, a closed set (`redis_unavailable`, `timeout`, `auth`, `oom`, `other`; Redis reply words such as NOAUTH or WRONGPASS are classifier inputs only, never emitted), and `failures_since_last_log`, the integer count of attempts folded into the line; no key, token, user or object (`authz-sidecar` `051ef44`: `internal/decisioncache/cache.go:598`, classifier `internal/decisioncache/errorclass.go`). The disarmed warn also carries `error_class` from the same set |
| `authz-sidecar` | `authz.decision_cache.token_rollback` | warn when a scope token is read back at the value before the latest one (a failover, restore or replay that may have undone a clear); at most one line per second per replica; fields `token_scope` (`project`, `subject`, `global`) and `rollbacks_since_last_log`; no key, token, user or object (`authz-sidecar` `dd02250`: `internal/decisioncache/cache.go:46,610-644`) |
| `authz-sidecar` | `authz.cache_status.invalid` | warn when a decision's cache status falls outside the closed set and is reported as `bypass`; at most one line per interval; fields `cache_status`, `request_id`, `trace_id` (`authz-sidecar: internal/decision/engine.go:272-288`) |
| `authz-openfga` | none | it defines no structured logging; delivery and fixture scripts print CLI refusal lines with exit codes, and the engine writes upstream JSON logs (`authz-openfga: scripts/openfga/delivery.py:1266-1269`, `docker-compose.yml:37`) |

A row marked planned is an accepted design that no code emits yet; it is not verified against source.

Service-specific error codes (authorization mesh), same rules as above (UPPER_SNAKE, append-only):

| Owner | `code` | Status | Emitted when |
|---|---|---|---|
| `authz-sidecar` | `AUTHZ_CACHE_CLEAR_RATE_LIMITED` | emitted (CACHE-1 P5, `authz-sidecar` `ac89ce0`) | `429` on `POST /internal/authz/cache/clear` when the actor bucket, the replica bucket or the fleet cooldown refuses the request; `Retry-After` header and `meta` `{"retry_after_seconds":n}` (`authz-sidecar: internal/httpserver/clear.go:29,201-206,224-233`; `internal/observability/cache_clear.go:21`; `docs/integrations/gateway/authz-sidecar-contract.md:644`). |
| `authz-sidecar` | `NOT_FOUND` | emitted (`authz-sidecar` `ac89ce0`) | `404` catch-all envelope for every unmatched path and for the clear route while it is disabled or the peer is refused; the body is one fixed byte string, so those cases are indistinguishable (`authz-sidecar: internal/httpserver/envelope.go:16,25,52-54,73-82`) |
| `authz-sidecar` | `METHOD_NOT_ALLOWED` | emitted (`authz-sidecar` `ac89ce0`) | `405` catch-all envelope with an `Allow` header when a known fixed route (`/internal/authz/check`, `/api/health`, `/api/ready`) receives another method (`authz-sidecar: internal/httpserver/envelope.go:17,65-82`) |
| `authz-sidecar` | `READINESS_OPENFGA_CONFIG_MISSING`, `READINESS_OPENFGA_STORE_PIN_MISSING`, `READINESS_OPENFGA_MODEL_PIN_MISSING`, `READINESS_OPENFGA_API_UNAVAILABLE`, `READINESS_OPENFGA_MODEL_FENCE_INVALID`, `READINESS_OPENFGA_MODEL_FENCE_UNAVAILABLE` | emitted (`authz-sidecar` `48ce029` registry) | `503` readiness check codes inside a `SERVICE_NOT_READY` body: OpenFGA url not configured, no store pin, no model pin, API did not answer, engine model differs from the bundle model, engine model could not be verified |
| `authz-sidecar` | `READINESS_OPENFGA_CONFIG_READY`, `READINESS_OPENFGA_STORE_PIN_READY`, `READINESS_OPENFGA_MODEL_PIN_READY`, `READINESS_OPENFGA_API_READY`, `READINESS_OPENFGA_MODEL_FENCE_READY` | emitted (`authz-sidecar` `48ce029` registry) | `200` readiness check codes inside a `SERVICE_READY` body, one per passing check above |

Each service's complete code and event list is its registry, `docs/contracts/<service>/errors/error-codes.json` (reference 10). `authz-sidecar` committed its registry in `48ce029`. This table names only the codes no other owner defines. `AUTHZ_ALLOWED`, `AUTHZ_DENIED`, the location codes and the other `AUTHZ_*` decision codes belong to `26-request-time-authorization-openfga/40-decision-and-enforcement.md`. `AUTH_*` and `TENANT_CONTEXT_*` belong to `$alaa-trust-gateway-auth` `references/50-deny-codes.md`. `INPUT_VALIDATION_FAILED` belongs to reference 10.

Conformance gaps against the shared names above:

| Service | Shared names emitted | Shared names not emitted |
|---|---|---|
| `entitlement-api` | `http.request.completed`, `http.request.failed`, `request.shed` (in-flight cap and body budget), `dependency.unavailable` (database pool or pooler refusal; entitlement-api `f6a77d1`) | all others; readiness, trust, denial, and validation outcomes return only a response, and broker outages log without `event` |
| `entitlement-projector` | `queue.publish.failed` (receipt or notice publish not confirmed) | all others; readiness is metric-only, and startup and exit logs carry no `event` (`cmd/projector/main.go`) |
| `authz-sidecar` | `http.request.completed`, `http.request.failed`, `authz.denied`, `input.validation.failed`, `auth.context.invalid`, `request.shed`, `service.readiness.failed` | `service.readiness.recovered`, `dependency.call.failed`, `dependency.unavailable` (OpenFGA non-200 answers log without `event`), `queue.publish.failed` (no broker) |

All three Go services emit `panic.recovered` with `PANIC_RECOVERED`, which the shared list now names (registered 2026-10-10 from existing emitters).

## Domain event envelope

### Scope: which messages this envelope binds

Apply this test before applying anything else in this section, because the envelope binds only half of the
messages a service produces, and rewriting the other half breaks working code.

**Does any consumer outside this repository read this message?**

- **No.** The message is enqueued and consumed inside this repository — a Laravel job the service dispatches
  and handles itself, a framework event the service listens to itself, an async continuation of its own
  request. The framework's own job and event mechanism governs it entirely. This contract states nothing
  about its body, its serialization, or its field names, and an agent does not convert it. A Laravel job
  payload is a serialized job by design, and rewriting it into this envelope stops the framework from
  dispatching it at all.
- **Yes.** The message crosses to another repository — another service consumes it, or this service is
  instructing another service to act. The envelope below is binding, with no per-service variation.

Make the boundary observable, not a judgement call. A message is inter-service when a repository other than
the producing one contains a consumer bound to it: a queue declaration, a listener registration, or a row in
`23-queue-and-exchange-registry.md` naming a different service in its `Consumes` column. A message is
internal when the only code that reads it lives in the same repository that writes it — `auth` enqueuing an
SMS job and `auth` handling it is internal even though the job travels through the shared broker, because no
second repository binds to that queue.

Two consequences worth stating so they are not rediscovered:
- Transport does not decide the answer. A message on RabbitMQ can be internal, and an internal message that
  later gains an out-of-repository consumer becomes inter-service on that day and adopts this envelope in the
  same change that adds the consumer.
- The name is governed either way. `23-queue-and-exchange-registry.md` registers the queue name of an
  internal job as well as an inter-service message, because two services declaring a queue called `default`
  on one vhost collide whatever is inside their messages.

### The envelope

The event names above name **log records**. This section names **broker messages**: the durable facts a
service publishes for other services to consume. One service publishing `event_name`, a second `event_type`,
and a third `event` means no consumer can be written once and no operator can search the fleet for the same
field, which is the drift this section removes.

Every Ala domain event published to a broker is a JSON object with snake_case keys at every level,
including nested objects, and carries exactly these fields:

| Field | Required | Value |
|---|---|---|
| `message_id` | yes | lowercase UUIDv7; the logical message identity, never the broker delivery tag |
| `message_type` | yes | the event name, `<service>.<aggregate>.<action>.v<major>`, lowercase snake_case segments |
| `message_version` | yes | positive integer equal to the `<major>` in `message_type` |
| `occurred_at` | yes | RFC3339 UTC instant at which the fact became true, not the publish time |
| `producer_service` | yes | the canonical service identity from `10-core-service-contract.md` |
| `correlation_id` | yes | the `request_id` of the request that produced the fact; `message_id` when no request produced it |
| `causation_id` | optional | the `message_id` of the message that caused this one |
| `idempotency_key` | yes | stable across every republication of the same fact, so a consumer deduplicates on it |
| `traceparent` | yes | the canonical `traceparent` of the producing request, so the consumer continues the trace |
| `project_id` | yes | the public UUIDv7 project identifier; `null` only for a fact the owning repository documents as platform-scoped |
| `aggregate_type` | yes | the owning aggregate, singular lowercase snake_case: `session`, `comment`, `grant` |
| `aggregate_id` | yes | the public identifier of the aggregate instance |
| `aggregate_version` | optional | positive integer; required when a consumer must reject an out-of-order state change |
| `payload` | yes | JSON object carrying the fact's own fields |

Rules:
- These are the same field names as the notification command envelope in
  `27-notification-service-contract.md`, deliberately: a service writes one serializer and one consumer
  base for both. A command carries no `project_id` and no `aggregate_*`; an event carries them. Where the
  two files disagree about a command, that file wins for commands.
- `event_id`, `event_name`, `event_type`, `event_version`, `payload_version`, `producer`, `actor`,
  `resource`, `context`, `data`, and `headers` are not fields of this envelope. A service emitting any of
  them renames it to the field above with the same meaning, through the deprecation procedure in
  `22-failure-load-and-deprecation-contract.md`.
- The envelope carries identity, ordering, and correlation only. The acting user, the changed values, the
  reason, and every other domain fact go inside `payload`, so that adding a domain field never changes the
  envelope and a consumer can validate the envelope without knowing the domain.
- Identifiers inside `payload` follow the public-identifier rule in
  `25-end-to-end-flow-and-boundaries.md`. A database integer in a payload is a violation there; this
  section does not create an exception to it.
- The key set is closed. A service that needs a field the table does not have puts it in `payload` or
  proposes the field here first; it does not add a top-level key locally.

Observable that decides compliance: one committed fixture per published `message_type` in the producing
repository, asserted against by a test, whose top-level key set equals the required fields above plus any
optional field the producer actually sets.

## Broker exchange, routing key, and queue names

`23-queue-and-exchange-registry.md` owns them: the event-versus-command split, the naming grammar for every
exchange and queue, the prohibition on the AMQP default exchange and on a shared `events` exchange, the
consumer-owns-its-queues rule, and the registry of every name that exists in the fleet or is owed to it.
Read it before declaring any topology, and register a new name there before the declaring code merges.

This file owns only the field the routing key carries: `message_type`, defined in the table above.

## Probe-noise rule

Rules:
- suppress low-value `http.request.completed` logs for successful `/api/health`
- suppress low-value `http.request.completed` logs for successful `/api/ready`
- keep not-ready responses observable
- keep unexpected failures observable
- if readiness transition tracking exists, use `service.readiness.failed` and `service.readiness.recovered`

## Metrics boundary rule

When the service emits metrics from the request middleware layer, keep labels bounded.

Allowed defaults:
- templated route or route name
- HTTP method
- status code or status class
- service
- env

Forbidden defaults:
- `user_id`
- `project_id`
- raw path
- query string
- exception message as a metric label

Use `24-metric-registry.md` for the exact `alaa_*` metric family names and the metric naming and unit-suffix rules. Use `$alaa-observability-soc` for which families a service is required to expose, the label allow and deny lists beyond the request middleware layer, histogram and exemplar policy, and Collector ownership.

## `RequestObservabilityMiddleware` contract

For Laravel services, apply this middleware early on `/api/*` traffic.

Preferred order:
1. `RequestObservabilityMiddleware`
2. tenant or project normalization needed before bindings
3. `SubstituteBindings`
4. `ResolveUserMiddleware` or the equivalent trusted-user normalization layer
5. controller and policy-facing code

Required behavior:
- compute canonical `X-Request-Id`
- compute canonical `traceparent`
- derive and expose `trace_id` from the canonical trace context
- store request-scoped correlation context on the request
- capture request start time
- attach `X-Request-Id` and `traceparent` to API responses
- preserve enough request context for the exception handler to attach the same headers to rendered API error responses
- emit `http.request.completed` or `http.request.failed` with the exact code rules above
- emit bounded-cardinality HTTP metrics when the repository has a metrics boundary

Required support components:
- request context normalizer
- request-id generator and validator
- `traceparent` parser and generator
- `trace_id` extractor for logs, OTLP log records, and request attributes
- route-template or route-name resolver
- request-duration capture
- log-context sharing mechanism
- exception-path header attachment hook
- probe-noise decision logic
- metrics emission boundary

Laravel implementation rules:
- use the current Laravel logging-context sharing mechanism
- keep request state off static properties
- stay Octane-safe
- keep response-header attachment in middleware or Resource response boundaries, not in services
- when middleware rethrows, have the exception handler read the shared request context and attach `X-Request-Id` and `traceparent` to rendered API error responses
- inspect the current stack before reordering middleware blindly
