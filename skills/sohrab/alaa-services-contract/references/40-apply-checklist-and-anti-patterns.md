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
