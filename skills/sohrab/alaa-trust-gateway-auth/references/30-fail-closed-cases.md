# Fail-closed cases at the trust boundary

Read this file when any part of the trust boundary stops answering, answers
partially, or answers with something a service cannot verify.

Apply /alaa-security-review's fail-closed discriminator to these trust-boundary cases;
/alaa-reliability-sla owns contributor degradation, timeout shape, retry legality and backoff.
This file owns the boundary-specific denial cases, not either general doctrine.

Each case below gives the observable symptom, the decision, the outward response,
the log, and the test that proves it. A case with no test is not closed.

---

## 1. The gateway is unreachable, or the request did not cross it

**Symptom.** A request arrives carrying `X-User-Id`, `X-Project-Id`, `X-Access`
or any other trusted header, and the service cannot establish that the request
entered through the trusted edge — the peer address is outside the trusted proxy
set, the service listens on a route the edge does not front, or the edge is down
and traffic reached the service by another path.

**Decision.** Deny. A trusted header carries no signature. Its entire
trustworthiness is the claim that it was written by the gateway after
verification, and that claim rests only on the network path. A service that
accepts the header without the path has no authentication at all, and the caller
chooses its own user id and project id.

**Response.** `AUTH_CONTEXT_MISSING` with the service status policy in
`references/50-deny-codes.md`. Do not echo the received header values.

**Obligation on a directly reachable service.** A service that can be reached
without crossing the gateway strips and rejects every trusted header at its own
edge, and it does this whether or not it also blocks the exposure at the network
layer. The two are not alternatives: the network block is the control that can be
misconfigured silently, and the edge strip is the control that fails loudly.
Configure both.

**Log.** `code`, `route`, `auth_source: service`, `request_id`, and the peer
address. Never the header values, because a forged `X-User-Id` in a log is
indistinguishable from a real one to whoever reads it later.

**Test.** Send every trusted header directly to the service's own listener from
outside the trusted proxy set and assert the documented denial status. A test that only exercises the
gateway path proves nothing about this case.

---

## 2. The request-time checker fails, times out, or returns an unparseable answer

**Symptom.** `authz-sidecar` or `entitlement-spoa` does not answer inside its
budget, returns a malformed body, or returns a decision the gateway cannot map.

**Decision.** Deny at the gateway. The checker owns the route decision; an absent
decision is not an allow. The protected backend is not called.

**Response.** Use `alaa-services-contract references/26-request-time-authorization-openfga/40-decision-and-enforcement.md`
for the status/code mapping: explicit denial and dependency unavailability are distinct classes.
That static contract is not evidence of a deployed gateway response. An unparseable or unmappable
answer still denies; if the owner has no matching public-code row, report the gap and stop that
contract decision rather than infer `403` or `503`. Never expose dependency topology or verifier internals.

**What a downstream service does.** Nothing different. A service behind the
gateway never observes this case, because the request does not arrive. A service
that has built a fallback for "the checker did not answer" has built a bypass.

**Timeout, retry budget and circuit shape for the checker call belong to**
`/alaa-reliability-sla`; the values belong to
`alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`.

**Test.** Point the checker at a black hole and assert the route denies rather
than allows, and that the denial arrives inside the configured budget.

---

## 3. A required claim or a required trusted header is absent

**Symptom.** The gateway finds a protected route whose token is missing `pid` or
`sub`; or a service finds `X-Project-Id` absent on a tenant-scoped HTTP route.

**Decision.** Deny.

**Response.** The gateway returns `401` and the canonical translation is
`AUTH_MISSING_REQUIRED_CLAIM` with `meta.claim` naming the safe claim name. A
service missing `X-Project-Id` on an HTTP route returns `400` with
`TENANT_CONTEXT_MISSING`. Falling back to a default project id is confined to
console and queue execution, where there is no caller to authenticate, and is
never reached from an HTTP request.

**Scope.** This case is a route whose project id must arrive as a trusted header. A
route that admits tokenless requests takes a guest request's project id from the
request body, or from a `project_id` query parameter when the request has no body,
so an absent header there is the normal shape and not a deny;
`references/10-verification-and-ingress.md` states that rule and what it rejects.

**Test.** For each required claim, issue a token without it and assert the
gateway denies before any backend is contacted.

---

### 3a. A route requires an actor but the user UUID is absent or invalid

**Symptom.** A route whose contract requires an authenticated actor receives no
`X-User-Id`, or receives a value that is malformed or not UUIDv7. The gateway must
reject a token with a missing or invalid `sub`; the service also validates trusted
header shape at ingress rather than trusting malformed context.

**Decision.** Deny under the existing owning error policy. Do not parse a numeric
fallback, accept both UUID and numeric forms, resolve the identity remotely, or
derive an actor from request data. Preserve the route's established response code.

**Scope.** This is only for routes requiring an actor. Guest, tokenless, and public
routes retain their existing optional-actor semantics. UUID possession never grants
authorization; normal permission, tenant, and business checks still apply.

**Test.** On an actor-required route, test absent, malformed, and wrong-version
identity and assert denial before the protected operation. On a public or guest
route, verify actor absence retains its documented behavior.

## 4. `rol` is absent from a token, so `X-User-Roles` is not injected

**Symptom.** A verified access token carries no `rol` claim, so the gateway
injects no `X-User-Roles`, and a service that reads roles sees nothing.

**Decision.** The gateway forwards the request; a missing optional claim is not a
verification failure. The service denies any operation whose authorization
depends on a role it cannot see. A service never treats an absent
`X-User-Roles` as "no restrictions apply".

**This is not a migration allowance.** An earlier revision of this skill wrote
the absence as a tolerance the gateway extends to older tokens, with no end date
and no observable that says the migration is finished. That form is a permanent
fail-open licence written as a temporary one. The correct form has an external
referent: the absence is bounded by the access-token lifetime, so the last token
issued before `rol` shipped expires at most one access-token lifetime after that
deployment, and after that instant a request without `rol` is an anomaly rather
than a legacy case. The observable that closes this case is the gateway metric
for tokens verified without `rol` reaching zero and staying there across a full
token lifetime. Until it does, roles decide nothing.

**Authorization never rests on `X-User-Roles` in the first place.** See the
absolute in `SKILL.md`: an authorization decision behind the gateway is taken
from the decoded `X-Access` permission bitmap. `X-User-Roles` is an
issuance-time snapshot carried for display, audit and coarse routing.

**Test.** Issue a token with no `rol`, assert the request is forwarded, and
assert every role-gated operation denies.

---

## 5. The permission bitmap is stale

**Symptom.** A permission was revoked, or the catalog was regenerated, after the
access token was issued. The token still carries the old `prm`, so `X-Access`
still grants the revoked permission until the token expires.

**Decision.** This case is currently undetectable inside a service, and saying so
is more useful than pretending otherwise. `prv` (permission catalog version) and
`av` (authorization version) are the two claims that would let a service notice
that its own catalog version and the token's disagree, and they are deliberately
not forwarded as headers. The component that could act on the condition is denied
the metadata that detects it.

**What follows from that, in constraint form.** Revocation latency at this
boundary equals the remaining access-token lifetime, and every design that needs
faster revocation than that obtains it by shortening the access token or by
revoking the session, never by adding a per-request permission lookup in a
service. A per-request lookup reintroduces the callback pattern the compact-claim
contract exists to remove, and it makes every service a dependency of auth on the
hot path. Revoking the session ends refresh, not the live access token, which the
gateway accepts until `exp` (case 9).

**When faster revocation is genuinely required**, the change is a contract change:
forwarding `prv` to services, or shortening the token. Both are decided in
`alaa-services-contract` and `/alaa-permission-generator`, not inside a service.

**Test.** Assert that a service takes no action on `prv` or `av`, because it
cannot see them. A service containing code that reads either from a header is
reading something the gateway does not send.

---

## 6. `X-Access` is malformed, or resolves to zero known permissions

**Symptom.** `X-Access` is absent, is not unpadded base64url, or decodes to a set
of ids none of which this service knows.

**Decision.** Deny during trusted-context normalization, at ingress, before any
route handler runs.

**Response.** `401` with `AUTH_ACCESS_HEADER_MISSING` when the header is absent or
blank, and `401` with `AUTH_ACCESS_BITMAP_INVALID` when it is present but
unusable or maps to no known permission for this service.

**Why at ingress and not later.** The common legacy failure is to decode, map
what is recognised, find nothing, and let the request continue until a later
generic `unauthorized` fires. That produces a deny with the wrong code, a log line
that does not say what actually happened, and an incident that cannot be
diagnosed from the logs. The code in the response and the code in the deny log
are identical, and both name the bitmap.

**A set bit whose id this service does not know grants nothing and is not an
error.** The bitmap is issued against the whole platform catalog, so a service
always sees ids outside its own range. Only the empty result is a failure.

**Test.** Feed the normalizer an empty value, a padded value, a value with a
character outside the base64url alphabet, a value of impossible length, a value
whose set bits are all outside this service's range, and a value wider than this
service's maximum id. The first four deny with `AUTH_ACCESS_BITMAP_INVALID`, the
fifth denies with the same code, and the sixth decodes normally.
`scripts/trust_boundary_check.py --self-test` carries these as executable
vectors.

---

## 7. A client-supplied opaque value decodes to a scope that disagrees with the request

**Symptom.** A pagination cursor, a continuation token, a saved-view handle or any
other value the service handed out earlier comes back, decodes successfully, and
yields a project id, actor id, filter scope or sort scope that does not match the
trusted request context.

**Decision.** Deny. Decoding successfully is not evidence of anything: the values
in this platform are unsigned base64 JSON, so a caller can edit any field and
re-encode. See the policy stated in `SKILL.md`; this case is where it is enforced.

**Response.** `403` with `TENANT_CONTEXT_INVALID` when the mismatch is on the
tenant boundary, and `400` with the service's own invalid-cursor code otherwise.

**The mechanism — cursor shape, signing, what a cursor binds — belongs to**
`/alaa-keyset-pagination` and
`alaa-services-contract`. Only the trust rule is stated here.

**Test.** Take a cursor issued to project A, present it on a request whose trusted
`X-Project-Id` is project B, and assert the deny. Repeat with the actor id.

---

## 8. A bypass switch is enabled in a deployed environment

**Symptom.** An environment file sets a switch that disables gateway proof
verification, trusted-header verification, or step-up enforcement.

**Decision.** A truthy bypass switch in any environment file that is not
explicitly local or test, with no recorded decision beside it naming the
compensating control, the verifier and the date, is a `/alaa-security-review` trigger and blocks the change.

**Unverified, and stated as unverified.** `alaa-go-chi-development`
`references/12-kit-capability-map.md:191` names a kit key `BYPASS_GATEWAY_PROOF`
and describes it as defaulting to true. A case-insensitive search of the gateway
repository's charts, HAProxy assets and documentation on 2026-07-27 returned no
occurrence of that name, and neither did the auth repository. Whether the key
exists on the kit side was not confirmed this session. Treat it as a kit-side
claim to verify against kit source before acting on it, and do not restate it
here as a platform default in either direction. The two switches that were
confirmed are `totpProof.enabled`, true in every render inspected, and
`AUTH_TOTP_ENABLED`, false by default.

**Test.** `scripts/trust_boundary_check.py --env-root <dir>` audits every
environment file under a path and exits 1 on an undocumented truthy bypass.

---

## 9. A revoked access token reaches a sensitive auth route

**Symptom.** Logout, revoke-all and the admin TOTP reset only set `revoked` flags in
auth's database (auth `app/Repositories/Auth/DatabaseTokenSessionRepository.php`).
The gateway verifies the JWT without a revocation lookup, so the revoked access
token passes it until `ACCESS_TOKEN_TTL_MINUTES` ends (auth `config/auth.php:46`,
default 15). The value is env-controlled: the owner may lower it to 1 minute in
production or raise it under load.

**Decision.** On its live-token routes (`references/60-auth-service-v3-contract.md`),
auth denies unless its own database shows the token live. Middleware
`reject_revoked_access_token` (auth `app/Http/Middleware/RejectRevokedAccessToken.php`)
reads `X-Access-Token-Id`, which the gateway sets from the verified `jti` after
deleting any client copy (gateway `snapshots/alaa-service.haproxy.cfg:226`, `:920`),
and runs one primary-key lookup on auth's own database (auth
`app/Repositories/Auth/DatabaseAccessTokenSessionLookup.php`). It makes no
inter-service call and shortens the window only on those routes; elsewhere case 5
holds. The admin session revoke routes are live-token routes. The guard runs before
the permission check there, so a stale caller token gets `401 SESSION_EXPIRED` and not
`403 AUTHZ_DENIED`.

**Response.** `401 SESSION_EXPIRED` when the header is missing or malformed, or the
token row is unknown, revoked, expired or another user's.

**Log.** `auth.access_token.rejected` with `code`, `reason`, `route_name` and
`user_id`.

**Test.** Revoke a session, replay its access token on each live-token route and
assert `401 SESSION_EXPIRED`; repeat with the header absent and with an unknown,
expired and another user's token id (auth `tests/Feature/RevokedAccessTokenGuardTest.php`).

---

## 10. TOTP enrolment without a fresh SMS-OTP login

**Symptom.** TOTP enroll or confirm arrives on a session whose SMS-OTP login is older
than `AUTH_TOTP_ENROLL_FRESH_LOGIN_SECONDS` (default 600, clamped to 60..86400; auth
`config/auth.php:120`), or whose login time cannot be read.

**Decision.** Deny, because a stolen access token could otherwise bind the thief's
authenticator to an account that has none, and `409 TOTP_ALREADY_ENABLED` would then
lock the owner out. Middleware `totp_fresh_login` (auth
`app/Http/Middleware/RequireFreshTotpEnrollmentLogin.php`) takes the login time from
the ULID of the session's refresh-token family, found through `X-Access-Token-Id`,
and fails closed whenever it cannot read that time. With TOTP disabled it steps
aside and the route answers `404`.

**Response.** `403 TOTP_FRESH_LOGIN_REQUIRED` with `meta.max_age_seconds`, naming no
session id and no time; the enrolment quota is not spent.

**Log.** `auth.totp.fresh_login.denied` with `code`, `reason`, `route_name` and
`user_id`.

**Test.** Assert a deny for a stale login, an unreadable login time and a missing
header, and a pass inside the bound (auth `tests/Feature/TotpFreshLoginTest.php`).

---

## TOTP step-up

Step-up decides whether a caller may act, so a service denies whenever it cannot
decide that a valid proof is present. A control that guesses on missing evidence
grants the sensitive operation to exactly the caller it was added to stop.

The gateway verifies a presented proof and injects three backend-only headers
only when every check passed, and it returns no TOTP error and blocks no request.
An absent proof and an invalid proof are therefore indistinguishable to a
service, and both deny.

- **Deny with `403` `TOTP_STEP_UP_REQUIRED` and `meta.purpose` when any of the
  three step-up headers is absent on a step-up-required route**, because the
  client needs that exact purpose string to request a usable proof.
- **Deny on a purpose mismatch**, because a valid proof for any purpose reaches
  every route.
- **Deny when `X-TOTP-VERIFIED-UNTIL` parses to an instant at or before now**, and
  never re-apply clock skew, because the gateway already applied it and
  re-applying widens the real lifetime past what the operator configured.
- **Deny when a step-up header arrives on a route the gateway did not
  authenticate**, because the gateway processes a proof only alongside a verified
  bearer.
- **Deny when the gateway is unreachable or the request arrived on a bypassing
  path**, because a step-up header carries no signature a service can check and
  its trustworthiness rests entirely on having crossed the gateway.
- **Return `503` with a distinct unavailable code rather than the step-up
  challenge when the decision itself depends on a store that is down**, because a
  challenge tells the client to spend a TOTP code the service cannot evaluate.
- **Never allow a `required` step-up operation because the feature flag is off in
  this environment.** Deny with `403` `TOTP_UNAVAILABLE`. Remove the route's
  requirement deliberately and record the removal, so an operator reading the route
  list sees the real protection state.
- **The only exception is an `optional` route**: a self-protective action on the
  caller's own account (for example revoke all own sessions) passes while the flag
  is off, because blocking a user from protecting their own account is worse than
  the step-up gap. With the flag on it behaves like `required`.
- **Choose the mode per route by risk, explicitly.** Admin and high-risk operations
  are `required`. A missing or unknown mode is a configuration error, never a
  default. The gateway never enforces TOTP; the backend decides.
- **Log the denial with the proof id, the required purpose, the presented
  purpose, the route, the user id, the project id and the decision.** Never log
  the proof token, a TOTP code, a recovery code, the enrolment secret or the
  `otpauth_uri`, because those five reconstruct the credential and a proof id
  does not.

**Every service other than auth enforces step-up against the gateway-injected
headers.** Auth verifies the TOTP code itself, and enforces `require_totp` routes
against its own proof record (`require_totp:<purpose>,<optional|required>`) and
`gateway_step_up` routes, which are always `required`, against the three headers
(auth `app/Http/Middleware/RequireTotpMiddleware.php`,
`app/Http/Middleware/RequireGatewayStepUpProof.php`).

**Proof binding is local to auth.** Auth binds each proof it issues to the active
TOTP credential in its own Redis and denies a proof whose credential is no longer
the enabled one, so a disable or reset voids earlier proofs at once on auth routes;
an unreadable store fails closed (auth `app/Support/Auth/TotpStepUpProofStore.php`,
`app/Support/Auth/TotpProofBindingVerifier.php`). An agent debugging a step-up
denial at auth checks the binding record and the credential state, not only the
headers. Every other service honours a gateway-verified proof until its `exp`,
because services make no direct call to auth (owner rule). The step-up contract is
`/alaa-services-contract` `references/32-auth-totp-and-step-up-contract.md`.

**Test.** For a step-up-required route: assert a deny with each of the three
headers removed in turn; assert a deny when `X-TOTP-PURPOSE` names a different
purpose; assert a deny when `X-TOTP-VERIFIED-UNTIL` is one second in the past and
an allow when it is one second in the future; assert a deny when the headers
arrive without gateway authentication; and assert that no denial log line contains
the proof token or any code.

---

## Test obligations for the trusted-context contract as a whole

These four are the standing proof that the compact contract is implemented, not
merely documented. A change to claim projection, header injection or ingress
normalization is not finished until all four pass.

1. **Gateway tests prove that spoofed inbound trusted headers are stripped and
   replaced.** Send every trusted header from a client, with a valid token, and
   assert the backend receives the values from the token and not the values from
   the client.
2. **Gateway tests prove that compact claim values reach upstream headers.** For
   every claim in the projection table, assert the corresponding header arrives
   with the claim's value.
3. **Downstream tests prove that identity and location headers are parsed once
   into a trusted request context.** Assert that no policy, controller,
   repository or job reads a raw trusted header after normalization.
4. **Token tests prove that the emitted JWT uses only the compact custom-claim
   contract.** Assert that no claim outside the documented set is present.

Test placement, layering and what belongs in a unit versus an integration test
are owned by `/alaa-testing-strategy`.
