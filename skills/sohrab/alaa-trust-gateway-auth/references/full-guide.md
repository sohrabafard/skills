# Purpose
Use this skill when a service lives behind the Ala gateway, or when a change touches auth headers, tenant context, reverse-proxy trust, or request identity propagation.

This skill gives one clear trust model so agents do not guess.

# When to use
- Building or reviewing a downstream service behind the gateway
- Adding middleware that reads user or tenant context from headers
- Debugging auth failures, tenant mismatch, or missing headers
- Changing gateway config, ingress behavior, trusted proxy settings, or service exposure
- Reviewing whether a service is safe to expose directly or must stay behind the gateway

# Companion skill routing (mandatory)
Read this skill first for any gateway-backed auth, trusted-header, tenant-context, or downstream trust-boundary task.

This skill defines the shared trust model. It does not replace the domain-specific companion skills below.

Before proposing code or config changes, the agent must identify which companion skill(s) apply to the current task and read them before continuing.

Mandatory routing rules:
- If the task touches JWT correctness, token verification, authn/authz risk, header trust, tenant-isolation risk, or token-handling mistakes, read `alaa-security-review` first.
- If the task touches Laravel middleware, guards, request-context builders, Policies, Gates, controllers, services, DTO boundaries, response envelopes, or PHP/Laravel clean-code decisions inside those files, read `alaa-laravel-architecture` and `alaa-php-clean-code` first.
- If the task touches Octane, long-lived workers, request-scoped auth state, tenant-context reset, or performance-sensitive auth middleware, read `alaa-octane-performance` first.
- If the task touches deny logging, request correlation, trace propagation, security events, or auth error observability, read `alaa-observability-soc` first.
- If the task touches trusted proxy boundaries, direct service exposure, container networking, edge-only exposure, or `X-Forwarded-*` behavior, read `alaa-docker-production` first.
- If the task touches HAProxy ACL order, JWT verification behavior, header mutation, path stripping, route exposure, or gateway-side auth flow, read `alaa-haproxy` first.
- If the task touches Arvan/Kubernetes entrypoints, ingress vs load balancer exposure, edge trust boundaries, or public service exposure on Arvan, read `caas-arvan-kuber` first.

Do not continue with implementation advice until the relevant companion skill has been read.
If multiple areas apply, read all relevant companion skills and follow the stricter rule when they overlap.

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

# Canonical rename plan
- Shared concept: `tenant_id`, `tenant_public_id`, and `project_id` point at one tenant-boundary concept at the public platform edge.
- Canonical public field name: `project_id`
- Canonical trusted header name: `X-PROJECT-ID`
- Legacy names to rename during refactor:
  - `tenant_id` -> `project_id`
  - `tenant_public_id` -> `project_id`
  - `X-Tenant-Public-Id` -> `X-PROJECT-ID`
- Migration rule: keep trust semantics unchanged while renaming. Only the public boundary name changes; the boundary meaning does not.
- Validation rule for the public identifier: validate canonical `project_id` values as UUIDv7.
- Example canonical value: `018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- Internal-key rule during migration: if a service still keeps an internal numeric tenant or project key in its own database, treat that key as a service-local storage detail, not as the public boundary contract and not as a replacement for `project_id`.
- Documentation rule: OpenAPI, README examples, and service docs should prefer `project_id` / `X-PROJECT-ID`. If a legacy alias still appears, mark it explicitly as legacy and equivalent to the public `project_id` boundary.

# Core trust model
- The gateway is the authentication boundary for protected HTTP routes.
- The gateway verifies the Bearer JWT and then injects trusted request headers for downstream services.
- Downstream services must still do authorization and tenant-safe data access.
- Client-supplied internal auth headers are never trusted.
- Tenant context is derived from the verified token, not from request body, query string, route params, or client-supplied headers.
- Naming rule: `tenant_id`, `tenant_public_id`, and `project_id` refer to the same tenant-boundary concept in the current platform.
- Refactor target standard: rename `tenant_id` and `tenant_public_id` usages to `project_id` wherever the field represents the shared tenant boundary.
- Header target standard: rename `X-Tenant-Public-Id` to `X-PROJECT-ID` in service contracts and docs during the platform refactor.
- Until that refactor is complete, treat `tenant_id` and `tenant_public_id` only as legacy aliases of the same trusted boundary and normalize them back to the canonical gateway-derived `project_id` / `X-PROJECT-ID` contract.

# How auth enters the system
## Protected routes
- Auth enters through `Authorization: Bearer <token>`.
- The gateway extracts the bearer token from the `Authorization` header.
- If a protected route has no bearer token, the gateway returns `401 missing_token`.

## Public routes
The current gateway config marks these paths as public and skips JWT checks for them:
- `/auth/api/v2/login`
- `/auth/api/v2/otp/request`
- `/auth/api/v2/otp/verify`
- `/auth/api/v2/token/refresh`
- `/auth/api/v2/logout`
- `/auth/api/health`
- `/vod/api/health`
- `/comment/api/health`
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
- If the gateway still exposes `/auth/api/v2/*` for auth, treat that as gateway drift to remove. Do not reintroduce `/api/v2` into auth-service and do not teach new services to depend on retired auth v2 routes.

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

# Auth-service v3 endpoint and client contract
Use this section when the task is specifically about auth-service endpoint behavior, client integration order, direct local backend testing, or the current v3 contract.

For auth-service endpoint details, trust sources in this order:
1. `D:\Sohrab\Project\auth\routes\api.php`
2. `D:\Sohrab\Project\auth\docs\ops\auth-session-contract.md`
3. `D:\Sohrab\Project\auth\docs\ops\auth-profile-v3-contract.md`
4. `D:\Sohrab\Project\auth\docs\ops\totp-step-up-mechanism.md`
5. `D:\Sohrab\Project\auth\docs\ops\postman\auth-service-v3.postman_collection.json`
6. `D:\Sohrab\Project\auth\README.md`

If auth-service docs and route definitions disagree, trust `routes/api.php`.

## Canonical gateway-facing client flow
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

## Auth request details from the auth repo and Postman collection
- OTP request, OTP verify, and refresh requests use `Accept: application/json` and `Content-Type: application/json`.
- The current Postman collection also sends `X-Request-Id` and `X-Device-Id` on those public auth requests.
- `X-Device-Id` is optional client/device metadata for auth-service. It is not a trusted gateway auth header.
- `POST /auth/api/v3/token/refresh` currently expects the refresh token from the HttpOnly `auth_refresh_token` cookie first.
- Refresh request body must include `access_token`, and may include `device_id`.
- Auth-service also accepts device id through the configured device header, currently `X-Device-Id`.
- If `access_token` is missing or not a string-shaped value, refresh returns `422` JSON.
- If the refresh cookie is missing, refresh returns a `401` session-expired style response.
- `POST /auth/api/v3/logout` is currently public in the auth-service contract and can revoke from either `refresh_token` in the request body or the `auth_refresh_token` cookie.
- Do not teach clients to depend on retired `/auth/api/v2/*` auth routes or a one-step `/login` path. The active auth-service contract is the v3 OTP request -> OTP verify flow.

## Current protected auth-service route families behind the gateway
Gateway-facing protected auth-service routes are:
- `/auth/api/v3/sessions*`
- `/auth/api/v3/totp*`
- `/auth/api/v3/admin/users/{user}/sessions*`
- `/auth/api/v3/admin/users/{user}/authz-overrides*`
- `/auth/api/v3/profile*`

Service-local protected auth-service routes after prefix stripping are:
- `/api/v3/sessions*`
- `/api/v3/totp*`
- `/api/v3/admin/users/{user}/sessions*`
- `/api/v3/admin/users/{user}/authz-overrides*`
- `/api/v3/profile*`

## Direct local backend testing contract for auth-service
- The current auth Postman collection tests protected auth-service routes directly against service-local `/api/v3/*` URLs such as `http://localhost/api/v3/sessions`.
- In that direct local mode, Postman sends trusted headers such as `X-USER-ID` and `X-PROJECT-ID` to the local backend instead of sending a Bearer token.
- This is backend-only local testing. It is not the public client contract and it must not be copied into browser/mobile client guidance.
- Current auth Postman examples still use numeric compatibility fixtures such as `gatewayProjectId=1` and profile payload examples that show `project_id: 1`.
- Treat those numeric examples as the auth-service local compatibility state and test fixture during migration, not as a reason to weaken the shared gateway trust model or to let clients choose tenant context.

## Protected-flow request families that agents should know
### Session management
- `GET /auth/api/v3/sessions` lists session families for the authenticated user.
- `DELETE /auth/api/v3/sessions/{session}` revokes one session family or access-token session.
- `DELETE /auth/api/v3/sessions` revokes all active sessions for the authenticated user.

### TOTP management and step-up
- `GET /auth/api/v3/totp` returns current TOTP status.
- `POST /auth/api/v3/totp/enroll` starts enrollment.
- `POST /auth/api/v3/totp/confirm` requires JSON body `{ "code": "123456" }`.
- `POST /auth/api/v3/totp/recovery-codes/regenerate` requires JSON body `{ "code": "123456" }`.
- `POST /auth/api/v3/totp/step-up` requires JSON body with `purpose` plus either `code` or `recovery_code`.
- `DELETE /auth/api/v3/totp` requires either `code` or `recovery_code` in the request body.
- Purpose names are free-form but restricted to letters, digits, `.`, `_`, `:`, and `-`.
- Step-up proof is purpose-specific. A proof for `profile.write` does not satisfy `profile.photo`.

### Admin authorization overrides
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

### Profile reads and writes
- `GET /auth/api/v3/profile` returns the canonical profile projection.
- `PATCH /auth/api/v3/profile` and `PUT /auth/api/v3/profile` accept sectioned JSON with `identity`, `contact`, `location`, `health`, and `academic` objects.
- The current Postman examples show a representative profile update body that includes `identity.first_name`, `identity.last_name`, `contact.email`, `location.school_id`, `health.blood_type_id`, and `academic.grade_level_id` style fields.
- `GET /auth/api/v3/profile/catalogs`, `GET /auth/api/v3/profile/academic-history`, and `GET /auth/api/v3/profile/assignment-history` are trusted-gateway reads.
- `POST /auth/api/v3/profile/photo`, `POST /auth/api/v3/profile/national-card`, and `GET /auth/api/v3/profile/national-card` are also trusted-gateway routes.

## Response and observability facts from the auth repo
- All `/api/*` routes are JSON-only for both success and error paths.
- Resource responses wrap only the top-level payload in `data`; nested child resources are inline objects.
- `/api/*` responses include `X-Request-Id`, `X-Correlation-Id`, and `traceparent`.
- If `X-Request-Id` or `X-Correlation-Id` is already present from the caller or gateway, auth-service preserves it.

# What the gateway verifies
For protected routes, the current HAProxy logic verifies these checks in order:
1. A bearer token exists.
2. The JWT `alg` value is in the allowlist.
3. The token signature is valid for the mounted public key.
4. The token has a usable `exp` claim.
5. The token is not expired, with configured clock skew.
6. The token is not before `nbf`, with configured clock skew.
7. Required claims are present.
8. Optional issuer and audience checks can run if configured.

## Current deployment-specific truth
From the current values used by this repo:
- Allowed algorithm: `RS256`
- Clock skew: `30` seconds
- Required claims: `project_id` and `sub`
- `iss` validation exists in the template but is not currently enabled because the issuer list is empty
- `aud` validation exists in the template but is not currently enabled because the audience list is empty

## What the gateway does not verify
- It does not do business authorization.
- It does not decide whether a user may perform a domain action.
- It does not evaluate `X-ACCESS` or `X-USER-SCOPES` for route permission.
- It does not derive tenant from hostname, path prefix, body, or query string.
- It does not introspect opaque tokens.

## Important doc drift
The README mentions an opaque-token fallback idea, but the active HAProxy config does not implement pass-through for opaque access tokens. In practice, this gateway is configured for JWT verification, not opaque-token introspection.

# Header trust rules
## Headers the gateway rejects from client input
Before any auth context is injected, the gateway deletes these incoming headers to stop spoofing. This sanitize step must run on all routes, including public routes that do not receive injected auth context:
- `X-PROJECT-ID`
- `X-USER-ID`
- `X-USER-MOBILE`
- `X-ACCESS`
- `X-ACCESS-TOKEN-ID`
- `X-TOKEN-CLIENT-ID`
- `X-TOKEN-ISSUED-AT`
- `X-TOKEN-NOT-BEFORE`
- `X-TOKEN-EXPIRES-AT`
- `X-USER-SCOPES`
- `X-PROFILE`

This means downstream services must treat these names as trusted only when they were added by the gateway, not when they arrive from an untrusted caller.

## Headers the gateway injects after successful verification
The current mapping is:
- `project_id` -> `X-PROJECT-ID`
- `sub` -> `X-USER-ID`
- `mobile` -> `X-USER-MOBILE`
- `perm_bm` -> `X-ACCESS`
- `jti` -> `X-ACCESS-TOKEN-ID`
- `aud` -> `X-TOKEN-CLIENT-ID`
- `iat` -> `X-TOKEN-ISSUED-AT`
- `nbf` -> `X-TOKEN-NOT-BEFORE`
- `exp` -> `X-TOKEN-EXPIRES-AT`
- `scopes` -> `X-USER-SCOPES`
- `profile` -> `X-PROFILE`

Only claims that are present are injected.

## X-Profile profile propagation contract
- Auth-service is the source of truth for the latest user profile.
- Auth-service must emit JWT claim `profile` when trusted downstream services need profile context.
- The `profile` claim value must be a base64url-encoded UTF-8 JSON object whose canonical keys are `first_name`, `last_name`, and `shahr` when they are present.
  ```json
  {
    "first_name": null,
    "last_name": null,
    "shahr": null
  }
  ```
- Auth-service should omit any key whose value is `null`, and it may omit the entire `profile` claim when all three canonical fields are `null`.
- Gateway must strip any inbound `X-PROFILE` / `X-Profile`, verify the token, and if the verified token has a `profile` claim, copy that exact claim value into `X-PROFILE`.
- Gateway must not decode, reshape, normalize, or re-encode the `profile` claim before forwarding it.
- If the verified token has no `profile` claim, the gateway must not fabricate `X-PROFILE`.
- Downstream services that need profile data must base64url-decode `X-Profile`, JSON-decode the UTF-8 payload, require a JSON object, and normalize each canonical field independently: missing key => `null`, explicit JSON `null` => `null`, trimmed empty string => `null`, non-empty string => keep, non-string non-null => `AUTH_PROFILE_HEADER_INVALID`.
- Downstream services may store immutable request-time snapshots for historical or audit purposes, but their local `users` projection should always hold the latest profile state known from auth-service.
- Source-of-truth rule: auth-service always owns the latest profile state. Downstream services may cache or project it locally, but they must not treat their local copy as the source of truth.
## Auth-service local trusted header contract
- Auth-service's `trusted_gateway` guard currently consumes only:
  - `X-USER-ID`
  - `X-PROJECT-ID`
- Auth-service does not currently read `X-ACCESS`, `X-USER-SCOPES`, `X-USER-MOBILE`, or token-metadata headers on its protected v3 routes.
- Current auth-service behavior currently parses trusted `X-USER-ID` and `X-PROJECT-ID` as positive integers on protected gateway-backed routes.
- Current auth-service standard no longer requires any extra backend-only signature header on trusted routes. The trust boundary is the sanitized gateway path plus the required injected identity headers.
- Target standard after the current platform decision: the shared gateway boundary still carries public UUIDv7 `project_id` in JWTs and `X-PROJECT-ID`, while auth-service may keep a separate internal numeric project key during migration.
- Auth-service follow-through rule: do not freeze the current positive-integer header parser into the shared public contract. Translate the trusted public `project_id` boundary to the internal numeric key at auth-service ingress, or complete the broader model migration later.
- For direct backend testing against auth-service, send the service-local route plus those exact trusted headers. Do not expect auth-service to parse a Bearer token locally on `/api/v3/profile*`, `/api/v3/sessions*`, `/api/v3/totp*`, or admin trusted-gateway routes.

## Other header behavior
- `Authorization` is stripped after successful verification in the current deployment values.
- `X-Request-ID` is preserved if the client already sent one; otherwise the gateway generates one.
- `X-Request-ID` is for tracing only. It is not an auth or tenant header.
- The gateway overwrites `X-Forwarded-Proto` to `https` because TLS terminates upstream.
- The repo does not show equivalent sanitization or re-issuance for `X-Forwarded-For` or `X-Real-IP`.

# Tenant and user context
## Tenant context
- The current tenant context is the public `project_id` claim from the verified JWT.
- In this gateway, public `project_id` is required on protected routes.
- This is the main tenant boundary header propagated to downstream services as `X-PROJECT-ID`.
- `tenant_id` and `tenant_public_id` are not different security concepts here. They are legacy names for the same public tenant boundary.
- Platform refactor target: standardize shared gateway and service contracts on public `project_id` / `X-PROJECT-ID`, and rename legacy `tenant_id`, `tenant_public_id`, and `X-Tenant-Public-Id` usages to that standard.
- Validation rule for the public tenant/project identifier: when a service validates the shared public tenant boundary value, validate it as UUIDv7.
- UUIDv7 example for `project_id`: `018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- Migration rule for storage-backed services: if a service still keeps an internal numeric tenant or project key, translate the trusted public `project_id` boundary to that internal key near ingress and keep the internal key out of public headers, public tokens, and public API examples.
- Auth-service is the current explicit case for this split: public gateway boundary should stay UUIDv7, while auth-service may still keep an internal numeric project key until the local model is migrated.
- API-document rule: service OpenAPI or README examples should use the same UUIDv7 example shape for public `project_id`, and should explain that older names such as `tenant_public_id` map to the same shared concept and are scheduled to be renamed.

## User identity
- The current user identity is `sub` from the verified JWT.
- It is propagated to downstream services as `X-USER-ID`.
- Some downstream services intentionally allow anonymous or analytics-only traffic. In those services, `X-USER-ID` may be absent while `X-PROJECT-ID` is still required.
- If the platform decides a given route must always carry an access token, remove that route from the gateway public list instead of teaching downstream services to partially trust missing auth context.
- When `X-USER-ID` is absent, do not synthesize a trusted actor from client payload fields such as `identity.user_id`, `visitor_id`, `device_id`, or similar client-generated identifiers. If such fields are stored, classify them as untrusted analytics metadata only.
- Mobile, token id, audience, issue time, not-before time, expiry time, scopes, and permission bitmap are supplemental context, not replacements for server-side authorization rules.

## Services without a tenant boundary
- Not every gateway-backed service is currently tenant-scoped.
- VOD's current header-auth path reads `X-USER-ID` and `X-ACCESS`, maps permissions from service-local config, and does not derive tenant context from gateway headers.
- Target standard: do not invent `project_id` enforcement in a service that has no real tenant boundary just to make documentation look uniform.
- If such a service later becomes tenant-aware, add trusted `X-PROJECT-ID` normalization first and then scope reads and writes from that trusted value.

## What not to do
- Do not derive tenant from a client body field such as `project_id` or `tenant_id` when `X-PROJECT-ID` is already available from the trusted gateway.
- Do not trust `X-PROJECT-ID` or `X-USER-ID` if the service is reachable directly by clients or untrusted internal callers.
- Do not let route params or query params override the trusted tenant context.

# What downstream services must do
## Network and trust boundary rules
- A service may trust gateway auth headers only if the request came through the trusted edge and gateway path.
- If a service can be reached directly, it must either block that exposure or strip and reject internal auth headers at its own edge.
- Internal auth headers are hop-by-hop trust artifacts inside your platform, not public API inputs.

## Authentication vs authorization
- Treat the gateway as the authentication and context-propagation layer.
- Treat each downstream service as the authorization layer for business actions.
- A verified token plus injected headers does not mean the user may perform the requested operation.
- Legacy migration rule: do not copy older per-request auth-service callback patterns into new gateway-backed services.
- Ticket-service still contains legacy internal route groups that accept a separate `user-token` header and call auth-service endpoints such as `/api/v2/checkUserAccess` and `/api/v2/authorizeWithPermissionName` on each request.
- Target standard: for services behind the gateway, replace that pattern with gateway-verified Bearer JWT flow, trusted `X-*` header normalization once at ingress, and local authorization inside the service.
- If a legacy `user-token` path must remain temporarily during migration, classify it as a service-specific compatibility path only. Do not document it as the canonical platform auth contract and do not let it weaken gateway-trusted header rules for normal service routes.

## Laravel Gate and policy flow
- Build the request-scoped actor and tenant context before any framework authorization runs.
- In comment-service, `ResolveUserMiddleware` builds a lightweight authenticated user from trusted headers, service classes call `Gate::forUser($user)->authorize(...)`, and policies return domain-specific deny codes.
- In comment-service, `AuthServiceProvider` stores denied Gate ability context and `AuthorizationErrorRenderer` turns policy denials into a stable `403` JSON envelope and audit event.
- Keep raw gateway-header parsing in middleware or a dedicated request-context layer, not in controllers and not scattered across policies.
- In Laravel services with mixed legacy guard access patterns, resolve the trusted actor once and attach it to every guard and resolver the codebase still reads, such as `Auth::user()`, `$request->user()`, `auth('api')->user()`, or a legacy custom guard.
- VOD shows a practical compatibility pattern: after resolving the user from trusted headers, set the default auth user, set each legacy guard that existing code still reads, and set the request user resolver in the same middleware.
- If you migrate only one guard while other legacy guard lookups remain, helpers, policies, and controllers can disagree about whether the request is authenticated.
- Use policy or Gate responses to express business authorization decisions after auth context normalization, not as a substitute for gateway verification.

## Tenant-safe request handling
- Build request-scoped auth context once near the service edge.
- Normalize at least these fields into a trusted request context object:
  - tenant or project id
  - actor or user id
  - token id when useful for audit
  - request id for trace correlation
- Authorization code should read the normalized request context or server-side request attributes only. Do not re-read raw tenant or actor headers inside policies, services, or repositories after normalization.
- Laravel Eloquent safety rule: if you attach trusted `project_id` or similar request-scoped auth context directly to a model instance for compatibility, keep it transient and non-dirty immediately or keep that context off the model entirely.
- Auth-service shows one safe compatibility pattern for non-persistent model context: set the trusted attribute for request-time reads, then call `syncOriginalAttribute('project_id')` so later `save()` calls do not try to persist a gateway-only attribute into the database.
- HTTP requests without `X-PROJECT-ID` must be rejected with `400`; fallback to the default project id is only allowed for console or queue execution, not normal HTTP traffic.
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.
- If a client-supplied tenant selector in body, query, route, or non-trusted header conflicts with the trusted tenant context, deny explicitly instead of silently choosing one source.
- If a service accepts an extra tenant-shaped identifier for resource lookup, reporting, or local routing, treat it as an untrusted selector until it is matched against the trusted tenant context.
- If a route or service intentionally supports anonymous traffic, make that policy explicit. In that mode, tenant context can still be mandatory while actor context is optional.
- Even in anonymous or analytics flows, never let request-body identity fields override or replace trusted gateway tenant context.

## Async ingest and accept-then-validate flows
- Some downstream services accept transport with `202 Accepted` and then validate trusted context inside an async pipeline or ingestion worker.
- Plain meaning: `202` means `I received your request and queued or started processing it`. It does not mean `auth and tenant validation already succeeded`.
- This pattern is common in analytics or ingestion services where the HTTP layer accepts a batch quickly and deeper validation happens in transforms, workers, queues, or sinks after the response is sent.
- Example: a request reaches the service, the HTTP source returns `202`, then a later transform notices that trusted `X-PROJECT-ID` is missing or malformed and drops the data. In that case the transport was accepted, but the business result is still a denial or discard.
- If required trusted context is missing after accept, log a canonical internal code such as `AUTH_CONTEXT_MISSING` or `TENANT_CONTEXT_MISMATCH` and drop, quarantine, or dead-letter the data according to service policy.
- Do not invent a second public `401` or `403` contract after a `202` has already been returned. The caller already received the transport response; the later auth result belongs in logs, metrics, audit events, dead-letter reasons, or operator-facing monitoring.
- If the product needs the client to receive immediate auth failure, do not use accept-then-validate for that route. Move auth/context checks before the `202` response or require the gateway to enforce them earlier.

## Header usage rules
- Use `X-PROJECT-ID` as the public tenant boundary input.
- If a legacy service still exposes `X-Tenant-Public-Id`, treat it as the old name for the same public `project_id` boundary and plan to rename it to `X-PROJECT-ID` during refactor.
- When validating the public tenant boundary value carried in `X-PROJECT-ID`, validate it as UUIDv7.
- Example header value: `X-PROJECT-ID: 018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- If a service still needs an internal numeric project key after validation, derive or load it from the trusted public `X-PROJECT-ID` boundary inside the service and keep that numeric key service-local.
- API-document rule: document `X-PROJECT-ID` with a UUIDv7 example, and if a service still mentions `X-Tenant-Public-Id` or `tenant_public_id`, mark that name as legacy and equivalent to the public `project_id` boundary.
- Use `X-USER-ID` as the authenticated actor id.
- Use `X-ACCESS` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-REQUEST-ID` only as correlation.
- Keep one canonical spelling for documentation and tests even though HTTP header names are case-insensitive. Current examples in this skill use `X-Project-ID`, `X-User-Id`, `X-User-Mobile`, `X-Access`, and `X-Profile`.
- Treat `X-USER-MOBILE` as supplemental identity or audit context by default.
- Each downstream service must expose one config switch that decides whether `X-USER-MOBILE` is optional or required. The default policy should be optional.
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
- Use `X-PROFILE` / `X-Profile` only for trusted profile context copied from the verified JWT `profile` claim.
- Required decode flow for `X-PROFILE` when the header is present:
  - reject blank or non-base64url values
  - base64url-decode with strict alphabet checking
  - JSON-decode the UTF-8 payload
  - require a JSON object
  - normalize `first_name`, `last_name`, and `shahr` independently: missing key => `null`, explicit `null` => `null`, trimmed empty string => `null`, non-empty string => keep
  - treat malformed payloads, non-object payloads, or invalid non-null field types as canonical code `AUTH_PROFILE_HEADER_INVALID`
- If `X-PROFILE` is absent, downstream services must interpret that as all canonical profile fields being `null` unless a route explicitly forces trusted profile presence.
- Storage rule for services that persist profile data:
  - keep the latest user projection in the local `users` read model
  - keep immutable request-time snapshots only when the domain needs historical or audit context
- Do not rebuild authorization from raw client headers.

## Permission bitmap and downstream role contract
- `X-ACCESS` carries the gateway-injected copy of auth-service's `perm_bm` permission bitmap.
- `X-ACCESS` may carry a compact permission bitmap rather than human-readable scopes.
- The bitmap must be base64url-encoded raw bytes. Permission IDs are 1-based and use least-significant-bit-first packing inside each byte.
- Permission meaning comes from the downstream service's permission map, not from hard-coded bit labels at the gateway.
- Auth-service is the current producer of the bitmap claim and emits these companion JWT claims together:
  - `perm_bm`
  - `perm_catalog_version`
  - `authz_version`
- Auth-service derives `perm_bm` from `permission_catalog.bit_index`, not from mutable local package table IDs.
- Auth-service compilation precedence is `direct deny > direct allow > role grants`.
- If a downstream service, gateway extension, or debugging tool inspects raw JWT claims instead of injected headers, treat `perm_catalog_version` and `authz_version` as the companion invalidation metadata for `perm_bm`.
- Current gateway behavior documented in this skill injects `perm_bm` as `X-ACCESS`, but it does not yet document companion header injection for `perm_catalog_version` or `authz_version`.
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
- Ticket-service confirms the same bitmap contract and currently maps these ids from `X-ACCESS`:
  - `14` -> `crm_get_tickets`
  - `15` -> `crm_post_ticket_reply`
  - `16` -> `crm_put_ticket`
  - `17` -> `crm_post_bulk_ticket`
- VOD confirms the same bitmap contract and keeps its service-local permission-id map in `config/permissions.php`; its current mapped set covers ids `1-13` and `22-39`.
- Laravel compatibility pattern: decode the bitmap once in auth middleware, map ids to permission names from service-local config, attach the mapped names to the request-scoped user object, and let `isAbleTo` or policy checks read those normalized permission names.
- Do not authenticate the actor successfully and then silently continue with an empty decoded permission set on routes that expect permission-bearing context. Fail during trusted-context normalization with the canonical auth code instead.
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
- Ticket-service shows a common legacy failure mode: decode `X-ACCESS`, map known ids from config, and if nothing valid remains, let the request continue until a later generic `unauthorized` or `access_denied` path fires.
- Target standard: do not defer malformed or unknown-only bitmap failures to later generic auth checks. Fail during trusted-context normalization with canonical code `AUTH_ACCESS_BITMAP_INVALID` so the outward response and deny logs stay specific and consistent.

## Logging and observability
- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
- Preserve inbound `traceparent`, `tracestate`, and `baggage` across HTTP boundaries. On async boundaries, forward `traceparent` and `tracestate`, and only forward baggage keys that were explicitly reviewed as safe.
- If a service maps an internal policy decision to a route-specific outward deny code, the API response `code` and the emitted deny log `code` must stay identical.
- When auth context is missing or malformed, make the denial observable.

# Auth and token error contract
Use this section as the standard contract for auth and token-related deny responses and logs across downstream services.

This contract is intentionally aligned with `alaa-observability-soc`:
- response codes must be stable
- logs must repeat the same stable `code`
- logs must include request correlation and safe auth context
- messages must stay user-safe and not leak verifier internals

## Contract rules
- Use a stable machine-readable `code` in both the API response and logs.
- Use a short user-facing `message` in English.
- Keep `meta` safe and small.
- Do not put raw tokens, full JWT payloads, secrets, stack traces, or key material in response or logs.
- Prefer one canonical code per auth failure class across services.
- If a downstream service translates a gateway denial, preserve the same semantic code instead of inventing a new synonym.
- A service may keep internal policy or framework deny labels, but the final outward response `code` and deny-log `code` must match exactly.

## Recommended response envelope
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

## Recommended log fields for auth denies
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

## Canonical auth and token codes
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
  - `meta.claim` may contain a safe claim name such as `project_id` or `sub`

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

- `AUTH_PROFILE_HEADER_INVALID`
  - HTTP: `400`
  - Meaning: `X-Profile` is present but is not a valid base64url(JSON) profile payload, does not decode to a JSON object, or contains invalid non-null values for `first_name`, `last_name`, or `shahr`

- `AUTH_PROFILE_HEADER_REQUIRED`
  - HTTP: `400`
  - Meaning: the route or operation explicitly requires trusted `X-Profile`, but it was missing or blank

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

## Mapping from current gateway error names
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

Important: do not collapse downstream header-validation failures into gateway verifier failures. For example, `AUTH_ACCESS_BITMAP_INVALID` and `AUTH_ROLE_RESOLUTION_FAILED` happen after gateway verification, inside the downstream service's trusted-context normalization layer.

## Async transport note for canonical codes
- For accept-then-validate services, keep the public transport contract and the internal auth result separate.
- If the HTTP layer already returned `202`, use canonical codes such as `AUTH_CONTEXT_MISSING`, `TENANT_CONTEXT_MISSING`, or `TENANT_CONTEXT_MISMATCH` in logs, metrics, dead-letter reasons, or audit events instead of trying to send a later public auth response.

## Guidance for future backend harmonization
- In the first step, new services and changed services should adopt these codes for auth and token failures.
- In the second step, existing services can be migrated gradually by adding the canonical code to logs first, then aligning response payloads.
- If a service already has a deployed response contract, prefer additive migration over breaking changes.

Before using the checklist below, confirm that all relevant companion skills have already been read for the current task. The checklist assumes that gateway trust rules from this skill and implementation/deployment rules from the companion skill set are both in scope.

# Service implementation checklist
Use this checklist when adapting a downstream service to this trust model:
1. Confirm the service is not directly exposed to untrusted traffic, or add header stripping at the service edge.
2. Create one request-scoped auth context builder near ingress or middleware.
3. Read tenant from `X-PROJECT-ID` and actor from `X-USER-ID`.
4. If the service still uses legacy names such as `tenant_id`, `tenant_public_id`, or `X-Tenant-Public-Id`, map them to `project_id` as part of the refactor plan and keep the trust semantics unchanged.
5. Validate the public tenant boundary value as UUIDv7 when that value is exposed in service contracts, and if the service still keeps an internal numeric key, translate after that validation instead of replacing the public boundary contract.
6. Reject protected requests if trusted tenant context is missing, and reject missing actor context when the route or service policy requires an authenticated actor.
7. When a route or write path consumes trusted profile data, decode `X-Profile` when present, normalize nullable `first_name`, `last_name`, and `shahr`, and keep the latest local user projection separate from immutable request-time snapshots. Use `AUTH_PROFILE_HEADER_REQUIRED` only for routes that intentionally force trusted profile presence.
8. Keep authorization in service-layer policies or domain logic, not in controllers and not in reverse-proxy assumptions.
9. Deny client tenant-override attempts explicitly instead of silently preferring one tenant source.
10. Scope every tenant-aware query or command by the trusted tenant context.
11. Keep deny response codes and deny log codes aligned, with request and trace correlation attached.
12. Add tests for spoofed headers, missing tenant context, malformed `X-Profile`, cross-tenant access attempts, conflicting tenant selectors, and any route that intentionally allows anonymous traffic.

Run this review checklist only after reading the relevant companion skill(s) for the task area. A review is incomplete if it checks gateway trust rules but skips the applicable Laravel, security, observability, Octane, proxy, or Arvan companion guidance.

# Review checklist for agents
Flag a problem when you see any of these:
- A service trusts `X-PROJECT-ID` or `X-USER-ID` on a public endpoint without a trusted proxy boundary.
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
- A service treats `X-PROFILE` as client-provided, raw JSON, or a gateway-decoded value instead of the exact base64url claim copied from the verified token.
- A service stores historical profile snapshots but fails to refresh the latest local user projection from the trusted gateway payload.
- A service keeps documenting `tenant_id`, `tenant_public_id`, or `X-Tenant-Public-Id` as if they were different concepts instead of a legacy alias scheduled to be renamed to `project_id` / `X-PROJECT-ID`.

- A service derives `tenant_id` or `project_id` from request body fields before trusted `X-PROJECT-ID`.
- A service upgrades payload identity such as `identity.user_id`, `visitor_id`, or `device_id` into trusted actor context when `X-USER-ID` is missing.
- A team treats async `202 Accepted` transport as proof that trusted auth or tenant validation succeeded.

# Laravel and Octane guidance
- In Laravel services, parse trusted gateway headers once in middleware or a dedicated request-context layer, then pass normalized context into services and policies.
- Keep controllers thin. Authorization belongs in Policies, Gates, or service-layer domain checks.
- If a Laravel compatibility layer temporarily attaches trusted gateway context to an Eloquent user model, keep that attribute request-scoped only and prevent dirty persistence of non-column values.
- Auth-service currently uses `setAttribute('project_id', $projectId)` plus `syncOriginalAttribute('project_id')` so protected profile or session writes can read trusted project context without later trying to update `users.project_id`.
- In Octane or other long-lived workers, auth and tenant context must be strictly request-scoped and reset every request.

# Related skills and required read order
These are not optional background references. They are required companion reads when the task enters their scope.

- `alaa-security-review`
  Read before reviewing or changing JWT verification, token handling, header trust, tenant isolation, authn/authz controls, or abuse-resistant auth behavior.

- `alaa-laravel-architecture`
  Read before changing Laravel middleware, guards, Policies, Gates, service-layer authorization, request-context normalization, DTO boundaries, or auth-related response contracts.

- `alaa-php-clean-code`
  Read before writing or refactoring PHP / Laravel code in gateway-aware middleware, guards, request-context builders, DTOs, services, or auth-facing response mappers so the code follows the shared clean-code, pattern, type-safety, and Laravel best-practice baseline.

- `alaa-octane-performance`
  Read before changing auth or tenant-context handling in Octane or any long-lived worker environment, or when auth middleware sits on a hot path.

- `alaa-observability-soc`
  Read before changing auth error codes, deny logging, request correlation, `X-Request-Id`, `X-Correlation-Id`, trace propagation, or SOC-facing auth event behavior.

- `alaa-docker-production`
  Read before changing trusted proxy boundaries, direct service exposure, container networking, or `X-Forwarded-*` handling at deployment/runtime edges.

- `alaa-haproxy`
  Read before changing gateway ACLs, header sanitization or injection, path-prefix stripping, JWT verification order, public vs protected route behavior, or HAProxy-side auth enforcement.

- `caas-arvan-kuber`
  Read before changing Arvan/Kubernetes exposure mode, ingress vs load balancer entrypoints, or any public-entry trust boundary in Arvan environments.

Routing rule:
- If a task matches any bullet above, read that companion skill before proceeding.
- If a task matches more than one bullet, read all matching skills before proceeding.
- If a task does not match any bullet, stay with this skill and the target repository's local docs/code.
# Anti-patterns
- Trusting internal auth headers on directly exposed services.
- Letting request body, route params, or query params override trusted tenant context.
- Treating gateway authentication as full authorization.
- Spreading raw header reads across the codebase instead of normalizing them once.
- Treating `X-Profile` as raw JSON instead of base64url(JSON) copied unchanged from the verified `profile` token claim.
- Silently accepting a client tenant selector that conflicts with trusted tenant context.
- Treating `tenant_id`, `tenant_public_id`, and `project_id` as different tenant-boundary concepts when they are supposed to be one shared concept under the `project_id` name.
- Logging raw access tokens.
- Assuming README design notes are more accurate than active HAProxy config.
- Applying this skill in isolation when the task clearly also requires one or more companion skills.
