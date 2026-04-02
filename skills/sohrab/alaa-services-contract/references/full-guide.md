# Purpose

Use this skill to hard-code the Ala backend service contract across Ala services.

This contract exists so agent outputs stay consistent across services and so operational visibility remains predictable for developers, SOC operators, and platform maintainers.

This skill is intentionally Ala-specific. It may mention Ala service names and Ala platform expectations. The portability requirement for this skill is about filesystem independence and reuse across machines, not about being generic to unrelated organizations.

# When to use

- creating or changing `auth`, `comment`, `ticket`, `vod`, `wa`, or another Ala backend service
- standardizing `/api/health`
- standardizing `/api/ready`
- fixing exact readiness payloads and check naming
- standardizing `X-Request-Id` and `traceparent`
- enforcing request and readiness event names and machine-readable codes
- standardizing `RequestObservabilityMiddleware`
- standardizing `ResolveUserMiddleware`
- aligning Laravel Resource-first `/api/*` success responses
- helping a new Ala service understand the current service landscape, ownership boundaries, and expected interaction model before implementation
- forcing cross-service consistency where agents would otherwise improvise

# Hard contract rule

This skill is not a soft recommendation layer.

Rules:
- enforce exact contract outputs where this guide defines exact outputs
- prefer one Ala-wide contract over local convenience
- do not silently downgrade exact contract requirements into "one good option"
- when a repo cannot conform exactly, stop and report the blocker
- when this skill replaces a legacy header, field, event, or helper, remove the old implementation instead of keeping stale compatibility code in the service

# Service modes

## Mode A - any Ala backend service
Owns:
- canonical `service` identity
- route family split
- `/api/health`
- `/api/ready`
- readiness naming
- response headers
- request and readiness event naming
- request or readiness log field schema
- Ala service map and interaction orientation for new services

## Mode B - Laravel backend service
Adds:
- route names `api.health` and `api.ready`
- `php artisan ops:ready --json`
- Laravel middleware ordering guidance
- Resource-first `/api/*` success responses

## Mode C - Laravel downstream trusted service
Adds:
- exact trusted-header handling
- one normalized actor context
- request and auth facade parity
- `ResolveUserMiddleware` or equivalent downstream normalization layer

## Mode D - Laravel auth-boundary service
Allows:
- request guards or `Auth::viaRequest(...)` instead of a literal downstream `ResolveUserMiddleware`

But still requires:
- the same exact trusted-header semantics
- the same outward auth behavior
- the same observability contract
- the same response contract where applicable

# Auth-specific routing note

- when the task touches the `auth` service and any frontend or frontend-facing profile integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing
- treat that document as the canonical frontend integration contract for auth academic policy
- when auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort

# Ala service map

Use this map when designing a new service or changing service-to-service interaction boundaries.

| Service | Primary ownership | Interaction and alignment note |
|---|---|---|
| `auth` | canonical auth and profile truth, OTP login, token lifecycle, RBAC compilation, trusted profile APIs | downstream services should trust gateway-derived identity and should not duplicate canonical auth or profile ownership |
| `comment` | tenant-scoped comments, replies, likes, moderation, durable outbox publication | frontends and backends should use the comment API or comment events rather than couple to comment tables |
| `ticket` | support-ticket management, ticket messages, queue-driven notifications, local user projection | protected routes trust gateway-derived context; cross-service consumers should respect ticket ownership and its service-local API |
| `vod` | video or VOD domain backend currently using Laravel, Octane, and RabbitMQ | align it to the same operational and trusted-ingress contract; refresh exact domain ownership from current repo docs before broad changes |
| `wa` | watch-time and video analytics ingestion into ClickHouse through Vector | non-Laravel runtime, but it should still follow Ala operational and observability naming where applicable |

Rules:
- keep this map updated as Ala services evolve
- do not invent service responsibilities that conflict with the owning repo docs
- use this map to help new services align with the existing system instead of duplicating ownership

# Canonical service identity

Rules:
- derive `service` from `APP_NAME` or equivalent config
- keep it machine-readable and stable
- use the Ala service identifier such as `auth`, `comment`, `ticket`, `vod`, or `wa`
- never return framework or runtime names
- never append env or version strings

# Route families

| Family | Purpose | Public client use? | Notes |
|---|---|---:|---|
| public API | product-facing API behavior | yes | keep independent from probes |
| trusted internal | sanitized gateway-derived context | no | align exactly with `$alaa-trust-gateway-auth` |
| operational | liveness and readiness | no | keep auth requirements explicit and minimal |

Rules:
- operational routes must remain callable without bearer tokens, cookies, OTP, or end-user state
- `/api/ready` is not a product feature endpoint

# Operational caller expectations

`GET /api/health` and `GET /api/ready` exist for:
- gateway and ingress probes
- orchestrators and rollout automation
- runtime validation scripts
- smoke checks
- automated tests

Rules:
- end-user clients should not depend on these routes for product behavior
- `/api/ready` may be called by gateway, ingress, orchestrators, or runtime validators, but the contract must not assume one specific caller

# End-to-end platform flow and boundaries

Treat the default Ala flow like this:
- public client or frontend -> gateway -> backend service
- backend service -> backend service only for internal workloads that truly require a synchronous hop
- backend service -> async infrastructure for queue, event, or job delivery when appropriate

Rules:
- do not let services recreate browser-facing trust assumptions on internal hops
- frontend clients call documented gateway-facing routes, not service-local routes discovered from backend repos
- frontend clients must never generate or rely on trusted internal headers such as `X-Project-ID`, `X-User-Id`, `X-Access`, or `X-Profile`
- trusted headers belong to the gateway-to-service contract, not the public client contract
- keep route ownership clear so frontend, gateway, and backend work stay aligned
- if a route is operational, frontend clients must not treat it as product behavior
- preserve `X-Request-Id` and `traceparent` across internal HTTP hops
- if a frontend or service needs domain behavior from another service, prefer that service's public API or events over direct table coupling

# Exact `/api/health`

Contract:
- method and path: `GET /api/health`
- auth: none
- success status: `200`
- JSON keys: `status`, `service`, `timestamp`
- `status`: `ok`
- `service`: canonical service identity
- `timestamp`: ISO-8601 UTC

Exact example:
```json
{
  "status": "ok",
  "service": "auth",
  "timestamp": "2026-04-02T11:22:33.123Z"
}
```

Rules:
- do not call PostgreSQL, Redis, RabbitMQ, ClickHouse, or another service
- do not gate on business bootstrap state
- use this route only for process-level liveness

# Exact `/api/ready`

Contract:
- method and path: `GET /api/ready`
- auth: none
- status `200` when ready
- status `503` when not ready

Exact top-level JSON keys:
- `status`
- `code`
- `checks`
- `failed_checks`
- `timestamp`
- `service`

Exact top-level values:
- `status`: `ready` or `not_ready`
- `code`: `SERVICE_READY` or `SERVICE_NOT_READY`
- `timestamp`: ISO-8601 UTC
- `service`: canonical service identity

Exact `checks.<name>` shape:
- `status`: `up` or `down`
- `required`: boolean
- `code`: stable machine-readable code
- `message`: short operational English sentence

Exact example:
```json
{
  "status": "not_ready",
  "code": "SERVICE_NOT_READY",
  "checks": {
    "database": {
      "status": "down",
      "required": true,
      "code": "READINESS_DATABASE_UNAVAILABLE",
      "message": "Database connection failed."
    },
    "redis": {
      "status": "up",
      "required": false,
      "code": "READINESS_REDIS_READY",
      "message": "Redis is reachable."
    }
  },
  "failed_checks": [
    "database"
  ],
  "timestamp": "2026-04-02T11:22:33.123Z",
  "service": "comment"
}
```

# Exact readiness naming

Canonical built-in check names:
- `database`
- `clickhouse`
- `redis`
- `rabbitmq`

Rules:
- add service-specific bootstrap checks only when they are true rollout prerequisites
- keep ordering stable
- keep failed required checks listed in deterministic order
- keep keys present even when prerequisites are down
- prefer codes like `READINESS_<CHECK>_READY`, `READINESS_<CHECK>_UNAVAILABLE`, `READINESS_<CHECK>_MISSING`, `READINESS_<CHECK>_INVALID`
- do not proxy another service's `/api/ready` without an approved rollout reason

# Illustrative auth readiness precedent

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

# Exact observability headers

Target contract headers:
- `X-Request-Id`
- `traceparent`

Non-target legacy headers:
- `X-Correlation-Id`
- `X-Trace-Id`

Rules:
- new implementations must target only `X-Request-Id` and `traceparent`
- if a service still emits, parses, forwards, tests, or documents `X-Correlation-Id`, migrate it to `X-Request-Id` plus `traceparent` and remove the stale implementation in the same effort
- after applying this skill, no service code, config, docs, tests, or emitted response headers should still contain `X-Correlation-Id`

# Exact `X-Request-Id`

Rules:
- preserve a safe inbound value
- otherwise generate lowercase UUIDv7
- keep it stable for the request lifetime
- return it on every `/api/*` response, including rendered API error responses
- log it on request completion, failure, and auth-context denial paths

# Exact `traceparent`

Canonical format:
- `00-{trace_id}-{parent_id}-01`

Rules:
- `trace_id` is 32 lowercase hex characters and non-zero
- `parent_id` is 16 lowercase hex characters and non-zero
- valid inbound `traceparent` is preserved
- invalid inbound `traceparent` is ignored and replaced
- response always returns the canonical `traceparent`
- logs use `trace_id` derived from the canonical `traceparent`
- do not require `X-Trace-Id` as a response header

# Exact log field contract

For middleware and operational flows owned by this skill, log at minimum:
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
- `user_id` when available and safe
- `http.method`
- `http.route`
- `http.status`
- `duration_ms`

This aligns with `$alaa-observability-soc` and keeps SOC queries stable.

# Exact event and code contract

Use these exact event names for flows owned by this skill:
- `http.request.completed`
- `http.request.failed`
- `service.readiness.failed`
- `service.readiness.recovered` when transition tracking is implemented
- `auth.context.invalid`
- `authz.denied`
- `input.validation.failed`

Use these exact code expectations:
- `HTTP_REQUEST_COMPLETED` with `http.request.completed`
- `HTTP_REQUEST_FAILED` with `http.request.failed`
- `SERVICE_NOT_READY` with `service.readiness.failed`
- `SERVICE_READY` with `service.readiness.recovered` when used
- `AUTH_*` codes from `$alaa-trust-gateway-auth` with `auth.context.invalid`
- stable domain denial codes with `authz.denied`
- stable validation codes with `input.validation.failed`

Rules:
- do not invent alternate names for the same event
- do not rename these fields casually because SOC dashboards and operator habits depend on them

# Probe-noise and metrics contract

Rules:
- suppress low-value completed logs for successful `/api/health`
- suppress low-value completed logs for successful `/api/ready`
- keep readiness failures observable
- keep request failures observable
- if transition logs are implemented, use `service.readiness.failed` and `service.readiness.recovered`

Metrics labels may use:
- templated route or route name
- method
- status code or status class
- service
- env

Metrics labels must not use:
- `user_id`
- `project_id`
- raw path
- query string
- exception message

# `RequestObservabilityMiddleware`

For Laravel services, apply `RequestObservabilityMiddleware` early on `/api/*` traffic.

Preferred order:
1. `RequestObservabilityMiddleware`
2. tenant or project normalization needed before bindings
3. `SubstituteBindings`
4. `ResolveUserMiddleware` or equivalent trusted-user normalization layer
5. controller and policy-facing code

Required behavior:
- compute canonical `X-Request-Id`
- compute canonical `traceparent`
- store request-scoped context
- capture request start time
- attach headers to API responses
- preserve enough request context for the exception handler to attach the same headers to rendered API error responses
- emit exact request and readiness events and codes defined above
- emit bounded-cardinality metrics when the repo has a metrics boundary

Required support components:
- request context normalizer
- request-id generator and validator
- `traceparent` parser and generator
- route resolver
- duration capture
- log-context sharing mechanism
- exception-path header attachment hook
- probe-noise decision helper
- metrics emission boundary

Implementation rule:
- when middleware rethrows, have the exception handler read the shared request context and attach `X-Request-Id` and `traceparent` to rendered API error responses

# `ResolveUserMiddleware`

For downstream trusted Laravel services, use `ResolveUserMiddleware` or an equivalent request-based layer that satisfies the same semantics.

Exact trusted headers:
- `X-Project-ID`
- `X-User-Id`
- `X-Access`
- `X-User-Mobile`
- `X-Profile`

Exact validation posture:
- `X-Project-ID` is UUIDv7
- `X-User-Id` is positive integer
- `X-Access` is base64url permission bitmap and must map to at least one known permission
- `X-User-Mobile` follows `$alaa-trust-gateway-auth`
- `X-Profile` is base64url JSON object when present
- `shahr` follows `$alaa-trust-gateway-auth`
- auth error codes come from `$alaa-trust-gateway-auth`

Required behavior:
- parse trusted headers once
- build one normalized actor context
- synchronize `$request->user()` and `Auth::user()`
- synchronize legacy guards still in use
- keep normalization out of controllers and policies

Required support components:
- trusted request context helper
- trusted actor DTO
- permission bitmap decoder and mapper
- trusted profile parser and normalizer
- auth-state synchronizer
- optional role-derivation helper
- stable API-error mapping path

# Laravel success-response contract

For Laravel `/api/*` success responses:
- use `JsonResource` or `ResourceCollection`
- keep a top-level `data` key
- use `meta` only for transport metadata
- use `links` only for true document navigation or pagination
- keep nested child resources inline
- keep controllers responsible for HTTP status and serialization
- keep services returning domain data or DTOs instead of transport-shaped arrays
- do not leak raw models, persistence-only fields, or temporary internal fields

Default implementation guidance:
- preserve an existing success envelope only when it already matches the current contract or the contract is being intentionally revised in the same effort
- keep current error responses aligned by default unless a stricter contract is explicitly in scope
- inspect existing repository patterns before changing response serialization
- use Laravel Boost `search-docs` first for version-specific Resource guidance when it is available
- keep docs, examples, and Postman artifacts aligned with the shipped Resource shape when the contract changes

Why this rule exists:
- it keeps response shapes consistent across endpoints
- it makes tests simpler because assertions target one transport boundary
- it makes docs and Postman examples easier to keep synchronized
- it prevents accidental leakage of internal IDs, persistence details, or backend-only fields
- it makes contract review safer because the public success shape is centralized instead of scattered

Auth reference precedent:
- auth repository commit `40d7e6e` is the approved reference precedent for this rule
- that precedent established Resource-first success responses for `/api/*`
- it also established service or domain DTOs under the controller boundary, controller-owned HTTP status and serialization, and removal of backend-only public leakage such as `access_token_id`

# Copy baselines

When a Laravel repository needs implementation help, use `references/50-laravel-copy-baselines.md` as the copy-oriented baseline and adapt only namespaces and helper wiring, not behavior.

Do not assume the middleware can attach headers after a rethrow. The exception handler must attach `X-Request-Id` and `traceparent` to rendered API error responses by reading the shared request context.

# Apply workflow

1. identify service mode
2. load the smallest relevant contract file
3. load companion skills
4. inspect the current repo shape
5. converge routes, middleware, helpers, headers, events, and envelopes to the exact contract
6. add missing helper components instead of hand-waving them
7. test the changed surfaces
8. update docs and artifacts

# Review checklist

Flag a problem when you see:
- `/api/health` touching external dependencies
- `/api/ready` with the wrong envelope or wrong key names
- `X-Correlation-Id` remains anywhere in service code, config, tests, docs, or emitted headers after migration
- `X-Trace-Id` still treated as a response-header requirement
- rendered API error responses missing `X-Request-Id` or `traceparent`
- different event names for the same request or readiness flows
- trusted headers parsed outside the ingress layer
- divergence between `$request->user()` and `Auth::user()`
- Laravel controllers or services shaping transport arrays instead of Resources
- docs or Postman drift

# Anti-patterns

- treating the contract as optional
- keeping repo-local variants without a blocker
- moving event or code naming away from `$alaa-observability-soc`
- moving auth errors away from `$alaa-trust-gateway-auth`
- leaving `X-Correlation-Id` anywhere in the service after migrating to `X-Request-Id`
- keeping stale compatibility branches, helpers, tests, or docs for removed contract surfaces
- assuming middleware can attach response headers after a rethrow without exception-handler support
- leaving helper dependencies implicit
