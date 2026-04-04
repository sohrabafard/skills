# Alaa Services Contract Full Guide

## Purpose and use

Use this skill to hard-code the Ala backend service contract across Ala services.

This contract exists so agent outputs stay consistent across services and so operational visibility remains predictable for developers, SOC operators, and platform maintainers.

This skill is intentionally Ala-specific. It may mention Ala service names and Ala platform expectations. The portability requirement for this skill is about filesystem independence and reuse across machines, not about being generic to unrelated organizations.

Use it when:
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

## Hard contract rule

This skill is not a soft recommendation layer.

Rules:
- enforce exact contract outputs where this guide defines exact outputs
- prefer one Ala-wide contract over local convenience
- do not silently downgrade exact contract requirements into "one good option"
- when a repo cannot conform exactly, stop and report the blocker
- when this skill replaces a legacy header, field, event, or helper, remove the old implementation instead of keeping stale compatibility code in the service

## Service modes

### Mode A - Any Ala backend service

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

### Mode B - Laravel backend service

Adds:
- route names `api.health` and `api.ready`
- `php artisan ops:ready --json`
- Laravel middleware ordering guidance
- Resource-first `/api/*` success responses

### Mode C - Laravel downstream trusted service

Adds:
- exact trusted-header handling
- one normalized actor context
- request and auth facade parity
- `ResolveUserMiddleware` or equivalent downstream normalization layer

### Mode D - Laravel auth-boundary service

Allows:
- request guards or `Auth::viaRequest(...)` instead of a literal downstream `ResolveUserMiddleware`

But still requires:
- the same exact trusted-header semantics
- the same outward auth behavior
- the same observability contract
- the same response contract where applicable

## Auth-specific routing note

- When the task touches the `auth` service and any frontend or frontend-facing identity integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing.
- Treat that document as the canonical frontend integration contract for auth academic policy.
- When auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort.

## Ala service map

Use this map when designing a new service or changing service-to-service interaction boundaries.

| Service | Primary ownership | Interaction and alignment note |
|---|---|---|
| `auth` | canonical auth and identity truth, OTP login, token lifecycle, RBAC compilation, trusted profile APIs | downstream services should trust gateway-derived identity and should not duplicate canonical auth or profile ownership |
| `comment` | tenant-scoped comments, replies, likes, moderation, durable outbox publication | frontends and backends should use the comment API or comment events rather than couple to comment tables |
| `ticket` | support-ticket management, ticket messages, queue-driven notifications, local user projection | protected routes trust gateway-derived context; cross-service consumers should respect ticket ownership and its service-local API |
| `vod` | video or VOD domain backend currently using Laravel, Octane, and RabbitMQ | align it to the same operational and trusted-ingress contract; refresh exact domain ownership from current repo docs before broad changes |
| `wa` | watch-time and video analytics ingestion into ClickHouse through Vector | non-Laravel runtime, but it should still follow Ala operational and observability naming where applicable |

Rules:
- keep this map updated as Ala services evolve
- do not invent service responsibilities that conflict with the owning repo docs
- use this map to help new services align with the existing system instead of duplicating ownership

## Canonical service identity

Rules:
- derive `service` from `APP_NAME` or equivalent config
- keep it machine-readable and stable
- use the Ala service identifier such as `auth`, `comment`, `ticket`, `vod`, or `wa`
- never return framework or runtime names
- never append env or version strings

## Route families and operational callers

| Family | Purpose | Public client use? | Notes |
|---|---|---:|---|
| public API | product-facing API behavior | yes | keep independent from probes |
| trusted internal | sanitized gateway-derived context | no | align exactly with `$alaa-trust-gateway-auth` |
| operational | liveness and readiness | no | keep auth requirements explicit and minimal |

Rules:
- operational routes must remain callable without bearer tokens, cookies, OTP, or end-user state
- `/api/ready` is not a product feature endpoint

Operational caller expectations:
- `GET /api/health` and `GET /api/ready` exist for gateway and ingress probes
- `GET /api/health` and `GET /api/ready` exist for orchestrators and rollout automation
- `GET /api/health` and `GET /api/ready` exist for runtime validation scripts
- `GET /api/health` and `GET /api/ready` exist for smoke checks and automated tests

Rules:
- end-user clients should not depend on these routes for product behavior
- `/api/ready` may be called by gateway, ingress, orchestrators, or runtime validators, but the contract must not assume one specific caller

## End-to-end platform flow and boundaries

Treat the default Ala flow like this:
- public client or frontend -> gateway -> backend service
- backend service -> backend service only for internal workloads that truly require a synchronous hop
- backend service -> async infrastructure for queue, event, or job delivery when appropriate

### Frontend and gateway orientation

Rules:
- frontend clients call documented gateway-facing routes, not service-local routes discovered from backend repos
- frontend clients must never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, `X-User-Mobile`, `X-User-Fname`, `X-User-Lname`, or `X-Location-*`
- trusted headers belong to the gateway-to-service contract, not the public client contract
- keep route ownership clear so frontend, gateway, and backend work stay aligned
- if a route is operational, frontend clients must not treat it as product behavior
- if a route previously depended on the retired profile blob, move that client integration to the public auth or profile APIs instead of reviving `X-Profile`

Route-shape reminder:
- gateway-facing routes may include a service prefix such as `/auth`, `/comment`, `/ticket`, `/vod`, or `/wa`
- trusted internal routes stay service-owned and are not public frontend discovery surfaces
- operational routes remain separate from product routes even when they share the `/api/*` prefix

### Operational caller expectations

Rules:
- end-user clients should not depend on operational routes for product behavior
- `/api/ready` is an operational contract and must not turn into a login helper, feature-flag probe, or frontend preflight endpoint
- the contract must not assume one specific operational caller

### Internal hop discipline

Rules:
- preserve `X-Request-Id` and `traceparent` across internal HTTP hops
- keep trusted header parsing and normalization close to the receiving edge
- do not proxy another service's `/api/ready` unless that dependency is an explicit approved rollout requirement
- if a service depends on shared infrastructure such as Redis or RabbitMQ, check that infrastructure directly instead of proxying another app's status
- if a frontend or service needs domain behavior from another service, prefer that service's public API or events over direct table coupling
- downstream services may consume compact trusted name and location headers, but they must not fabricate display-name fields from compact ids unless another explicit source-of-truth contract owns that lookup
- backend services may keep local user projections or immutable request snapshots, but auth-service remains the source of truth for the latest identity state

## Deployment and runtime contract

Use this section when the task touches how an Ala service is deployed, discovered, bootstrapped, or supplied with runtime infrastructure.

### Ownership split

Rules:
- treat Arvan Kubernetes as the primary production path for Ala services
- treat Docker Compose and Docker Swarm as supported Ala runtime modes that must still satisfy the same service contract
- load `$caas-arvan-kuber` for Helm, values layering, OCI chart delivery, cluster secrets, and GitLab rollout mechanics
- load `$alaa-docker-production` for Dockerfile hardening, runtime-user rules, Compose and Swarm delivery mechanics, and registry-plumbing details
- do not duplicate Kubernetes implementation detail in this guide when the concern is already owned by `$caas-arvan-kuber`

### Required deployment modes

Normalized Ala deployment modes:

| Mode | Status in the Ala contract | Primary use |
|---|---|---|
| Arvan Kubernetes | primary production path | managed production rollout |
| Docker Compose | supported Ala runtime mode | single-host local, validation, or operator-managed runtime |
| Docker Swarm | supported Ala runtime mode | multi-node Docker runtime with production-capable service discovery |

Rules:
- new or refactored Ala services should document the Arvan Kubernetes path and the Docker Compose and Docker Swarm path
- when a repository cannot support one of the Docker modes yet, report the blocker explicitly instead of silently omitting the mode
- prefer one wrapper entrypoint such as `scripts/docker/up-local.sh <compose|swarm>` or `dev|compose|swarm|prod` aliases when a repo exposes both modes
- keep mode names explicit in docs, scripts, and examples

### PostgreSQL source modes

Rules:
- choose the PostgreSQL source mode explicitly; do not auto-switch based on discovery
- keep the app runtime tuple explicit and stable: `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`
- keep bootstrap or admin connectivity separate from the app runtime tuple
- shared-mode bootstrap and external-mode provisioning must never be treated as permission to create a second runtime Postgres

#### Mode 1 - Shared Ala Postgres

This mode uses the canonical Ala shared infra and canonical names.

Rules:
- when shared mode is selected, the service must target the canonical shared infra identity and canonical Postgres endpoint for that environment
- if the canonical shared infra already exists, the service must reuse it
- if the canonical shared infra already exists, the service must not create another Postgres, another infra project, or another shared-infra identity
- if the existing shared infra is unhealthy, unreachable, misnamed, or incompatible, fail fast and report the blocker explicitly
- only create shared infra when shared mode is explicitly selected, the canonical shared infra is absent, and the service owns a safe idempotent bootstrap path

##### Helm and Arvan Kubernetes shared mode

Rules:
- support the current Ala `infra-pipeline` model where runtime DB settings and bootstrap DB settings are provided through the shared platform flow
- keep the app runtime connection tuple explicit even when some values come from `infra-pipeline`-managed secrets or overlays
- keep app runtime DB host selection separate from `dbBootstrap.pgHost`
- do not require service-local chart logic to invent a second Postgres when `infra-pipeline`-managed shared Postgres is the selected mode

##### Docker Compose and Docker Swarm shared mode

Rules:
- in Docker shared mode, reuse the canonical shared infra project and canonical shared Postgres instead of creating a second service-local Postgres when shared infra already exists
- wrapper scripts may bootstrap the canonical shared infra only when it is absent and shared mode is explicitly selected
- wrapper scripts must fail fast on unhealthy or incompatible existing shared infra instead of auto-falling back to a new local Postgres

#### Mode 2 - External Postgres

This mode is operator-selected explicitly.

Rules:
- use the explicit app runtime tuple `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, and `DB_PASSWORD`
- do not auto-switch into shared mode just because shared infra is discoverable
- do not create shared infra in external mode
- in Helm or Arvan Kubernetes external mode, allow runtime secrets or overlays to supply the full app tuple from an operator-managed external database
- in Docker Compose and Docker Swarm external mode, allow the app to connect directly to an external database without starting shared Postgres
- if the external database and user already exist, allow provisioning to be disabled

#### Provisioning and admin separation

Rules:
- treat `DB_PROVISION_*` and equivalent bootstrap or admin credentials as a separate provisioning path, not as part of the app runtime tuple
- only use `DB_PROVISION_*` when the selected mode requires service-owned database or schema provisioning
- in external mode, `DB_PROVISION_*` may target the external server for one-time or idempotent provisioning, but that must not create or imply a second runtime Postgres
- in shared mode, `DB_PROVISION_*` may help provision the service-owned database, schema, user, or grants inside the canonical shared Postgres, but that must not create a second Postgres instance

### Shared Docker network contract

The canonical Ala shared Docker network is:
- `alaa-shared-network`

Rules:
- attach every Ala service that needs cross-repo Docker communication to `alaa-shared-network`
- create the shared network automatically when it does not exist
- do not require operators to create the network manually before first deploy
- keep cross-service Docker DNS on the shared network instead of inventing per-repo isolated networks when inter-service routing is required

### Shared Docker infra contract

The canonical Ala shared Docker infra identity is:
- `alaa-shared-infra`

Rules:
- if the canonical shared infra exists, it must be reused
- if the canonical shared infra exists, it must not create a second shared-infra copy, another Postgres, or a renamed sibling infra project
- if the canonical shared infra exists but is unhealthy, unreachable, misnamed, or incompatible, fail fast and report the blocker explicitly
- only create the canonical shared infra when it is absent, shared mode is explicitly selected, and the service bootstrap owns a safe, idempotent creation path
- keep shared infra names stable across repos so services can discover the same Postgres, Redis, RabbitMQ, ClickHouse, or equivalent dependencies
- do not create a second copy of shared infra in shared mode

### Canonical service naming and Docker DNS contract

Rules:
- keep the top-level Compose or stack project name aligned with the service slug such as `auth`, `gateway`, `comment`, `ticket`, `vod`, or `wa`
- for PHP or Laravel HTTP entry services, expose the canonical internal app alias `<service>-platform-app-php`
- use the HTTP-serving app service, not workers, as the canonical backend alias
- make gateways, reverse proxies, and internal Docker callers target the canonical alias instead of replica container names or node IPs
- in Swarm, configure the canonical HTTP service with `endpoint_mode: vip` or an equivalent stable service-DNS behavior
- when a service is not PHP-based, expose one stable internal DNS name and document the equivalent canonical alias explicitly

### Gateway routing contract for Docker runtimes

Rules:
- in Docker Compose and Docker Swarm, gateway-side backend discovery should use direct DNS against the canonical backend alias
- do not couple gateway config to replica names, task IDs, or host IP lists
- keep gateway backend naming aligned with the service-owned canonical alias
- when a backend is not yet wired into the shared Docker runtime, document the gap instead of inventing alternate names

### Infra bootstrap and service-owned data contract

Rules:
- before app startup, ensure the required shared infra exists or can be reused safely
- keep infra bootstrap idempotent so repeated deploys converge instead of drift
- each service owns its own database, schema, user, grants, and bootstrap data inside the shared infra
- for PostgreSQL-backed services, provision a dedicated database and/or schema and service user, then apply the required grants idempotently
- in shared mode, do that provisioning inside the canonical shared Postgres instead of creating a new Postgres instance
- in external mode, provision against the explicit external server only when external provisioning is intentionally enabled
- do not treat app runtime credentials as bootstrap or admin credentials
- preserve the administrator or `postgres` maintenance path instead of narrowing infra access so far that emergency operations break
- for ClickHouse-backed services, create the service-local database, users, and DDL idempotently before assuming runtime readiness
- do not couple one service to another service's application schema or service-owned tables

### Secret and key material contract

Rules:
- never bake application secrets, App keys, Passport keys, or runtime credentials into images or committed files
- in Arvan Kubernetes, let the infra pipeline or chart-driven secret mounts provide the runtime secret material and follow `$caas-arvan-kuber`
- in Docker Compose and Docker Swarm, let wrapper scripts generate, synchronize, or provision the runtime secret material before bringing services up
- auth owns its own App key and Passport private and public key pair
- gateway may consume only the auth public key required to verify access tokens
- in Docker runtimes, synchronize the gateway copy of the auth public key automatically instead of relying on manual operator copying
- in Swarm, prefer external secrets with explicit `uid`, `gid`, and restrictive file `mode`

### Registry contract

Rules:
- route public upstream image pulls through a configurable pull-through mirror
- use `mirror.cdn.ir` as the normalized Ala default when the environment does not explicitly override the mirror
- treat the pull-through mirror rule as mandatory for all public upstream images in Ala repositories, including CI helper images, validation images, OpenFGA runtime or CLI images, and public Dockerfile base images
- for Ala GitLab pipelines, treat `MAIN_PUBLIC_DOCKER_REGISTRY_MIRROR` as the canonical public-mirror input variable
- normalize repo-local CI variables such as `PUBLIC_DOCKER_REGISTRY` from `MAIN_PUBLIC_DOCKER_REGISTRY_MIRROR` when a repository wants a shorter local alias, but do not invent direct-public fallback behavior in CI
- push and pull first-party images and OCI artifacts through the private registry path
- for Ala GitLab pipelines, keep first-party registry auth and OCI delivery on `MAIN_DOCKER_PRIVATE_REGISTRY`, `MAIN_DOCKER_PRIVATE_REGISTRY_USER`, and `MAIN_DOCKER_PRIVATE_REGISTRY_PASS`
- for Arvan Kubernetes image pulls, treat `MAIN_IMAGE_PULL_SECRET_NAME` as the canonical input for the namespace-local docker-registry secret name and wire it into the chart or manifest instead of assuming anonymous pulls
- keep registry credentials explicit in CI, runtime, and cluster configuration instead of relying on anonymous behavior
- do not hardcode direct Docker Hub pulls when the family mirror contract exists
- keep the repo-local environment variable names explicit in docs and CI, even when different repos choose slightly different variable names
- do not leave Kubernetes pull-secret values cosmetic; if a deploy script sets `image.pullSecrets` or an equivalent field, the chart or manifest must render that field into the pod spec

### Testing and validation contract

Rules:
- treat PostgreSQL and any service-required infra such as Redis, RabbitMQ, or ClickHouse as the production truth
- for Laravel services, also support fast tests and runtime validation on SQLite unless a documented blocker makes that impossible
- keep SQLite support as a test and validation acceleration path, not as a substitute for production readiness checks
- validate Docker configuration before deploy and fail fast on missing secrets, invalid Compose models, or missing bootstrap prerequisites
- keep service-level readiness checks aligned with the dependencies the service actually owns

## Exact `/api/health`

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

## Exact `/api/ready`

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

### Exact readiness naming

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

### Illustrative auth readiness precedent

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

## Observability contract

### Exact response headers

The target Ala response-header contract is:
- `X-Request-Id`
- `traceparent`

Non-target legacy headers:
- `X-Correlation-Id`
- `X-Trace-Id`

Rules:
- new implementations must target only `X-Request-Id` and `traceparent`
- if a service still emits, parses, forwards, tests, or documents `X-Correlation-Id`, migrate it to `X-Request-Id` plus `traceparent` and remove the stale implementation in the same effort
- after applying this skill, no service code, config, docs, tests, or emitted response headers should still contain `X-Correlation-Id`

### Exact `X-Request-Id` rules

Rules:
- preserve a nonblank safe inbound `X-Request-Id`
- treat a value as safe only if it is one visible token, trimmed, and reasonably bounded in length
- if absent or invalid, generate a new lowercase UUIDv7
- keep it stable for the lifetime of the request
- return it on every `/api/*` response including `/api/health`, `/api/ready`, and rendered API error responses
- include it in every structured request log and relevant denial or failure log

### Exact `traceparent` rules

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
- do not require a separate `X-Trace-Id` response header

### Structured log field contract

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
- `project_id` when available
- `user_id` when available and safe
- `http.method`
- `http.route` or route name
- `http.status`
- `duration_ms`

Keep the field names stable so SOC queries and runbooks remain reusable.

This aligns with `$alaa-observability-soc` and keeps SOC queries stable.

### Event and code naming contract

For request and operational flows owned by this skill, use these exact event names:
- `http.request.completed`
- `http.request.failed`
- `service.readiness.failed`
- `service.readiness.recovered` when a repository explicitly tracks readiness transitions
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
- do not invent alternate names for the same event type
- keep `event` and `code` aligned
- keep user-facing messages separate from these machine-readable names

### Probe-noise rule

Rules:
- suppress low-value `http.request.completed` logs for successful `/api/health`
- suppress low-value `http.request.completed` logs for successful `/api/ready`
- keep not-ready responses observable
- keep unexpected failures observable
- if readiness transition tracking exists, use `service.readiness.failed` and `service.readiness.recovered`

### Metrics boundary rule

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

## `RequestObservabilityMiddleware`

For Laravel services, apply `RequestObservabilityMiddleware` early on `/api/*` traffic.

Preferred order:
1. `RequestObservabilityMiddleware`
2. tenant or project normalization needed before bindings
3. `SubstituteBindings`
4. `ResolveUserMiddleware` or the equivalent trusted-user normalization layer
5. controller and policy-facing code

Required behavior:
- compute canonical `X-Request-Id`
- compute canonical `traceparent`
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

## `ResolveUserMiddleware`

For downstream trusted Laravel services, use `ResolveUserMiddleware` or an equivalent request-based layer that satisfies the same semantics.

Exact trusted headers:
- `X-Project-Id`
- `X-User-Id`
- `X-Access`
- `X-Access-Token-Id`
- `X-User-Mobile`
- `X-User-Fname`
- `X-User-Lname`
- `X-Location-Ostan`
- `X-Location-Shahrestan`
- `X-Location-Bakhsh`
- `X-Location-Shahr`
- `X-Location-Shobe`
- `X-Location-School`

Required validation behavior:
- validate `X-Project-Id` as UUIDv7
- validate `X-User-Id` as a positive integer
- decode `X-Access` as the base64url permission bitmap
- reject `X-Access` when it maps to zero known permissions after service-local mapping
- normalize `X-Access-Token-Id` as an optional non-empty trusted token identifier when present
- handle `X-User-Mobile` exactly according to `$alaa-trust-gateway-auth`
- normalize `X-User-Fname` and `X-User-Lname` as nullable trimmed strings
- validate each `X-Location-*` header as a non-negative integer when present
- use the exact auth error codes owned by `$alaa-trust-gateway-auth`

Actor context must be able to hold at least:
- trusted project identifier
- trusted user identifier
- normalized permission names
- trusted access-token identifier when present
- normalized first and last name values
- normalized location object with `ostan`, `shahrestan`, `bakhsh`, `shahr`, `shobe`, and `school`
- trusted mobile when present
- `request_id`
- `trace_id`
- optional derived role when the service uses role inference

Auth synchronization rules:
- keep `$request->user()` and `Auth::user()` consistent
- also synchronize documented legacy guards that the repository still reads
- do not rebuild the actor independently in controllers or policies
- keep synchronization request-scoped and Octane-safe

Required support components:
- trusted request context helper
- trusted actor context value object or DTO
- permission bitmap decoder and mapper
- compact trusted user-projection normalizer
- auth-state synchronizer
- optional role-derivation helper when needed
- stable API-error mapping path aligned with `$alaa-trust-gateway-auth`

Implementation rules:
- do not parse raw trusted headers in controllers, policies, resources, or repositories
- keep policy and Gate decisions focused on business authorization after auth context is normalized
- if the service persists trusted user data, keep mutable projections separate from immutable snapshots
- do not fabricate display-city fields from compact location ids unless another contract owns that lookup

## Laravel success-response contract

Treat Resources as the public success-response boundary for Laravel `/api/*` success responses.

Rules:
- use `JsonResource` or `ResourceCollection`
- keep controllers responsible for HTTP status and transport serialization
- keep services returning domain data or typed DTOs, not transport-shaped arrays
- keep Resources responsible for public field shaping
- keep controllers thin and deterministic

Exact success envelope rules:
- every successful `/api/*` JSON response must use a top-level `data` key unless a documented exception exists
- `data` must be an object for one resource or one compound result
- `data` must be an array for collections
- nested child resources stay inline and do not get their own nested `data` wrapper
- use top-level `meta` only for transport metadata
- use top-level `links` only for pagination or true document navigation concerns

Boundary rules:
- do not return transport-shaped arrays from services
- do not leak raw models, internal IDs, persistence-only fields, or temporary implementation fields through controllers
- attach transport headers at the Resource response boundary when needed

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

Laravel implementation rules:
- inspect middleware order relative to `SubstituteBindings`
- use request-scoped auth normalization compatible with Laravel guards
- use current Laravel request-based auth mechanisms when appropriate
- use current Laravel logging-context sharing mechanisms
- keep Octane request state isolated per request
- keep controllers thin and Resources explicit

## Copy baselines

When a Laravel repository needs implementation help, use `references/50-laravel-copy-baselines.md` as the copy-oriented baseline and adapt only namespaces and helper wiring, not behavior.

Do not assume the middleware can attach headers after a rethrow. The exception handler must attach `X-Request-Id` and `traceparent` to rendered API error responses by reading the shared request context.

Snapshot baseline:
- if a repo stores request-time user context, keep mutable projections separate from immutable snapshots
- prefer a repository-owned projection that preserves compact ids instead of inventing display names
- keep missing location ids explicit instead of fabricating location names

## Apply workflow and review checklist

### Apply workflow

1. identify service mode
2. load the smallest relevant contract file
3. load companion skills
4. inspect the current repo shape
5. converge routes, middleware, helpers, headers, events, envelopes, and runtime rules to the exact contract
6. remove active dependencies on retired trust surfaces such as `X-Profile` or old claim names when the compact contract replaced them
7. add missing helper or support components instead of hand-waving them
8. add or align `/api/health`, `/api/ready`, and `ops:ready --json` when the target is Laravel
9. add or align `RequestObservabilityMiddleware` and `ResolveUserMiddleware` semantics where required
10. update docs, Postman, and runbooks in the same patch when public or operational behavior changes
11. run focused tests for every changed contract surface
12. report blockers explicitly when exact convergence is not possible

### Minimum validation checklist

#### Operational

- `/api/health` is public and dependency-free
- `/api/ready` is public and uses the exact envelope
- `service` comes from the canonical service config
- healthy and not-ready paths are covered
- `ops:ready --json` matches the route when implemented

#### Observability

- missing or invalid `X-Request-Id` generates lowercase UUIDv7
- valid incoming `X-Request-Id` is preserved
- missing or invalid `traceparent` generates a fresh valid value
- valid incoming `traceparent` is preserved
- `/api/health` and `/api/ready` return `X-Request-Id` and `traceparent`
- rendered API error responses after exceptions still return `X-Request-Id` and `traceparent`
- no service code, config, docs, tests, or emitted headers still mention `X-Correlation-Id`
- successful probes stay low-noise
- readiness failure and request failure logs use the exact event and code rules
- metrics use bounded labels only

#### Trusted ingress

- missing, blank, or invalid `X-Project-Id`
- missing, blank, or invalid `X-User-Id`
- missing, invalid, or zero-known-permission `X-Access`
- invalid `X-User-Mobile`
- malformed `X-User-Fname` or `X-User-Lname`
- malformed `X-Location-*` values
- parity between `$request->user()` and `Auth::user()`
- parity with any legacy guard still in use

#### Laravel response boundary

- successful `/api/*` responses use the exact `data` envelope
- `meta` and `links` follow the contract
- Resources do not leak internal fields
- docs and Postman examples match the actual public response shape

### Review checklist

#### Core and deployment

- `/api/health` touches PostgreSQL, Redis, RabbitMQ, ClickHouse, or another service
- `/api/ready` depends on tokens, cookies, OTP, or end-user state
- `/api/ready` uses the wrong envelope or wrong key names
- no explicit shared-versus-external Postgres mode selection in deploy-facing docs or config expectations
- no documented Arvan Kubernetes production path
- no Compose or no Swarm story and no explicit blocker
- no `alaa-shared-network` use where cross-service Docker routing is required
- no reuse or bootstrap path for `alaa-shared-infra`
- a service-local Postgres or sibling infra project is created while canonical shared infra already exists
- automatic fallback from shared mode to a new local Postgres
- implicit switching between shared and external Postgres modes
- `DB_PROVISION_*` or equivalent bootstrap credentials are treated as the app runtime tuple
- gateway or another proxy targets replica names, task IDs, or host IPs instead of the canonical backend alias
- no canonical `<service>-platform-app-php` alias for a PHP or Laravel HTTP service and no documented equivalent
- secrets or keys are copied manually instead of being generated, synchronized, or mounted by the deploy path
- direct public-registry pulls remain instead of the configured pull-through mirror
- no private-registry story exists for first-party images or OCI artifacts
- no SQLite fast-test path exists for a new Laravel service and no documented blocker exists

#### Observability and trusted ingress

- `service` returns a framework or runtime name
- `X-Correlation-Id` remains anywhere in service code, config, tests, docs, or emitted headers after the migration
- `X-Trace-Id` is still treated as a response-header requirement
- request or readiness logs invent alternate event names for the same flow
- metrics use unbounded labels
- trusted headers are parsed in controllers, policies, or repositories
- `$request->user()` and `Auth::user()` can diverge within one request
- compact trusted name and location headers are re-parsed in multiple layers instead of one normalization path
- a repository keeps old and new trust contracts active in parallel without an explicit migration blocker
- a repository invents location-name lookup behavior even though the compact contract only carries ids

#### Laravel boundary and docs

- Laravel services return transport-shaped arrays or raw models instead of Resource boundaries
- docs or API artifacts drift from implementation

### Anti-patterns

- treating the skill as optional guidance instead of a hard contract
- copying only part of the `/api/ready` contract and changing the rest locally
- leaving `X-Correlation-Id` anywhere in the service after migrating to `X-Request-Id`
- inventing local event names that conflict with `$alaa-observability-soc`
- inventing local auth error names that conflict with `$alaa-trust-gateway-auth`
- keeping stale compatibility branches, helpers, tests, or docs for removed contract surfaces
- assuming middleware can attach response headers after a rethrow without exception-handler support
- scattering trusted-user normalization across controllers, policies, resources, and observers
- leaving helper responsibilities implicit so each agent re-invents them
- reviving the retired profile-blob trust surface instead of consuming the compact header projection
- inventing location-name lookup behavior instead of treating compact ids as compact ids
