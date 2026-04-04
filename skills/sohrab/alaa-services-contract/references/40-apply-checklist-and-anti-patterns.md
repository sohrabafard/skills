# Apply Checklist And Anti-Patterns

## Step-by-step apply checklist

1. Identify the service mode first.
2. Read the smallest relevant contract file before changing code.
3. Load the required companion skills.
4. Inspect the current route families, middleware order, auth shape, observability shape, readiness checks, response boundaries, and trusted-header expectations.
5. Converge the repository to the exact contract instead of partially mirroring it.
6. Remove active dependencies on retired trust surfaces such as `X-Profile` or old claim names when the compact contract replaced them.
7. Add required helper or support components when they do not exist.
8. Add or align `/api/health`, `/api/ready`, and `ops:ready --json` when the target is Laravel.
9. Add or align `RequestObservabilityMiddleware` and `ResolveUserMiddleware` semantics where required.
10. Add or align exact response envelopes, exact headers, exact event names, and exact code naming.
11. Update docs, Postman, and runbooks in the same patch when public or operational behavior changes.
12. Run focused tests for every changed contract surface.
13. Report blockers explicitly when exact convergence is not possible.

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
- metrics use bounded labels only

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
- `service` returns a framework or runtime name
- `X-Correlation-Id` remains anywhere in service code, config, tests, docs, or emitted headers after the migration
- `X-Trace-Id` is still treated as a response-header requirement
- request or readiness logs invent alternate event names for the same flow
- metrics use unbounded labels
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
- scattering trusted-user normalization across controllers, policies, resources, and observers
- leaving helper responsibilities implicit so each agent re-invents them
- reviving the retired profile-blob trust surface instead of consuming the compact header projection
