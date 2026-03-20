# Gateway Request For Change

## Purpose
Track gateway changes requested by downstream service analysis so they can be reviewed and applied in the gateway repository after the shared auth skill is finalized.

## Requested changes

### 1) Remove WA ingest from gateway public routes
- Service: `wa`
- Requested outcome:
  - `WA` ingest must no longer be treated as a public route at the gateway.
  - Requests to the WA ingest route must carry `Authorization: Bearer <token>`.
  - Gateway must verify the token and inject the normal trusted auth/context headers before proxying.
- Why:
  - WA should always receive trusted tenant and actor context from the gateway.
  - Leaving WA public creates ambiguity about whether downstream code may trust missing or absent auth context.
  - This change keeps the trust model simple: WA is behind authenticated gateway flow, not mixed public/private behavior.
- Expected downstream effect:
  - `X-PROJECT-ID` remains required.
  - `X-USER-ID` and other verified token-derived headers are expected to be injected normally after verification.
  - WA should not need special-case logic that assumes missing access token on its normal gateway route.

### 2) Always sanitize spoofable internal auth/context headers on all routes, including public routes
- Scope: gateway-wide
- Requested outcome:
  - Gateway must delete spoofable inbound internal auth/context headers on every route before proxying.
  - This sanitize step must run even on public routes where the gateway does not inject verified auth context.
- At minimum sanitize these headers:
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
- Why:
  - Backend services should not need route-by-route confusion about whether a client-supplied internal header might survive on a public path.
  - Public route must not mean client can smuggle trusted internal header names downstream.
  - The safe invariant is: clients can never set internal auth/context headers for downstream services.
- Required behavior split:
  - Public route: sanitize spoofable internal headers, then proxy without verified auth injection unless explicitly configured otherwise.
  - Protected route: sanitize spoofable internal headers, verify token, then inject trusted auth/context headers.

## Recommended target standard
- Public vs protected should change whether the gateway verifies and injects auth context.
- Public vs protected should not change whether spoofable internal headers are sanitized.
- Downstream services should be able to rely on one invariant:
  - client-supplied internal auth/context headers never pass through the gateway unchanged.

## Requested by current service analysis
- `auth`
- `wa`

### 3) Replace retired auth v2 public routes with explicit auth v3 route mapping
- Service: `auth`
- Requested outcome:
  - Remove retired auth public routes from the gateway:
    - `/auth/api/v2/login`
    - `/auth/api/v2/otp/request`
    - `/auth/api/v2/otp/verify`
    - `/auth/api/v2/token/refresh`
    - `/auth/api/v2/logout`
  - Add the current auth public routes instead:
    - `/auth/api/v3/otp/request`
    - `/auth/api/v3/otp/verify`
    - `/auth/api/v3/token/refresh`
    - `/auth/api/v3/logout`
  - Keep `/auth/api/health` public.
  - Do not require or inject any extra backend-only `X-Gateway-Signature` header for auth-service trusted routes.
- Required explicit mapping:
  - `/auth/api/v2/login` -> replace with the v3 two-step login flow: first `POST /auth/api/v3/otp/request`, then `POST /auth/api/v3/otp/verify`
  - `/auth/api/v2/otp/request` -> `POST /auth/api/v3/otp/request`
  - `/auth/api/v2/otp/verify` -> `POST /auth/api/v3/otp/verify`
  - `/auth/api/v2/token/refresh` -> `POST /auth/api/v3/token/refresh`
  - `/auth/api/v2/logout` -> `POST /auth/api/v3/logout`
- Why:
  - Auth-service is now `v3` only and no longer exposes `/api/v2` routes locally.
  - The gateway already routes by the leading `/auth` prefix and strips that prefix before proxying, so auth-service should not keep a second inner `/auth` segment in its own v3 routes.
  - Auth-service now trusts the sanitized gateway boundary plus required injected `X-USER-ID` and `X-PROJECT-ID` headers, so a second backend-only signature header should not remain in the shared platform contract.
  - The shared skill should not teach new services or clients to depend on retired auth v2 gateway paths or the old duplicated `/auth/api/v3/auth/*` shape.
  - `POST /api/v3/logout` remains intentionally public in the current auth repo because it can revoke the refresh token from cookie or request body without requiring trusted gateway headers.
- Expected downstream effect:
  - Gateway-facing auth public routes match the current auth repo contract again.
  - Service-local auth public routes after prefix stripping are now:
    - `/api/v3/otp/request`
    - `/api/v3/otp/verify`
    - `/api/v3/token/refresh`
    - `/api/v3/logout`
  - Protected auth-service routes such as `/api/v3/profile*`, `/api/v3/sessions*`, `/api/v3/totp*`, and admin trusted-gateway routes stay behind the normal protected gateway flow.
