# Fleet Conformance Snapshot — 2026-07-25

This file is **not a rule file**. It states no contract and overrides nothing. Every rule it references is
owned by a numbered reference file, and that file wins in every case. This file records one thing: which Ala
component satisfies which of those rules on 2026-07-25, and what each component that does not must change.

Read it when you are planning migration work, sequencing a fleet change, or deciding which repository to
open first. Do not read it to learn a rule; open the owning file named beside the rule.

**Amended 2026-07-25, same day.** The owner ratified the twelve disagreements below with six amendments,
and applying them required a second evidence pass. That pass re-read metric-name constants and broker
configuration in the seven surveyed repositories, and read two repositories the original survey did not
cover at all: `notification` and `notif`. Findings from it are marked *second pass* and carry their own
evidence; they resolve several rows the first survey left UNDETERMINED and overturn one of its readings. The
second pass recorded no commit SHAs, so its findings are dated rather than pinned.

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

## Index: the twelve ratified disagreements, the six amendments, and where each rule now lives

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 1 | Single error envelope `{"error":{status,code,message,meta}}` | `10-core-service-contract.md` | `comment`, `content`, `entitlement-api`, `gateway`, kit | `auth`, `wa` |
| 2 | Error codes are UPPER_SNAKE, in one committed registry | `10-core-service-contract.md` | `comment`, `content`, `entitlement-api`, kit (casing) | `gateway`, `auth` (casing); `auth`, `content` (registry) |
| 3 | Keyset cursor pagination, `cursor`/`limit`, `meta.next_cursor` | `25-end-to-end-flow-and-boundaries.md` | kit; `entitlement-api` (keyset, cursor field unproven) | `auth`, `comment`, `content` |
| 4 | Public payloads carry public identifiers; one actor exception | `25-end-to-end-flow-and-boundaries.md` | `entitlement-api` (HTTP path), kit | `comment`, `auth`, `content` |
| 5 | One domain event envelope (`message_*` field vocabulary) | `20-operational-and-observability-contract.md` | none | `auth`, `content`, `comment`, `entitlement-api`; kit is closest |
| 6 | Exchange `<service>.events`, routing key is `message_type` verbatim | `23-queue-and-exchange-registry.md` | none | `auth`, `content`, `entitlement-platform`, `comment`; kit enforces no format |
| 7 | A service that authorizes reads `X-Access` | `28-backend-permission-authorization-and-role-freeze.md` | `comment`, `content`, `entitlement-api`, kit | `auth` |
| 8 | One request deadline, originated by the gateway from env and decremented per hop | `22-failure-load-and-deprecation-contract.md` | none | all seven; `gateway` owns the change that unblocks the rest |
| 9 | Every application metric name begins `alaa_` | `24-metric-registry.md` | `auth`, `content`, `comment` (*second pass*) | kit; `entitlement-platform` (*second pass*); `gateway`, `wa` unproven |
| 10 | Readiness `checks` is an object keyed by check name, each item carrying `required` | `10-core-service-contract.md` | `comment`, `content` (*second pass*, both fields evidenced) | kit |

Two further findings, same status as the ten:

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 11 | Every consumer sets explicit prefetch | `22-failure-load-and-deprecation-contract.md` | `entitlement-api`, `projector` (50) | `comment`, `content`, `auth`, kit |
| 12 | The gateway is the only end-user token verifier | `25-end-to-end-flow-and-boundaries.md` | all seven | none — freeze it |

Six obligations the amendments created on 2026-07-25. They are new, so the fleet is behind on all of them by
construction; that is not a defect in the services, it is what a new rule looks like on its first day.

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 13 | `error.meta` carries only permitted detail, and one `code` produces one `meta` key set | `10-core-service-contract.md` | none proven | every service that emits an error envelope; no repository has a per-code `meta` fixture |
| 14 | Every exchange and queue is registered before it is declared | `23-queue-and-exchange-registry.md` | none | all; the registry was created today, so every existing name is registered retroactively and every new one is not |
| 15 | Every metric is registered before it is emitted | `24-metric-registry.md` | none | all; same reason as #14 |
| 16 | `project_id` is UUIDv7 on payload, event, log field, and cache key | `25-end-to-end-flow-and-boundaries.md` | `entitlement-api` (UUIDv7 in events) | `auth` (`"project_id": 42` in the outbox envelope); `comment` (numeric `project_id` in resources); log-field and cache-key form unproven everywhere |
| 17 | `meta.prev_cursor` present and `null` at the start of a collection | `25-end-to-end-flow-and-boundaries.md` | none | all; the key did not exist before today, and the kit does not yet always render `meta.next_cursor` either |
| 18 | The gateway originates `X-Request-Deadline-Ms` from `GATEWAY_REQUEST_DEADLINE_MS` | `22-failure-load-and-deprecation-contract.md` | none | `gateway`; every other service is blocked on it and falls back to its own route default until it ships |

Two obligations added 2026-07-29, when the TOTP step-up rejection surface was registered. The emitting half
of #19 landed the same day; the rest of both rows is still ahead of the fleet.

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 19 | The gateway sets `X-TOTP-PROOF-REJECTED` on a presented-and-rejected proof, and a service acts on it only to change a message | `32-auth-totp-and-step-up-contract.md` | `gateway` (emits it, sanitizes it from client input, and proves presence, value, and absence at runtime) | no backend reads it, and no service that emits `TOTP_STEP_UP_REQUIRED` carries `meta.proof_rejected` yet — that key lands fleet-wide in one change or not at all |
| 20 | The gateway exports `alaa_gateway_totp_proof_verifications_total` | `24-metric-registry.md` | none | `gateway`; its Vector configuration has no `log_to_metric` transform, so step-up rejection alerting is log-search-only while the `auth` half of the same flow is a counter |

One obligation was added on 2026-08-12 after the owner selected network-only admission for service metrics.
No repository was re-surveyed for this amendment, so conformance remains unproven until each target's
application guard and rendered deployment exposure are checked together.

| # | Rule | Owning file | Conforms | Does not conform |
|---|---|---|---|---|
| 21 | The central scraper calls each private `GET /metrics` directly, with no application-layer credential or source-IP allowlist and no public gateway route | `21-alaa-platform-observability-directive.md` | none proven | `auth`, `comment`, `content`, and the `alaa-go-chi` kit require a fresh application-plus-deployment conformance pass |

Corrections to note, because the evidence did not support the first reading:
- #3: `entitlement-api` is keyset (`cursor` and `limit` reach the query services), but its survey shows
  responses wrapped only as `{"data":...}` by `writeData`; a `meta.next_cursor` field is not evidenced. It is
  keyset-conforming and cursor-field-unproven, not fully conforming.
- #4: `entitlement-api` retains `legacy_object_internal_id` in a migration column, which is schema residue,
  not a payload leak. Its survey states that a route deliberately returning a database integer is
  UNDETERMINED. Treat it as a survey question, not a confirmed violation.
- #9: the first survey left `comment` unproven because it catalogued metric label sets rather than names.
  *Second pass*: every name in `comment`'s `app/Support/Observability/MetricCatalog.php:18-125` begins
  `alaa_`, so `comment` conforms on the prefix. *Second pass*: `entitlement-platform` does **not** conform —
  `services/entitlement-api/internal/observability/metrics.go:93-196` registers fifteen `entitlement_*`
  names and the sidecar registers eight `authz_sidecar_*` names, none of them prefixed. The kit's bare names
  are quoted and confirmed. `gateway` and `wa` metric names remain UNDETERMINED.
- #10: *second pass*: `comment` and `content` both emit an object keyed by check name **and** carry
  `required` inside each item — `comment/app/Support/Operations/OperationalStatusService.php:216-236` and
  `content/app/Support/Operations/OperationalStatusService.php:268-290` build every item as
  `{status, required, code, message}`. The ratified shape is therefore what the two Laravel services already
  ship, and the kit is the only evidenced departure: `readykit/report.go:12-26` declares
  `Checks []CheckItem` with no name field of any kind, so its array cannot say which check failed. `auth`
  and `entitlement-api` list `checks` as a top-level key without evidencing its element type; both still
  need a one-line answer in the next pass.

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
6. **Emit the UUIDv7 project id in events, logs, and cache keys.** The outbox envelope carries
   `"project_id": 42`, an internal integer, where `entitlement-api` carries a UUIDv7. A consumer cannot map
   that integer. Rule: `25-end-to-end-flow-and-boundaries.md`, `Canonical project_id form`, which now binds
   four surfaces with no exception. Evidence: `app/Services/Messaging/RabbitMqOutboxPublisher.php:62-75`;
   `tests/Feature/OutboxRelayCommandTest.php:71-84`.
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
11. **Reconcile the outbox exchange name.** *Second pass*: `config/outbox.php:6` defaults to `auth.events`,
    which conforms, while `.env.example:238` overrides it to `auth-profile.events`, which does not — a hyphen
    is not a segment separator and the two spellings are two namespaces for one service. Fix the env example
    and any deployment that copies it. Rule: `23-queue-and-exchange-registry.md`.
12. **Rename the internal job queue.** *Second pass*: the worker queue is `sms`
    (`config/queue.php:79,102`; `.env.example:237,246`), a bare name in a shared vhost. It becomes
    `auth.jobs.sms`. Its *messages* stay whatever Laravel produces — the envelope scope test in
    `20-operational-and-observability-contract.md` frees an internal job from the envelope — but the name is
    governed regardless, because two services declaring `sms` collide. Rule:
    `23-queue-and-exchange-registry.md`.
13. **Build the command path to `notification`.** *Second pass*: `auth` has none. It sends OTP by calling
    the SMS provider directly through `app/Classes/sms/MedianaClient.php`, behind `MedianaChannel` and
    `MedianaPatternChannel`, so a provider outage is an `auth` outage on the login path. The path it will
    take publishes to the existing `notification.commands` exchange with routing key `sms.send_pattern.v1`;
    `auth` declares no queue. Rule: `23-queue-and-exchange-registry.md`, and
    `27-notification-service-contract.md` for the payload.
14. **Register and align the metric names.** *Second pass*: `auth` emits thirteen platform families through
    `app/Support/Observability/MetricsRegistry.php:85-221` plus seven `alaa_auth_*` business families at
    `:230-236`, all correctly prefixed. Two gaps: it does not emit
    `alaa_auth_token_validation_failed_total`, which this contract named before the registry existed and
    which is now marked `reserved`; and it emits no `alaa_requests_deadline_exhausted_total`, which it owes
    once it implements the deadline. Rule: `24-metric-registry.md`.
15. **Confirm the Passport `api` guard is unreachable.** `config/auth.php:19-22` configures a Passport guard
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
8. **Align the registered metric names.** *Second pass*: the prefix question is answered — every name in
   `app/Support/Observability/MetricCatalog.php:18-125` begins `alaa_`, so #9 is satisfied. What remains is
   registry alignment: `alaa_http_request_errors_total` becomes `alaa_http_request_failures_total`
   (`:29`); `alaa_queue_jobs_total` and `alaa_queue_job_duration_seconds` become
   `alaa_queue_messages_consumed_total` and `alaa_queue_message_duration_seconds` (`:60,65`); and the four
   outbox names at `:71-89` become the canonical outbox family. Rule: `24-metric-registry.md`.
9. **Rename the internal job queue.** *Second pass*: the queue is `events` (`config/queue.php:84`;
   `.env.example:128`), which is both a bare name and the same name `content` uses, so the two services
   collide on a shared vhost. It becomes `comment.jobs.outbox`. Rule:
   `23-queue-and-exchange-registry.md`.
10. **Keep the readiness shape.** *Second pass*: `app/Support/Operations/OperationalStatusService.php:216-236`
    already emits `checks` as an object keyed by name with `status`, `required`, `code`, and `message` in
    every item. That is the ratified shape; do not change it.

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
   `23-queue-and-exchange-registry.md`. Evidence:
   `app/Support/Content/RabbitMqIntegrationEventPublisher.php:15-28`; `config/events.php:10-14`.
   *Second pass*: the same rename covers four bare internal job queues — `events`, `progress`,
   `controlled-ops`, and `default` (`.env.example:101,103,109,179`) become `content.jobs.outbox`,
   `content.jobs.progress`, `content.jobs.controlled_ops`, and `content.jobs.default`. Their message bodies
   stay as Laravel produces them.
5. **Publish a complete error-code registry.** The survey could not enumerate the ControlledOps codes from
   this repository, so no test can assert the set. Rule: `10-core-service-contract.md`. Evidence:
   `app/Providers/ControlledOpsServiceProvider.php:1-20`.
6. **Set prefetch**, and **compute the ingress deadline**. Rule:
   `22-failure-load-and-deprecation-contract.md`. Evidence: `config/queue.php:84-113`.
7. **Align the outbox metric names.** *Second pass*: `alaa_content_outbox_events_published_total` and
   `alaa_content_outbox_publish_failures_total` are service-scoped spellings of a platform family and become
   `alaa_outbox_published_total` and `alaa_outbox_publish_failures_total`. Everything else `content` emits is
   already registered. Rule: `24-metric-registry.md`.
8. Already conforming and worth keeping: the error envelope including the debug-off `SERVER_ERROR` body,
   the `alaa_*` metric prefix, the readiness envelope — which *second pass* confirms emits `required` inside
   each name-keyed item at `app/Support/Operations/OperationalStatusService.php:268-290` — and the
   trusted-header set.

### `entitlement-platform` (`entitlement-api`, `projector`, `authz-sidecar`)

1. **Stop publishing to the default exchange.** `projector` publishes with exchange `""` and the queue name
   as routing key, which binds the producer to one consumer's queue name. Declare `entitlement.events` and
   bind consumers to it. Rule: `23-queue-and-exchange-registry.md`. Evidence:
   `services/projector/internal/runtime/amqp.go:100-107`; `services/entitlement-api/internal/mq/types.go:1-16`.
   *Second pass*: the five queue names themselves conform and are registered —
   `entitlement.projector.work`, `entitlement.reconciliation`, `notif.retrieve_users`, `notif.expand_users`,
   and `notif.recipient_chunks` (`internal/mq/types.go:16-20`), each with `.retry` and `.dlq`. The defect is
   the publish path, not the naming. `notif.recipient_chunks` has no wired consumer, which is an undrained
   durable queue and is recorded as such in the registry.
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
5. **Prefix the metric names `alaa_` and publish the catalog.** *Second pass*: the names are no longer
   UNDETERMINED. `services/entitlement-api/internal/observability/metrics.go:93-196` registers fifteen
   `entitlement_*` families and the sidecar registers eight `authz_sidecar_*` families; none is prefixed, so
   this service moves from unproven to confirmed non-conforming on #9. The HTTP and MQ families rename onto
   the platform names in `24-metric-registry.md`; the genuinely service-owned ones take the `alaa_`
   prefix and are already registered there under their new names. One catalog file per service makes the
   next survey cheap. Rule: `24-metric-registry.md`.
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
4. **Originate the deadline header.** The question is now decided, not open: the gateway sets
   `X-Request-Deadline-Ms` on every forwarded request from `GATEWAY_REQUEST_DEADLINE_MS`, default `180000`,
   strips any client-supplied value, and is the only component permitted to originate it. It forwards no
   deadline today. This is the change that unblocks the deadline for the whole fleet, because a service can
   only decrement a value something gave it. Rule: `22-failure-load-and-deprecation-contract.md`. Evidence:
   `charts/gateway/values.yaml:221-225`; the edge timeouts it already owns are at `values.yaml:44-50`
   (`client 30s`, `server 30s`, `httpRequest 10s`, `httpKeepAlive 10s`), and the new deadline is a request
   budget layered above them, not a replacement for them.
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
7. *Second pass*: `wa` declares no exchange and no queue. It is a Vector pipeline writing to ClickHouse, so
   it owns no row in `23-queue-and-exchange-registry.md` and the registry obligation does not apply to it.
   Record that in its `AGENTS.md` too, so the next agent does not go looking for a broker that is absent by
   design rather than by omission.

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
   consumer can parse both. *Second pass*: it is worse than a type mismatch — `CheckItem` has **no name
   field at all** (`readykit/report.go:11-22`), so the array cannot say which check failed even to a
   consumer willing to iterate it. Keep `required`, which the kit already has and which is what separates a
   degraded optional dependency from a failed mandatory one. Rule: `10-core-service-contract.md`.
3. **Always render `meta.next_cursor`, and add `meta.prev_cursor` beside it.** The Go field is a string
   with `omitempty`, so the last page omits the key while `CONTRACTS.md:72-73` documents `null`. The kit's
   own survey records this as its own drift; the contract resolves it in `CONTRACTS.md`'s favour. The
   amendment adds a second always-present key, `meta.prev_cursor`, `null` at the start of the collection, so
   the fix is one change to the envelope struct rather than two. Rule:
   `25-end-to-end-flow-and-boundaries.md`. Evidence: `httpkit/envelope.go:8-10`.
4. **Give the consumer abstraction a required prefetch parameter.** `ConsumerChannel` exposes only
   `Consume(ctx, queue)`, so no service built on it can bound its consumer even when it wants to, while the
   kit's own `AGENTS.md:15` requires bounded consumers. Rule:
   `22-failure-load-and-deprecation-contract.md`. Evidence: `mqkit/consumer.go:29-31,58-66`.
5. **Enforce the routing-key and exchange grammar in `mqkit/topology.go`.** The validator requires non-empty
   strings only, which is how four services reached four conventions. *Second pass*: `Topology`,
   `ExchangeDecl`, `QueueDecl`, and `DLQDecl` (`mqkit/topology.go:8-31`) already carry every field the
   grammar needs, so the change is validation logic, not new structure. Rule:
   `23-queue-and-exchange-registry.md`. Evidence: `mqkit/topology.go:73-127`.
6. **Extend `mqkit/envelope.go` with the event fields.** It already carries the command vocabulary
   (`message_id`, `message_type`, `message_version`, `occurred_at`, `producer_service`, `correlation_id`,
   `causation_id`, `idempotency_key`, `traceparent`, `payload`); domain events add `project_id`,
   `aggregate_type`, `aggregate_id`, and optional `aggregate_version`. Rule:
   `20-operational-and-observability-contract.md`. Evidence: `mqkit/envelope.go:16-33`.
7. **Resolve the `400`-versus-`422` validation status.** `CONTRACTS.md:10-21` documents `422` while
   `httpkit/bind.go` emits `400` and `errkit` permits both. One status per code, or the shared contract test
   proves nothing. Rule: `10-core-service-contract.md`. Evidence: `httpkit/bind.go:59-74`;
   `errkit/envelope.go:114-116`.
8. **Add an ingress deadline helper** that reads `X-Request-Deadline-Ms`, exposes the remainder on the
   request context, clamps outbound timeouts to it, and forwards the decremented value — so the rule ships
   once rather than per service. It must not add a kit env variable that sets or overrides the edge
   deadline: the kit's own decision register already settled that edge timeouts are gateway-owned and the
   kit's timeouts are the backend's handler budget
   (`docs/change-requests/2026-07-21-kit-bug-remediation-decision-register.md:102-104,955-960`), and the
   same principle governs the deadline. Rule: `22-failure-load-and-deprecation-contract.md`.
9. **Extend `contracttest` with the registered name sets.** `contracttest.AssertMetricNamesStable`
   (`contracttest/observability_contract.go:19-50`) already gathers from the live Prometheus registry and
   fails on an unexpected or missing family, which makes it the cheapest place in the fleet to enforce
   `24-metric-registry.md` for every Go service at once. The same package is where a queue-name assertion
   against `23-queue-and-exchange-registry.md` belongs. Rules: `24-metric-registry.md`,
   `23-queue-and-exchange-registry.md`.
10. Already conforming and worth keeping: the error envelope and its pre-marshaled canonical `500`, the
   UPPER_SNAKE code set with `FinalizeKnownCodes` registration, keyset-only pagination, the trusted-header
   parse with fail-closed defaults, receipt-based consumer idempotency, and the `contracttest` package —
   which is the right mechanism for enforcing everything in this file, and is currently the only one in the
   fleet.

### `notification` (*second pass*, not in the original seven)

`notification` is the Laravel service that owns every cross-service command queue in the fleet, and the
original survey did not cover it. It was read on 2026-07-25 for the queue registry; no commit was pinned and
no full twelve-section survey was run, so nothing below is a conformance verdict outside the topology.

1. Already conforming and load-bearing for the whole fleet: the `notification.commands` direct exchange, the
   `notification.commands.dlx` dead-letter exchange, the four ingress queues, their routing keys, and their
   `.dlq` queues (`config/queue.php:136-230`). Every row is registered in
   `23-queue-and-exchange-registry.md` and every producer integrates against it.
2. **Rename the legacy internal queue.** `config/queue.php:80` still carries `sms` as the default
   `RABBITMQ_QUEUE` for the pre-migration `notifications.consume` path. It becomes `notification.jobs.sms`,
   for the same collision reason as `auth`'s. Rule: `23-queue-and-exchange-registry.md`.
3. **Everything else about this service is unsurveyed**: its error envelope, its identifiers, its readiness
   shape, its metric names, and its deadline behaviour were not examined. Do not read the absence of items
   here as conformance. A full survey pass is owed before it can appear in the index table above.

### `notif` (*second pass*, the Go successor, not live)

`notif` is the Go service intended to replace `notification` once the `alaa-go-chi` kit stabilises. It is a
scaffold: its own `docs/BIG_PICTURE.md` marks domain behaviour, storage, queues, and route families as
unconfirmed until implemented, and no Go file in the repository declares a queue.

1. **It consumes nothing today.** Every `notif` row in `23-queue-and-exchange-registry.md` is `planned` and
   is evidence of a committed design document, not of a running consumer. Do not publish to a `notif` queue,
   and do not record `notif` as the owner of a family `notification` still serves.
2. **The migration is family-by-family, not service-by-service.** `notif` binds its own queues to the
   existing `notification.commands` exchange and shadow-processes one family at a time, comparing receipts
   against `notification` before each cutover, in risk order: `user_projection.upsert.v1` first,
   `sms.send_message.v1` second, `sms.send_pattern.v1` last. Producers change nothing throughout
   (`notif-service-go-architecture.md:255-262`).
3. **`notification.command.notification.store.v1` does not migrate.** It stays on `notification`, frozen
   except for security fixes, until the in-app inbox finds its own service
   (`notif-service-go-architecture.md:153-158`).
4. Because it is built on the kit, every kit item above is inherited by `notif` on its first day. The kit
   items are therefore the cheapest place to fix `notif`'s conformance, and fixing them in `notif` instead
   leaves the next kit-built service non-conforming again.

## What the surveys could not determine

Ask these in the next pass; each one blocked a conformance verdict above.

- Exact metric names for `gateway` and `wa`. Only generated exporter names and a console-sink Vector
  pipeline were visible. Ask for the metric-name constant file itself, or for a captured `/metrics` scrape.
  *Resolved by the second pass*: `comment`'s names (all `alaa_`-prefixed) and `entitlement-platform`'s names
  (fifteen `entitlement_*`, eight `authz_sidecar_*`, none prefixed) are now recorded above.
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
  rendered line UNDETERMINED, so the fleet has never actually compared two log lines side by side. The
  amendments make this more urgent, not less: the `project_id` log-field form cannot be checked from a field
  list, only from a rendered line.
- Whether any service builds a cache, lock, or rate-limit key from an internal numeric project id. The
  surveys looked at payloads and events, not at key construction, so the cache-key half of
  `Canonical project_id form` is unproven everywhere.
- Whether any service emits a stable `meta` key set per error `code`. No repository holds a per-code error
  fixture, so rule #13 is unproven for every service rather than failed by any of them.
- A full twelve-section survey of `notification` and `notif`. The second pass read their topology only.
