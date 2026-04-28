# Compact JWT and header trust model

## Ala end-to-end authn and authz picture

Use this section when an agent needs the whole Ala picture before making auth changes.

Default Ala flow:
- frontend or public client -> gateway -> backend service
- gateway -> active request-time checker such as `authz-sidecar` or `entitlement-spoa` -> OpenFGA
- normalized business change -> `entitlement-api` -> `projector` -> OpenFGA

Core meaning:
- the gateway owns authentication
- the active request-time checker owns the fine-grained route decision
- backend services consume trusted context and enforce business rules inside the service
- `entitlement-api` owns normalized authorization business truth
- `projector` writes derived tuples
- OpenFGA stores derived effective authorization state

## Layer ownership map

### Frontend or public client

- call documented gateway-facing routes only
- send `Authorization: Bearer ...` to the gateway only
- never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, or any `X-Authz-*` header
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

## What the gateway verifies
For protected routes, the current gateway (HAProxy) logic verifies these checks in order:
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
- Required claims: `pid` and `sub`
- `iss` validation exists in the template but is not currently enabled because the issuer list is empty
- `aud` validation exists in the template but is not currently enabled because the audience list is empty

## What the gateway does not verify
- It does not do business authorization.
- It does not decide whether a user may perform a domain action.
- It does not evaluate `X-Access` or `X-USER-SCOPES` for route permission.
- It does not consume backend permission-catalog generated configs or own permission-name-to-bitmap-id maps.
- It does not derive tenant from hostname, path prefix, body, or query string.
- It does not introspect opaque tokens.

## Headers the gateway rejects from client input
Before any auth context is injected, the gateway deletes these incoming headers to stop spoofing. This sanitize step must run on all routes, including public routes that do not receive injected auth context:
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

## Compact JWT claim to header map
The gateway injects these trusted headers after successful verification:
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

Only claims that are present are injected.
`prv` and `av` are compact versioning claims used for invalidation and diagnostics; they are not forwarded as headers by default.
`X-Access` is only the trusted gateway projection of verified `prm`; downstream service configs determine local permission names from `alaa-permission-catalog` generated outputs.

## Compact claim semantics

| Claim | Meaning                    | Notes                                              |
|-------|----------------------------|----------------------------------------------------|
| `pid` | project boundary id        | trusted tenant boundary after gateway verification |
| `sub` | authenticated user id      | user identifier                                    |
| `m`   | mobile                     | trusted mobile context                             |
| `prm` | permission bitmap          | compact authorization bitmap                       |
| `prv` | permission catalog version | invalidation metadata for `prm`                    |
| `av`  | authz version              | invalidation metadata for authorization state      |
| `fn`  | first name                 | trusted user first name                            |
| `ln`  | last name                  | trusted user last name                             |
| `loc` | location bundle            | see nested keys below                              |

### `loc` sub-keys

| Key  | Meaning    | Forwarded header        |
|------|------------|-------------------------|
| `o`  | ostan      | `X-Location-Ostan`      |
| `sr` | shahrestan | `X-Location-Shahrestan` |
| `b`  | bakhsh     | `X-Location-Bakhsh`     |
| `sh` | shahr      | `X-Location-Shahr`      |
| `br` | shobe      | `X-Location-Shobe`      |
| `sc` | school     | `X-Location-School`     |

## Auth-service local trusted header contract
- Auth-service's `trusted_gateway` guard currently consumes only:
  - `X-User-Id`
  - `X-Project-Id`
- Auth-service does not currently read `X-Access`, `X-User-Mobile`, `X-Access-Token-Id`, `X-TOKEN-*`, `X-USER-SCOPES`, or the name and location headers on its protected v3 routes.
- Current auth-service behavior parses trusted `X-User-Id` and `X-Project-Id` as positive integers on protected gateway-backed routes.
- Current auth-service standard no longer requires any extra backend-only signature header on trusted routes. The trust boundary is the sanitized gateway path plus the required injected identity headers.
- Target standard after the current platform decision: the shared gateway boundary carries the compact JWT claims above, while auth-service may keep a separate internal numeric project key during migration.
- Auth-service follow-through rule: do not freeze the current positive-integer header parser into the shared public contract. Translate the trusted public boundary to the internal numeric key at auth-service ingress, or complete the broader model migration later.
- For direct backend testing against auth-service, send the service-local route plus those exact trusted headers. Do not expect auth-service to parse a Bearer token locally on `/api/v3/profile*`, `/api/v3/sessions*`, `/api/v3/totp*`, or admin trusted-gateway routes.

## Other header behavior
- `Authorization` is stripped after successful verification in the current deployment values.
- `X-Request-ID` is preserved if the client already sent one; otherwise the gateway generates one.
- `X-Request-ID` is for tracing only. It is not an auth or tenant header.
- The gateway overwrites `X-Forwarded-Proto` to `https` because TLS terminates upstream.
- The repo does not show equivalent sanitization or re-issuance for `X-Forwarded-For` or `X-Real-IP`.

## Tenant and user context
### Tenant context
- The current tenant context is the compact `pid` claim from the verified JWT.
- In this gateway, compact `pid` is required on protected routes.
- This is the main tenant boundary header propagated to downstream services as `X-Project-Id`.
- `tenant_id` and `tenant_public_id` are legacy names for the same public tenant boundary.
- Platform refactor target: keep compact `pid` as the JWT claim key, keep `X-Project-Id` as the trusted header, and standardize public and service-facing payloads on `project_id`.
- Validation rule for the public tenant/project identifier: when a service validates the shared public tenant boundary value, validate it as UUIDv7.
- UUIDv7 example for `project_id`: `018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- Migration rule for storage-backed services: if a service still keeps an internal numeric tenant or project key, translate the trusted public boundary to that internal key near ingress and keep the internal key out of trusted headers, public API examples, and other public-facing contracts.
- API-document rule: service OpenAPI or README examples should use the same UUIDv7 example shape for public `project_id`, and should explain that older names such as `tenant_public_id` map to the same shared concept and are scheduled to be renamed.

### User identity
- The current user identity is `sub` from the verified JWT.
- It is propagated to downstream services as `X-User-Id`.
- Some downstream services intentionally allow anonymous or analytics-only traffic. In those services, `X-User-Id` may be absent while `X-Project-Id` is still required.
- If the platform decides a given route must always carry an access token, remove that route from the gateway public list instead of teaching downstream services to partially trust missing auth context.
- When `X-User-Id` is absent, do not synthesize a trusted actor from client payload fields such as `identity.user_id`, `visitor_id`, `device_id`, or similar client-generated identifiers. If such fields are stored, classify them as untrusted analytics metadata only.
- Mobile, token id, audience, issue time, not-before time, expiry time, scopes, and permission bitmap are supplemental context, not replacements for server-side authorization rules.

### Services without a tenant boundary
- Not every gateway-backed service is currently tenant-scoped.
- VOD's current header-auth path reads `X-User-Id` and `X-Access`, maps permissions from service-local config, and does not derive tenant context from gateway headers.
- Target standard: do not invent `project_id` enforcement in a service that has no real tenant boundary just to make documentation look uniform.
- If such a service later becomes tenant-aware, add trusted `X-Project-Id` normalization first and then scope reads and writes from that trusted value.

## What not to do
- Do not derive tenant from a client body field such as `project_id` or `tenant_id` when `X-Project-Id` is already available from the trusted gateway.
- Do not trust `X-Project-Id` or `X-User-Id` if the service is reachable directly by clients or untrusted internal callers.
- Do not let route params or query params override the trusted tenant context.
