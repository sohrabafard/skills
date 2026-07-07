# Modern experience playbook (best-in-class v3 apps)

Scope: the decisions that make a v3 app feel current and premium — mode selection, install/engagement surfaces, perceived performance, and modern UI capabilities. This file routes aggressively; depth lives in the named references.

## 1. Mode selection (SPA / SSR / PWA / native)

| Goal | Choice |
|---|---|
| Authenticated app tool, SEO irrelevant | SPA (+ PWA when offline/install matters) |
| Public content, SEO, social previews, fastest first paint | SSR (webserver: Hono for new apps unless the repo standardizes otherwise; Express/Fastify/Koa supported) — pair with `references/31-ssr-pwa-and-security.md` |
| Installed/offline experience on top of either | + PWA mode (see `30-service-worker-excellence.md`) |
| App-store presence, deep device APIs | Capacitor (preferred over Cordova for new work); Electron for desktop — structure per `references/35-platform-modes.md` |

SSR+PWA combine; verify takeover conditions before enabling. BEX for browser extensions.

## 2. Install and engagement surfaces (feature-detect all)

- Manifest quality first: name, icons (maskable), `description` + `screenshots` per form factor unlock Chromium's Richer Install UI.
- Safari 26 removed installability requirements — any page can be added to Home Screen/Dock; design the standalone display experience even if you never prompt.
- Install prompt (Chromium): capture `beforeinstallprompt`, offer install at a moment of demonstrated value (never on first paint).
- Push: standard Web Push everywhere; iOS needs Home-Screen install + user gesture; support Declarative Web Push payload shape (iOS 18.4+/Safari 18.5) so notifications work even without SW cooperation. Never gate a core flow on push.
- Badging (`navigator.setAppBadge`) for unread counts on installed apps (Chromium + WebKit).
- Web Share / Share Target, File Handling, Launch Handler, Window Controls Overlay: Chromium-only extras — additive only.

## 3. Perceived performance

- Route-level code splitting (lazy route components) is the baseline; consider `build.filenameBasedRouting` (vue-router v5) for new apps that want convention-driven routes.
- Speculation Rules API (Chromium): prefetch/prerender likely next documents. It complements, never replaces, SW precaching — speculation accelerates online navigations; SW caches guarantee offline/repeat visits. SW-controlled prefetches now run through the fetch handler.
- Same-document View Transitions for route changes and shared-element morphs; scroll-driven reveals as Tier-3 enhancement — implementation and motion-taste contract in `$alaa-frontend-developer` `references/25-modern-css-and-motion.md`.
- Quasar 2.19+ raised browser targets to Baseline widely-available (Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+): modern CSS Tier 1–2 (container queries, `:has()`, nesting, `oklch`, `@starting-style`, popover) is safe inside Quasar's own support matrix.
- Web Vitals workflow: `$alaa-frontend-developer` `references/40-performance-and-realtime.md`.

## 4. Auth and identity UX

- SMS OTP autofill + WebOTP + device trust: this skill's `40-webotp-and-device-trust.md`.
- Token storage, silent refresh, protected routes: `$alaa-frontend-developer` `references/21-ssr-auth-and-session-patterns.md`; gateway trust: `$alaa-trust-gateway-auth`.
- Offer passkey enrollment after successful OTP login; passkeys are Baseline across engines and are the modern trusted-device primitive.

## 5. Offline-first data

Service worker owns asset/navigation caching (`30-service-worker-excellence.md`). Structured records — drafts, progress, outbox, sync cursors — are IndexedDB territory: design them with `$alaa-indexeddb-browser-storage` (`references/70-offline-sync-outbox-cache-patterns.md`, `references/95-alaa-integration-playbook.md`). Do not blur this boundary; it is what keeps both layers testable.

## 6. Quality gates

Every "modern" feature above is progressive enhancement over a fully working baseline. Before claiming done: clean-code gates (`$alaa-vue-typescript-clean-code`), QA/verification mapping (`$alaa-frontend-developer` `references/50-qa-and-verification.md`), reduced-motion and a11y checks for any motion, and the SW verification minimum (install → update → offline) when PWA surfaces changed.
