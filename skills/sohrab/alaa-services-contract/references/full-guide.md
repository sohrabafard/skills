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
- `30-trusted-ingress-and-laravel-contract.md`
- `40-apply-checklist-and-anti-patterns.md`
- `50-laravel-copy-baselines.md`

---

# Scope, Service Modes, And Auth Routing

Use this file when the task is about onboarding an agent to the Ala services contract before code changes start.

## Purpose and use

Use this skill to hard-code the Ala backend service contract across Ala services.

This contract exists so agent outputs stay consistent across services and so operational visibility remains predictable for developers, SOC operators, and platform maintainers.

This skill is intentionally Ala-specific. The portability requirement for this skill is about filesystem independence and reuse across machines, not about being generic to unrelated organizations.

Use it when:
- creating or changing `auth`, `content`, `comment`, `ticket`, `vod`, `wa`, or another Ala backend service
- explaining how a frontend-facing backend sits behind the gateway and inside the wider Ala platform
- standardizing the shared `service-ci-kit` GitLab CI/CD baseline for new or refactored Ala services
- standardizing `/api/health`
- standardizing `/api/ready`
- fixing exact readiness payloads and check naming
- standardizing `X-Request-Id` and `traceparent`
- enforcing request and readiness event names and machine-readable codes
- standardizing `RequestObservabilityMiddleware`
- standardizing `ResolveUserMiddleware`
- adding or reviewing the Alaa Platform Observability Directive
- aligning OpenTelemetry and Prometheus behavior across Go and Laravel services
- aligning Laravel Resource-first `/api/*` success responses
- helping a new Ala service understand the current service landscape, ownership boundaries, and expected interaction model before implementation
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
- Collector gateway ownership
- Prometheus scrape rules and metric naming
- shared metric catalog and validation rules
- cross-runtime observability guidance for Go and Laravel

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

## Auth-specific routing note

- When the task touches the `auth` service and any frontend or frontend-facing identity integration depends on academic form behavior, read `docs/ops/auth-academic-policy-contract.md` in the `auth` repository before planning or editing.
- Treat that document as the canonical frontend integration contract for auth academic policy.
- When auth academic policy changes, update the frontend implementation and any contract-facing docs or Postman artifacts in the same effort.

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
| `entitlement-api` | normalized authorization business truth | other services must not treat OpenFGA tuples as the source of truth for business grants |
| `projector` | derived tuple projection into OpenFGA | keep it as a derived-state writer, not as the business-truth owner |

Components currently under evaluation but expected to follow this contract where relevant:
- `notification-core`
- `realtime-hub`
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
- Use the actual Ala service identifier such as `auth`, `content`, `comment`, `ticket`, `vod`, or `wa`.
- Do not return framework or runtime names such as `Laravel`, `Go`, `Node`, or `PHP`.
- Do not decorate the value with environment or version strings.

## Route families

Every route belongs to exactly one family:

| Family           | Purpose                                  |   Public client use? | Contract rule                                 |
|------------------|------------------------------------------|---------------------:|-----------------------------------------------|
| public API       | product-facing API behavior              | yes, when documented | keep separate from operational probes         |
| trusted internal | sanitized gateway-derived context        |                   no | align exactly with `$alaa-trust-gateway-auth` |
| operational      | liveness, readiness, rollout diagnostics |                   no | keep auth expectations explicit and minimal   |

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

---

# Alaa Platform Observability Directive

Use this file when the task includes telemetry architecture, OpenTelemetry exporter setup, OTLP endpoint ownership, Collector gateway design, Prometheus scrape endpoints, metric catalogs, queue or dependency instrumentation, or cross-runtime observability alignment between Go and Laravel services.

## Contract posture

This directive extends `20-operational-and-observability-contract.md`.

Working rule:
- apply `20-operational-and-observability-contract.md` and this file together for observability work
- `20` owns the exact stable surfaces such as response headers, event names, machine-readable codes, and middleware invariants
- this file owns the larger telemetry design, OTLP path, Collector gateway rules, Prometheus contract, and validation expectations

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

Observability must respect those boundaries:
- gateway telemetry must explain trust-boundary behavior
- authz-runtime telemetry must explain route-time allow or deny behavior
- service telemetry must explain work done inside the service boundary
- entitlement control-plane telemetry must explain derived-state maintenance, not pretend to be the source of business truth

## Platform direction

Every long-lived Ala service must be prepared to:
- produce standard telemetry with official OpenTelemetry and Prometheus libraries
- send traces and logs to an OTLP endpoint
- expose a Prometheus-compatible internal metrics endpoint for scraping
- stay vendor-neutral in application code

The platform direction is:
- application code produces correct telemetry
- Collector tiers receive, process, batch, retry, route, redact, transform, and fan out telemetry
- Prometheus scrapes service metrics from internal endpoints
- backends can change later by configuration without redesigning each service

The current Ala target architecture is:
- application services send OpenTelemetry traces, exceptions, and structured logs to a gateway OpenTelemetry Collector endpoint
- application services expose Prometheus-compatible metrics endpoints; metrics are first-class and must not be skipped when tracing is added
- the gateway Collector exports to SigNoz or another approved backend through Collector configuration
- SigNoz tokens, endpoints, and exporter-specific headers belong in Collector or deployment secrets, not application code

### What goes where

Use this ownership table to avoid moving platform concerns into application code:

| Data type                           | App code        | OTel Collector          | Metrics backend |
| ----------------------------------- | --------------- | ----------------------- | --------------- |
| traces                              | yes             | receive/process/export  | yes             |
| exceptions                          | yes             | receive/process/export  | yes             |
| structured logs                     | yes             | collect/process/export  | yes             |
| Prometheus metrics                  | expose endpoint | scrape/forward optional | yes             |
| retry/compression/fan-out/redaction | no by default   | yes                     | no              |

Rules:
- keep telemetry endpoint configuration in env or deployment config
- do not hard-code backend-specific behavior in service code
- do not build custom multi-backend fan-out, retry queues, compression, or redaction pipelines inside application code unless the platform explicitly approves an exception
- do not replace the Prometheus scrape contract with ad hoc pushing for normal services
- do not use the Pushgateway for normal long-lived service metrics; only use it for explicit service-level batch-job cases when the lifecycle is intentionally decoupled from individual instances
- do not deliver "tracing only" observability; metrics, logs, traces, and exceptions are all part of done

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
- `project_id` when available
- `user_id` when available and allowed
- `http.method` when request-related
- `http.route` or a stable route name when request-related
- `http.status` when request-related
- `duration_ms` when the log measures work over time

Keep these field names stable.

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

## Service adoption checklist

When applying this skill to a service, finish by checking:
- `/api/health`
- `/api/ready`
- `X-Request-Id`
- `traceparent`
- structured JSON logs
- exact event/code naming
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
- it sends traces and logs through the OTLP path without backend-specific code branches
- it exposes a Prometheus-compatible internal metrics endpoint
- it provides the shared HTTP, readiness, dependency, DB, and queue metrics that apply to it
- it uses bounded labels only
- real resource identifiers appear only in logs or trace attributes when needed, never as metric labels
- OTLP exporter endpoint and protocol are controlled by env or deployment config
- no vendor-specific backend coupling exists in application code
- it captures readiness failures, request failures, queue failures, dependency failures, and important denials with enough context for diagnosis
- it makes slow routes, slow queries, slow dependencies, repeated retries, and repeated denials easy to identify
- its collector path is observable enough to show queue pressure, export failures, or dropped telemetry when those happen

## Anti-patterns

- building custom telemetry fan-out inside application code
- treating telemetry as optional after feature work is done
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

Route-shape reminder:
- gateway-facing routes may include a service prefix such as `/auth`, `/content`, `/comment`, `/ticket`, `/vod`, or `/wa`
- trusted internal routes stay service-owned and are not public frontend discovery surfaces
- operational routes remain separate from product routes even when they share the `/api/*` prefix
- service-local routes may differ after gateway prefix stripping
- use `$alaa-trust-gateway-auth` for exact trusted-ingress and prefix-strip behavior when the task depends on those details

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

---

# Apply Checklist And Anti-Patterns

## Step-by-step apply checklist

1. Read `AGENTS.md`.
2. Identify the repository role and service mode.
3. Read the smallest owning reference file first.
4. Read `21-alaa-platform-observability-directive.md` whenever observability design, OTLP configuration, Prometheus metrics, or Collector topology is in scope.
5. Confirm the canonical Ala service identity.
6. Confirm the exact route-family split.
7. Align `/api/health` and `/api/ready` to the exact contract.
8. Align exact readiness check names and codes.
9. Align `X-Request-Id`, `traceparent`, request logging, and stable event/code naming.
10. Align `RequestObservabilityMiddleware` and `ResolveUserMiddleware` semantics where required.
11. Align the Alaa Platform Observability Directive when the task touches logs, traces, metrics, queues, DBs, dependencies, or workers.
12. Add or align exact response envelopes, exact headers, exact event names, exact code naming, and exact metric names where the contract owns them.
13. Update docs, Postman, and runbooks in the same patch when public or operational behavior changes.
14. Run focused tests for every changed contract surface.
15. Report blockers explicitly when exact convergence is not possible.

## Short service adoption checklist

When applying this skill to a service, finish by checking:
- `/api/health`
- `/api/ready`
- `X-Request-Id`
- `traceparent`
- structured JSON logs
- exact event/code naming
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
- `/api/health` and `/api/ready` return `X-Request-Id` and `traceparent`
- rendered API error responses after exceptions still return `X-Request-Id` and `traceparent`
- no service code, config, docs, tests, or emitted headers still mention `X-Correlation-Id`
- successful probes stay low-noise
- readiness failure and request failure logs use the exact event and code rules
- logs are structured JSON in production
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
- invalid `X-User-Mobile`
- malformed `X-User-Fname` or `X-User-Lname`
- malformed `X-Location-*` values
- parity between `$request->user()` and `Auth::user()`
- parity with any legacy guard still in use

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
- request or readiness logs invent alternate event names for the same flow
- logs are not structured JSON in production
- the service hard-codes vendor-specific telemetry backends instead of targeting OTLP and the shared metrics contract
- metrics use unbounded labels or raw user or tenant identifiers
- a public route exposes the internal metrics endpoint
- a normal long-lived service uses Pushgateway for app metrics
- trusted headers are parsed in controllers, policies, or repositories
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
- leaving helper responsibilities implicit so each agent re-invents them
- reviving the retired profile-blob trust surface instead of consuming the compact header projection
- pushing observability logic into app code that belongs in the Collector layer

---

# Laravel Copy Baselines

Use these baselines when a Laravel repository needs copy-oriented implementation help.

Rules:
- Adapt namespaces and injected helpers to the target repository.
- Preserve the owned behavior and field names.
- Do not change headers, event names, code names, envelope shapes, or metric names while copying.

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
