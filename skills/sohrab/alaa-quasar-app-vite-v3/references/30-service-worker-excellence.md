# Service worker excellence (offline, performance, updates, debugging)

Scope: custom high-performance/debuggable Quasar app-vite v3 PWA SW (Workbox 7.4.x, InjectManifest, `/src-pwa/sw/custom-sw.{js,ts}`). Verified 2026-07-08 against developer.chrome.com/docs/workbox, web.dev, MDN, webkit.org, chromestatus, and npm. Also load `references/32-pwa-injectmanifest-guard.md` for single-`__WB_MANIFEST`/change safety; `$alaa-frontend-developer` `references/30-pwa-sw-and-offline.md` for app-side policy; `$alaa-indexeddb-browser-storage` for structured offline data/outboxes.

## 1. Strategy by resource

| Resource | Strategy (`workbox-strategies`) | Plugins |
|---|---|---|
| Navigation/HTML | Precached shell via `NavigationRoute(createHandlerBoundToURL(...))` for installed-first UX; or `NetworkFirst` + navigation preload for freshness | `setCatchHandler` offline fallback |
| Hashed build assets | `precacheAndRoute(self.__WB_MANIFEST)` | — |
| Non-hashed CSS/JS, font CSS | `StaleWhileRevalidate` | `BroadcastUpdatePlugin` when UI notification matters |
| Images/avatars | `CacheFirst` | `ExpirationPlugin({ maxEntries, maxAgeSeconds, purgeOnQuotaError: true })` + `CacheableResponsePlugin({ statuses: [0, 200] })` |
| API reads (JSON) | `NetworkFirst` + `networkTimeoutSeconds`; or `StaleWhileRevalidate` for tolerant data | `ExpirationPlugin` |
| Mutations (POST/PUT/DELETE) | `NetworkOnly` | `BackgroundSyncPlugin('queue', { maxRetentionTime })` |
| Explicitly precached audio/video | `CacheFirst` | `RangeRequestsPlugin` + `CacheableResponsePlugin({ statuses: [200] })`; never cache partial 206s |
| Auth/session/token | `NetworkOnly`; never queue | —; see §7 |

`workbox-recipes` (`pageCache`, `staticResourceCache`, `imageCache`, `offlineFallback`, `warmStrategyCache`) packages these primitives and is a valid start.

Precache only the offline boot shell. Exclude large media, sourcemaps, and rarely used lazy chunks (`globIgnores`, `maximumFileSizeToCacheInBytes`); set `dontCacheBustURLsMatching` for hashed Vite assets; call `cleanupOutdatedCaches()`. Every manifest change redownloads changed entries, so builds must be deterministic to avoid no-op deploy churn. Name every runtime cache (`cacheName`) and pair it with `ExpirationPlugin` + `purgeOnQuotaError: true`. Never use `CacheFirst` for navigation (stale HTML can persist indefinitely) or blindly precache all of `dist`.

## 2. Offline mutations and IndexedDB

`BackgroundSyncPlugin` stores failed requests in IndexedDB and replays on `sync`. Firefox and all Safari/iOS lack Background Sync; Workbox falls back to replay on SW start—safe but slower. Also expose “retry now” by messaging the SW to call `queue.replayRequests()`. Replays require server idempotency keys; tokens may expire before replay; notify clients from `onSync` via `postMessage`. Cache Storage is only for Request/Response pairs. Drafts, entity caches, outbox records, and sync cursors belong in IndexedDB per `$alaa-indexeddb-browser-storage` `references/70-offline-sync-outbox-cache-patterns.md`; coordinate schema upgrades across SW/window contexts and broadcast via `BroadcastChannel`/`postMessage`.

## 3. Performance

SW cold boot taxes every navigation. Mitigate in order: (1) precached-shell navigation; (2) navigation preload for network strategies—`workbox-navigation-preload.enable()`, Chrome 59+/Firefox 99+/Safari 15.4+; consume `event.preloadResponse` (Workbox `NetworkFirst` does) or double-fetch; (3) Static Routing API—Chrome 123+, `event.addRoutes()` during `install`—to bypass SW for routes such as `/api/analytics` and third-party beacons; progressive enhancement, non-Chromium support unverified; (4) keep the SW bundle small: no heavy top-level imports; rely on InjectManifest bundling/tree-shaking. Scope `caches.match()` with `cacheName`; large unscoped caches slow lookups.

Opaque no-CORS responses are quota-heavy (Chrome counts ~7MB minimum each). Prefer CORS/`crossorigin`; cache status 0 only deliberately. `BroadcastUpdatePlugin` on `StaleWhileRevalidate` emits `{ type: 'CACHE_UPDATED' }` after changed revalidation; show freshness UI, never hard-reload. Monitor `navigator.storage.estimate()`; request `navigator.storage.persist()` for irreplaceable data.

## 4. Update lifecycle

Contract: new SW bytes → `install` (new precache beside old) → wait until every old-SW client closes (refresh is insufficient) → `activate` → control new clients only unless `clients.claim()`.

- Never call unconditional top-level `self.skipWaiting()` in a code-split SPA: mid-session activation can purge the old precache, making running-app lazy chunks 404/white-screen. `clientsClaim()` alone is safe/recommended for first-install coverage.
- Safe flow: detect waiting worker → show “update available” → on acceptance send `{ type: 'SKIP_WAITING' }` → SW calls `self.skipWaiting()` → reload once on takeover; guard `controllerchange` against loops:

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

Quasar `register-sw` exposes `updated()`/`offline()`-style hooks. `workbox-window` equivalents are `waiting`/`controlling` and `messageSkipWaiting()`; also check `registration.waiting` on load because a worker may already wait. In long-lived SPAs call `registration.update()` on `visibilitychange` or an interval. Serve unfingerprinted `sw.js` with `Cache-Control: no-cache`; with `importScripts`, register using `updateViaCache: 'none'`. Retain old hashed CDN assets for at least one deploy generation. Pre-test a same-URL kill-switch SW that deletes caches, unregisters, and passes fetches through.

Prompt + reload-once is the safe fresh pattern. Never HTTP-cache SW, auto-skip-waiting, or reload every `controllerchange` without the guard.

## 5. Debugging and tests

DevTools Application: SW lifecycle, Update-on-reload, **Bypass for network** (different from Network “Disable cache”; often use both), Offline, skipWaiting, Cache Storage/quota, Manifest warnings. Background Services (Sync/Push/Periodic/Fetch) records up to 3 days with DevTools closed. Use `chrome://serviceworker-internals` for zombie registrations; Safari 26+ uses Develop → Inspect Apps and Devices. Workbox dev builds log verbosely; `self.__WB_DISABLE_DEV_LOGS = true` silences them; production strips logs.

Playwright SW interception remains experimental/Chromium-only (`PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS=1`). Prefer observable tests: load → `context.setOffline(true)` → assert offline shell and queued mutation; `serviceWorkers: 'block'` for no-SW baseline; inspect readiness with `page.evaluate(() => navigator.serviceWorker.ready)`. Diagnose first: stale HTML=`CacheFirst` navigation; post-deploy white screen=skipWaiting/chunk mismatch; quota exhaustion=opaque padding; day-late update=HTTP-cached `sw.js`; broken seeking=missing `RangeRequestsPlugin`; cross-user private data=§7.

## 6. Support/progressive enhancement (2026)

Core SW, Cache Storage, and navigation preload are Baseline/widely available in all engines; every iOS browser is WebKit. Install: Chromium `beforeinstallprompt`; Richer Install UI needs manifest `description` + `screenshots`. Safari 26 lets any site enter Home Screen as a web app without SW/manifest; Firefox desktop has no install. Web Push: all engines, Safari 16.1+/iOS 16.4+; iOS requires Home-Screen install + gesture permission, uses APNs, and forbids silent push. Declarative Web Push (JSON; no SW required, optional SW override) shipped iOS/iPadOS 18.4 + macOS Safari 18.5; Chromium unverified—support both payload paths.

Background Sync is Chromium-only (~76% global). Periodic Background Sync/Background Fetch are experimental, Chromium-only, installed-PWA-gated. Badging (`setAppBadge`) supports Chromium/WebKit, not Firefox. Web Share Target, File Handling, Launch Handler, and Window Controls Overlay are Chromium-only/not Baseline. Feature-detect everything (`'sync' in registration`, `'periodicSync' in registration`, `'setAppBadge' in navigator`, `navigator.serviceWorker.controller`). Core flows must work without SW (first visit, hostile WebViews, private modes) and never depend on push/background sync.

## 7. Security invariants

HTTPS only. Scope defaults to the script directory unless `Service-Worker-Allowed` widens it; serve from root and treat scope as containment. Cache Storage is origin-wide, persistent, and locally inspectable: never cache authenticated/user-scoped APIs without logout purge; use `NetworkOnly` for auth/token/session; on logout message SW to purge user caches. Never store tokens in Cache Storage or Background Sync—queue app-level operations, not credential-bearing raw requests. SDK/gateway (`$alaa-trust-gateway-auth`) owns trusted headers/tokens; SW never mints, attaches, or persists auth context.

## 8. Quasar v3 wiring

- Custom SW: `/src-pwa/sw/custom-sw.{js,ts}` (v3 moved it under `sw/`); TS config `/src-pwa/sw/tsconfig.json` extends `../../.quasar/tsconfig.pwa-sw.json`; ESLint glob `src-pwa/sw/**/*.ts`.
- `quasar.config`: `pwa.workboxMode: 'InjectManifest'`; hooks `pwa.extendPWAInjectManifestOptions` / `pwa.extendPWAGenerateSWOptions` (v3 names). SW source must contain exactly one `self.__WB_MANIFEST`.
- Registration: `src-pwa/register-sw` (v3 `sourceFiles` default). Put update UX there and surface prompts through normal notify/store, not `window.confirm`.
- SSR+PWA takeover/registration timing: `references/31-ssr-pwa-and-security.md`.
- `GenerateSW` fits default caching; use `InjectManifest` only when §§1–7 require custom behavior.
