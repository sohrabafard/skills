# Frontend SDK Consumption Contract

Use this file when frontend or host-app code consumes the `@alaa/*` SDK packages: choosing which package to import,
deciding what the app is responsible for versus what the SDK owns, wiring auth/token/refresh, attaching correlation
headers, or reviewing a change that touches the browser-to-gateway boundary from the client side.

This file is the client-side companion to `25-end-to-end-flow-and-boundaries.md` (platform flow and gateway
orientation). That file says what the public client is allowed to do against the gateway; this file says how the
frontend SDK layer is allowed to deliver it. Read both when the task spans client and gateway.

It exists because the most common frontend mistake is not a wrong API call — it is the app reaching past the SDK's
public surface to re-own a concern the SDK already owns (trust headers, refresh, errors). That duplicates logic and
leaks layering. The rules below keep responsibility where it belongs.

## SDK package topology (one mental model)

The `@alaa/*` SDK is layered, and each layer has one job:

- `@alaa/sdk-core` — framework-free infrastructure: HTTP transport, cache, the trusted-header deny-list, branded
  errors, and the event primitives. It is composed *by* the SDK packages; it is not an app-facing package.
- domain SDKs (`@alaa/sdk-auth`, `@alaa/sdk-content`, `@alaa/sdk-comment`, `@alaa/sdk-tusd`, `@alaa/sdk-wa`) — one
  service domain each, built on core. They own service routes, request shaping, and service-local security rules.
- `@alaa/sdk` — the aggregate / mother package. The composition root that assembles core plus the domain SDKs into one
  instance with one shared core, one cache, one event bus, and one lifecycle. This is the app's factory entry.
- `@alaa/sdk-vue` — the Vue adapter. Composables (`useAlaaSdk`) and Vue-shaped glue over the aggregate. This is the
  app's entry inside Vue components/composables.

## The single consumption rule

- Frontend/host code imports the SDK **only** through `@alaa/sdk` (factory + types) and `@alaa/sdk-vue` (Vue
  composables). Nothing else.
- Do **not** import `@alaa/sdk-core` or a domain SDK (`@alaa/sdk-auth`, etc.) directly from app/host code. Core is
  infrastructure the aggregate composes; importing it from the app skips the curated public surface and couples the app
  to an internal package (a dependency-inversion violation).
- If the app needs something that only lives on core or a domain SDK, the fix is to **expose it on the `@alaa/sdk`
  aggregate's public exports**, then import it from `@alaa/sdk` — not to reach into core from the app. Treat widening
  the aggregate surface as the sanctioned path, and pair it with `$alaa-mono-package`.
- The aggregate's public surface today includes `createAlaaSdk`, `createAlaaSdkFromCore`, `isAlaaSdkError`, the gateway
  prefix/service-name defaults, the version matrix, the UI capability surface (`PERMISSIONS`,
  `decodeUnverifiedUiAuthorization`, and the `PermissionKey` / `UnverifiedUiAuthorization` types), and the public types.
  Consume those; do not re-derive them.

## Responsibility ownership (who owns what)

The app must not re-implement anything the SDK or gateway already owns. Default ownership:

- **Trusted-header rejection** → SDK, at two layers, fail-closed. The domain SDK rejects caller-supplied forbidden
  headers when it builds the request (`@alaa/sdk-auth`'s `rejectForbiddenCallerHeaders`), and `@alaa/sdk-core`'s
  transport re-asserts the deny-list on the *final* outbound headers right before the fetch
  (`assertNoTrustedCallerHeaders`, which permits only the SDK's own `Authorization`). The app never re-checks or
  duplicates either layer. The one thing the SDK cannot police is code that runs *inside* a host-injected custom fetch
  after that final assert (the documented "custom-fetch bypass"); the gateway is the authoritative enforcement there, so
  a host-injected fetch must only ever add public-safe correlation headers (`X-Request-Id` / `traceparent`).
- **Token attach + refresh** → SDK. The bearer token is attached by the SDK; refresh is SDK-owned and
  single-flight. The app never re-implements refresh, never queues its own refresh, and never decodes the token itself —
  the one sanctioned read is the SDK's own `decodeUnverifiedUiAuthorization` (see *UI capability hints* below).
- **UI capability hints** → SDK computes, app stores. The SDK owns the unverified decode; the app owns recomputing the
  snapshot on every token-lifecycle path and exposing typed helpers. Neither owns authorization — the gateway does.
- **Branded errors + events** → SDK. The app classifies failures with `isAlaaSdkError` and subscribes to the SDK event
  bus; it does not parse raw responses or invent its own error taxonomy from response bodies.
- **Route/prefix composition** → SDK + config seams (see `25-end-to-end-flow-and-boundaries.md`). The app supplies
  gateway base URLs / public config; it does not rewrite child route paths to satisfy gateway routing.
- **Data shaping + UI policy** → app. Redirects, profile-completion gates, which surface renders, and host wiring are
  the app's job — not the SDK's.

## Trust boundary (client side)

- From the browser the app sends only: `Authorization: Bearer <opaque-token>`, `X-Request-Id`, and `traceparent`.
- The app never sends trusted internal gateway headers — `X-Project-Id`, `X-User-Id`, `X-Access`, `X-Profile`,
  `X-User-*`, `X-Location-*`, `X-Gateway-Auth`, `x-access-token-id`, `x-user-scopes`, and the `x-token-*` / `x-authz-*`
  families. Those belong to the gateway-to-service contract, not the public client.
- The access token is opaque to the client for every security purpose. Do not hand-roll a decoder, do not branch on its
  claims for anything that must be correct, and do not persist it. Never write a bearer token into a non-HttpOnly
  cookie, into SSR HTML, or into serialized SSR store state.
- **One bounded exception — UI capability hints.** The SDK may expose a deliberately named unverified decoder (today
  `decodeUnverifiedUiAuthorization` from `@alaa/sdk`) that reads **only** `prm`, `prv`, and `av` to shape the interface:
  hide a control, skip a request the caller would be denied. Rules:
  - It never verifies the signature and is never an authorization decision. The gateway and the owning service stay
    authoritative; a deny response is the only authoritative answer.
  - It fails closed, never throws, returns no raw token and no raw claims, logs nothing, and persists nothing.
  - Compare against generated `PERMISSIONS.*` values — never raw permission strings, never bitmap ids.
  - An empty permission set is a legitimate ready state. Never treat it as a broken session and never log the user out
    because a bitmap failed to decode.
  - Every other claim, including `rol` and `pid`, stays unparsed.
  - Reading `prm` from your own token is not the same as sending `X-Access`. The header deny-list above is unchanged.
- `project_id` is a public UUIDv7 sourced from app config/env (such as `PROJECT_ID`). On a call the app makes with no
  access token it travels in the request **body**, or as a **query parameter** when that request has no body to put it
  in — a GET or a HEAD. This is the general rule, not an OTP exception: where the endpoint's contract needs a project
  and there is no token, those two channels are the only ones there are. The pre-auth OTP request and verify calls are
  the body instance the app already ships; the query form serializes through the SDK's existing query input and adds no
  transport. Send it on exactly one channel per request, chosen by whether the request has a body, and never on both.
- The query parameter rides the SDK's own HTTP call, not the page address. No route, link, or browser URL in the app
  gains a `project_id`, and none is added to make a call match one.
- Never send `project_id` as a trusted header, with a token or without one. `x-project-id` is in the SDK's forbidden
  trusted-header set, and building request headers that contain it raises instead of sending. When the app does hold a
  token, the gateway supplies the project id downstream from the verified claim and the app adds nothing; a
  client-asserted `project_id` on such a request is not read downstream, so do not add one to make a call succeed. What
  the receiving service does with either channel is owned by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) in
  `alaa-trust-gateway-auth references/10-verification-and-ingress.md`.

## UI capability hints in app code

The rules above say what the hints *are*. This is how the app consumes them.

**Shape.** `decodeUnverifiedUiAuthorization(token)` returns a frozen
`{ state, permissions, catalogVersion?, authorizationVersion? }`. `state` is `unavailable` (no token: SSR first render,
anonymous, logged out), `invalid` (a token was present but unreadable), or `ready` (claims were read; `permissions` may
legitimately be empty).

**One recompute point.** The app calls the decoder in exactly one place — wherever it sets the access token (in the
current host, the auth store's `setAccessToken`). Every lifecycle path funnels through that setter, so login, refresh,
cross-tab storage sync, hydrate-from-storage, and logout all stay in step with no extra wiring. Never recompute in a
component, a route guard, or a watcher; never cache a second copy.

**Typed helpers, not raw arrays.** The store exposes `hasPermission(p)`, `hasAnyPermission([...])`, and
`hasAllPermissions([...])`, each taking generated `PERMISSIONS.*` values. All three return `false` unless `state` is
`ready`, so a missing or unreadable token degrades to "show nothing extra". Components call the helpers; they do not
read `permissions` directly, do not import the decoder, and do not import `@alaa/sdk-auth` or any package `src/*` —
the app's import is `@alaa/sdk`.

**Keep it out of the user model.** Capabilities are session state derived from the token, not user identity. Do not add
a `permissions` field to the `User` model, do not persist the snapshot separately from the token, and do not send it
anywhere.

**Staleness is the common bug.** The token is an issuance-time snapshot, so a permission granted on the backend does
**not** appear in the UI until the next login, token refresh, or reissuance. When an agent is asked "the user has the
permission but the button is still hidden", the answer is almost always a stale token, not a decoder bug — check
`catalogVersion` (`prv`) and `authorizationVersion` (`av`) as diagnostics, and confirm against a real backend call.
Treat `prv`/`av` as diagnostics only: do not branch on them and do not use them as cache keys.

**What the states mean for UI.** `ready` → render by capability. `unavailable` → render the anonymous/loading surface,
never an error. `invalid` → render exactly as `unavailable`; it is a corrupt stored value, not a security event, and it
must not sign the user out or block a retry. Under SSR the first render is always `unavailable`, so permission-dependent
markup must not differ between server and client render in a way that breaks hydration — gate on the client, or render
the same neutral surface both times.

**Hints reduce dead ends; they never protect anything.** Keep full error handling on every call you might skip: a
request can still return 403 when the hint said otherwise, and that deny is the authoritative answer. Never use hints
as the sole basis for a route guard, and never rely on a hidden control as a security measure — anyone can edit the
stored token, and the decoder does not verify it.

## SSR and lifecycle rules

- On the server, create one SDK/core per request. Do not hold a module-level SDK singleton that carries per-user state
  across requests.
- In the browser, one SDK/core per app session is fine, but recreate it (or clear scoped cache) on logout or actor
  change, so one user's cached data cannot serve another.
- Refresh relies on the HttpOnly refresh cookie (`credentials: 'include'` on refresh/logout/session calls). The app
  never reads that cookie.

## Observability and correlation (align with the platform directive)

- The app attaches `X-Request-Id` and a synthesized W3C `traceparent` (`00-<32hex>-<16hex>-01`) — one trace id per SSR
  request and per browser navigation — purely as request headers. See `20-operational-and-observability-contract.md`
  for the exact header rules and `21-alaa-platform-observability-directive.md` for the telemetry architecture.
- Client auth/event telemetry is allow-list only: emit low-cardinality fields (event, step, surface, code, request_id,
  trace_id) and never PII, OTP codes, tokens, profile values, or TOTP secrets. Pair with `$alaa-observability-soc` for
  the redaction contract and `$alaa-signoz-clickhouse-docs` for how those fields are queried downstream.

## Documentation requirement

- Every exported function, composable, factory, and public type the app adds around the SDK carries doc comments
  (TSDoc for `.ts`, JSDoc otherwise) with typed params/returns. No undocumented public surface. Pair with
  `$alaa-frontend-doc-annotations`.

## Anti-patterns (do not do these)

- **Reaching into core to re-own an SDK concern.** Importing `@alaa/sdk-core` (or a domain SDK) into the app to add a
  redundant guard — for example re-checking the forbidden trusted-header deny-list in the app's own `fetch` wrapper.
  The SDK transport already rejects forbidden caller headers fail-closed, and the app wrapper only ever *adds*
  `X-Request-Id` / `traceparent`, so the second check guards a hypothetical while leaking the layering. Correct: trust
  the SDK boundary; if you genuinely need the helper, expose it on `@alaa/sdk` first.
- Re-implementing token refresh, a refresh queue, or token persistence in the app.
- Hand-rolling a token decoder in app code, or branching on token claims for anything that must be correct. The only
  sanctioned read is the SDK's unverified UI-hint decoder, and its output may never gate a security decision.
- Using a UI capability hint as a route guard, as the sole gate on a privileged surface, or as a reason to drop 403
  handling. Hiding a control is not protecting it.
- Recomputing the capability snapshot outside the single token setter, caching a second copy, persisting it separately
  from the token, or hanging it off the `User` model.
- Treating `state: "invalid"` or an empty permission set as a broken session — signing the user out, forcing a refresh
  loop, or showing an error instead of the anonymous surface.
- Sending any trusted gateway header from the browser, or putting `project_id` in a header.
- Importing a sibling SDK package's `src/*` instead of its public `dist`/entry export.
- Parsing raw error bodies instead of using `isAlaaSdkError` + the SDK error taxonomy.

## Apply checklist

- App SDK imports come only from `@alaa/sdk` and `@alaa/sdk-vue`.
- No app import of `@alaa/sdk-core` or a domain SDK; no app re-implementation of trust/refresh/error ownership.
- Outbound client headers are limited to `Authorization: Bearer`, `X-Request-Id`, `traceparent`.
- No token in cookie/SSR HTML/SSR state; token treated as opaque except for the SDK's unverified UI-hint decode, whose
  result never gates a security decision; `project_id` only in the body or a query parameter, never a header, always
  from config, and on one channel per request.
- One SDK/core per SSR request; browser SDK reset on logout/actor change.
- Capability hints recomputed in exactly one place (the token setter); components use the typed helpers with
  `PERMISSIONS.*` values; every hinted call still handles 403.
- Client telemetry is redacted/allow-listed; public surface is documented.

## Companion routing

- `$alaa-trust-gateway-auth` — exact trusted-header, token, and gateway-boundary semantics.
- `$alaa-security-review` — mandatory for any change to tokens, refresh, headers, or the client trust boundary.
- `$alaa-frontend-developer` — the three-layer client architecture (presentation → flow composable → store → SDK) and
  SSR auth/session patterns.
- `$alaa-mono-package` — when a needed helper must be promoted onto the `@alaa/sdk` public surface, or when SDK package
  boundaries/exports change.
- `$alaa-observability-soc` and `$alaa-signoz-clickhouse-docs` — redaction contract and downstream querying.
- `$alaa-frontend-doc-annotations` — documentation pass for the public surface the app adds.

For SDK package internals (not app consumption), read the package's own `packages/<name>/developer_guide.md` and
`packages/developer_guide.md`; do not encode package internals here.
