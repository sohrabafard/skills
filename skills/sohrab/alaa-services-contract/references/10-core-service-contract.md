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
