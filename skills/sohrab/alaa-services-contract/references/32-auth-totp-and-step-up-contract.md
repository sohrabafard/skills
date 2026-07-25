# Auth TOTP And Step-Up Contract

Use this file when the task touches auth TOTP management, optional MFA setup, forced route-level TOTP enforcement, SDK/client handling of TOTP errors, QR setup UX, or `require_totp:<purpose>` rollout.

## Source priority

For the current auth implementation, trust these sources in order. Every path is relative to the root of
the `auth` repository checkout; resolve them there and never hardcode an absolute machine path.

1. `routes/api.php`
2. `bootstrap/app.php`
3. `app/Http/Controllers/Api/V3/TotpController.php`
4. `docs/contracts/auth/endpoints/totp.md`
5. `docs/contracts/auth/flows/totp-enrollment.md`
6. `docs/contracts/auth/flows/totp-step-up.md`
7. `docs/ops/totp-step-up-mechanism.md`

If implementation and docs disagree, trust route/controller/middleware source first, report contract drift, and align docs plus API artifacts before closing the task.

## Feature flag and availability

- TOTP management is feature-flagged by `AUTH_TOTP_ENABLED` through `auth.totp.enabled`.
- When disabled, `/api/v3/totp*` answers HTTP 404 with body `{ "message": "TOTP feature is disabled." }`.
- Clients normalize that response as `totp_unavailable` and hide or disable the TOTP setup UI. Never treat it as an ordinary missing route, because a missing route means a deploy defect and this means a flag is off.
- When enabled, self-service setup routes are usable by any authenticated user, and enrollment is never forced by the flag alone. Only `require_totp:<purpose>` on a route forces it.
- In image-first or cached-config runtimes, changing `AUTH_TOTP_ENABLED` requires refreshing config and recreating affected app/worker containers as appropriate.

## Public versus internal route shape

- Browser, mobile, and SDK clients call the gateway public prefix, normally `/auth/api/v3/totp*`, with `Authorization: Bearer <access token>`.
- Public clients must never send trusted internal headers such as `X-User-Id`, `X-Project-Id`, `X-Access`, `X-User-Role`, or gateway-forged profile headers.
- Backend-local `/api/v3/totp*` examples are only for direct service tests, trusted gateway tests, and internal documentation.
- Preserve normal auth, role, permission, tenant/project, and business authorization checks. TOTP is a step-up proof, not a replacement for authorization.

## Optional enrollment lifecycle

1. Client calls `GET /auth/api/v3/totp` to read status.
2. If `enabled=false`, client may show setup UI.
3. Client calls `POST /auth/api/v3/totp/enroll` with an empty body.
4. Backend responds with `secret`, `otpauth_uri`, `recovery_codes`, and `status.enabled=false`.
5. Backend does not return a QR image. The client generates a QR code from `otpauth_uri` and also shows the manual `secret` fallback.
6. User scans the QR code in an authenticator app such as Google Authenticator, Microsoft Authenticator, 1Password, or Bitwarden.
7. User enters the 6-digit code from the authenticator app.
8. Client calls `POST /auth/api/v3/totp/confirm` with `{ "code": "123456" }`.
9. TOTP is enabled only after confirm succeeds.
10. Client shows recovery codes once and never logs, persists, or sends them to analytics.

Never log or persist TOTP `secret`, `otpauth_uri`, user-entered TOTP codes, or recovery codes outside the intended secure storage and one-time display path.

## Forced route-level TOTP

To force TOTP on a sensitive route, keep the route behind the normal authenticated gateway/trusted flow and add `require_totp:<purpose>`.

Example Laravel route shape:

```php
Route::middleware('auth:trusted_gateway')->group(function (): void {
    Route::delete('sessions', [SessionController::class, 'destroyAll'])
        ->middleware('require_totp:auth.sessions.revoke_all');
});
```

Purpose rules:

- Use stable, action-specific purpose names, such as `auth.sessions.revoke_all`, `profile.write`, `profile.photo`, or `catalog.school.write`.
- The purpose scopes the short-lived proof, not the authenticator enrollment. One authenticator-app entry serves all purposes.
- A successful step-up for one purpose must not unlock a different purpose.
- Do not use generic names such as `default`, `admin`, `write`, or route paths that may change.
- Do not silently attach forced TOTP. Update route docs, OpenAPI, Postman, SDK/client notes, tests, and rollout notes.

## Site-level credential and purpose-scoped proof

- The platform uses one site-level TOTP enrollment per user. The authenticator entry created during setup is not tied to
  one downstream route or service.
- The `purpose` is attached to each short-lived proof, not to the stored authenticator secret. Use purpose-specific
  proof when the same user must re-authenticate for a sensitive action.
- A future separate setup domain may introduce a different enrollment purpose only if the repository contract explicitly
  documents that new credential boundary. Do not create a new authenticator setup for ordinary force-TOTP routes.

## Signed proof-token target

The target cross-service flow is signed proof-token based:

1. The client calls the protected route normally.
2. The gateway or backend returns a TOTP challenge with the required `purpose`.
3. The client calls `POST /auth/api/v3/totp/step-up` with that `purpose` and a fresh TOTP code or recovery code.
4. Auth verifies the code against the user's enabled site-level TOTP credential and returns:

```json
{
  "purpose": "content.bulk_delete",
  "verified_until": "2026-07-04T12:05:00Z",
  "proof_token": "<opaque signed proof token>"
}
```

The proof token must bind at least user, project or tenant context where applicable, purpose, proof id, issued time,
expiry, and issuer. The token must be opaque to public clients. Public docs and examples must use placeholders only.

## Client proof cache

The client may cache the returned `proof_token` in its auth-state storage, similar to an access token, until
`verified_until`.

Rules:

- Cache by user/session, project or tenant context where applicable, and purpose.
- Do not cache, log, persist, serialize, or replay the submitted TOTP code.
- Do not create a refresh token for TOTP proof. When the proof expires or the gateway rejects it, prompt for a new TOTP
  code and obtain a fresh proof through `POST /auth/api/v3/totp/step-up`.
- Clear cached proofs on logout, account switch, project switch, TOTP disable/reset, token/session revocation,
  permission context changes, explicit step-up failure, or proof expiry.

## Gateway and downstream service contract

Public clients retry force-TOTP routes with only:

```http
X-TOTP-Proof: <opaque signed proof token>
```

Gateway responsibilities:

- Strip any inbound trusted backend `X-TOTP-*` headers from public requests.
- Verify `X-TOTP-Proof` signature, issuer, expiry, user/session binding, project binding where applicable, and purpose.
- Forward only gateway-verified backend metadata to the downstream service:
  - `X-TOTP-PURPOSE`
  - `X-TOTP-VERIFIED-UNTIL`
  - `X-TOTP-PROOF-ID`

Downstream service responsibilities:

- Never validate raw TOTP codes.
- Never trust public `X-TOTP-*` metadata.
- Enforce only route/business purpose policy against gateway-verified proof metadata after normal authentication,
  authorization, tenant, and business checks remain in place.

## Client challenge handling

Clients and SDKs model forced TOTP as a challenge-and-retry flow:

- On `TOTP_STEP_UP_REQUIRED`, preserve the original request intent, show a TOTP challenge, call `POST /auth/api/v3/totp/step-up` with the same purpose plus `code` or `recovery_code`, cache the returned `proof_token` until `verified_until`, then retry the original request with public `X-TOTP-Proof`.
- On `TOTP_REQUIRED`, guide the user through status, enroll, confirm, and then step-up or retry the original action if it still requires proof.
- On `TOTP_UNAVAILABLE`, show a controlled unavailable state and report rollout/config drift to operators.
- On `TOTP_STEP_UP_FAILED` or `TOTP_DISABLE_FAILED`, keep the challenge open and do not update local enabled state.
- On `TOTP_RATE_LIMITED`, stop retries until the returned retry window expires.
- On `AUTH_LIMITER_UNAVAILABLE`, fail closed with a temporary unavailable state.

## SDK and frontend contract

A public SDK exposes explicit operations for:

- `getTotpStatus`
- `enrollTotp`
- `confirmTotp`
- `regenerateTotpRecoveryCodes`
- `disableTotp`
- `verifyTotpStepUp`

SDK/frontend expectations:

- Keep the auth base URL and gateway prefix configurable.
- Generate the QR code client-side from `otpauth_uri`; do not expect a server-generated image unless implementation changes and the public contract is updated.
- Invalidate cached TOTP status and pending challenge state after TOTP mutations.
- Return the step-up `proof_token` to host code but do not store it inside the SDK unless the host explicitly delegates a
  storage adapter with the cache and clear rules above.
- Do not cache mutation responses that contain secrets or recovery codes.
- Ensure SSR builds do not render browser-only QR libraries on the server without a client-only guard.
- Never include trusted gateway headers in public SDK examples.

## Review

The TOTP and step-up review checklist is owned by `$alaa-security-review`, so that a reviewer who loads
that skill sees it. This file owns the shapes it triggers against: the public versus internal route shape,
the `otpauth_uri`-not-an-image setup contract, the purpose naming rules, the proof-token binding
requirements, the client proof-cache rules, and the gateway and downstream header responsibilities above.
When a change touches any of those shapes, load `$alaa-security-review` and run its checklist against
them.
