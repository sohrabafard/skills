# What a service behind the gateway does with trusted context

Read this file when you are writing or reviewing the ingress layer of a service
that sits behind the gateway: middleware, guards, request-context builders, tenant
scoping, or the code that turns headers into an actor.

## Layer ownership

| Layer | Owns |
|---|---|
| Frontend or public client | calling documented gateway-facing routes, and sending `Authorization: Bearer` to the gateway and nowhere else |
| Gateway | authentication, sanitizing spoofable inbound headers, injecting trusted headers from verified claims, calling the request-time checker, denying on deny or dependency failure |
| Request-time checker (`authz-sidecar`, `entitlement-spoa`) | the fine-grained route decision, against the pinned OpenFGA model |
| Backend service | normalizing trusted context once, then business authorization and tenant-safe data access |
| `entitlement-api` | normalized authorization business truth |
| `projector` | derived tuple writes; it is the only intended writer |
| OpenFGA | derived effective authorization state, never the business source of truth |

A public client never generates a trusted internal header and never calls
`authz-sidecar`, `entitlement-spoa` or OpenFGA directly.

A normal backend service does not behave like the gateway, the request-time checker
or the entitlement control plane. A verified token plus injected headers does not
mean the caller may perform the requested operation; it means the caller is who the
headers say. Business authorization still runs.

`X-Authz-*` decision metadata is observability, not a credential and not a second
authorization system. A service that re-derives a decision from allow-side
`X-Authz-*` values has built a parallel authorizer that will disagree with the real
one.

## Normalize once, at ingress

Build the request-scoped trusted context once, near the service edge, and read only
that context afterwards. Normalize at least: project id, actor id, token id when
the domain audits it, request id for correlation, and the trusted name and location
fields the service actually uses.

- No policy, controller, repository, job or helper re-reads a raw trusted header
  after normalization. A second read is a second parser, and the two disagree the
  first time a header shape changes.
- In a codebase with mixed guard access patterns, resolve the trusted actor once and
  attach it to every resolver the code still reads — `Auth::user()`,
  `$request->user()`, `auth('api')->user()`, and any legacy custom guard. Migrating
  one guard while others remain produces helpers, policies and controllers that
  disagree about whether the request is authenticated.
- In Octane or any long-lived worker, trusted context is strictly request-scoped and
  reset on every request. Read `/alaa-octane-performance`
  (`$alaa-octane-performance`) before putting auth state anywhere a worker keeps.
- If a compatibility layer attaches trusted context to an Eloquent model, keep the
  attribute transient and non-dirty so a later `save()` cannot persist a
  gateway-only value into a column. Auth-service demonstrates the pattern: set the
  attribute for request-time reads, then sync the original so the model is not dirty.

Framework-shape questions — where the middleware lives, what the DTO looks like,
how the response is built — belong to `/alaa-laravel-architecture`
(`$alaa-laravel-architecture`) and `/alaa-php-clean-code` (`$alaa-php-clean-code`).

## Tenant-safe request handling

- Scope every tenant-aware read and write by the trusted tenant context. Not the
  first query — every query.
- Reject an HTTP request that lacks `X-Project-Id` on a tenant-scoped route with
  `400` and `TENANT_CONTEXT_MISSING`. Falling back to a default project id is
  confined to console and queue execution, where there is no caller. A route that
  admits tokenless requests takes a guest request's project id from the request body,
  or from a `project_id` query parameter when the request has no body;
  `references/10-verification-and-ingress.md` states that rule and what it rejects.
- When a client-supplied tenant selector in a body, query string, route parameter or
  untrusted header conflicts with the trusted tenant context, deny explicitly with
  `TENANT_CONTEXT_INVALID`. Silently preferring one source is how a cross-tenant read
  ships without anyone choosing it. A selector is a field the route reads while
  trusted context is present; a guest route's `project_id`, in the body or the query
  string, is read only on the branch where no trusted `X-Project-Id` arrived, so on
  the branch where the header is present there is nothing to compare.
- An extra tenant-shaped identifier accepted for lookup, reporting or local routing
  is an untrusted selector until it has been matched against the trusted context.
- Never let a request-body identity field override or replace trusted tenant context,
  including in anonymous and analytics flows.
- Validate the public boundary value as UUIDv7. Derive any internal numeric key from
  it inside the service and keep that key service-local.

## Anonymous and partially-trusted modes

- A service that intentionally serves anonymous traffic states that policy
  explicitly. In that mode tenant context stays mandatory while actor context is
  optional.
- A route serving anonymous reads scopes by a client-asserted project id only under
  the read rule in `references/10-verification-and-ingress.md`, which states the test
  a route passes to be listed, what ingress does for a route that is not listed, and
  what takes a listed route off again.
- When `X-User-Id` is absent, never synthesize a trusted actor from a client payload
  field such as `identity.user_id`, `visitor_id` or `device_id`. Store those as
  untrusted analytics metadata if the domain needs them, and classify them that way
  in the schema.
- Not every gateway-backed service is tenant-scoped. Do not invent `project_id`
  enforcement in a service that has no real tenant boundary to make documentation
  look uniform. When such a service later becomes tenant-aware, add trusted
  `X-Project-Id` normalization first, then scope reads and writes from it.

## Accept-then-validate

Some services accept a batch with `202 Accepted` and validate trusted context inside
the pipeline afterwards.

`202` means the request was received and queued. It does not mean auth and tenant
validation succeeded. A later transform that finds `X-Project-Id` missing or
malformed drops the data: the transport was accepted and the business result is a
denial.

- When required trusted context is missing after accept, log the canonical code —
  `AUTH_CONTEXT_MISSING`, `TENANT_CONTEXT_MISSING`, `TENANT_CONTEXT_MISMATCH` — and
  drop, quarantine or dead-letter according to service policy.
- Do not invent a second public `401` or `403` after a `202` has been returned. The
  caller already has the transport response; the auth result belongs in logs,
  metrics, audit events, dead-letter reasons and operator-facing monitoring.
- When the product needs the client to learn about an auth failure immediately, that
  route does not use accept-then-validate. Move the checks before the `202`, or have
  the gateway enforce them.

## Header-by-header rules

- `X-Project-Id` is the public tenant boundary input. `X-User-Id` is the
  authenticated actor. `X-REQUEST-ID` is correlation only.
- `X-Access` and `X-USER-SCOPES` are verified token context; server-side permission
  rules still run.
- `X-User-Mobile` is supplemental identity or audit context by default. Each service
  exposes one config switch deciding whether it is optional or required, defaulting
  to optional. When it is optional and absent, continue without mobile context. When
  it is present and malformed, return `422` `AUTH_MOBILE_HEADER_INVALID`. When it is
  required and missing or blank, return `401` `AUTH_MOBILE_HEADER_MISSING`.
- `X-User-Fname` and `X-User-Lname` are optional trusted strings; every
  `X-Location-*` header is an optional trusted integer id.
- Normalize the compact null sentinels — empty string for a name, `0` for a location
  id — once at ingress, into the repository's own shape for absence. See
  `references/20-claims-headers-and-sentinels.md`.
- When a header is absent entirely, do not fabricate it. Normalize the absence
  consistently and document the chosen behaviour.
- Do not derive a location display name from a compact id. The claim carries the id
  and nothing else, so a name derived locally is a second catalog that will disagree
  with auth's. When the product needs names, add the lookup as a named contract with
  an owning service, and cite that contract where the lookup is used.
- Keep one canonical spelling in docs and tests even though HTTP header names are
  case-insensitive.
- Keep the trusted projection compact. A second user-context shape in the same
  service guarantees the two diverge.
- When the service persists user data, keep the latest projection in a local `users`
  read model, and keep immutable request-time snapshots only where the domain needs
  history or audit.

`scripts/trust_boundary_check.py --source-root <dir> --allowlist <file>` reports
every `X-*` name the service reads that is not on the frozen list.

## Consuming the permission bitmap

The obligation is stated as an absolute in `SKILL.md`: an authorization decision
behind the gateway comes from the decoded `X-Access` bitmap, through the decoder
emitted and governed by `/alaa-permission-generator`
(`$alaa-permission-generator`). This section covers what a service does around that
decoder.

- `X-Access` is the gateway's projection of the verified `prm` claim. Permission
  meaning comes from the service's generated, committed permission map — a PHP
  config, a generated Go map, or the generated TypeScript catalog — never from a
  bit label written by hand and never from the gateway.
- Auth derives `perm_bm` from catalog-owned `bit_index`, not from a local package
  table id. Compilation precedence in auth is direct deny, then direct allow, then
  role grants.
- Decode once, at ingress. Map known ids to permission names from the generated
  config, attach the names to the request-scoped actor, and let policy checks read
  the normalized names.
- A set bit whose id this service does not know grants nothing and is not an error.
  The bitmap is issued against the whole platform catalog, so out-of-range ids are
  the normal case, and a bitmap wider than this service's maximum decodes rather
  than fails.
- A protected request whose bitmap resolves to zero known permissions is rejected
  during normalization with `AUTH_ACCESS_BITMAP_INVALID`. The legacy failure mode —
  decode, find nothing, continue until a later generic `unauthorized` fires —
  produces a deny with the wrong code and a log that cannot be diagnosed.
- The frontend's unverified UI-hint decode of its own token is a different case: a
  valid token with no recognised permissions is legitimate there and never
  invalidates a session or signs the user out. Reading `prm` from your own token is
  also not asserting `X-Access`, which a public client never sends.
- A service defines and documents its own role derivation from decoded permissions,
  and does not assume another service uses the same ids or the same derivation.

**This skill states no permission id and no id range.** Ids, ranges, ownership and
the active count are catalog state that changes without this skill knowing, and a
copied range is stale the day it is written. Resolve every id from
`/alaa-permission-generator` (`$alaa-permission-generator`) and the catalog's own
generated output. As one observation with a date attached: on 2026-07-27 the
catalog held 130 active permissions with highest bitmap id 130, contiguous from 1,
which is ahead of the 119 recorded in `alaa-services-contract`
`references/35-permission-catalog-and-service-configs.md:58`. Verify against the
catalog, not against either number.

## Logging denies

- Log the same `code` in the response and in the deny log. When a service maps an
  internal policy decision to a route-specific outward code, the two stay identical,
  or the log cannot be joined to the incident.
- Log `code`, reason, HTTP status, request id, project id and user id when known,
  `token_jti` when known, route, and `auth_source` (`gateway` or `service`).
- Never log a raw token, a full JWT payload, a proof token, a TOTP code, a recovery
  code, key material or a stack trace in an auth deny.
- Preserve inbound `traceparent`, `tracestate` and `baggage` across HTTP boundaries.
  On async boundaries forward `traceparent` and `tracestate`, and forward only
  baggage keys reviewed as safe.
- Requirement levels, gates and reasons for telemetry are owned by
  `/alaa-observability-soc` (`$alaa-observability-soc`); field names and values are
  owned by `alaa-services-contract`.
