# Modern experience playbook (v3)

Scope: current/premium v3 mode, install/engagement, perceived performance, and UI decisions. Depth stays in routed references.

## 1. Mode

| Goal | Choice |
|---|---|
| Authenticated tool; no SEO | SPA; add PWA for install/offline |
| Public content, SEO/social previews, fastest first paint | SSR; Hono for new apps unless repo standardizes another supported server (Express/Fastify/Koa); load `references/31-ssr-pwa-and-security.md` |
| Install/offline atop SPA/SSR | PWA; `references/30-service-worker-excellence.md` |
| Store presence/deep device APIs | Capacitor (new-work preference over Cordova); Electron for desktop; `references/35-platform-modes.md` |

SSR+PWA can combine only after verifying takeover conditions. Use BEX for browser extensions.

## 2. Install/engagement—detect all

Manifest needs name, maskable icons, and per-form-factor `description` + `screenshots` for Chromium Richer Install UI. Safari 26 removed installability requirements: any page can enter Home Screen/Dock, so design standalone without assuming prompts. On Chromium capture `beforeinstallprompt`; offer only after demonstrated value, never first paint.

Standard Web Push is universal; iOS requires Home-Screen install + gesture. Support Declarative Web Push payloads (iOS 18.4+/Safari 18.5) so notifications work without SW cooperation; push never gates core flow. `navigator.setAppBadge` supports installed-app unread counts on Chromium/WebKit. Web Share/Share Target, File Handling, Launch Handler, and Window Controls Overlay are Chromium-only additive extras.

## 3. Perceived performance

Lazy route components are baseline; new convention-routed apps may consider `build.filenameBasedRouting` (vue-router v5). Chromium Speculation Rules prefetch/prerender likely next documents; it complements, never replaces, SW precache: speculation accelerates online navigation; SW guarantees offline/repeat. SW-controlled prefetch now traverses the fetch handler.

Use same-document View Transitions for routes/shared elements; scroll-driven reveals only as Tier 3. Motion/taste: `$alaa-ui-ux-design-system` `references/70-motion-and-modern-css.md`. Quasar 2.19+ targets Baseline widely available—Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+—so supported CSS Tier 1–2 includes container queries, `:has()`, nesting, `oklch`, `@starting-style`, and popover. Web Vitals: `$alaa-frontend-developer` `references/40-performance-and-realtime.md`.

## 4. Auth, offline, and gates

OTP autofill/WebOTP/device trust: `40-webotp-and-device-trust.md`. Permission-gated recording/camera/geolocation/notification/sensor primer/recovery: `45-browser-apis-and-permissions.md`. Token storage/refresh/protected routes: `$alaa-frontend-developer` `references/21-ssr-auth-and-session-patterns.md`; trust: `$alaa-trust-gateway-auth`. After OTP success offer passkey enrollment; passkeys are Baseline across engines and the modern trusted-device primitive.

Offline boundary: SW owns asset/navigation caching (`30-service-worker-excellence.md`). IndexedDB owns drafts, progress, outbox, and cursors; use `$alaa-indexeddb-browser-storage` `references/70-offline-sync-outbox-cache-patterns.md` + `references/95-alaa-integration-playbook.md`. Keep layers separate/testable.

Every modern feature is progressive enhancement over a working baseline. Before done: `$alaa-vue-typescript-clean-code`; `$alaa-frontend-developer` `references/50-qa-and-verification.md`; reduced-motion/a11y checks for motion; and PWA install → update → offline minimum after SW changes.
