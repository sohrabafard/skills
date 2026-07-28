# Ala Services, Auth, Authz, and TOTP: Skill-Only Assessment

Generated: 2026-07-27 22:22:42 Asia/Tehran

## Evidence boundary

This assessment uses only the installed skill documents and their routed references. It does not use
memory, application source code, live runtime inspection, or web research. It describes the intended
contract encoded by the skills, not verified fleet conformance.

## Intended architecture

```text
Public client
  |
  | Authorization: Bearer <access token>
  v
Gateway
  |-- verifies the end-user access token
  |-- strips spoofable trusted headers
  |-- projects verified claims into trusted headers
  |-- optionally asks the request-time authz checker
  v
Backend service
  |-- normalizes trusted context once at ingress
  |-- enforces exact coarse permissions
  |-- enforces tenant and business invariants
  `-- never verifies the end-user bearer token

Fine-grained authorization write path:
entitlement-api -> event -> projector -> OpenFGA

Fine-grained authorization read path:
gateway -> authz-sidecar or entitlement-spoa -> OpenFGA check
```

## Authentication

- `auth` is the identity, sign-in, access-token, refresh-session, and profile source of truth.
- Public login is an OTP request followed by OTP verification.
- Auth issues the access token. The refresh token is carried in an HttpOnly cookie and rotated on refresh.
- The gateway is the only component that verifies an end-user bearer token for gateway-fronted routes.
- A normal backend must not parse, validate, introspect, refresh, or otherwise consume that bearer token.
- The gateway projects verified claims into trusted headers, including:
  - `pid` -> `X-Project-Id`
  - `sub` -> `X-User-Id`
  - `prm` -> `X-Access`
  - `rol` -> `X-User-Roles`
  - selected token, profile, and location claims -> their declared trusted headers
- The gateway strips client-supplied copies of trusted headers on public and protected routes before
  injecting verified values.
- Actor and tenant context come from verified token claims, never from request bodies, query parameters,
  route parameters, or client-supplied internal headers.

## Coarse authorization

- The permission catalog is the sole allocator of permission names and global bitmap ids.
- Auth compiles the user's current coarse permissions into the compact `prm` bitmap.
- The gateway does not interpret the bitmap; it forwards it as trusted `X-Access`.
- Each backend decodes `X-Access` once at ingress using the canonical decoder and its generated,
  committed service permission map.
- Application checks use permission names, not bitmap ids.
- Unknown bits grant nothing. A server-side protected request resolving to zero known permissions fails
  closed.
- The backend role contract is frozen: `rol` and `X-User-Roles` are passive metadata and must not decide
  access, policies, scopes, response shape, routing, validation, workflow, or side effects.
- Exact permissions cannot be bypassed by a broad role such as `admin`.

## Fine-grained authorization

- Coarse permissions answer whether the caller may use a service capability.
- OpenFGA answers whether this caller may perform an operation on this specific object.
- `entitlement-api` owns normalized authorization business truth.
- `projector` is the only intended OpenFGA tuple writer.
- OpenFGA stores derived effective authorization state; it is not the business source of truth.
- The gateway calls `authz-sidecar` or `entitlement-spoa` for configured route families.
- The checker maps an endpoint category and target type to one final `can_*` relation and performs a
  pinned OpenFGA check.
- Runtime checks use final `can_*` relations. Grant and deny tuples are write-side inputs, not the
  relation checked by normal request-time callers.
- A frontend or normal backend must not call the sidecar or OpenFGA directly.
- Allow-side `X-Authz-*` values are observability metadata, not a backend credential or authorization
  input.
- Even after gateway and OpenFGA allow, the backend still enforces tenant boundaries, ownership,
  validation, business invariants, and data-safety rules.

## TOTP and step-up

- Auth alone owns the TOTP credential and validates raw TOTP and recovery codes.
- Enrollment is optional unless a route explicitly requires step-up for a stable, action-specific
  purpose.
- Enrollment follows status -> enroll -> client-generated QR from `otpauth_uri` -> confirm.
- A sensitive operation first produces `TOTP_STEP_UP_REQUIRED` with the required purpose.
- The client sends a fresh TOTP or recovery code to auth's step-up endpoint.
- Auth returns a short-lived opaque signed proof bound to user, applicable project or tenant, purpose,
  proof id, issue time, expiry, and issuer.
- The client retries the original request with public `X-TOTP-Proof`.
- The gateway consumes and verifies the raw proof and injects only:
  - `X-TOTP-PURPOSE`
  - `X-TOTP-VERIFIED-UNTIL`
  - `X-TOTP-PROOF-ID`
- The backend never sees the raw proof and never validates a TOTP code.
- The backend must compare the injected purpose with the operation's required purpose and must reject an
  expired proof. The gateway validates that a purpose claim exists but does not know each route's required
  purpose.
- TOTP is additive. It does not replace authentication, coarse permissions, OpenFGA, tenant scoping, or
  business authorization.

## Service interaction rules

- Public clients call documented gateway routes and never service-local or internal authz routes.
- Services normalize trusted context once at ingress; controllers, policies, repositories, and jobs do
  not repeatedly parse raw trusted headers.
- Tenant-aware reads and writes are all scoped by trusted tenant context.
- A client-provided selector that disagrees with trusted context is denied.
- Synchronous service-to-service calls are reserved for real internal dependencies; domain integration
  should prefer the owning service's API or events instead of direct table coupling.
- Internal calls preserve request and trace correlation and use explicit timeout and retry budgets.
- Internal service-to-service mTLS is described as a deferred coordinated platform initiative. Private
  networking and trusted headers are not to be described as cryptographic service authentication.

## Fail-closed posture

- A request that bypasses the gateway cannot make trusted headers trustworthy.
- Missing required identity or tenant context denies.
- Missing, malformed, or unusable `X-Access` denies at ingress.
- Request-time authorization failure denies; the backend must not add a fallback.
- Missing, mismatched, or expired TOTP proof metadata denies a step-up-required operation.
- Stale coarse-permission revocation remains effective until access-token refresh, expiry, or session
  revocation because the authorization-version claims are not forwarded to services.

## Contract drift visible inside the skills

These points require resolution or live-source verification before implementation:

1. Request-time checker failure is described as `403 AUTHZ_DENIED` in the trust-boundary fail-closed
   reference, but the OpenFGA request-time reference defines gateway-owned `503 AUTHZ_*` responses for
   timeout, unavailability, and pin failures.
2. The backend role-freeze reference forbids role-derived authorization, while a downstream-normalization
   paragraph says a service defines role derivation from decoded permissions. The explicit role-freeze
   reference claims precedence, so role-derived backend decisions remain forbidden.
3. The shared boundary requires UUIDv7 `project_id`, while the auth v3 reference records a current
   positive-integer parser as migration compatibility. The numeric behavior must not be generalized into
   the platform contract.
4. The TOTP enrollment contract intentionally returns `secret`, `otpauth_uri`, and recovery codes once to
   the client, while the auth v3 reference also says these values never leave auth. Those statements cannot
   both be literal; the intended safe interpretation is that enrollment material may cross only the
   explicit one-time enrollment response and must never reach logs, analytics, unrelated services, or
   persistent client storage.

## What this assessment cannot establish

- Whether the current gateway, auth, entitlement, or downstream repositories implement these contracts.
- Which route groups are active in a deployed environment.
- Whether current OpenFGA store and model pins agree.
- Whether every service consumes generated permission maps and canonical decoders.
- Whether the documented auth and TOTP migration states are still current.
- Whether the fleet currently passes the stated fail-closed and conformance tests.

Those are implementation and runtime questions and require source or rendered-runtime inspection, which
was intentionally excluded.

## Skill sources used

- `alaa-services-contract`
- `alaa-trust-gateway-auth`
- `alaa-permission-generator`
- `alaa-prompting-guide` (repository-required consultation; it did not supply platform contract facts)
