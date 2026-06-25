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
  prefix/service-name defaults, the version matrix, and the public types. Consume those; do not re-derive them.

## Responsibility ownership (who owns what)

The app must not re-implement anything the SDK or gateway already owns. Default ownership:

- **Trusted-header rejection** → SDK. The SDK transport rejects caller-supplied trusted gateway headers fail-closed
  (`@alaa/sdk-auth`'s `rejectForbiddenCallerHeaders` over core's deny-list). The app never re-checks or duplicates this.
- **Token attach + refresh** → SDK. The opaque bearer token is attached by the SDK; refresh is SDK-owned and
  single-flight. The app never re-implements refresh, never queues its own refresh, and never decodes the token.
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
- The access token is opaque to the client. Do not decode it, branch on its claims, or persist it. Never write a bearer
  token into a non-HttpOnly cookie, into SSR HTML, or into serialized SSR store state.
- `project_id` is a public UUIDv7. Send it only in the request **body** where the contract requires it (for example the
  OTP request), sourced from app config/env (such as `PROJECT_ID`). Never send it as a trusted header from the client.

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
- Decoding the access token or branching on its claims in client code.
- Sending any trusted gateway header from the browser, or putting `project_id` in a header.
- Importing a sibling SDK package's `src/*` instead of its public `dist`/entry export.
- Parsing raw error bodies instead of using `isAlaaSdkError` + the SDK error taxonomy.

## Apply checklist

- App SDK imports come only from `@alaa/sdk` and `@alaa/sdk-vue`.
- No app import of `@alaa/sdk-core` or a domain SDK; no app re-implementation of trust/refresh/error ownership.
- Outbound client headers are limited to `Authorization: Bearer`, `X-Request-Id`, `traceparent`.
- No token in cookie/SSR HTML/SSR state; token treated as opaque; `project_id` only in body, from config.
- One SDK/core per SSR request; browser SDK reset on logout/actor change.
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
