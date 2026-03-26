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
