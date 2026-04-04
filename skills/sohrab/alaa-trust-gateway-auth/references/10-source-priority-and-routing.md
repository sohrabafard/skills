# Source priority

When facts conflict, trust sources in this order:
1. The active HAProxy template and values in the gateway repo
2. Rendered manifests from the gateway repo
3. Gateway docs and README text
4. Older team assumptions

If README text and HAProxy config disagree, trust the config.

# Execution order for agents
Use this execution order:

1. Read this skill to establish the shared trust boundary.
2. Determine whether the task is gateway-side, downstream-service-side, observability-side, runtime-side, or deployment-side.
3. Read the matching companion skill(s) before giving implementation advice.
4. Then inspect repository-local code, docs, and configs.
5. Only after that, propose or implement changes.

Examples:
- Gateway ACL/header change -> read `alaa-haproxy`, then inspect gateway config.
- Laravel trusted-header middleware change -> read `alaa-laravel-architecture` and `alaa-php-clean-code`; if Octane is used, also read `alaa-octane-performance`.
- Auth deny logging or trace propagation change -> read `alaa-observability-soc`.
- Public exposure or trusted-proxy deployment change -> read `alaa-docker-production`; on Arvan, also read `caas-arvan-kuber`.
- JWT/header-trust review -> read `alaa-security-review` before suggesting fixes.

# Compact trust boundary
- Shared concept: `tenant_id`, `tenant_public_id`, `project_id` and the compact JWT claim `pid` point at one tenant-boundary concept at the public platform edge.
- Canonical JWT claim key: `pid`
- Canonical public API field name: `project_id`
- Canonical trusted header name: `X-Project-Id`
- Legacy names to rename during refactor:
  - `tenant_id` -> `project_id` at public API and service-domain boundaries
  - `tenant_public_id` -> `project_id` at public API and service-domain boundaries
  - `tenant_id` -> `pid` only inside compact JWT claim mapping or other gateway-internal trust-boundary notation
  - `tenant_public_id` -> `pid` only inside compact JWT claim mapping or other gateway-internal trust-boundary notation
  - `X-Tenant-Public-Id` -> `X-Project-Id`
- Migration rule: keep trust semantics unchanged while renaming. Public API payloads and docs keep the `project_id` name; compact JWT and gateway-internal claim mapping use `pid`.
- Validation rule for the public identifier: validate the trusted project boundary (`project_id`) as UUIDv7 after gateway verification.
- Example canonical value: `018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- Internal-key rule during migration: if a service still keeps an internal numeric tenant or project key in its own database, treat that key as a service-local storage detail, not as the public boundary contract and not as a replacement for `pid`.
- Documentation rule: OpenAPI, README examples, and service docs should prefer `project_id` for public API fields and `X-Project-Id` for trusted headers. Use `pid` only when the subject is the compact JWT claim map or another gateway-internal trust-boundary detail. If a legacy alias still appears, mark it explicitly as legacy and equivalent to the public tenant boundary.

# Core trust model
- The gateway is the authentication boundary for protected HTTP routes.
- The gateway verifies the Bearer JWT and then injects trusted request headers for downstream services.
- Downstream services must still do authorization and tenant-safe data access.
- Client-supplied internal auth headers are never trusted.
- Tenant context is derived from the verified token, not from request body, query string, route params, or client-supplied headers.
- Naming rule: `tenant_id`, `tenant_public_id`, `project_id`, and `pid` refer to the same tenant-boundary concept in the current platform, but they belong to different layers.
- Refactor target standard: rename `tenant_id` and `tenant_public_id` usages to `project_id` at public API or service-domain boundaries and to `pid` only inside compact JWT claim handling.
- Header target standard: rename `X-Tenant-Public-Id` to `X-Project-Id` in service contracts and docs during the platform refactor.
- Until that refactor is complete, treat `tenant_id` and `tenant_public_id` only as legacy aliases of the same trusted boundary and normalize them back to the canonical layer-specific contract: `project_id` in public APIs and `pid` / `X-Project-Id` in compact JWT and trusted-header handling.

# How auth enters the system
## Protected routes
- Auth enters through `Authorization: Bearer <token>`.
- The gateway extracts the bearer token from the `Authorization` header.
- If a protected route has no bearer token, the gateway returns `401 missing_token`.

## Public routes
The current gateway config marks these paths as public and skips JWT checks for them:
- `/auth/api/v3/otp/request`
- `/auth/api/v3/otp/verify`
- `/auth/api/v3/token/refresh`
- `/auth/api/v3/logout`
- `/auth/api/ready`
- `/auth/api/health`
- `/vod/api/ready`
- `/vod/api/health`
- `/comment/api/ready`
- `/comment/api/health`
- `/ticket/api/ready`
- `/ticket/api/health`
- `/wa/api/ready`
- `/healthz`
- `/wa/ingest/v1/events`

Important: a public path at the gateway does not automatically mean the downstream service should trust the caller. The downstream service must still apply its own route-level rules.
- Gateway rule: sanitize internal auth/context headers on every route, including public routes. Even when the gateway skips token verification for a public route, it must still delete spoofable inbound `X-*` auth/context headers before proxying.

## Auth-service route drift that must not be copied forward
- Auth-service is now `v3` only and no longer exposes `/api/v2` routes locally.
- Current auth-service local public routes are:
  - `/api/v3/otp/request`
  - `/api/v3/otp/verify`
  - `/api/v3/token/refresh`
  - `/api/v3/logout`
- Current auth-service local protected gateway routes are:
  - `/api/v3/sessions*`
  - `/api/v3/totp*`
  - `/api/v3/admin/users/{user}/sessions*`
  - `/api/v3/admin/users/{user}/authz-overrides*`
  - `/api/v3/profile*`
- If any gateway or repo doc still mentions `/auth/api/v2/*`, treat that as legacy drift to remove, not as active client guidance.
- Do not reintroduce `/api/v2` into auth-service and do not teach new services or callers to depend on retired auth v2 routes.

## Gateway-facing routes vs service-local routes
This distinction is mandatory.

- Clients call the gateway-facing route, which includes the service prefix used for gateway routing.
- The gateway routes by prefix and may strip that prefix before proxying to the backend service.
- A backend service must therefore document and implement its own local route shape, not the gateway-facing one.

Current HAProxy behavior:
- Routing happens by path prefix such as `/auth`, `/vod`, `/comment`, `/ticket`, and `/wa`.
- When `stripPathPrefix: true`, the gateway removes that prefix before sending the request to the downstream service.

Example for auth service:
- Gateway-facing public route: `/auth/api/v3/otp/request`
- Service-local route after prefix strip: `/api/v3/otp/request`

Example for auth health:
- Gateway-facing route: `/auth/api/health`
- Service-local route: `/api/health`

Rule for future agents:
- When writing or reviewing the gateway itself, use gateway-facing routes.
- When writing or reviewing a downstream service, use service-local routes after prefix stripping.
- Never force a backend service to define routes with the gateway prefix unless that backend is intentionally designed that way.

## Current forwarded header surface
- The current forwarded identity and token headers injected after verification are `X-Project-Id`, `X-User-Id`, `X-User-Mobile`, `X-Access`, `X-Access-Token-Id`, `X-TOKEN-CLIENT-ID`, `X-TOKEN-ISSUED-AT`, `X-TOKEN-NOT-BEFORE`, `X-TOKEN-EXPIRES-AT`, `X-USER-SCOPES`, `X-User-Fname`, `X-User-Lname`, `X-Location-Ostan`, `X-Location-Shahrestan`, `X-Location-Bakhsh`, `X-Location-Shahr`, `X-Location-Shobe`, and `X-Location-School`.
