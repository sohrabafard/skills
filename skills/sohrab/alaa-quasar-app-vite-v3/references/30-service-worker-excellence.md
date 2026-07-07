# Service worker excellence (offline, performance, updates, debugging)

Scope: implementing a full-featured, high-performance, debuggable custom service worker for a Quasar app-vite v3 PWA (Workbox 7.4.x, InjectManifest, `/src-pwa/sw/custom-sw.{js,ts}`). Verified 2026-07-08 against developer.chrome.com/docs/workbox, web.dev, MDN, webkit.org, chromestatus, and npm. For the change-safety invariants (single `__WB_MANIFEST`, safe-vs-risky edits) also load `references/32-pwa-injectmanifest-guard.md`; for app-side SW policy also `$alaa-frontend-developer` `references/30-pwa-sw-and-offline.md`; for structured offline data and outbox design route to `$alaa-indexeddb-browser-storage`.

## 1. Strategy selection per resource class (the core table)

| Resource class | Strategy (`workbox-strategies`) | Plugins |
|---|---|---|
| Navigations/HTML | Precached app shell via `NavigationRoute(createHandlerBoundToURL(...))` for installed-first UX, or `NetworkFirst` + navigation preload for content-fresh UX | offline fallback via `setCatchHandler` |
| Hashed build assets | Precache (`precacheAndRoute(self.__WB_MANIFEST)`) | — |
| Non-hashed CSS/JS, font CSS | `StaleWhileRevalidate` | `BroadcastUpdatePlugin` when the UI should know |
| Images/avatars | `CacheFirst` | `ExpirationPlugin({ maxEntries, maxAgeSeconds, purgeOnQuotaError: true })` + `CacheableResponsePlugin({ statuses: [0, 200] })` |
| API reads (JSON) | `NetworkFirst` with `networkTimeoutSeconds`, or `StaleWhileRevalidate` for tolerant data | `ExpirationPlugin` |
| Mutations (POST/PUT/DELETE) | `NetworkOnly` | `BackgroundSyncPlugin('queue', { maxRetentionTime })` |
| Audio/video | `CacheFirst`, explicitly pre-cached | `RangeRequestsPlugin` + `CacheableResponsePlugin({ statuses: [200] })` — never cache 206 partials |
| Auth/session/token endpoints | `NetworkOnly`, no queue | — (see section 7) |

`workbox-recipes` (`pageCache`, `staticResourceCache`, `imageCache`, `offlineFallback`, `warmStrategyCache`) are the same primitives packaged — fine as starting points.

Precache hygiene: precache only what the shell needs to boot offline. Exclude large media, sourcemaps, and per-route lazy chunks the median user never loads (`globIgnores`, `maximumFileSizeToCacheInBytes`); use `dontCacheBustURLsMatching` for already-hashed Vite assets; call `cleanupOutdatedCaches()`. Every manifest change re-downloads changed entries — keep builds deterministic so no-op deploys don't churn clients.

✅ Do — name every runtime cache (`cacheName`) and pair each with `ExpirationPlugin` + `purgeOnQuotaError: true`.

❌ Don't — `CacheFirst` on navigations (pins stale HTML forever — the classic production outage) or precache "everything in dist" because it was easy.

## 2. Offline mutations and IndexedDB coordination

- `BackgroundSyncPlugin` stores failed requests in IndexedDB and replays on the `sync` event; where Background Sync is unsupported (Firefox and all Safari/iOS), Workbox itself degrades to replay-on-SW-start — the pattern is cross-browser-safe, just less timely. Add a manual "retry now" path: message the SW to call `queue.replayRequests()`.
- Replayed requests need server-side idempotency keys; tokens may have expired by replay time; notify clients from `onSync` via `postMessage`.
- Boundary: Cache Storage holds Request/Response pairs only. Structured app data (drafts, entity caches, outbox records, sync cursors) lives in IndexedDB — design it per `$alaa-indexeddb-browser-storage` (`references/70-offline-sync-outbox-cache-patterns.md`); coordinate schema upgrades across SW and window contexts and broadcast changes via `BroadcastChannel`/`postMessage`.

## 3. Performance

- SW cold-boot latency taxes every navigation. Mitigate in order: (1) precached-shell navigations; (2) **navigation preload** for network-going navigation strategies — `workbox-navigation-preload.enable()`, supported Chrome 59+/Firefox 99+/Safari 15.4+; if you enable it, consume `event.preloadResponse` (Workbox's `NetworkFirst` does) or you double-fetch; (3) Static Routing API (Chrome 123+, `event.addRoutes()` in `install`) to bypass the SW entirely for routes that never need it (`/api/analytics`, third-party beacons) — progressive enhancement, non-Chromium support unverified; (4) keep the SW bundle small: no heavy top-level imports, rely on InjectManifest's bundling + tree-shaking.
- Scope `caches.match()` lookups with `cacheName`; huge unscoped caches slow every lookup.
- Opaque responses (no-cors cross-origin) are quota bombs: Chrome accounts ~7MB minimum per opaque entry. Prefer CORS (`crossorigin` attribute) so responses aren't opaque; opt into caching status 0 only deliberately.
- `BroadcastUpdatePlugin` on `StaleWhileRevalidate` routes posts `{ type: 'CACHE_UPDATED' }` to clients when revalidation changed content — show a "fresh content" affordance, don't hard-reload.
- Monitor `navigator.storage.estimate()`; request `navigator.storage.persist()` for data you cannot lose.

## 4. Update lifecycle (the part users feel)

Contract: new SW bytes → `install` (new precache alongside old) → waiting until all old-SW clients close (refresh is NOT enough) → `activate` → controls new clients only unless `clients.claim()`.

Rules:

- **Never unconditional `self.skipWaiting()` at top level** in a code-split SPA: the new SW activates mid-session, purges the old precache, and the running app's lazy chunks 404 — white screen. This is the single most common SW production failure.
- `clientsClaim()` alone is safe and recommended (first-install coverage).
- Prompt-for-update pattern: detect the waiting worker → show a dignified "update available" affordance → on accept, message `{ type: 'SKIP_WAITING' }` → SW calls `self.skipWaiting()` → reload once on take-over with a `refreshing` guard so `controllerchange` can't loop:

```ts
// src-pwa/register-sw (Quasar hooks) or workbox-window equivalent
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

- Quasar's `register-sw` exposes `updated()`/`offline()` style hooks; `workbox-window` (`waiting`/`controlling` events, `messageSkipWaiting()`) is the equivalent library path and also covers the "SW was already waiting before this page loaded" case (`registration.waiting` on load).
- Long-lived SPA sessions: call `registration.update()` on `visibilitychange` or an interval so updates are found without navigation.

Safe deploys:

- Serve `sw.js` with `Cache-Control: no-cache`; the SW URL never changes and is never fingerprinted. If you use `importScripts`, register with `updateViaCache: 'none'`.
- Keep old hashed assets on the CDN for at least one deploy generation so old-SW sessions can still lazy-load.
- Keep a tested **kill-switch SW** ready (same URL, cleans caches, unregisters, passthrough fetch) before you ever need it.

✅ Do — ship prompt-for-update with reload-once; it is the only pattern that is both fresh and safe for code-split apps.

❌ Don't — cache the SW file, auto-skipWaiting "so users always get the latest", or reload on every `controllerchange` without the guard.

## 5. Debugging and testing

- DevTools → Application: Service Workers pane (lifecycle, Update-on-reload, **Bypass for network** — distinct from Network panel's Disable-cache; debugging often needs both), Offline emulation, skipWaiting link, Cache Storage and quota inspectors, Manifest installability warnings. Background services recording (Sync/Push/Periodic/Fetch) records up to 3 days even with DevTools closed.
- `chrome://serviceworker-internals` for zombie registrations; Safari 26+ can inspect SWs via Develop → Inspect Apps and Devices.
- Workbox logs: verbose in dev builds automatically; silence with `self.__WB_DISABLE_DEV_LOGS = true`; production builds strip logs.
- Playwright: SW network interception is still experimental and Chromium-only (`PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS=1`). Test observable behavior instead: load app → `context.setOffline(true)` → assert offline shell renders and mutations queue; use `serviceWorkers: 'block'` to test the no-SW baseline; assert registration state via `page.evaluate(() => navigator.serviceWorker.ready)`.
- Production failure signatures to check first: stale HTML (CacheFirst navigation), white screen after deploy (skipWaiting chunk mismatch), quota exhaustion (opaque padding), update delayed a day (HTTP-cached sw.js), broken media seeking (missing RangeRequestsPlugin), logged-out user seeing cached private data (section 7).

## 6. Browser support and progressive enhancement (2026)

- Core SW + Cache Storage + navigation preload: Baseline widely available (all engines; iOS browsers are all WebKit).
- Installability: Chromium `beforeinstallprompt` + Richer Install UI (manifest `description` + `screenshots`); **Safari 26 removed installability requirements** — any site can be added to Home Screen as a web app, no SW/manifest required; Firefox desktop has no install.
- Push: standard Web Push everywhere including Safari 16.1+/iOS 16.4+, but iOS requires Home-Screen install + user-gesture permission, delivered via APNs, no silent push. **Declarative Web Push** (JSON payload, no SW needed, SW may optionally override) shipped iOS/iPadOS 18.4 + macOS Safari 18.5; Chromium status unverified — design payloads to serve both paths.
- Background Sync: Chromium-only (~76% global). Periodic Background Sync and Background Fetch: Chromium-only, experimental, installed-PWA gated. Badging (`setAppBadge`): Chromium + WebKit, no Firefox. Web Share Target / File Handling / Launch Handler / Window Controls Overlay: Chromium-only, not Baseline.
- Rule: feature-detect every capability (`'sync' in registration`, `'periodicSync' in registration`, `'setAppBadge' in navigator`, `navigator.serviceWorker.controller`); the app must be fully functional with no SW at all (first visit, hostile WebViews, private modes); never gate a core flow on push or background sync.

## 7. Security invariants

- HTTPS only; SW scope = script directory unless `Service-Worker-Allowed` widens it — serve from root, and treat scope as a containment boundary.
- Never cache authenticated/user-scoped API responses in Cache Storage without a logout purge story: Cache Storage is origin-wide, persistent, and locally inspectable. `NetworkOnly` for auth/token/session endpoints; purge user-scoped caches on logout by messaging the SW; never store tokens in Cache Storage or the background-sync queue (queue app-level operations, not credential-bearing raw requests).
- Trusted-header discipline and token handling stay owned by the SDK/gateway layer (`$alaa-trust-gateway-auth`); the SW must not mint, attach, or persist auth context.

## 8. Quasar v3 wiring specifics

- Custom SW lives in `/src-pwa/sw/custom-sw.{js,ts}` (v3 moved it into the `sw/` subfolder); TS config at `/src-pwa/sw/tsconfig.json` extending `../../.quasar/tsconfig.pwa-sw.json`; ESLint glob `src-pwa/sw/**/*.ts`.
- `quasar.config`: `pwa.workboxMode: 'InjectManifest'`, hooks `pwa.extendPWAInjectManifestOptions` / `pwa.extendPWAGenerateSWOptions` (v3 names). Exactly one `self.__WB_MANIFEST` reference must exist in the SW source.
- Registration file: `src-pwa/register-sw` (v3 `sourceFiles` default) — put the update-UX wiring there, and surface the prompt through the app's normal notify/store layer, not `window.confirm`.
- SSR+PWA combos: the SW takeover conditions and register timing follow `references/31-ssr-pwa-and-security.md`.
- GenerateSW remains valid for simple apps with default caching; choose InjectManifest when you need any of sections 1–7 beyond defaults.
