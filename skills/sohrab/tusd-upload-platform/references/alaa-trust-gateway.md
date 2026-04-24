# Ala Trust Gateway for tusd

## Contents

- [Core Rule](#core-rule)
- [Trusted Context](#trusted-context)
- [Method Authorization](#method-authorization)
- [Upload Session Flow](#upload-session-flow)
- [Frontend Boundary](#frontend-boundary)
- [Ownership Store](#ownership-store)
- [Anti-Patterns](#anti-patterns)

## Core Rule

Ala public clients call the gateway. The gateway is the external trust boundary: it verifies bearer tokens, strips spoofable internal headers, injects trusted identity/project context, optionally calls request-time authorization, and forwards to the correct backend. Downstream services still own normalized request handling, upload ownership, and business authorization.

## Trusted Context

The upload service may rely on these only after the trusted gateway path injected them:

- `X-Project-Id`: tenant/project boundary.
- `X-User-Id`: authenticated actor.
- `X-Access`: verified access bitmap/context.
- `X-Access-Token-Id`: token id for audit/revocation correlation.
- `X-User-Mobile`, `X-User-Fname`, `X-User-Lname`, and `X-Location-*`: optional compact profile/location context.
- `X-Request-Id` and `traceparent`: correlation/tracing only, never authorization.

Browser code must not create or forward trusted internal headers.

## Method Authorization

| Method | Required control |
|---|---|
| `OPTIONS` | CORS policy for approved origins and headers; avoid exposing trusted internal headers. |
| `POST /files/` | Gateway auth, upload-session validation, tenant/user binding, metadata allowlist, size/type policy. |
| `HEAD /files/{id}` | Gateway auth plus upload ownership/session check before revealing offset. |
| `PATCH /files/{id}` | Gateway auth plus ownership/session check before accepting bytes. |
| `DELETE /files/{id}` | Gateway auth plus explicit cancel/termination policy. |
| `GET /files/{id}` | Disable by default or protect with a separate download/asset authorization flow. |

`pre-create` controls creation only. It does not protect resume, offset inspection, termination, or download by itself.

## Upload Session Flow

1. Vue calls an app API such as `POST /api/uploads/sessions` through the gateway.
2. PHP/Octane or Go control-plane code reads trusted context and validates business policy.
3. The control plane creates an upload record and returns safe client fields: endpoint or pre-created upload URL, app upload id, allowed metadata, max size, retry/resume policy, and expiration.
4. Vue starts tus-js-client through the gateway-facing endpoint.
5. `pre-create` validates the upload session and binds tus upload id to project/user/session.
6. Gateway or embedded middleware verifies `HEAD`, `PATCH`, and `DELETE` ownership for the upload id.
7. `post-finish` marks raw upload completion and enqueues durable downstream work.

## Frontend Boundary

Vue may keep local UI state, progress, resumability fingerprints, and a safe app upload id. Vue must not keep storage credentials, trusted headers, object keys, provider tokens, or final business truth.

When a token refresh is needed, refresh through the normal auth flow and then create or resume with fresh safe headers. Do not retry 401/403 blindly.

## Ownership Store

Persist at least:

- app upload id, tus upload id, upload URL path
- project id, user id, optional access token id
- state, size, offset, metadata allowlist values, storage target
- object key or local staging path generated server-side
- processing job id, provider id, final asset id when available
- request id, trace id, created/updated/finished/expires timestamps

## Anti-Patterns

- Vue sends `X-User-Id`, `X-Project-Id`, or `X-Access`.
- Gateway protects only `POST` but leaves `HEAD` or `PATCH` public.
- Client metadata controls tenant, object key, storage backend, or provider target.
- Upload URL is logged or sent to Sentry as a raw URL.
- Product UI treats tus completion as final asset readiness when scan/relay/transcode still has to run.
