---
name: alaa-trust-gateway-auth
description: "Source-of-truth for Ala gateway auth trust: how Bearer JWT enters, what HAProxy verifies, which X-* headers are sanitized or injected, how tenant context is derived, and what downstream services must do with trusted context."
---

# Purpose
Use this skill when a service lives behind the Ala gateway, or when a change touches auth headers, tenant context, reverse-proxy trust, or request identity propagation.

This skill gives one clear trust model so agents do not guess.

# When to use
- Building or reviewing a downstream service behind the gateway
- Adding middleware that reads user or tenant context from headers
- Debugging auth failures, tenant mismatch, or missing headers
- Changing gateway config, ingress behavior, trusted proxy settings, or service exposure
- Reviewing whether a service is safe to expose directly or must stay behind the gateway

# Source priority
When facts conflict, trust sources in this order:
1. The active HAProxy template and values in the gateway repo
2. Rendered manifests from the gateway repo
3. Gateway docs and README text
4. Older team assumptions

If README text and HAProxy config disagree, trust the config.

# Core trust model
- The gateway is the authentication boundary for protected HTTP routes.
- The gateway verifies the Bearer JWT and then injects trusted request headers for downstream services.
- Downstream services must still do authorization and tenant-safe data access.
- Client-supplied internal auth headers are never trusted.
- Tenant context is derived from the verified token, not from request body, query string, route params, or client-supplied headers.
- Naming rule: `tenant_id` and `project_id` refer to the same tenant-boundary concept in the current platform. The current cross-service canonical name remains `project_id` / `X-PROJECT-ID` for compatibility during refactor. If a service uses `tenant_id` internally, treat it as an internal alias of the same trusted boundary and normalize it back to the canonical gateway-derived project context.

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

## Gateway-facing routes vs service-local routes
This distinction is mandatory.

- Clients call the gateway-facing route, which includes the service prefix used for gateway routing.
- The gateway routes by prefix and may strip that prefix before proxying to the backend service.
- A backend service must therefore document and implement its own local route shape, not the gateway-facing one.

Current HAProxy behavior:
- Routing happens by path prefix such as `/auth`, `/vod`, `/comment`, `/ticket`, and `/wa`.
- When `stripPathPrefix: true`, the gateway removes that prefix before sending the request to the downstream service.

Example for auth service:
- Gateway-facing public route: `/auth/api/v2/login`
- Service-local route after prefix strip: `/api/v2/login`

Example for auth health:
- Gateway-facing route: `/auth/api/health`
- Service-local route: `/api/health`

Rule for future agents:
- When writing or reviewing the gateway itself, use gateway-facing routes.
- When writing or reviewing a downstream service, use service-local routes after prefix stripping.
- Never force a backend service to define routes with the gateway prefix unless that backend is intentionally designed that way.

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

Only claims that are present are injected.

## Other header behavior
- `Authorization` is stripped after successful verification in the current deployment values.
- `X-Request-ID` is preserved if the client already sent one; otherwise the gateway generates one.
- `X-Request-ID` is for tracing only. It is not an auth or tenant header.
- The gateway overwrites `X-Forwarded-Proto` to `https` because TLS terminates upstream.
- The repo does not show equivalent sanitization or re-issuance for `X-Forwarded-For` or `X-Real-IP`.

# Tenant and user context
## Tenant context
- The current tenant context is `project_id` from the verified JWT.
- In this gateway, `project_id` is required on protected routes.
- This is the main tenant boundary header propagated to downstream services as `X-PROJECT-ID`.
- `tenant_id` is not a different security concept here. It is the same tenant boundary under a different local name. Until a platform-wide refactor is completed, standardize shared gateway and service contracts on `project_id` / `X-PROJECT-ID` and treat `tenant_id` only as an internal alias that must not change trust semantics.

## User identity
- The current user identity is `sub` from the verified JWT.
- It is propagated to downstream services as `X-USER-ID`.
- Some downstream services intentionally allow anonymous or analytics-only traffic. In those services, `X-USER-ID` may be absent while `X-PROJECT-ID` is still required.
- If the platform decides a given route must always carry an access token, remove that route from the gateway public list instead of teaching downstream services to partially trust missing auth context.
- When `X-USER-ID` is absent, do not synthesize a trusted actor from client payload fields such as `identity.user_id`, `visitor_id`, `device_id`, or similar client-generated identifiers. If such fields are stored, classify them as untrusted analytics metadata only.
- Mobile, token id, audience, issue time, not-before time, expiry time, scopes, and permission bitmap are supplemental context, not replacements for server-side authorization rules.

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

## Laravel Gate and policy flow
- Build the request-scoped actor and tenant context before any framework authorization runs.
- In comment-service, `ResolveUserMiddleware` builds a lightweight authenticated user from trusted headers, service classes call `Gate::forUser($user)->authorize(...)`, and policies return domain-specific deny codes.
- In comment-service, `AuthServiceProvider` stores denied Gate ability context and `AuthorizationErrorRenderer` turns policy denials into a stable `403` JSON envelope and audit event.
- Keep raw gateway-header parsing in middleware or a dedicated request-context layer, not in controllers and not scattered across policies.
- Use policy or Gate responses to express business authorization decisions after auth context normalization, not as a substitute for gateway verification.

## Tenant-safe request handling
- Build request-scoped auth context once near the service edge.
- Normalize at least these fields into a trusted request context object:
  - tenant or project id
  - actor or user id
  - token id when useful for audit
  - request id for trace correlation
- HTTP requests without `X-PROJECT-ID` must be rejected with `400`; fallback to the default project id is only allowed for console or queue execution, not normal HTTP traffic.
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.
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
- Use `X-PROJECT-ID` as the tenant boundary input.
- Use `X-USER-ID` as the authenticated actor id.
- Use `X-ACCESS` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-REQUEST-ID` only as correlation.
- Keep one canonical spelling for documentation and tests even though HTTP header names are case-insensitive. Current examples in this skill use `X-Project-ID`, `X-User-Id`, `X-User-Mobile`, and `X-Access`.
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
- Do not rebuild authorization from raw client headers.

## Permission bitmap and downstream role contract
- `X-ACCESS` may carry a compact permission bitmap rather than human-readable scopes.
- The bitmap must be base64url-encoded raw bytes. Permission IDs are 1-based and use least-significant-bit-first packing inside each byte.
- Permission meaning comes from the downstream service's permission map, not from hard-coded bit labels at the gateway.
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
- Comment-service currently derives roles like this:
  - admin when all configured permissions are present
  - moderator when any moderation signal permission is present
  - student otherwise
- Current example bitmaps from comment-service docs are:
  - `AAAC` for minimal student access
  - `AAAW` for moderator access
  - `AAAe` for admin access
- Reusable reference implementation: `references/permission-bitmap.php`
- Do not assume another service uses the same permission ids or role derivation unless that service explicitly adopts that exact mapping.
- The bitmap width is produced by the auth service against the full global permission set, so downstream services should expect a common bitmap width even when each service only cares about a subset of ids.

## Logging and observability
- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
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

- `AUTHZ_DENIED`
  - HTTP: `403`
  - Meaning: caller is authenticated but not allowed to perform the requested action

- `TENANT_CONTEXT_MISMATCH`
  - HTTP: `403`
  - Meaning: trusted tenant context and requested target do not match

- `TENANT_CONTEXT_MISSING`
  - HTTP: `401` or `403` depending on service policy
  - Meaning: tenant-safe operation could not proceed because trusted tenant context is absent

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

# Service implementation checklist
Use this checklist when adapting a downstream service to this trust model:
1. Confirm the service is not directly exposed to untrusted traffic, or add header stripping at the service edge.
2. Create one request-scoped auth context builder near ingress or middleware.
3. Read tenant from `X-PROJECT-ID` and actor from `X-USER-ID`.
4. Reject protected requests if trusted tenant context is missing, and reject missing actor context when the route or service policy requires an authenticated actor.
5. Keep authorization in service-layer policies or domain logic, not in controllers and not in reverse-proxy assumptions.
6. Scope every tenant-aware query or command by the trusted tenant context.
7. Log denials with request id and safe auth context.
8. Add tests for spoofed headers, missing tenant context, cross-tenant access attempts, and any route that intentionally allows anonymous traffic.

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
- Different services use different auth failure codes for the same deny class without a compatibility reason.

- A service derives `tenant_id` or `project_id` from request body fields before trusted `X-PROJECT-ID`.
- A service upgrades payload identity such as `identity.user_id`, `visitor_id`, or `device_id` into trusted actor context when `X-USER-ID` is missing.
- A team treats async `202 Accepted` transport as proof that trusted auth or tenant validation succeeded.

# Laravel and Octane guidance
- In Laravel services, parse trusted gateway headers once in middleware or a dedicated request-context layer, then pass normalized context into services and policies.
- Keep controllers thin. Authorization belongs in Policies, Gates, or service-layer domain checks.
- In Octane or other long-lived workers, auth and tenant context must be strictly request-scoped and reset every request.

# Related skills and why to use them
- `alaa-security-review`: use this to review auth correctness, JWT rules, header trust, and token-handling mistakes.
- `alaa-laravel-architecture`: use this to place authorization in the correct Laravel layer and keep controllers thin.
- `alaa-octane-performance`: use this when the service runs on Octane and request-scoped tenant or auth state must not leak between requests.
- `alaa-observability-soc`: use this for denial logging, safe auth telemetry, request correlation, and incident-ready traces.
- `alaa-docker-production`: use this for trusted proxy boundaries, network exposure, and safe `X-Forwarded-*` handling at container and deployment level.
- `haproxy-3.2`: use this when the change touches HAProxy auth flow, ACL order, header mutation, or verification behavior.
- `caas-arvan-kuber`: use this for Arvan or Kubernetes edge exposure behavior, ingress vs load balancer choices, and public-entry trust boundaries.

# Anti-patterns
- Trusting internal auth headers on directly exposed services.
- Letting request body, route params, or query params override trusted tenant context.
- Treating gateway authentication as full authorization.
- Spreading raw header reads across the codebase instead of normalizing them once.
- Logging raw access tokens.
- Assuming README design notes are more accurate than active HAProxy config.
