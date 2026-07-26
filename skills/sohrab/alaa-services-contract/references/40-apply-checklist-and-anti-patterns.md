# Apply Checklist And Anti-Patterns

## Step-by-step apply checklist

1. Read `AGENTS.md`.
2. Identify the repository role and service mode.
3. Read the smallest owning reference file first.
4. Read `21-alaa-platform-observability-directive.md` whenever observability design, OTLP configuration, queryable `trace_id`, exception delivery, SigNoz, Sentry, Prometheus metrics, or Collector topology is in scope.
5. Confirm the canonical Ala service identity.
6. Confirm the exact route-family split.
7. Align `/api/health` and `/api/ready` to the exact contract.
8. Align exact readiness check names and codes.
9. Align `X-Request-Id`, `traceparent`, queryable `trace_id`, request logging, and stable event/code naming.
10. Align `RequestObservabilityMiddleware` and `ResolveUserMiddleware` semantics where required.
11. Align public `project_id` fields as canonical UUIDv7 inputs resolved server-side after validation, and keep trusted `X-Project-Id` normalization inside one request-context builder.
12. Align permission configs with `alaa-permission-catalog` generated outputs when the task touches `config/permissions.php`, generated Go permission maps, the generated TypeScript `permission-catalog.ts`, permission names, bitmap ids, `X-Access`, or drift checks.
13. Verify backend decisions use exact permission checks and do not add role-based authorization or other role-dependent behavior while `28-backend-permission-authorization-and-role-freeze.md` remains active.
14. Align the observability names and values in `21-alaa-platform-observability-directive.md`, the metric names in `24-metric-registry.md`, and the broker names in `23-queue-and-exchange-registry.md` when the task touches logs, traces, metrics, queues, DBs, dependencies, or workers, and take requirement levels and gates from `$alaa-observability-soc`.
15. Align every outbound call, retry, connection pool, and ingress admission decision to `22-failure-load-and-deprecation-contract.md` when the task adds or changes any of them.
16. Add or align exact response envelopes, exact headers, exact event names, exact code naming, and exact metric names where the contract owns them.
17. Update docs, Postman, and runbooks in the same patch when public or operational behavior changes.
18. Run focused tests for every changed contract surface. A test that would still pass against a plausible broken
    implementation of that surface does not count as one; `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns how
    a test is judged to be a test and at which proof level its result may be reported, and this item owns only that
    the run happened for every surface the change touched.
19. When the change removes or renames a contract surface, run the deprecation procedure in `22-failure-load-and-deprecation-contract.md` instead of deleting the surface directly.
20. Report blockers explicitly when exact convergence is not possible, using the three-case rule in `SKILL.md`.

## Short service adoption checklist

When applying this skill to a service, finish by checking:
- `/api/health`
- `/api/ready`
- `X-Request-Id`
- `traceparent`
- queryable `trace_id`
- structured JSON logs
- exact event/code naming
- exception evidence through OTel/SigNoz and Sentry when present
- Prometheus endpoint and applicable baseline metric families
- bounded labels
- OTLP exporter endpoint via env
- no vendor-specific backend coupling

## Minimum validation checklist

### Operational
- `/api/health` is public and dependency-free
- `/api/ready` is public and uses the exact envelope
- `service` comes from the canonical service config
- healthy and not-ready paths are covered
- `ops:ready --json` matches the route when implemented

### Observability
- missing invalid `X-Request-Id` generates lowercase UUIDv7
- valid incoming `X-Request-Id` is preserved
- missing invalid `traceparent` generates a fresh valid value
- valid incoming `traceparent` is preserved
- `trace_id` is directly queryable in structured logs and OTLP log records
- `/api/health` and `/api/ready` return `X-Request-Id` and `traceparent`
- rendered API error responses after exceptions still return `X-Request-Id` and `traceparent`
- no service code, config, docs, tests, or emitted headers still mention `X-Correlation-Id`
- successful probes stay low-noise
- readiness failure and request failure logs use the exact event and code rules
- logs are structured JSON in production
- unhandled and actionable handled exceptions are recorded on spans and emitted as structured logs; Sentry is used when present but is not the only exception path
- traces and logs use the OTLP path without backend-specific code branches
- metrics use bounded labels only
- real resource identifiers appear only in logs or trace attributes when needed, never as metric labels
- the internal metrics endpoint is scrapeable and not treated as a public client API
- OTLP exporter endpoint and protocol come from env or deployment config
- HTTP latency uses histograms, not summaries, unless a documented exception exists
- Pushgateway is not used for normal long-lived service metrics
- the service exposes the baseline metric families that apply to it
- if a Collector gateway is part of the task, queue and exporter failure behavior is observable

### Failure behaviour and load
- every outbound HTTP, database, cache, and broker client is constructed with an explicit timeout
- the gateway sets `X-Request-Deadline-Ms` on every forwarded request from `GATEWAY_REQUEST_DEADLINE_MS`, default `180000`, and strips any client-supplied value
- no service defines an env variable that sets, overrides, or extends the edge deadline
- each service reads `X-Request-Deadline-Ms` at ingress, clamps every outbound per-attempt timeout to the remainder, refuses with `503 DEPENDENCY_UNAVAILABLE` without calling anything when the remainder is non-positive, and forwards the decremented value on every internal hop
- a service called without the header falls back to its own route default rather than running unbounded
- `alaa_requests_deadline_exhausted_total` is exported by every service that implements the deadline
- the retry budget is at most 3 total attempts, with exponential backoff and full jitter, never a fixed delay
- no retry exists on the gateway authorization hop or on a readiness dependency probe
- every retried `POST` carries an `Idempotency-Key` that is byte-identical across retries of one logical operation
- a route that cannot be made idempotent records `idempotent: false` and its callers retry zero times
- no client library retry is nested inside this skill's retry budget for the same call
- an unreachable `auth` never causes a local user projection to answer an authorization or entitlement question
- an unreachable authorization runtime never causes a backend to allow the request or to check OpenFGA itself
- an unreachable notification broker leaves the command in a durable outbox, never dropped and never sent over business HTTP
- the database pool has an explicit maximum, an explicit acquire timeout, and worker containers have their own maximum
- `replicas * max_connections_per_container` stays at or below 60% of the target Postgres `max_connections`
- ingress sheds a product request with `503` and `Retry-After: 1` at the in-flight maximum instead of queueing it
- `/api/health` and `/api/ready` are never shed
- `alaa_http_requests_in_flight`, `alaa_db_pool_in_use`, and `alaa_queue_backlog` are exported wherever the corresponding bound is set

### Contract deprecation
- every deprecated surface carries a recorded `Deprecated <date>, removed after <date>` in its owning reference file
- the replacement surface is documented beside the deprecated one
- the window meets the minimum for that surface class: 90 days public, 30 days service-to-service, 0 days `reserved`
- the deprecation is recorded in this skill, in the owning repo's release notes, and as an issue in every named consuming repository
- removal happened only after the window ended and every named consumer moved, and it deleted the compatibility code, tests, docs, and API artifacts together

### Response envelopes, codes, and pagination
- every `4xx` and `5xx` body is `{"error":{"status","code","message","meta"}}`, with `meta` an object and
  `status` equal to the status line
- a `4xx` and a `5xx` saved example both exist and both satisfy that shape
- `/api/ready` `503` uses the readiness envelope, not the error envelope
- no `4xx` or `5xx` returns an empty body; where the runtime cannot render one, the repository records which
  component does
- every emitted code matches `^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$` and appears in one committed registry a test reads
- list routes accept `cursor` and `limit`, reject `page`, `per_page`, and `offset`, and return both
  `meta.next_cursor` and `meta.prev_cursor` as a string or `null`, with neither key omitted
- any offset list satisfies all five conditions of the admin-table exception in
  `25-end-to-end-flow-and-boundaries.md` and declares its own response envelope rather than using `meta`
- a `limit` above the documented maximum is rejected, not clamped
- no payload field carries an auto-increment database id, except the actor identifier received in `X-User-Id`
- readiness `checks` is an object keyed by check name, not an array, and every item carries `status`,
  `required`, `code`, and `message`
- `error.meta` carries only the four permitted kinds of detail, carries no exception text, SQL, internal
  identifier, secret, or extra PII, and one `code` always produces one `meta` key set
- every field named `project_id` is a UUIDv7 string on the HTTP payload, the event envelope, the log field,
  and the cache key
- no payload, event, or log carries a database integer under any name other than the recorded actor-identifier debt

### Async messages
- the internal-versus-inter-service test in `20-operational-and-observability-contract.md` was applied
  before any message was reshaped, and no framework-internal job was converted to the domain envelope
- every published domain event carries the exact envelope field set, with `payload` holding the domain fields
- the exchange is `<service>.events` and the routing key equals `message_type` byte-for-byte
- no domain event is published to the default exchange, and no publisher binding resolves to a log or no-op
  sink outside a test
- every consumer sets an explicit prefetch at its construction site or in committed configuration
- every exchange and queue name in the repository has a row in `23-queue-and-exchange-registry.md`, and a
  new name was registered there before the declaring code merged
- a command goes to the receiver's command queue and an event goes to the producer's own topic exchange
- every metric name in the repository has a row in `24-metric-registry.md`, and a new name was registered
  there before the emitting code merged

### Trusted ingress
- missing blank invalid `X-Project-Id`
- missing invalid `X-User-Id`
- missing invalid zero-known-permission `X-Access`
- `X-Access` decoding against the generated, committed service permission config
- exact permission checks cover allow and deny behavior without a role-derived fallback
- `X-User-Roles` presence, absence, or value cannot change authorization, access level, scopes, response shape, routing, validation, features, workflows, or side effects
- catalog drift check before and after permission-config changes when `alaa-permission-catalog` is available
- invalid `X-User-Mobile`
- malformed `X-User-Fname` or `X-User-Lname`
- malformed `X-Location-*` values
- parity between `$request->user()` and `Auth::user()`
- parity with any legacy guard still in use

### Public project selector
- public `project_id` accepts a mapped canonical UUIDv7
- public `project_id` rejects integer `1` and string `"1"`
- unmapped UUIDv7 returns validation errors
- services receive the resolved internal project id only after validation
- docs, Postman, and examples do not teach internal ids for public request bodies

### Laravel response boundary
- successful `/api/*` responses use the exact `data` envelope
- `meta` and `links` follow the contract
- Resources do not leak internal fields
- docs and Postman examples match the actual public response shape

## Review checklist

Flag a problem when you see any of these:
- `/api/health` calls PostgreSQL, Redis, RabbitMQ, ClickHouse, or another service
- `/api/ready` depends on tokens, cookies, OTP, or end-user state
- the readiness envelope or key names differ from the contract
- a new or refactored Ala service invents repo-local GitLab CI instead of defaulting to `service-ci-kit`
- `.gitlab-ci.yml` is not a thin wrapper in a repo that should follow the shared kit
- shared `ci/scripts/*` or local semantic-release helper trees appear in a service repo without an explicit blocker
- the repository diverges from the shared kit baseline without documenting the reason
- `service` returns a framework or runtime name
- `X-Correlation-Id` remains anywhere in service code, config, tests, docs, or emitted headers after the migration
- `X-Trace-Id` is still treated as a response-header requirement
- `trace_id` is missing as a queryable field and operators must parse `traceparent`
- request or readiness logs invent alternate event names for the same flow
- logs are not structured JSON in production
- the service hard-codes vendor-specific telemetry backends instead of targeting OTLP and the shared metrics contract
- exceptions are observable only in Sentry, or only in local logs when Sentry is absent
- metrics use unbounded labels or raw user or tenant identifiers
- a public route exposes the internal metrics endpoint
- a normal long-lived service uses Pushgateway for app metrics
- trusted headers are parsed in controllers, policies, or repositories
- a backend uses `rol`, `X-User-Roles`, a stored role snapshot, or a role-derived tier for authorization or any other runtime decision
- a backend adds a role resolver, role-to-permission map, role-derived fallback, role middleware, or role-dependent tests while the provisional freeze is active
- a privileged-looking role bypasses a missing permission or OpenFGA denial
- `config/permissions.php` invents or hand-renumbers bitmap ids instead of consuming `alaa-permission-catalog` generated output
- a generated Go permission map or the generated TypeScript `permission-catalog.ts` is hand-edited instead of regenerated and reapplied
- frontend code hand-writes permission strings or bitmap ids, decodes the access token itself, or treats an unverified UI permission hint as an authorization decision
- permission config changes are applied across multiple services in one implicit phase
- a service extraction reuses legacy VOD bitmap ids for new `content_*` permissions
- public `project_id` is normalized to an integer before validation
- tests or Postman examples send internal numeric `project_id` values for public routes
- `$request->user()` and `Auth::user()` can diverge within one request
- Laravel services return transport-shaped arrays or raw models instead of Resource boundaries
- docs or API artifacts drift from implementation
- compact trusted name and location headers are re-parsed in multiple layers instead of one normalization path
- a repository keeps old and new trust contracts active in parallel without an explicit migration blocker
- a repository invents location-name lookup behavior even though the compact contract only carries ids
- an outbound internal call has no explicit timeout, or retries a non-idempotent operation with no idempotency key
- a retry uses a fixed delay, retries a `4xx` other than `429`, or nests inside a client library's own retry
- a backend allows a request, or performs its own OpenFGA check, because the authorization runtime was unreachable
- a connection pool is unbounded, has an unbounded acquire wait, or a worker container inherits the HTTP pool default
- a product request waits in an application-level queue instead of being shed at the in-flight maximum
- `/api/health` or `/api/ready` is subject to shedding or rate limiting
- an error body uses a framework default shape such as `{"message": ..., "errors": {...}}`, omits `meta`, or
  sets `meta` to `null`
- an error code is lowercase, or exists only in a documentation artifact no test reads
- a list route reads `per_page`, `page`, or `offset` without satisfying all five conditions of the
  admin-table exception, or a repository mandates keyset pagination in its own `AGENTS.md` while its code
  calls an offset paginator or no paginator at all
- an event envelope uses `event_id`, `event_name`, `event_type`, `event_version`, `payload_version`, `data`,
  or `headers` instead of the canonical field names
- a routing key is rewritten from the event name, or a domain event is published to the default exchange
- a service other than the gateway parses, verifies, or refreshes an end-user bearer token
- a service that makes authorization decisions has no executable read of `X-Access`
- an application metric name does not begin `alaa_`, or is emitted without a row in `24-metric-registry.md`
- an exchange or queue is declared with no row in `23-queue-and-exchange-registry.md`, or a command is
  published to the sender's own exchange instead of the receiver's command queue
- an internal framework job is rewritten into the domain event envelope, or an inter-service message is left
  in the framework's own shape
- an error `meta` carries exception text, SQL, a stack fragment, an internal identifier, a secret, or PII the
  request did not already carry, or one `code` produces two different `meta` key sets
- a field named `project_id` carries an integer in a payload, an event, a log field, or a cache key
- a new numeric identifier is added and justified by citing the actor-identifier exception
- a contract surface is deleted or renamed without the deprecation procedure, or a deprecation carries no removal date

## Anti-patterns

- treating the skill as optional guidance instead of a hard contract
- copying only part of the `/api/ready` contract and changing the rest locally
- leaving `X-Correlation-Id` anywhere in the service after migrating to `X-Request-Id`
- inventing local event names that conflict with `$alaa-observability-soc`
- inventing local auth error names that conflict with `$alaa-trust-gateway-auth`
- treating user roles as backend authority before this skill explicitly finalizes and activates role semantics
- storing passive role metadata in a way that feeds authorization interfaces, high-cardinality metric labels, or undocumented retention
- keeping stale compatibility branches, helpers, tests, or docs for removed contract surfaces
- reintroducing duplicated GitLab CI logic into service repositories instead of updating `service-ci-kit` first
- scattering trusted-user normalization across controllers, policies, resources, and observers
- accepting storage ids such as `project_id: 1` from public clients instead of UUIDv7 project ids
- using one normalizer for both public `project_id` and trusted `X-Project-Id` when the public path must be stricter
- leaving helper responsibilities implicit so each agent re-invents them
- reviving the retired profile-blob trust surface instead of consuming the compact header projection
- pushing observability logic into app code that belongs in the Collector layer
- treating Sentry as the main observability backend instead of a focused exception, release, and developer-debugging layer
- calling a dependency with no timeout because it has always been fast
- retrying a call that has no idempotency guarantee, or generating a fresh idempotency key per attempt
- absorbing an authorization-runtime outage by allowing the request instead of failing closed
- keeping a compatibility alias alive past its recorded removal date, or deprecating a surface with no recorded date at all
- restating a requirement level, gate, or threshold that `$alaa-observability-soc` owns, or a reliability rationale that `$alaa-reliability-sla` owns
