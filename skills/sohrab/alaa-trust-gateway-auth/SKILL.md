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
Before any auth context is injected, the gateway deletes these incoming headers to stop spoofing:
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

## User identity
- The current user identity is `sub` from the verified JWT.
- It is propagated to downstream services as `X-USER-ID`.
- Mobile, token id, audience, issue time, not-before time, expiry time, scopes, and permission bitmap are supplemental context, not replacements for server-side authorization rules.

## What not to do
- Do not derive tenant from a client body field such as `project_id` when `X-PROJECT-ID` is already available from the trusted gateway.
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

## Tenant-safe request handling
- Build request-scoped auth context once near the service edge.
- Normalize at least these fields into a trusted request context object:
  - tenant or project id
  - actor or user id
  - token id when useful for audit
  - request id for trace correlation
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.

## Header usage rules
- Use `X-PROJECT-ID` as the tenant boundary input.
- Use `X-USER-ID` as the authenticated actor id.
- Use `X-ACCESS` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-REQUEST-ID` only as correlation.
- Do not rebuild authorization from raw client headers.

## Logging and observability
- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
- When auth context is missing or malformed, make the denial observable.

# Service implementation checklist
Use this checklist when adapting a downstream service to this trust model:
1. Confirm the service is not directly exposed to untrusted traffic, or add header stripping at the service edge.
2. Create one request-scoped auth context builder near ingress or middleware.
3. Read tenant from `X-PROJECT-ID` and actor from `X-USER-ID`.
4. Reject protected requests if trusted tenant or actor context is missing.
5. Keep authorization in service-layer policies or domain logic, not in controllers and not in reverse-proxy assumptions.
6. Scope every tenant-aware query or command by the trusted tenant context.
7. Log denials with request id and safe auth context.
8. Add tests for spoofed headers, missing tenant context, and cross-tenant access attempts.

# Review checklist for agents
Flag a problem when you see any of these:
- A service trusts `X-PROJECT-ID` or `X-USER-ID` on a public endpoint without a trusted proxy boundary.
- A service accepts tenant id from request body or route and lets it override gateway context.
- Business authorization is missing because the team assumed the gateway already handled it.
- A direct service exposure lets clients send internal auth headers.
- Raw tokens are logged.
- Request-scoped auth or tenant context can leak across requests.
- A service depends on opaque-token behavior that the current gateway does not implement.

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
