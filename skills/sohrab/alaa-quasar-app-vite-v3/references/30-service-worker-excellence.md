# Service worker excellence (offline, performance, updates, debugging)

Scope: a custom, high-performance, debuggable Quasar app-vite v3 PWA service worker (Workbox 7.4.x, `InjectManifest`, `/src-pwa/sw/custom-sw.{js,ts}`). Verified 2026-07-08 against developer.chrome.com/docs/workbox, web.dev, MDN, webkit.org, chromestatus, and npm; refresh browser claims per `references/80-upstream-deltas-and-live-checks.md` §6.

Also load `references/32-pwa-injectmanifest-guard.md` (single `__WB_MANIFEST`, versioned location, change safety) before opening any file under `src-pwa/`; `references/34-frontend-failure-and-degradation.md` for what the user sees when caching fails; `references/37-pwa-operations-record.md` for what ships with the change. App-side offline policy is `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/30-pwa-sw-and-offline.md`.

## 1. Strategy by resource

| Resource | Strategy (`workbox-strategies`) | Plugins |
|---|---|---|
| Navigation/HTML | Precached shell via `NavigationRoute(createHandlerBoundToURL(...))` for installed-first UX; or `NetworkFirst` + navigation preload for freshness | `setCatchHandler` offline fallback |
| Hashed build assets | `precacheAndRoute(self.__WB_MANIFEST)` | — |
| Non-hashed CSS/JS, font CSS | `StaleWhileRevalidate` | `BroadcastUpdatePlugin` when UI notification matters |
| Images/avatars | `CacheFirst` | `ExpirationPlugin({ maxEntries, maxAgeSeconds, purgeOnQuotaError: true })` + `CacheableResponsePlugin({ statuses: [0, 200] })` |
| API reads (JSON), unauthenticated | `NetworkFirst` + `networkTimeoutSeconds`; or `StaleWhileRevalidate` for tolerant data | `ExpirationPlugin` |
| Mutations (POST/PUT/DELETE) | `NetworkOnly` | `BackgroundSyncPlugin('queue', { maxRetentionTime })` |
| Explicitly precached audio/video | `CacheFirst` | `RangeRequestsPlugin` + `CacheableResponsePlugin({ statuses: [200] })`; never cache partial 206s |
| Auth, session, token, and every credentialed request | `NetworkOnly`; never queued | see §7 |

`workbox-recipes` (`pageCache`, `staticResourceCache`, `imageCache`, `offlineFallback`, `warmStrategyCache`) packages these primitives and is a valid start.

Precache only the offline boot shell. Exclude large media, sourcemaps, and rarely used lazy chunks (`globIgnores`, `maximumFileSizeToCacheInBytes`); set `dontCacheBustURLsMatching` for hashed Vite assets; call `cleanupOutdatedCaches()`. Every manifest change redownloads changed entries, so builds must be deterministic to avoid no-op deploy churn. Name every runtime cache (`cacheName`) and pair it with `ExpirationPlugin` + `purgeOnQuotaError: true`; record every name in `references/37-pwa-operations-record.md`. Never use `CacheFirst` for navigation — stale HTML can persist indefinitely — and never precache all of `dist`.

**Player media is not this file's ground.** Streamed and downloaded video and audio are `/alaa-shaka-player` (`$alaa-shaka-player`), `references/50-offline-and-in-app-download.md`; its offline store is IndexedDB, not Cache Storage. A service-worker route that intercepts segment requests interferes with the player's own networking engine (`/alaa-shaka-player` (`$alaa-shaka-player`), `references/40-networking-engine-and-filters.md`). The only media a service worker caches is a small, explicitly listed set of app-owned audio or video assets.

## 2. Offline mutations and IndexedDB

`BackgroundSyncPlugin` stores failed requests in IndexedDB and replays them on `sync`. Firefox and every Safari/iOS build lack Background Sync; Workbox falls back to replay on service-worker start — safe but slower. Also expose "retry now" by messaging the service worker to call `queue.replayRequests()`. Replays require server idempotency keys; tokens may expire before replay; notify clients from `onSync` via `postMessage`.

Cache Storage holds Request/Response pairs only. Drafts, entity caches, outbox records, and sync cursors belong in IndexedDB.

A service worker that writes IndexedDB opens the database with no version argument and closes on `versionchange` without prompting; the window owns the version integer. Concurrency between a service-worker write and a tab write, the shared `BroadcastChannel` vocabulary, and the Web Locks discipline are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/41-multitab-versionchange-and-locks.md`.

Outbox row states and the browser-side outbox itself are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/71-browser-outbox.md`; caches and drafts are `references/70-cache-and-drafts.md` in the same skill.

## 3. Performance

Service-worker cold boot taxes every navigation. Mitigate in order: (1) precached-shell navigation; (2) navigation preload for network strategies — `workbox-navigation-preload.enable()`, Chrome 59+/Firefox 99+/Safari 15.4+; consume `event.preloadResponse` (Workbox `NetworkFirst` does) or double-fetch; (3) Static Routing API — Chrome 123+, `event.addRoutes()` during `install` — to bypass the service worker for routes such as `/api/analytics` and third-party beacons; progressive enhancement, non-Chromium support unverified; (4) keep the service-worker bundle small: no heavy top-level imports; rely on `InjectManifest` bundling and tree-shaking.

**Cache lookup cost has a budget.** `caches.match()` without a `cacheName` searches every cache in the origin in order, so lookup cost grows with the number of caches and with entries per cache. Scope every lookup with `cacheName`. Cap each runtime cache with `ExpirationPlugin({ maxEntries })` — an unbounded runtime cache is an unbounded lookup. When a cache would exceed a few thousand entries, the access pattern is a key-value store, not a response cache: move it to IndexedDB with an index. Complexity budgets and structure choice are `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`), `references/10-complexity-budget.md` and `references/30-choosing-a-structure.md`.

Opaque no-CORS responses are quota-heavy — Chrome counts roughly 7 MB minimum each. Prefer CORS and `crossorigin`; cache status 0 only deliberately. `BroadcastUpdatePlugin` on `StaleWhileRevalidate` emits `{ type: 'CACHE_UPDATED' }` after a changed revalidation; show freshness UI, never hard-reload. Monitor `navigator.storage.estimate()`; request `navigator.storage.persist()` for irreplaceable data. Quota, eviction, and recovery semantics are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/30-quota-model-and-budgets.md` and `references/32-eviction-and-recovery.md`.

## 4. Update lifecycle

Contract: new service-worker bytes -> `install` (new precache beside old) -> wait until every old-service-worker client closes (refresh is insufficient) -> `activate` -> control new clients only unless `clients.claim()`.

- Never call unconditional top-level `self.skipWaiting()` in a code-split SPA: mid-session activation can purge the old precache, making the running app's lazy chunks 404 and white-screen. `clientsClaim()` alone is safe and recommended for first-install coverage.
- Safe flow: detect the waiting worker -> show "update available" -> on acceptance send `{ type: 'SKIP_WAITING' }` -> the service worker calls `self.skipWaiting()` -> reload once on takeover; guard `controllerchange` against loops:

```ts
// src-pwa/register-sw or workbox-window equivalent
let refreshing = false
navigator.serviceWorker.addEventListener('controllerchange', () => {
  if (refreshing) return
  refreshing = true
  window.location.reload()
})
```

```ts
// src-pwa/sw/custom-sw.ts
self.addEventListener('message', (e) => {
  if (e.data?.type === 'SKIP_WAITING') self.skipWaiting()
})
```

Quasar's `register-sw` exposes `updated()` and `offline()` hooks; the `workbox-window` equivalents are `waiting` and `controlling` plus `messageSkipWaiting()`. Also check `registration.waiting` on load, because a worker may already be waiting. In long-lived SPAs call `registration.update()` on `visibilitychange` or on an interval. Serve an unfingerprinted `sw.js` with `Cache-Control: no-cache`; with `importScripts`, register using `updateViaCache: 'none'`. Retain old hashed CDN assets for at least one deploy generation, and record that retention in `references/37-pwa-operations-record.md`. Pre-test a same-URL kill-switch service worker that deletes caches, unregisters, and passes fetches through.

Prompt plus reload-once is the safe fresh pattern. Never HTTP-cache the service worker, never auto-skip-waiting, and never reload on every `controllerchange` without the guard.

Every transition above is an emitted event; what is emitted and with which names is `references/36-client-observability-contract.md`.

## 5. Debugging and tests

DevTools Application: service-worker lifecycle, Update-on-reload, **Bypass for network** (different from Network "Disable cache"; often use both), Offline, skipWaiting, Cache Storage and quota, Manifest warnings. Background Services (Sync/Push/Periodic/Fetch) records up to 3 days with DevTools closed. Use `chrome://serviceworker-internals` for zombie registrations; Safari 26+ uses Develop -> Inspect Apps and Devices. Workbox dev builds log verbosely; `self.__WB_DISABLE_DEV_LOGS = true` silences them, and production strips logs.

Playwright service-worker interception remains experimental and Chromium-only (`PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS=1`). Prefer observable tests: load -> `context.setOffline(true)` -> assert the offline shell and the queued mutation; `serviceWorkers: 'block'` for a no-service-worker baseline; inspect readiness with `page.evaluate(() => navigator.serviceWorker.ready)`. The regression set that must exist in CI is `references/75-testing-ci-playbook.md`.

Diagnose first: stale HTML means `CacheFirst` navigation; a post-deploy white screen means skipWaiting or a chunk mismatch; quota exhaustion means opaque padding; a day-late update means an HTTP-cached `sw.js`; broken seeking means a missing `RangeRequestsPlugin`; cross-user private data means §7. The wider symptom table is `references/34-frontend-failure-and-degradation.md` §5.

## 6. Support and progressive enhancement (2026)

Core service workers, Cache Storage, and navigation preload are Baseline and widely available in all engines; every iOS browser is WebKit. Install: Chromium `beforeinstallprompt`; Richer Install UI needs manifest `description` plus `screenshots`. Safari 26 lets any site enter the Home Screen as a web app without a service worker or manifest; Firefox desktop has no install. Web Push: all engines, Safari 16.1+/iOS 16.4+; iOS requires Home-Screen install plus a gesture permission, uses APNs, and forbids silent push. Declarative Web Push (JSON; no service worker required, optional service-worker override) shipped in iOS/iPadOS 18.4 and macOS Safari 18.5; Chromium support is unverified, so support both payload paths.

Background Sync is Chromium-only (roughly 76% global). Periodic Background Sync and Background Fetch are experimental, Chromium-only, and installed-PWA-gated. Badging (`setAppBadge`) is supported on Chromium and WebKit, not Firefox. Web Share Target, File Handling, Launch Handler, and Window Controls Overlay are Chromium-only and not Baseline. Feature-detect everything (`'sync' in registration`, `'periodicSync' in registration`, `'setAppBadge' in navigator`, `navigator.serviceWorker.controller`). Core flows must work without a service worker — first visit, hostile WebViews, private modes — and must never depend on push or background sync.

## 7. Security invariants

HTTPS only. Scope defaults to the script directory unless `Service-Worker-Allowed` widens it; serve from the root and treat scope as containment.

**Cache no response whose request carried a credential.** A credential is a cookie, an `Authorization` header, or any trusted header. Route every such request `NetworkOnly`. To cache one, the endpoint is named explicitly in the `pwa` section of `quasar.config` with a written justification and a matching logout-purge entry recorded in `references/37-pwa-operations-record.md`; an endpoint not named there is not cached. Cache Storage is origin-wide, persistent, and locally inspectable, so a cached authenticated response is readable by the next user of the device.

**Never store a token in Cache Storage or in a Background Sync queue.** Queue application-level operations, not credential-bearing raw requests. The SDK and gateway own trusted headers and tokens — `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) — and the service worker never mints, attaches, or persists auth context. Frontend step-up consequences are `references/41-step-up-and-permission-hints.md`.

On logout, message the service worker to delete every cache holding user-scoped data, by name, from the list in the operations record. Threat classes and review triggers are `/alaa-security-review` (`$alaa-security-review`), `references/25-browser-trust-and-output.md`.

## 8. Quasar v3 wiring

- Custom service worker: `/src-pwa/sw/custom-sw.{js,ts}` in v3; TypeScript config `/src-pwa/sw/tsconfig.json` extends `../../.quasar/tsconfig.pwa-sw.json`; ESLint glob `src-pwa/sw/**/*.ts`. The `sourceFiles` default that points at it is stated once, in `references/32-pwa-injectmanifest-guard.md`.
- `quasar.config`: `pwa.workboxMode: 'InjectManifest'`; hooks `pwa.extendPWAInjectManifestOptions` and `pwa.extendPWAGenerateSWOptions` (v3 names). The service-worker source must contain exactly one `self.__WB_MANIFEST`.
- **A `src-pwa/sw/custom-sw.*` file is only built when `pwa.workboxMode` is `'InjectManifest'`.** With `workboxMode: 'GenerateSW'` that file is not shipped and none of its rules are in effect, however correct they look in review.
- Registration lives in `src-pwa/register-sw`. Put the update UX there and surface prompts through the app's normal notify or store layer, never `window.confirm`.
- SSR + PWA takeover and registration timing: `references/31-ssr-pwa-and-security.md`.
- `GenerateSW` fits default caching; choose `InjectManifest` only when §§1-7 require custom behaviour.

Search: `Workbox`, `InjectManifest`, `GenerateSW`, `precacheAndRoute`, `__WB_MANIFEST`, `NetworkFirst`, `StaleWhileRevalidate`, `CacheFirst`, `NetworkOnly`, `ExpirationPlugin`, `BackgroundSyncPlugin`, `RangeRequestsPlugin`, `navigation preload`, `addRoutes`, `skipWaiting`, `clientsClaim`, `controllerchange`, `updateViaCache`, `kill switch`, `setAppBadge`, `declarative web push`, `logout purge`.
