# Frontend failure and degradation

You are about to decide what a user sees when the SSR process throws, the API cannot be reached, the network is gone, or a deploy left a stale bundle in the cache. This file states where those decisions land in a Quasar app. The doctrine behind them — deadline values, retry counts, backoff shape, breaker thresholds, idempotency, degradation levels — is `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/10-deadlines-and-timeouts.md`, `references/20-retries.md`, `references/50-degradation.md`, `references/60-idempotency.md`. Take every number from there; this file decides only which Quasar surface enforces it.

Also load `references/30-service-worker-excellence.md` (cache behaviour), `references/31-ssr-pwa-and-security.md` (SSR wiring), `references/36-client-observability-contract.md` (what the failure emits), and `references/37-pwa-operations-record.md` (what ships with the release).

## 1. SSR render failure

An `@quasar/app-vite` v3 SSR app answers from `dist/ssr/index.js`. The render middleware is last in `ssr.middlewares` and it is the only place a render throw can be classified. Classify every throw into exactly one of four classes and answer differently for each.

| Class | Detection | Answer |
| --- | --- | --- |
| Route not found | the thrown value has `routeNotFound` | `404` with the app's not-found body |
| Redirect | the thrown value has `redirectUrl` and `redirectHttpStatusCode` | `c.redirect(...)` with that status |
| Upstream unreachable before the gateway (DNS, connection refused, connection failed, connect timeout, TLS) | the error carries the SDK's own upstream brand — never a bare `ECONNREFUSED` string match, which also fires on an inbound client disconnect | transient classes: `503` plus `Retry-After`; TLS or unknown-configuration classes: `502` with no `Retry-After`, because a retry cannot fix a misconfiguration |
| Anything else | fell through the three above | `500` |

Rules, all unconditional:

- **The production response body carries a stable error code and a request id, and nothing else.** No stack, no upstream hostname, no native cause string, no request payload, no header values. `serve.devError()` exists on dev only; guard every use of it with `import.meta.env.QUASAR_DEV`.
- **Do not answer a failed server render by serving the client shell.** A silent SPA fallback returns `200`, so the failure disappears from status-code monitoring and the user gets a page whose data never arrives. If a route is genuinely safe to render in the browser, mark it client-rendered in the router so it never renders on the server, rather than falling back at runtime.
- **Every SSR failure class emits one structured log line and one metric increment, and the emission is fail-open** — a broken emitter never turns a `503` into an unhandled crash. Names come from `/alaa-services-contract` (`$alaa-services-contract`); see `references/36-client-observability-contract.md` §4 for the server half of the seam.
- **`Retry-After` is only sent for a class where a retry can succeed.** Sending it on a configuration error trains clients and proxies to hammer a broken deployment.
- The SSR process is a long-lived server: an unhandled rejection in a boot file or a middleware can take it down for every user. Boot files that call the network at module scope are a per-request failure surface — see `references/22-cli-cookbook-and-examples.md` for the request-scoped factory shape.

## 2. API unreachable, from the browser

- **Every browser request carries a finite deadline.** Attach `AbortSignal.timeout(ms)` (or the SDK's deadline option) to every `fetch` and to every SDK call; a request with no deadline is a permanent spinner. The value is `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/10-deadlines-and-timeouts.md`.
- **Retry only requests that are safe to repeat.** A `GET` may be retried under the backoff policy of `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/20-retries.md`. A `POST`, `PUT`, `PATCH`, or `DELETE` is retried only when it carries an idempotency key the server honours; without a key it is not retried, it is surfaced to the user with an explicit retry control.
- **Every asynchronous surface renders three states and no fourth.** In flight — a `QSkeleton`, `QInnerLoading`, or `QLinearProgress` bound to the same request; failed and retryable — an inline message with a retry control that reissues exactly that request; failed and terminal — a message that names what the user can do instead. A spinner with no timeout and no error branch is an incomplete implementation, not a loading state.
- **A failed background refresh never destroys displayed data.** When a revalidation fails while stale data is on screen, keep the stale data, mark it stale in the UI, and offer a manual refresh. Replacing content with an error page loses the user's place.
- **Never use `Notify` alone for a failure the user must act on.** A toast dismisses itself; if the user must retry, the retry control lives in the surface that failed.

## 3. Offline and degradation matrix

Every PWA release ships a route-by-route matrix. It is a required artifact, recorded per `references/37-pwa-operations-record.md`, with exactly one of three values per route:

| Value | Meaning | What must exist |
| --- | --- | --- |
| Works offline | the route renders and is usable with no network | precached shell entry, and any data it reads lives in IndexedDB |
| Degrades | the route renders with reduced content, clearly labelled | a rendered offline state, not an empty page |
| Hard fails | the route cannot function offline | the offline fallback navigation from `setCatchHandler`, naming the route and what the user should do |

Rules:

- **A route is offline-capable only if a check proves it**, run as the offline assertion in `references/75-testing-ci-playbook.md`. A route claimed offline-capable in the matrix but not covered by that check is recorded as unverified.
- **Structured offline data is not a service-worker concern.** Cache Storage holds Request/Response pairs only; drafts, progress, outbox rows, and cursors are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/70-cache-and-drafts.md` and `references/71-browser-outbox.md`.
- **Offline media is not precached by the service worker.** Downloaded video and audio live in the offline media store owned by `/alaa-shaka-player` (`$alaa-shaka-player`), `references/50-offline-and-in-app-download.md`, over the storage substrate of `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/72-offline-media-store.md`.
- **`navigator.onLine` is a hint, not a state.** It reports link status, not reachability. Drive offline UI from an actual failed request or from the service worker's `offline()` hook, and use `navigator.onLine === false` only to skip a request you already know will fail.

## 4. Stale bundle and unrecoverable client state

- **A post-deploy white screen with 404s on hashed chunks is a precache or skip-waiting failure, not a build failure.** The mechanism and the reload-once guard are `references/30-service-worker-excellence.md` §4.
- **Every PWA has a tested kill switch**: a same-URL service worker that deletes every cache, unregisters itself, and passes fetches through. Test it before it is needed; an untested kill switch is not a kill switch. Its location and last test date are recorded in `references/37-pwa-operations-record.md`.
- **A client-side recovery path never silently discards user data.** Before clearing caches or storage from the app, either flush the outbox or tell the user exactly what will be lost.

## 5. Symptom, diagnosis, smallest retry, escalation

| Symptom | Likely cause | Smallest retry | Escalate when |
| --- | --- | --- | --- |
| SSR returns `500` for every route, dev is fine | boot file or middleware throwing on the server; browser API read during render | run `node dist/ssr/index.js` locally and read the first stack frame; grep the boot files for `window`, `document`, `localStorage` | the stack points inside `node_modules/@quasar/app-vite` — that is an upstream report, not an app fix |
| SSR returns `503` with `Retry-After` | pre-gateway upstream failure classified by the render middleware | curl the gateway URL from the SSR host | the upstream is healthy from the host but the SSR container still fails — network policy, not app code |
| Page renders on the server, blank after hydration | hydration mismatch, or a client chunk 404 | open the console; a mismatch warning and a 404 are different failures | a mismatch that reproduces only after a deploy — see `references/70-guardrails-a11y-performance-monorepo.md` signature table |
| Spinner never resolves | request with no deadline | add the deadline; confirm the request appears in the network panel | the request never leaves the browser — a Permissions-Policy or mixed-content block, see `references/45-browser-apis-and-permissions.md` |
| App works online, blank offline | offline fallback navigation not registered | verify `setCatchHandler` and the precached shell entry | the shell is precached but navigation still fails — check the navigation strategy in `references/30-service-worker-excellence.md` §1 |
| Users on the old build for days | `sw.js` served with a long HTTP cache lifetime | serve `sw.js` with `Cache-Control: no-cache`, register with `updateViaCache: 'none'` | the CDN overrides the origin header — that is a deploy configuration issue for `/alaa-frontend-devops` (`$alaa-frontend-devops`) |
| Mutation lost after a reconnect | queued request replayed without an idempotency key, or the token expired before replay | inspect the Background Sync queue in DevTools Background Services | duplicates reached the server — the contract is `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/60-idempotency.md` |

✅ Do — give every request a deadline, classify every SSR throw, and render an explicit failure state. ❌ Don't — return `200` with an empty shell when the server render failed; monitoring then reports the outage as healthy traffic.

Search: `SSR 500`, `dist/ssr/index.js`, `serve.devError`, `Retry-After`, `503`, `502`, `AbortSignal.timeout`, `offline fallback`, `setCatchHandler`, `degradation matrix`, `kill switch`, `navigator.onLine`, `stale chunk 404`.
