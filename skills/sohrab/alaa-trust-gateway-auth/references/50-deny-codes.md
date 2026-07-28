# Deny codes at the trust boundary

Read this file when you are choosing the code a deny carries, translating a gateway
error name into a service contract, or reconciling two services that deny the same
thing differently.

The response envelope, the field set inside it, and the platform-wide error-code
taxonomy are owned by `/alaa-services-contract` (`$alaa-services-contract`)
`references/10-core-service-contract.md`. What this file owns is which code applies
to which trust-boundary failure and what it maps from.

## Three rules that decide most cases

1. **The `code` in the API response and the `code` in the deny log are byte
   identical.** A service may keep internal policy labels, but the outward code and
   the logged code never diverge, because the log is how an incident is joined to a
   report and a rename in one place breaks that join silently.
2. **One canonical code per failure class across services.** When a service
   translates a gateway denial, it preserves the semantic code rather than inventing
   a synonym. Two names for one class means an alert matches half the fleet.
3. **The code set is append-only.** Add a code; never repurpose one. A caller that
   branches on a code branches on its old meaning until it is redeployed.

Never put a raw token, a full JWT payload, a secret, key material or a stack trace
in a response or a log. Keep `message` short, user-facing and free of verifier
internals, and keep `meta` small and safe — a claim name such as `pid`, a header
name such as `X-User-Mobile`, a purpose string.

## Canonical codes

| Code | HTTP | Applies when |
|---|---|---|
| `AUTH_MISSING_TOKEN` | 401 | a protected route carries no usable bearer token |
| `AUTH_INVALID_TOKEN` | 401 | the token exists but cannot be accepted, and no narrower reason may be exposed |
| `AUTH_TOKEN_EXPIRED` | 401 | the token is expired |
| `AUTH_TOKEN_NOT_YET_VALID` | 401 | `nbf` is in the future |
| `AUTH_INVALID_SIGNATURE` | 401 | signature verification failed; the gateway promotes this class to higher-severity logging |
| `AUTH_DISALLOWED_ALG` | 401 | the JWT algorithm is not on the allow-list |
| `AUTH_BAD_ISSUER` | 401 | the issuer is invalid for this verifier |
| `AUTH_BAD_AUDIENCE` | 401 | the audience is invalid for this verifier |
| `AUTH_MISSING_REQUIRED_CLAIM` | 401 | a required claim is absent; `meta.claim` names it |
| `AUTH_CONTEXT_MISSING` | 401 or 403 by service policy | the service expected trusted gateway context and did not receive enough of it |
| `AUTH_ACCESS_HEADER_MISSING` | 401 | `X-Access` was expected and is missing or blank |
| `AUTH_ACCESS_BITMAP_INVALID` | 401 | `X-Access` is present but not a valid unpadded base64url bitmap, or maps to no known permission for this service |
| `AUTH_ROLE_RESOLUTION_FAILED` | 401 | permission context decoded but no internal role or tier could be derived |
| `AUTH_MOBILE_HEADER_MISSING` | 401 | configuration requires `X-User-Mobile` and it is missing or blank |
| `AUTH_MOBILE_HEADER_INVALID` | 422 | `X-User-Mobile` is present and malformed |
| `AUTH_NAME_OR_LOCATION_HEADER_INVALID` | 400 | a trusted name or location header violates the compact contract |
| `AUTH_NAME_OR_LOCATION_HEADER_REQUIRED` | 400 | a route that deliberately requires trusted identity headers did not receive one |
| `TOTP_REQUIRED` | 403 | the operation requires TOTP and the actor has not enrolled |
| `TOTP_STEP_UP_REQUIRED` | 403 | a step-up-required route received no valid proof; `meta.purpose` names the purpose the client must request |
| `AUTHZ_DENIED` | 403 | the caller is authenticated and not allowed to perform the action |
| `TENANT_CONTEXT_MISSING` | 400 on an HTTP route, or 401/403 by service policy | a tenant-safe operation has no trusted tenant context |
| `TENANT_CONTEXT_MISMATCH` | 403 | trusted tenant context and the requested target do not match |
| `TENANT_CONTEXT_INVALID` | 403 | a client-supplied tenant selector conflicts with trusted context, or a tenant-override attempt was detected |

## Translating gateway error names

The gateway emits lower-level names. A service that logs or surfaces the same
problem in its own contract translates them:

| Gateway name | Canonical code |
|---|---|
| `missing_token` | `AUTH_MISSING_TOKEN` |
| `disallowed_alg` | `AUTH_DISALLOWED_ALG` |
| `invalid_signature` | `AUTH_INVALID_SIGNATURE` |
| `verify_error` | `AUTH_INVALID_TOKEN` |
| `missing_exp` | `AUTH_INVALID_TOKEN` |
| `expired` | `AUTH_TOKEN_EXPIRED` |
| `not_yet_valid` | `AUTH_TOKEN_NOT_YET_VALID` |
| `bad_issuer` | `AUTH_BAD_ISSUER` |
| `bad_audience` | `AUTH_BAD_AUDIENCE` |
| `missing_claim_<claim>` | `AUTH_MISSING_REQUIRED_CLAIM` |

The gateway also records a `totp_proof_status` field — `validated`,
`invalid_signature`, `expired`, `context_mismatch` and similar — for SOC visibility.
It does not change the request's status, and it has no canonical service-side
translation because the request was not denied at the gateway.

**Do not collapse a downstream header-validation failure into a gateway verifier
failure.** `AUTH_ACCESS_BITMAP_INVALID` and `AUTH_ROLE_RESOLUTION_FAILED` happen
after gateway verification, inside the service's normalization layer, and an
incident that confuses the two sends an operator to the wrong repository.

## Async transport

For an accept-then-validate service, the public transport contract and the internal
auth result stay separate. Once `202` has been returned, the canonical code appears
in logs, metrics, dead-letter reasons and audit events, and no later public auth
response is sent.

## Adopting these codes in an existing service

A new or changed service adopts these codes directly. An existing service with a
deployed response contract migrates additively: add the canonical code to logs
first, then align the response payload in a version the callers were told about.
Do not break a deployed response contract to reach uniformity.
