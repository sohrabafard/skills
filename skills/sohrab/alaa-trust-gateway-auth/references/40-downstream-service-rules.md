# What downstream services must do

## How this fits with entitlement-platform

- authentication still belongs to the gateway
- route-level fine-grained authorization belongs to the active request-time checker such as `authz-sidecar` or `entitlement-spoa`
- normalized authorization business truth belongs to `entitlement-api`
- derived tuple writes belong to `projector`
- OpenFGA stores derived effective authorization state

For a normal backend behind the gateway, the practical rule is:
- trust the gateway authentication result
- trust the gateway allow or deny decision for the route
- normalize trusted identity context once
- then enforce service-local business authorization and data-safety rules inside the backend

Do not make a normal downstream service behave like the gateway, the request-time checker, or the entitlement control plane.

## Network and trust boundary rules

- A service may trust gateway auth headers only if the request came through the trusted edge and sanitized gateway path.
- If a service can be reached directly, it must either block that exposure or strip and reject internal auth headers at its own edge.
- Internal auth headers are hop-by-hop trust artifacts inside your platform, not public API inputs.
- Frontend clients must never generate or rely on trusted internal headers such as `X-Project-Id`, `X-User-Id`, `X-Access`, `X-User-Mobile`, `X-User-Fname`, `X-User-Lname`, or `X-Location-*`.

## Authentication vs authorization

- Treat the gateway as the authentication and context-propagation layer.
- Treat the active request-time checker as the route-level fine-grained authorization layer.
- Treat each downstream service as the business-authorization layer for business actions after trusted context is normalized.
- A verified token plus injected headers does not mean the user may perform the requested operation.
- Legacy migration rule: do not copy older per-request auth-service callback patterns into new gateway-backed services.
- If a legacy `user-token` path must remain temporarily during migration, classify it as a service-specific compatibility path only. Do not document it as the canonical platform auth contract and do not let it weaken gateway-trusted header rules for normal service routes.
- Do not treat allow-side `X-Authz-*` decision metadata as a second authorization system.
- Do not call OpenFGA directly from a normal downstream service unless that repository explicitly owns request-time authorization runtime behavior.
- Do not make the gateway a backend permission-catalog consumer. The gateway verifies JWTs, strips spoofable headers, injects trusted context, and delegates route/resource authorization to the `authz-sidecar`/OpenFGA path when configured.

## Laravel Gate and policy flow

- Build the request-scoped actor and tenant context before any framework authorization runs.
- Keep raw gateway-header parsing in middleware or a dedicated request-context layer, not in controllers and not scattered across policies.
- In Laravel services with mixed legacy guard access patterns, resolve the trusted actor once and attach it to every guard and resolver the codebase still reads, such as `Auth::user()`, `$request->user()`, `auth('api')->user()`, or a legacy custom guard.
- If you migrate only one guard while other legacy guard lookups remain, helpers, policies, and controllers can disagree about whether the request is authenticated.
- Use policy or Gate responses to express business authorization decisions after auth context normalization, not as a substitute for gateway verification.
- Compact trusted name and location headers belong to the same one-time normalization layer; do not re-read them in policies or controllers.

## Tenant-safe request handling

- Build request-scoped auth context once near the service edge.
- Normalize at least these fields into a trusted request context object:
  - tenant or project id
  - actor or user id
  - token id when useful for audit
  - request id for trace correlation
  - trusted compact name fields when the service uses them
  - trusted compact location ids when the service uses them
- Authorization code should read the normalized request context or server-side request attributes only. Do not re-read raw tenant or actor headers inside policies, services, or repositories after normalization.
- Laravel Eloquent safety rule: if you attach trusted `project_id` or similar request-scoped auth context directly to a model instance for compatibility, keep it transient and non-dirty immediately or keep that context off the model entirely.
- Auth-service shows one safe compatibility pattern for non-persistent model context: set the trusted attribute for request-time reads, then sync the original attribute so later `save()` calls do not try to persist a gateway-only value into the database.
- HTTP requests without `X-Project-Id` must be rejected with `400`; fallback to the default project id is only allowed for console or queue execution, not normal HTTP traffic.
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.
- If a client-supplied tenant selector in body, query, route, or non-trusted header conflicts with the trusted tenant context, deny explicitly instead of silently choosing one source.
- If a service accepts an extra tenant-shaped identifier for resource lookup, reporting, or local routing, treat it as an untrusted selector until it is matched against the trusted tenant context.
- If a route or service intentionally supports anonymous traffic, make that policy explicit. In that mode, tenant context can still be mandatory while actor context is optional.
- Even in anonymous or analytics flows, never let request-body identity fields override or replace trusted gateway tenant context.
- Do not derive location display names from compact ids unless another explicit contract adds that source of truth.

## Async ingest and accept-then-validate flows

- Some downstream services accept transport with `202 Accepted` and then validate trusted context inside an async pipeline or ingestion worker.
- Plain meaning: `202` means `I received your request and queued or started processing it`. It does not mean `auth and tenant validation already succeeded`.
- This pattern is common in analytics or ingestion services where the HTTP layer accepts a batch quickly and deeper validation happens in transforms, workers, queues, or sinks after the response is sent.
- Example: a request reaches the service, the HTTP source returns `202`, then a later transform notices that trusted `X-Project-Id` is missing or malformed and drops the data. In that case the transport was accepted, but the business result is still a denial or discard.
- If required trusted context is missing after accept, log a canonical internal code such as `AUTH_CONTEXT_MISSING` or `TENANT_CONTEXT_MISMATCH` and drop, quarantine, or dead-letter the data according to service policy.
- Do not invent a second public `401` or `403` contract after a `202` has already been returned. The caller already received the transport response; the later auth result belongs in logs, metrics, audit events, dead-letter reasons, or operator-facing monitoring.
- If the product needs the client to receive immediate auth failure, do not use accept-then-validate for that route. Move auth/context checks before the `202` response or require the gateway to enforce them earlier.

## Header usage rules

- Use `X-Project-Id` as the public tenant boundary input.
- If a legacy service still exposes `X-Tenant-Public-Id`, treat it as the old name for the same public `project_id` boundary and plan to rename it to `X-Project-Id` during refactor.
- When validating the public tenant boundary value carried in `X-Project-Id`, validate it as UUIDv7.
- Example header value: `X-Project-Id: 018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- If a service still needs an internal numeric project key after validation, derive or load it from the trusted public `X-Project-Id` boundary inside the service and keep that numeric key service-local.
- API-document rule: document `X-Project-Id` with a UUIDv7 example, and if a service still mentions `X-Tenant-Public-Id` or `tenant_public_id`, mark that name as legacy and equivalent to the public `project_id` boundary.
- Use `X-User-Id` as the authenticated actor id.
- Use `X-Access` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-REQUEST-ID` only as correlation.
- Keep one canonical spelling for documentation and tests even though HTTP header names are case-insensitive.
- Treat `X-User-Mobile` as supplemental identity or audit context by default.
- Each downstream service must expose one config switch that decides whether `X-User-Mobile` is optional or required. The default policy should be optional.
- If that config marks mobile as required, the service must enforce it automatically and return the same shared error code and response contract used everywhere else.
- Shared mobile-header contract:
  - when mobile is optional and the header is absent, continue without mobile context
  - when mobile is present but malformed, return `422` with code `AUTH_MOBILE_HEADER_INVALID`
  - when mobile is required but missing or blank, return `401` with code `AUTH_MOBILE_HEADER_MISSING`
  - use one stable response envelope for both cases:
    ```json
    {
      "error": {
        "status": 401,
        "code": "AUTH_MOBILE_HEADER_MISSING",
        "message": "Required user mobile header is missing.",
        "meta": {
          "header": "X-User-Mobile"
        }
      }
    }
    ```
  - invalid-format example:
    ```json
    {
      "error": {
        "status": 422,
        "code": "AUTH_MOBILE_HEADER_INVALID",
        "message": "Invalid user mobile format.",
        "meta": {
          "header": "X-User-Mobile",
          "expected_format": "11 digits starting with 09"
        }
      }
    }
    ```
- Treat `X-User-Fname` and `X-User-Lname` as optional trusted strings.
- Treat every `X-Location-*` header as an optional trusted integer identifier.
- If auth-service emits compact null sentinels such as empty string or `0`, normalize them once near ingress into the repository-owned projection shape instead of leaking raw sentinel handling across the codebase.
- If the headers are absent entirely, do not fabricate them in the service. Normalize that absence consistently in the local projection and document the chosen behavior.
- Keep the trusted projection surface compact and do not invent a second user-context shape.
- Consume the dedicated compact headers directly and keep local projection rules service-owned.
- If a service persists user data, keep the latest user projection in the local `users` read model and keep immutable request-time snapshots only when the domain needs historical or audit context.
- Do not rebuild authorization from raw client headers.

## Permission bitmap and downstream role contract

- `alaa-permission-catalog` is the normative owner for permission names, service ownership, and bitmap ids.
- Auth remains the only runtime issuer of JWT authorization claims: `prm`, `prv`, and `av`.
- `X-Access` carries the gateway-injected copy of auth-service's verified `prm` permission bitmap claim.
- `X-Access` may carry a compact permission bitmap rather than human-readable scopes.
- The bitmap must be unpadded base64url-encoded raw bytes.
- Permission `bitmap_id` values are 1-based.
- Auth `bit_index` values are zero-based and equal `bitmap_id - 1`.
- Bits are packed least-significant-bit first inside each byte.
- Permission meaning comes from the downstream service's generated, committed permission map, not from hard-coded bit labels at the gateway.
- Downstream `config/permissions.php` maps or generated Go permission maps must be generated from
  `alaa-permission-catalog` and committed per service; do not hand-maintain local bitmap ids.
- Auth-service derives `perm_bm` from catalog-owned `bit_index`, not from mutable local package table IDs.
- Auth-service compilation precedence is `direct deny > direct allow > role grants`.
- If a downstream service, gateway extension, or debugging tool inspects raw JWT claims instead of injected headers, treat `prv` and `av` as the companion invalidation metadata for `prm`.
- Required decode flow:
  - reject empty or non-base64url values
  - base64url-decode with strict alphabet checking
  - enumerate set bits up to the maximum configured permission id
  - map known ids to permission names from config
  - ignore unknown ids
  - treat the header as invalid if no known permissions remain after mapping
- Comment-service currently uses these permission ids:
  - `18` -> `comment_get_index`
  - `19` -> `comment_approve`
  - `20` -> `comment_delete`
  - `21` -> `comment_reply`
  - `40` -> `comment_get_show`
- Services must define and document their own role or authorization derivation from decoded permissions.
- Ticket-service currently maps these ids from `X-Access`:
  - `14` -> `crm_get_tickets`
  - `15` -> `crm_post_ticket_reply`
  - `16` -> `crm_put_ticket`
  - `17` -> `crm_post_bulk_ticket`
- Current canonical catalog outcomes:
  - `wa_get_watch_stats` owns bitmap id `1`; WA service-local config adoption is deferred until WA has a committed permission-consumer shape.
  - `comment_get_index` owns bitmap id `18`.
  - `comment_get_show` owns bitmap id `40`.
  - extracted `content_*` permissions own bitmap ids `64-78`.
  - ControlledOps `content_bulk_*` permissions own bitmap ids `79-91`.
  - tusd upload-intake permissions own bitmap ids `92-95`.
  - legacy VOD ids remain stable and must not be reused across the extracted content service boundary.
- VOD keeps legacy service-local permission ids stable; extracted content-service permissions use new catalog-owned ids and are not runtime aliases for VOD permissions.
- Laravel compatibility pattern: decode the bitmap once in auth middleware, map ids to permission names from service-local config, attach the mapped names to the request-scoped user object, and let `isAbleTo` or policy checks read those normalized permission names.
- Do not authenticate the actor successfully and then silently continue with an empty decoded permission set on routes that expect permission-bearing context. Fail during trusted-context normalization with canonical code `AUTH_ACCESS_BITMAP_INVALID` so the outward response and deny logs stay specific and consistent.
- Comment-service currently derives roles like this:
  - admin when all configured permissions are present
  - moderator when any moderation signal permission is present
  - student otherwise
- Recompute example bitmaps from the generated service config whenever permission ids change; do not preserve stale examples by hand.
- Reusable reference implementation: `./permission-bitmap.php`
- Do not assume another service uses the same permission ids or role derivation unless that service explicitly adopts that exact mapping.
- The bitmap width is produced by the auth service against the full global permission set, so downstream services should expect a common bitmap width even when each service only cares about a subset of ids.
- Ticket-service shows a common legacy failure mode: decode `X-Access`, map known ids from config, and if nothing valid remains, let the request continue until a later generic `unauthorized` or `access_denied` path fires.
- Target standard: do not defer malformed or unknown-only bitmap failures to later generic auth checks. Fail during trusted-context normalization with canonical code `AUTH_ACCESS_BITMAP_INVALID` so the outward response and deny logs stay specific and consistent.

## Logging and observability

- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
- Preserve inbound `traceparent`, `tracestate`, and `baggage` across HTTP boundaries. On async boundaries, forward `traceparent` and `tracestate`, and only forward baggage keys that were explicitly reviewed as safe.
- If a service maps an internal policy decision to a route-specific outward deny code, the API response `code` and the emitted deny log `code` must stay identical.
- When auth context is missing or malformed, make the denial observable.
