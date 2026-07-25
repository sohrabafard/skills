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
