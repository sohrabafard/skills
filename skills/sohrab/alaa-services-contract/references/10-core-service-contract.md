# Core Service Contract

## Hard contract posture

This skill exists to make Ala services converge on one contract.

Rules:
- Treat the contract as exact unless a blocking incompatibility is reported.
- Do not let agents choose alternative `/api/ready` shapes, alternate headers, different event names, or repo-local metric families just because they also look reasonable.
- Prefer convergence to the Ala contract over local stylistic preference.
- If a service still carries a replaced contract surface such as `X-Correlation-Id`, migrate it fully and delete the stale implementation in the same effort.

## Ala service map

| Service | Primary ownership | Main interaction expectations |
|---|---|---|
| `auth` | canonical auth and profile truth, OTP login, token lifecycle, RBAC compilation, trusted profile APIs | downstream services trust gateway-derived identity and must not duplicate canonical auth or profile ownership |
| `content` | macroservice for `course`, `set`, and `content`; long-term learning-content source of truth | use `content` for the new educational-content domain model instead of reviving legacy `vod` ownership |
| `vod` | legacy learning and playback service during migration | keep it aligned to the same platform contract while moving learning-content responsibilities to `content` |
| `comment` | tenant-scoped comments, replies, likes, moderation, durable outbox publication | frontends and backends use the comment API or comment events and must not read or write comment tables directly |
| `ticket` | support-ticket management, ticket messages, queue-driven notifications, local user projection | protected routes trust gateway-derived context; cross-service consumers must go through the ticket API and must not couple to ticket tables |
| `wa` | watch-time and analytics ingestion into ClickHouse via Vector and related intake flows | non-Laravel runtime is fine, but it must still align to Ala operational and observability naming where applicable |
| `gateway` | HAProxy ingress gateway, JWT verification, trusted-header injection, request-time authz hop, structured gateway logs, and HAProxy metrics | do not force app middleware or app spans onto it; preserve HAProxy metrics and Vector log-pipeline ownership |
| `entitlement-api` | normalized authorization business truth | other services must not treat OpenFGA tuples as the source of truth for business grants |
| `projector` | derived tuple projection into OpenFGA | keep it as a derived-state writer, not as the business-truth owner |
| `authz-sidecar` | request-time authorization runtime for gateway-protected route families | emit decision evidence, propagate trace context, and keep route-time decisions separate from service business authorization |
| `notification` | in-development notification service and delivery workflows | converge on this contract before production readiness, including exception evidence when Sentry is absent |

Components currently under evaluation but expected to follow this contract where relevant:
- `notification-core`
- `realtime-hub`
- `assessment`
- delivery workers
- queue or broker surfaces that expose service-owned metrics, traces, or readiness behavior

Rules:
- Keep this map updated as Ala services evolve.
- Do not invent service responsibilities that conflict with the owning repo docs.
- Use this map to help new services choose correct interaction boundaries instead of duplicating ownership that already belongs elsewhere.

## Canonical service identity

Rules:
- Derive the `service` field from `APP_NAME` or an equivalent service-level config.
- Keep it stable and machine-readable.
- Use the actual Ala service identifier such as `auth`, `content`, `comment`, `ticket`, `gateway`, `entitlement-api`, `projector`, `authz-sidecar`, `notification`, `vod`, or `wa`.
- Do not return framework or runtime names such as `Laravel`, `Go`, `Node`, or `PHP`.
- Do not decorate the value with environment or version strings.

## Route families

Every route belongs to exactly one family:

| Family | Purpose | Public client use? | Contract rule |
|---|---|---:|---|
| public API | product-facing API behavior | yes, when documented | keep separate from operational probes |
| trusted internal | sanitized gateway-derived context | no | align exactly with `$alaa-trust-gateway-auth` |
| operational | liveness, readiness, rollout diagnostics | no | keep auth expectations explicit and minimal |

Rules:
- Do not merge operational probes into product-facing route groups just for convenience.
- Do not require bearer tokens, session cookies, OTP, or end-user state for operational routes.
- Keep `/api/ready` as an operational contract, not a client product feature.

## Exact error envelope

Every Ala service returns this exact JSON body for every `4xx` and `5xx` response on every route it owns,
including responses rendered by a framework exception handler and responses produced at the gateway edge:

```json
{
  "error": {
    "status": 422,
    "code": "INPUT_VALIDATION_FAILED",
    "message": "One operational English sentence.",
    "meta": {}
  }
}
```

Rules:
- The body has exactly one top-level key, `error`. A body whose top level is `message`, `errors`, `code`,
  `detail`, `title`, or a bare array is a contract violation, because a client that branches on
  `error.code` cannot read it and every consumer then carries a second parser per service it calls.
- `error` carries exactly the keys `status`, `code`, `message`, and `meta`, in every error response, with
  no key omitted. A consumer reads `error.meta` without a presence check.
- `status` is the integer HTTP status of the response and equals the status line. A body that disagrees
  with its own status line is a contract violation.
- `code` is a stable machine-readable identifier from the service's committed registry, under the casing
  rule in the next section.
- `message` is one short operational English sentence written for an operator. It is never the branching
  key, never a localized end-user string, and never a raw exception message or stack fragment when debug
  mode is off.
- `meta` is a JSON object. It is `{}` when there is nothing to add. It is never `null`, never a string,
  and never an array, because a consumer that must first test the type of `meta` cannot share one error
  reader across services. Field-level validation failures go under `meta.errors`, an object keyed by field
  name whose values are arrays of message strings.
- The envelope is identical for validation failures, authentication failures, authorization denials, rate
  limiting, and unexpected exceptions. Only the four values change.
- A framework's default error body is replaced, not wrapped. A Laravel `{"message": ..., "errors": {...}}`
  validation body and a bare `{"code": ..., "message": ...}` body are migrated to the envelope above
  through the deprecation procedure in `22-failure-load-and-deprecation-contract.md`.
- An empty body on a `4xx` or `5xx` is a contract violation. When a runtime cannot render a body for a
  status — a Vector source, a proxy short-circuit — the component in front of it renders the envelope for
  that status, and the owning repository records in its own `AGENTS.md` which component renders it. Silence
  is not a contract; a caller cannot distinguish a rejected request from a dropped connection.

Two carve-outs, and no others:
- `GET /api/ready` answers `503` with the readiness envelope defined below, not with this envelope. It
  carries its own `code`, and that `code` follows the same casing rule.
- `/metrics` is a Prometheus text endpoint. A denial there returns the status with a text body, because a
  scraper does not parse JSON.

Observable that decides compliance: for every `4xx` and `5xx` saved example in the repository's tests and
Postman collection,
`jq -e '.error | has("status") and has("code") and has("message") and (.meta | type == "object")'` succeeds,
and `.error.status` equals the example's own status. A repository holding no `4xx` and no `5xx` saved
example has not proven the envelope and is non-conforming until it adds one of each.

## Error code registry and casing

Rules:
- Every `code` this skill governs — in an error body, in a readiness body, in a structured log, in a job
  or outbox record — matches `^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$`: UPPER_SNAKE ASCII, no lowercase, no hyphen,
  no dot. Two services spelling one failure `unauthorized` and `AUTH_UNAUTHENTICATED` force every consumer,
  dashboard, and alert expression to match both spellings forever.
- The code names the failure, not the transport. `NOT_FOUND` is a code; `404` is not.
- Every code a service can emit is listed in one committed registry file in the service repository, and a
  test reads that file and fails when emitted code and registry diverge. A list that lives only in a
  documentation artifact no test reads is not a registry, because nothing fails when the two disagree.
- The registry is append-only. Adding a code is a normal change. Renaming or removing one follows the
  deprecation procedure in `22-failure-load-and-deprecation-contract.md`.
- The event-to-code pairs for request and operational flows are named in
  `20-operational-and-observability-contract.md`. They belong in the same registry and satisfy the same
  pattern; do not keep a second list for them.

Observable that decides compliance: a test enumerates every code the service can emit, asserts each matches
the pattern above, and asserts each appears in the committed registry file in the same repository.

## Operational caller expectations

`GET /api/health` and `GET /api/ready` exist for:
- gateway and ingress probes
- orchestrators and rollout automation
- runtime validation scripts
- smoke checks
- automated tests

Rules:
- these two routes are operational only; a public client contract, SDK method, or frontend code path must never depend on either for product behavior
- `/api/ready` may be called by gateway, ingress, orchestrators, or runtime validators, and the contract must not assume one specific caller
- `/api/ready` must not become a login helper, a feature-flag probe, or a frontend preflight endpoint
- neither route is ever load-shed or rate-limited; see `22-failure-load-and-deprecation-contract.md`

## Exact `/api/health` contract

`GET /api/health` is process-level liveness only.

Required HTTP contract:
- unauthenticated
- status `200`
- route name `api.health` in Laravel services

Required JSON contract:
```json
{
  "status": "ok",
  "service": "comment",
  "timestamp": "2026-04-02T11:22:33.123Z"
}
```

Rules:
- `status` must be `ok`
- keys must be exactly `status`, `service`, `timestamp`
- `timestamp` must be ISO-8601 UTC
- do not call PostgreSQL, Redis, RabbitMQ, ClickHouse, or any other external dependency
- do not gate `/api/health` on seed data, migrations, or business bootstrap state

## Exact `/api/ready` contract

`GET /api/ready` is rollout-grade readiness.

Required HTTP contract:
- unauthenticated
- status `200` when ready
- status `503` when any required dependency or bootstrap invariant is not ready
- route name `api.ready` in Laravel services

Required JSON contract:
```json
{
  "status": "ready",
  "code": "SERVICE_READY",
  "checks": {
    "database": {
      "status": "up",
      "required": true,
      "code": "READINESS_DATABASE_READY",
      "message": "Database connection is ready."
    },
    "redis": {
      "status": "up",
      "required": false,
      "code": "READINESS_REDIS_READY",
      "message": "Redis is reachable."
    }
  },
  "failed_checks": [],
  "timestamp": "2026-04-02T11:22:33.123Z",
  "service": "comment"
}
```

Rules:
- top-level keys must be exactly `status`, `code`, `checks`, `failed_checks`, `timestamp`, `service`
- `status` must be `ready` or `not_ready`
- `code` must be `SERVICE_READY` or `SERVICE_NOT_READY`
- `checks` must be an object keyed by canonical check name. A JSON array of check objects is a contract
  violation even when every element carries the same four fields, because a consumer reading
  `checks.database.status` cannot read an array and a shared readiness reader cannot be written once.
  Observable: `jq -e '.checks | type == "object"'` succeeds on both a ready and a not-ready fixture.
- `failed_checks` must be a stable ordered array of failed required check names
- `timestamp` must be ISO-8601 UTC
- `service` must use the canonical service identity

Each `checks.<name>` item must contain exactly:
- `status`: `up` or `down`
- `required`: boolean
- `code`: stable machine-readable code
- `message`: short operational English sentence

## Readiness naming and failure rules

Canonical check names:
- `database` for the primary PostgreSQL-style database
- `clickhouse` for ClickHouse
- `redis` for Redis
- `rabbitmq` for RabbitMQ

Rules:
- Add service-specific bootstrap checks only when they are real rollout prerequisites.
- Keep check ordering stable.
- Keep keys present even when prerequisites are down.
- Prefer codes like `READINESS_<CHECK>_READY`, `READINESS_<CHECK>_UNAVAILABLE`, `READINESS_<CHECK>_MISSING`, or `READINESS_<CHECK>_INVALID`.
- Do not make `/api/ready` depend on end-user state, OTP, or access tokens.
- Do not proxy another service's `/api/ready` unless that dependency is an explicit approved rollout requirement.

## Illustrative auth readiness precedent

Use this example only as a concrete precedent for how a service may express real bootstrap prerequisites. Do not copy these checks blindly into another service.

```json
{
  "status": "ready",
  "code": "SERVICE_READY",
  "checks": {
    "database": {
      "status": "up",
      "required": true,
      "code": "READINESS_DATABASE_READY",
      "message": "Database connection is ready."
    },
    "redis": {
      "status": "up",
      "required": true,
      "code": "READINESS_REDIS_READY",
      "message": "Redis is reachable."
    },
    "rabbitmq": {
      "status": "up",
      "required": true,
      "code": "READINESS_RABBITMQ_READY",
      "message": "RabbitMQ is reachable."
    },
    "passport": {
      "status": "up",
      "required": true,
      "code": "READINESS_PASSPORT_READY",
      "message": "Passport personal access client bootstrap is ready."
    },
    "permission_catalog": {
      "status": "up",
      "required": true,
      "code": "READINESS_PERMISSION_CATALOG_READY",
      "message": "Permission catalog bootstrap is ready."
    },
    "projects": {
      "status": "up",
      "required": true,
      "code": "READINESS_PROJECTS_READY",
      "message": "Projects bootstrap is ready."
    }
  },
  "failed_checks": [],
  "timestamp": "2026-04-02T11:22:33.123Z",
  "service": "auth"
}
```

## Frozen operational surfaces

The fleet already agrees here. In the 2026-07-25 fleet survey, `auth`, `comment`, `content`,
`entitlement-api`, and the shared `alaa-go-chi` kit each serve `GET /api/health` and `GET /api/ready` with
the same top-level keys, the same `ready` and `not_ready` vocabulary, the same `SERVICE_READY` and
`SERVICE_NOT_READY` codes, and the same 200/503 split. Convergence that already happened is worth as much
as convergence still owed, so these surfaces are frozen:

- The two paths, the health keys, the readiness top-level keys, the two status values, the two codes, and
  the 200/503 split change only through the deprecation procedure in
  `22-failure-load-and-deprecation-contract.md`. A repository does not renegotiate them locally, and an
  agent does not improve them.
- A component whose runtime cannot serve these two paths — an HAProxy edge, a Vector pipeline — records in
  its own repository which endpoint answers each probe and which component renders the body, and the
  gateway route table aliases the public path to it. Current per-component status is in
  `95-fleet-conformance.md`.
- Adding a check to `checks` is not a change to this surface. Adding, renaming, or removing a top-level key
  is.

## Laravel operational baseline

For Laravel services:
- implement `GET /api/health`
- implement `GET /api/ready`
- implement `php artisan ops:ready --json`
- back the route and command with one shared readiness collector when feasible
- test healthy and not-ready paths explicitly
