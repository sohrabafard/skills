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
- The `profile` claim value must be a base64url-encoded UTF-8 JSON object whose canonical keys are `first_name`, `last_name`, and `shahr` when they are present. When `shahr` exists, it is an object with fixed keys `id` and `name`.
  ```json
  {
    "first_name": null,
    "last_name": null,
    "shahr": {
      "id": null,
      "name": "Mashhad"
    }
  }
  ```
- Auth-service should omit any key whose value is `null`, and it may omit the entire `profile` claim when all three canonical fields are `null`.
- Gateway must strip any inbound `X-PROFILE` / `X-Profile`, verify the token, and if the verified token has a `profile` claim, copy that exact claim value into `X-PROFILE`.
- Gateway must not decode, reshape, normalize, or re-encode the `profile` claim before forwarding it.
- If the verified token has no `profile` claim, the gateway must not fabricate `X-PROFILE`.
- Downstream services that need profile data must base64url-decode `X-Profile`, JSON-decode the UTF-8 payload, require a JSON object, normalize `first_name` and `last_name` as nullable trimmed strings, and validate `shahr` as either missing or an object with keys `id` and `name`: missing key => `null`, explicit JSON `null` => `null`, `shahr.name` trimmed empty => `AUTH_PROFILE_HEADER_INVALID`, `shahr.name` non-empty string => keep, `shahr.id` integer or `null` => keep, and any other non-null `shahr` shape => `AUTH_PROFILE_HEADER_INVALID`.
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
