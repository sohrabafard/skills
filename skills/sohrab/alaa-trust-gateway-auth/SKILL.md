---
name: alaa-trust-gateway-auth
description: "Trust-boundary authority for the Ala gateway: who may assert a trusted request header, and what a service behind it may believe. Use when gateway header sanitizing or injection, JWT verification order, compact claim projection (pid, sub, prm, rol, loc) into X-Project-Id, X-User-Id, X-Access, X-User-Roles and X-Location-*, X-Access bitmap consumption, TOTP step-up headers, a public path's optional bearer, the dropped-bearer marker (WWW-Authenticate), tenant scoping behind the gateway including a guest project_id, WA ingest tenant or user attribution, auth-service v3 route shape, or a fail-closed case at that boundary is in scope: bypassed edge, absent claim, invalid bitmap. Do not use it for a service not behind the Ala gateway; route header names and response envelopes to alaa-services-contract, the permission bit contract and decoders to alaa-permission-generator, fail-closed doctrine to alaa-security-review, and cursor mechanics to alaa-keyset-pagination."
---

# Alaa Trust Gateway Auth

This skill owns one question: **who may assert a trusted request header, and what
may be believed about a request because it carries one.** The gateway authenticates
and injects. The request-time checker decides the route. A backend normalizes
trusted context once, then enforces its own business rules. This skill states the
boundary between those, and every way it fails.

Read in this order: this file; the reference the router names; the owning skill named
below, when your change lands on its ground; the repository. Only then propose a change.

## Absolutes

**Only the gateway treats `Authorization: Bearer` as raw bearer input.** No backend
parses, verifies or introspects a bearer token on a gateway-fronted route. Reason:
two verifiers means two verification policies, and the weaker one decides.

**The gateway deletes every spoofable inbound trusted header on every route,
including public routes.** A public route makes the bearer optional; it never skips
sanitizing. Observable: the delete list runs unconditionally, and every header the gateway
injects appears in it.

**Tenant and actor context are derived from the verified token** — never from a
request body, query string, route parameter or client-supplied header. When a
client-supplied selector disagrees with the trusted context, deny rather than
choose: a silent choice is a cross-tenant read nobody decided to ship. A request
with no accepted bearer (none, or one the gateway dropped on a public path: not
trusted; the gateway currently forwards its `Authorization` header to the backend,
`references/10-verification-and-ingress.md`) has no claim to
derive from, so a guest carries `project_id` in the body, or in the query
string when the request has no body. That value attributes a write.
That value scopes a read only on an explicitly listed route. That value authorizes nothing. Once a
verified claim is present, nothing reads that value.

**A public client never generates, sends or relies on a trusted internal header.**
Every such header is on the gateway's delete list precisely so a client's copy
cannot survive. A client that sends one is confused or hostile, and neither earns an
exception.

**An authorization decision behind the gateway is taken from the decoded `X-Access`
permission bitmap, and from no other source** — not a role string, not a per-request
database lookup, not a claim read directly from a token. **The decoder is the one
emitted and governed by `/alaa-permission-generator`,
never a locally written one.** Reason: a local decoder is only ever discovered to be
wrong by the incident it causes. Take the decoder, the conformance vectors and the
harness from `alaa-permission-generator` `references/shared-consumer-contract.md`
and the per-language consumer references beside it. This skill states the
obligation, not the bit contract.

**A client-supplied opaque value carries no trust.** After decoding it, compare
every scope-bearing field it yields against the trusted request context, and deny on
mismatch. The decoded value never becomes a source of tenant, actor or scope. The
mechanism stays with `/alaa-keyset-pagination` and
`/alaa-services-contract`.

## Fail-closed cases

Each case carries its symptom, decision, response, log and test in
`references/30-fail-closed-cases.md`.

| You are looking at | Case |
|---|---|
| a service reachable without crossing the gateway, or an edge that is down | 1 — deny `AUTH_CONTEXT_MISSING` with the status policy in `references/50-deny-codes.md`; strip at the service edge *and* block the exposure |
| a request-time checker that timed out, failed, or answered unparseably | 2 — the gateway denies under the decision and enforcement contract named in that case; a service-side fallback is a bypass |
| a required claim or trusted header absent, including `rol` | 3 and 4 — deny; an absent role never means "no restrictions apply"; an absent `X-Project-Id` on a route with a guest rule is the guest shape (case 3 Scope), not a deny; a missing or failing bearer on a public path is dropped, not denied (case 3 Scope) |
| a malformed `X-Access`, or a permission revoked after issuance | 5 and 6 — deny at ingress with `AUTH_ACCESS_BITMAP_INVALID`; revocation latency equals the remaining token lifetime and is not fixed inside a service; an absent or blank `X-Access` denies with `AUTH_ACCESS_HEADER_MISSING` |
| a step-up proof absent, expired, or issued for another purpose | TOTP — deny `403 TOTP_STEP_UP_REQUIRED` with `meta.purpose`; absent and invalid are indistinguishable by design |

## Router

| You are about to | Read |
|---|---|
| change gateway verification order, the public-route list, prefix stripping or sanitizing; decide what a public path does with a present, absent or failing bearer, or when the gateway sets the dropped-bearer marker; decide where a request's `X-Project-Id` came from; or touch WA ingest tenant or user attribution | `references/10-verification-and-ingress.md` |
| decide which claim a value travels in, which header it arrives as, what absence looks like, or which step-up headers a service may read | `references/20-claims-headers-and-sentinels.md` |
| decide what happens when the gateway, a claim, a header, a checker or a proof is missing or wrong | `references/30-fail-closed-cases.md` |
| write or review a service's ingress layer — middleware, guards, context builders, tenant scoping, bitmap consumption | `references/40-downstream-normalization.md` |
| choose the code a deny carries, or reconcile two services denying one thing differently | `references/50-deny-codes.md` |
| work on an auth-service v3 route, the OTP or refresh flow, step-up issuance, or direct local testing | `references/60-auth-service-v3-contract.md` |
| review a trust-boundary change and need the observable that decides a defect | `references/70-review-and-anti-patterns.md` |
| assert a gateway or auth behaviour someone will act on, or find a fact older than your change | `references/90-source-map.md` |
| find that your change lands on header names, envelopes, error taxonomy, platform values, the TOTP claim set or step-up response, purpose naming or proof caching, the bit contract or permission id allocation, fail-closed doctrine, reliability doctrine, OpenFGA modelling, cursors, HAProxy, Laravel, PHP or Octane code, telemetry, exposure or trusted-proxy delivery | *What this skill does not own* in `references/90-source-map.md`; it names the owner of each ground |

## Check it mechanically

```
python3 scripts/trust_boundary_check.py --gateway-config <configmap> --gateway-config <values>
python3 scripts/trust_boundary_check.py --source-root <dir> --allowlist <frozen-header-list>
python3 scripts/trust_boundary_check.py --env-root <dir>
python3 scripts/trust_boundary_check.py --bitmap <value> --max-permission-id <n>
```

Exit codes:

- `0`: every requested check passed.
- `1`: a defect was found. Fix it before the change ships. Fix it in the gateway or environment configuration first.
- `2`: the invocation was wrong.
- `3`: a check could not run for want of input. Supply it; never report a pass for a check that did not run.

`--help` and the script docstring carry the full
contract. The canonical bitmap vectors and the cross-runtime harness belong to
`/alaa-permission-generator`.

## When not to use

Do not use this skill for authentication in a service that does not sit behind the
Ala gateway. It assumes a verifying edge that such a service lacks, and its rules
will read as permission to trust headers nobody sanitized. Do not use it alone when
the change also lands on an owner's ground in *What this skill does not own* in `references/90-source-map.md`. Read the matching skill, and follow
the stricter rule where they overlap.
