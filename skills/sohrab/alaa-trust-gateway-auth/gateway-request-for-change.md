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
- `wa`
