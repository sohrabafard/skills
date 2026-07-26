# End-To-End Flow And Boundaries

Use this file when the task is about how the Ala platform fits together end-to-end, especially for onboarding an agent or a frontend developer to the shared system shape.

## High-level system view

The Ala platform is organized in layers with clear ownership:
- client applications send public traffic to the gateway
- the gateway is the external trust boundary
- the gateway verifies access tokens for protected routes, removes untrusted internal headers, injects trusted identity and project context, and forwards requests to the right backend
- when a route family needs fine-grained request-time authorization, the gateway calls `authz-sidecar` or `entitlement-spoa`
- backend services own their business domains and internal logic
- entitlement-platform keeps normalized authorization business truth in `entitlement-api`, projects derived tuples through `projector`, and serves request-time checks from OpenFGA

Rules:
- do not let services recreate browser-facing trust assumptions on internal hops
- the gateway is the only component that verifies an end-user access token. `auth` issues tokens, the
  gateway verifies them, and every other service consumes the trusted headers the gateway projects. No
  other service parses, validates, introspects, or refreshes a bearer token, and no other service reads
  `Authorization` on a product route, because a second verifier drifts from the gateway's answer on
  algorithm, clock skew, issuer, audience, and revocation, and the two then disagree during exactly the
  incident that needs one answer. Observable: in a backend repository, a search for `Authorization`,
  `Bearer`, or the JWT library name returns no read on a product route; an outbound `Authorization` header
  carrying a service credential to a dependency such as OpenFGA is not an end-user token and is out of
  scope for this rule.
- keep route ownership clear so frontend, gateway, and backend work stay aligned
- prefer direct ownership boundaries over convenience coupling across service internals
- backend services may keep local user projections or immutable request snapshots, but `auth` remains the source of truth for current identity state

## Current services and responsibilities

### Existing services

- `auth`
  - canonical auth and profile source of truth for sign-in, tokens, sessions, profile truth, and trusted identity APIs
- `content`
  - new macroservice for `course`, `set`, and `content`
- `vod`
  - legacy learning and playback service during migration; on the deprecation path for learning-content ownership
- `comment`
  - discussion service for comments, replies, likes, moderation, and related activity
- `ticket`
  - support service for ticket creation, replies, assignment, status changes, and follow-up flows
- `wa`
  - watch and analytics ingestion service for event intake and related processing flows
- `entitlement-api`
  - normalized authorization business truth
- `projector`
  - derived tuple writer into OpenFGA
- OpenFGA
  - derived authorization graph for fast request-time checks

### Components being evaluated

These are not yet stable ownership surfaces. Each must satisfy every surface this skill defines that it
actually exposes: envelopes, headers, event and code names, readiness shape, metric names, and the failure
and load contract. Being under evaluation does not exempt a component from a surface it exposes.
- `notification-core`
- `realtime-hub`
- delivery workers
- queue or broker backbones such as RabbitMQ or Redis Streams

## Baseline platform flow

Treat the default Ala flow like this:
- public client or frontend -> gateway -> backend service
- gateway -> request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa` when the route family uses entitlement-platform authorization
- backend service -> backend service only for internal workloads that truly require a synchronous hop
- backend service -> async infrastructure for queue, event, or job delivery when appropriate
- normalized business change -> `entitlement-api` -> `projector` -> OpenFGA for derived fine-grained authorization state

## Simple user journey

In a normal user journey:
- a learner calls a gateway-facing route
- if the route is protected, the gateway verifies the token, strips spoofed internal headers, injects trusted context such as `X-User-Id` and `X-Project-Id`, and decides whether request-time authorization is also required
- sign-in and token refresh flows reach `auth`
- every new learning-content integration targets `content`; only traffic already migrating may still pass through `vod`, and no new integration is built against `vod`
- discussion actions reach `comment`
- support actions reach `ticket`
- watch or telemetry ingestion reaches `wa`
- protected route families that use fine-grained authorization are checked first by `authz-sidecar` or `entitlement-spoa`, using the derived authorization state stored in OpenFGA

From the user point of view, this feels like one product. Inside the platform, each layer keeps a clear responsibility.

## Media timeline unit contract

This contract applies only to media playback positions, media durations, timepoints, and watch analytics. It does not redefine ISO-8601 timestamps, database `created_at`/`updated_at` fields, log fields, metric suffixes, or timeout configuration.

- `content` owns editorial and product playback time in whole seconds: `time_seconds`, `duration_seconds`, `estimated_duration_seconds`, and `last_position_seconds`.
- The client sends and consumes video-linked `comment.timestamp` values in whole seconds. `comment-service` persists the integer unchanged; it must not silently convert the client contract.
- `wa` owns analytics event times and watch-segment positions in whole milliseconds, using fields explicitly suffixed `_ms`, including `event_ts_ms`, `start_pos_ms`, `segment_from_ms`, `segment_to_ms`, and `segment_watched_wall_ms`.
- At the client-to-WA boundary, convert seconds to milliseconds exactly once (`seconds * 1000`). When WA analytics is used to position a content timepoint or a comment/note, convert milliseconds to seconds exactly once (`milliseconds / 1000`) and apply the receiving field's documented integer/rounding policy.
- Do not infer a unit from a bare field name. New cross-service media timeline fields must use an explicit `_seconds` or `_ms` suffix. A pre-existing bare field keeps its owning client/service contract and must be documented at the integration boundary.

## How entitlement-platform fits into the Ala stack

- entitlement-platform does not own authentication; the gateway does
- entitlement-platform may own request-time fine-grained route authorization through `authz-sidecar` or `entitlement-spoa`
- entitlement-platform keeps normalized authorization business truth in `entitlement-api`
- `projector` writes derived tuples
- OpenFGA stores derived effective authorization state

For a normal backend behind gateway, the practical rule is:
- trust the gateway authentication result
- trust the gateway allow or deny result for the route
- normalize trusted identity context once near ingress
- still enforce business authorization, validation, and data-safety rules inside the backend

Do not make a normal backend behave like the gateway, the request-time checker, or the entitlement control plane unless the repository explicitly owns that role.

## Frontend and gateway orientation

Rules:
- frontend clients call documented gateway-facing routes, not service-local routes discovered from backend repos
- frontend clients must never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, `X-User-Roles`, `X-User-Mobile`, `X-User-Fname`, `X-User-Lname`, or `X-Location-*`
- trusted headers belong to the gateway-to-service contract, not the public client contract
- if a route is operational, frontend clients must not treat it as product behavior
- if a route previously depended on the retired profile blob, move that client integration to the public auth or profile APIs instead of reviving `X-Profile`
- for auth terms acceptance and the retired `accept-terms` flow, read `05-scope-service-modes-and-auth-routing.md`, which owns the auth policy routing

Route-shape reminder:
- gateway-facing routes may include a service prefix such as `/auth`, `/content`, `/comment`, `/ticket`, `/vod`, `/wa`, or `/entitlement`
- the current default public gateway service-prefix map for frontend clients and framework-free SDKs is:
  - `auth` -> `/auth`
  - `content` -> `/content`
  - `comment` -> `/comment`
  - `tusd` -> `/tusd`
  - `wa` -> `/wa`
  - `entitlement` -> `/entitlement`
- `entitlement` is the `entitlement-api` admin/control-plane surface (a privileged admin/operator SDK such as `@alaa/sdk-entitlement`), not an anonymous end-user route family; the public prefix uses the short key `/entitlement`, never `/entitlement-api`, and the internal service name stays `entitlement-api`. As with every entry here, the gateway repo owns activation — verify the rendered HAProxy route table before relying on it.
- that first service prefix is a gateway routing prefix, not necessarily a backend route prefix and not necessarily the same concept as a child SDK `servicePrefix`, `apiPrefix`, or fixed ingest path
- clients and SDKs compose the public gateway path exactly once, through an existing public configuration seam such as a service base URL or a child route-prefix option, and must not change a child SDK or service route definition in order to satisfy gateway routing
- trusted internal routes stay service-owned and are not public frontend discovery surfaces
- operational routes remain separate from product routes even when they share the `/api/*` prefix
- service-local routes may differ after gateway prefix stripping
- when `stripPathPrefix: true`, the gateway routes on the public prefixed path, strips only the configured gateway prefix, and forwards the remaining backend-visible service-local path
- do not collapse or de-duplicate repeated path segments at runtime; if a duplicate segment appears, decide whether it is intentional public-vs-child route composition or a bad config, then fix the config seam rather than rewriting paths ad hoc
- for client SDK and frontend package work, do not change child SDK source or backend routes to add a gateway prefix; prefer public config such as core `baseUrls`, child `servicePrefix`/`apiPrefix`, or service-specific path options
- if a child path is fixed, as with WA ingest, apply the gateway prefix through the service base URL
- for aggregate SDKs such as `@alaa/sdk`, default `createAlaaSdk(config)`-style factories to the canonical prefix map, but never rewrite service roots supplied through an injected core; the core owner must provide gateway-compatible roots
- for the current frontend SDK set, auth is special: preserve the auth child route prefix that already includes its service route family and point the auth core base at the gateway root; apply content, comment, tusd, and WA gateway prefixes through shared core `baseUrls`
- do not pass child route-prefix overrides solely for gateway routing, and do not trim, rewrite, or de-duplicate repeated path segments between the gateway prefix and child-defined route path
- before claiming a prefix is active in an environment, verify the gateway route table and the rendered HAProxy config: in the `gateway` repository, read `charts/gateway/values*.yaml` and `docker/values.shared-network.yaml`, then the rendered `gateway.loadbalancer.yaml` or `gateway.ingress.yaml`. Resolve those paths against the local checkout of `gateway`; never hardcode an absolute machine path into this skill or into a service repository.
- use `$alaa-trust-gateway-auth` for exact trusted-ingress and prefix-strip behavior when the task depends on those details; use `$alaa-haproxy` when actual HAProxy routing, ACL order, or path rewriting is in scope

## Role snapshot propagation and provisional backend freeze

Auth issues the compact `rol` access-token claim as a deterministic JSON array of canonical role names. New and refreshed tokens include the claim even when the array is empty. Each role must match `^[a-z][a-z0-9_]{0,47}$`; the array must be bytewise sorted, duplicate-free, contain at most 16 roles, and serialize to at most 1024 bytes of compact JSON.

Gateway rules:
- delete every client-supplied `X-User-Roles` header on public and protected routes before routing
- after successful JWT verification, treat an absent `rol` as temporary compatibility with older tokens
- when `rol` is present, reject malformed JSON, a non-array value, non-string entries, invalid names, unsorted or duplicate values, more than 16 entries, or compact JSON larger than 1024 bytes before proxying
- inject only the normalized compact JSON array as trusted `X-User-Roles`

Downstream rules:
- user-role semantics are not finalized for backend decision-making; read `28-backend-permission-authorization-and-role-freeze.md`
- authorize with catalog-owned permission bits from trusted `X-Access`, plus the contract-defined OpenFGA decision where applicable
- do not add role-based authorization, access tiers, policy selection, data scopes, response shaping, routing, validation, or feature behavior
- a service that passively captures `X-User-Roles` must accept it only from the sanitized gateway path, validate the same bounds near ingress, and keep it distinct from `X-Access`
- roles may be retained only as non-authoritative observability or future-use metadata; their presence, absence, or freshness must not change request outcomes
- do not let a public client supply or override role context
- role changes take effect for new or refreshed access tokens; existing access tokens retain their issuance-time snapshot until refresh, expiry, or revocation
- do not activate role-based backend behavior until this skill explicitly records finalized role semantics and rollout rules

## Operational caller expectations

`10-core-service-contract.md` owns who may call `GET /api/health` and `GET /api/ready` and what a client
must not depend on them for. Read it there.

## Private and public identifier boundary

Rules:
- private database identifiers belong to the service that owns the database and may be used for local persistence, joins, query planning, deterministic ordering, and pagination
- signed opaque cursors may encode private identifiers when needed for stable pagination, but clients must not parse, construct, or depend on cursor contents
- public APIs, URLs, event contracts, SDKs, client-visible references, and cross-service object references expose the owning domain's public identifier, never its private database identifier
- another service must not require access to, or synchronous resolution of, an owning service's private identifier
- OpenFGA and other systems outside the owning database boundary use the canonical public identifier or the contract-defined reversible object identifier derived from it, because the request and authorization boundaries carry public object identity
- for grant discovery, internal ordering may use `updated_at DESC, grant_stream_id DESC`; the private `grant_stream_id` may appear only inside a signed opaque cursor, while response bodies and public references continue to use public identifiers

How to decide whether a field breaks the rule above: for every field in every Resource, DTO, serializer, and
event payload, if dropping the row's auto-increment `id` column would change that field's value, the field
carries a private identifier and is a violation. A field named `id` that returns a UUIDv7 `public_id` passes;
a field named `section_key`, `user_id`, `flagged_by`, or `resolved_by` that returns a table's integer key
fails, whatever it is named.

There is exactly one fleet-wide exception, and it is the **actor identifier**. Read what it is before
reading what it permits: it is **technical debt this contract has recorded and accepted for now, owned by
`auth`**. It is not a design choice, not a precedent, and not a demonstration that numeric identifiers are
acceptable when convenient.

The debt exists because `auth` authenticates against its own `users.id` and puts that integer in the token's
`sub` claim. The gateway projects the claim it was given, so every downstream service receives the integer,
and OpenFGA subjects already encode it as `user:<decimal>`. No consumer chose this; each inherited it from
the token. Recording it as debt rather than leaving it as a bare exception is what stops the next agent from
citing it as precedent — a new numeric identifier for a new domain resource is a violation of the rule
above, and the existence of this row is an argument against it, not for it. There is no second exception,
and adding one is a contract change, not a local decision.

The exception, precisely:
- The numeric `X-User-Id` the gateway projects from the verified `sub` claim is `auth`'s `users.id`. Every
  service already receives it, and OpenFGA subjects already encode it as `user:<decimal>`. A payload may
  carry that value in a field named exactly `user_id` or ending `_user_id`.
- A service must carry the value it received in `X-User-Id` into such a field, never its own local
  users-table key, because two services emitting different numbers for one person is the failure this
  exception is narrow enough to prevent.
- The exception covers the actor identifier and nothing else. A comment id, a course id, a section id, a
  grant id, a flag id, or any other domain resource id is a public identifier and is never a database
  integer on the wire.
- `auth` owns the change that ends the debt, and no other service can end it: `users.uuidv7` already
  exists, and the exception closes when `auth` puts a public user identifier in the token claim, the gateway
  projects it, and every consumer reads it. Until that change ships, a service that invents its own public
  user identifier creates a third spelling of one person and is a violation today.
- The debt's per-service status and the migration item on `auth` are recorded in `95-fleet-conformance.md`.
  A dated closure record belongs there when the change ships, not in this rule.

### Canonical `project_id` form

`project_id` is a canonical UUIDv7 string on every surface where that field name appears. There is no
exception, and unlike the actor identifier above, none has ever been accepted.

The four surfaces, named because each one has been got wrong somewhere in the fleet:
- **HTTP payload** — request bodies, query parameters, DTOs, Resources, and serializers, inbound and
  outbound.
- **Event envelope** — the `project_id` field of the domain event envelope in
  `20-operational-and-observability-contract.md`, and of any command that carries one.
- **Log field** — the `project_id` structured log field in the same file.
- **Cache key** — every cache, lock, and rate-limit key whose scope is a project.

A service may still store, join, and index on an internal numeric project key. What it may not do is spell
that integer `project_id` on any of the four surfaces above. The reason differs per surface and all four
matter: a consumer in another service holds no mapping from `42` to a project and cannot recover the scope
of a fact; an operator correlating a log line to an event cannot join two different spellings of one tenant;
and a cache key built from the storage id cannot be invalidated by any component that holds only the public
identifier, so two services caching one tenant's data build two key spaces that never invalidate each other.

This is a live violation, not a hypothetical: `auth`'s outbox envelope emits `"project_id": 42`
(`app/Services/Messaging/RabbitMqOutboxPublisher.php:62-75`, asserted by
`tests/Feature/OutboxRelayCommandTest.php:71-84`) while `entitlement-api` emits a UUIDv7 in the same field.
Any consumer that reads both is reading two incompatible types under one name.

When no mapped row exists for an internal project id, the service omits the field entirely and emits
`input.validation.failed` with a stable validation code naming the unmapped id. It must not emit `null` as
if the project were absent, must not fall back to the internal numeric id, and must not invent a placeholder
UUID. An unmapped id is a data defect in the project registry, and substituting a value moves the defect
into every downstream consumer.

Observable that decides compliance: every Resource, serializer, outbox builder, event builder, log-context
builder, and cache-key builder that writes `project_id` writes the UUIDv7 string, never the column a foreign
key references. Search the repository for `project_id` and check the type at each write site; an integer at
any of them fails.

Laravel-specific validation, the registry lookup, and the resolve-in / resolve-out helper names are owned by
`30-trusted-ingress-and-laravel-contract.md`.

## List pagination contract

This file owns the **wire shape**: which parameters a list route accepts, which keys its response carries,
and which keys it must not. It does not own the **design method** — how to derive an ordering tuple whose
final component is unique, which composite index serves it, how the continuation predicate is written, what
the signed cursor carries, and how nullable sort columns, mutable sort values, and backward traversal are
handled. Those belong to `alaa-keyset-pagination`, invoked as `/alaa-keyset-pagination` in Claude Code and
`$alaa-keyset-pagination` in Codex. Read that skill before writing or reviewing a paginated query; read this
section for the keys that cross the wire.

Every list route on every Ala service paginates by keyset cursor. Offset pagination is forbidden on any list
a client can page through, except under the admin-table exception stated below, because an offset page
silently repeats or skips rows when a row is inserted or deleted between two requests, and because deep
`OFFSET` makes the database read and discard every skipped row on every page.

Request rules:
- The cursor parameter is `cursor`. Its value is the opaque string the previous response returned, and the
  client sends it back unchanged.
- The page-size parameter is `limit`, a positive integer, with a maximum the route documents.
- A `limit` above the documented maximum is rejected with `400` and code `INPUT_VALIDATION_FAILED`. It is
  not silently clamped, because a client that asked for 500 and received 100 cannot tell it received a
  partial answer.
- `page`, `per_page`, `offset`, and `skip` are not accepted parameters. A service that accepts one today
  removes it through the deprecation procedure in `22-failure-load-and-deprecation-contract.md`.

Response rules:
- A collection response body carries `data` as an array, `meta.next_cursor`, and `meta.prev_cursor`.
- `meta.next_cursor` is a string when a further page exists and is `null` on the last page. `meta.prev_cursor`
  is a string when a page exists before the current one and is `null` at the start of the collection. Both
  keys are present in every collection response, including the first page and the last page, because a
  consumer must distinguish "no page in that direction" from "this service forgot the cursor", and an
  omitted key cannot express that difference.
- The client echoes back whichever of the two cursors it holds in the same `cursor` parameter. Direction is
  encoded inside the signed cursor, not in the parameter name, so a client cannot pair a forward boundary
  with a backward request. A route does not document backward pagination until the reversal tests named by
  `alaa-keyset-pagination` (`/alaa-keyset-pagination`, `$alaa-keyset-pagination`),
  `references/70-test-list.md`, pass.
- `has_more` and `type` are not emitted. `has_more` is `next_cursor !== null` by construction, and a second
  spelling of one fact diverges the first time a service computes it from the row count instead; `type` is
  constant across every Ala keyset list and only invites clients to branch on it.
- `meta` may carry service-declared counters the route documents, such as `meta.counts`. It must not carry
  `total`, `total_pages`, `current_page`, `last_page`, or `per_page`: those are offset artifacts, and a
  client that reads them builds page-number navigation the service cannot serve.
- A `links` object built from page numbers is not emitted for a keyset list. `links` stays available for
  true document navigation, per `30-trusted-ingress-and-laravel-contract.md`.

Ordering and cursor rules:
- The query orders by a stable tuple whose final component is unique, and the cursor encodes that tuple, so
  two rows with equal sort values cannot straddle a page boundary.
- The cursor is opaque and signed; clients must not parse, construct, or depend on its contents. It may
  encode private identifiers, per the identifier boundary above.

The admin-table offset exception:

Offset is permitted on a list only when every one of these five conditions holds. Four are checkable from
the route table and the route's own code; the fifth is checkable from its documentation. A route that
satisfies four of five uses keyset.

1. The route is mounted under an admin-only path and requires an admin permission checked at request time,
   from trusted `X-Access` per `28-backend-permission-authorization-and-role-freeze.md`.
2. The route is absent from the public gateway route table and from every published SDK and client bundle.
3. The list's size does not grow with tenant data. A table of projects, providers, permission definitions,
   or configured roles qualifies; a table of comments, courses, tickets, watch events, or notifications does
   not, however small it is today.
4. The route enforces a documented maximum reachable offset and a documented maximum page size, and rejects
   a request above either with `400` and code `INPUT_VALIDATION_FAILED`. It does not clamp.
5. The route's own documentation records `pagination: offset` together with the named operational
   requirement that makes exact totals necessary — which report, which operator workflow. "Totals are nice
   to have" and "an operator asked for totals" are not requirements.

An offset route does not use the `meta` collection envelope, because `total`, `total_pages`, `current_page`,
`last_page`, and `per_page` are forbidden inside `meta` by the rule above and that rule is not relaxed here.
It declares its own response envelope in its documentation, so no consumer can mistake one shape for the
other and no shared client parser has to guess which it received.

Observable that decides whether a route has claimed the exception legitimately: a route emitting `total`,
`total_pages`, `current_page`, `last_page`, or `per_page` that is reachable without an admin permission, or
that appears in the public gateway route table, is a violation regardless of what its documentation says.
The five conditions and their reasoning are owned by `alaa-keyset-pagination`
(`/alaa-keyset-pagination`, `$alaa-keyset-pagination`), `references/10-route-mode-and-sort-allowlist.md`;
this section is the contract text that authorizes them.

Scope:
- A route that returns a bounded set with no paging parameters at all — a fixed catalog, a per-user session
  list — documents `paginated: false` in its OpenAPI or route documentation and returns `data` with no
  `meta.next_cursor`. A result set that grows with tenant data may not use that declaration.

Observable that decides compliance: the repository contains a keyset paginator call site for every list
route that has not recorded the five-condition exception above, no such route validates or reads
`per_page`/`page`/`offset`, and a saved example for at least one list route shows both a non-null and a
`null` value for each of `meta.next_cursor` and `meta.prev_cursor`. A repository whose own `AGENTS.md` mandates
keyset pagination while its list code calls an offset paginator, or calls no paginator at all, is
non-conforming even though its documentation is correct.

## Internal service-to-service mTLS rollout status

Decision:
- internal service-to-service mTLS is deferred as a coordinated platform initiative until the major system components and their internal route contracts are complete
- this deferral applies to internal service hops generally; it is not a statement that the earlier entitlement-to-content concern was specifically a gateway-to-service hop
- do not block a feature or introduce bespoke per-service mTLS terminators, sidecars, certificate mounts, internal Services, or NetworkPolicies solely to complete one service while this deferral is active
- reactivate mTLS work only through an explicit platform-wide decision, or stop for a new security decision when a route would expose high-risk production traffic beyond the approved private boundary

Interim rules:
- keep internal routes private and absent from public gateway or frontend discovery surfaces
- preserve spoofing defenses, trusted-header sanitization, request correlation, timeouts, bounds, and fail-closed behavior required by the owning service contract
- document the temporary network or trusted-header assumption; do not describe a private network or an identity header as cryptographic service authentication
- do not invent a repo-local replacement authentication scheme during the deferral

## Internal hop discipline

Every rule about how long an internal hop may take, how many times it may be retried, whether it may be
retried at all, and what the caller does when the far side is unreachable lives in
`22-failure-load-and-deprecation-contract.md`. Read it before writing any internal client. The rules below
are the correlation and ownership half of the same seam.

Rules:
- preserve `X-Request-Id` and `traceparent` across internal HTTP hops
- construct every internal client with an explicit timeout and an explicit retry budget from
  `22-failure-load-and-deprecation-contract.md`; an internal call with a default or absent timeout is a
  contract violation even when the dependency is healthy
- keep trusted header parsing and normalization close to the receiving edge
- keep operational routes separate from product-facing routes
- do not proxy another service's `/api/ready` unless that dependency is an explicit approved rollout requirement
- if a service depends on shared infrastructure such as Redis or RabbitMQ, check that infrastructure directly instead of proxying another app's status
- if a frontend or service needs domain behavior from another service, prefer that service's public API or events over direct table coupling
- downstream services may consume compact trusted name and location headers, but they must not fabricate display-name fields from compact ids unless another explicit source-of-truth contract owns that lookup
- backend services may keep local user projections or immutable request snapshots, but `auth` remains the source of truth for the latest identity state

## Repo-role reminders

### Frontend repository

- call gateway-facing public routes only
- never generate trusted internal headers
- never call `authz-sidecar`, `entitlement-spoa`, or OpenFGA directly

### Gateway repository

- own authentication, spoofing defense, trusted-header injection, and request-time authorization inputs
- keep request-time authorization fail-closed

### Backend service behind gateway

- consume normalized trusted context
- keep controllers and policies away from raw header parsing
- do not use allow-side `X-Authz-*` metadata as authorization input

### Entitlement-platform repository

- own fine-grained authorization contracts, request-time checker behavior, and tuple projection rules
- do not turn OpenFGA into business truth

## Why this file exists

This file gives one concise picture of:
- what the public client is allowed to do
- what the gateway owns
- what backend services own
- how `content` and legacy `vod` fit during migration
- where async boundaries belong

That helps agents keep frontend, gateway, and backend work consistent instead of treating each repository as an isolated system.
