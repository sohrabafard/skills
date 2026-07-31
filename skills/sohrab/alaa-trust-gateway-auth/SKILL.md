---
name: alaa-trust-gateway-auth
description: "Trust-boundary authority for the Ala gateway: who may assert a trusted request header, and what a service behind it may believe. Use when gateway header sanitizing or injection, JWT verification order, compact claim projection (pid, sub, prm, rol, loc) into X-Project-Id, X-User-Id, X-Access, X-User-Roles and X-Location-*, X-Access permission-bitmap consumption, TOTP step-up headers, tenant scoping behind the gateway including a guest project_id in a body or query parameter, auth-service v3 route shape, or a fail-closed case at that boundary is in scope: bypassed edge, absent claim, invalid bitmap. Do not use it for a service not behind the Ala gateway; route header names and response envelopes to alaa-services-contract, the permission bit contract and decoders to alaa-permission-generator, fail-closed doctrine to alaa-security-review, and cursor mechanics to alaa-keyset-pagination."
---

# Alaa Trust Gateway Auth

This skill owns one question: **who may assert a trusted request header, and what
may be believed about a request because it carries one.** The gateway authenticates
and injects; the request-time checker decides the route; a backend normalizes
trusted context once, then enforces its own business rules. This skill states the
boundary between those, and every way it fails.

Read this file, then the reference the router names, then the owning skill named
below when your change lands on its ground, then the repository, and only then
propose a change.

## Absolutes

**Only the gateway treats `Authorization: Bearer` as raw bearer input.** No backend
parses, verifies or introspects a bearer token on a gateway-fronted route, because
two verifiers means two verification policies and the weaker one decides.

**The gateway deletes every spoofable inbound trusted header on every route,
including public routes.** A public route skips token verification, not sanitizing.
Observable: the delete list runs unconditionally and every header the gateway
injects appears in it.

**Tenant and actor context are derived from the verified token** — never from a
request body, query string, route parameter or client-supplied header. When a
client-supplied selector disagrees with the trusted context, deny rather than
choose: a silent choice is a cross-tenant read nobody decided to ship. A tokenless
route has no token to derive from, so a guest carries `project_id` in the body, or
in the query string when the request has no body. That value attributes a write,
scopes a read only on an explicitly listed route, authorizes nothing, and is not
read at all once a verified claim is present.

**A public client never generates, sends or relies on a trusted internal header.**
Every such header is on the gateway's delete list precisely so a client's copy
cannot survive; a client sending one is confused or hostile, and neither earns an
exception.

**An authorization decision behind the gateway is taken from the decoded `X-Access`
permission bitmap, and from no other source** — not a role string, not a per-request
database lookup, not a claim read directly from a token. **The decoder is the one
emitted and governed by `/alaa-permission-generator` (`$alaa-permission-generator`),
never a locally written one**, because a local decoder is only ever discovered to be
wrong by the incident it causes. Take the decoder, the conformance vectors and the
harness from `alaa-permission-generator` `references/shared-consumer-contract.md`
and the per-language consumer references beside it. This skill states the
obligation, not the bit contract.

**A client-supplied opaque value carries no trust.** After decoding it, compare
every scope-bearing field it yields against the trusted request context and deny on
mismatch. The decoded value never becomes a source of tenant, actor or scope. The
mechanism stays with `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) and
`/alaa-services-contract` (`$alaa-services-contract`).

## Fail-closed cases

Each case carries its symptom, decision, response, log and test in
`references/30-fail-closed-cases.md`.

| You are looking at | Case |
|---|---|
| a service reachable without crossing the gateway, or an edge that is down | 1 — deny `401 AUTH_CONTEXT_MISSING`; strip at the service edge *and* block the exposure |
| a request-time checker that timed out, failed, or answered unparseably | 2 — the gateway denies `403 AUTHZ_DENIED`; a service-side fallback is a bypass |
| a required claim or trusted header absent, including `rol` | 3 and 4 — deny; an absent role never means "no restrictions apply" |
| a malformed `X-Access`, or a permission revoked after issuance | 5 and 6 — deny at ingress with `AUTH_ACCESS_BITMAP_INVALID`; revocation latency equals the remaining token lifetime and is not fixed inside a service |
| a step-up proof absent, expired, or issued for another purpose | TOTP — deny `403 TOTP_STEP_UP_REQUIRED` with `meta.purpose`; absent and invalid are indistinguishable by design |

## Router

| You are about to | Read |
|---|---|
| change gateway verification order, the public-route list, prefix stripping or sanitizing, or decide where a request's `X-Project-Id` came from | `references/10-verification-and-ingress.md` |
| decide which claim a value travels in, which header it arrives as, what absence looks like, or which step-up headers a service may read | `references/20-claims-headers-and-sentinels.md` |
| decide what happens when the gateway, a claim, a header, a checker or a proof is missing or wrong | `references/30-fail-closed-cases.md` |
| write or review a service's ingress layer — middleware, guards, context builders, tenant scoping, bitmap consumption | `references/40-downstream-normalization.md` |
| choose the code a deny carries, or reconcile two services denying one thing differently | `references/50-deny-codes.md` |
| work on an auth-service v3 route, the OTP or refresh flow, step-up issuance, or direct local testing | `references/60-auth-service-v3-contract.md` |
| review a trust-boundary change and need the observable that decides a defect | `references/70-review-and-anti-patterns.md` |
| assert a gateway or auth behaviour someone will act on, or find a fact older than your change | `references/90-source-map.md` |

## Check it mechanically

```
python3 scripts/trust_boundary_check.py --self-test
python3 scripts/trust_boundary_check.py --gateway-config <configmap> --gateway-config <values>
python3 scripts/trust_boundary_check.py --source-root <dir> --allowlist <frozen-header-list>
python3 scripts/trust_boundary_check.py --env-root <dir>
python3 scripts/trust_boundary_check.py --bitmap <value> --max-permission-id <n>
```

Exit `0` every requested check passed; `1` a defect was found, fixed before the
change ships and in the gateway or environment configuration first; `2` the
invocation was wrong; `3` a check could not run for want of input — supply it, and
never report a pass for a check that did not run. `--help` carries the full
contract. The canonical bitmap vectors and the cross-runtime harness belong to
`/alaa-permission-generator` (`$alaa-permission-generator`).

## What this does not own

| Ground | Owner |
|---|---|
| Trusted header **names**, response envelopes, error taxonomy, platform values | `/alaa-services-contract` (`$alaa-services-contract`) |
| TOTP proof claim set, step-up response body, purpose naming, client proof caching | `/alaa-services-contract` (`$alaa-services-contract`) `references/32-auth-totp-and-step-up-contract.md` |
| The permission bit contract, id allocation, catalog drift, decoders and harness | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| Fail-closed doctrine, threat classes, security-review triggers | `/alaa-security-review` (`$alaa-security-review`) |
| Timeout shape, retry legality, backoff, circuit breakers, degrade doctrine | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Object-level relations, tuple modelling, OpenFGA model design | vendored `openfga`; `/alaa-services-contract` (`$alaa-services-contract`) `references/26-request-time-authorization-openfga.md` |
| Cursor shape, signing, and what a cursor binds | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) |
| HAProxy directives, ACL syntax, SPOE and Lua mechanics | `/alaa-haproxy` (`$alaa-haproxy`), `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) |
| Laravel middleware, guard, policy and DTO shape; PHP code shape; Octane request state | `/alaa-laravel-architecture` (`$alaa-laravel-architecture`), `/alaa-php-clean-code` (`$alaa-php-clean-code`), `/alaa-octane-performance` (`$alaa-octane-performance`) |
| Telemetry requirement levels and gates; exposure and trusted-proxy delivery | `/alaa-observability-soc` (`$alaa-observability-soc`), `/alaa-docker-production` (`$alaa-docker-production`), `/caas-arvan-kuber` (`$caas-arvan-kuber`) |

## When not to use

Do not use this skill for authentication in a service that does not sit behind the
Ala gateway: it assumes a verifying edge that such a service lacks, and its rules
will read as permission to trust headers nobody sanitized. Do not use it alone when
the change also lands on an owner's ground above; read the matching skill and follow
the stricter rule where they overlap.
