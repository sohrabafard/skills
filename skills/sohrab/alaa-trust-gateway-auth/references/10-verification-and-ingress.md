# What the gateway verifies, and what enters behind it

Read this file when you are changing gateway verification order, the public-route
list, path-prefix stripping, or the sanitize step; or when you need to know which
route shape a piece of code is written against.

## Verification order on a protected route

The gateway (HAProxy) applies these checks in this order:

1. A bearer token exists.
2. The JWT `alg` value is on the allow-list. **This runs before verification**, not
   after, because an allow-list applied after the algorithm has already been used
   to select a verifier does not prevent algorithm confusion.
3. The signature is valid for the mounted public key.
4. The token has a usable `exp`.
5. The token is not expired, within the configured clock skew.
6. The token is not before `nbf`, within the configured clock skew.
7. Every required claim is present.
8. Issuer and audience checks run when configured.

Deployment values observed in the current render: allowed algorithm `RS256`, clock
skew 30 seconds, required claims `pid` and `sub`. Issuer and audience validation
exist in the template and are inactive because both lists are empty. Re-derive
these from the gateway repository before relying on them; they are deployment
values, not contract.

## What the gateway does not do

- It does not perform business authorization and does not decide whether a user may
  perform a domain action.
- It does not evaluate `X-Access` or `X-USER-SCOPES` for route permission.
- It does not consume any service's generated permission map and owns no
  permission-name-to-bitmap-id mapping.
- It does not derive tenant from hostname, path prefix, body or query string.
- It does not introspect opaque tokens. **If any README or design note still
  describes opaque-token passthrough, or the retired profile-blob header contract,
  that text is drift to remove rather than a compatibility state to preserve.** A
  service built against either will fail closed at the first request, because
  neither is implemented anywhere in the current path.

## Sanitize runs on every route

The gateway deletes every spoofable inbound auth and context header before
proxying, and this step runs on public routes as well as protected ones. A public
route skips token verification; it does not skip sanitizing. Without that, a
public route is a direct channel for a client to hand a backend a chosen
`X-User-Id`.

The delete list covers the whole trusted-header set — the identity, token-metadata,
name and location headers, `X-User-Roles`, and the three backend-only `X-TOTP-*`
names — plus a wildcard sweep of `x-location-*`, `x-authz-*` and `x-totp-*`, which
spares only the public proof carrier `X-TOTP-Proof`. The authoritative list of
names lives with the gateway configuration; the frozen contract-level set is owned
by `alaa-services-contract` `references/30-trusted-ingress-and-laravel-contract.md`.

**Every header the gateway injects also appears in the delete list, and the delete
list runs unconditionally.** A header that is injected but not deleted is forgeable
by any public client, and no amount of service-side care detects the forgery,
because the forged value is byte-identical to a real one. Prose cannot catch this
class of defect — the two lists live hundreds of lines apart in one template.
`scripts/trust_boundary_check.py --gateway-config <path>...` checks the symmetry
mechanically, and a finding there is fixed in the gateway configuration before any
service-side change ships.

## Public routes

The gateway currently treats these paths as public and skips token verification:

- `/auth/api/v3/otp/request`, `/auth/api/v3/otp/verify`, `/auth/api/v3/token/refresh`,
  `/auth/api/v3/logout`
- `/auth/api/ready`, `/auth/api/health`
- `/vod/api/ready`, `/vod/api/health`
- `/comment/api/ready`, `/comment/api/health`
- `/ticket/api/ready`, `/ticket/api/health`
- `/wa/api/ready`
- `/healthz`
- `/wa/ingest/v1/events`

A public path at the gateway is not permission to trust the caller. The service
behind it applies its own route-level rules, and it receives no trusted context to
lean on.

**When a route must always carry an access token, remove it from the public list.**
Do not teach a downstream service to partially trust missing auth context, because
that moves the decision from one auditable list into every service's middleware.

## Gateway-facing routes versus service-local routes

This distinction is mandatory, and getting it wrong produces a service whose
documented routes do not exist.

- A client calls the gateway-facing route, which carries the service prefix the
  gateway routes on: `/auth`, `/vod`, `/comment`, `/ticket`, `/wa`.
- When `stripPathPrefix: true`, the gateway removes that prefix before proxying.
- The backend therefore implements and documents the **service-local** shape.

Gateway-facing `/auth/api/v3/otp/request` is service-local `/api/v3/otp/request`.
Gateway-facing `/auth/api/health` is service-local `/api/health`.

Write gateway-facing routes when the subject is the gateway. Write service-local
routes when the subject is a backend. A backend carries the gateway prefix in its
own route definitions only when the gateway's routing configuration for that
service sets `stripPathPrefix: false`; read that value before writing either
shape, because guessing produces routes that answer 404 in one environment and
work in another.

## The tenant boundary and its names

`tenant_id`, `tenant_public_id`, `project_id` and the compact claim `pid` are one
concept expressed at four layers. The canonical form per layer is fixed:

| Layer | Canonical name |
|---|---|
| Compact JWT claim | `pid` |
| Public API field | `project_id` |
| Trusted header | `X-Project-Id` |

Rename `tenant_id` and `tenant_public_id` to `project_id` at public API and
service-domain boundaries, and to `pid` only inside compact JWT claim mapping.
Rename `X-Tenant-Public-Id` to `X-Project-Id`. Keep trust semantics unchanged
while renaming: a rename that also changes who may assert the value is not a
rename.

Validate the public boundary value as UUIDv7 after gateway verification. Example:
`018f7d8f-8cb0-7a85-9a89-e3f61052f840`.

A service that still keeps an internal numeric project key translates the trusted
public boundary into that key at ingress and keeps the numeric key out of trusted
headers, public API examples and every other public-facing contract. The numeric
key is service-local storage, not the boundary.

Where a legacy alias still appears in OpenAPI, a README or a service doc, mark it
explicitly as legacy and equivalent to the public boundary rather than documenting
it as a second concept.

## Auth-service route drift that must not be copied forward

Auth-service is `v3` only and exposes no `/api/v2` routes. Any gateway or repository
document still naming `/auth/api/v2/*` is drift to remove, not active client
guidance. Do not reintroduce `/api/v2`, and do not teach a new service or caller to
depend on a retired auth v2 route or a one-step `/login` path.

Route families and the current client flow are in
`references/60-auth-service-v3-contract.md`.
