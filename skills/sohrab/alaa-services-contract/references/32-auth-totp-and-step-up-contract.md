# Auth TOTP And Step-Up Contract

Use this file when the task touches auth TOTP management, optional MFA setup, forced route-level TOTP enforcement, SDK/client handling of TOTP errors, QR setup UX, or `require_totp:<purpose>` rollout.

## Source priority

For the current auth implementation, trust these sources in order:

1. `D:\Sohrab\Project\auth\routes\api.php`
2. `D:\Sohrab\Project\auth\bootstrap\app.php`
3. `D:\Sohrab\Project\auth\app\Http\Controllers\Api\V3\TotpController.php`
4. `D:\Sohrab\Project\auth\docs\contracts\auth\endpoints\totp.md`
5. `D:\Sohrab\Project\auth\docs\contracts\auth\flows\totp-enrollment.md`
6. `D:\Sohrab\Project\auth\docs\contracts\auth\flows\totp-step-up.md`
7. `D:\Sohrab\Project\auth\docs\ops\totp-step-up-mechanism.md`

If implementation and docs disagree, trust route/controller/middleware source first, report contract drift, and align docs plus API artifacts before closing the task.

## Feature flag and availability

- TOTP management is feature-flagged by `AUTH_TOTP_ENABLED` through `auth.totp.enabled`.
- When disabled, `/api/v3/totp*` should answer as unavailable, commonly HTTP 404 with `{ "message": "TOTP feature is disabled." }`.
- Clients should normalize this as `totp_unavailable` and hide or disable TOTP setup UI. Do not treat it as an ordinary missing route.
- When enabled, self-service setup routes should be usable by authenticated users without forcing every user to enroll.
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

## Client challenge handling

Clients and SDKs should model forced TOTP as a challenge-and-retry flow:

- On `TOTP_STEP_UP_REQUIRED`, preserve the original request intent, show a TOTP challenge, call `POST /auth/api/v3/totp/step-up` with the same purpose plus `code` or `recovery_code`, then retry the original request after success.
- On `TOTP_REQUIRED`, guide the user through status, enroll, confirm, and then step-up or retry the original action if it still requires proof.
- On `TOTP_UNAVAILABLE`, show a controlled unavailable state and report rollout/config drift to operators.
- On `TOTP_STEP_UP_FAILED` or `TOTP_DISABLE_FAILED`, keep the challenge open and do not update local enabled state.
- On `TOTP_RATE_LIMITED`, stop retries until the returned retry window expires.
- On `AUTH_LIMITER_UNAVAILABLE`, fail closed with a temporary unavailable state.

## SDK and frontend contract

A public SDK should expose explicit operations for:

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
- Do not cache mutation responses that contain secrets or recovery codes.
- Ensure SSR builds do not render browser-only QR libraries on the server without a client-only guard.
- Never include trusted gateway headers in public SDK examples.

## Review checklist

Flag the change when any of these appear:

- A public client sends trusted internal headers.
- Docs or SDK claim the backend returns a QR image while the implementation only returns `otpauth_uri`.
- Docs say TOTP is disabled while `AUTH_TOTP_ENABLED=true`, or docs imply forced route TOTP exists without route evidence.
- A forced-TOTP route lacks challenge-and-retry client guidance.
- TOTP is used instead of role/permission/business authorization.
- Purpose names are unstable, generic, user-controlled, or route-path-derived.
- OpenAPI, Postman, endpoint docs, flow docs, tests, or SDK contracts are not aligned with route behavior.
