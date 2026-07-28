# Review triggers and anti-patterns

Read this file when you are reviewing a change that touches the trust boundary, or
when you need the observable that decides whether something you are looking at is a
defect.

Every row below states what you can see in the code or config. A review item you
cannot point at is not a review item.

## Flag it when you observe this

| Observable | Why it is a defect |
|---|---|
| A service reads `X-Project-Id` or `X-User-Id` on a listener reachable without crossing the gateway, and does not strip and reject trusted headers at its own edge | the caller chooses its own identity; there is no authentication on that path |
| A header the gateway injects does not appear in the delete list, or the delete list is conditional on the route being protected | the header is forgeable by any public client on the routes where the delete does not run |
| A tenant id is read from a request body, query string or route parameter and used when `X-Project-Id` is present | the client selects the tenant, and cross-tenant reads follow |
| A client-supplied tenant selector and the trusted context differ, and the code picks one without denying | the choice is silent, so the wrong choice never surfaces in review or in logs |
| Business authorization is absent because the gateway is assumed to have handled it | the gateway authenticates; it does not decide domain actions |
| A permission middleware or authorization wrapper contains an early return, a feature-flag short circuit, or a `TODO` bypass ahead of the real check | requests still look authenticated while authorization is disabled |
| An authorization decision reads a role string, a per-request database lookup, or a claim taken directly from a token instead of the decoded `X-Access` bitmap | four sources of truth for one decision, three of which no one is testing |
| A decoder for the permission bitmap is written locally instead of taken from `alaa-permission-generator` | a bug in bit order or padding is then fixed in one service and not the others |
| A permission id or id range appears hardcoded outside a generated, committed map | the catalog moves and the hardcoded copy does not |
| A raw access token, JWT payload, proof token, TOTP code, recovery code, enrolment secret or `otpauth_uri` reaches a log | those values reconstruct the credential from the log alone |
| Request-scoped auth or tenant context is held in a singleton, a static, or anything a long-lived worker keeps between requests | one request's actor answers another request |
| A raw trusted header is read in a policy, controller, repository or job after ingress normalization | a second parser that will disagree with the first |
| A backend service is documented with gateway-facing routes although the gateway strips its prefix | the documented routes do not exist on that service |
| A service depends on opaque-token introspection, or on the retired profile-blob header contract | neither is implemented in the current path |
| Two services use different codes for the same deny class with no stated compatibility reason | an alert or a dashboard matches half the fleet |
| A response `code` and the deny-log `code` for the same event differ | the incident cannot be joined to the report |
| A service documents a header rule its code does not enforce | the document is read as the contract and the gap ships |
| A step-up-required route is allowed because the step-up feature flag is off in this environment | the route's protection state is invisible to whoever reads the route list |
| An `X-TOTP-*` name other than the three backend-only headers is read by a service | that name is not on the sanitize list, so a public client can set it |
| `202 Accepted` is treated as evidence that auth and tenant validation succeeded | the transport was accepted; the auth result had not been computed yet |
| A client payload field such as `identity.user_id`, `visitor_id` or `device_id` is promoted to trusted actor context when `X-User-Id` is absent | the client names the actor |
| A truthy bypass switch appears in a deployed environment file with no recorded decision beside it | a control is off and nobody chose it in a way that can be audited |
| `tenant_id`, `tenant_public_id` or `X-Tenant-Public-Id` is documented as a distinct concept rather than a legacy alias | two names for one boundary, enforced differently |

## Anti-patterns, named

- **Trusting internal auth headers on a directly exposed service.** The single most
  expensive one, because it looks correct in every test that goes through the
  gateway.
- **Treating gateway authentication as full authorization.** The gateway answers who,
  not whether.
- **Spreading raw header reads across the codebase** instead of normalizing once.
- **Treating a compact identity header as raw client data** rather than as a value
  copied verbatim from a verified claim.
- **Building a fallback for a failed authorization dependency.** A fallback on this
  boundary is a bypass with a friendlier name.
- **Rebuilding authorization from raw client headers** in a service that already has
  the decoded bitmap.
- **Storing a historical identity snapshot and never refreshing the latest local user
  projection** from the trusted payload.
- **Believing a README over the active HAProxy configuration.** The config is what
  runs.
- **Reviewing this boundary with this skill alone** when the change also lands in
  Laravel, HAProxy, security, observability, Octane or deployment ground. The
  companion table in `SKILL.md` names which one, and a review that skips the matching
  companion is incomplete.

## Before you call a trust-boundary change reviewed

1. The service is not reachable without crossing the gateway, or it strips and
   rejects trusted headers at its own edge — and both were checked, not one.
2. One request-scoped context builder exists near ingress, and nothing downstream
   re-reads a raw trusted header.
3. Tenant comes from `X-Project-Id` and actor from `X-User-Id`; the public boundary
   value is validated as UUIDv7; any internal numeric key is derived after that
   validation and stays service-local.
4. A protected request with missing trusted tenant context is rejected, and a route
   requiring an actor rejects a missing actor.
5. Every tenant-aware query and command is scoped by the trusted context.
6. A client tenant-override attempt is denied explicitly.
7. Deny response codes and deny log codes match, with request and trace correlation
   attached.
8. Tests exist for spoofed headers, missing tenant context, malformed compact
   identity headers, cross-tenant access, conflicting tenant selectors, an invalid
   and an unknown-only permission bitmap, every step-up denial case, and any route
   that deliberately allows anonymous traffic.
9. `scripts/trust_boundary_check.py` has been run and its output reported, including
   any check that could not run.
