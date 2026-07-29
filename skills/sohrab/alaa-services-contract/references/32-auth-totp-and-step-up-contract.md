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
  "proof_token": "<signed proof token>"
}
```

The proof token must bind at least user, project or tenant context where applicable, purpose, proof id, issued time,
expiry, and issuer. The proof token is a compact JWT signed by Auth. A public client treats it as an opaque bearer
credential, parses none of its claims and acts on none of them, because only the gateway's signature verification
makes any claim inside it trustworthy. Public docs and examples must use placeholders only.

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
X-TOTP-Proof: <signed proof token>
```

Gateway responsibilities:

- Strip any inbound trusted backend `X-TOTP-*` headers from public requests.
- Verify the `X-TOTP-Proof` token's `alg` against an allow-list before verifying its signature, then
  verify the signature, `typ`, `aud`, and `iss`, and check `exp` and `nbf` against the configured
  clock skew, because an algorithm chosen by the presenter defeats signature verification and a
  shared signing key makes `aud` the control that separates a proof from an access token.
- Bind the proof to the authenticated access token by requiring the proof's `sub` and `pid` to equal
  the access token's `sub` and `pid`, and inject no metadata when either differs, because an
  unbound proof is spendable by any authenticated caller who obtains it.
- Require `purpose` to be present and non-empty and forward it verbatim as `X-TOTP-PURPOSE`, because
  the gateway holds no route-to-purpose map and only the route's own service knows which purpose it
  requires.
- Send `X-TOTP-VERIFIED-UNTIL` as the proof's `exp` in Unix epoch seconds. The step-up response body's
  `verified_until` carries that same instant as an ISO 8601 string, so a service parses this header as an integer and
  never reuses a parser written against the response body.
- Set exactly these four backend-only headers, and no other `X-TOTP-*` name. This is the complete set a
  service behind the gateway may believe; a reader of this table needs no other list.

| Header | Set when | What a service may believe |
|---|---|---|
| `X-TOTP-PURPOSE` | the proof is fully valid | the verified `purpose` the proof was issued for |
| `X-TOTP-VERIFIED-UNTIL` | the proof is fully valid | the verified `exp`, in Unix epoch seconds |
| `X-TOTP-PROOF-ID` | the proof is fully valid | the verified `jti` |
| `X-TOTP-PROOF-REJECTED` | a proof was presented and none of the three above was set | why the proof bought nothing. Advisory only: it may change a message and must never change a decision. Owned by **Rejected-proof advisory header** below |

The gateway injects the first three headers only when the proof is fully valid, and injects none of them when
the proof is absent, expired, unbound, or wrongly signed. It returns no TOTP error and blocks no request in
either case, because it holds no route-to-purpose map and so cannot know whether the route being called requires
step-up at all. The step-up decision is therefore identical with and without the advisory header: a service that
requires step-up denies the operation whenever the three verified headers are absent, and reads
`X-TOTP-PROOF-REJECTED` only to say why it denied.

Downstream service responsibilities:

- Never validate raw TOTP codes.
- Never trust public `X-TOTP-*` metadata.
- Enforce only route/business purpose policy against gateway-verified proof metadata after normal authentication,
  authorization, tenant, and business checks remain in place.
- Read `X-TOTP-PROOF-REJECTED` only to choose a message. A service that never reads it behaves exactly as it
  did before the header existed.

## Rejected-proof advisory header

`X-TOTP-PROOF-REJECTED` closes one blind spot and grants no new authority. Without it, a request whose proof
the gateway rejected reaches a service byte-identical to a request that carried no proof at all, so a
signing-key rotation, an issuer rename, or an audience change makes every step-up route re-challenge forever
with the cause visible only in the gateway's `totp_proof_status` log field. Every gateway fact in this
section is verified in the `gateway` repository at the path given beside it.

Rules:

- **Only the gateway sets it**, on the same footing as the three verified headers: the gateway strips any
  inbound spelling from client input before any decision, so a client cannot forge it. The three verified
  names are configured at `charts/gateway/values.yaml:228-230` and stripped at `:268-270`, and the
  `x-totp-` prefix sweep at `haproxy/lua/authz-sidecar.lua:496` already covers every `X-TOTP-*` name except
  the public `X-TOTP-Proof` carrier itself. A new name is added to both places or it is forgeable.
- **It appears exactly when a proof was presented and bought nothing** — the request carried
  `X-TOTP-Proof` and the gateway set none of the three verified headers. It is absent on a fully valid
  proof and absent when no proof was presented. There is no fourth case, deliberately: making its presence
  the exact complement of injection is what removes the indistinguishability, and any carve-out would
  recreate a state — proof presented, nothing injected, nothing said — that a service still cannot tell
  apart from no proof at all.
- **It is advisory and non-blocking.** A service must not change an allow or deny decision, a route, a
  permission check, a tenant scope, or a side effect on its presence, absence, or value. It may change only
  a message. That is what keeps the gateway's TOTP handling non-blocking end to end: a wrong value here
  changes a sentence, never a decision, so a mistyped key path or a stale audience list still costs a
  re-challenge and nothing more — which is the property that made this header acceptable where a gateway
  error was not.
- **A service that does not read it behaves exactly as before.** Adding the header changes no existing
  service's behaviour on its own.

### The value vocabulary

The value is one of the eighteen codes below and nothing else. Each is the gateway's `totp_proof_status`
value for the same outcome, uppercased under a `TOTP_PROOF_` prefix, so the header value is derivable and
the two vocabularies cannot drift. Derivation is not registration: a new status is added to this table
before the gateway ships it, because a mechanical rule produces a spelling, not a registered code.

The gateway applies its status rules in order and the last match wins
(`charts/gateway/templates/configmap.yaml:835-836`), so a proof that trips more than one condition reports
only the last matching one. Read the value as *a* reason, never as the complete list of what is wrong.

| Header value | Gateway `totp_proof_status` | Meaning |
|---|---|---|
| `TOTP_PROOF_PRESENT_UNVERIFIED` | `present_unverified` | the verification rules did not reach a conclusion for a proof on an authenticated request. A gateway defect state, not a client one; a non-zero rate is an incident |
| `TOTP_PROOF_UNAUTHENTICATED_ROUTE` | `unauthenticated_route` | the proof arrived on a request the gateway did not authenticate — a public path carrying no bearer, or a protected path whose bearer failed verification. A statement about the request, not the route |
| `TOTP_PROOF_DISALLOWED_ALG` | `disallowed_alg` | the proof's `alg` is not on the allow-list, checked before the signature so a presenter cannot choose the algorithm |
| `TOTP_PROOF_INVALID_SIGNATURE` | `invalid_signature` | signature verification failed. The value a signing-key rotation produces fleet-wide and at once |
| `TOTP_PROOF_BAD_TYPE` | `bad_type` | `typ` is not the expected proof type |
| `TOTP_PROOF_BAD_AUDIENCE` | `bad_audience` | `aud` is not the expected audience — the control that separates a proof from an access token signed by the same key |
| `TOTP_PROOF_BAD_ISSUER` | `bad_issuer` | `iss` is not the expected issuer |
| `TOTP_PROOF_MISSING_CLAIM_SUB` | `missing_claim_sub` | required claim `sub` absent |
| `TOTP_PROOF_MISSING_CLAIM_PID` | `missing_claim_pid` | required claim `pid` absent |
| `TOTP_PROOF_MISSING_CLAIM_PURPOSE` | `missing_claim_purpose` | required claim `purpose` absent |
| `TOTP_PROOF_MISSING_CLAIM_JTI` | `missing_claim_jti` | required claim `jti` absent |
| `TOTP_PROOF_MISSING_CLAIM_IAT` | `missing_claim_iat` | required claim `iat` absent |
| `TOTP_PROOF_MISSING_CLAIM_NBF` | `missing_claim_nbf` | required claim `nbf` absent |
| `TOTP_PROOF_MISSING_CLAIM_EXP` | `missing_claim_exp` | required claim `exp` absent |
| `TOTP_PROOF_EXPIRED` | `expired` | `exp` is at or before now. The ordinary case — a user who paused mid-flow — and the one whose message quality this header exists to fix |
| `TOTP_PROOF_NOT_YET_VALID` | `not_yet_valid` | `nbf` is further ahead than the configured clock skew |
| `TOTP_PROOF_ISSUED_IN_FUTURE` | `issued_in_future` | `iat` is further ahead than the configured clock skew. `exp` and `nbf` do not cover this: they bound when the proof stops and starts being usable, while only `iat` states when the second factor was actually presented, which is the fact a step-up window measures. Reported after `not_yet_valid` because the two normally co-occur and this is the more diagnostic of the pair — an issuer clock running ahead, rather than a client presenting a proof early |
| `TOTP_PROOF_CONTEXT_MISMATCH` | `context_mismatch` | the proof's `sub` or `pid` does not equal the access token's |

There is one status value per required claim rather than one folded `missing_claim`, because an issuer that
stopped emitting `pid` and one that stopped emitting `jti` have different fixes
(`charts/gateway/templates/configmap.yaml:859-865`).

Two `totp_proof_status` values never appear in this header, and their absence is the contract: `absent`,
because no proof was presented, and `validated`, because the three verified headers were injected instead.

`context_mismatch` deliberately does not say which binding failed. The gateway records that in a separate
log field, because a `sub` mismatch is an attack shape and a `pid` mismatch is usually a client that
switched project without clearing its proof cache as this file's cache rules require — a distinction for an
operator, not for a value a service may only print.

### Why the value is UPPER_SNAKE while the log field stays lowercase

Two surfaces, two rules, and they do not conflict.

`totp_proof_status` is a structured log field whose value is a status word. The gateway emits no TOTP error,
so nothing in that field reaches a client, and it stays lowercase — the gateway states exactly this at
`charts/gateway/templates/configmap.yaml:831-833`. Nothing here changes it.

`X-TOTP-PROOF-REJECTED` carries a machine-readable code across a service boundary, and a service that
surfaces it copies the value verbatim into an error envelope. That puts the value under the code rule in
`10-core-service-contract.md`, section **Error code registry and casing**: every code this skill governs
matches `^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$`. A lowercase value would arrive in a public `error.meta` as the one
lowercase code in the fleet, and every client and SOC expression would have to match two casings for one
vocabulary forever.

The `TOTP_PROOF_` prefix is not decoration. `EXPIRED` alone says nothing about what expired once it sits in
an envelope beside other codes; the prefix is what makes each value self-describing at its destination.

### `TOTP_PROOF_*` is gateway-owned, and ownership is by enumeration rather than by prefix

Decided: the eighteen codes above belong to the `gateway` repository's committed code registry, not to
`auth`'s.

- `10-core-service-contract.md` binds every code to one committed registry in the repository that can emit
  it, with a test that fails when emitted code and registry diverge. Only the gateway can emit these —
  `auth` never sees the retry that carries the proof — so listing them in `auth`'s registry would add rows
  that `auth`'s own test can never exercise, which is the split-registry failure that rule exists to
  prevent.
- The prefix is not the ownership boundary, because `auth` already carries `TOTP_PROOF_TOKEN_UNAVAILABLE`
  in its own `app/Enums/ApiErrorCode.php`. Ownership is by the enumeration above: those eighteen values are the
  gateway's and are the complete `X-TOTP-PROOF-REJECTED` vocabulary; every other `TOTP_*` code, including
  that one, is `auth`'s. Do not "fix" the overlap by renaming either side — a rename of a public code costs
  a 90-day window under `22-failure-load-and-deprecation-contract.md` and buys nothing a reader needs.
- What a client branches on is decided by position, not by prefix, and position is unambiguous even where
  the prefixes overlap. `auth`'s TOTP codes appear as a top-level `error.code`. A gateway
  `TOTP_PROOF_*` value never does: it never sets an HTTP status, never appears in `error.code`, and appears
  only as advisory detail inside `meta`.

### Surfacing it to a client is a fleet-coordinated change, not a per-service one

Reading the header is optional. Putting its value in a client-visible envelope is not, once any service
does it. `10-core-service-contract.md` binds one `meta` key set to one `code` in **every** service that
emits it, and `TOTP_STEP_UP_REQUIRED` is emitted by many. So:

- The key is `meta.proof_rejected`: a string carrying one registered value from the table above, or `null`.
- A service that emits `TOTP_STEP_UP_REQUIRED` carries that key on every such response, `null` when the
  gateway set no header. A key present on some of them and absent on others is the two-shapes-for-one-code
  defect that rule exists to prevent.
- Adoption is therefore one coordinated change across every service that emits `TOTP_STEP_UP_REQUIRED`,
  never one service at a time. Until it is made, a service that reads the header uses it for service-local
  logging only and adds no key to the envelope.

The counter that makes a rejection spike visible without log search is
`alaa_gateway_totp_proof_verifications_total`, registered in `24-metric-registry.md`.

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
requirements, the client proof-cache rules, the gateway and downstream header responsibilities above, and
the advisory-and-non-blocking rule on `X-TOTP-PROOF-REJECTED`. When a change touches any of those shapes,
load `$alaa-security-review` and run its checklist against them.
