# Fleet Conformance Snapshot — 2026-07-25

This file is **not a rule file**. It states no contract and overrides nothing. Every rule it references is
owned by a numbered reference file, and that file wins in every case. This file records one thing: which Ala
component satisfies which of those rules on 2026-07-25, and what each component that does not must change.

Read it when you are planning migration work, sequencing a fleet change, or deciding which repository to
open first. Do not read it to learn a rule; open the owning file named beside the rule.

**This snapshot goes stale.** It was produced from a survey of seven repositories at the commits below and
is accurate to nothing else. A conformance claim here that contradicts the repository in front of you means
the repository moved and this file did not; the repository wins, and the change that moved it updates this
file in the same effort.

| Component | Surveyed commit |
|---|---|
| `auth` | `2d062c2d843b7c502409e19599cd9b0c6336150b` |
| `comment` | `2a87f3986963bf5eefd04884aa2a807c046e1e00` |
| `content` | `922c5662c8e787c809184a065fa591f3296df9b4` |
| `entitlement-platform` (`entitlement-api`, `projector`, `authz-sidecar`) | `20ba532322fa599d285bd3316b9eb87870104ea` |
| `gateway` | `779aea869315a5853d49de264a99bb2df6087550` |
| `wa` | `691baf4473a78013087d4f5397fd2e9978b472ac` |
| `alaa-go-chi` kit | `f166b57e579e0dedf4a2954944f98d42d9538fd6` |

## How to refresh this file

Re-run the same twelve-section survey against each repository, one repository per run, answering from
executable code and committed artifacts with `file:line` evidence, and marking anything unproven `ABSENT` or
`UNDETERMINED` rather than inferring it. The sections are:

`SERVICE` (name, language and framework with version, runtime, surveyed commit SHA), then
`1. ERROR CONTRACT`, `2. HTTP SURFACE`, `3. IDENTIFIERS`, `4. AUTH AND TRUST`, `5. EVENTS AND ASYNC`,
`6. FAILURE BEHAVIOUR`, `7. CONCURRENCY AND LOAD`, `8. OBSERVABILITY`, `9. DATA`, `10. CONTRACT ARTIFACTS`,
`11. WHAT THIS SERVICE THINKS THE RULES ARE`, `12. DRIFT AND GAPS FOUND`.

Two survey habits are what made this file usable, so keep them: section 11 asks the repository what it
believes the shared rule is, which is how a doc-versus-code conflict becomes visible; and section 3 asks the
surveyor to *search* for internal identifier exposure rather than assume there is none.

## Index: the ten disagreements and where each rule now lives

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 1 | Single error envelope `{"error":{status,code,message,meta}}` | `10-core-service-contract.md` | `comment`, `content`, `entitlement-api`, `gateway`, kit | `auth`, `wa` |
| 2 | Error codes are UPPER_SNAKE, in one committed registry | `10-core-service-contract.md` | `comment`, `content`, `entitlement-api`, kit (casing) | `gateway`, `auth` (casing); `auth`, `content` (registry) |
| 3 | Keyset cursor pagination, `cursor`/`limit`, `meta.next_cursor` | `25-end-to-end-flow-and-boundaries.md` | kit; `entitlement-api` (keyset, cursor field unproven) | `auth`, `comment`, `content` |
| 4 | Public payloads carry public identifiers; one actor exception | `25-end-to-end-flow-and-boundaries.md` | `entitlement-api` (HTTP path), kit | `comment`, `auth`, `content` |
| 5 | One domain event envelope (`message_*` field vocabulary) | `20-operational-and-observability-contract.md` | none | `auth`, `content`, `comment`, `entitlement-api`; kit is closest |
| 6 | Exchange `<service>.events`, routing key is `message_type` verbatim | `20-operational-and-observability-contract.md` | none | `auth`, `content`, `entitlement-platform`, `comment`; kit enforces no format |
| 7 | A service that authorizes reads `X-Access` | `28-backend-permission-authorization-and-role-freeze.md` | `comment`, `content`, `entitlement-api`, kit | `auth` |
| 8 | One request deadline computed at ingress | `22-failure-load-and-deprecation-contract.md` | none | all seven |
| 9 | Every application metric name begins `alaa_` | `21-alaa-platform-observability-directive.md` | `auth`, `content` | kit; `comment`, `entitlement-platform`, `gateway`, `wa` unproven |
| 10 | Readiness `checks` is an object keyed by check name | `10-core-service-contract.md` | `comment`, `content` | kit |

Two further findings, same status as the ten:

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 11 | Every consumer sets explicit prefetch | `22-failure-load-and-deprecation-contract.md` | `entitlement-api`, `projector` (50) | `comment`, `content`, `auth`, kit |
| 12 | The gateway is the only end-user token verifier | `25-end-to-end-flow-and-boundaries.md` | all seven | none — freeze it |

Corrections to note, because the evidence did not support the first reading:
- #3: `entitlement-api` is keyset (`cursor` and `limit` reach the query services), but its survey shows
  responses wrapped only as `{"data":...}` by `writeData`; a `meta.next_cursor` field is not evidenced. It is
  keyset-conforming and cursor-field-unproven, not fully conforming.
- #4: `entitlement-api` retains `legacy_object_internal_id` in a migration column, which is schema residue,
  not a payload leak. Its survey states that a route deliberately returning a database integer is
  UNDETERMINED. Treat it as a survey question, not a confirmed violation.
- #9: `comment`'s survey catalogues metric label sets, not metric names; its prefix is unproven either way.
  The kit's bare names are quoted and confirmed. `entitlement-platform`, `gateway`, and `wa` metric names
  were all UNDETERMINED at survey time.
- #10: only the kit (array) and `comment` (object keyed by dependency) are literally evidenced. `content` is
  strongly implied by its readiness test. `auth` and `entitlement-api` list `checks` as a top-level key
  without evidencing its element type; both need a one-line answer in the next pass.

## Per-service migration list

### `auth`

`auth` is the service every other service depends on for identity, and it is the furthest from the shared
response contract. Sequence it first: every consumer that has to special-case `auth` today writes that
special case into its own SDK, and each one is a second migration later.

1. **Adopt the error envelope.** Replace the Laravel validation body
   `{"message": ..., "errors": {...}}` and the bare `{"code": ..., "message": ...}` bodies with
   `{"error":{status,code,message,meta}}`; validation detail moves to `meta.errors`.
   Rule: `10-core-service-contract.md`. Evidence: `tests/Feature/ApiJsonErrorFormatTest.php:32-56`;
   `app/Http/Controllers/Api/Auth/AuthController.php:95-105`; `bootstrap/app.php:65-69`. This is the largest
   single item in the fleet and it is public-observable, so it runs the 90-day window in
   `22-failure-load-and-deprecation-contract.md`.
2. **Uppercase the lowercase codes.** `session_expired`, `too_many_attempts`, `account_blocked`, and
   `refresh_token_compromised` become UPPER_SNAKE; the `OTP_*`, `TOTP_*`, and `READINESS_*` families already
   comply. Rule: `10-core-service-contract.md`. Evidence: `app/Services/Auth/TokenService.php:41-45`;
   `app/Http/Controllers/Api/Auth/AuthController.php:101-153`.
3. **Make the code registry executable.** `docs/contracts/auth/errors/error-codes.json:1-7` is documentation
   that no test reads while codes are emitted inline across controllers and middleware. Add the test that
   fails when the two diverge. Rule: `10-core-service-contract.md`.
4. **Replace `per_page` offset pagination with keyset.** Admin catalog lists call Laravel `paginate(...)`
   with a validated `per_page`. `auth`'s own `AGENTS.md:8` already mandates keyset, and its survey records
   this as its own DRIFT. Rule: `25-end-to-end-flow-and-boundaries.md`. Evidence:
   `app/Http/Requests/Admin/AdminCatalogIndexRequest.php:21`; `app/Services/Admin/AdminCatalogService.php:39-65`.
5. **Stop emitting the internal user id from `ProfileResource`.** `id => $this->resource->publicUserId ?? $user->id`
   falls back to the table key, and three tests assert the numeric value. The actor-identifier exception in
   `25-end-to-end-flow-and-boundaries.md` permits the gateway-projected numeric id in a field named
   `user_id`; it does not permit a resource's own `id` to be a table key. Evidence:
   `app/Http/Resources/V3/ProfileResource.php:35-37`; `tests/Feature/AuthSuccessResponseContractTest.php:66-80`.
6. **Emit the UUIDv7 project id in events.** The outbox envelope carries `"project_id": 42`, an internal
   integer, where `entitlement-api` carries a UUIDv7. A consumer cannot map that integer. Rule:
   `30-trusted-ingress-and-laravel-contract.md` (absolute) with the observable added there. Evidence:
   `app/Services/Messaging/RabbitMqOutboxPublisher.php:62-75`; `tests/Feature/OutboxRelayCommandTest.php:71-84`.
7. **Rename the event envelope fields** to `message_id`, `message_type`, `message_version`,
   `producer_service`, `correlation_id`, `traceparent`, `aggregate_*`, `payload`. Today it emits `event_id`,
   `event_name`, `payload_version`, and `headers`. Rule: `20-operational-and-observability-contract.md`.
   Evidence: `app/Services/Messaging/RabbitMqOutboxPublisher.php:62-75`.
8. **Stop rewriting the routing key.** `str_replace('_','-', str_replace('.v','.version-', $eventName))` turns
   `auth.session.created.v1` into `auth.session.created.version-1`, which no code search finds. Publish with
   the routing key equal to `message_type`. The exchange `auth.events` already conforms. Rule:
   `20-operational-and-observability-contract.md`. Evidence:
   `app/Services/Messaging/RabbitMqOutboxPublisher.php:20-23,57-60`.
9. **Read `X-Access`.** `auth`'s own `docs/contracts/auth/permissions.md:5-24` documents the gateway
   projecting `prm` into `X-Access`, and the survey found no executable read anywhere in `app`, `config`,
   `routes`, or `tests`; admin routes authorize from Spatie role middleware instead, which the freeze in
   `28-backend-permission-authorization-and-role-freeze.md` forbids. Evidence: `routes/api.php:63-75`;
   `app/Providers/AuthServiceProvider.php:28-33`.
10. **Set an explicit prefetch** on every queue consumer, and **compute the ingress deadline** in
    `RequestObservabilityMiddleware`. Rules: `22-failure-load-and-deprecation-contract.md`.
11. **Confirm the Passport `api` guard is unreachable.** `config/auth.php:19-22` configures a Passport guard
    while every protected route uses `auth:trusted_gateway` (`routes/api.php:43`). A configured but unrouted
    token verifier is a second verification policy waiting to be wired up, against the single-verifier rule
    in `25-end-to-end-flow-and-boundaries.md`. Either prove no route resolves it and record that, or remove
    it. Token *issuance* stays with `auth` and is unaffected.

### `comment`

1. **Publish for real.** `OutboxPublisherInterface` is bound to `LogOutboxPublisher`, so the service
   publishes nothing to the broker while its README describes durable downstream delivery. Every consumer
   that believes it is subscribed to comment events is receiving silence. Rule:
   `20-operational-and-observability-contract.md`. Evidence: `app/Providers/AppServiceProvider.php:37-43`;
   `app/Outbox/LogOutboxPublisher.php:1-30`.
2. **Declare `comment.events` and bind consumers to it.** No exchange or routing-key configuration exists;
   `config/queue.php:82-109` carries only a queue name. Rule: `20-operational-and-observability-contract.md`.
3. **Move the n8n relay envelope onto the canonical field names.** It emits `event`, `version`,
   `aggregate_id` as an integer, `actor_id`, and `context`. Rule:
   `20-operational-and-observability-contract.md`. Evidence:
   `app/Listeners/CommentEvents/EventRelayToN8n.php:118-136`.
4. **Stop emitting numeric `user_id`, `flagged_by`, `resolved_by`, and the internal `project_id`** from
   resources. `comment`'s own contract already forbids it, and its survey records this as its own DRIFT.
   The actor-identifier exception covers only `user_id` when the value is the one received in `X-User-Id`;
   `flagged_by` and `resolved_by` end `_by`, not `_user_id`, so rename them or carry public identifiers.
   Rule: `25-end-to-end-flow-and-boundaries.md`. Evidence: `app/Http/Resources/CommentResource.php:33-39`;
   `app/Http/Resources/ModerationFlagResource.php:31-41`; `docs/contracts/comment/api-reference.md:47-51`.
5. **Replace `per_page` page pagination with keyset.** Evidence:
   `app/Repositories/PostgresCommentRepository.php:48`; `app/Http/Requests/Comment/IndexCommentRequest.php:50-76`.
   Rule: `25-end-to-end-flow-and-boundaries.md`.
6. **Render a `5xx` body.** The renderers cover `ApiErrorException`, authorization, and validation; no
   unexpected-exception JSON renderer exists, so the generic `5xx` body is unproven. Add the renderer and a
   saved `5xx` example. Rule: `10-core-service-contract.md`. Evidence: `bootstrap/app.php:68-129`.
7. **Set prefetch**, and **compute the ingress deadline**. Rules:
   `22-failure-load-and-deprecation-contract.md`. Evidence: `config/queue.php:82-109`;
   `app/Http/Middleware/RequestObservabilityMiddleware.php:45-61`.
8. **Confirm the metric prefix.** The survey catalogued labels, not names. If the names are bare, prefix them
   `alaa_`. Rule: `21-alaa-platform-observability-directive.md`. Evidence:
   `app/Support/Observability/MetricCatalog.php:18-125`.

### `content`

1. **Add a paginator.** `content`'s `AGENTS.md:17-22` mandates keyset pagination, its course list returns a
   resource collection with no `paginate`, `simplePaginate`, or `cursorPaginate` call at all, and its tests
   mention `page` and `per_page`. This is the one service where the migration is additive rather than a
   replacement. Rule: `25-end-to-end-flow-and-boundaries.md`. Evidence:
   `app/Http/Controllers/Api/V2/CourseManagementController.php:23-35`;
   `tests/Feature/Api/V2/CourseListFilterTest.php:464-465`.
2. **Resolve `SectionResource`.** It emits `section_key` as the public `id`, and a saved Postman example
   shows a numeric `31`. Either `section_key` is a real public identifier, in which case document it and fix
   the example, or it is a table key, in which case it is a violation. Rule:
   `25-end-to-end-flow-and-boundaries.md`. Evidence: `app/Http/Resources/Api/V2/SectionResource.php:15-20`;
   `docs/postman/content.postman_collection.json:626-674`.
3. **Rename the event envelope fields.** It emits `event_id`, `event_name`, `event_version`, `producer`,
   `request_id`, `actor`, `resource:{type,id}`, and `data`; `request_id` becomes `correlation_id`, `data`
   becomes `payload`, `resource` becomes `aggregate_type`/`aggregate_id`, and `actor` moves into `payload`.
   Rule: `20-operational-and-observability-contract.md`. Evidence: `app/Models/OutboxEvent.php:60-77`.
4. **Rename the exchange from `events` to `content.events`.** The routing key already equals the event name
   and conforms as soon as the field is renamed to `message_type`. Rule:
   `20-operational-and-observability-contract.md`. Evidence:
   `app/Support/Content/RabbitMqIntegrationEventPublisher.php:15-28`; `config/events.php:10-14`.
5. **Publish a complete error-code registry.** The survey could not enumerate the ControlledOps codes from
   this repository, so no test can assert the set. Rule: `10-core-service-contract.md`. Evidence:
   `app/Providers/ControlledOpsServiceProvider.php:1-20`.
6. **Set prefetch**, and **compute the ingress deadline**. Rule:
   `22-failure-load-and-deprecation-contract.md`. Evidence: `config/queue.php:84-113`.
7. Already conforming and worth keeping: the error envelope including the debug-off `SERVER_ERROR` body,
   the `alaa_*` metric names, the readiness envelope, and the trusted-header set.

### `entitlement-platform` (`entitlement-api`, `projector`, `authz-sidecar`)

1. **Stop publishing to the default exchange.** `projector` publishes with exchange `""` and the queue name
   as routing key, which binds the producer to one consumer's queue name. Declare `entitlement.events` and
   bind consumers to it. Rule: `20-operational-and-observability-contract.md`. Evidence:
   `services/projector/internal/runtime/amqp.go:100-107`; `services/entitlement-api/internal/mq/types.go:1-16`.
2. **Rename the event envelope fields** — `event_id`, `event_type`, `aggregate_version`, `schema_version`,
   `producer` become the canonical names; `aggregate_version` keeps its name and meaning. Rule:
   `20-operational-and-observability-contract.md`. Evidence:
   `services/entitlement-api/internal/outbox/events.go:20-45,187-195`.
3. **Emit `meta.next_cursor`.** The query path is keyset, but responses are wrapped only as `{"data":...}`;
   confirm the cursor field name and align it. Rule: `25-end-to-end-flow-and-boundaries.md`. Evidence:
   `services/entitlement-api/internal/httpserver/errors.go:117-123`;
   `services/entitlement-api/internal/httpserver/admin.go:416-420`.
4. **Answer the `legacy_object_internal_id` question.** Confirm no current route or DTO returns a database
   integer, then drop the legacy column or document why it stays. Rule:
   `25-end-to-end-flow-and-boundaries.md`. Evidence:
   `services/entitlement-api/migrations/000003_public_object_ids_and_structured_reasons.up.sql:1-14,84-95`.
5. **Prefix the metric names `alaa_` and publish the catalog.** The exact exported names were UNDETERMINED
   because collectors are split across files; one catalog file per service makes the next survey cheap.
   Rule: `21-alaa-platform-observability-directive.md`. Evidence:
   `services/entitlement-api/internal/observability/metrics.go:1-220`.
6. **Confirm the readiness `checks` element type** is an object keyed by check name. Rule:
   `10-core-service-contract.md`. Evidence: `services/entitlement-api/internal/health/service.go:30-44`.
7. **Compute the ingress deadline.** The `context.Context` plumbing already reaches every outbound call, so
   this service is one middleware away; nothing at ingress sets a deadline today. Rule:
   `22-failure-load-and-deprecation-contract.md`. Evidence:
   `services/entitlement-api/internal/config/config.go:189-192`.
8. Already conforming and worth keeping: the error envelope with `meta`, UPPER_SNAKE codes, prefetch `50` on
   both consumers, manual acknowledgement after handler success, publisher confirms, the `.retry`/`.dlq`
   topology, `Idempotency-Key` on write routes, and UUIDv7 public identifiers.

### `gateway`

1. **Uppercase every gateway-owned error code.** `unauthorized`, `not_found`, `rate_limit_exceeded`,
   `backend_unavailable`, `missing_token`, `disallowed_alg`, `invalid_signature`, `verify_error`,
   `missing_exp`, `expired`, `not_yet_valid`, `bad_issuer`, `bad_audience`, `missing_claim_<claim>`,
   `invalid_role_claim`, and the `authz_*` family become UPPER_SNAKE. This skill already names the gateway's
   authorization codes in UPPER_SNAKE — `22-failure-load-and-deprecation-contract.md` cites
   `AUTHZ_SERVICE_UNAVAILABLE` — and the gateway's own
   `docs/errors-events-observability.md:132-137` uses that spelling too, so the config is the outlier
   against both. Rule: `10-core-service-contract.md`. Evidence: `haproxy/errors/401.http:1-6`;
   `charts/gateway/templates/configmap.yaml:340-479`.
2. **Render an error envelope for backend responses that carry none.** `wa` returns empty `404`, `405`, and
   `503` bodies through the gateway. HAProxy can return a JSON body on those statuses for that backend, and
   this is the component that can. Rule: `10-core-service-contract.md`. Evidence:
   `charts/gateway/values.vk.yaml:132-158`; `docs/postman/wa.postman_collection.json:501-592`.
3. **Add a `504` errorfile.** Connect and server timeouts are configured with no `504` mapping, so a gateway
   timeout returns whatever HAProxy defaults to rather than the envelope. Rule:
   `10-core-service-contract.md`. Evidence: `charts/gateway/templates/configmap.yaml:114-127`.
4. **Decide the deadline header.** The gateway is where a fleet-wide request deadline is cheapest to
   originate, and it forwards no deadline today. Rule: `22-failure-load-and-deprecation-contract.md`.
   Evidence: `charts/gateway/values.yaml:221-225`.
5. Already conforming and worth keeping, and it is the fleet's single most valuable convergence: the gateway
   is the only component that verifies a JWT, it strips client-supplied trusted headers before routing, it
   projects the frozen claim-to-header map, it fails closed on authz-sidecar unavailability, and it emits
   `X-Request-Id` plus `traceparent` with `trace_id` as a first-class log field.

### `wa`

`wa` is a Vector pipeline, not an application runtime. Do not migrate it by pretending otherwise; migrate it
by naming the component that renders each surface.

1. **Get an error envelope in front of it.** Vector's `http_server` source returns a fixed `202` and cannot
   render error bodies, so the gateway renders `4xx`/`5xx` for `/wa/*`, and `wa`'s `AGENTS.md` records that
   the gateway owns it. Rule: `10-core-service-contract.md`, empty-body clause. Evidence:
   `vector/wa-vector.yaml:12-29`.
2. **Serve the probe paths or alias them explicitly.** `GET /health` on `8687` answers today and the gateway
   aliases `/wa/api/ready` to it. Record that mapping in the `wa` repository, and align the Kubernetes probes,
   which are TCP checks on the ingest port and therefore prove only that a socket is open. Rule:
   `10-core-service-contract.md`, frozen surfaces clause. Evidence: `charts/wa/templates/deployment.yaml:67-76`.
3. **Read and store `traceparent`.** `X-Request-Id` is stored; trace context is neither read nor stored, so a
   watch event cannot be joined to the request that produced it. Rule:
   `20-operational-and-observability-contract.md`. Evidence: `vector/wa-vector.yaml:44-48`;
   `clickhouse/ddl/001_init.sql:19-32`.
4. **Validate the identifier formats it documents.** Its contract says playback ids are UUIDv7 and event ids
   UUIDv4; the runtime string-coerces whatever arrives. Either validate in the remap or delete the claim.
   Rule: `25-end-to-end-flow-and-boundaries.md`. Evidence: `vector/wa-vector.yaml:175-187`.
5. **Publish its metric names.** Vector `internal_metrics` are routed to a console sink and no metric name is
   declared in the repository, so no dashboard can be written against it. Rule:
   `21-alaa-platform-observability-directive.md`. Evidence: `vector/wa-vector.yaml:341-348`.
6. `wa` makes no authorization decision, so the `X-Access` obligation does not apply to it. Record that in
   its `AGENTS.md`, per `28-backend-permission-authorization-and-role-freeze.md`.

### `alaa-go-chi` kit

The kit is not deployed, which makes it the highest-leverage repository in this list: every rule it gets
right is inherited by every Go service built on it, and every rule it gets wrong is inherited the same way.

1. **Prefix every metric name `alaa_`.** `http_requests_total`, `http_request_duration_seconds`,
   `http_requests_in_flight`, `outbox_depth`, `outbox_oldest_age_seconds`, `outbox_publish_failures_total`,
   `job_lane_depth`, `job_lane_oldest_age_seconds`, `job_dead_depth`, `consumer_lag`, `pg_pool_wait_seconds`,
   `seed_runs_total`, `service_readiness`, `service_readiness_transitions_total`, and
   `http_server_error_total` are all bare. Rule: `21-alaa-platform-observability-directive.md`. Evidence:
   `obskit/metricnames.go:3-26`.
2. **Make readiness `checks` an object keyed by check name.** The kit emits an array of
   `{status,required,code,message}`; `comment` and `content` emit an object. Same field, two types, and no
   consumer can parse both. Rule: `10-core-service-contract.md`. Evidence: `readykit/report.go:18-37`.
3. **Always render `meta.next_cursor`.** The Go field is a string with `omitempty`, so the last page omits the
   key while `CONTRACTS.md:72-73` documents `null`. The kit's own survey records this as its own drift; the
   contract now resolves it in `CONTRACTS.md`'s favour. Rule: `25-end-to-end-flow-and-boundaries.md`.
   Evidence: `httpkit/envelope.go:8-10`.
4. **Give the consumer abstraction a required prefetch parameter.** `ConsumerChannel` exposes only
   `Consume(ctx, queue)`, so no service built on it can bound its consumer even when it wants to, while the
   kit's own `AGENTS.md:15` requires bounded consumers. Rule:
   `22-failure-load-and-deprecation-contract.md`. Evidence: `mqkit/consumer.go:29-31,58-66`.
5. **Enforce the routing-key and exchange grammar in `mqkit/topology.go`.** The validator requires non-empty
   strings only, which is how four services reached four conventions. Rule:
   `20-operational-and-observability-contract.md`. Evidence: `mqkit/topology.go:73-127`.
6. **Extend `mqkit/envelope.go` with the event fields.** It already carries the command vocabulary
   (`message_id`, `message_type`, `message_version`, `occurred_at`, `producer_service`, `correlation_id`,
   `causation_id`, `idempotency_key`, `traceparent`, `payload`); domain events add `project_id`,
   `aggregate_type`, `aggregate_id`, and optional `aggregate_version`. Rule:
   `20-operational-and-observability-contract.md`. Evidence: `mqkit/envelope.go:16-33`.
7. **Resolve the `400`-versus-`422` validation status.** `CONTRACTS.md:10-21` documents `422` while
   `httpkit/bind.go` emits `400` and `errkit` permits both. One status per code, or the shared contract test
   proves nothing. Rule: `10-core-service-contract.md`. Evidence: `httpkit/bind.go:59-74`;
   `errkit/envelope.go:114-116`.
8. **Add an ingress deadline helper**, so the deadline rule ships once rather than per service. Rule:
   `22-failure-load-and-deprecation-contract.md`.
9. Already conforming and worth keeping: the error envelope and its pre-marshaled canonical `500`, the
   UPPER_SNAKE code set with `FinalizeKnownCodes` registration, keyset-only pagination, the trusted-header
   parse with fail-closed defaults, receipt-based consumer idempotency, and the `contracttest` package —
   which is the right mechanism for enforcing everything in this file, and is currently the only one in the
   fleet.

## What the surveys could not determine

Ask these in the next pass; each one blocked a conformance verdict above.

- Exact metric names for `comment`, `entitlement-platform`, `gateway`, and `wa`. Only label sets, split
  collector files, or generated exporter names were visible. Ask for the metric-name constant file itself.
- The readiness `checks` element type for `auth` and `entitlement-api`. Ask for one literal ready fixture and
  one literal not-ready fixture per service, not a field list.
- `entitlement-api`'s list-response cursor field name.
- Whether any current `entitlement-api` route or DTO returns a database integer.
- The generic `5xx` body for `comment`, and the response charset for `comment` and `content`, both of which
  the surveys marked undeterminable without running the service. Ask for a rendered response captured in a
  test rather than read from code.
- `content`'s complete ControlledOps error-code set, which lives outside the repository.
- Whether `content`'s `section_key` is an intentional public key or a table key.
- Queue worker count and prefetch for `auth`, which were UNDETERMINED from executable config; the answer may
  live in a deployment repository rather than the service repository, and if so the next survey should say
  which repository owns each runtime bound.
- Whether any service other than `entitlement-api` accepts `Idempotency-Key` on a write route. Only
  `entitlement-api` was confirmed to accept it; `auth`, `comment`, and `gateway` confirmed absence; `content`
  accepts a body-level `idempotency_key` instead, which is a different mechanism and needs a decision.
- A real emitted log line from any service. Every survey returned the field list from code and marked the
  rendered line UNDETERMINED, so the fleet has never actually compared two log lines side by side.
