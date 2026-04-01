# Adoption Checklist And Anti-Patterns

## Apply this skill to a service

1. Inspect the service's required infrastructure and bootstrap invariants. Do not copy the `auth` checks blindly.
2. Add or align `GET /api/health` as a process-level route that has no external dependency checks.
3. Add or align `GET /api/ready` with the exact shared envelope from `20-health-and-readiness-contract.md`.
4. Source the `service` field from `APP_NAME`.
5. Add deterministic check keys, status values, codes, and failure messages.
6. Use `database` for PostgreSQL-style readiness, `clickhouse` for ClickHouse readiness, and include both when the service depends on both stores.
7. If the service is Laravel-based, inspect existing response patterns first and adopt Resource-first success responses with controller-owned transport concerns.
8. Add or align `php artisan ops:ready --json` when the service is Laravel-based.
9. Add feature tests for ready and not-ready paths.
10. Update operational docs, runbooks, and API artifacts when those documents already cover health, readiness, or response-contract behavior.

## Validation targets

- `/api/health` returns `200` without requiring PostgreSQL, ClickHouse, Redis, RabbitMQ, or any other external dependency.
- `/api/ready` returns `200` only when all required checks are up.
- `/api/ready` returns `503` and a stable `failed_checks` list when any required check is down.
- `service` matches `APP_NAME`.
- correlation headers and probe logging behavior stay aligned with the observability baseline.
- required checks match the real service dependencies instead of copied assumptions from another service.
- for example, if `wa` depends on ClickHouse, its readiness contract should check `clickhouse` rather than pretending that dependency is `database`.
- if the service is Laravel-based, successful JSON responses are centralized through Resources and do not leak backend-only fields such as internal IDs or persistence details.

## Anti-patterns

- requiring an access token, OTP, or user session for `/api/health` or `/api/ready`
- returning `Laravel` or another framework name in `service`
- using `/api/ready` as a client preflight, login helper, or feature-availability endpoint
- making `/api/health` depend on Redis, RabbitMQ, PostgreSQL, ClickHouse, or another service
- inventing a new readiness payload shape for each service
- silently returning `200` when a required dependency is down
- omitting deterministic failed check keys when a prerequisite dependency is unavailable
- copying auth-specific readiness checks into another service without reviewing that service's real bootstrap requirements or real infrastructure stack
- collapsing PostgreSQL and ClickHouse into one ambiguous check when the service depends on both
- forcing Laravel Resource rules onto non-Laravel services
- for Laravel services, shaping success payloads ad hoc inside services or controllers instead of centralizing them through Resources
