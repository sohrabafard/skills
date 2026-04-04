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

Run this review checklist only after reading the relevant companion skill(s) for the task area. A review is incomplete if it checks gateway trust rules but skips the applicable Laravel, security, observability, Octane, proxy, or Arvan companion guidance.

# Review checklist for agents
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
- A service keeps documenting `tenant_id`, `tenant_public_id`, or `X-Tenant-Public-Id` as if they were different concepts instead of a legacy alias scheduled to be renamed to `project_id` / `X-Project-Id`.

- A service derives `tenant_id` or `project_id` from request body fields before trusted `X-Project-Id`.
- A service upgrades payload identity such as `identity.user_id`, `visitor_id`, or `device_id` into trusted actor context when `X-User-Id` is missing.
- A team treats async `202 Accepted` transport as proof that trusted auth or tenant validation succeeded.

# Laravel and Octane guidance
- In Laravel services, parse trusted gateway headers once in middleware or a dedicated request-context layer, then pass normalized context into services and policies.
- Keep controllers thin. Authorization belongs in Policies, Gates, or service-layer domain checks.
- If a Laravel compatibility layer temporarily attaches trusted gateway context to an Eloquent user model, keep that attribute request-scoped only and prevent dirty persistence of non-column values.
- Auth-service currently uses request-scoped trusted tenant context and syncs it into the model only for protected request-time reads so later saves do not try to persist a gateway-only attribute into the database.
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
  Read before changing auth error codes, deny logging, request correlation, `X-Request-Id`, `traceparent`, full removal of `X-Correlation-Id`, or SOC-facing auth event behavior.

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
- Treating the compact identity headers as raw data instead of copied verified claims.
- Silently accepting a client tenant selector that conflicts with trusted tenant context.
- Treating `tenant_id`, `tenant_public_id`, and `project_id` as different tenant-boundary concepts when they are supposed to be one shared concept under the public boundary name.
- Logging raw access tokens.
- Assuming README design notes are more accurate than active HAProxy config.
- Applying this skill in isolation when the task clearly also requires one or more companion skills.
