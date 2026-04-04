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

When facts conflict, trust sources in this order:
1. The active HAProxy template and values in the gateway repo.
2. Rendered manifests from the gateway repo.
3. Gateway docs and README text.
4. Older team assumptions.

If README text and HAProxy config disagree, trust the config.

Execution order:
1. Read this guide to establish the shared trust boundary.
2. Determine whether the task is gateway-side, downstream-service-side, observability-side, runtime-side, or deployment-side.
3. Read the matching companion skill or skills before giving implementation advice.
4. Inspect repository-local code, docs, and configs.
5. Only after that, propose or implement changes.

## Compact claim and header contract

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
| `m` | mobile | `X-USER-MOBILE` |
| `prm` | permission bitmap | `X-ACCESS` |
| `prv` | permission catalog version | not forwarded by default |
| `av` | authorization version | not forwarded by default |
| `pid` | public project boundary | `X-PROJECT-ID` |
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

Rules:
- `project_id`, `tenant_id`, `tenant_public_id`, and `pid` point at one tenant-boundary concept, but they belong to different layers.
- Canonical public API field name: `project_id`.
- Canonical trusted header name: `X-PROJECT-ID`.
- Canonical compact JWT claim key: `pid`.
- Public and service-facing payloads keep the field name `project_id`; only the compact JWT claim uses `pid`.
- `prv` and `av` are raw JWT metadata only unless a future contract explicitly gives them a forwarded use.
- The gateway injects trusted headers only from verified claims.
- Missing optional compact fields are not fabricated by the gateway.
- If auth-service chooses to emit compact null sentinels such as empty string for names or `0` for location ids, downstream services must normalize those sentinels once near ingress instead of spreading raw sentinel handling across the codebase.

## Trusted ingress and auth-service boundary

### Core trust model

- The gateway is the authentication boundary for protected HTTP routes.
- The gateway verifies the Bearer JWT and then injects trusted request headers for downstream services.
- Downstream services must still do authorization and tenant-safe data access.
- Client-supplied internal auth headers are never trusted.
- Tenant context is derived from the verified token, not from request body, query string, route params, or client-supplied headers.
- Header target standard: rename `X-Tenant-Public-Id` to `X-PROJECT-ID` in service contracts and docs during the platform refactor.
- Until the refactor is complete, treat `tenant_id` and `tenant_public_id` only as legacy aliases of the same trusted boundary and normalize them back to the canonical layer-specific contract: `project_id` in public APIs and `pid` plus `X-PROJECT-ID` in compact JWT and trusted-header handling.

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
- If any gateway or repo doc still mentions `/auth/api/v2/*`, treat that as legacy drift to remove, not as active client guidance.
- Do not reintroduce `/api/v2` into auth-service and do not teach new services or callers to depend on retired auth v2 routes.

### Gateway-facing routes vs service-local routes

This distinction is mandatory.

- Clients call the gateway-facing route, which includes the service prefix used for gateway routing.
- The gateway routes by prefix and may strip that prefix before proxying to the backend service.
- A backend service must therefore document and implement its own local route shape, not the gateway-facing one.

Current HAProxy behavior:
- routing happens by path prefix such as `/auth`, `/vod`, `/comment`, `/ticket`, and `/wa`
- when `stripPathPrefix: true`, the gateway removes that prefix before sending the request to the downstream service

Example for auth service:
- gateway-facing public route: `/auth/api/v3/otp/request`
- service-local route after prefix strip: `/api/v3/otp/request`

Rule for future agents:
- when writing or reviewing the gateway itself, use gateway-facing routes
- when writing or reviewing a downstream service, use service-local routes after prefix stripping
- never force a backend service to define routes with the gateway prefix unless that backend is intentionally designed that way

### Auth-service v3 endpoint and client contract

Canonical gateway-facing client flow:
1. Client calls `POST /auth/api/v3/otp/request`.
2. Client receives OTP out-of-band.
3. Client calls `POST /auth/api/v3/otp/verify`.
4. Successful verify returns the access token in the JSON body and sets the refresh token in the HttpOnly `auth_refresh_token` cookie.
5. Client calls gateway-protected routes with `Authorization: Bearer <access token>` on the gateway-facing route.
6. When the access token expires or is rejected by the gateway, client calls `POST /auth/api/v3/token/refresh`.
7. Successful refresh rotates the refresh token, returns a new access token, and replaces the refresh cookie.
8. Client calls `POST /auth/api/v3/logout` when it wants to revoke the current refresh-token session.

Auth request details from the auth repo and Postman collection:
- OTP request, OTP verify, and refresh requests use `Accept: application/json` and `Content-Type: application/json`.
- The current Postman collection also sends `X-Request-Id` and `X-Device-Id` on those public auth requests.
- `X-Device-Id` is optional client or device metadata for auth-service. It is not a trusted gateway auth header.
- `POST /auth/api/v3/token/refresh` expects the refresh token from the HttpOnly cookie first.
- Refresh request body must include `access_token`, and may include `device_id`.
- `POST /auth/api/v3/logout` is public in the auth-service contract and can revoke from either `refresh_token` in the request body or the refresh-token cookie.

Current protected auth-service route families behind the gateway:
- `/auth/api/v3/sessions*`
- `/auth/api/v3/totp*`
- `/auth/api/v3/admin/users/{user}/sessions*`
- `/auth/api/v3/admin/users/{user}/authz-overrides*`
- `/auth/api/v3/profile*`

Direct local backend testing contract for auth-service:
- backend-only Postman tests may call service-local `/api/v3/*` routes directly
- in that local mode, Postman sends trusted headers such as `X-USER-ID` and `X-PROJECT-ID` instead of a Bearer token
- this is backend-only local testing, not the public client contract
- current auth Postman examples still use numeric compatibility fixtures in some places; treat those as migration fixtures, not as permission to weaken the shared public boundary contract

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
- it does not evaluate `X-ACCESS` or `X-USER-SCOPES` for route permission
- it does not derive tenant from hostname, path prefix, body, or query string
- it does not introspect opaque tokens

Important doc drift:
- if any README text still suggests opaque-token passthrough or the old profile-blob header contract, treat that as drift to remove

### Header trust rules

Headers the gateway rejects from client input:
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
- `X-User-Fname`
- `X-User-Lname`
- `X-Location-Ostan`
- `X-Location-Shahrestan`
- `X-Location-Bakhsh`
- `X-Location-Shahr`
- `X-Location-Shobe`
- `X-Location-School`

Headers the gateway injects after successful verification:
- `pid` -> `X-PROJECT-ID`
- `sub` -> `X-USER-ID`
- `m` -> `X-USER-MOBILE`
- `prm` -> `X-ACCESS`
- `jti` -> `X-ACCESS-TOKEN-ID`
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
- the gateway must not fabricate missing optional compact values
- `prv` and `av` stay out of the forwarded header contract unless a future revision explicitly adds them

### Auth-service local trusted header contract

- Auth-service's `trusted_gateway` guard currently consumes only `X-USER-ID` and `X-PROJECT-ID`.
- Auth-service does not currently read `X-ACCESS`, `X-USER-SCOPES`, `X-USER-MOBILE`, token-metadata headers, or the compact name and location headers on its protected v3 routes.
- Current auth-service behavior parses trusted `X-USER-ID` and `X-PROJECT-ID` as positive integers on protected gateway-backed routes.
- Current auth-service standard no longer requires any extra backend-only signature header on trusted routes.
- Do not freeze the current positive-integer parser into the shared public contract. Translate the trusted public project boundary to the internal numeric key at auth-service ingress, or complete the broader model migration later.

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
- this is the main tenant boundary header propagated to downstream services as `X-PROJECT-ID`
- platform refactor target: keep compact `pid` as the JWT claim key, keep `X-PROJECT-ID` as the trusted header, and standardize public and service-facing payloads on `project_id`
- validation rule for the shared public tenant or project identifier: validate it as UUIDv7

User identity:
- the current user identity is `sub` from the verified JWT
- it is propagated to downstream services as `X-USER-ID`
- some downstream services intentionally allow anonymous or analytics-only traffic; in those services, `X-USER-ID` may be absent while `X-PROJECT-ID` is still required
- mobile, token id, audience, issue time, not-before time, expiry time, scopes, compact names, compact location ids, and permission bitmap are supplemental context, not replacements for server-side authorization rules

## Downstream normalization and authorization

### Network and trust boundary rules

- A service may trust gateway auth headers only if the request came through the trusted edge and sanitized gateway path.
- If a service can be reached directly, it must either block that exposure or strip and reject internal auth headers at its own edge.
- Internal auth headers are hop-by-hop trust artifacts inside your platform, not public API inputs.

### Authentication vs authorization

- Treat the gateway as the authentication and context-propagation layer.
- Treat each downstream service as the authorization layer for business actions.
- A verified token plus injected headers does not mean the user may perform the requested operation.
- Do not copy older per-request auth-service callback patterns into new gateway-backed services.

### Laravel Gate and policy flow

- Build the request-scoped actor and tenant context before any framework authorization runs.
- Keep raw gateway-header parsing in middleware or a dedicated request-context layer, not in controllers and not scattered across policies.
- In Laravel services with mixed legacy guard access patterns, resolve the trusted actor once and attach it to every guard and resolver the codebase still reads.
- Use policy or Gate responses to express business authorization decisions after auth context normalization, not as a substitute for gateway verification.

### Tenant-safe request handling

- Build request-scoped auth context once near the service edge.
- Normalize at least tenant or project id, actor id, token id when useful, request id, and any compact name or location fields the service actually uses.
- Authorization code should read the normalized request context or server-side request attributes only.
- HTTP requests without `X-PROJECT-ID` must be rejected with `400`; fallback to the default project id is only allowed for console or queue execution, not normal HTTP traffic.
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.
- If a client-supplied tenant selector conflicts with the trusted tenant context, deny explicitly instead of silently choosing one source.
- Never derive location display names from compact ids unless another explicit source-of-truth contract adds that behavior.

### Async ingest and accept-then-validate flows

- `202 Accepted` means transport accepted, not that auth and tenant validation already succeeded.
- If required trusted context is missing after accept, log a canonical internal code such as `AUTH_CONTEXT_MISSING` or `TENANT_CONTEXT_MISMATCH` and drop, quarantine, or dead-letter the data according to service policy.
- If the product needs the client to receive immediate auth failure, do not use accept-then-validate for that route.

### Header usage rules

- Use `X-PROJECT-ID` as the trusted tenant boundary input and `project_id` as the public payload field name.
- Use `X-USER-ID` as the authenticated actor id.
- Use `X-ACCESS` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-USER-MOBILE` as supplemental identity or audit context by default.
- Treat `X-User-Fname` and `X-User-Lname` as optional trusted strings.
- Treat every `X-Location-*` header as an optional trusted integer identifier.
- If compact null sentinels such as empty string or `0` appear, normalize them once near ingress into the repository-owned projection shape.
- If the headers are absent entirely, do not fabricate them in the service.
- Keep the trusted projection surface compact and do not invent a second user-context shape.

### Permission bitmap and downstream role contract

- `X-ACCESS` carries the gateway-injected copy of auth-service's `prm` permission bitmap.
- The bitmap must be base64url-encoded raw bytes. Permission IDs are 1-based and use least-significant-bit-first packing inside each byte.
- Permission meaning comes from the downstream service's permission map, not from hard-coded bit labels at the gateway.
- If raw JWT claims are inspected for diagnostics, `prv` and `av` are the companion invalidation metadata for `prm`.
- Do not silently continue with an empty decoded permission set on routes that expect permission-bearing context.

### Logging and observability

- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
- Preserve inbound `traceparent`, `tracestate`, and `baggage` across HTTP boundaries. On async boundaries, forward only reviewed-safe baggage keys.
- If a service maps an internal policy decision to a route-specific outward deny code, the API response code and emitted deny-log code must stay identical.

## Error contract, review checklist, and anti-patterns

Contract rules:
- Use a stable machine-readable `code` in both the API response and logs.
- Use a short user-facing `message` in English.
- Keep `meta` safe and small.
- Do not put raw tokens, full JWT payloads, secrets, stack traces, or key material in response or logs.
- If a downstream service translates a gateway denial, preserve the same semantic code instead of inventing a new synonym.

Recommended response envelope:

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

Recommended log fields for auth denies:
- `code`
- `message` or `reason`
- `http.status`
- `request_id`
- `project_id` when known
- `user_id` when known
- `token_jti` when known
- `route` or normalized path
- `auth_source`

Canonical compact-contract codes that commonly matter in downstream services:
- `AUTH_MISSING_REQUIRED_CLAIM`
- `AUTH_CONTEXT_MISSING`
- `AUTH_ACCESS_BITMAP_INVALID`
- `AUTH_MOBILE_HEADER_INVALID`
- `AUTH_NAME_OR_LOCATION_HEADER_INVALID`
- `AUTH_NAME_OR_LOCATION_HEADER_REQUIRED`
- `AUTHZ_DENIED`
- `TENANT_CONTEXT_MISMATCH`
- `TENANT_CONTEXT_MISSING`
- `TENANT_CONTEXT_INVALID`

Mapping from current gateway error names:
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

Service implementation checklist:
1. Confirm the service is not directly exposed to untrusted traffic, or add header stripping at the service edge.
2. Create one request-scoped auth context builder near ingress or middleware.
3. Read tenant from `X-PROJECT-ID` and actor from `X-USER-ID`.
4. Map legacy tenant names such as `tenant_id`, `tenant_public_id`, or `X-Tenant-Public-Id` back to `project_id` and `X-PROJECT-ID`.
5. Validate the public tenant boundary value as UUIDv7 when that value is exposed in service contracts.
6. Reject protected requests if trusted tenant context is missing, and reject missing actor context when the route or service policy requires an authenticated actor.
7. When a route or write path consumes trusted compact identity headers, normalize the trusted name and location headers once, keep the latest local user projection separate from immutable request-time snapshots, and use `AUTH_NAME_OR_LOCATION_HEADER_REQUIRED` only for routes that intentionally force trusted identity presence.
8. Keep authorization in service-layer policies or domain logic, not in controllers and not in reverse-proxy assumptions.
9. Deny client tenant-override attempts explicitly instead of silently preferring one tenant source.
10. Scope every tenant-aware query or command by the trusted tenant context.
11. Keep deny response codes and deny log codes aligned, with request and trace correlation attached.
12. Add tests for spoofed headers, missing tenant context, malformed compact identity headers, cross-tenant access attempts, conflicting tenant selectors, and any route that intentionally allows anonymous traffic.

Review checklist for agents:
- a service trusts `X-PROJECT-ID` or `X-USER-ID` on a public endpoint without a trusted proxy boundary
- a service accepts tenant id from request body or route and lets it override gateway context
- business authorization is missing because the team assumed the gateway already handled it
- a direct service exposure lets clients send internal auth headers
- raw tokens are logged
- request-scoped auth or tenant context can leak across requests
- a backend service is documented with gateway-facing routes even though the gateway strips its service prefix before proxying
- a service treats the compact identity headers as client-provided or gateway-decoded values instead of verified-token derivatives
- a service stores historical identity snapshots but fails to refresh the latest local user projection from the trusted gateway payload

Laravel and Octane guidance:
- parse trusted gateway headers once in middleware or a dedicated request-context layer, then pass normalized context into services and policies
- keep controllers thin
- if a Laravel compatibility layer temporarily attaches trusted gateway context to an Eloquent model, keep that attribute request-scoped only and prevent dirty persistence of non-column values
- in Octane or other long-lived workers, auth and tenant context must be strictly request-scoped and reset every request

Anti-patterns:
- trusting internal auth headers on directly exposed services
- letting request body, route params, or query params override trusted tenant context
- treating gateway authentication as full authorization
- spreading raw header reads across the codebase instead of normalizing them once
- treating compact identity headers as raw data instead of copied verified claims
- silently accepting a client tenant selector that conflicts with trusted tenant context
- logging raw access tokens
- assuming README design notes are more accurate than active HAProxy config
