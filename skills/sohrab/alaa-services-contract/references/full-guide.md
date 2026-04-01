# Purpose
Use this skill to keep Ala backend services operationally and contractually consistent across frameworks and repositories.

This skill is the source of truth for:
- service naming
- process-level health and rollout-grade readiness contracts
- dependency and bootstrap check rules
- operational route expectations versus public API expectations
- inter-service contract discipline
- Laravel-only success-response rules when the target service is Laravel-based

# When to use
- Creating or changing a backend service such as `auth`, `vod`, `comment`, `ticket`, or `wa`
- Standardizing `/api/health` or `/api/ready`
- Reviewing whether a route is public, trusted-internal, or operational
- Aligning service names, readiness checks, and probe response envelopes
- Applying the shared Ala contract to an existing service
- Changing API response shaping in a Laravel service

# Companion skill routing (mandatory)
Read this skill first for cross-service contract work, then route to the skills that own deeper concerns.

Mandatory routing rules:
- If the task is non-trivial, multi-file, or behavior-changing, read `$alaa-workflow` first.
- If the task touches gateway-derived identity, trusted headers, tenant or project propagation, or downstream trust semantics, read `$alaa-trust-gateway-auth` first.
- If the task touches logs, traces, correlation headers, probe noise, alerts, or observability behavior, read `$alaa-observability-soc` first.
- If the task touches schema, seed/bootstrap state, Redis, PostgreSQL, ClickHouse, or other persistence invariants, read `$alaa-data-layer` first.
- If the task touches RabbitMQ or queue-plane readiness expectations, read `$alaa-async-messaging` and `$alaa-laravel-job-rabbitmq` first.
- If the task changes Laravel controller, service, request, resource, or DTO boundaries, read `$alaa-laravel-architecture` and `$alaa-php-clean-code` first.
- If the task changes docs, Postman artifacts, runbooks, or contract examples, read `$alaa-docs-farsi` first.

Do not continue with implementation advice until the relevant companion skill has been read.

# Execution order for agents
Use this execution order:

1. Read this skill to establish the shared service contract.
2. Determine whether the task is mainly about operational routes, readiness, inter-service HTTP behavior, or Laravel response shaping.
3. Determine whether the target service is Laravel-based or not.
4. Read every companion skill that applies to the current task.
5. Inspect the target repository's actual dependencies, current contracts, and current response shapes.
6. Only then propose or implement changes.

# Core service contract

## Canonical service identity
- `service` must be a stable machine-readable service identifier derived from `APP_NAME` or an equivalent service-level config.
- Expected examples are `auth`, `vod`, `comment`, `ticket`, and `wa`.
- Do not return framework, vendor, or runtime names such as `Laravel`, `Go`, or `Node`.
- Do not decorate the value with environment names, version strings, or human-facing labels.

## Route family expectations
| Route family            | Purpose                                             | Public client use?   | Notes                                                  |
|-------------------------|-----------------------------------------------------|----------------------|--------------------------------------------------------|
| Public API routes       | Product-facing browser, mobile, or partner behavior | Yes, when documented | Keep these independent from operational probes.        |
| Trusted internal routes | Gateway-derived or downstream trusted context       | No                   | Use `$alaa-trust-gateway-auth` as the source of truth. |
| Operational routes      | Liveness, readiness, rollout checks, smoke probes   | No                   | Keep auth expectations explicit and minimal.           |

## Operational caller expectations
- `GET /api/health` and `GET /api/ready` exist for gateway, ingress, orchestrator, runtime validation scripts, smoke checks, and automated tests.
- End-user clients should not depend on these routes for product behavior.
- `/api/ready` may be called by a gateway, ingress, orchestrator, or runtime validator, but the contract must not assume one specific caller.
- Keep operational routes available without access tokens, OTP, cookies, or end-user session state.

## Service-specific infrastructure modeling
- Define readiness checks from the real infrastructure and bootstrap requirements of that service.
- Use `database` for PostgreSQL-style primary database readiness.
- Use `clickhouse` as a separate readiness check when the service depends on ClickHouse.
- If a service depends on both PostgreSQL and ClickHouse, include both `database` and `clickhouse`.
- Do not copy another service's readiness checks blindly.
- Auth-specific checks such as `passport`, `permission_catalog`, or `projects` are valid only when they are true readiness prerequisites for that service.

# Health and readiness contract

## `/api/health`
Use `GET /api/health` as the process-level liveness route.

Contract:
- auth: none
- success status: `200`
- payload keys: `status`, `service`, `timestamp`
- `status` value: `ok`
- `service` value: derived from `APP_NAME`
- `timestamp`: ISO-8601 UTC string

Rules:
- do not call Redis, RabbitMQ, PostgreSQL, ClickHouse, or any other external dependency from `/api/health`
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
- `failed_checks`: stable ordered list of failed required check names
- `timestamp`: ISO-8601 UTC string
- `service`: derived from `APP_NAME`

Each `checks.<name>` item must use this exact shape:
- `status`: `up` or `down`
- `required`: boolean
- `code`: stable machine-readable code
- `message`: short operational sentence in English

## Canonical check naming
- use `database` for PostgreSQL-style primary database readiness
- use `clickhouse` as a separate readiness check for ClickHouse
- use `redis` for Redis
- use `rabbitmq` for RabbitMQ
- add service-specific bootstrap keys only when they are real readiness prerequisites for that service

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

## Failure and code rules
- include every required dependency or bootstrap invariant the service must satisfy before safe rollout
- keep check keys deterministic for that service
- keep failure codes stable and machine-readable
- prefer code families such as `READINESS_<CHECK>_READY`, `READINESS_<CHECK>_UNAVAILABLE`, `READINESS_<CHECK>_MISSING`, or `READINESS_<CHECK>_INVALID`
- when a prerequisite dependency is down, keep downstream check keys present and return deterministic failure information rather than omitting them
- do not make `/api/ready` depend on public-client state, OTP flow, or access tokens
- if short-lived caching is needed to reduce probe load, keep the response contract unchanged

## Observability alignment
- return `X-Request-Id`, `X-Correlation-Id`, and `traceparent` on `/api/health` and `/api/ready` when the shared request stack already supports them
- keep successful health and readiness probes low-noise in normal request-completion logs when observability standards already support that behavior
- keep readiness transition logs when they are operationally valuable

## Laravel baseline for health and readiness
For Laravel services, standardize these defaults unless the repository already documents a different shared pattern:
- route names: `api.health` and `api.ready`
- `GET /api/health` for process-level liveness
- `GET /api/ready` for rollout-grade readiness
- `php artisan ops:ready --json` backed by the same readiness collector when feasible
- feature tests for both healthy and not-ready paths

# Inter-service HTTP and context

## Baseline flow
Treat the default Ala flow like this:
- public client -> gateway -> backend service
- backend service -> backend service only for internal workloads that truly require it
- backend service -> async infrastructure for queue, event, or job delivery when appropriate

Do not let services recreate browser-facing trust assumptions on internal hops.

## Trust-boundary handoff
- Use `$alaa-trust-gateway-auth` as the source of truth for gateway-derived identity, trusted headers, tenant or project propagation, and downstream auth semantics.
- Do not redefine trusted auth headers in this skill.
- Do not let one service invent a new internal auth contract that conflicts with the gateway-trust model.

## Correlation and probe traceability
- Preserve `X-Request-Id`, `X-Correlation-Id`, and `traceparent` across internal HTTP hops when the shared stack already supports them.
- Return the same correlation headers from `/api/health` and `/api/ready` when possible so probes remain traceable.
- Keep probe logging low-noise, but do not remove transition logs that are operationally valuable.

## Readiness boundaries
- Prefer direct checks of the service's own required infrastructure and bootstrap state.
- Do not implement `/api/ready` by calling another service's `/api/ready` unless that dependency is an explicit, approved part of rollout semantics.
- Avoid transitive readiness chains that amplify unrelated failures across the platform.
- If a service depends on shared infrastructure such as Redis or RabbitMQ, check that infrastructure directly instead of proxying another app's status.

## HTTP contract discipline
- Keep operational routes separate from product-facing routes.
- Do not require bearer tokens, OTP, user cookies, or session state for operational routes.
- Keep machine-readable fields stable and English-language messages short and operational.
- Prefer one shared operational envelope across Ala services over per-service custom payload shapes.

# Laravel service rules

## Scope
Apply this section only when the target service is Laravel-based.

## Core rule
For Laravel APIs, treat Resources as the public success-response contract.

- Use Laravel Resources for successful JSON HTTP responses.
- Let services return domain data or small DTOs instead of transport-shaped arrays or `JsonResponse` instances.
- Let controllers own HTTP status codes and response serialization through `JsonResource` or `ResourceCollection`.
- Keep business logic separate from transport concerns.
- Make the Resource the single place that defines what the client is allowed to see.

## Default behavior
- Preserve existing success envelopes unless the contract is intentionally changed.
- Keep error responses aligned with the current service convention by default.
- Inspect existing repository patterns before changing response serialization.
- Use Laravel Boost `search-docs` first for version-specific Resource guidance.
- Keep docs, examples, and Postman artifacts aligned with the shipped Resource shape when the contract changes.

## Latest Laravel guidance worth using
These points reflect current official Laravel Resource guidance and should be used when they fit the repository style:
- Prefer explicit `JsonResource` and `ResourceCollection` classes for transport-safe serialization.
- Use `collection(...)` or a dedicated collection resource when returning collections or paginated results.
- Laravel's `toResource()` and `toResourceCollection()` convenience methods are acceptable when they reduce boilerplate and match the repository's style; do not force them into a repo that already prefers explicit resource instantiation.
- If the outer response needs transport-level headers, use the Resource response boundary through `response()` or `withResponse()` instead of pushing header logic into services.
- Laravel 13 JSON:API resources are opt-in only when the public contract is actually JSON:API. Do not switch a normal Ala API to JSON:API just because the framework supports it.
- Conditional attributes and relationships belong in the Resource layer when they are serialization concerns, not in services when they are only about transport shape.

## Boundary rules
- Do not return `JsonResponse` payload arrays from services.
- Do not let controllers leak raw models, persistence-only attributes, internal IDs, or temporary implementation fields.
- Use DTOs when a stable typed boundary is helpful between service and controller layers.
- Keep Resources focused on transport-safe serialization, not domain behavior.
- Keep controllers thin and deterministic.

## Testing and docs alignment
- Add focused JSON contract tests for success responses.
- Keep docs, examples, and Postman artifacts aligned with the actual Resource output.
- For Laravel success-response tests, prefer assertions that make leaked internal fields obvious.
- When a Resource intentionally changes the public contract, document that change explicitly.

## Auth reference precedent
The auth repository commit `40d7e6e` is the approved reference precedent for this rule.

That precedent established:
- Resource-first success responses for `/api/*`
- service/domain DTOs under the controller boundary
- controller-owned HTTP status codes and serialization
- preservation of current error conventions
- removal of backend-only public leakage such as `access_token_id`

# Service implementation checklist
Use this checklist when applying this skill to a service:
1. Inspect the service's required infrastructure and bootstrap invariants. Do not copy `auth` checks blindly.
2. Add or align `GET /api/health` as a process-level route that has no external dependency checks.
3. Add or align `GET /api/ready` with the shared readiness envelope and real service-specific checks.
4. Source the `service` field from `APP_NAME` or the equivalent service identity config.
5. Add deterministic check keys, status values, codes, and failure messages.
6. Use `database` for PostgreSQL-style readiness, `clickhouse` for ClickHouse readiness, and include both when the service depends on both stores.
7. If the service is Laravel-based, inspect existing response patterns first and adopt Resource-first success responses with controller-owned transport concerns.
8. Add or align `php artisan ops:ready --json` when the service is Laravel-based.
9. Add feature or integration tests for ready and not-ready paths.
10. Update operational docs, runbooks, and API artifacts when those documents already cover health, readiness, or response-contract behavior.

# Review checklist for agents
Flag a problem when you see any of these:
- `/api/health` calling external dependencies
- `/api/ready` requiring an access token, OTP, cookie, or user session
- `service` returning `Laravel`, `Go`, or another framework/runtime name instead of the service identifier
- readiness checks copied from another service without verifying the real infra stack
- PostgreSQL and ClickHouse collapsed into one ambiguous check when the service depends on both
- a service implementing `/api/ready` by proxying another service's readiness without an approved rollout reason
- operational routes documented as client-facing product APIs
- Laravel Resource rules forced onto a non-Laravel service
- in a Laravel service, success payloads shaped ad hoc inside services or controllers instead of centralizing them through Resources
- Laravel responses leaking internal IDs, persistence details, or temporary implementation fields
- docs or Postman examples drifting from the actual contract

# Anti-patterns
- Treating `/api/ready` as a client preflight, login helper, or feature-availability endpoint
- Returning `200` from readiness when a required dependency is down
- Omitting deterministic failed check keys when a prerequisite dependency is unavailable
- Making `/api/health` depend on Redis, RabbitMQ, PostgreSQL, ClickHouse, or another service
- Inventing a new readiness payload shape for each service
- Forcing Laravel-specific implementation rules onto non-Laravel services
- In Laravel services, returning transport-shaped arrays from services, leaking raw models, or scattering transport concerns across layers
