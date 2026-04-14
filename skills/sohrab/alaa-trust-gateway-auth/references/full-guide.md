# Alaa Trust Gateway Auth Full Guide

## Purpose and use

Use this skill when a service lives behind the Ala gateway, or when a change touches auth headers, tenant context, reverse-proxy trust, or request identity propagation.

This guide exists so agents do not guess about the gateway trust boundary.

Use it for:
- building or reviewing a downstream service behind the gateway
- adding middleware that reads user or tenant context from headers
- debugging auth failures, tenant mismatch, or missing headers
- changing gateway config, ingress behavior, trusted-proxy settings, or service exposure
- reviewing whether a service is safe to expose directly or must stay behind the gateway

## Ala end-to-end authn and authz picture

Use this section when the task spans frontend, gateway, downstream service, or entitlement-platform behavior and one shared platform picture is required before implementation.

Default Ala flow:
- frontend or public client -> gateway -> backend service
- gateway -> active request-time checker such as `authz-sidecar` or `entitlement-spoa` -> OpenFGA
- normalized business change -> `entitlement-api` -> `projector` -> OpenFGA

Plain meaning:
- the gateway owns authentication
- the active request-time checker owns the fine-grained route decision
- downstream backends consume normalized trusted context and still own business authorization inside the service
- `entitlement-api` owns normalized authorization business truth
- `projector` writes derived tuples
- OpenFGA stores derived effective authorization state

## Layer ownership map

### Frontend or public client

- call documented gateway-facing routes only
- send `Authorization: Bearer ...` only to the gateway
- never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, or `X-Authz-*`
- never call `authz-sidecar`, `entitlement-spoa`, or OpenFGA directly

### Gateway

- verify the access token
- sanitize spoofable inbound auth and authz headers
- inject trusted headers from verified claims
- derive request-time authorization inputs such as endpoint category
- call the active request-time checker
- fail closed on deny or dependency failure

### Active request-time checker

- trust only sanitized gateway context
- normalize trusted route context when needed
- map `endpoint_category + target_type` to the final `can_*` permission
- check OpenFGA with the pinned model
- return an allow or deny decision plus observability metadata

### Downstream backend service

- trust only sanitized gateway context
- normalize trusted headers once near ingress
- do business authorization after identity normalization
- never treat `X-Authz-*` decision metadata as a credential

### Entitlement control plane

- `entitlement-api` owns normalized authorization aggregates
- `projector` is the only intended tuple writer
- OpenFGA is derived authorization state, not the business source of truth

## Companion skill routing

Read this skill first for any gateway-backed auth, trusted-header, tenant-context, or downstream trust-boundary task.

Before proposing code or config changes, identify which companion skill or skills apply to the current task and read them before continuing.

Mandatory routing rules:
- If the task touches JWT correctness, token verification, authn or authz risk, header trust, tenant-isolation risk, or token-handling mistakes, read `alaa-security-review` first.
- If the task touches Laravel middleware, guards, request-context builders, Policies, Gates, controllers, services, DTO boundaries, response envelopes, or PHP and Laravel clean-code decisions inside those files, read `alaa-laravel-architecture` and `alaa-php-clean-code` first.
- If the task touches Octane, long-lived workers, request-scoped auth state, tenant-context reset, or performance-sensitive auth middleware, read `alaa-octane-performance` first.
- If the task touches deny logging, request correlation, trace propagation, security events, or auth error observability, read `alaa-observability-soc` first.
- If the task touches trusted proxy boundaries, direct service exposure, container networking, edge-only exposure, or `X-Forwarded-*` behavior, read `alaa-docker-production` first.
- If the task touches HAProxy ACL order, JWT verification behavior, header mutation, path stripping, route exposure, or gateway-side auth flow, read `alaa-haproxy` first.
- If the task touches Arvan or Kubernetes entrypoints, ingress versus load balancer exposure, edge trust boundaries, or public service exposure on Arvan, read `caas-arvan-kuber` first.

Do not continue with implementation advice until the relevant companion skill has been read. If multiple areas apply, read all relevant companion skills and follow the stricter rule when they overlap.

## Source priority and execution order

### Source priority

When facts conflict, trust sources in this order:
1. The active HAProxy template and values in the gateway repo.
2. Rendered manifests from the gateway repo.
3. Gateway docs and README text.
4. Older team assumptions.

If README text and HAProxy config disagree, trust the config.

### Execution order for agents

Use this execution order:
1. Read this skill to establish the shared trust boundary.
2. Determine whether the task is gateway-side, downstream-service-side, observability-side, runtime-side, or deployment-side.
3. Read the matching companion skill or skills before giving implementation advice.
4. Then inspect repository-local code, docs, and configs.
5. Only after that, propose or implement changes.

Examples:
- Gateway ACL or header change -> read `alaa-haproxy`, then inspect gateway config.
- Laravel trusted-header middleware change -> read `alaa-laravel-architecture` and `alaa-php-clean-code`; if Octane is used, also read `alaa-octane-performance`.
- Auth deny logging or trace propagation change -> read `alaa-observability-soc`.
- Public exposure or trusted-proxy deployment change -> read `alaa-docker-production`; on Arvan, also read `caas-arvan-kuber`.
- JWT or header-trust review -> read `alaa-security-review` before suggesting fixes.

## Compact claim and header contract

### Compact trust boundary

- Shared concept: `tenant_id`, `tenant_public_id`, `project_id`, and the compact JWT claim `pid` point at one tenant-boundary concept at the public platform edge.
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
- Validation rule for the public identifier: validate the trusted project boundary as UUIDv7 after gateway verification.
- Example canonical value: `018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- Internal-key rule during migration: if a service still keeps an internal numeric tenant or project key in its own database, treat that key as a service-local storage detail, not as the public boundary contract and not as a replacement for `pid`.
- Documentation rule: OpenAPI, README examples, and service docs should prefer `project_id` for public API fields and `X-Project-Id` for trusted headers. Use `pid` only when the subject is the compact JWT claim map or another gateway-internal trust-boundary detail. If a legacy alias still appears, mark it explicitly as legacy and equivalent to the public tenant boundary.

### JWT claim contract

Standard JWT claims remain unchanged:
- `aud`
- `jti`
- `iat`
- `nbf`
- `exp`
- `sub`
- `scopes`

Custom compact claims:
- `m`
- `prm`
- `prv`
- `av`
- `pid`
- `loc`
- `fn`
- `ln`

Example payload:

```json
{
  "aud": ["3"],
  "jti": "01JQ8Q7QW6YJ7M9X4D3P2K1H8N",
  "iat": 1775296800,
  "nbf": 1775296800,
  "exp": 1775300400,
  "sub": "1001",
  "scopes": [],
  "prm": "AAABgQ",
  "prv": 1,
  "av": 2,
  "m": "09123456789",
  "pid": "018f7d8f-8cb0-7a85-9a89-e3f61052f840",
  "loc": {
    "o": 8,
    "sr": 257,
    "b": 12,
    "sh": 2576,
    "br": 12354,
    "sc": 9988
  },
  "fn": "Sohrab",
  "ln": "Aboozarkhanifard"
}
```

Compact claim meaning table:

| Key | Meaning | Forwarded header |
|---|---|---|
| `m` | mobile | `X-User-Mobile` |
| `prm` | permission bitmap | `X-Access` |
| `prv` | permission catalog version | not forwarded by default |
| `av` | authorization version | not forwarded by default |
| `pid` | public project boundary | `X-Project-Id` |
| `fn` | first name | `X-User-Fname` |
| `ln` | last name | `X-User-Lname` |
| `loc` | location bundle | `X-Location-*` |

`loc` sub-keys:

| Key | Meaning | Forwarded header |
|---|---|---|
| `o` | ostan | `X-Location-Ostan` |
| `sr` | shahrestan | `X-Location-Shahrestan` |
| `b` | bakhsh | `X-Location-Bakhsh` |
| `sh` | shahr | `X-Location-Shahr` |
| `br` | shobe | `X-Location-Shobe` |
| `sc` | school | `X-Location-School` |

### Header contract rules

- The gateway sanitizes client-supplied copies of trusted auth headers before proxying.
- The gateway injects trusted headers only from verified claims.
- Keep one canonical spelling in docs and tests even though HTTP header names are case-insensitive.
- This guide uses `X-Project-Id`, `X-User-Id`, and `X-User-Mobile` as the canonical spellings for the tenant and actor headers.
- `prv` and `av` remain raw JWT metadata only unless a future contract explicitly adds a forwarded use.
- The request-for-change intent remains active:
  - `0` means the source value was null for a location id
  - empty string means the source value was null for a name field
- Gateway rule: do not invent values that are not present in the verified claims. If auth-service emitted the compact sentinel value, forward that value; if the claim is absent, do not fabricate it at the gateway.
- Downstream rule: if auth-service emits compact null sentinels such as empty string for names or `0` for location ids, normalize those sentinels once near ingress instead of spreading raw sentinel handling across the codebase.

## Trusted ingress and auth-service boundary

### Core trust model

- The gateway is the authentication boundary for protected HTTP routes.
- The gateway verifies the Bearer JWT and then injects trusted request headers for downstream services.
- The active request-time checker performs the route-level fine-grained authorization decision.
- Downstream services must still do business authorization and tenant-safe data access after trusted context normalization.
- Client-supplied internal auth headers are never trusted.
- Tenant context is derived from the verified token, not from request body, query string, route params, or client-supplied headers.
- Naming rule: `tenant_id`, `tenant_public_id`, `project_id`, and `pid` refer to the same tenant-boundary concept in the current platform, but they belong to different layers.
- Refactor target standard: rename `tenant_id` and `tenant_public_id` usages to `project_id` at public API or service-domain boundaries and to `pid` only inside compact JWT claim handling.
- Header target standard: rename `X-Tenant-Public-Id` to `X-Project-Id` in service contracts and docs during the platform refactor.
- Until that refactor is complete, treat `tenant_id` and `tenant_public_id` only as legacy aliases of the same trusted boundary and normalize them back to the canonical layer-specific contract: `project_id` in public APIs and `pid` plus `X-Project-Id` in compact JWT and trusted-header handling.

### How auth enters the system

Protected routes:
- Auth enters through `Authorization: Bearer <token>`.
- The gateway extracts the bearer token from the `Authorization` header.
- If a protected route has no bearer token, the gateway returns `401 missing_token`.

Public routes:
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

Important:
- a public path at the gateway does not automatically mean the downstream service should trust the caller
- the downstream service must still apply its own route-level rules
- the gateway must sanitize spoofable inbound auth and context headers on every route, including public routes

### Auth-service route drift that must not be copied forward

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

### Gateway-facing routes vs service-local routes

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

### Auth-service v3 endpoint and client contract

Use this section when the task is specifically about auth-service endpoint behavior, client integration order, direct local backend testing, or the current v3 contract.

For auth-service endpoint details, trust sources in this order:
1. `D:\Sohrab\Project\auth\routes\api.php`
2. `D:\Sohrab\Project\auth\docs\ops\auth-session-contract.md`
3. `D:\Sohrab\Project\auth\docs\ops\auth-profile-v3-contract.md`
4. `D:\Sohrab\Project\auth\docs\ops\totp-step-up-mechanism.md`
5. `D:\Sohrab\Project\auth\docs\ops\postman\auth-service-v3.postman_collection.json`
6. `D:\Sohrab\Project\auth\README.md`

If auth-service docs and route definitions disagree, trust `routes/api.php`.

Canonical gateway-facing client flow:
1. Client calls `POST /auth/api/v3/otp/request` with JSON body:
   ```json
   {
     "mobile": "09120000000",
     "national_code": "1234567890"
   }
   ```
2. Client receives OTP out-of-band.
3. Client calls `POST /auth/api/v3/otp/verify` with JSON body:
   ```json
   {
     "mobile": "09120000000",
     "code": "11111"
   }
   ```
4. Successful verify returns a JSON body with `message`, `profile`, and `token`, where `token.access_token` is the Bearer JWT and `token.token_type` is `Bearer`.
5. The same successful verify call also sets the refresh token in the HttpOnly `auth_refresh_token` cookie.
6. Client calls gateway-protected routes with `Authorization: Bearer <access token>` on the gateway-facing route.
7. Gateway verifies the token and injects trusted headers for downstream services.
8. When the access token expires or is rejected by the gateway, client calls `POST /auth/api/v3/token/refresh`.
9. Successful refresh rotates the refresh token, returns a new access token, and replaces the refresh cookie.
10. Client calls `POST /auth/api/v3/logout` when it wants to revoke the current refresh-token session.

Auth request details from the auth repo and Postman collection:
- OTP request, OTP verify, and refresh requests use `Accept: application/json` and `Content-Type: application/json`.
- The current Postman collection also sends `X-Request-Id` and `X-Device-Id` on those public auth requests.
- `X-Device-Id` is optional client or device metadata for auth-service. It is not a trusted gateway auth header.
- `POST /auth/api/v3/token/refresh` currently expects the refresh token from the HttpOnly `auth_refresh_token` cookie first.
- Refresh request body must include `access_token`, and may include `device_id`.
- Auth-service also accepts device id through the configured device header, currently `X-Device-Id`.
- If `access_token` is missing or not a string-shaped value, refresh returns `422` JSON.
- If the refresh cookie is missing, refresh returns a `401` session-expired style response.
- `POST /auth/api/v3/logout` is currently public in the auth-service contract and can revoke from either `refresh_token` in the request body or the `auth_refresh_token` cookie.
- Do not teach clients to depend on retired `/auth/api/v2/*` auth routes or a one-step `/login` path. The active auth-service contract is the v3 OTP request -> OTP verify flow.

Current protected auth-service route families behind the gateway:
- Gateway-facing protected auth-service routes are:
  - `/auth/api/v3/sessions*`
  - `/auth/api/v3/totp*`
  - `/auth/api/v3/admin/users/{user}/sessions*`
  - `/auth/api/v3/admin/users/{user}/authz-overrides*`
  - `/auth/api/v3/profile*`
- Service-local protected auth-service routes after prefix stripping are:
  - `/api/v3/sessions*`
  - `/api/v3/totp*`
  - `/api/v3/admin/users/{user}/sessions*`
  - `/api/v3/admin/users/{user}/authz-overrides*`
  - `/api/v3/profile*`

Direct local backend testing contract for auth-service:
- The current auth Postman collection tests protected auth-service routes directly against service-local `/api/v3/*` URLs such as `http://localhost/api/v3/sessions`.
- In that direct local mode, Postman sends trusted headers such as `X-User-Id` and `X-Project-Id` to the local backend instead of sending a Bearer token.
- This is backend-only local testing. It is not the public client contract and it must not be copied into browser or mobile client guidance.
- Current auth Postman examples still use numeric compatibility fixtures such as `gatewayProjectId=1` and profile payload examples that show `project_id: 1`.
- Treat those numeric examples as the auth-service local compatibility state and test fixture during migration, not as a reason to weaken the shared gateway trust model or to let clients choose tenant context.

Protected-flow request families that agents should know:

Session management:
- `GET /auth/api/v3/sessions` lists session families for the authenticated user.
- `DELETE /auth/api/v3/sessions/{session}` revokes one session family or access-token session.
- `DELETE /auth/api/v3/sessions` revokes all active sessions for the authenticated user.

TOTP management and step-up:
- `GET /auth/api/v3/totp` returns current TOTP status.
- `POST /auth/api/v3/totp/enroll` starts enrollment.
- `POST /auth/api/v3/totp/confirm` requires JSON body `{ "code": "123456" }`.
- `POST /auth/api/v3/totp/recovery-codes/regenerate` requires JSON body `{ "code": "123456" }`.
- `POST /auth/api/v3/totp/step-up` requires JSON body with `purpose` plus either `code` or `recovery_code`.
- `DELETE /auth/api/v3/totp` requires either `code` or `recovery_code` in the request body.
- Purpose names are free-form but restricted to letters, digits, `.`, `_`, `:`, and `-`.
- Step-up proof is purpose-specific. A proof for `profile.write` does not satisfy `profile.photo`.

Admin authorization overrides:
- `GET /auth/api/v3/admin/users/{user}/authz-overrides` supports optional query filters such as `project_id` and `service_key`.
- `PUT /auth/api/v3/admin/users/{user}/authz-overrides` uses a JSON body shaped like:
  ```json
  {
    "permission_key": "school_post",
    "effect": "deny",
    "project_id": 42,
    "service_key": "auth-profile"
  }
  ```
- `DELETE /auth/api/v3/admin/users/{user}/authz-overrides` uses the same selector fields except `effect`.
- Admin session revocation routes are `DELETE /auth/api/v3/admin/users/{user}/sessions` and `DELETE /auth/api/v3/admin/users/{user}/sessions/{session}`.

Profile reads and writes:
- `GET /auth/api/v3/profile` returns the canonical profile projection.
- `PATCH /auth/api/v3/profile` and `PUT /auth/api/v3/profile` accept sectioned JSON with `identity`, `contact`, `location`, `health`, and `academic` objects.
- The current Postman examples show a representative profile update body that includes `identity.first_name`, `identity.last_name`, `contact.email`, `location.school_id`, `health.blood_type_id`, and `academic.grade_level_id` style fields.
- `GET /auth/api/v3/profile/catalogs`, `GET /auth/api/v3/profile/academic-history`, and `GET /auth/api/v3/profile/assignment-history` are trusted-gateway reads.
- `POST /auth/api/v3/profile/photo`, `POST /auth/api/v3/profile/national-card`, and `GET /auth/api/v3/profile/national-card` are also trusted-gateway routes.

Response and observability facts from the auth repo:
- All `/api/*` routes are JSON-only for both success and error paths.
- Resource responses wrap only the top-level payload in `data`; nested child resources are inline objects.
- The target `/api/*` response-header contract is `X-Request-Id` plus `traceparent`.
- If `X-Request-Id` or a valid inbound `traceparent` is already present from the caller or gateway, auth-service preserves it.
- If auth-service still emits or documents `X-Correlation-Id`, treat that as migration drift to remove, not as a compatibility state to preserve.

### What the gateway verifies

For protected routes, the current gateway logic verifies these checks in order:
1. A bearer token exists.
2. The JWT `alg` value is in the allowlist.
3. The token signature is valid for the mounted public key.
4. The token has a usable `exp` claim.
5. The token is not expired, with configured clock skew.
6. The token is not before `nbf`, with configured clock skew.
7. Required claims are present.
8. Optional issuer and audience checks can run if configured.

Current deployment-specific truth:
- allowed algorithm: `RS256`
- clock skew: `30` seconds
- required claims: `pid` and `sub`
- `iss` validation exists in the template but is not currently enabled because the issuer list is empty
- `aud` validation exists in the template but is not currently enabled because the audience list is empty

What the gateway does not verify:
- it does not do business authorization
- it does not decide whether a user may perform a domain action
- it does not evaluate `X-Access` or `X-USER-SCOPES` for route permission
- it does not derive tenant from hostname, path prefix, body, or query string
- it does not introspect opaque tokens

Important doc drift:
- if any README text still suggests opaque-token passthrough or the old profile-blob header contract, treat that as drift to remove

### Header trust rules

Headers the gateway rejects from client input:
- `X-Project-Id`
- `X-User-Id`
- `X-User-Mobile`
- `X-Access`
- `X-Access-Token-Id`
- `X-TOKEN-CLIENT-ID`
- `X-TOKEN-ISSUED-AT`
- `X-TOKEN-NOT-BEFORE`
- `X-TOKEN-EXPIRES-AT`
- `X-USER-SCOPES`
- `X-User-Fname`
- `X-User-Lname`
- `X-Location-Ostan`
- `X-Location-Shahrestan`
- `X-Location-Bakhsh`
- `X-Location-Shahr`
- `X-Location-Shobe`
- `X-Location-School`

Headers the gateway injects after successful verification:
- `pid` -> `X-Project-Id`
- `sub` -> `X-User-Id`
- `m` -> `X-User-Mobile`
- `prm` -> `X-Access`
- `jti` -> `X-Access-Token-Id`
- `aud` -> `X-TOKEN-CLIENT-ID`
- `iat` -> `X-TOKEN-ISSUED-AT`
- `nbf` -> `X-TOKEN-NOT-BEFORE`
- `exp` -> `X-TOKEN-EXPIRES-AT`
- `scopes` -> `X-USER-SCOPES`
- `fn` -> `X-User-Fname`
- `ln` -> `X-User-Lname`
- `loc.o` -> `X-Location-Ostan`
- `loc.sr` -> `X-Location-Shahrestan`
- `loc.b` -> `X-Location-Bakhsh`
- `loc.sh` -> `X-Location-Shahr`
- `loc.br` -> `X-Location-Shobe`
- `loc.sc` -> `X-Location-School`

Rules:
- only claims that are present are injected
- `prv` and `av` stay out of the forwarded header contract unless a future revision explicitly adds them
- the current forwarded identity and token surface is `X-Project-Id`, `X-User-Id`, `X-User-Mobile`, `X-Access`, `X-Access-Token-Id`, `X-TOKEN-CLIENT-ID`, `X-TOKEN-ISSUED-AT`, `X-TOKEN-NOT-BEFORE`, `X-TOKEN-EXPIRES-AT`, `X-USER-SCOPES`, `X-User-Fname`, `X-User-Lname`, and the `X-Location-*` headers

### Auth-service local trusted header contract

- Auth-service's `trusted_gateway` guard currently consumes only:
  - `X-User-Id`
  - `X-Project-Id`
- Auth-service does not currently read `X-Access`, `X-User-Mobile`, `X-Access-Token-Id`, `X-TOKEN-*`, `X-USER-SCOPES`, or the name and location headers on its protected v3 routes.
- Current auth-service behavior parses trusted `X-User-Id` and `X-Project-Id` as positive integers on protected gateway-backed routes.
- Current auth-service standard no longer requires any extra backend-only signature header on trusted routes. The trust boundary is the sanitized gateway path plus the required injected identity headers.
- Target standard after the current platform decision: the shared gateway boundary carries the compact JWT claims above, while auth-service may keep a separate internal numeric project key during migration.
- Auth-service follow-through rule: do not freeze the current positive-integer header parser into the shared public contract. Translate the trusted public boundary to the internal numeric key at auth-service ingress, or complete the broader model migration later.
- For direct backend testing against auth-service, send the service-local route plus those exact trusted headers. Do not expect auth-service to parse a Bearer token locally on `/api/v3/profile*`, `/api/v3/sessions*`, `/api/v3/totp*`, or admin trusted-gateway routes.

### Other header behavior

- `Authorization` is stripped after successful verification in the current deployment values.
- `X-Request-ID` is preserved if the client already sent one; otherwise the gateway generates one.
- `X-Request-ID` is for tracing only. It is not an auth or tenant header.
- The gateway overwrites `X-Forwarded-Proto` to `https` because TLS terminates upstream.
- The repo does not show equivalent sanitization or re-issuance for `X-Forwarded-For` or `X-Real-IP`.

### Tenant and user context

Tenant context:
- the current tenant context is the compact `pid` claim from the verified JWT
- in this gateway, compact `pid` is required on protected routes
- this is the main tenant boundary header propagated to downstream services as `X-Project-Id`
- `tenant_id` and `tenant_public_id` are legacy names for the same public tenant boundary
- platform refactor target: keep compact `pid` as the JWT claim key, keep `X-Project-Id` as the trusted header, and standardize public and service-facing payloads on `project_id`
- validation rule for the public tenant or project identifier: when a service validates the shared public boundary value, validate it as UUIDv7
- UUIDv7 example for `project_id`: `018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- migration rule for storage-backed services: if a service still keeps an internal numeric tenant or project key, translate the trusted public boundary to that internal key near ingress and keep the internal key out of trusted headers, public API examples, and other public-facing contracts
- API-document rule: service OpenAPI or README examples should use the same UUIDv7 example shape for public `project_id`, and should explain that older names such as `tenant_public_id` map to the same shared concept and are scheduled to be renamed

User identity:
- the current user identity is `sub` from the verified JWT
- it is propagated to downstream services as `X-User-Id`
- some downstream services intentionally allow anonymous or analytics-only traffic; in those services, `X-User-Id` may be absent while `X-Project-Id` is still required
- if the platform decides a given route must always carry an access token, remove that route from the gateway public list instead of teaching downstream services to partially trust missing auth context
- when `X-User-Id` is absent, do not synthesize a trusted actor from client payload fields such as `identity.user_id`, `visitor_id`, `device_id`, or similar client-generated identifiers. If such fields are stored, classify them as untrusted analytics metadata only
- mobile, token id, audience, issue time, not-before time, expiry time, scopes, and permission bitmap are supplemental context, not replacements for server-side authorization rules

Services without a tenant boundary:
- not every gateway-backed service is currently tenant-scoped
- VOD's current header-auth path reads `X-User-Id` and `X-Access`, maps permissions from service-local config, and does not derive tenant context from gateway headers
- target standard: do not invent `project_id` enforcement in a service that has no real tenant boundary just to make documentation look uniform
- if such a service later becomes tenant-aware, add trusted `X-Project-Id` normalization first and then scope reads and writes from that trusted value

What not to do:
- do not derive tenant from a client body field such as `project_id` or `tenant_id` when `X-Project-Id` is already available from the trusted gateway
- do not trust `X-Project-Id` or `X-User-Id` if the service is reachable directly by clients or untrusted internal callers
- do not let route params or query params override the trusted tenant context

## Downstream normalization and authorization

### Network and trust boundary rules

- A service may trust gateway auth headers only if the request came through the trusted edge and sanitized gateway path.
- If a service can be reached directly, it must either block that exposure or strip and reject internal auth headers at its own edge.
- Internal auth headers are hop-by-hop trust artifacts inside your platform, not public API inputs.
- Frontend clients must never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, `X-User-Mobile`, `X-User-Fname`, `X-User-Lname`, or `X-Location-*`.

### Authentication vs authorization

- Treat the gateway as the authentication and context-propagation layer.
- Treat the active request-time checker as the route-level fine-grained authorization layer.
- Treat each downstream service as the business-authorization layer for business actions after trusted context is normalized.
- A verified token plus injected headers does not mean the user may perform the requested operation.
- Legacy migration rule: do not copy older per-request auth-service callback patterns into new gateway-backed services.
- If a legacy `user-token` path must remain temporarily during migration, classify it as a service-specific compatibility path only. Do not document it as the canonical platform auth contract and do not let it weaken gateway-trusted header rules for normal service routes.
- Do not treat allow-side `X-Authz-*` decision metadata as a second authorization system.
- Do not call OpenFGA directly from a normal downstream service unless that repository explicitly owns request-time authorization runtime behavior.

### Laravel Gate and policy flow

- Build the request-scoped actor and tenant context before any framework authorization runs.
- Keep raw gateway-header parsing in middleware or a dedicated request-context layer, not in controllers and not scattered across policies.
- In Laravel services with mixed legacy guard access patterns, resolve the trusted actor once and attach it to every guard and resolver the codebase still reads, such as `Auth::user()`, `$request->user()`, `auth('api')->user()`, or a legacy custom guard.
- If you migrate only one guard while other legacy guard lookups remain, helpers, policies, and controllers can disagree about whether the request is authenticated.
- Use policy or Gate responses to express business authorization decisions after auth context normalization, not as a substitute for gateway verification.
- Compact trusted name and location headers belong to the same one-time normalization layer; do not re-read them in policies or controllers.

### Tenant-safe request handling

- Build request-scoped auth context once near the service edge.
- Normalize at least these fields into a trusted request context object:
  - tenant or project id
  - actor or user id
  - token id when useful for audit
  - request id for trace correlation
  - trusted compact name fields when the service uses them
  - trusted compact location ids when the service uses them
- Authorization code should read the normalized request context or server-side request attributes only. Do not re-read raw tenant or actor headers inside policies, services, or repositories after normalization.
- Laravel Eloquent safety rule: if you attach trusted `project_id` or similar request-scoped auth context directly to a model instance for compatibility, keep it transient and non-dirty immediately or keep that context off the model entirely.
- Auth-service shows one safe compatibility pattern for non-persistent model context: set the trusted attribute for request-time reads, then sync the original attribute so later `save()` calls do not try to persist a gateway-only value into the database.
- HTTP requests without `X-Project-Id` must be rejected with `400`; fallback to the default project id is only allowed for console or queue execution, not normal HTTP traffic.
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.
- If a client-supplied tenant selector in body, query, route, or non-trusted header conflicts with the trusted tenant context, deny explicitly instead of silently choosing one source.
- If a service accepts an extra tenant-shaped identifier for resource lookup, reporting, or local routing, treat it as an untrusted selector until it is matched against the trusted tenant context.
- If a route or service intentionally supports anonymous traffic, make that policy explicit. In that mode, tenant context can still be mandatory while actor context is optional.
- Even in anonymous or analytics flows, never let request-body identity fields override or replace trusted gateway tenant context.
- Do not derive location display names from compact ids unless another explicit contract adds that source of truth.

### Async ingest and accept-then-validate flows

- Some downstream services accept transport with `202 Accepted` and then validate trusted context inside an async pipeline or ingestion worker.
- Plain meaning: `202` means `I received your request and queued or started processing it`. It does not mean auth and tenant validation already succeeded.
- This pattern is common in analytics or ingestion services where the HTTP layer accepts a batch quickly and deeper validation happens in transforms, workers, queues, or sinks after the response is sent.
- Example: a request reaches the service, the HTTP source returns `202`, then a later transform notices that trusted `X-Project-Id` is missing or malformed and drops the data. In that case the transport was accepted, but the business result is still a denial or discard.
- If required trusted context is missing after accept, log a canonical internal code such as `AUTH_CONTEXT_MISSING` or `TENANT_CONTEXT_MISMATCH` and drop, quarantine, or dead-letter the data according to service policy.
- Do not invent a second public `401` or `403` contract after a `202` has already been returned. The caller already received the transport response; the later auth result belongs in logs, metrics, audit events, dead-letter reasons, or operator-facing monitoring.
- If the product needs the client to receive immediate auth failure, do not use accept-then-validate for that route. Move auth or context checks before the `202` response or require the gateway to enforce them earlier.

### Header usage rules

- Use `X-Project-Id` as the public tenant boundary input.
- If a legacy service still exposes `X-Tenant-Public-Id`, treat it as the old name for the same public `project_id` boundary and plan to rename it to `X-Project-Id` during refactor.
- When validating the public tenant boundary value carried in `X-Project-Id`, validate it as UUIDv7.
- Example header value: `X-Project-Id: 018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- If a service still needs an internal numeric project key after validation, derive or load it from the trusted public `X-Project-Id` boundary inside the service and keep that numeric key service-local.
- API-document rule: document `X-Project-Id` with a UUIDv7 example, and if a service still mentions `X-Tenant-Public-Id` or `tenant_public_id`, mark that name as legacy and equivalent to the public `project_id` boundary.
- Use `X-User-Id` as the authenticated actor id.
- Use `X-Access` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-REQUEST-ID` only as correlation.
- Keep one canonical spelling for documentation and tests even though HTTP header names are case-insensitive.
- Treat `X-User-Mobile` as supplemental identity or audit context by default.
- Each downstream service must expose one config switch that decides whether `X-User-Mobile` is optional or required. The default policy should be optional.
- If that config marks mobile as required, the service must enforce it automatically and return the same shared error code and response contract used everywhere else.
- Shared mobile-header contract:
  - when mobile is optional and the header is absent, continue without mobile context
  - when mobile is present but malformed, return `422` with code `AUTH_MOBILE_HEADER_INVALID`
  - when mobile is required but missing or blank, return `401` with code `AUTH_MOBILE_HEADER_MISSING`
  - use one stable response envelope for both cases:
    ```json
    {
      "error": {
        "status": 401,
        "code": "AUTH_MOBILE_HEADER_MISSING",
        "message": "Required user mobile header is missing.",
        "meta": {
          "header": "X-User-Mobile"
        }
      }
    }
    ```
  - invalid-format example:
    ```json
    {
      "error": {
        "status": 422,
        "code": "AUTH_MOBILE_HEADER_INVALID",
        "message": "Invalid user mobile format.",
        "meta": {
          "header": "X-User-Mobile",
          "expected_format": "11 digits starting with 09"
        }
      }
    }
    ```
- Treat `X-User-Fname` and `X-User-Lname` as optional trusted strings.
- Treat every `X-Location-*` header as an optional trusted integer identifier.
- If auth-service emits compact null sentinels such as empty string or `0`, normalize them once near ingress into the repository-owned projection shape instead of leaking raw sentinel handling across the codebase.
- If the headers are absent entirely, do not fabricate them in the service. Normalize that absence consistently in the local projection and document the chosen behavior.
- Keep the trusted projection surface compact and do not invent a second user-context shape.
- Consume the dedicated compact headers directly and keep local projection rules service-owned.
- If a service persists user data, keep the latest user projection in the local `users` read model and keep immutable request-time snapshots only when the domain needs historical or audit context.
- Do not rebuild authorization from raw client headers.

### Permission bitmap and downstream role contract

- `X-Access` carries the gateway-injected copy of auth-service's `prm` permission bitmap claim.
- `X-Access` may carry a compact permission bitmap rather than human-readable scopes.
- The bitmap must be base64url-encoded raw bytes. Permission IDs are 1-based and use least-significant-bit-first packing inside each byte.
- Permission meaning comes from the downstream service's permission map, not from hard-coded bit labels at the gateway.
- Auth-service is the current producer of the bitmap claim and emits companion JWT invalidation metadata under `prv` and `av`.
- Auth-service derives `perm_bm` from `permission_catalog.bit_index`, not from mutable local package table IDs.
- Auth-service compilation precedence is `direct deny > direct allow > role grants`.
- If a downstream service, gateway extension, or debugging tool inspects raw JWT claims instead of injected headers, treat `prv` and `av` as the companion invalidation metadata for `prm`.
- Required decode flow:
  - reject empty or non-base64url values
  - base64url-decode with strict alphabet checking
  - enumerate set bits up to the maximum configured permission id
  - map known ids to permission names from config
  - ignore unknown ids
  - treat the header as invalid if no known permissions remain after mapping
- Comment-service currently uses these permission ids:
  - `18` -> `comment_get`
  - `19` -> `comment_approve`
  - `20` -> `comment_delete`
  - `21` -> `comment_reply`
  - `22` -> `comment_get_show`
- Services must define and document their own role or authorization derivation from decoded permissions.
- Ticket-service currently maps these ids from `X-Access`:
  - `14` -> `crm_get_tickets`
  - `15` -> `crm_post_ticket_reply`
  - `16` -> `crm_put_ticket`
  - `17` -> `crm_post_bulk_ticket`
- VOD keeps its service-local permission-id map in `config/permissions.php`; its current mapped set covers ids `1-13` and `22-39`.
- Laravel compatibility pattern: decode the bitmap once in auth middleware, map ids to permission names from service-local config, attach the mapped names to the request-scoped user object, and let `isAbleTo` or policy checks read those normalized permission names.
- Do not authenticate the actor successfully and then silently continue with an empty decoded permission set on routes that expect permission-bearing context. Fail during trusted-context normalization with canonical code `AUTH_ACCESS_BITMAP_INVALID` so the outward response and deny logs stay specific and consistent.
- Comment-service currently derives roles like this:
  - admin when all configured permissions are present
  - moderator when any moderation signal permission is present
  - student otherwise
- Current example bitmaps from comment-service docs are:
  - `AAAC` for minimal student access
  - `AAAW` for moderator access
  - `AAAe` for admin access
- Reusable reference implementation: `./permission-bitmap.php`
- Do not assume another service uses the same permission ids or role derivation unless that service explicitly adopts that exact mapping.
- The bitmap width is produced by the auth service against the full global permission set, so downstream services should expect a common bitmap width even when each service only cares about a subset of ids.
- Ticket-service shows a common legacy failure mode: decode `X-Access`, map known ids from config, and if nothing valid remains, let the request continue until a later generic `unauthorized` or `access_denied` path fires.
- Target standard: do not defer malformed or unknown-only bitmap failures to later generic auth checks. Fail during trusted-context normalization with canonical code `AUTH_ACCESS_BITMAP_INVALID` so the outward response and deny logs stay specific and consistent.

### Logging and observability

- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
- Preserve inbound `traceparent`, `tracestate`, and `baggage` across HTTP boundaries. On async boundaries, forward `traceparent` and `tracestate`, and only forward baggage keys that were explicitly reviewed as safe.
- If a service maps an internal policy decision to a route-specific outward deny code, the API response `code` and the emitted deny log `code` must stay identical.
- When auth context is missing or malformed, make the denial observable.

## Error contract, review checklist, and anti-patterns

Use this section as the standard contract for auth and token-related deny responses and logs across downstream services.

This contract is intentionally aligned with `alaa-observability-soc`:
- response codes must be stable
- logs must repeat the same stable `code`
- logs must include request correlation and safe auth context
- messages must stay user-safe and not leak verifier internals

### Contract rules

- Use a stable machine-readable `code` in both the API response and logs.
- Use a short user-facing `message` in English.
- Keep `meta` safe and small.
- Do not put raw tokens, full JWT payloads, secrets, stack traces, or key material in response or logs.
- Prefer one canonical code per auth failure class across services.
- If a downstream service translates a gateway denial, preserve the same semantic code instead of inventing a new synonym.
- A service may keep internal policy or framework deny labels, but the final outward response `code` and deny-log `code` must match exactly.

### Recommended response envelope

```json
{
  "error": {
    "status": 401,
    "code": "AUTH_MISSING_TOKEN",
    "message": "Access token is required.",
    "meta": {}
  }
}
```

### Recommended log fields for auth denies

At minimum log:
- `code`
- `message` or `reason`
- `http.status`
- `request_id`
- `project_id` when known
- `user_id` when known
- `token_jti` when known
- `route` or normalized path
- `auth_source` such as `gateway` or `service`

### Canonical auth and token codes

Use these codes by default unless an existing production contract already forces a different stable value:

- `AUTH_MISSING_TOKEN`
  - HTTP: `401`
  - Meaning: protected route has no usable bearer token

- `AUTH_INVALID_TOKEN`
  - HTTP: `401`
  - Meaning: token exists but cannot be accepted
  - Use when the service should not expose a narrower verifier reason to callers

- `AUTH_TOKEN_EXPIRED`
  - HTTP: `401`
  - Meaning: token is expired

- `AUTH_TOKEN_NOT_YET_VALID`
  - HTTP: `401`
  - Meaning: token `nbf` is in the future

- `AUTH_INVALID_SIGNATURE`
  - HTTP: `401`
  - Meaning: signature verification failed
  - Gateway note: this is the class currently promoted to higher-severity forwarding in gateway logs

- `AUTH_DISALLOWED_ALG`
  - HTTP: `401`
  - Meaning: JWT algorithm is not allowed

- `AUTH_BAD_ISSUER`
  - HTTP: `401`
  - Meaning: issuer is invalid for this verifier

- `AUTH_BAD_AUDIENCE`
  - HTTP: `401`
  - Meaning: audience is invalid for this verifier

- `AUTH_MISSING_REQUIRED_CLAIM`
  - HTTP: `401`
  - Meaning: one required token claim is missing
  - `meta.claim` may contain a safe claim name such as `pid` or `sub`

- `AUTH_CONTEXT_MISSING`
  - HTTP: `401` or `403` depending on service policy
  - Meaning: the downstream service expected trusted gateway context but did not receive enough of it

- `AUTH_ACCESS_HEADER_MISSING`
  - HTTP: `401`
  - Meaning: downstream trusted context expected `X-Access`, but it was missing or blank

- `AUTH_ACCESS_BITMAP_INVALID`
  - HTTP: `401`
  - Meaning: `X-Access` exists but is not a valid supported base64url permission bitmap, or it maps to no known permissions for that service

- `AUTH_ROLE_RESOLUTION_FAILED`
  - HTTP: `401`
  - Meaning: the service decoded permission context but could not derive its internal role or permission tier

- `AUTH_MOBILE_HEADER_MISSING`
  - HTTP: `401`
  - Meaning: the service configuration requires `X-User-Mobile`, but the header is missing or blank

- `AUTH_MOBILE_HEADER_INVALID`
  - HTTP: `422`
  - Meaning: `X-User-Mobile` is present but malformed for the service contract

- `AUTH_NAME_OR_LOCATION_HEADER_INVALID`
  - HTTP: `400`
  - Meaning: one of the trusted name or location headers is malformed or violates the compact gateway contract

- `AUTH_NAME_OR_LOCATION_HEADER_REQUIRED`
  - HTTP: `400`
  - Meaning: the route or operation explicitly requires trusted compact identity headers, but one or more were missing or blank

- `AUTHZ_DENIED`
  - HTTP: `403`
  - Meaning: caller is authenticated but not allowed to perform the requested action

- `TENANT_CONTEXT_MISMATCH`
  - HTTP: `403`
  - Meaning: trusted tenant context and requested target do not match

- `TENANT_CONTEXT_MISSING`
  - HTTP: `401` or `403` depending on service policy
  - Meaning: tenant-safe operation could not proceed because trusted tenant context is absent

- `TENANT_CONTEXT_INVALID`
  - HTTP: `403`
  - Meaning: client-supplied tenant selectors or tenant-shaped headers conflict with trusted tenant context, or the service detected an invalid tenant-override attempt

### Mapping from current gateway error names

The gateway currently emits lower-level names such as:
- `missing_token`
- `disallowed_alg`
- `invalid_signature`
- `verify_error`
- `missing_exp`
- `expired`
- `not_yet_valid`
- `bad_issuer`
- `bad_audience`
- `missing_claim_<claim>`

When a downstream service needs to log or surface the same problem in its own contract, map them like this:
- `missing_token` -> `AUTH_MISSING_TOKEN`
- `disallowed_alg` -> `AUTH_DISALLOWED_ALG`
- `invalid_signature` -> `AUTH_INVALID_SIGNATURE`
- `verify_error` -> `AUTH_INVALID_TOKEN`
- `missing_exp` -> `AUTH_INVALID_TOKEN`
- `expired` -> `AUTH_TOKEN_EXPIRED`
- `not_yet_valid` -> `AUTH_TOKEN_NOT_YET_VALID`
- `bad_issuer` -> `AUTH_BAD_ISSUER`
- `bad_audience` -> `AUTH_BAD_AUDIENCE`
- `missing_claim_<claim>` -> `AUTH_MISSING_REQUIRED_CLAIM`

Important:
- do not collapse downstream header-validation failures into gateway verifier failures
- `AUTH_ACCESS_BITMAP_INVALID` and `AUTH_ROLE_RESOLUTION_FAILED` happen after gateway verification, inside the downstream service's trusted-context normalization layer

### Async transport note for canonical codes

- For accept-then-validate services, keep the public transport contract and the internal auth result separate.
- If the HTTP layer already returned `202`, use canonical codes such as `AUTH_CONTEXT_MISSING`, `TENANT_CONTEXT_MISSING`, or `TENANT_CONTEXT_MISMATCH` in logs, metrics, dead-letter reasons, or audit events instead of trying to send a later public auth response.

### Guidance for future backend harmonization

- In the first step, new services and changed services should adopt these codes for auth and token failures.
- In the second step, existing services can be migrated gradually by adding the canonical code to logs first, then aligning response payloads.
- If a service already has a deployed response contract, prefer additive migration over breaking changes.

Before using the checklists below, confirm that all relevant companion skills have already been read for the current task. The checklists assume that gateway trust rules from this skill and implementation or deployment rules from the companion skill set are both in scope.

### Service implementation checklist

Use this checklist when adapting a downstream service to this trust model:
1. Confirm the service is not directly exposed to untrusted traffic, or add header stripping at the service edge.
2. Create one request-scoped auth context builder near ingress or middleware.
3. Read tenant from `X-Project-Id` and actor from `X-User-Id`.
4. If the service still uses legacy names such as `tenant_id`, `tenant_public_id`, or `X-Tenant-Public-Id`, map them to `project_id` as part of the refactor plan and keep the trust semantics unchanged.
5. Validate the public tenant boundary value as UUIDv7 when that value is exposed in service contracts, and if the service still keeps an internal numeric key, translate after that validation instead of replacing the public boundary contract.
6. Reject protected requests if trusted tenant context is missing, and reject missing actor context when the route or service policy requires an authenticated actor.
7. When a route or write path consumes trusted compact identity headers, normalize the trusted name and location headers once, keep the latest local user projection separate from immutable request-time snapshots, and use `AUTH_NAME_OR_LOCATION_HEADER_REQUIRED` only for routes that intentionally force trusted identity presence.
8. Keep authorization in service-layer policies or domain logic, not in controllers and not in reverse-proxy assumptions.
9. Deny client tenant-override attempts explicitly instead of silently preferring one tenant source.
10. Scope every tenant-aware query or command by the trusted tenant context.
11. Keep deny response codes and deny log codes aligned, with request and trace correlation attached.
12. Add tests for spoofed headers, missing tenant context, malformed compact identity headers, cross-tenant access attempts, conflicting tenant selectors, and any route that intentionally allows anonymous traffic.

### Review checklist for agents

Flag a problem when you see any of these:
- A service trusts `X-Project-Id` or `X-User-Id` on a public endpoint without a trusted proxy boundary.
- A service accepts tenant id from request body or route and lets it override gateway context.
- Business authorization is missing because the team assumed the gateway already handled it.
- A direct service exposure lets clients send internal auth headers.
- Raw tokens are logged.
- Request-scoped auth or tenant context can leak across requests.
- A service depends on opaque-token behavior that the current gateway does not implement.
- A backend service is documented with gateway-facing routes even though the gateway strips its service prefix before proxying.
- A service documents a header rule that the code does not actually enforce yet.
- A permission middleware or authorization wrapper contains a temporary early return or bypass ahead of the real checks, effectively disabling authorization while requests still look authenticated.
- Different services use different auth failure codes for the same deny class without a compatibility reason.
- A service accepts conflicting client-supplied tenant selectors and trusted tenant context without an explicit deny.
- A service treats the compact identity headers as client-provided or gateway-decoded values instead of the exact values copied from the verified token.
- A service stores historical identity snapshots but fails to refresh the latest local user projection from the trusted gateway payload.
- A service keeps documenting `tenant_id`, `tenant_public_id`, or `X-Tenant-Public-Id` as if they were different concepts instead of a legacy alias scheduled to be renamed to `project_id` and `X-Project-Id`.
- A service derives `tenant_id` or `project_id` from request body fields before trusted `X-Project-Id`.
- A service upgrades payload identity such as `identity.user_id`, `visitor_id`, or `device_id` into trusted actor context when `X-User-Id` is missing.
- A team treats async `202 Accepted` transport as proof that trusted auth or tenant validation succeeded.

### Laravel and Octane guidance

- In Laravel services, parse trusted gateway headers once in middleware or a dedicated request-context layer, then pass normalized context into services and policies.
- Keep controllers thin. Authorization belongs in Policies, Gates, or service-layer domain checks.
- If a Laravel compatibility layer temporarily attaches trusted gateway context to an Eloquent user model, keep that attribute request-scoped only and prevent dirty persistence of non-column values.
- Auth-service currently uses request-scoped trusted tenant context and syncs it into the model only for protected request-time reads so later saves do not try to persist a gateway-only attribute into the database.
- In Octane or other long-lived workers, auth and tenant context must be strictly request-scoped and reset every request.

### Related skills and required read order

These are not optional background references. They are required companion reads when the task enters their scope.

- `alaa-security-review`
  - Read before reviewing or changing JWT verification, token handling, header trust, tenant isolation, authn or authz controls, or abuse-resistant auth behavior.
- `alaa-laravel-architecture`
  - Read before changing Laravel middleware, guards, Policies, Gates, service-layer authorization, request-context normalization, DTO boundaries, or auth-related response contracts.
- `alaa-php-clean-code`
  - Read before writing or refactoring PHP or Laravel code in gateway-aware middleware, guards, request-context builders, DTOs, services, or auth-facing response mappers so the code follows the shared clean-code, pattern, type-safety, and Laravel best-practice baseline.
- `alaa-octane-performance`
  - Read before changing auth or tenant-context handling in Octane or any long-lived worker environment, or when auth middleware sits on a hot path.
- `alaa-observability-soc`
  - Read before changing auth error codes, deny logging, request correlation, `X-Request-Id`, `traceparent`, full removal of `X-Correlation-Id`, or SOC-facing auth event behavior.
- `alaa-docker-production`
  - Read before changing trusted proxy boundaries, direct service exposure, container networking, or `X-Forwarded-*` handling at deployment or runtime edges.
- `alaa-haproxy`
  - Read before changing gateway ACLs, header sanitization or injection, path-prefix stripping, JWT verification order, public versus protected route behavior, or HAProxy-side auth enforcement.
- `caas-arvan-kuber`
  - Read before changing Arvan or Kubernetes exposure mode, ingress versus load balancer entrypoints, or any public-entry trust boundary in Arvan environments.

Routing rule:
- If a task matches any bullet above, read that companion skill before proceeding.
- If a task matches more than one bullet, read all matching skills before proceeding.
- If a task does not match any bullet, stay with this skill and the target repository's local docs or code.

### Anti-patterns

- Trusting internal auth headers on directly exposed services.
- Letting request body, route params, or query params override trusted tenant context.
- Treating gateway authentication as full authorization.
- Spreading raw header reads across the codebase instead of normalizing them once.
- Treating the compact identity headers as raw data instead of copied verified claims.
- Silently accepting a client tenant selector that conflicts with trusted tenant context.
- Treating `tenant_id`, `tenant_public_id`, and `project_id` as different tenant-boundary concepts when they are supposed to be one shared concept under the public boundary name.
- Logging raw access tokens.
- Assuming README design notes are more accurate than active HAProxy config.
- Applying this skill in isolation when the task clearly also requires one or more companion skills.
