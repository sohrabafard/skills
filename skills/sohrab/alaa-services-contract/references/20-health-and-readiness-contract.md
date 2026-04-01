# Health And Readiness Contract

## `/api/health`

Use `GET /api/health` as the process-level liveness route.

Contract:
- auth: none
- success status: `200`
- payload keys: `status`, `service`, `timestamp`
- `status` value: `ok`
- `service` value: derived from `APP_NAME`
- `timestamp`: ISO-8601 UTC string

Behavior rules:
- do not call Redis, RabbitMQ, the database, ClickHouse, or any other external dependency from `/api/health`
- keep `/api/health` independent from business bootstrap state
- use `/api/health` to prove the app boot path, routing, and middleware path are alive

Example:

```json
{
  "status": "ok",
  "service": "auth",
  "timestamp": "2026-04-01T05:56:53.522505Z"
}
```

## `/api/ready`

Use `GET /api/ready` as the rollout-grade readiness route.

HTTP contract:
- auth: none
- `200` when the service is ready to serve traffic
- `503` when any required dependency or bootstrap invariant is not ready

JSON contract:
- `status`: `ready` or `not_ready`
- `code`: `SERVICE_READY` or `SERVICE_NOT_READY`
- `checks`: object keyed by canonical check name
- `failed_checks`: list of failed required check names in stable order
- `timestamp`: ISO-8601 UTC string
- `service`: derived from `APP_NAME`

Each `checks.<name>` item must use this exact shape:
- `status`: `up` or `down`
- `required`: boolean
- `code`: stable machine-readable code
- `message`: short operational sentence in English

Canonical check naming:
- use `database` for PostgreSQL-style primary database readiness
- use `clickhouse` as a separate readiness check for ClickHouse
- use `redis` for Redis
- use `rabbitmq` for RabbitMQ
- add service-specific bootstrap keys such as `passport`, `permission_catalog`, or `projects` only when they are real readiness prerequisites for that service

Current auth reference example:

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
  "timestamp": "2026-04-01T05:56:53.522505Z",
  "service": "auth"
}
```

Example shape for a service that depends on both PostgreSQL and ClickHouse:

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
    "clickhouse": {
      "status": "up",
      "required": true,
      "code": "READINESS_CLICKHOUSE_READY",
      "message": "ClickHouse is reachable."
    },
    "redis": {
      "status": "up",
      "required": true,
      "code": "READINESS_REDIS_READY",
      "message": "Redis is reachable."
    }
  },
  "failed_checks": [],
  "timestamp": "2026-04-01T05:56:53.522505Z",
  "service": "wa"
}
```

Readiness rules:
- include every required dependency or bootstrap invariant the service must satisfy before safe rollout
- define the checks from the real infrastructure of that service, not from another service template
- use `database` only for PostgreSQL-style primary database checks
- use `clickhouse` as a separate check whenever the service depends on ClickHouse
- if a service depends on both PostgreSQL and ClickHouse, include both checks
- keep check keys deterministic for that service
- keep failure codes stable and machine-readable
- prefer code families such as `READINESS_<CHECK>_READY`, `READINESS_<CHECK>_UNAVAILABLE`, `READINESS_<CHECK>_MISSING`, or `READINESS_<CHECK>_INVALID`
- when a prerequisite dependency is down, keep downstream check keys present and return deterministic failure information rather than omitting them
- do not make `/api/ready` depend on public-client state, OTP flow, or access tokens
- if short-lived caching is needed to reduce probe load, keep the response contract unchanged

Recommended check selection:
- include required infrastructure such as PostgreSQL, ClickHouse, Redis, RabbitMQ, object storage, or other mandatory backing services
- choose the actual backing systems of that service instead of copying another service's checks
- include required bootstrap invariants such as seed data, signing keys, or schema-dependent data prerequisites
- include optional dependencies only when there is a clear operational reason, and mark them with `required: false`

## Observability alignment

- return `X-Request-Id`, `X-Correlation-Id`, and `traceparent` on `/api/health` and `/api/ready` when the shared request stack already supports them
- keep successful health and readiness probes low-noise in normal request-completion logs when observability standards already support that behavior
