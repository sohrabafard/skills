# Auth-service v3 contract and route shapes

Read this file when the task is about auth-service endpoint behaviour, the client
integration order, direct local backend testing, or the current v3 route families.

## Where the truth is

Resolve auth-service endpoint questions from the auth repository, in this order.
Paths are repository-relative; check the repository out wherever your machine keeps
it and resolve them from its root.

1. `routes/api.php`
2. `docs/ops/auth-session-contract.md`
3. `docs/ops/auth-profile-v3-contract.md`
4. `docs/ops/totp-step-up-mechanism.md`
5. `docs/ops/postman/auth-service-v3.postman_collection.json`
6. `README.md`

When the documents and the route definitions disagree, `routes/api.php` wins,
because it is the thing that runs.

## The client flow

1. `POST /auth/api/v3/otp/request` with `{"mobile": "09120000000", "national_code": "1234567890"}`.
2. The client receives the OTP out of band.
3. `POST /auth/api/v3/otp/verify` with `{"mobile": "09120000000", "code": "11111"}`.
4. A successful verify returns `message`, `profile` and `token`, where
   `token.access_token` is the bearer JWT and `token.token_type` is `Bearer`.
5. The same response sets the refresh token in the HttpOnly `auth_refresh_token`
   cookie.
6. The client calls gateway-protected routes with
   `Authorization: Bearer <access token>` on the gateway-facing route.
7. The gateway verifies the token and injects trusted headers.
8. When the access token expires or is rejected, the client calls
   `POST /auth/api/v3/token/refresh`.
9. A successful refresh rotates the refresh token, returns a new access token and
   replaces the cookie.
10. `POST /auth/api/v3/logout` revokes the current refresh-token session.

Request details:

- OTP request, OTP verify and refresh send `Accept: application/json` and
  `Content-Type: application/json`.
- The Postman collection also sends `X-Request-Id` and `X-Device-Id` on those public
  requests. `X-Device-Id` is optional client metadata for auth-service. It is not a
  trusted gateway auth header, it is not sanitized as one, and no authorization
  decision reads it.
- Refresh takes the refresh token from the `auth_refresh_token` cookie first. Its
  body includes `access_token` and may include `device_id`. A missing or
  non-string-shaped `access_token` returns `422`; a missing refresh cookie returns a
  `401` session-expired response.
- `POST /auth/api/v3/logout` is public in the auth-service contract and revokes from
  either `refresh_token` in the body or the cookie.
- Do not teach a client to depend on a retired `/auth/api/v2/*` route or a one-step
  `/login` path. The active contract is OTP request then OTP verify.

## Protected route families

Gateway-facing:

- `/auth/api/v3/sessions*`
- `/auth/api/v3/totp*`
- `/auth/api/v3/admin/users/{user_uuid}/sessions*`
- `/auth/api/v3/admin/users/{user_uuid}/totp`
- `/auth/api/v3/admin/users/{user_uuid}/authz-overrides*`
- `/auth/api/v3/profile*`

Service-local, after prefix stripping: the same paths without the `/auth` prefix.

### Sessions

`GET /auth/api/v3/sessions` lists session families for the authenticated user.
`DELETE /auth/api/v3/sessions/{session}` revokes one family or access-token session.
`DELETE /auth/api/v3/sessions` revokes every active session for the user.

### TOTP management and step-up

- `GET /auth/api/v3/totp` returns TOTP status.
- `POST /auth/api/v3/totp/enroll` starts enrolment; on an enabled factor it answers
  `409 TOTP_ALREADY_ENABLED` and changes nothing (auth
  `app/Services/Security/TotpService.php`).
- `POST /auth/api/v3/totp/confirm` takes `{"code": "123456"}`.
- Enroll and confirm also need a fresh SMS-OTP login (`totp_fresh_login`;
  `references/30-fail-closed-cases.md` case 10).
- `POST /auth/api/v3/totp/recovery-codes/regenerate` takes `{"code": "123456"}`.
- `POST /auth/api/v3/totp/step-up` takes `purpose` plus either `code` or
  `recovery_code`, and returns the proof the client presents in `X-TOTP-Proof`.
- `DELETE /auth/api/v3/totp` takes either `code` or `recovery_code`.
- Purpose names are free-form, restricted to letters, digits, `.`, `_`, `:` and `-`.
- Step-up proof is purpose-specific: a proof for `profile.write` does not satisfy
  `profile.photo`, and the comparison that enforces this runs in the backend, never
  at the gateway. See `references/20-claims-headers-and-sentinels.md` for the
  headers and `references/30-fail-closed-cases.md` for every denial case.
- The enrolment secret, the `otpauth_uri`, a raw TOTP code and a recovery code never
  leave auth and never appear in a log anywhere.

### Admin authorization overrides

`GET /auth/api/v3/admin/users/{user}/authz-overrides` supports optional `project_id`
and `service_key` filters. `PUT` takes a body shaped like
`{"permission_key": "school_post", "effect": "deny", "project_id": 42, "service_key": "auth-profile"}`.
`DELETE` uses the same selectors without `effect`. Admin session revocation is
`DELETE /auth/api/v3/admin/users/{user}/sessions` and
`DELETE /auth/api/v3/admin/users/{user}/sessions/{session}`.

The admin TOTP reset `DELETE /auth/api/v3/admin/users/{user_uuid}/totp` needs
`auth_admin_users_totp_reset` and a gateway-verified step-up for purpose
`auth.totp.admin_reset:<user_uuid>`; peer protection refuses it with
`403 TOTP_ADMIN_RESET_FORBIDDEN` (auth `app/Services/Admin/TotpAdminResetGuard.php`).

### Live-token guard

`reject_revoked_access_token` runs on TOTP enroll, confirm, recovery-codes
regenerate, step-up and disable, on the admin TOTP reset, on the authz-override
`PUT` and `DELETE`, and on both admin session revoke routes (`DELETE .../sessions` and
`DELETE .../sessions/{session}`; auth `routes/api.php`). On the session revoke routes
it runs before `access_permission`, so a revoked or missing token gets
`401 SESSION_EXPIRED` ahead of any `403 AUTHZ_DENIED`, and nothing is revoked. Denials
are `references/30-fail-closed-cases.md` case 9.

### Profile

`GET /auth/api/v3/profile` returns the canonical profile projection. `PATCH` and
`PUT` accept sectioned JSON with `identity`, `contact`, `location`, `health` and
`academic` objects. `GET /auth/api/v3/profile/catalogs`,
`/profile/academic-history` and `/profile/assignment-history` are trusted-gateway
reads. `POST /auth/api/v3/profile/photo`, `POST /auth/api/v3/profile/national-card`
and `GET /auth/api/v3/profile/national-card` are trusted-gateway routes.

## Auth-service's own trusted-header contract

Auth-service's target trusted-gateway contract consumes the existing `X-User-Id`
as the canonical Auth user UUIDv7 and `X-Project-Id` as the public project UUIDv7.
On routes requiring an actor, missing, malformed, or wrong-version user identity
fails closed under the existing route error policy; guest, tokenless, and public
routes retain their optional-actor semantics. Auth resolves the UUID to its private
numeric `users.id` only inside Auth. Route
middleware also reads `X-Access` (`access_permission`; auth
`app/Support/Auth/TrustedAccessPermissionSet.php`), `X-Access-Token-Id`
(`reject_revoked_access_token`, `totp_fresh_login`) and the three `X-TOTP-*` step-up
headers (`gateway_step_up`; auth `app/Http/Middleware/RequireGatewayStepUpProof.php`).
Auth does not read `X-User-Roles`, `X-User-Mobile`, the `X-TOKEN-*` headers,
`X-USER-SCOPES`, or the name and location headers on its v3 routes (verified
2026-10-20 at auth `77977c3`). No extra backend-only signature header is required: the trust boundary is
the sanitized gateway path plus the injected identity headers.

**Do not freeze that positive-integer parser into the shared public contract.**
Translate the trusted public user UUID to the internal numeric key only at Auth's
own storage boundary. The public project boundary remains UUIDv7 `pid`.

**Identity target (approved 2026-10-21; adoption not asserted here).** Auth's
existing `users.uuidv7` is the sole public user ID. Access-token `sub`, TOTP proof
`sub`, and the existing `X-User-Id` projection use that same UUID; issuance,
refresh, and session paths preserve the alignment. Admin target-user paths use the
same UUID, while Auth may resolve it to `users.id` internally. UUID possession is
not authorization. The canonical shape and first-release compatibility limit are
owned by `/alaa-services-contract` references `25` and `22`.

## Direct local backend testing

The auth Postman collection tests protected routes directly against service-local
`/api/v3/*` URLs such as `http://localhost/api/v3/sessions`, sending `X-User-Id` and
`X-Project-Id` instead of a bearer token, because auth-service does not parse a
bearer locally on its protected v3 routes.

This is backend-only local testing. It is not the public client contract and it is
never copied into browser or mobile client guidance. The collection's numeric
fixtures — `gatewayProjectId=1`, `project_id: 1` in profile examples — are the
auth-service local compatibility state during migration, and they are not a reason
to weaken the shared trust model or to let a client choose tenant context.

A service that accepts trusted headers on a locally reachable listener has the
exposure described in `references/30-fail-closed-cases.md` case 1, and closes it the
same way.

## Response and observability facts

- Every `/api/*` route is JSON-only on both success and error paths.
- A resource response wraps only the top-level payload in `data`; nested child
  resources are inline objects.
- The `/api/*` response-header contract is `X-Request-Id` plus `traceparent`. An
  inbound `X-Request-Id` or a valid inbound `traceparent` is preserved.
- `X-Correlation-Id`, wherever auth-service still emits or documents it, is
  migration drift to remove rather than a compatibility state to preserve.
