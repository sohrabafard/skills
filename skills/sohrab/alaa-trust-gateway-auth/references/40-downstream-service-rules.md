# What downstream services must do
## Network and trust boundary rules
- A service may trust gateway auth headers only if the request came through the trusted edge and gateway path.
- If a service can be reached directly, it must either block that exposure or strip and reject internal auth headers at its own edge.
- Internal auth headers are hop-by-hop trust artifacts inside your platform, not public API inputs.

## Authentication vs authorization
- Treat the gateway as the authentication and context-propagation layer.
- Treat each downstream service as the authorization layer for business actions.
- A verified token plus injected headers does not mean the user may perform the requested operation.
- Legacy migration rule: do not copy older per-request auth-service callback patterns into new gateway-backed services.
- Ticket-service still contains legacy internal route groups that accept a separate `user-token` header and call auth-service endpoints such as `/api/v2/checkUserAccess` and `/api/v2/authorizeWithPermissionName` on each request.
- Target standard: for services behind the gateway, replace that pattern with gateway-verified Bearer JWT flow, trusted `X-*` header normalization once at ingress, and local authorization inside the service.
- If a legacy `user-token` path must remain temporarily during migration, classify it as a service-specific compatibility path only. Do not document it as the canonical platform auth contract and do not let it weaken gateway-trusted header rules for normal service routes.

## Laravel Gate and policy flow
- Build the request-scoped actor and tenant context before any framework authorization runs.
- In comment-service, `ResolveUserMiddleware` builds a lightweight authenticated user from trusted headers, service classes call `Gate::forUser($user)->authorize(...)`, and policies return domain-specific deny codes.
- In comment-service, `AuthServiceProvider` stores denied Gate ability context and `AuthorizationErrorRenderer` turns policy denials into a stable `403` JSON envelope and audit event.
- Keep raw gateway-header parsing in middleware or a dedicated request-context layer, not in controllers and not scattered across policies.
- In Laravel services with mixed legacy guard access patterns, resolve the trusted actor once and attach it to every guard and resolver the codebase still reads, such as `Auth::user()`, `$request->user()`, `auth('api')->user()`, or a legacy custom guard.
- VOD shows a practical compatibility pattern: after resolving the user from trusted headers, set the default auth user, set each legacy guard that existing code still reads, and set the request user resolver in the same middleware.
- If you migrate only one guard while other legacy guard lookups remain, helpers, policies, and controllers can disagree about whether the request is authenticated.
- Use policy or Gate responses to express business authorization decisions after auth context normalization, not as a substitute for gateway verification.

## Tenant-safe request handling
- Build request-scoped auth context once near the service edge.
- Normalize at least these fields into a trusted request context object:
  - tenant or project id
  - actor or user id
  - token id when useful for audit
  - request id for trace correlation
- Authorization code should read the normalized request context or server-side request attributes only. Do not re-read raw tenant or actor headers inside policies, services, or repositories after normalization.
- Laravel Eloquent safety rule: if you attach trusted `project_id` or similar request-scoped auth context directly to a model instance for compatibility, keep it transient and non-dirty immediately or keep that context off the model entirely.
- Auth-service shows one safe compatibility pattern for non-persistent model context: set the trusted attribute for request-time reads, then call `syncOriginalAttribute('project_id')` so later `save()` calls do not try to persist a gateway-only attribute into the database.
- HTTP requests without `X-PROJECT-ID` must be rejected with `400`; fallback to the default project id is only allowed for console or queue execution, not normal HTTP traffic.
- Scope every tenant-aware read and write by the trusted tenant context.
- Reject protected requests when required trusted context is missing.
- If a client-supplied tenant selector in body, query, route, or non-trusted header conflicts with the trusted tenant context, deny explicitly instead of silently choosing one source.
- If a service accepts an extra tenant-shaped identifier for resource lookup, reporting, or local routing, treat it as an untrusted selector until it is matched against the trusted tenant context.
- If a route or service intentionally supports anonymous traffic, make that policy explicit. In that mode, tenant context can still be mandatory while actor context is optional.
- Even in anonymous or analytics flows, never let request-body identity fields override or replace trusted gateway tenant context.

## Async ingest and accept-then-validate flows
- Some downstream services accept transport with `202 Accepted` and then validate trusted context inside an async pipeline or ingestion worker.
- Plain meaning: `202` means `I received your request and queued or started processing it`. It does not mean `auth and tenant validation already succeeded`.
- This pattern is common in analytics or ingestion services where the HTTP layer accepts a batch quickly and deeper validation happens in transforms, workers, queues, or sinks after the response is sent.
- Example: a request reaches the service, the HTTP source returns `202`, then a later transform notices that trusted `X-PROJECT-ID` is missing or malformed and drops the data. In that case the transport was accepted, but the business result is still a denial or discard.
- If required trusted context is missing after accept, log a canonical internal code such as `AUTH_CONTEXT_MISSING` or `TENANT_CONTEXT_MISMATCH` and drop, quarantine, or dead-letter the data according to service policy.
- Do not invent a second public `401` or `403` contract after a `202` has already been returned. The caller already received the transport response; the later auth result belongs in logs, metrics, audit events, dead-letter reasons, or operator-facing monitoring.
- If the product needs the client to receive immediate auth failure, do not use accept-then-validate for that route. Move auth/context checks before the `202` response or require the gateway to enforce them earlier.

## Header usage rules
- Use `X-PROJECT-ID` as the public tenant boundary input.
- If a legacy service still exposes `X-Tenant-Public-Id`, treat it as the old name for the same public `project_id` boundary and plan to rename it to `X-PROJECT-ID` during refactor.
- When validating the public tenant boundary value carried in `X-PROJECT-ID`, validate it as UUIDv7.
- Example header value: `X-PROJECT-ID: 018f7d8f-8cb0-7a85-9a89-e3f61052f840`
- If a service still needs an internal numeric project key after validation, derive or load it from the trusted public `X-PROJECT-ID` boundary inside the service and keep that numeric key service-local.
- API-document rule: document `X-PROJECT-ID` with a UUIDv7 example, and if a service still mentions `X-Tenant-Public-Id` or `tenant_public_id`, mark that name as legacy and equivalent to the public `project_id` boundary.
- Use `X-USER-ID` as the authenticated actor id.
- Use `X-ACCESS` and `X-USER-SCOPES` as verified token context, but still enforce server-side permission rules.
- Treat `X-REQUEST-ID` only as correlation.
- Keep one canonical spelling for documentation and tests even though HTTP header names are case-insensitive. Current examples in this skill use `X-Project-ID`, `X-User-Id`, `X-User-Mobile`, `X-Access`, and `X-Profile`.
- Treat `X-USER-MOBILE` as supplemental identity or audit context by default.
- Each downstream service must expose one config switch that decides whether `X-USER-MOBILE` is optional or required. The default policy should be optional.
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
- Use `X-PROFILE` / `X-Profile` only for trusted profile context copied from the verified JWT `profile` claim.
- Required decode flow for `X-PROFILE` when the header is present:
  - reject blank or non-base64url values
  - base64url-decode with strict alphabet checking
  - JSON-decode the UTF-8 payload
  - require a JSON object
  - normalize `first_name` and `last_name` as nullable trimmed strings
  - validate `shahr` as either missing or an object with fixed `id` and `name` keys: missing key => `null`, explicit `null` => `null`, `name` trimmed empty => `AUTH_PROFILE_HEADER_INVALID`, `name` non-empty string => keep, `id` integer or `null` => keep
  - treat malformed payloads, non-object payloads, or any other invalid non-null `shahr` shape as canonical code `AUTH_PROFILE_HEADER_INVALID`
- If `X-PROFILE` is absent, downstream services must interpret that as all canonical profile fields being `null` unless a route explicitly forces trusted profile presence.
- Storage rule for services that persist profile data:
  - keep the latest user projection in the local `users` read model
  - keep immutable request-time snapshots only when the domain needs historical or audit context
- Do not rebuild authorization from raw client headers.

## Permission bitmap and downstream role contract
- `X-ACCESS` carries the gateway-injected copy of auth-service's `perm_bm` permission bitmap.
- `X-ACCESS` may carry a compact permission bitmap rather than human-readable scopes.
- The bitmap must be base64url-encoded raw bytes. Permission IDs are 1-based and use least-significant-bit-first packing inside each byte.
- Permission meaning comes from the downstream service's permission map, not from hard-coded bit labels at the gateway.
- Auth-service is the current producer of the bitmap claim and emits these companion JWT claims together:
  - `perm_bm`
  - `perm_catalog_version`
  - `authz_version`
- Auth-service derives `perm_bm` from `permission_catalog.bit_index`, not from mutable local package table IDs.
- Auth-service compilation precedence is `direct deny > direct allow > role grants`.
- If a downstream service, gateway extension, or debugging tool inspects raw JWT claims instead of injected headers, treat `perm_catalog_version` and `authz_version` as the companion invalidation metadata for `perm_bm`.
- Current gateway behavior documented in this skill injects `perm_bm` as `X-ACCESS`, but it does not yet document companion header injection for `perm_catalog_version` or `authz_version`.
- Required decode flow:
  - reject empty or non-base64url values
  - base64url-decode with strict alphabet checking
  - enumerate set bits up to the maximum configured permission id
  - map known ids to permission names from config
  - ignore unknown ids
  - treat the header as invalid if no known permissions remain after mapping
- Comment-service currently uses these permission ids:
  - `18` -> `comment_get`
  - `19` -> `comment_approve`
  - `20` -> `comment_delete`
  - `21` -> `comment_reply`
  - `22` -> `comment_get_show`
- Services must define and document their own role or authorization derivation from decoded permissions.
- Ticket-service confirms the same bitmap contract and currently maps these ids from `X-ACCESS`:
  - `14` -> `crm_get_tickets`
  - `15` -> `crm_post_ticket_reply`
  - `16` -> `crm_put_ticket`
  - `17` -> `crm_post_bulk_ticket`
- VOD confirms the same bitmap contract and keeps its service-local permission-id map in `config/permissions.php`; its current mapped set covers ids `1-13` and `22-39`.
- Laravel compatibility pattern: decode the bitmap once in auth middleware, map ids to permission names from service-local config, attach the mapped names to the request-scoped user object, and let `isAbleTo` or policy checks read those normalized permission names.
- Do not authenticate the actor successfully and then silently continue with an empty decoded permission set on routes that expect permission-bearing context. Fail during trusted-context normalization with the canonical auth code instead.
- Comment-service currently derives roles like this:
  - admin when all configured permissions are present
  - moderator when any moderation signal permission is present
  - student otherwise
- Current example bitmaps from comment-service docs are:
  - `AAAC` for minimal student access
  - `AAAW` for moderator access
  - `AAAe` for admin access
- Reusable reference implementation: `./permission-bitmap.php`
- Do not assume another service uses the same permission ids or role derivation unless that service explicitly adopts that exact mapping.
- The bitmap width is produced by the auth service against the full global permission set, so downstream services should expect a common bitmap width even when each service only cares about a subset of ids.
- Ticket-service shows a common legacy failure mode: decode `X-ACCESS`, map known ids from config, and if nothing valid remains, let the request continue until a later generic `unauthorized` or `access_denied` path fires.
- Target standard: do not defer malformed or unknown-only bitmap failures to later generic auth checks. Fail during trusted-context normalization with canonical code `AUTH_ACCESS_BITMAP_INVALID` so the outward response and deny logs stay specific and consistent.

## Logging and observability
- Log denies and mismatches with request id and safe auth context.
- Never log the raw token.
- Prefer logging `jti`, tenant id, user id, denial reason, and trace or request id.
- Preserve inbound `traceparent`, `tracestate`, and `baggage` across HTTP boundaries. On async boundaries, forward `traceparent` and `tracestate`, and only forward baggage keys that were explicitly reviewed as safe.
- If a service maps an internal policy decision to a route-specific outward deny code, the API response `code` and the emitted deny log `code` must stay identical.
- When auth context is missing or malformed, make the denial observable.
