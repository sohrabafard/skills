# Auth TOTP And Step-Up Contract

Use this file when the task touches auth TOTP management, optional MFA setup, forced route-level TOTP enforcement on an Auth route or a downstream route, SDK/client handling of TOTP errors, QR setup UX, or `require_totp:<purpose>` rollout.

## Source priority

For the current auth implementation, trust these sources in order. Every path is relative to the root of
the `auth` repository checkout; resolve them there and never hardcode an absolute machine path.

1. `routes/api.php`
2. `bootstrap/app.php`
3. `app/Http/Controllers/Api/Auth/TotpController.php`
4. `docs/contracts/auth/endpoints/totp.md`
5. `docs/contracts/auth/flows/totp-enrollment.md`
6. `docs/contracts/auth/flows/totp-step-up.md`
7. `docs/ops/totp-step-up-mechanism.md`

If implementation and docs disagree, trust route/controller/middleware source first, report contract drift, and align docs plus API artifacts before closing the task.

## Related: OTP purposes are not step-up purposes

The SMS-OTP `purpose` on `/otp/request` and `/otp/verify` (allowlist `login`, `registration`) is a
separate namespace from the TOTP step-up purposes below. Its contract lives in
`/alaa-trust-gateway-auth` `references/60-auth-service-v3-contract.md` section "The generic OTP
component".

## Feature flag and availability

- TOTP management is feature-flagged by `AUTH_TOTP_ENABLED` through `auth.totp.enabled`.
- Only Auth knows the flag and a user's enrollment state, because no trusted header carries either.

| Response | Emitted by | When |
|---|---|---|
| `404 TOTP_FEATURE_DISABLED`, message `TOTP feature is disabled.` | every Auth `/api/v3/totp*` route, step-up included | the flag is off |
| `403 TOTP_UNAVAILABLE` | Auth's `gateway_step_up` guard, and its `require_totp` guard in `required` mode | the flag is off |
| `403 TOTP_REQUIRED` with `meta.purpose` | both Auth guards | the flag is on and the caller has no enabled factor |
| `403 TOTP_STEP_UP_REQUIRED` with `meta.purpose` | both Auth guards and every downstream guard | the caller has no usable proof for the purpose the route requires |

- `meta.purpose` is the exact purpose the route requires, never the presented one. `TOTP_STEP_UP_REQUIRED` carries the same `meta` key set from every emitter, under the one-key-set rule in `10-core-service-contract.md`.
- Verified 2026-11-16 at auth `caa45fed`: `<repo>/app/Http/Controllers/Api/Auth/TotpController.php:169-178`, `<repo>/app/Support/Http/ApiErrorResponseRenderer.php:58-64,164`, `<repo>/app/Http/Middleware/RequireTotpMiddleware.php:54-71`, `<repo>/app/Http/Middleware/RequireGatewayStepUpProof.php:73-90` and `<repo>/tests/Feature/TotpManagementTest.php:57`.
- Clients normalize the 404 as `totp_unavailable` and hide or disable the TOTP setup UI. Never treat it as an ordinary missing route, because a missing route means a deploy defect and this means a flag is off.
- When enabled, self-service setup routes are usable by any authenticated user, and enrollment is never forced by the flag alone. Only a route that requires step-up forces it.
- Turning the flag off stops proof issuance, because step-up answers the 404. **Proof binding to the issuing credential** below owns what a flag change, a disable or a reset revokes.
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

Enroll and confirm need a fresh SMS-OTP login. `/alaa-trust-gateway-auth` `references/30-fail-closed-cases.md` case 10 owns that rule and `TOTP_FRESH_LOGIN_REQUIRED`.

Never log or persist TOTP `secret`, `otpauth_uri`, user-entered TOTP codes, or recovery codes outside the intended secure storage and one-time display path.

## Forced route-level TOTP

The service that owns a route enforces step-up on it. The gateway never enforces TOTP: it verifies `X-TOTP-Proof`, injects the `X-TOTP-*` headers and returns no TOTP response. A route uses exactly one of two enforcement paths. To lift a step-up requirement on either path, remove it from the route deliberately and record the removal, so an operator who reads the route list sees the real protection state.

| Path | Routes | The guard decides from | Knows the flag and enrollment |
|---|---|---|---|
| Auth-local | Auth's own routes | `require_totp`: Auth's local proof record. `gateway_step_up`: the three verified headers and the credential binding | yes |
| Downstream proof | every other service's routes | the three verified headers only | no |

**Downstream service responsibilities** below owns the downstream path. The rest of this section, up to **Purpose rules**, owns the Auth-local path.

On an Auth route, keep the route behind the normal authenticated gateway/trusted flow and add `require_totp:<purpose>,<mode>`.

Example Laravel route shape:

```php
Route::middleware('auth:trusted_gateway')->group(function (): void {
    Route::delete('sessions', [SessionController::class, 'destroyAll'])
        ->middleware('require_totp:auth.sessions.revoke_all,optional');
});
```

Mode rules (`<mode>` is `optional` or `required`):

- Modes exist only on Auth's `require_totp` guard. A downstream guard has no mode.
- `required` is for admin and high-risk operations. With `AUTH_TOTP_ENABLED=false` the request fails closed with `403 TOTP_UNAVAILABLE`. With TOTP enabled it answers as the table in **Feature flag and availability** states.
- `optional` is for self-protective actions on the caller's own account, such as revoking all own sessions. It passes when `AUTH_TOTP_ENABLED=false`, because blocking a user from protecting their own account is worse than the step-up gap. With TOTP enabled it behaves like `required`.
- Choose the mode per route by risk. A disabled flag never permits a `required` operation.
- A missing or unknown mode is a configuration error and fails loudly. There is no default mode.
- Auth's `gateway_step_up` middleware (admin SMS campaigns, admin TOTP reset) is always `required`.

Purpose rules:

- Use stable, action-specific purpose names, such as `auth.sessions.revoke_all`, `profile.write`, `profile.photo`, or `catalog.school.write`.
- The purpose scopes the short-lived proof, not the authenticator enrollment. One authenticator-app entry serves all purposes.
- A successful step-up for one purpose must not unlock a different purpose.
- Do not use generic names such as `default`, `admin`, `write`, or route paths that may change.
- Do not silently attach forced TOTP. Update route docs, OpenAPI, Postman, SDK/client notes, tests, and rollout notes.

## Adding step-up to a route

A new step-up route changes only its own service, with the two exceptions below.

- **No new enrollment.** The user's one site-level credential serves every purpose, as the next section states.
- **No Auth registration.** Auth holds no purpose allow-list. It signs any purpose of at most 120 characters that matches `^[A-Za-z0-9._:-]+$` (auth `<repo>/app/Http/Requests/Auth/TotpStepUpRequest.php:17`).
- **No gateway TOTP registration.** The gateway holds no route-to-purpose map and verifies every presented proof (gateway `<repo>/docs/totp-proof-gateway-contract.md:3`, `<repo>/charts/gateway/values.yaml:200-206`).
- **Exception: a documented allow-list.** When current Auth or gateway source documents an allow-list of purposes or step-up routes, report the registration as a required change in that repository. None existed at auth `caa45fed` and gateway `1042fd4` on 2026-11-16.
- **Exception: route exposure.** Exposing a new path through the gateway, or making a path public, is a separate change. Before it, read `/alaa-trust-gateway-auth` `references/10-verification-and-ingress.md`. It owns the public-route list and what a public path does with a bearer. `references/30-fail-closed-cases.md` ("TOTP step-up") owns when the gateway processes a proof on a public path. `references/90-source-map.md` ("What this skill does not own") names the owners of deployment exposure.

Report three kinds of evidence separately, each by name:

| Kind | Covers | Proved by |
|---|---|---|
| Local enforcement | the service's guard: the required purpose, the three headers and the deny shape | service tests that inject the trusted headers |
| Deployment prerequisites | `AUTH_TOTP_ENABLED=true`; proof-token issuance on (`AUTH_TOTP_PROOF_TOKEN_ENABLED`), because step-up without it returns no `proof_token`; gateway `totpProof.enabled`; one audience, issuer and verification key shared by Auth and the gateway; the route reachable only through the gateway | the deployed Auth and gateway profiles |
| Ingress acceptance | the challenge, the step-up call and the retry with `X-TOTP-Proof` through the deployed gateway | an observed run against the real ingress |

A header-injection test proves local enforcement only. The gateway's `<repo>/ci/scripts/smoke-totp-proof.sh` runs a rendered configuration against an echo backend, so it proves neither the deployed profile nor ingress acceptance. When live gateway evidence is unavailable, report ingress acceptance as not run. Never report it as passed from the other two kinds. When a deployed profile is unreadable, report deployment prerequisites as not verified, because a chart or config default is not the deployed profile.

Take the downstream guard contract from **Downstream service responsibilities** below and the two files it names, not from an existing service. `95-fleet-conformance.md` row 22 records what each current service does and which code questions its owner has not decided.

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
2. The route's service answers `403 TOTP_STEP_UP_REQUIRED` with the required purpose in `meta.purpose`. The gateway returns no TOTP challenge.
3. The client calls `POST /auth/api/v3/totp/step-up` with that `purpose` and a fresh TOTP code or recovery code.
4. Auth verifies the code against the user's enabled site-level TOTP credential and returns:

```json
{
  "purpose": "auth.messaging.campaign.create",
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
- Keep cached proofs across an ordinary same-session token refresh. A refresh is neither a logout nor a login: the
  gateway binds a proof to the access token's `sub` and `pid`, not to one access token (gateway
  `<repo>/docs/totp-proof-gateway-contract.md:20`, read 2026-11-16 at `1042fd4`).

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

- Define which operations require step-up, and one stable purpose for each under **Purpose rules**. Only the
  route's service holds that policy.
- Take the step-up decision from all three verified headers. `/alaa-trust-gateway-auth`
  `references/20-claims-headers-and-sentinels.md` ("TOTP step-up headers") owns the exact purpose comparison, the
  integer expiry check and what each header proves.
- Deny as `/alaa-trust-gateway-auth` `references/30-fail-closed-cases.md` ("TOTP step-up") states. It owns which
  conditions deny, and which of them carry `403 TOTP_STEP_UP_REQUIRED` with `meta.purpose`.
- Never infer the Auth feature flag or the user's enrollment state, and never emit `TOTP_FEATURE_DISABLED`,
  `TOTP_UNAVAILABLE` or `TOTP_REQUIRED`, because none of the four headers carries that state. The client learns
  it from Auth, as **Client challenge handling** states.
- Never validate raw TOTP codes.
- Never trust public `X-TOTP-*` metadata.
- Enforce only route/business purpose policy against gateway-verified proof metadata after normal authentication,
  authorization, tenant, and business checks remain in place.
- Read `X-TOTP-PROOF-REJECTED` only to choose a message. A service that never reads it behaves exactly as it
  did before the header existed.

## Proof binding to the issuing credential

Auth binds a step-up proof to the credential that issued it, so on Auth's own routes a disable or reset invalidates
every earlier proof.

- A downstream service honours a gateway-verified proof until its `exp`, because the gateway verifies a proof by
  signature and a service makes no direct call to Auth (owner rule). A disable, a reset, or `AUTH_TOTP_ENABLED`
  turned off stops new issuance and revokes no proof downstream. The proof lifetime is in `/alaa-trust-gateway-auth`
  `references/20-claims-headers-and-sentinels.md`. State no shorter downstream revocation time without evidence
  from the deployed gateway.
- With `AUTH_TOTP_ENABLED` off, Auth's `gateway_step_up` guard and its `required` `require_totp` guard deny at
  once with `TOTP_UNAVAILABLE`, also for a proof that was valid when issued (`<repo>/tests/Feature/AdminWriteStepUpTest.php:227-241`, `<repo>/app/Http/Middleware/RequireTotpMiddleware.php:54-57`).
- `auth` stores the issuing credential's id under the proof's `jti` and under the local proof key. A request passes
  only when the stored id equals the user's currently enabled credential (`app/Support/Auth/TotpProofBindingVerifier.php:29-40`,
  `app/Services/Security/TotpStepUpService.php:89-98`). A disable or reset retires the credential and forgets the user's
  proofs, so an earlier proof stops working at once, not at its expiry (`app/Support/Auth/TotpStepUpProofStore.php:80-103`).
- The check runs inside `auth` with no call to another service. It covers both enforcement paths: `require_totp`
  against the local proof record, and `gateway_step_up` against the gateway-injected `X-TOTP-PROOF-ID`
  (`app/Http/Middleware/RequireGatewayStepUpProof.php:75-84`). Only `auth`'s own routes enforce it
  (`/alaa-trust-gateway-auth` `references/90-source-map.md`).
- An unreadable proof store fails closed: the read raises `DependencyUnavailableException`
  (`TotpStepUpProofStore.php:111-118`), answered `503 DEPENDENCY_UNAVAILABLE` (`bootstrap/app.php:108-126`), never as a
  valid proof. A failed forget after a disable or reset is only logged, because the binding check already refuses a
  retired credential.
- The Redis keys are registered in `29-redis-key-registry.md`.

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
| `TOTP_PROOF_UNAUTHENTICATED_ROUTE` | `unauthenticated_route` | the proof arrived on a request that carried no accepted bearer — none, or one that failed a check — on a public path or a protected one. For what counts as an accepted bearer, read `alaa-trust-gateway-auth references/10-verification-and-ingress.md` ("A public path takes an optional bearer", owner ruling 2026-11-14); for when the gateway processes a proof beside one, read `alaa-trust-gateway-auth references/30-fail-closed-cases.md` ("TOTP step-up"). A statement about the request, not the route |
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

- On `TOTP_STEP_UP_REQUIRED`, after the status read below when the route is outside Auth, preserve the original request intent, show a TOTP challenge, call `POST /auth/api/v3/totp/step-up` with `meta.purpose` from that response plus `code` or `recovery_code`, cache the returned `proof_token` until `verified_until`, then retry the original request with public `X-TOTP-Proof`.
- Send the server's `meta.purpose` unchanged. Never derive the purpose from the route or from a client-side table, because only the route's service knows which purpose it requires.
- On `TOTP_STEP_UP_REQUIRED` from a route outside Auth, read `GET /auth/api/v3/totp` before you show the code prompt. When `enabled=false`, run the enrollment path first. Such a route answers `TOTP_STEP_UP_REQUIRED` to an unenrolled user too, and Auth answers that user's step-up with `422 TOTP_STEP_UP_FAILED` and counts a failed attempt (auth `<repo>/app/Services/Security/TotpStepUpService.php:51-53`, `<repo>/app/Http/Controllers/Api/Auth/TotpController.php:132-134,197-204`, read 2026-11-16 at `caa45fed`).
- On `TOTP_REQUIRED`, guide the user through status, enroll, confirm, and then step-up or retry the original action if it still requires proof.
- On `TOTP_FRESH_LOGIN_REQUIRED`, send the user through a new SMS-OTP login, then resume enrollment. An ordinary token refresh does not satisfy it (auth `<repo>/docs/ops/totp-step-up-mechanism.md:19`).
- On `TOTP_UNAVAILABLE`, or on `404 TOTP_FEATURE_DISABLED` from the status read or the step-up call made while recovering from a step-up challenge, show a controlled unavailable state and report rollout/config drift to operators. The original operation stays denied.
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

The TOTP and step-up review checklist is owned by `/alaa-security-review`, so that a reviewer who loads
that skill sees it. This file owns the shapes it triggers against: the public versus internal route shape,
the `otpauth_uri`-not-an-image setup contract, the two enforcement paths, the purpose naming rules, the
proof-token binding requirements, the client proof-cache rules, the gateway and downstream header
responsibilities above, and the advisory-and-non-blocking rule on `X-TOTP-PROOF-REJECTED`. When a change
touches any of those shapes, load `/alaa-security-review` and run its checklist against them.
