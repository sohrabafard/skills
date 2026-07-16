# Alaa Services Contract Full Guide

This file preserves the complete contract in one place.
It mirrors the split references below and should be kept aligned with them in the same patch.

## Included references
- `05-scope-service-modes-and-auth-routing.md`
- `10-core-service-contract.md`
- `15-deployment-and-runtime-contract.md`
- `20-operational-and-observability-contract.md`
- `21-alaa-platform-observability-directive.md`
- `25-end-to-end-flow-and-boundaries.md`
- `26-request-time-authorization-openfga.md`
- `27-notification-service-contract.md`
- `30-trusted-ingress-and-laravel-contract.md`
- `32-auth-totp-and-step-up-contract.md`
- `35-permission-catalog-and-service-configs.md`
- `40-apply-checklist-and-anti-patterns.md`
- `50-laravel-copy-baselines.md`
- `60-frontend-sdk-consumption-contract.md`
- `65-frontend-page-kit-and-widgets-contract.md`

---

# Scope, Service Modes, And Auth Routing

Use this file when the task is about onboarding an agent to the Ala services contract before code changes start.

## Purpose and use

Use this skill to hard-code the Ala backend service contract across Ala services.

This contract exists so agent outputs stay consistent across services and so operational visibility remains predictable for developers, SOC operators, and platform maintainers.

This skill is intentionally Ala-specific. The portability requirement for this skill is about filesystem independence and reuse across machines, not about being generic to unrelated organizations.

Use it when:
- creating or changing `auth`, `content`, `comment`, `ticket`, `gateway`, `entitlement-platform`, `vod`, `wa`, `notification`, `assessment`, or another Ala backend or platform service
- explaining how a frontend-facing backend sits behind the gateway and inside the wider Ala platform
- standardizing the shared `service-ci-kit` GitLab CI/CD baseline for new or refactored Ala services
- standardizing `/api/health`
- standardizing `/api/ready`
- fixing exact readiness payloads and check naming
- standardizing `X-Request-Id`, `traceparent`, and queryable `trace_id`
- enforcing request and readiness event names and machine-readable codes
- standardizing `RequestObservabilityMiddleware`
- standardizing `ResolveUserMiddleware`
- adding or reviewing the Alaa Platform Observability Directive
- aligning OpenTelemetry, SigNoz, Sentry, and Prometheus behavior across Go, Laravel, HAProxy, Vector, OpenFGA, and future services
- aligning Laravel Resource-first `/api/*` success responses
- helping a new Ala service understand the current service landscape, ownership boundaries, and expected interaction model before implementation
- clarifying auth terms acceptance so agents do not search for or invent a retired accept-terms API
- clarifying optional auth TOTP setup, authenticator QR generation, recovery-code handling, and SDK/frontend expectations
- adding, reviewing, or documenting route-level `require_totp:<purpose>` enforcement
- forcing cross-service consistency where agents would otherwise improvise

## Platform ownership picture

Use this picture before code changes when a repo needs platform orientation.

Default Ala flow:
- frontend or public client -> gateway -> backend service
- gateway may call a request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa`
- entitlement-platform keeps fine-grained authorization state through `entitlement-api`, `projector`, and OpenFGA

Plain meaning:
- the gateway owns authentication, spoofed-header removal, and trusted header injection
- entitlement-platform owns route-level fine-grained authorization state and runtime checks when those checks are enabled
- a normal backend service behind the gateway still owns request normalization, business authorization, response shaping, and observability inside the service
- frontend code must use gateway-facing routes and must never generate trusted internal headers

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
- request and readiness log field schema
- Ala service map and interaction orientation for new services

Read next:
- `10-core-service-contract.md`
- `20-operational-and-observability-contract.md`

### Mode A+ - Platform observability directive

Adds:
- the platform-wide telemetry path
- OpenTelemetry SDK and OTLP configuration rules
- queryable `trace_id`
- exception delivery through SigNoz when Sentry is absent
- Collector gateway ownership
- Prometheus scrape rules and metric naming
- shared metric catalog and validation rules
- cross-runtime observability guidance for Go, Laravel, HAProxy, Vector, WA, OpenFGA, and future services

Read next:
- `20-operational-and-observability-contract.md`
- `21-alaa-platform-observability-directive.md`

### Mode B - Laravel backend service

Adds:
- route names `api.health` and `api.ready`
- `php artisan ops:ready --json`
- Laravel middleware ordering guidance
- Resource-first `/api/*` success responses

Read next:
- `10-core-service-contract.md`
- `30-trusted-ingress-and-laravel-contract.md`

### Mode A++ - Deployment and runtime contract

Adds:
- Arvan Kubernetes versus Docker ownership
- shared `service-ci-kit` GitLab CI/CD baseline for Ala services
- thin-wrapper `.gitlab-ci.yml` and shared-versus-local CI ownership
- shared-versus-external Postgres mode selection
- canonical shared Docker network, shared infra, DNS alias, registry, and runtime-secret rules

Read next:
- `10-core-service-contract.md`
- `15-deployment-and-runtime-contract.md`

### Mode C - Laravel downstream trusted service

Adds:
- exact trusted-header handling
- one normalized actor context
- request and auth facade parity
- `ResolveUserMiddleware` or equivalent downstream normalization layer

Read next:
- `30-trusted-ingress-and-laravel-contract.md`
- `$alaa-trust-gateway-auth`

### Mode C+ - Permission catalog consumer

Adds:
- generated service-local permission configs
- permission bitmap id governance
- `X-Access` permission-name mapping
- catalog drift checks
- one-service-at-a-time apply discipline

Read next:
- `35-permission-catalog-and-service-configs.md`
- `$alaa-trust-gateway-auth`

### Mode D - Laravel auth-boundary service

Allows:
- request guards or `Auth::viaRequest(...)` instead of a literal downstream `ResolveUserMiddleware`

But still requires:
- the same exact trusted-header semantics
- the same outward auth behavior
- the same observability contract
- the same response contract where applicable

Read next:
- `30-trusted-ingress-and-laravel-contract.md`
- `50-laravel-copy-baselines.md`

### Mode D+ - Auth TOTP management and forced route step-up

Use when the task is about optional TOTP enrollment, authenticator-app setup, QR generation, `AUTH_TOTP_ENABLED`, recovery codes, forced route-level MFA, `require_totp:<purpose>`, signed step-up proof tokens, local proof caching, gateway `X-TOTP-Proof` verification, or SDK/frontend step-up handling.

Read next:
- `32-auth-totp-and-step-up-contract.md`
- `$alaa-trust-gateway-auth` for gateway trust boundaries and public/internal route separation
- `$alaa-frontend-developer` for SDK and frontend challenge-and-retry behavior

## Auth-specific routing note

- When the task touches the `auth` service and any frontend or frontend-facing identity integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing.
- Treat that document as the canonical frontend integration contract for auth academic policy.
- When auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort.
- Auth terms acceptance is implicit in successful OTP verification and login. Treat `user/accept-terms-and-conditions` as a retired flow, not as a missing current API.
- The frontend may present a non-removable terms notice or required checkbox before OTP request. The backend acceptance moment is successful `POST /api/v3/otp/verify`, when the service creates the authenticated session.
- Do not add or search for a separate accept-terms endpoint, request field, `terms_accepted_at`, `terms_version`, or consent table unless the user explicitly asks to change the legal/audit contract. If they do, treat it as a new product/legal contract change that needs docs, Postman, tests, and migration planning.
- Auth TOTP is optional self-service until a route explicitly attaches `require_totp:<purpose>`. When `AUTH_TOTP_ENABLED=true`, clients can expose setup and recovery-code flows; when disabled, clients should treat the TOTP API as unavailable, not as a generic missing route.
- The backend returns `secret` and `otpauth_uri` for setup; clients generate the QR code from `otpauth_uri`. Forced route rollout must document the purpose, signed proof-token target, client cache and retry behavior, gateway `X-TOTP-Proof` verification, downstream `X-TOTP-*` metadata, and Postman/OpenAPI examples.

## Working rule

- Start here when the task is cross-cutting or the target repository is new to the Ala contract.
- When the target is a new or refactored Ala service, read the deployment contract before inventing repo-local GitLab CI behavior.
- When observability design is part of the task, read `21-alaa-platform-observability-directive.md` early instead of treating metrics or tracing as an afterthought.
- After choosing a service mode, move to the smallest contract file that owns the exact rule you need.
- Keep `full-guide.md` as the merged preserved view, not as the only place where agents can discover these onboarding rules.

---

# Core Service Contract

## Hard contract posture

This skill exists to make Ala services converge on one contract.

Rules:
- Treat the contract as exact unless a blocking incompatibility is reported.
- Do not let agents choose alternative `/api/ready` shapes, alternate headers, different event names, or repo-local metric families just because they also look reasonable.
- Prefer convergence to the Ala contract over local stylistic preference.
- If a service still carries a replaced contract surface such as `X-Correlation-Id`, migrate it fully and delete the stale implementation in the same effort.

## Ala service map

This skill should help a new service understand the current Ala service landscape before it aligns itself.

| Service | Primary ownership | Main interaction expectations |
|---|---|---|
| `auth` | canonical auth and profile truth, OTP login, token lifecycle, RBAC compilation, trusted profile APIs | downstream services should trust gateway-derived identity and should not duplicate canonical auth or profile ownership |
| `content` | macroservice for `course`, `set`, and `content`; long-term learning-content source of truth | use `content` for the new educational-content domain model instead of reviving legacy `vod` ownership |
| `vod` | legacy learning and playback service during migration | keep it aligned to the same platform contract while moving learning-content responsibilities to `content` |
| `comment` | tenant-scoped comments, replies, likes, moderation, durable outbox publication | frontends and backends should use the comment API or comment events rather than couple to comment tables |
| `ticket` | support-ticket management, ticket messages, queue-driven notifications, local user projection | protected routes trust gateway-derived context; cross-service consumers should respect ticket ownership and its service-local API |
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

## Operational caller expectations

`GET /api/health` and `GET /api/ready` exist for:
- gateway and ingress probes
- orchestrators and rollout automation
- runtime validation scripts
- smoke checks
- automated tests

Rules:
- end-user clients should not depend on these routes for product behavior
- `/api/ready` may be called by gateway, ingress, orchestrators, or runtime validators, but the contract must not assume one specific caller

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
- `checks` must be an object keyed by canonical check name
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

## Laravel operational baseline

For Laravel services:
- implement `GET /api/health`
- implement `GET /api/ready`
- implement `php artisan ops:ready --json`
- back the route and command with one shared readiness collector when feasible
- test healthy and not-ready paths explicitly

---

# Deployment and Runtime Contract

Use this file when the task touches how an Ala service is deployed, discovered, bootstrapped, or supplied with runtime infrastructure.

This file is Ala-specific and normative. Use `$alaa-docker-production` for generic Docker engineering details and `$caas-arvan-kuber` for the primary Arvan Kubernetes production path.

## Ownership split

Rules:
- treat Arvan Kubernetes as the primary production path for Ala services
- treat Docker Compose and Docker Swarm as supported Ala runtime modes that must still satisfy the same service contract
- load `$caas-arvan-kuber` for Helm, values layering, OCI chart delivery, cluster secrets, and GitLab rollout mechanics
- load `$alaa-docker-production` for Dockerfile hardening, runtime-user rules, Compose and Swarm delivery mechanics, and registry-plumbing details
- do not duplicate Kubernetes implementation detail in this file when the concern is already owned by `$caas-arvan-kuber`

## GitLab CI/CD baseline contract

Rules:
- for Ala Laravel backend services that follow the shared `platform-app-php` delivery model, default to the shared `service-ci-kit` project for GitLab CI/CD
- keep `.gitlab-ci.yml` as a thin include-based wrapper and pin an explicit `SERVICE_CI_KIT_REF`
- keep shared CI logic in `service-ci-kit`; do not copy shared `ci/scripts/*` trees or local semantic-release helper trees into service repositories
- keep only service-local CI assets in the app repo, such as `.gitlab-ci.yml`, `.releaserc.json`, `ci/helm/values.app.yaml`, `ci/helm/values.app.ops.yaml`, `ci/helm/values.app.hpa.yaml`, `ci/helm/values.ci.runtime.yaml`, and optional local overlays that the shared kit intentionally consumes
- when shared CI behavior must change, update `service-ci-kit` first, release a new kit ref, and then bump the pinned ref in service repositories
- load `$alaa-gitlab-ci-cd` for GitLab authoring, validation, and debugging, but keep the Ala fleet policy in this skill instead of moving it into the generic GitLab skill
- if a repository cannot use `service-ci-kit`, report the blocker explicitly instead of silently reintroducing a repo-owned pipeline

## Required deployment modes

Normalized Ala deployment modes:

| Mode             | Status in the Ala contract | Primary use                                                         |
|------------------|----------------------------|---------------------------------------------------------------------|
| Arvan Kubernetes | primary production path    | managed production rollout                                          |
| Docker Compose   | supported Ala runtime mode | single-host local, validation, or operator-managed runtime          |
| Docker Swarm     | supported Ala runtime mode | multi-node Docker runtime with production-capable service discovery |

Rules:
- new or refactored Ala services should document the Arvan Kubernetes path and the Docker Compose and Docker Swarm path
- when a repository cannot support one of the Docker modes yet, report the blocker explicitly instead of silently omitting the mode
- prefer one wrapper entrypoint such as `scripts/docker/up-local.sh <compose|swarm>` or `dev|compose|swarm|prod` aliases when a repo exposes both modes
- keep mode names explicit in docs, scripts, and examples

## PostgreSQL source modes

Rules:
- choose the PostgreSQL source mode explicitly; do not auto-switch based on discovery
- keep the app runtime tuple explicit and stable: `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`
- keep bootstrap or admin connectivity separate from the app runtime tuple
- shared-mode bootstrap and external-mode provisioning must never be treated as permission to create a second runtime Postgres

### Mode 1 - Shared Ala Postgres

This mode uses the canonical Ala shared infra and canonical names.

Rules:
- when shared mode is selected, the service must target the canonical shared infra identity and canonical Postgres endpoint for that environment
- if the canonical shared infra already exists, the service must reuse it
- if the canonical shared infra already exists, the service must not create another Postgres, another infra project, or another shared-infra identity
- if the existing shared infra is unhealthy, unreachable, misnamed, or incompatible, fail fast and report the blocker explicitly
- only create shared infra when shared mode is explicitly selected, the canonical shared infra is absent, and the service owns a safe idempotent bootstrap path

#### Helm and Arvan Kubernetes shared mode

Rules:
- support the current Ala `infra-pipeline` model where runtime DB settings and bootstrap DB settings are provided through the shared platform flow
- keep the app runtime connection tuple explicit even when some values come from `infra-pipeline`-managed secrets or overlays
- keep app runtime DB host selection separate from `dbBootstrap.pgHost`
- do not require service-local chart logic to invent a second Postgres when `infra-pipeline`-managed shared Postgres is the selected mode

#### Docker Compose and Docker Swarm shared mode

Rules:
- in Docker shared mode, reuse the canonical shared infra project and canonical shared Postgres instead of creating a second service-local Postgres when shared infra already exists
- wrapper scripts may bootstrap the canonical shared infra only when it is absent and shared mode is explicitly selected
- wrapper scripts must fail fast on unhealthy or incompatible existing shared infra instead of auto-falling back to a new local Postgres

### Mode 2 - External Postgres

This mode is operator-selected explicitly.

Rules:
- use the explicit app runtime tuple `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, and `DB_PASSWORD`
- do not auto-switch into shared mode just because shared infra is discoverable
- do not create shared infra in external mode
- in Helm or Arvan Kubernetes external mode, allow runtime secrets or overlays to supply the full app tuple from an operator-managed external database
- in Docker Compose and Docker Swarm external mode, allow the app to connect directly to an external database without starting shared Postgres
- if the external database and user already exist, allow provisioning to be disabled

### Provisioning and admin separation

Rules:
- treat `DB_PROVISION_*` and equivalent bootstrap or admin credentials as a separate provisioning path, not as part of the app runtime tuple
- only use `DB_PROVISION_*` when the selected mode requires service-owned database or schema provisioning
- in external mode, `DB_PROVISION_*` may target the external server for one-time or idempotent provisioning, but that must not create or imply a second runtime Postgres
- in shared mode, `DB_PROVISION_*` may help provision the service-owned database, schema, user, or grants inside the canonical shared Postgres, but that must not create a second Postgres instance

## Shared Docker network contract

The canonical Ala shared Docker network is:
- `alaa-shared-network`

Rules:
- attach every Ala service that needs cross-repo Docker communication to `alaa-shared-network`
- create the shared network automatically when it does not exist
- do not require operators to create the network manually before first deploy
- keep cross-service Docker DNS on the shared network instead of inventing per-repo isolated networks when inter-service routing is required

## Shared Docker infra contract

The canonical Ala shared Docker infra identity is:
- `alaa-shared-infra`

Rules:
- if the canonical shared infra exists, must reuse it
- if the canonical shared infra exists, must not create a second shared-infra copy, another Postgres, or a renamed sibling infra project
- if the canonical shared infra exists but is unhealthy, unreachable, misnamed, or incompatible, fail fast and report the blocker explicitly
- only create the canonical shared infra when it is absent, shared mode is explicitly selected, and the service bootstrap owns a safe, idempotent creation path
- keep shared infra names stable across repos so services can discover the same Postgres, Redis, RabbitMQ, ClickHouse, or equivalent dependencies
- do not create a second copy of shared infra in shared mode

## Canonical service naming and Docker DNS contract

Rules:
- keep the top-level Compose or stack project name aligned with the service slug such as `auth`, `gateway`, `comment`, `ticket`, `vod`, or `wa`
- for PHP or Laravel HTTP entry services, expose the canonical internal app alias `<service>-platform-app-php`
- use the HTTP-serving app service, not workers, as the canonical backend alias
- make gateways, reverse proxies, and internal Docker callers target the canonical alias instead of replica container names or node IPs
- in Swarm, configure the canonical HTTP service with `endpoint_mode: vip` or an equivalent stable service-DNS behavior
- when a service is not PHP-based, expose one stable internal DNS name and document the equivalent canonical alias explicitly

## Gateway routing contract for Docker runtimes

Rules:
- in Docker Compose and Docker Swarm, gateway-side backend discovery should use direct DNS against the canonical backend alias
- do not couple gateway config to replica names, task IDs, or host IP lists
- keep gateway backend naming aligned with the service-owned canonical alias
- when a backend is not yet wired into the shared Docker runtime, document the gap instead of inventing alternate names

## Infra bootstrap and service-owned data contract

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

## Secret and key material contract

Rules:
- never bake application secrets, App keys, Passport keys, or runtime credentials into images or committed files
- in Arvan Kubernetes, let the infra pipeline or chart-driven secret mounts provide the runtime secret material and follow `$caas-arvan-kuber`
- in Docker Compose and Docker Swarm, let wrapper scripts generate, synchronize, or provision the runtime secret material before bringing services up
- auth owns its own App key and Passport private and public key pair
- gateway may consume only the auth public key required to verify access tokens
- in Docker runtimes, synchronize the gateway copy of the auth public key automatically instead of relying on manual operator copying
- in Swarm, prefer external secrets with explicit `uid`, `gid`, and restrictive file `mode`

## Registry contract

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

## Testing and validation contract

Rules:
- treat PostgreSQL and any service-required infra such as Redis, RabbitMQ, or ClickHouse as the production truth
- for Laravel services, also support fast tests and runtime validation on SQLite unless a documented blocker makes that impossible
- keep SQLite support as a test and validation acceleration path, not as a substitute for production readiness checks
- validate Docker configuration before deploy and fail fast on missing secrets, invalid Compose models, or missing bootstrap prerequisites
- keep service-level readiness checks aligned with the dependencies the service actually owns

## Review checklist

Flag a problem when you see:
- no documented Arvan Kubernetes production path
- no Compose or no Swarm story and no explicit blocker
- no shared `service-ci-kit` baseline for an Ala Laravel backend that follows the shared `platform-app-php` delivery model
- a non-thin `.gitlab-ci.yml` in a service repo that should use the shared kit
- shared `ci/scripts/*` or local semantic-release helper trees reintroduced into a service repo
- undocumented divergence from the shared kit baseline
- no explicit shared-versus-external Postgres mode selection
- no `alaa-shared-network` use where cross-service Docker routing is required
- no reuse or bootstrap path for `alaa-shared-infra`
- a service-local Postgres or sibling infra project being created while canonical shared infra already exists
- automatic fallback from shared mode to a new local Postgres
- implicit switching between shared and external Postgres modes
- `DB_PROVISION_*` or equivalent bootstrap credentials being treated as the app runtime tuple
- gateway or another proxy targeting replica names, task IDs, or host IPs instead of the canonical backend alias
- no canonical `<service>-platform-app-php` alias for a PHP or Laravel HTTP service and no documented equivalent
- secrets or keys copied manually instead of being generated, synchronized, or mounted by the deploy path
- direct public-registry pulls instead of the configured pull-through mirror
- no private-registry story for first-party images or OCI artifacts
- no SQLite fast-test path for a new Laravel service and no documented blocker

---

# Operational And Observability Contract

This file owns the exact stable observability surfaces that must not drift across Ala services.

Use `21-alaa-platform-observability-directive.md` together with this file when the task includes telemetry architecture, OpenTelemetry Collector design, Prometheus metric catalogs, or cross-runtime observability guidance. If these two files appear to conflict, this file owns the exact header, event, code, and middleware invariants.

## Exact response headers

The target Ala response-header contract is:
- `X-Request-Id`
- `traceparent`

Rules:
- Do not make `X-Correlation-Id` part of the final contract.
- Do not make `X-Trace-Id` part of the final contract.
- If a service still emits, parses, forwards, tests, or documents `X-Correlation-Id`, migrate it to `X-Request-Id` plus `traceparent` and remove the stale code in the same effort.
- After applying this skill, no service code, config, docs, tests, or emitted response headers should still contain `X-Correlation-Id`.

## Exact `X-Request-Id` rules

Rules:
- Preserve a nonblank safe inbound `X-Request-Id`.
- Treat a value as safe only if it is one visible token, trimmed, and reasonably bounded in length.
- If absent or invalid, generate a new lowercase UUIDv7.
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
- `project_id` when available
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

Use these exact code expectations:
- `HTTP_REQUEST_COMPLETED` with `http.request.completed`
- `HTTP_REQUEST_FAILED` with `http.request.failed`
- `SERVICE_NOT_READY` with `service.readiness.failed`
- `SERVICE_READY` with `service.readiness.recovered` when used
- `AUTH_*` codes from `$alaa-trust-gateway-auth` with `auth.context.invalid`
- stable domain denial codes with `authz.denied`
- stable validation codes with `input.validation.failed`

Rules:
- Do not invent alternate names for the same event type.
- Keep `event` and `code` aligned.
- Keep user-facing messages separate from these machine-readable names.

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

Use `21-alaa-platform-observability-directive.md` for the exact metric families, histogram rules, collector ownership rules, and wider Prometheus contract.

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

---

# Alaa Platform Observability Directive

Use this file when the task includes telemetry architecture, OpenTelemetry exporter setup, OTLP endpoint ownership, queryable `trace_id`, Collector gateway design, SigNoz, Sentry, exception delivery, Prometheus scrape endpoints, metric catalogs, queue or dependency instrumentation, Vector pipelines, OpenFGA telemetry, or cross-runtime observability alignment between Go, Laravel, HAProxy, Vector, WA, OpenFGA, and future services.

## Contract posture

This directive extends `20-operational-and-observability-contract.md`.

Working rule:
- apply `20-operational-and-observability-contract.md` and this file together for observability work
- `20` owns the exact stable surfaces such as response headers, event names, machine-readable codes, and middleware invariants
- this file owns the larger telemetry design, OTLP path, Collector gateway rules, Prometheus contract, and validation expectations
- pair with `$alaa-observability-soc` for the signal decision model, SOC evidence, alert/runbook rules, Sentry role, and SigNoz/Sentry split
- pair with `$vector-rust-observability-pipelines` when Vector topology, VRL transforms, buffering, acknowledgements, or log-to-OTLP conversion are in scope
- pair with `$alaa-trust-gateway-auth` when trusted headers, request-time authorization, or gateway-derived identity affect telemetry
- pair with `$openfga` when the work changes OpenFGA model, tuple, permission, SDK, or test behavior rather than only observing OpenFGA as a runtime dependency

## Why this directive exists

The Ala platform needs one stable observability shape across services so operators can answer the same questions quickly everywhere:
- what happened
- where it happened
- why it failed or slowed down
- whether the root cause is local, upstream, downstream, or infrastructure-related
- which routes, jobs, queries, and code paths need attention

This directive exists to make that outcome repeatable across:
- Go services
- PHP and Laravel services
- gateway-adjacent components
- queue workers and background consumers
- entitlement control-plane components such as `entitlement-api` and `projector`
- future services such as `notification-core`, `realtime-hub`, and delivery workers
- in-development services such as `assessment` and `notification`

## How this fits the Ala platform

Treat the platform like this:
- public clients call the gateway
- the gateway authenticates requests, strips spoofed internal headers, injects trusted identity and project context, and routes the request
- when a route family needs request-time fine-grained authorization, the gateway calls `authz-sidecar` or `entitlement-spoa`
- backend services still own request normalization, business validation, business authorization, response shaping, and service-local observability
- `entitlement-api` owns normalized authorization business truth
- `projector` writes derived tuples
- OpenFGA stores the derived authorization graph used for fast request-time checks
- `content` is the new macroservice for `course`, `set`, and `content`
- `vod` still exists during migration but is on the deprecation path for learning-content ownership
- `notification` is in development and must converge on the same request correlation, exception, log, metric, and Collector rules before production readiness
- `assessment` is treated as a future Ala service in this contract until a local repository provides stricter source truth
- `wa` is a Vector and ClickHouse ingestion runtime, so apply the same trusted-header, request-id, SOC evidence, and operational visibility goals without forcing Laravel or Go middleware shapes onto it

Observability must respect those boundaries:
- gateway telemetry must explain trust-boundary behavior
- authz-runtime telemetry must explain route-time allow or deny behavior
- service telemetry must explain work done inside the service boundary
- entitlement control-plane telemetry must explain derived-state maintenance, not pretend to be the source of business truth
- WA telemetry must explain ingest acceptance, Vector parsing/routing, drop reasons, ClickHouse sink state, and stored raw analytics rows
- OpenFGA telemetry must be described as native runtime telemetry for the derived authorization graph, not as the business source of truth

## Current Ala service reality

Use this table as a starting point, then re-check the target repository before editing because repo truth wins.

| Service or repo | Current shape to preserve |
|-----------------|---------------------------|
| `auth` | Laravel token-issuer boundary. Uses `X-Request-Id`, `traceparent`, structured logs, OTLP traces/logs, and internal `/metrics`. Do not let observability work reshape token, refresh, session, profile, admin, or TOTP behavior. |
| `ticket` | Laravel service with Sentry present, OTel/Prometheus rollout, root internal `/metrics`, and exact `X-Request-Id` plus `traceparent` response contract. Sentry may remain for exception tracking but does not replace OTel/SigNoz/Prometheus. |
| `comment-service` | Laravel service with canonical `APP_NAME=comment`, OTel traces/logs, Prometheus `/metrics`, and docs that explicitly keep metrics scrape-based. |
| `content` | Laravel macroservice for course, set, and content. Uses manual OTel traces/logs, Prometheus `/metrics`, and outbox rows carrying `request_id` and `traceparent`; AMQP trace headers may require driver extension work. |
| `gateway` | HAProxy gateway. HAProxy owns request serving, trusted-header injection, trace context preservation/generation, and built-in Prometheus metrics at internal `:8404/metrics`. Vector owns optional log parsing, PII guard, buffering, and OTLP log export. Gateway does not currently emit app spans just because it propagates trace context. |
| `entitlement-platform` | Go services `entitlement-api`, `projector`, and `authz-sidecar` use OTel tracing and Prometheus metrics. OpenFGA uses native OTLP/gRPC and native Prometheus metrics. Logs are structured JSON; OTLP log export may be intentionally deferred per repo truth. |
| `wa` | Vector plus ClickHouse ingestion runtime. Canonical routes are `POST /ingest/v1/events` and `GET /health`; trusted headers include `X-Project-Id`, `X-Request-Id`, and optional `X-User-Id`. Apply Vector pipeline reliability and internal metrics rules instead of Laravel middleware rules. |
| `notification` | In-development Laravel service. It already uses `X-Request-Id`, `traceparent`, request observability middleware, and Sentry scaffolding. It must converge on the full OTel/Prometheus/SigNoz contract before production readiness. |
| `assessment` | Future or absent in this local workspace during this rewrite. Apply the generic Ala service contract until repo-local source truth exists. |

Rules:
- never flatten these runtime differences into one implementation template
- keep the outcome consistent even when implementation mechanisms differ
- do not invent a new observability route, header, event, metric family, or backend role for a repo when the platform contract already defines one

## Platform direction

Every long-lived Ala service must:
- produce standard telemetry with official OpenTelemetry and Prometheus libraries
- send traces and logs to an OTLP endpoint
- expose a Prometheus-compatible internal metrics endpoint for scraping
- stay vendor-neutral in application code
- capture exception evidence even when Sentry is not present
- make `trace_id` directly queryable anywhere operators query logs or OTLP log records

The platform direction is:
- application code produces correct telemetry
- Collector tiers receive, process, batch, retry, route, redact, transform, and fan out telemetry
- Prometheus scrapes service metrics from internal endpoints
- backends can change later by configuration without redesigning each service

The current Ala target architecture is:
- application services send OpenTelemetry traces, exception evidence, and structured logs to a gateway OpenTelemetry Collector endpoint
- application services expose Prometheus-compatible metrics endpoints; metrics are first-class and must not be skipped when tracing is added
- the gateway Collector exports to SigNoz or another approved backend through Collector configuration
- SigNoz tokens, endpoints, and exporter-specific headers belong in Collector or deployment secrets, not application code
- Sentry may be added for exception grouping, stack traces, releases, source maps, and developer workflow, but it is not required for exceptions to be observable
- when Sentry is absent, exception spans and structured exception logs must still reach SigNoz through the OTLP Collector path

### What goes where

Use this ownership table to avoid moving platform concerns into application code:

| Data type                           | App code        | OTel Collector          | SigNoz / metrics backend | Sentry |
|-------------------------------------|-----------------|-------------------------|---------------------------|--------|
| traces                              | yes             | receive/process/export  | yes                       | optional, not source of truth |
| exceptions                          | record on spans and logs | receive/process/export | yes, required when Sentry absent | optional specialized grouping |
| structured logs                     | yes             | collect/process/export  | yes                       | optional only if approved |
| Prometheus metrics                  | expose endpoint | scrape/forward optional | yes                       | no |
| retry/compression/fan-out/redaction | no by default   | yes                     | no                        | no |

Rules:
- keep telemetry endpoint configuration in env or deployment config
- do not hard-code backend-specific behavior in service code
- do not build custom multi-backend fan-out, retry queues, compression, or redaction pipelines inside application code unless the platform explicitly approves an exception
- do not replace the Prometheus scrape contract with ad hoc pushing for normal services
- do not use the Pushgateway for normal long-lived service metrics; only use it for explicit service-level batch-job cases when the lifecycle is intentionally decoupled from individual instances
- do not deliver "tracing only" observability; metrics, logs, traces, and exceptions are all part of done
- do not deliver "Sentry only" exception visibility; exceptions must also be visible through the platform OTel/SigNoz path when Sentry is absent or disabled

## OpenTelemetry SDK and OTLP rules

### Resource identity

Use standard OTel resource identity consistently:
- `service.name` must match the Ala service name
- `service.version` should come from the build or release version
- `deployment.environment.name` should come from the deployment environment
- add other resource attributes only when they are stable, useful, and policy-safe

Real resource identifiers belong in the right signal:
- use real identifiers in structured logs and trace attributes when they are needed for debugging and allowed by data-protection policy
- examples include `request_id`, `project_id`, `user_id`, `content_id`, `set_id`, `ticket_id`, or an upstream dependency request id
- real resource identifiers MUST NOT appear as Prometheus metric labels
- use bounded metric labels such as route pattern, operation, dependency, status class, code, queue, job name, and outcome
- `trace_id` is special: it is high-cardinality and must not be a normal metric label, but it must be directly queryable in structured logs and OTLP log records

### Trace queryability

`traceparent` is the propagation contract, not the only query field.

Rules:
- keep `traceparent` as the W3C context carrier across HTTP, RPC, queue, and worker boundaries
- derive `trace_id` from the canonical trace context once at the request or job boundary
- include `trace_id` as a first-class structured log field
- when exporting OTLP logs, populate native trace context fields when supported by the exporter or pipeline
- when building OTLP LogRecord payloads manually or through Vector, set native `traceId`, `spanId`, and trace flags from `traceparent`
- keep `traceparent` as an additional field only when useful for debugging propagation, parent/span id, or sampled flag behavior
- never require operators to parse `traceparent` during normal incident queries
- never add `trace_id` to Prometheus metric labels; use exemplars if the metrics stack supports trace linking

### Configuration rules

Keep OTLP configuration externalized. The common baseline is:
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_EXPORTER_OTLP_PROTOCOL`
- `OTEL_EXPORTER_OTLP_HEADERS`
- `OTEL_EXPORTER_OTLP_TIMEOUT`
- signal-specific overrides only when the platform actually needs different values for traces, metrics, or logs

Rules:
- keep a code-level configuration equivalent for any env-driven behavior
- do not require code edits to move from one backend or collector endpoint to another
- keep OTLP timeouts configurable, not hard-coded
- do not put secrets directly in source code
- default shared Docker Compose or Swarm service containers to the Collector DNS endpoint `http://otel-collector:4318`
- treat `host.docker.internal` as a local developer override only; do not commit it as the service default
- for Laravel or PHP long-lived workers, default to bounded scheduled flushing with `OTEL_SCHEDULED_FLUSH_ENABLED=true`
- keep `OTEL_FLUSH_ON_OPERATION=false` by default; enable it only for controlled full-fidelity verification that intentionally accepts operation-boundary export cost
- allow per-request structured logging to stay unsampled when the service contract requires it
- keep OTLP log and trace export batched, fail-open, circuit-breakered, and bounded so Collector problems do not degrade request latency
- express OTLP/exporter timeout defaults in milliseconds; use `OTEL_EXPORTER_OTLP_TIMEOUT=500`, `OTEL_BSP_EXPORT_TIMEOUT=500`, and `OTEL_BLRP_EXPORT_TIMEOUT=500` for high-traffic Laravel local runtime fallbacks unless production telemetry SLOs justify explicit different values

### Package guidance

Use explicit, vendor-neutral packages:

For Go:
- use official OpenTelemetry Go modules under `go.opentelemetry.io/otel` and `go.opentelemetry.io/contrib/...`
- use official OTLP exporters from the OpenTelemetry Go modules
- expose Prometheus metrics with the official Prometheus Go client `github.com/prometheus/client_golang/...`

For PHP and Laravel:
- the baseline Composer set for Ala PHP and Laravel services is `open-telemetry/api`, `open-telemetry/context`, `open-telemetry/sdk`, and `open-telemetry/exporter-otlp`
- application code and shared internal libraries should depend on classes and interfaces from `open-telemetry/api`; keep SDK, exporter, and provider wiring in bootstrap or infrastructure code
- treat `open-telemetry/context` as effectively baseline for real platform services because queues, workers, downstream HTTP calls, custom middleware, and manual boundaries need explicit context propagation when automatic propagation is not enough
- use the official Laravel auto-instrumentation package `open-telemetry/opentelemetry-auto-laravel` where auto-instrumentation is appropriate
- when using official PHP auto-instrumentation or zero-code instrumentation, install and enable the OpenTelemetry PHP extension, the SDK, and the needed instrumentation libraries; the extension by itself does not generate traces
- for a Laravel manual-instrumentation baseline, the expected Composer starting point is `composer require open-telemetry/api open-telemetry/context open-telemetry/sdk open-telemetry/exporter-otlp`
- for official Laravel auto-instrumentation, add `open-telemetry/opentelemetry-auto-laravel` and satisfy its `ext-opentelemetry` requirement instead of substituting an unrelated package
- because Ala platform observability includes structured logs, use the official `open-telemetry/opentelemetry-logger-monolog` package when sending Laravel Monolog records through the OpenTelemetry logging pipeline
- use only a platform-approved Prometheus-compatible metrics endpoint package for Laravel services
- do not treat third-party Laravel OpenTelemetry helpers as platform defaults; verify the exact package name, maintenance status, Octane behavior, and production readiness before approving one
- a helper such as `keepsuit/laravel-opentelemetry` may be approved as an optional app-level convenience layer for Laravel ergonomics, but it is not the canonical platform package contract
- do not cite `spatie/laravel-opentelemetry` as a canonical package name; as of 2026-04-21 verification, public package evidence points to `spatie/laravel-open-telemetry`, and that package must not be used as the platform default unless the platform explicitly re-approves it despite the maintenance and production-readiness warnings seen during verification

### Propagation rules

Preserve W3C context end-to-end:
- `traceparent`
- `tracestate`
- `baggage` when used

Apply this across:
- incoming HTTP
- outgoing HTTP
- gRPC or RPC calls
- message queues
- background jobs and consumers

Rules:
- preserve valid inbound `traceparent`
- do not fail the request only because an inbound `traceparent` is malformed
- continue the trace in consumers when context exists in message metadata
- when async context is absent, start a new trace and log the boundary clearly
- derive the logged `trace_id` from the canonical trace context
- export or map the same `trace_id` into OTLP logs so SigNoz log search can join with traces without parsing `traceparent`
- prefer OTel semantic conventions for HTTP, DB, messaging, and RPC rather than inventing local attribute names

## OpenTelemetry Collector gateway contract

### Baseline deployment pattern

The default platform pattern is a Collector gateway tier:
- applications or local agents send OTLP telemetry to a stable central endpoint
- one or more gateway collectors receive, process, and export telemetry
- the stable OTLP endpoint can exist per cluster, per region, or per environment
- the approved backend can be SigNoz, but applications must still target the Collector endpoint rather than a SigNoz-specific endpoint

In Kubernetes or OpenShift:
- use a Deployment for a gateway tier by default
- use a DaemonSet or other agent pattern only when host-level collection or a local hop is explicitly needed
- if the platform later adopts an agent-to-gateway design, keep agent configuration small and focused while gateways own heavier processing

For Ala teams that do not own cluster-wide infrastructure:
- target the stable platform-provided OTLP endpoint
- do not invent repo-local collector topologies unless a real blocker is documented

### Collector-owned responsibilities

The Collector tier owns:
- protocol termination for telemetry intake
- batching
- exporter retries
- sending queues
- durable buffering when required
- secure egress, authentication, and TLS
- attribute enrichment
- filtering and dropping
- redaction and masking
- transformation and normalization
- backend routing and fan-out
- SigNoz exporter configuration when SigNoz is the active backend
- centralized sampling policy
- Collector self-telemetry

The application tier does not own those concerns by default.

### Recommended processor placement

Rules:
- place `memory_limiter` first in the pipeline when used
- place `batch` after the work that changes or filters telemetry
- keep redaction, transform, and filter logic in the Collector when the goal is governance, cost control, or backend normalization
- keep tail sampling on gateway collectors only
- if probabilistic sampling is used across multiple collectors, keep the configuration consistent across them
- if tail sampling is used on multiple gateway instances, ensure trace-affinity routing so all spans for one trace reach the same sampling decision point

### Reliability rules

Collector reliability must be designed explicitly:
- use sending queues for exporters that cross a network
- tune queue size and retry windows according to expected data volume and acceptable downtime
- use persistent queue storage such as `file_storage` when losing queued telemetry on Collector restart is not acceptable
- monitor queue depth, queue capacity, and exporter failure metrics
- remember that WAL-style persistence improves resilience but is not a substitute for a dedicated message broker

### Security rules

Rules:
- store Collector secrets and credentials in a secret store, encrypted filesystem, or env expansion sourced from secret management
- use encryption and authentication on non-local network links
- minimize enabled components; do not enable receivers, exporters, or extensions that are not needed
- keep bind addresses private unless exposure is explicitly required
- do not expose OTLP receivers, debug endpoints, or health extensions on public interfaces by default
- treat 0.0.0.0 binds as an explicit choice to justify, not a casual default

### Collector observability

The Collector itself must be observable:
- collect internal Collector metrics
- expose internal metrics for scraping or forward them internally through OTLP according to the platform design
- keep a health endpoint or equivalent extension for operations
- use debug or local exporters only for controlled troubleshooting, not as a normal production sink

## Logging directive

All production service logs must be structured JSON.

Free-form text logs are not acceptable as the main production service log shape.

### Mandatory fields

At minimum, every operational log related to a request, job, readiness check, denial, or failure path must include:
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
- `project_id` when available
- `user_id` when available and allowed
- `http.method` when request-related
- `http.route` or a stable route name when request-related
- `http.status` when request-related
- `duration_ms` when the log measures work over time

Keep these field names stable.

Trace field rule:
- `trace_id` is mandatory for query speed.
- `traceparent` is the propagation carrier and may also be logged, but it is not a substitute for a separate `trace_id`.
- Vector and other log-pipeline agents must preserve or map `trace_id` into the backend query model.

### Recommended additional fields

Use them when relevant:
- `operation`
- `component`
- `dependency`
- `queue`
- `job_name`
- `attempt`
- `db.system`
- `db.operation`
- `db.statement_fingerprint`
- `error.kind`
- `error.message`
- `error.stack`
- `outcome`

### Data-protection rules

Rules:
- do not log passwords
- do not log secrets
- do not log raw bearer tokens
- do not log full JWTs
- do not log raw `X-Access`
- do not log full request bodies unless a very specific audited flow explicitly allows it
- do not log PII unless an approved operational reason exists and the data is masked, minimized, or reduced

If token-level correlation is needed, prefer:
- token `jti`
- a short fingerprint
- a stable internal code

### Probe-noise rule

Do not emit low-value completion logs for successful:
- `/api/health`
- `/api/ready`

Still log:
- readiness failures
- unexpected health failures
- readiness recovery transitions when tracked

## Error capture and exception handling rules

### Core rule

Handle errors cleanly:
- either return them upward with context
- or handle and log them at the correct boundary

Do not keep logging and returning the same error repeatedly through the same chain.

### What must be observable

At minimum, capture:
- unhandled exceptions
- request-level failures
- queue or job failures
- downstream dependency failures
- database failures
- authorization denials that matter operationally
- validation failures at the correct aggregation level
- business-critical failures even when the user-facing response stays graceful

Exception routing rules:
- if Sentry is installed and enabled, send exception events to Sentry for grouping, release regression, stack-trace workflow, and developer assignment
- regardless of Sentry, record exceptions on active OTel spans when a span exists
- regardless of Sentry, emit structured exception logs with `trace_id`, `request_id`, `service`, `event`, `code`, route or operation, exception type, safe message, and stack trace when policy allows
- if Sentry is absent, the OTLP logs/traces to Collector -> SigNoz path becomes the required exception visibility path
- do not hide handled-but-actionable exceptions only because no Sentry DSN exists

### Required captured context

Whenever possible, include:
- `request_id`
- `trace_id`
- `project_id`
- `user_id` when safe
- route or operation name
- stable machine-readable `code`
- dependency name when a downstream system is involved
- retry attempt when relevant
- job name when relevant

### Runtime-specific rules

For Go services:
- return errors with context
- log structurally
- do not swallow errors
- do not log and return the same error repeatedly
- record the error in the span when work fails
- set span status correctly

For Laravel or PHP services:
- establish request correlation early in middleware
- make the exception handler return `X-Request-Id` and `traceparent` on rendered API error responses
- keep observability state request-scoped
- stay Octane-safe
- for workers and scheduled commands, establish fresh per-job or per-command context and reset any request-like state between units of work

## Trace instrumentation rules

Every service must trace enough work to reveal slow routes, slow dependencies, and expensive internal operations.

At minimum, traces must cover:
- incoming HTTP request
- middleware or request pipeline
- trusted-context normalization
- service-local authorization and validation steps when those are important to diagnosis
- outgoing dependency calls
- significant database operations or query groups
- queue publish
- queue consume
- long-running internal operations
- final response generation

### Route and operation naming

Never use raw paths with live IDs as the primary route identity.

Use:
- a stable route name
- or a templated route pattern

Good example:
- `/api/v2/course/{course_id}/set/{set_id}/content/{content_id}`

Bad example:
- `/api/v2/course/8472/set/99/content/4431`

### Trace attribute rules

Rules:
- prefer OTel semantic conventions for HTTP, DB, messaging, and RPC
- use stable operation names and bounded attributes
- do not use raw SQL text, raw tokens, or raw PII as general span attributes
- use real resource identifiers as span attributes only when they materially help debugging and are policy-safe
- never copy those identifiers into Prometheus labels
- if query-level grouping is needed, use a safe fingerprint
- make retry paths, timeout paths, and cancellation paths visible

### Async boundaries

For messaging and jobs:
- propagate trace context in message headers or metadata
- continue traces in consumers when possible
- include queue name, job name, attempt, and outcome in the span attributes when those values are bounded and policy-safe
- make dead-letter, retry, and nack behavior visible in traces and logs

## Prometheus scrape contract

Every long-lived Ala service must expose a Prometheus-compatible metrics endpoint.

Rules:
- the endpoint is internal, scrapeable, and production-ready
- it is not a public client API
- default to `/metrics` unless a repository already has a different internal path owned by platform contract
- keep exposure behind internal service discovery, internal ingress, or network policy as appropriate
- do not depend on Pushgateway for normal service metrics
- prefer Prometheus pull collection for normal service endpoints

### Metric design rules

Rules:
- use bounded labels only
- use explicit base units
- use counters for totals
- use gauges for values that can go down
- use histograms for latency distributions
- avoid summaries for multi-replica request latency unless there is a very specific justified exception
- if the monitoring stack has explicitly enabled and validated native histograms end-to-end, they may be rolled out deliberately; otherwise keep classic histograms with explicit buckets
- do not use raw user IDs, project IDs, request IDs, raw URLs, query strings, SQL text, exception text, email addresses, or phone numbers as labels
- do not use real resource identifiers such as content ids, set ids, ticket ids, order ids, token ids, or dependency request ids as labels
- prefer service-discovery or target labels for metadata such as service and environment when the platform already injects them, instead of duplicating the same dimensions in every metric

### Allowed label examples

Use these when relevant and bounded:
- `service`
- `env`
- `http_method`
- `http_route`
- `http_status_code`
- `http_status_class`
- `operation`
- `dependency`
- `queue`
- `job_name`
- `db_system`
- `db_operation`
- `outcome`

### Forbidden label examples

Do not use:
- `user_id`
- `project_id`
- `request_id`
- real content, set, ticket, order, token, or dependency request ids
- raw URL
- query string
- email
- phone
- token
- exception text
- SQL text

### Exemplars

If the stack supports exemplars:
- use them on latency histograms where they add real debugging value
- attach trace identifiers as exemplar data, not as normal metric labels
- keep exemplar usage deliberate and bounded

## Mandatory baseline metric catalog

All application metrics must use stable names and must not invent random per-repo naming styles.

### HTTP request metrics

Every HTTP service must expose:
- `alaa_http_requests_total`
  - Counter. Total number of HTTP requests.
- `alaa_http_request_duration_seconds`
  - Histogram. End-to-end request duration.
- `alaa_http_requests_in_flight`
  - Gauge. Current in-flight requests.
- `alaa_http_request_failures_total`
  - Counter. Failed request count.

Recommended labels:
- `http_method`
- `http_route`
- `http_status_code` or `http_status_class`
- `service` and `env` only when those are not already injected elsewhere

### Readiness and health metrics

Every service must expose:
- `alaa_service_ready`
  - Gauge. `1` when ready, `0` when not ready.
- `alaa_service_readiness_failures_total`
  - Counter. Readiness failures.
- `alaa_service_restarts_total`
  - Counter when available from the app boundary or local runtime tracking.

### Authorization and validation metrics

Where relevant, expose:
- `alaa_auth_context_invalid_total`
- `alaa_authz_denied_total`
- `alaa_input_validation_failed_total`
- `alaa_rate_limit_exceeded_total`

Recommended labels:
- `http_route`
- `code`
- `outcome`

### Database metrics

Every service that owns database access must expose enough metrics to show DB pressure and slow queries.

Required baseline:
- `alaa_db_queries_total`
- `alaa_db_query_duration_seconds`
- `alaa_db_query_failures_total`
- `alaa_db_connections_active`
- `alaa_db_pool_in_use`
- `alaa_db_pool_idle`

When supported safely, also expose:
- `alaa_db_transactions_total`
- `alaa_db_transaction_duration_seconds`
- `alaa_db_lock_wait_seconds`
- `alaa_db_deadlocks_total`

Recommended labels:
- `db_system`
- `db_operation`
- `outcome`

Do not use raw SQL text as a label.
If query-level grouping is needed, use a safe fingerprint.

### Downstream dependency metrics

Every service that calls other services or external systems must expose:
- `alaa_dependency_requests_total`
- `alaa_dependency_request_duration_seconds`
- `alaa_dependency_request_failures_total`
- `alaa_dependency_timeouts_total`

Recommended labels:
- `dependency`
- `operation`
- `outcome`

### Queue and async metrics

Any service that publishes or consumes async jobs must expose:
- `alaa_queue_messages_published_total`
- `alaa_queue_messages_consumed_total`
- `alaa_queue_message_failures_total`
- `alaa_queue_message_duration_seconds`
- `alaa_queue_retries_total`
- `alaa_queue_dead_letter_total`

If backlog visibility is owned by the service or safely available, also expose:
- `alaa_queue_backlog`
- `alaa_queue_consumer_lag_seconds`

Recommended labels:
- `queue`
- `job_name`
- `outcome`

### Worker and runtime metrics

For long-lived workers and background consumers, expose runtime health metrics.

Common baseline:
- `alaa_worker_jobs_in_progress`
- `alaa_worker_restarts_total`
- `alaa_worker_memory_bytes`

For Go services, also preserve or expose where relevant:
- goroutine count
- garbage-collection cycles
- garbage-collection pause duration
- heap usage

For Laravel or Octane services, also preserve or expose where relevant:
- Octane worker count
- worker restart count
- queue worker failure count
- queue busy signals
- long job execution time

### Business metrics

Each service must expose a small set of service-owned business metrics beyond the shared baseline.

Examples:
- auth service
  - `alaa_auth_login_attempts_total`
  - `alaa_auth_login_failures_total`
  - `alaa_auth_token_issued_total`
  - `alaa_auth_token_validation_failed_total`
- content or vod service
  - `alaa_content_requests_total`
  - `alaa_content_access_denied_total`
  - `alaa_video_playback_authorizations_total`
- comment service
  - `alaa_comment_created_total`
  - `alaa_comment_deleted_total`
  - `alaa_comment_moderation_actions_total`
- ticket service
  - `alaa_ticket_created_total`
  - `alaa_ticket_reply_created_total`
  - `alaa_ticket_status_changed_total`
- wa service
  - `alaa_watch_events_ingested_total`
  - `alaa_watch_ingest_failures_total`
  - `alaa_watch_pipeline_backpressure_total`

Rules:
- keep business metrics owned by the service that actually owns the behavior
- keep labels bounded
- do not invent large per-feature metric trees without a real operational need

## Runtime-specific implementation notes

### Laravel and PHP

Rules:
- establish request correlation early on `/api/*` traffic
- keep request-scoped observability state request-scoped and Octane-safe
- attach `X-Request-Id` and `traceparent` to success responses and rendered API error responses
- normalize trusted gateway headers once and do not re-parse them in controllers or policies
- treat each queue job, consumer loop unit, or scheduled command as a fresh unit of work with fresh context
- keep the Prometheus endpoint internal and low-noise
- keep logs structured and avoid multiline free-form stack traces as the primary production format
- remember that Octane keeps the Laravel application in memory between requests, so never keep request, user, span, baggage, or trusted-header state in long-lived statics or singletons without an explicit reset path
- do not claim the OpenTelemetry PHP extension is universally required for every possible Octane implementation; require it for official PHP auto-instrumentation or for any chosen package that depends on extension hooks, and evaluate manual instrumentation separately

### Go

Rules:
- apply the same contract through top-level HTTP middleware, router middleware, and gRPC interceptors when those exist
- preserve and propagate `context.Context`
- use a structured logger
- expose a Prometheus metrics endpoint
- record failed operations in spans
- keep error handling clean and non-duplicative
- in long-lived consumers, restore context from message metadata when available and clearly mark retry or dead-letter behavior

## Collector and Prometheus deployment notes for Ala

For Ala environments:
- on Kubernetes or OpenShift, prefer one shared Collector gateway tier per environment or per cluster boundary rather than embedding custom collector topologies into every service repository
- when using the official Collector Helm chart, choose the deployment mode intentionally; gateway tiers usually use `deployment`, while host-level or node-level collection usually points to `daemonset`
- keep metrics endpoints internal and scrape them through platform discovery or explicit scrape configuration
- keep the same contract in Docker Compose and Docker Swarm: OTLP to the shared collector endpoint, Prometheus scraping internal service metrics, and no public metrics endpoint
- when SigNoz is the selected backend, put SigNoz exporter endpoints, access tokens, headers, and TLS options only in the Collector deployment configuration or secrets

## Sentry contract

Sentry is allowed but scoped.

Use Sentry for:
- exception grouping
- stack traces
- first-seen and regression workflow
- releases
- frontend source maps or debug IDs
- developer notifications and ownership
- profiling only when deliberately sampled

Rules:
- Sentry is not the main Ala observability backend.
- Do not send normal service metrics only to Sentry.
- Do not make Sentry traces the only distributed trace path when the service is part of the Ala OTel/SigNoz platform.
- Do not make Sentry the only exception path.
- If Sentry is absent or disabled, exception spans and structured exception logs must still reach SigNoz through OTLP and the Collector.
- Keep `SENTRY_SEND_DEFAULT_PII=false` unless there is an explicit approved data policy.
- Keep Sentry trace and profile sample rates `0` or low until overhead, cost, and duplication with SigNoz are reviewed.
- Put Sentry auth tokens for source-map or release uploads in CI/CD secrets, not source files.

## Service adoption checklist

When applying this skill to a service, finish by checking:
- `/api/health`
- `/api/ready`
- `X-Request-Id`
- `traceparent`
- queryable `trace_id`
- structured JSON logs
- exact event/code naming
- exception evidence through Sentry when present and through SigNoz/OTLP always
- Prometheus endpoint and applicable baseline metric families
- bounded labels
- OTLP exporter endpoint via env
- no vendor-specific backend coupling

## Minimum validation checklist

A service is not considered observability-complete unless all of the following are true:
- it emits structured JSON logs in production
- it returns `X-Request-Id` and `traceparent` on `/api/*` responses
- it preserves valid inbound correlation and generates valid values when missing
- it propagates W3C trace context across HTTP and async boundaries
- it makes `trace_id` directly queryable in structured logs and OTLP log records
- it sends traces and logs through the OTLP path without backend-specific code branches
- it exposes a Prometheus-compatible internal metrics endpoint
- it provides the shared HTTP, readiness, dependency, DB, and queue metrics that apply to it
- it uses bounded labels only
- real resource identifiers appear only in logs or trace attributes when needed, never as metric labels
- OTLP exporter endpoint and protocol are controlled by env or deployment config
- no vendor-specific backend coupling exists in application code
- it captures readiness failures, request failures, queue failures, dependency failures, and important denials with enough context for diagnosis
- it captures exception evidence in SigNoz through OTel spans/logs when Sentry is absent, and in both SigNoz and Sentry when Sentry is deliberately enabled
- it makes slow routes, slow queries, slow dependencies, repeated retries, and repeated denials easy to identify
- its collector path is observable enough to show queue pressure, export failures, or dropped telemetry when those happen

## Anti-patterns

- building custom telemetry fan-out inside application code
- treating telemetry as optional after feature work is done
- treating Sentry as the only exception pipeline
- forcing operators to parse `traceparent` because `trace_id` is missing from logs
- using raw IDs or unbounded text as metric labels
- exposing the metrics endpoint as a public client API
- using Pushgateway for normal long-lived service metrics
- logging raw JWTs, raw `X-Access`, or secret values
- using raw paths with IDs as the primary route dimension
- using summaries for multi-replica HTTP latency when histograms are the correct platform choice
- applying tail sampling in the wrong place or without trace-affinity routing
- hiding collector queue pressure or exporter failures
- duplicating the same error log at every layer
- inventing repo-local event names or metric families that break platform dashboards and alerts

---

# End-To-End Flow And Boundaries

Use this file when the task is about how the Ala platform fits together end-to-end, especially for onboarding an agent or a frontend developer to the shared system shape.

## High-level system view

The Ala platform is organized in layers with clear ownership:
- client applications send public traffic to the gateway
- the gateway is the external trust boundary
- the gateway verifies access tokens for protected routes, removes untrusted internal headers, injects trusted identity and project context, and forwards requests to the right backend
- when a route family needs fine-grained request-time authorization, the gateway calls `authz-sidecar` or `entitlement-spoa`
- backend services own their business domains and internal logic
- entitlement-platform keeps normalized authorization business truth in `entitlement-api`, projects derived tuples through `projector`, and serves request-time checks from OpenFGA

Rules:
- do not let services recreate browser-facing trust assumptions on internal hops
- keep route ownership clear so frontend, gateway, and backend work stay aligned
- prefer direct ownership boundaries over convenience coupling across service internals
- backend services may keep local user projections or immutable request snapshots, but `auth` remains the source of truth for current identity state

## Current services and responsibilities

### Existing services

- `auth`
  - canonical auth and profile source of truth for sign-in, tokens, sessions, profile truth, and trusted identity APIs
- `content`
  - new macroservice for `course`, `set`, and `content`
- `vod`
  - legacy learning and playback service during migration; on the deprecation path for learning-content ownership
- `comment`
  - discussion service for comments, replies, likes, moderation, and related activity
- `ticket`
  - support service for ticket creation, replies, assignment, status changes, and follow-up flows
- `wa`
  - watch and analytics ingestion service for event intake and related processing flows
- `entitlement-api`
  - normalized authorization business truth
- `projector`
  - derived tuple writer into OpenFGA
- OpenFGA
  - derived authorization graph for fast request-time checks

### Components being evaluated

These are not yet stable ownership surfaces, but they should follow the same platform contract where relevant:
- `notification-core`
- `realtime-hub`
- delivery workers
- queue or broker backbones such as RabbitMQ or Redis Streams

## Baseline platform flow

Treat the default Ala flow like this:
- public client or frontend -> gateway -> backend service
- gateway -> request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa` when the route family uses entitlement-platform authorization
- backend service -> backend service only for internal workloads that truly require a synchronous hop
- backend service -> async infrastructure for queue, event, or job delivery when appropriate
- normalized business change -> `entitlement-api` -> `projector` -> OpenFGA for derived fine-grained authorization state

## Simple user journey

In a normal user journey:
- a learner calls a gateway-facing route
- if the route is protected, the gateway verifies the token, strips spoofed internal headers, injects trusted context such as `X-User-Id` and `X-Project-Id`, and decides whether request-time authorization is also required
- sign-in and token refresh flows reach `auth`
- learning-page data should reach `content` in the long-term platform direction, while some migration traffic may still pass through `vod`
- discussion actions reach `comment`
- support actions reach `ticket`
- watch or telemetry ingestion reaches `wa`
- protected route families that use fine-grained authorization are checked first by `authz-sidecar` or `entitlement-spoa`, using the derived authorization state stored in OpenFGA

From the user point of view, this feels like one product. Inside the platform, each layer keeps a clear responsibility.

## How entitlement-platform fits into the Ala stack

- entitlement-platform does not own authentication; the gateway does
- entitlement-platform may own request-time fine-grained route authorization through `authz-sidecar` or `entitlement-spoa`
- entitlement-platform keeps normalized authorization business truth in `entitlement-api`
- `projector` writes derived tuples
- OpenFGA stores derived effective authorization state

For a normal backend behind gateway, the practical rule is:
- trust the gateway authentication result
- trust the gateway allow or deny result for the route
- normalize trusted identity context once near ingress
- still enforce business authorization, validation, and data-safety rules inside the backend

Do not make a normal backend behave like the gateway, the request-time checker, or the entitlement control plane unless the repository explicitly owns that role.

## Frontend and gateway orientation

Rules:
- frontend clients call documented gateway-facing routes, not service-local routes discovered from backend repos
- frontend clients must never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, `X-User-Mobile`, `X-User-Fname`, `X-User-Lname`, or `X-Location-*`
- trusted headers belong to the gateway-to-service contract, not the public client contract
- if a route is operational, frontend clients must not treat it as product behavior
- if a route previously depended on the retired profile blob, move that client integration to the public auth or profile APIs instead of reviving `X-Profile`
- for auth terms acceptance, frontend may show a non-removable terms notice or required checkbox before OTP request; successful OTP verification and login is the backend acceptance moment
- do not look for, call, or create a separate `accept-terms` API in the current auth flow unless the product/legal requirement explicitly changes to auditable terms-version persistence

Route-shape reminder:
- gateway-facing routes may include a service prefix such as `/auth`, `/content`, `/comment`, `/ticket`, `/vod`, `/wa`, or `/entitlement`
- the current default public gateway service-prefix map for frontend clients and framework-free SDKs is:
  - `auth` -> `/auth`
  - `content` -> `/content`
  - `comment` -> `/comment`
  - `tusd` -> `/tusd`
  - `wa` -> `/wa`
  - `entitlement` -> `/entitlement`
- `entitlement` is the `entitlement-api` admin/control-plane surface (a privileged admin/operator SDK such as `@alaa/sdk-entitlement`), not an anonymous end-user route family; the public prefix uses the short key `/entitlement`, never `/entitlement-api`, and the internal service name stays `entitlement-api`. As with every entry here, the gateway repo owns activation — verify the rendered HAProxy route table before relying on it.
- that first service prefix is a gateway routing prefix, not necessarily a backend route prefix and not necessarily the same concept as a child SDK `servicePrefix`, `apiPrefix`, or fixed ingest path
- clients and SDKs should compose the public gateway path exactly once through existing public configuration seams, such as service base URLs or child route-prefix options, without changing child SDK/service route definitions just to satisfy gateway routing
- trusted internal routes stay service-owned and are not public frontend discovery surfaces
- operational routes remain separate from product routes even when they share the `/api/*` prefix
- service-local routes may differ after gateway prefix stripping
- when `stripPathPrefix: true`, the gateway routes on the public prefixed path, strips only the configured gateway prefix, and forwards the remaining backend-visible service-local path
- do not collapse or de-duplicate repeated path segments at runtime; if a duplicate segment appears, decide whether it is intentional public-vs-child route composition or a bad config, then fix the config seam rather than rewriting paths ad hoc
- for client SDK and frontend package work, do not change child SDK source or backend routes to add a gateway prefix; prefer public config such as core `baseUrls`, child `servicePrefix`/`apiPrefix`, or service-specific path options
- if a child path is fixed, as with WA ingest, apply the gateway prefix through the service base URL
- for aggregate SDKs such as `@alaa/sdk`, default `createAlaaSdk(config)`-style factories to the canonical prefix map, but never rewrite service roots supplied through an injected core; the core owner must provide gateway-compatible roots
- for the current frontend SDK set, auth is special: preserve the auth child route prefix that already includes its service route family and point the auth core base at the gateway root; apply content, comment, tusd, and WA gateway prefixes through shared core `baseUrls`
- do not pass child route-prefix overrides solely for gateway routing, and do not trim, rewrite, or de-duplicate repeated path segments between the gateway prefix and child-defined route path
- before claiming a prefix is active in an environment, verify the gateway route table and rendered HAProxy config when available; in the current local convention this usually means checking `D:/Sohrab/Project/gateway/charts/gateway/values*.yaml`, `D:/Sohrab/Project/gateway/docker/values.shared-network.yaml`, and rendered `gateway.loadbalancer.yaml` or `gateway.ingress.yaml`
- use `$alaa-trust-gateway-auth` for exact trusted-ingress and prefix-strip behavior when the task depends on those details; use `$alaa-haproxy` when actual HAProxy routing, ACL order, or path rewriting is in scope

## Operational caller expectations

`GET /api/health` and `GET /api/ready` exist for:
- gateway and ingress probes
- orchestrators and rollout automation
- runtime validation scripts
- smoke checks
- automated tests

Rules:
- end-user clients should not depend on these routes for product behavior
- `/api/ready` is an operational contract and must not turn into a login helper, feature-flag probe, or frontend preflight endpoint
- the contract must not assume one specific operational caller

## Internal hop discipline

Rules:
- preserve `X-Request-Id` and `traceparent` across internal HTTP hops
- keep trusted header parsing and normalization close to the receiving edge
- keep operational routes separate from product-facing routes
- do not proxy another service's `/api/ready` unless that dependency is an explicit approved rollout requirement
- if a service depends on shared infrastructure such as Redis or RabbitMQ, check that infrastructure directly instead of proxying another app's status
- if a frontend or service needs domain behavior from another service, prefer that service's public API or events over direct table coupling
- downstream services may consume compact trusted name and location headers, but they must not fabricate display-name fields from compact ids unless another explicit source-of-truth contract owns that lookup
- backend services may keep local user projections or immutable request snapshots, but `auth` remains the source of truth for the latest identity state

## Repo-role reminders

### Frontend repository

- call gateway-facing public routes only
- never generate trusted internal headers
- never call `authz-sidecar`, `entitlement-spoa`, or OpenFGA directly

### Gateway repository

- own authentication, spoofing defense, trusted-header injection, and request-time authorization inputs
- keep request-time authorization fail-closed

### Backend service behind gateway

- consume normalized trusted context
- keep controllers and policies away from raw header parsing
- do not use allow-side `X-Authz-*` metadata as authorization input

### Entitlement-platform repository

- own fine-grained authorization contracts, request-time checker behavior, and tuple projection rules
- do not turn OpenFGA into business truth

## Why this file exists

This file gives one concise picture of:
- what the public client is allowed to do
- what the gateway owns
- what backend services own
- how `content` and legacy `vod` fit during migration
- where async boundaries belong

That helps agents keep frontend, gateway, and backend work consistent instead of treating each repository as an isolated system.

---

# Request-Time Authorization With OpenFGA

Use this section for fine-grained, per-resource authorization: a route that must answer "may *this* user act on *this* object?" before the backend runs. `End-To-End Flow And Boundaries` explains who owns what; this section explains how the request-time decision is made, what data crosses each hop, how to add a protected route, and how to debug one. Pair with `$alaa-trust-gateway-auth`, `$alaa-haproxy`, and `$openfga`.

## Why this layer exists

Authentication answers "who is this user?" (the compact JWT and trusted headers `X-User-Id`, `X-Project-Id`, `X-Access`). It does not answer "may this user open course 12, set 55, content 901?" That is a relationship between a user and a specific object, and it changes constantly. Encoding it in a token would make tokens huge and stale, so the platform keeps it in OpenFGA and asks at request time. The decision is fail-closed: a "no" or an unreachable decision means the backend is never called.

## The two paths and the single seam

OpenFGA is the seam between a write path and a read path. A bug is almost always "the tuple was never written" (write path) or "the route asked the wrong question" (read path).

- Write path (truth -> graph): `entitlement-api` owns business truth and emits a change event on every grant/deny change. `projector` consumes it and writes or deletes the matching tuples. `projector` is the only tuple writer.
- Read path (request -> decision): the gateway authenticates, builds a canonical object id, and asks `authz-sidecar` (or `entitlement-spoa`). The sidecar resolves the route to a final `can_*` permission and runs one OpenFGA `check`. The sidecar is read-only.

Grant vs permission: `projector` writes `grant_*`/`deny_*` relations; the OpenFGA model derives the final `can_*` permissions from them with inheritance and deny precedence; the sidecar always checks a `can_*` relation, never a raw grant. A "view" purchase on content 901 is stored as `grant_view`, and a later `can_view` check passes because the model resolves `can_view` from `grant_view` unless a deny overrides it.

## Read path, hop by hop

Worked example: `GET /vod/api/v3/course/12/set/55/content/901` for user `91`. The gateway repo `docs/authz-openfga-flow.md` has the full diagrams.

1. Gateway matches a route group. Protected routes are declared in `authzRouteGroups` (gateway `charts/gateway/values.yaml` and overlays), binding method + anchored public path regex to an `endpointCategory` and an `identityMode`. Two identity modes: `canonical_from_param` (VOD, ticket: the gateway builds the object id from a path param) and `comment_service_bundle` (comment: the gateway forwards a typed target ref and the sidecar normalizes).
2. Gateway builds the canonical object id (Lua, `haproxy/lua/authz-sidecar.lua`) in the fixed shape `<type>:p_<project_segment>__<tag>_<resource_segment>`. `project_segment` is the lowercase Crockford Base32 of the project UUIDv7 (26 chars). `resource_segment` is the Crockford Base32 of the integer id. `tag` is per type: `course`->`crs`, `set`->`set`, `content`->`cnt`, `assessment`->`asm`, `ticket_category`->`tcat`, `product`->`prd`. Content `901` -> `content:p_01hzy0f6m4p7n8q9r0s1t2v3wx__cnt_w5`.
3. Gateway -> `authz-sidecar`: a `HEAD /internal/authz/check` subrequest, carrying allowlisted trusted headers (`authzSidecar.requestHeaderAllowlist`). For `canonical_from_param` it sends `X-Authz-Endpoint-Category` and `X-Authz-Canonical-Object-Id` plus `X-Project-Id`, `X-User-Id`, `X-Request-Id`, `traceparent`, `X-Access`. For `comment_service_bundle` it sends `X-Authz-Service-Key` and the comment target/lineage/story refs instead. These `X-Authz-*` headers are stripped from client input at the edge.
4. `authz-sidecar` -> OpenFGA: after validating context (`X-Project-Id` is a UUIDv7, `X-User-Id` is a non-zero integer, category is known, object id matches the contract pattern), it resolves the final permission from `endpoint-permissions.yaml`, confirms the store and model pins, checks a short-TTL cache, and on a miss calls `POST {OPENFGA_API_URL}/stores/{OPENFGA_STORE_ID}/check` with body `{ "authorization_model_id": "<model id>", "tuple_key": { "user": "user:91", "relation": "can_view", "object": "content:p_01hzy0f6m4p7n8q9r0s1t2v3wx__cnt_w5" } }`. `user` is `user:` + the numeric `X-User-Id`. OpenFGA replies `{ "allowed": true|false }`; any non-`200` is a dependency failure. The runtime check sends no `context`; the optional `context` object (for conditional `not_expired` tuples) appears only in manual tooling examples.
5. Decision and enforcement. The sidecar maps the result to a status the gateway enforces fail-closed:
  - `204` `AUTHZ_ALLOWED` -> copy allow-only `X-Authz-*` metadata downstream and forward; event `http.request.completed`.
  - `403` `AUTHZ_DENIED` / `AUTHZ_TARGET_RULE_MISMATCH` -> gateway-owned `403`; event `authz.denied`.
  - `401` `AUTH_CONTEXT_MISSING` -> gateway-owned `401`; event `auth.context.invalid`.
  - `400` `AUTHZ_REQUEST_CONTEXT_INVALID` / `AUTHZ_ENDPOINT_CATEGORY_INVALID` / `AUTHZ_OBJECT_ID_INVALID` / `AUTHZ_NORMALIZATION_FAILED` -> gateway-owned `400`; event `input.validation.failed`.
  - `503` `AUTHZ_SERVICE_TIMEOUT` / `AUTHZ_SERVICE_UNAVAILABLE` / `AUTHZ_STORE_NOT_PINNED` / `AUTHZ_MODEL_NOT_PINNED` -> gateway-owned `503`; event `http.request.failed`.
  On allow the sidecar returns `X-Authz-Decision-Id`, `X-Authz-Decision-Code`, `X-Authz-Model-Id`, `X-Authz-Model-Label`, `X-Authz-Allow-Reason`, `X-Authz-Allow-Modifiers`, and a base64url `X-Authz-Decision-Artifact`. Allow-side `X-Authz-*` headers copied to the backend are observability only; a backend must never treat them as an authorization input and must still enforce its own business rules.

## Endpoint category -> permission mapping

Source: `entitlement-platform/platform/openfga/contracts/endpoint-permissions.yaml`. Runtime callers check `can_*` only.

| Endpoint category | Target type | Final permission |
|---|---|---|
| `course_page` | `course` | `can_preview` |
| `set_page` | `set` | `can_preview` |
| `watch_content` | `content` | `can_view` |
| `list_comments` | `course` / `set` | `can_preview` |
| `list_comments` | `content` | `can_view` |
| `post_comment` | `course` / `set` / `content` | `can_comment` |
| `open_ticket_category` | `ticket_category` | `can_use_ticket` |
| `take_assessment` | `assessment` | `can_take` |

## Store, model, and pinning

Three identifiers must agree across `projector` and `authz-sidecar`: `OPENFGA_STORE_ID` (the isolated namespace holding tuples and model versions, the `/stores/{store_id}/...` segment), `OPENFGA_AUTHORIZATION_MODEL_ID` (a specific immutable model version, pinned so a model edit never silently changes live decisions), and `OPENFGA_MODEL_LABEL` (default `authz_v1`, the human-readable label echoed in logs and `X-Authz-Model-Label`). Upload a new model id before writing new tuple shapes, and roll back the label and model id together.

## Adding a new request-time-authorized route

This spans two repositories; prepare the contract before exposing the route, or it fails closed for everyone.

In `entitlement-platform`:
1. Confirm the OpenFGA model has the target type and the final `can_*` relation; if new, add them, upload the model, and re-pin `OPENFGA_AUTHORIZATION_MODEL_ID` (bump `OPENFGA_MODEL_LABEL`) for both `projector` and `authz-sidecar`.
2. Add the `endpoint_category` + `target_type` -> `final_permission` rule to `endpoint-permissions.yaml`; the category name must match what the gateway sends.
3. Ensure `projector` writes the grant/deny tuples for that scope type and `entitlement-api` emits the events; without tuples every `can_*` check returns `allowed: false`.

In `gateway`:
4. Add the `authzRouteGroups` entry to `charts/gateway/values.yaml` and every active overlay: `name`, `enabled: true`, `enforcer: sidecar`, `method`, an anchored `publicPathRegex` capturing the resource id, `endpointCategory` (matching step 2), and `identityMode`.
5. For `canonical_from_param`, extend the Lua extractor `extract_public_path_context` in `haproxy/lua/authz-sidecar.lua` with a branch for the new route-group name that pulls the resource id from the path. The `captures` field in values is documentation; the Lua extractor is what reads the id. Forgetting this branch is the most common reason a new canonical route fails with `AUTHZ_REQUEST_CONTEXT_INVALID`.
6. If the target type is new, add its tag to `RESOURCE_TAGS` in the same Lua file (for example `assessment = "asm"`).
7. Confirm the headers the sidecar needs are in `authzSidecar.requestHeaderAllowlist`.
8. Render the chart, run the gateway authz smoke harness, and verify the store/model pins match across `projector` and `authz-sidecar`. A `comment_service_bundle` route skips steps 5-6 but must be a supported normalization target in the contract.

## Debugging an authz decision

Every hop shares `X-Request-Id` and `traceparent`. Work the path in order.
1. Read the gateway access log: check `endpoint_category`, `canonical_object_id`, `sidecar_status`, `sidecar_decision_code`.
2. `400 AUTHZ_OBJECT_ID_INVALID` / `AUTHZ_REQUEST_CONTEXT_INVALID`: the gateway built a bad or empty object id; suspect a missing Lua extractor branch, a wrong `publicPathRegex`, or a missing resource tag.
3. `400 AUTHZ_ENDPOINT_CATEGORY_INVALID`: the gateway's `endpointCategory` is not in `endpoint-permissions.yaml`; the repos disagree on the name.
4. `403 AUTHZ_TARGET_RULE_MISMATCH`: the category exists but has no rule for that target type; add the target rule.
5. `403 AUTHZ_DENIED`: the contract resolved a `can_*` but OpenFGA said no. A write-path question: reproduce the `check`, then `read` the tuples for that user and object. If the expected `grant_*` tuple is missing, look at `projector` (did the event arrive and validate?) and `entitlement-api` (was the grant created?).
6. `401 AUTH_CONTEXT_MISSING`: identity did not reach the sidecar; the upstream JWT/trusted-header step is the suspect.
7. `503 AUTHZ_*`: dependency or pin failure (`STORE_NOT_PINNED`/`MODEL_NOT_PINNED` are config; `SERVICE_TIMEOUT`/`SERVICE_UNAVAILABLE` are reachability). Fail-closed by design.
8. Allowed but the backend still rejects: that is backend business authorization, not this layer.
Confirm the sidecar's `authz decision` log line and that its `authorization_model_id` matches the model that actually holds your tuples; a stale pin makes "the tuple exists but the check denies."

## Anti-patterns

- Calling OpenFGA, `authz-sidecar`, or `entitlement-spoa` directly from a frontend or normal backend.
- Checking a `grant_*`/`deny_*` relation at request time instead of a `can_*`.
- Adding a gateway route group before the permission rule and tuples exist.
- Adding a `canonical_from_param` route group without the Lua extractor branch.
- Treating allow-side `X-Authz-*` headers as authorization input in a backend.
- Letting `projector` and `authz-sidecar` drift onto different model ids.

## Source of truth

- Gateway read path, full diagrams and worked example: gateway repo `docs/authz-openfga-flow.md`.
- Write path and reconciliation: gateway repo `docs/entitlement-projector.md`.
- Route groups and Lua: gateway `charts/gateway/values.yaml`, `charts/gateway/templates/configmap.yaml`, `haproxy/lua/authz-sidecar.lua`.
- Model, object-id encoding, conditions, endpoint mapping: `entitlement-platform` `platform/openfga/contracts/authorization-contract.yaml` and `endpoint-permissions.yaml`.
- Runnable OpenFGA `check`/`read`/`write`: `entitlement-platform` Postman collection.

---

# Notification Service Contract (Cross-Service)

Cross-service contract for how every Ala service talks to the `notification` service. Source of truth:
the `notification` repo owns `docs/async-contracts.md` (command ingress) and `docs/list_of_channels.md`
(channels); this section mirrors them and adds the `entitlement-platform` audience-resolution handshake.
When this section and the notification repo disagree, the notification repo wins. Status: the command
ingress is implemented; per-producer onboarding and the audience-to-command bridge are `reserved`.

Platform architecture context: the canonical high-level architecture (shared
`docs/high-level-Alaa-system-artitecture.md`, symlinked into each repo) describes the broader
notification system as still-being-evaluated components — a **Notification Core** business service, a
**Realtime Hub** for online SSE/WebSocket fan-out, **Delivery Workers** for web/SMS/(future) push, and
an internal **Queue/Broker** (Redis Streams or RabbitMQ). This section documents the *currently
implemented* cross-service ingress (`notification.commands` over RabbitMQ); the larger component split
and internal delivery backbone are an evaluated target, not finalized.

Platform shape: most Ala services are Laravel; only the `entitlement-platform` Go services are Go.
Laravel-first conventions (snake_case JSON everywhere), because PHP `json_decode` is case-sensitive.

## Notification roles

- Producer service: publishes RabbitMQ commands to notification instead of business HTTP.
- Notification service: consumes commands and performs delivery/storage/user-projection work with
  receipt-based deduplication.
- Audience-resolution authority: for access-derived audiences, `entitlement-platform` expands an object
  audience into explicit recipients; it owns the `notif.*` audience queues.

## Canonical command ingress (authoritative)

- Exchange `notification.commands` (`direct`); DLX `notification.commands.dlx`; ingress connection
  `rabbitmq_ingress`; receipts in `rabbitmq_command_receipts`.
- Queues / routing keys (DLQ key is `<rk>.failed`):
  `notification.command.sms.send_message.v1` (`sms.send_message.v1`),
  `notification.command.sms.send_pattern.v1` (`sms.send_pattern.v1`),
  `notification.command.notification.store.v1` (`notification.store.v1`),
  `notification.command.user_projection.upsert.v1` (`user_projection.upsert.v1`).
- Producers publish to `notification.commands` with the matching routing key; broker publish ack is the
  synchronous success boundary.

## Canonical command envelope (snake_case everywhere, including nested objects)

Required: `message_id` (UUIDv7), `message_type` (canonical family; alias `family`), `message_version`
(positive int; inferred from `.vN`), `occurred_at` (RFC3339; defaults to now), `producer_service`
(stable `services.name`; aliases `service_name`/`service_id`), `idempotency_key` (alias `dedupe_key`),
`payload` (plain JSON object, never a serialized Laravel job). Recommended: `correlation_id` (defaults
to `message_id`). Optional: `causation_id`. Idempotency dedupe is by `message_id` and
`(message_type, idempotency_key)`. The command envelope is NOT project-scoped; targeting is by explicit
recipients in the payload.

Command families: `sms.send_message.v1` `{ message, users:[{id,mobile}], provider_public_id? }`;
`sms.send_pattern.v1` `{ pattern_code, user:{id,mobile}, pattern_values:[{key,value}],
provider_public_id? }`; `notification.store.v1` `{ owner_id, message_public_id }`;
`user_projection.upsert.v1` `{ user_id, first_name, last_name, mobile, national_code }`.

## Recipient model (current) vs channel addressing (reserved)

Current/implemented: explicit recipients in the payload (`users[]`/`user`). Channel/audience addressing
is a notification-owned concept in `notification/docs/list_of_channels.md` and is NOT part of the
implemented command contract today. Mirror of the current inventory (do not emit channels absent from
that source): auth — `p:<project_id>:user#<user_id>`, `p:<project_id>:ostan#<ostan_id>`,
`p:<project_id>:shahrestan#<shahrestan_id>`, `p:<project_id>:bakhsh#<bakhsh_id>`,
`p:<project_id>:shahr#<shahr_id>`, `p:<project_id>:shobe#<shobe_id>`; content —
`p:<project_id>:course#<course_id>`, `p:<project_id>:set#<set_id>`, `p:<project_id>:content#<content_id>`.
Status: reserved/planning — update this section and the notification channel doc together when
implemented.

## Audience-resolution handshake (entitlement-platform `notif.*` queues)

Separate from the command ingress. Entitlement-owned queues that turn an access-derived object audience
into explicit recipients, using an entitlement-owned envelope (`schema_version`, `command_id`,
`project_id`), not the notification command envelope:

- `notif.retrieve_users` (entitlement `expansion-worker` consumes): `schema_version`, `command_id`,
  `project_id`, `notification_id`?, `target_type`, `object_type` (`course`|`set`|`content`),
  `content_id`?/`set_id`?/`course_id`?, `need_mobile`, `requested_at`.
- `notif.expand_users` (entitlement publishes): `schema_version`, `command_id`, `project_id`,
  `notification_id`?, `principal_type`, `principal_key`, `need_mobile`, `reason` (`{ type, ref }`).
- `notif.recipient_chunks` (entitlement publishes): `schema_version`, `command_id`, `project_id`,
  `notification_id`?, `chunk_no`, `users[]` of `{ user_id, mobile?, reason { type, ref },
  source_grant_revision_id }`.

Nested `reason` is `{ type, ref }` (lowercase). Reserved gap: bridging recipient chunks into
`notification.command.sms.*` commands is not built. These messages are an interim, not-yet-converged
shape and do not carry correlation (`request_id`/`trace_id`) or `producer` attribution; those must be
added before any production consumer is wired. The contract-complete envelope is `notification.commands`
(which carries `correlation_id`). See entitlement-platform `docs/api/internal-api.md`.

## Per-service notification matrix

| Service | Runtime | Direction | Contract | Status |
| --- | --- | --- | --- | --- |
| `entitlement-platform` | Go | audience resolution | entitlement-owned `notif.*` queues | entitlement side implemented; bridge to `notification.commands` reserved |
| `auth` | Laravel | producer | `notification.commands` (e.g. `sms.send_pattern`) | reserved |
| `content` | Laravel | producer | `notification.commands` | reserved |
| `comment` | Laravel | producer | `notification.commands` | reserved |
| `ticket` | Laravel | producer | `notification.commands` | reserved |
| `assessment` | Laravel | producer | `notification.commands` | reserved |
| `wa` | Laravel | future delivery channel | — | reserved |
| watchtime | Laravel | producer | `notification.commands` | reserved |

Any service owning users should also publish `user_projection.upsert.v1`.

## Notification language-specific rules

- Laravel producers: publish the canonical envelope with snake_case keys; `payload` is plain JSON,
  never a serialized Laravel job; consumers read with case-sensitive `json_decode`. Pair with
  `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq`.
- Go producers (the two `entitlement-platform` Go services): explicit snake_case `json:"..."` tags on
  all message structs including nested value objects. Pair with `$alaa-golang`.

## Notification anti-patterns

- Capitalized/Go-default JSON keys in any notification or `notif.*` message.
- Inventing queues/exchanges or a bespoke envelope instead of `notification.commands` plus the
  canonical envelope.
- Sending serialized Laravel jobs across repositories.
- Using RabbitMQ as a synchronous query/RPC layer for notification reads.
- Starting new internal business HTTP integrations with notification.
- Omitting `message_id` or `idempotency_key`; leaking/logging recipient PII beyond need.

---

# Trusted Ingress And Laravel Contract

## Service modes

### Mode B - Laravel backend service
Apply the Laravel response and middleware rules in this file.

### Mode C - Laravel downstream trusted service
Apply the full trusted-ingress contract in this file when the service consumes sanitized Ala gateway headers.

### Mode D - Laravel auth-boundary service
A Laravel service that owns the trust boundary may satisfy the trusted-ingress semantics with request guards or `Auth::viaRequest(...)` instead of a literal class named `ResolveUserMiddleware`, but its outward behavior must still match this contract.

## Trusted header names

Use these exact header names unless a temporary migration is explicitly documented:
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

## How trusted ingress relates to entitlement-platform

- the gateway owns authentication and trusted header injection
- a request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa` may already have enforced the route-level fine-grained decision
- the backend still owns normalized request handling and business authorization inside the service

Rules:
- trust the gateway allow or deny result for the route
- do not use allow-side `X-Authz-*` metadata as a credential
- do not bypass the shared platform contract with ad hoc direct OpenFGA checks from a normal downstream backend
- keep service-local policies and Gates focused on business rules after trusted context normalization

## `ResolveUserMiddleware` contract

Responsibility:
- parse trusted headers once
- validate them once
- build one normalized actor context
- synchronize request-time user access across request helpers, facades, and legacy guards still in use

Required validation behavior:
- validate `X-Project-Id` as UUIDv7
- validate `X-User-Id` as a positive integer
- decode `X-Access` as the base64url permission bitmap
- map `X-Access` only through the service's generated, committed catalog-owned permission config
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

## Canonical `project_id` boundary

Use this rule for every Ala Laravel service that accepts a client-visible project selector named `project_id`.

Public request rule:
- `project_id` in public request bodies, query parameters, and DTOs is a canonical UUIDv7 string
- the service resolves that UUIDv7 to its internal project key only after validation passes
- positive integer project ids are not accepted from public clients
- services may persist internal numeric project ids when that is their storage model
- public Resources and event or API payloads should expose the public UUIDv7 boundary when a mapped row exists

Trusted context rule:
- `X-Project-Id` is injected by the gateway from the verified token `pid` claim
- downstream services normalize trusted `X-Project-Id` once inside their trusted request context builder
- direct backend-only tests may keep numeric compatibility only when the service explicitly documents that local testing mode
- controllers, policies, Resources, repositories, jobs, and observers must not independently parse raw project identifiers

Preferred Laravel naming:
- `App\Support\Auth\TrustedProjectContext` for shared project-boundary helpers
- `App\Rules\MappedProjectUuidV7` for public UUIDv7 validation plus registry lookup
- `resolveInternalProjectId(mixed $value): ?int` to map a public UUIDv7 or documented trusted compatibility value to storage id
- `resolvePublicProjectId(?int $internalProjectId): ?string` to map storage id back to public UUIDv7
- `resolveBoundaryProjectId(mixed $value): int|string|null` only for trusted or serialization boundaries where existing internal compatibility is explicitly allowed

Implementation order:
1. validate the raw public input as string UUIDv7
2. confirm it maps to an approved project row or registry entry
3. store the resolved internal id in request attributes or a typed DTO
4. pass the internal id into services, queries, policies, events, and cache keys
5. expose the public UUIDv7 again at public response or token boundaries

Do not use a trait or request normalizer that converts public `project_id` to an integer before validation. That leaks the storage model into the public contract and allows internal ids such as `1` to become accepted API input.

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

---

# Auth TOTP And Step-Up Contract

Use this file when the task touches auth TOTP management, optional MFA setup, forced route-level TOTP enforcement, SDK/client handling of TOTP errors, QR setup UX, or `require_totp:<purpose>` rollout.

## Source priority

For the current auth implementation, trust these sources in order:

1. `D:\Sohrab\Project\auth\routes\api.php`
2. `D:\Sohrab\Project\auth\bootstrap\app.php`
3. `D:\Sohrab\Project\auth\app\Http\Controllers\Api\V3\TotpController.php`
4. `D:\Sohrab\Project\auth\docs\contracts\auth\endpoints\totp.md`
5. `D:\Sohrab\Project\auth\docs\contracts\auth\flows\totp-enrollment.md`
6. `D:\Sohrab\Project\auth\docs\contracts\auth\flows\totp-step-up.md`
7. `D:\Sohrab\Project\auth\docs\ops\totp-step-up-mechanism.md`

If implementation and docs disagree, trust route/controller/middleware source first, report contract drift, and align docs plus API artifacts before closing the task.

## Feature flag and availability

- TOTP management is feature-flagged by `AUTH_TOTP_ENABLED` through `auth.totp.enabled`.
- When disabled, `/api/v3/totp*` should answer as unavailable, commonly HTTP 404 with `{ "message": "TOTP feature is disabled." }`.
- Clients should normalize this as `totp_unavailable` and hide or disable TOTP setup UI. Do not treat it as an ordinary missing route.
- When enabled, self-service setup routes should be usable by authenticated users without forcing every user to enroll.
- In image-first or cached-config runtimes, changing `AUTH_TOTP_ENABLED` requires refreshing config and recreating affected app/worker containers as appropriate.

## Public versus internal route shape

- Browser, mobile, and SDK clients call the gateway public prefix, normally `/auth/api/v3/totp*`, with `Authorization: Bearer <access token>`.
- Public clients must never send trusted internal headers such as `X-User-Id`, `X-Project-Id`, `X-Access`, `X-User-Role`, or gateway-forged profile headers.
- Backend-local `/api/v3/totp*` examples are only for direct service tests, trusted gateway tests, and internal documentation.
- Preserve normal auth, role, permission, tenant/project, and business authorization checks. TOTP is a step-up proof, not a replacement for authorization.

## Optional enrollment lifecycle

1. Client calls `GET /auth/api/v3/totp` to read status.
2. If `enabled=false`, client may show setup UI.
3. Client calls `POST /auth/api/v3/totp/enroll` with an empty body.
4. Backend responds with `secret`, `otpauth_uri`, `recovery_codes`, and `status.enabled=false`.
5. Backend does not return a QR image. The client generates a QR code from `otpauth_uri` and also shows the manual `secret` fallback.
6. User scans the QR code in an authenticator app such as Google Authenticator, Microsoft Authenticator, 1Password, or Bitwarden.
7. User enters the 6-digit code from the authenticator app.
8. Client calls `POST /auth/api/v3/totp/confirm` with `{ "code": "123456" }`.
9. TOTP is enabled only after confirm succeeds.
10. Client shows recovery codes once and never logs, persists, or sends them to analytics.

Never log or persist TOTP `secret`, `otpauth_uri`, user-entered TOTP codes, or recovery codes outside the intended secure storage and one-time display path.

## Forced route-level TOTP

To force TOTP on a sensitive route, keep the route behind the normal authenticated gateway/trusted flow and add `require_totp:<purpose>`.

Example Laravel route shape:

```php
Route::middleware('auth:trusted_gateway')->group(function (): void {
    Route::delete('sessions', [SessionController::class, 'destroyAll'])
        ->middleware('require_totp:auth.sessions.revoke_all');
});
```

Purpose rules:

- Use stable, action-specific purpose names, such as `auth.sessions.revoke_all`, `profile.write`, `profile.photo`, or `catalog.school.write`.
- The purpose scopes the short-lived proof, not the authenticator enrollment. One authenticator-app entry serves all purposes.
- A successful step-up for one purpose must not unlock a different purpose.
- Do not use generic names such as `default`, `admin`, `write`, or route paths that may change.
- Do not silently attach forced TOTP. Update route docs, OpenAPI, Postman, SDK/client notes, tests, and rollout notes.

## Site-level credential and purpose-scoped proof

- The platform uses one site-level TOTP enrollment per user. The authenticator entry created during setup is not tied to
  one downstream route or service.
- The `purpose` is attached to each short-lived proof, not to the stored authenticator secret. Use purpose-specific
  proof when the same user must re-authenticate for a sensitive action.
- A future separate setup domain may introduce a different enrollment purpose only if the repository contract explicitly
  documents that new credential boundary. Do not create a new authenticator setup for ordinary force-TOTP routes.

## Signed proof-token target

The target cross-service flow is signed proof-token based:

1. The client calls the protected route normally.
2. The gateway or backend returns a TOTP challenge with the required `purpose`.
3. The client calls `POST /auth/api/v3/totp/step-up` with that `purpose` and a fresh TOTP code or recovery code.
4. Auth verifies the code against the user's enabled site-level TOTP credential and returns:

```json
{
  "purpose": "content.bulk_delete",
  "verified_until": "2026-07-04T12:05:00Z",
  "proof_token": "<opaque signed proof token>"
}
```

The proof token must bind at least user, project or tenant context where applicable, purpose, proof id, issued time,
expiry, and issuer. The token must be opaque to public clients. Public docs and examples must use placeholders only.

## Client proof cache

The client may cache the returned `proof_token` in its auth-state storage, similar to an access token, until
`verified_until`.

Rules:

- Cache by user/session, project or tenant context where applicable, and purpose.
- Do not cache, log, persist, serialize, or replay the submitted TOTP code.
- Do not create a refresh token for TOTP proof. When the proof expires or the gateway rejects it, prompt for a new TOTP
  code and obtain a fresh proof through `POST /auth/api/v3/totp/step-up`.
- Clear cached proofs on logout, account switch, project switch, TOTP disable/reset, token/session revocation,
  permission context changes, explicit step-up failure, or proof expiry.

## Gateway and downstream service contract

Public clients retry force-TOTP routes with only:

```http
X-TOTP-Proof: <opaque signed proof token>
```

Gateway responsibilities:

- Strip any inbound trusted backend `X-TOTP-*` headers from public requests.
- Verify `X-TOTP-Proof` signature, issuer, expiry, user/session binding, project binding where applicable, and purpose.
- Forward only gateway-verified backend metadata to the downstream service:
  - `X-TOTP-PURPOSE`
  - `X-TOTP-VERIFIED-UNTIL`
  - `X-TOTP-PROOF-ID`

Downstream service responsibilities:

- Never validate raw TOTP codes.
- Never trust public `X-TOTP-*` metadata.
- Enforce only route/business purpose policy against gateway-verified proof metadata after normal authentication,
  authorization, tenant, and business checks remain in place.

## Client challenge handling

Clients and SDKs should model forced TOTP as a challenge-and-retry flow:

- On `TOTP_STEP_UP_REQUIRED`, preserve the original request intent, show a TOTP challenge, call `POST /auth/api/v3/totp/step-up` with the same purpose plus `code` or `recovery_code`, cache the returned `proof_token` until `verified_until`, then retry the original request with public `X-TOTP-Proof`.
- On `TOTP_REQUIRED`, guide the user through status, enroll, confirm, and then step-up or retry the original action if it still requires proof.
- On `TOTP_UNAVAILABLE`, show a controlled unavailable state and report rollout/config drift to operators.
- On `TOTP_STEP_UP_FAILED` or `TOTP_DISABLE_FAILED`, keep the challenge open and do not update local enabled state.
- On `TOTP_RATE_LIMITED`, stop retries until the returned retry window expires.
- On `AUTH_LIMITER_UNAVAILABLE`, fail closed with a temporary unavailable state.

## SDK and frontend contract

A public SDK should expose explicit operations for:

- `getTotpStatus`
- `enrollTotp`
- `confirmTotp`
- `regenerateTotpRecoveryCodes`
- `disableTotp`
- `verifyTotpStepUp`

SDK/frontend expectations:

- Keep the auth base URL and gateway prefix configurable.
- Generate the QR code client-side from `otpauth_uri`; do not expect a server-generated image unless implementation changes and the public contract is updated.
- Invalidate cached TOTP status and pending challenge state after TOTP mutations.
- Return the step-up `proof_token` to host code but do not store it inside the SDK unless the host explicitly delegates a
  storage adapter with the cache and clear rules above.
- Do not cache mutation responses that contain secrets or recovery codes.
- Ensure SSR builds do not render browser-only QR libraries on the server without a client-only guard.
- Never include trusted gateway headers in public SDK examples.

## Review checklist

Flag the change when any of these appear:

- A public client sends trusted internal headers.
- Docs or SDK claim the backend returns a QR image while the implementation only returns `otpauth_uri`.
- Docs say TOTP is disabled while `AUTH_TOTP_ENABLED=true`, or docs imply forced route TOTP exists without route evidence.
- A forced-TOTP route lacks challenge-and-retry client guidance.
- A public client sends raw TOTP code to a downstream service instead of auth.
- A public client sends trusted backend `X-TOTP-*` metadata instead of public `X-TOTP-Proof`.
- A service accepts force-TOTP metadata without gateway stripping/verification ownership being documented.
- TOTP proof is refreshed without a new TOTP code.
- TOTP is used instead of role/permission/business authorization.
- Purpose names are unstable, generic, user-controlled, or route-path-derived.
- OpenAPI, Postman, endpoint docs, flow docs, tests, or SDK contracts are not aligned with route behavior.

---

# Permission Catalog And Service Configs

Use this file when an Ala service changes `config/permissions.php`, permission names, bitmap ids, generated permission artifacts, permission drift checks, or `X-Access` decoding behavior.

## Ownership

- `alaa-permission-catalog` is the normative cross-service source of truth for permission names, service ownership, generated permission snapshots, and bitmap ids.
- Auth is the only runtime issuer of JWT authorization claims: `prm`, `prv`, and `av`.
- Backend services are generated-config consumers. Their committed `config/permissions.php` files or generated Go
  service permission maps should come from the catalog output for that service.
- Gateway, `authz-sidecar`, entitlement-platform, and OpenFGA are route or resource authorization infrastructure. They do not own service-local permission-name-to-bitmap-id maps.

## Service Config Rules

- Do not invent, manually renumber, or hand-maintain bitmap ids in `config/permissions.php` or generated Go service
  permission maps.
- Generate service-local permission configs from `alaa-permission-catalog`, review the generated output, then commit the generated file in the target service during an explicit apply phase.
- Use CI drift checks to detect mismatch between the catalog and committed service configs.
- Treat drift as evidence. Do not let normal import or generate commands silently copy generated configs into source repositories.
- Source service CI may run catalog drift checks with temporary generated output, but it must not modify source files, stage files, or reinterpret report-only warnings as failures.

## Apply Phase Rules

- Permission config changes must happen through explicit apply phases, one service at a time.
- Each apply phase must name the service, the generated input path, the destination path, and the focused validation set before copying files.
- Keep unrelated repos untouched. Applying content config must not also apply comment, auth, WA, gateway, JWT semantics, or bitmap encoding changes unless the phase explicitly says so.
- After apply, run service-local tests that prove:
  - `X-Access` decodes against the committed generated config or Go permission map
  - trusted context resolution still rejects missing, malformed, or zero-known-permission bitmaps
  - service authorization behavior still matches local policies, Gates, or middleware
- Run catalog `check-drift` before and after permission-related work when the repo has access to `alaa-permission-catalog`.

## Extraction And Reuse Rules

- Bitmap ids are never reused.
- Removed permissions must become `deprecated` or `reserved`; do not delete published ids from the catalog.
- Service extraction must not reuse old bitmap ids across new service boundaries.
- Legacy VOD ids remain stable for VOD compatibility.
- Extracted `content_*` permissions receive new catalog-owned ids, currently `64-78`, and are not runtime aliases for VOD permissions.

## Current Canonical Outcomes

- Current generated catalog status is `clean` with `104` permissions. Fatal and error drift findings are `0`; current warnings are report-only unless a later policy promotes a scoped warning.
- `wa_get_watch_stats` owns bitmap id `1`; WA service-local config adoption is deferred until WA has a committed permission-consumer shape.
- `comment_get_index` owns bitmap id `18`.
- `comment_get_show` owns bitmap id `40`.
- Extracted content-service permissions own bitmap ids `64-78`.
- ControlledOps content bulk permissions own bitmap ids `79-91`.
- tusd upload-intake permissions own bitmap ids `92-95`: `upload_to_content_service`,
  `upload_to_ticket_service`, `upload_to_auth_service`, and `upload_to_comment_service`.
- entitlement-api admin coarse permissions own bitmap ids `96-104`; the generated Go map is compiled into the service
  and remains separate from object-level OpenFGA `can_*` relations.

## Current Permission Snapshot

Use this compact grouping instead of copying the full catalog into prompts:

| Range | Owner | Permissions |
| --- | --- | --- |
| `1` | `wa` | `wa_get_watch_stats` |
| `2-13` | `vod` | analytics and study-cell permissions |
| `14-17` | `ticket` | `crm_get_tickets`, `crm_post_ticket_reply`, `crm_put_ticket`, `crm_post_bulk_ticket` |
| `18-21`, `40` | `comment` | `comment_get_index`, `comment_approve`, `comment_delete`, `comment_reply`, `comment_get_show` |
| `22-39` | `vod` | legacy content, content-set, product, copy, and discount permissions |
| `41-63` | `auth` | profile, sessions, TOTP, admin authz override, and admin catalog permissions |
| `64-78` | `content` | extracted set, content, and course permissions |
| `79-91` | `content` | ControlledOps content bulk permissions |
| `92-95` | `tusd` | upload-intake permissions for content, ticket, auth, and comment handoff |
| `96-104` | `entitlement` | entitlement-api grant, explain, expansion, reconciliation, and projection admin permissions |

## Companion Skill Boundary

- Use `$alaa-trust-gateway-auth` for JWT claim semantics, `prm` to `X-Access` projection, bitmap packing, trusted-header spoofing defense, and gateway/auth ownership.
- Use this file for service-local generated config or Go map adoption, CI drift checks, and one-service-at-a-time
  apply discipline.

---

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
12. Align permission configs with `alaa-permission-catalog` generated outputs when the task touches `config/permissions.php`, permission names, bitmap ids, `X-Access`, or drift checks.
13. Align the Alaa Platform Observability Directive when the task touches logs, traces, metrics, queues, DBs, dependencies, or workers.
14. Add or align exact response envelopes, exact headers, exact event names, exact code naming, and exact metric names where the contract owns them.
15. Update docs, Postman, and runbooks in the same patch when public or operational behavior changes.
16. Run focused tests for every changed contract surface.
17. Report blockers explicitly when exact convergence is not possible.

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

### Trusted ingress
- missing blank invalid `X-Project-Id`
- missing invalid `X-User-Id`
- missing invalid zero-known-permission `X-Access`
- `X-Access` decoding against the generated, committed service permission config
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
- `config/permissions.php` invents or hand-renumbers bitmap ids instead of consuming `alaa-permission-catalog` generated output
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

## Anti-patterns

- treating the skill as optional guidance instead of a hard contract
- copying only part of the `/api/ready` contract and changing the rest locally
- leaving `X-Correlation-Id` anywhere in the service after migrating to `X-Request-Id`
- inventing local event names that conflict with `$alaa-observability-soc`
- inventing local auth error names that conflict with `$alaa-trust-gateway-auth`
- keeping stale compatibility branches, helpers, tests, or docs for removed contract surfaces
- reintroducing duplicated GitLab CI logic into service repositories instead of updating `service-ci-kit` first
- scattering trusted-user normalization across controllers, policies, resources, and observers
- accepting storage ids such as `project_id: 1` from public clients instead of UUIDv7 project ids
- using one normalizer for both public `project_id` and trusted `X-Project-Id` when the public path must be stricter
- leaving helper responsibilities implicit so each agent re-invents them
- reviving the retired profile-blob trust surface instead of consuming the compact header projection
- pushing observability logic into app code that belongs in the Collector layer
- treating Sentry as the main observability backend instead of a focused exception, release, and developer-debugging layer

---

# Laravel Copy Baselines

Use these baselines when a Laravel repository needs copy-oriented implementation help.

Rules:
- Adapt namespaces and injected helpers to the target repository.
- Preserve the owned behavior and field names.
- Do not change headers, event names, code names, envelope shapes, or metric names while copying.

## Public project selector baseline

Use this baseline whenever a Laravel service accepts public `project_id` input. Keep the names aligned unless the target repository already has an equivalent helper with the same semantics.

### `MappedProjectUuidV7` validation rule

```php
<?php

declare(strict_types=1);

namespace App\Rules;

use App\Support\Auth\TrustedProjectContext;
use Closure;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Translation\PotentiallyTranslatedString;

final class MappedProjectUuidV7 implements ValidationRule
{
    private const string CANONICAL_UUIDV7_PATTERN = '/^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/';

    /**
     * @param Closure(string, ?string=): PotentiallyTranslatedString $fail
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! is_string($value) || preg_match(self::CANONICAL_UUIDV7_PATTERN, $value) !== 1) {
            $fail('The :attribute must be a canonical UUIDv7 project id.');

            return;
        }

        if (TrustedProjectContext::resolveInternalProjectId($value) === null) {
            $fail('The selected :attribute is invalid.');
        }
    }
}
```

### Public FormRequest usage

```php
use App\Rules\MappedProjectUuidV7;
use App\Support\Auth\TrustedProjectContext;

public function rules(): array
{
    return [
        'project_id' => ['bail', 'required', 'string', new MappedProjectUuidV7],
    ];
}

protected function passedValidation(): void
{
    $projectId = TrustedProjectContext::resolveInternalProjectId(
        (string) $this->validated('project_id')
    );

    if ($projectId !== null) {
        $this->attributes->set('project_id', $projectId);
        $this->attributes->set('project_public_id', TrustedProjectContext::resolvePublicProjectId($projectId));
    }
}
```

### Controller or action usage

```php
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

private function resolveProjectId(Request $request): int
{
    $projectId = $request->attributes->get('project_id');

    if ((is_int($projectId) || is_string($projectId)) && (int) $projectId > 0) {
        return (int) $projectId;
    }

    throw ValidationException::withMessages([
        'project_id' => ['The selected project id is invalid.'],
    ]);
}
```

Usage rules:
- public FormRequests use `MappedProjectUuidV7`
- trusted-header middleware may use a separate trusted normalizer when compatibility requires it
- never convert public `project_id` to an integer in `prepareForValidation()`
- put the resolved internal id in request attributes or a typed DTO, not back into public input
- add tests that reject integer `1`, string `"1"`, malformed UUIDs, and unmapped UUIDv7 values
- keep Postman examples on a public UUIDv7 variable such as `authProjectId`, separate from trusted-header variables such as `gatewayProjectId`

## RequestObservabilityMiddleware baseline

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use App\Support\Observability\MetricsEmitter;
use App\Support\Observability\ProbeNoiseDecider;
use App\Support\Observability\RequestContext;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Symfony\Component\HttpFoundation\Response;

final class RequestObservabilityMiddleware
{
    public function __construct(
        private readonly RequestContext $requestContext,
        private readonly ProbeNoiseDecider $probeNoiseDecider,
        private readonly MetricsEmitter $metricsEmitter,
    ) {
    }

    public function handle(Request $request, Closure $next): Response
    {
        $context = $this->requestContext->start($request);

        Log::shareContext($context->toLogContext());

        try {
            /** @var Response $response */
            $response = $next($request);
        } catch (\Throwable $throwable) {
            $this->requestContext->shareExceptionContext($request, $context, $throwable);
            $this->requestContext->logRequestFailure($request, $context, $throwable);

            throw $throwable;
        }

        $this->requestContext->attachHeaders($response, $context);
        $this->requestContext->recordMetrics($request, $response, $context, $this->metricsEmitter);

        if (! $this->probeNoiseDecider->shouldSuppressCompletedLog($request, $response)) {
            $this->requestContext->logRequestCompleted($request, $response, $context);
        }

        return $response;
    }
}
```

Required helper responsibilities behind this baseline:
- normalize or generate `X-Request-Id`
- normalize or generate `traceparent`
- expose `trace_id`
- capture request duration
- resolve route name or templated route
- attach `X-Request-Id` and `traceparent`
- persist request correlation context so the exception handler can attach the same headers to rendered API error responses
- emit `http.request.completed` and `http.request.failed`
- enforce bounded metric labels

## MetricsEmitter baseline expectations

The request middleware metrics emitter should align to the shared metric contract.

Minimum request-middleware metrics:
- `alaa_http_requests_total`
- `alaa_http_request_duration_seconds`
- `alaa_http_requests_in_flight`
- `alaa_http_request_failures_total`

Rules:
- use route templates or stable route names, not raw paths
- do not label by `user_id`, `project_id`, request IDs, raw URLs, or exception text
- use histograms for request duration
- if the stack supports exemplars, attach trace identifiers as exemplar data rather than normal labels

## Exception-handler reminder

Do not assume the middleware can attach headers after a rethrow.

When the request pipeline throws and Laravel renders the API error later, the exception handler must read the shared request context and attach the same `X-Request-Id` and `traceparent` headers before returning the response.

## ResolveUserMiddleware baseline

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use App\Support\Auth\AuthStateSynchronizer;
use App\Support\Auth\TrustedActorContext;
use App\Support\Auth\TrustedRequestContext;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class ResolveUserMiddleware
{
    public function __construct(
        private readonly TrustedRequestContext $trustedRequestContext,
        private readonly AuthStateSynchronizer $authStateSynchronizer,
    ) {
    }

    public function handle(Request $request, Closure $next): Response
    {
        $actor = $this->trustedRequestContext->fromHeaders($request);

        $request->attributes->set(TrustedActorContext::class, $actor);
        $this->authStateSynchronizer->synchronize($request, $actor);

        return $next($request);
    }
}
```

Required helper responsibilities behind this baseline:
- validate trusted headers exactly according to `$alaa-trust-gateway-auth`
- decode and map the permission bitmap
- normalize compact trusted first and last names
- normalize compact trusted location ids into one repository-owned structure when needed
- normalize `X-Access-Token-Id` when the repository uses token-session context
- expose one trusted actor object
- synchronize `$request->user()` and `Auth::user()`
- support legacy guard synchronization when the repository still needs it

## Trusted actor DTO baseline

```php
<?php

declare(strict_types=1);

namespace App\Support\Auth;

final readonly class TrustedActorContext
{
    /**
     * @param list<string> $permissions
     * @param array{
     *     ostan?: int,
     *     shahrestan?: int,
     *     bakhsh?: int,
     *     shahr?: int,
     *     shobe?: int,
     *     school?: int
     * }|null $location
     */
    public function __construct(
        public string $projectId,
        public int $userId,
        public array $permissions,
        public ?string $mobile,
        public ?string $firstName,
        public ?string $lastName,
        public ?array $location,
        public ?string $tokenId,
        public ?string $role,
        public string $requestId,
        public string $traceId,
    ) {
    }
}
```

## Snapshot baseline

- if a repo stores request-time user context, keep mutable projections separate from immutable snapshots
- prefer a repository-owned projection that preserves compact ids instead of inventing display names
- keep missing location ids explicit instead of fabricating location names

## Route and response reminder

When copying middleware baselines into a Laravel repository, also enforce:
- `GET /api/health`
- `GET /api/ready`
- `php artisan ops:ready --json`
- top-level `data` envelope for successful `/api/*` responses
- `X-Request-Id` and `traceparent` response headers
- the metric families defined by `21-alaa-platform-observability-directive.md` when the service owns an HTTP metrics boundary

---

# Frontend SDK Consumption Contract

Use this file when frontend or host-app code consumes the `@alaa/*` SDK packages: choosing which package to import,
deciding what the app is responsible for versus what the SDK owns, wiring auth/token/refresh, attaching correlation
headers, or reviewing a change that touches the browser-to-gateway boundary from the client side.

This file is the client-side companion to `25-end-to-end-flow-and-boundaries.md` (platform flow and gateway
orientation). That file says what the public client is allowed to do against the gateway; this file says how the
frontend SDK layer is allowed to deliver it. Read both when the task spans client and gateway.

It exists because the most common frontend mistake is not a wrong API call — it is the app reaching past the SDK's
public surface to re-own a concern the SDK already owns (trust headers, refresh, errors). That duplicates logic and
leaks layering. The rules below keep responsibility where it belongs.

## SDK package topology (one mental model)

The `@alaa/*` SDK is layered, and each layer has one job:

- `@alaa/sdk-core` — framework-free infrastructure: HTTP transport, cache, the trusted-header deny-list, branded
  errors, and the event primitives. It is composed *by* the SDK packages; it is not an app-facing package.
- domain SDKs (`@alaa/sdk-auth`, `@alaa/sdk-content`, `@alaa/sdk-comment`, `@alaa/sdk-tusd`, `@alaa/sdk-wa`) — one
  service domain each, built on core. They own service routes, request shaping, and service-local security rules.
- `@alaa/sdk` — the aggregate / mother package. The composition root that assembles core plus the domain SDKs into one
  instance with one shared core, one cache, one event bus, and one lifecycle. This is the app's factory entry.
- `@alaa/sdk-vue` — the Vue adapter. Composables (`useAlaaSdk`) and Vue-shaped glue over the aggregate. This is the
  app's entry inside Vue components/composables.

## The single consumption rule

- Frontend/host code imports the SDK **only** through `@alaa/sdk` (factory + types) and `@alaa/sdk-vue` (Vue
  composables). Nothing else.
- Do **not** import `@alaa/sdk-core` or a domain SDK (`@alaa/sdk-auth`, etc.) directly from app/host code. Core is
  infrastructure the aggregate composes; importing it from the app skips the curated public surface and couples the app
  to an internal package (a dependency-inversion violation).
- If the app needs something that only lives on core or a domain SDK, the fix is to **expose it on the `@alaa/sdk`
  aggregate's public exports**, then import it from `@alaa/sdk` — not to reach into core from the app. Treat widening
  the aggregate surface as the sanctioned path, and pair it with `$alaa-mono-package`.
- The aggregate's public surface today includes `createAlaaSdk`, `createAlaaSdkFromCore`, `isAlaaSdkError`, the gateway
  prefix/service-name defaults, the version matrix, and the public types. Consume those; do not re-derive them.

## Responsibility ownership (who owns what)

The app must not re-implement anything the SDK or gateway already owns. Default ownership:

- **Trusted-header rejection** → SDK, at two layers, fail-closed. The domain SDK rejects caller-supplied forbidden
  headers when it builds the request (`@alaa/sdk-auth`'s `rejectForbiddenCallerHeaders`), and `@alaa/sdk-core`'s
  transport re-asserts the deny-list on the *final* outbound headers right before the fetch
  (`assertNoTrustedCallerHeaders`, which permits only the SDK's own `Authorization`). The app never re-checks or
  duplicates either layer. The one thing the SDK cannot police is code that runs *inside* a host-injected custom fetch
  after that final assert (the documented "custom-fetch bypass"); the gateway is the authoritative enforcement there, so
  a host-injected fetch must only ever add public-safe correlation headers (`X-Request-Id` / `traceparent`).
- **Token attach + refresh** → SDK. The opaque bearer token is attached by the SDK; refresh is SDK-owned and
  single-flight. The app never re-implements refresh, never queues its own refresh, and never decodes the token.
- **Branded errors + events** → SDK. The app classifies failures with `isAlaaSdkError` and subscribes to the SDK event
  bus; it does not parse raw responses or invent its own error taxonomy from response bodies.
- **Route/prefix composition** → SDK + config seams (see `25-end-to-end-flow-and-boundaries.md`). The app supplies
  gateway base URLs / public config; it does not rewrite child route paths to satisfy gateway routing.
- **Data shaping + UI policy** → app. Redirects, profile-completion gates, which surface renders, and host wiring are
  the app's job — not the SDK's.

## Trust boundary (client side)

- From the browser the app sends only: `Authorization: Bearer <opaque-token>`, `X-Request-Id`, and `traceparent`.
- The app never sends trusted internal gateway headers — `X-Project-Id`, `X-User-Id`, `X-Access`, `X-Profile`,
  `X-User-*`, `X-Location-*`, `X-Gateway-Auth`, `x-access-token-id`, `x-user-scopes`, and the `x-token-*` / `x-authz-*`
  families. Those belong to the gateway-to-service contract, not the public client.
- The access token is opaque to the client. Do not decode it, branch on its claims, or persist it. Never write a bearer
  token into a non-HttpOnly cookie, into SSR HTML, or into serialized SSR store state.
- `project_id` is a public UUIDv7. Send it only in the request **body** where the contract requires it (for example the
  OTP request), sourced from app config/env (such as `PROJECT_ID`). Never send it as a trusted header from the client.

## SSR and lifecycle rules

- On the server, create one SDK/core per request. Do not hold a module-level SDK singleton that carries per-user state
  across requests.
- In the browser, one SDK/core per app session is fine, but recreate it (or clear scoped cache) on logout or actor
  change, so one user's cached data cannot serve another.
- Refresh relies on the HttpOnly refresh cookie (`credentials: 'include'` on refresh/logout/session calls). The app
  never reads that cookie.

## Observability and correlation (align with the platform directive)

- The app attaches `X-Request-Id` and a synthesized W3C `traceparent` (`00-<32hex>-<16hex>-01`) — one trace id per SSR
  request and per browser navigation — purely as request headers. See `20-operational-and-observability-contract.md`
  for the exact header rules and `21-alaa-platform-observability-directive.md` for the telemetry architecture.
- Client auth/event telemetry is allow-list only: emit low-cardinality fields (event, step, surface, code, request_id,
  trace_id) and never PII, OTP codes, tokens, profile values, or TOTP secrets. Pair with `$alaa-observability-soc` for
  the redaction contract and `$alaa-signoz-clickhouse-docs` for how those fields are queried downstream.

## Documentation requirement

- Every exported function, composable, factory, and public type the app adds around the SDK carries doc comments
  (TSDoc for `.ts`, JSDoc otherwise) with typed params/returns. No undocumented public surface. Pair with
  `$alaa-frontend-doc-annotations`.

## Anti-patterns (do not do these)

- **Reaching into core to re-own an SDK concern.** Importing `@alaa/sdk-core` (or a domain SDK) into the app to add a
  redundant guard — for example re-checking the forbidden trusted-header deny-list in the app's own `fetch` wrapper.
  The SDK transport already rejects forbidden caller headers fail-closed, and the app wrapper only ever *adds*
  `X-Request-Id` / `traceparent`, so the second check guards a hypothetical while leaking the layering. Correct: trust
  the SDK boundary; if you genuinely need the helper, expose it on `@alaa/sdk` first.
- Re-implementing token refresh, a refresh queue, or token persistence in the app.
- Decoding the access token or branching on its claims in client code.
- Sending any trusted gateway header from the browser, or putting `project_id` in a header.
- Importing a sibling SDK package's `src/*` instead of its public `dist`/entry export.
- Parsing raw error bodies instead of using `isAlaaSdkError` + the SDK error taxonomy.

## Apply checklist

- App SDK imports come only from `@alaa/sdk` and `@alaa/sdk-vue`.
- No app import of `@alaa/sdk-core` or a domain SDK; no app re-implementation of trust/refresh/error ownership.
- Outbound client headers are limited to `Authorization: Bearer`, `X-Request-Id`, `traceparent`.
- No token in cookie/SSR HTML/SSR state; token treated as opaque; `project_id` only in body, from config.
- One SDK/core per SSR request; browser SDK reset on logout/actor change.
- Client telemetry is redacted/allow-listed; public surface is documented.

## Companion routing

- `$alaa-trust-gateway-auth` — exact trusted-header, token, and gateway-boundary semantics.
- `$alaa-security-review` — mandatory for any change to tokens, refresh, headers, or the client trust boundary.
- `$alaa-frontend-developer` — the three-layer client architecture (presentation → flow composable → store → SDK) and
  SSR auth/session patterns.
- `$alaa-mono-package` — when a needed helper must be promoted onto the `@alaa/sdk` public surface, or when SDK package
  boundaries/exports change.
- `$alaa-observability-soc` and `$alaa-signoz-clickhouse-docs` — redaction contract and downstream querying.
- `$alaa-frontend-doc-annotations` — documentation pass for the public surface the app adds.

For SDK package internals (not app consumption), read the package's own `packages/<name>/developer_guide.md` and
`packages/developer_guide.md`; do not encode package internals here.

---

# Frontend Page Kit And Widgets Contract

Use this file when building or consuming Page Kit, UI Kit, app-shell, or any widget in the clean-island package
families: defining a new widget or page package, wiring a widget into a host, deciding what a widget may own, or
reviewing a change that touches `@alaa/page-*`, `@alaa/widgets-*`, `@alaa/forms`, `@alaa/crud`, `@alaa/model`,
`@alaa/sanitize-html`, or `@alaa/app-shell`.

This file owns the *consumption and boundary* contract for the widget/page layer. It is the visual-layer companion to
`60-frontend-sdk-consumption-contract.md` (which owns how the host talks to backend services). Read both when a widget
needs data: the widget never fetches it, the host fetches it through the SDK and passes it in.

It exists to keep widgets reusable and safe. A widget that reaches for the store, the SDK, the token, or a trusted
header stops being a widget and becomes a hidden piece of the host — untestable, unportable, and a trust-boundary risk.

## Package families (one mental model)

- **Page Kit** (`@alaa/page-*`, `@alaa/widgets-*`) — the page-builder and widget system: schema, renderer, and the
  widget catalog.
- **UI Kit** (`@alaa/forms`, `@alaa/crud`) — the clean-island form and CRUD building blocks.
- **app-shell** (`@alaa/app-shell`) — the per-layout application shell.
- **support** (`@alaa/model`, `@alaa/sanitize-html`, and similar) — focused single-responsibility packages that widgets
  depend on instead of duplicating heavy logic.

These are isolated package lanes. They are not wired into the production app until a maintainer explicitly approves that
migration phase (see "Island isolation" below).

## Abstraction-first / contract-first

- Define the public contract first — the props in, the events out, and the public types — then build the implementation
  behind it. The contract is the deliverable; the internals are replaceable.
- A package/widget exposes a stable, minimal public surface and hides its internals. Consumers depend only on the public
  `dist`/entry exports, never on internal `src/*`.
- Cross-cutting or dependency-heavy logic becomes a focused single-responsibility package (the "extract, don't
  duplicate" rule), not a grab-bag `utils`. Pair with `$alaa-mono-package`.

## The three-layer rule

Data flows in exactly one direction, through three layers:

- **presentation** (widget / component) → **flow composable** → **store** → **SDK**

Rules:

- Widgets are **props-in / events-out**. They receive data through props and report intent through events. They render;
  they do not fetch.
- Widgets own **no host singletons** — no store, no SDK instance, no auth token, no trusted-header generator, no router.
  The host owns data and wiring; the widget owns presentation.
- The flow composable orchestrates; the store holds state; the SDK talks to services (under
  `60-frontend-sdk-consumption-contract.md`). A widget never calls the SDK, APIGateway, or a service route directly.

## Widget contract

- Inputs are explicit, typed props with documented shapes; outputs are explicit, typed events. No implicit globals.
- A widget is deterministic for a given set of props (important for SSR — see below).
- A widget does not read or write browser storage, tokens, or cookies. If it needs identity-derived data, the host
  passes it in as a prop.
- Keep widgets small and focused; prefer composing several small widgets over one large component.

## Consumption boundary (package hygiene)

- Consume sibling packages through their public `dist`/entry exports and `link:../<package-name>` dependencies. Never
  import a sibling's `src/*`.
- Keep `vue` and `quasar` as peer dependencies; do not bundle a second copy.
- Preserve the asset contract: package CSS/assets must reach `dist/ssr/client/assets` through the bundling graph
  (import CSS from the package entry). Pair with `$alaa-mono-package` for boundary, dedupe, and asset rules.

## Island isolation and migration gating

- Do not wire these packages into legacy production `src/*`, `src-ssr/*`, `src-pwa/*`, Quasar boot, the router,
  Vuex/Pinia, the service worker, root scripts, or legacy packages unless the task explicitly approves that migration.
- Host consumption goes through the sanctioned clean-island host lane (`src/new/` behind a `/new/` prefix), feature by
  feature, with explicit per-phase approval. The lane is additive and reversible.

## Security in widgets

- A widget never sends trusted gateway headers and never holds a token — those concerns live in the host + SDK
  (`60-frontend-sdk-consumption-contract.md`). A widget that needs them is mis-scoped.
- Raw/untrusted HTML renders only through the sanctioned sanitizer (`@alaa/sanitize-html` / DOMPurify) at the trust
  boundary. A single bypass of that one raw-HTML path is stored XSS — never hand-roll a regex sanitizer. Pair with
  `$alaa-security-review` for any raw-HTML or dangerouslySet-style path.

## SSR safety

- No browser-only APIs (`window`, `document`, `localStorage`, observers) during SSR render; guard with `onMounted` or a
  `typeof window` check.
- Deterministic render: no `Date.now()`, `Math.random()`, or locale/time-dependent output in the SSR path (it causes
  hydration mismatches).
- Clean up observers, listeners, timers, and abort controllers in `onBeforeUnmount`.

## Documentation requirement

- Every public prop, emit, component, composable, and exported type carries doc comments (TSDoc for `.ts`, JSDoc
  otherwise) with typed params/returns. The public contract is the documented surface. Pair with
  `$alaa-frontend-doc-annotations`.

## Anti-patterns (do not do these)

- A widget that imports the store, the SDK, the router, or a token directly.
- A widget that fetches its own data or calls a service route instead of receiving data via props.
- Importing a sibling package's `src/*` instead of its public `dist`/entry.
- Bundling `vue`/`quasar` into a package, or shipping assets outside the bundling graph so they miss
  `dist/ssr/client/assets`.
- Rendering untrusted HTML without the sanctioned sanitizer.
- Wiring an island package into legacy `src/*`/boot/router/store/SW without explicit migration approval.

## Apply checklist

- Public contract (props/events/types) defined and documented before internals.
- Widget is props-in / events-out, owns no host singletons, fetches no data.
- Data flows presentation → flow composable → store → SDK; no direct SDK/service calls from the widget.
- Sibling consumption is `dist`/entry + `link:`; `vue`/`quasar` are peers; assets reach `dist/ssr/client/assets`.
- No trusted headers/tokens in widgets; raw HTML only via the sanctioned sanitizer.
- SSR-safe and deterministic; no island wiring into legacy lanes without approval.

## Companion routing

- `$alaa-mono-package` — mandatory for any package boundary, exports, dedupe, asset, or extraction decision.
- `$alaa-frontend-developer` — the three-layer architecture and SSR component patterns.
- `$alaa-quasar-app-vite-v3` — exact Quasar component/SSR shapes and the app-vite build posture.
- `$alaa-security-review` — mandatory for raw-HTML/sanitization and any trust-boundary-adjacent widget path.
- `$alaa-frontend-doc-annotations` — documentation pass for the widget/package public surface.
- For data a widget needs, route through `60-frontend-sdk-consumption-contract.md` (host fetches, widget receives props).

For package internals and the package-family map, read `packages/developer_guide.md` and the package's own
`developer_guide.md`; do not encode package internals here.
