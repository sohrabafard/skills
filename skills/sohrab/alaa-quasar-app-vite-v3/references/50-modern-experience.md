# Modern experience: mode choice, install, perceived performance

You are about to choose SPA versus SSR versus PWA versus a native shell for new work, design the install and engagement path, or make first paint feel faster. Depth stays in the routed files; this one decides.

## 1. Mode choice

| Goal | Choice |
|---|---|
| Authenticated tool, no SEO requirement | SPA; add PWA for install and offline |
| Public content, SEO and social previews, fastest first paint | SSR; Hono for a new app unless the repository standardizes another supported server (Express, Fastify, Koa). Load `references/31-ssr-pwa-and-security.md` |
| Install and offline on top of SPA or SSR | PWA; `references/32-pwa-injectmanifest-guard.md`, then `references/30-service-worker-excellence.md` |
| Store presence or deep device APIs | Capacitor for new work over Cordova; Electron for desktop; `references/35-platform-modes.md` |
| Browser extension | BEX; `references/35-platform-modes.md` |

SSR plus PWA is combined only after the takeover conditions in `references/35-platform-modes.md` are met.

## 2. Install and engagement — feature-detect every item

The manifest needs a name, maskable icons, and per-form-factor `description` and `screenshots` for Chromium's Richer Install UI. Safari 26 removed installability requirements — any page can enter the Home Screen or Dock — so design the standalone experience without assuming a prompt exists. On Chromium, capture `beforeinstallprompt` and offer installation only after demonstrated value, never at first paint.

Standard Web Push is universal; iOS requires a Home-Screen install plus a gesture. Support Declarative Web Push payloads (iOS 18.4+, Safari 18.5) so notifications work without service-worker cooperation. **Push never gates a core flow.** Badging, Web Share Target, File Handling, Launch Handler, and Window Controls Overlay are Chromium-only additive extras; their support matrix is `references/30-service-worker-excellence.md` §6.

## 3. Perceived performance

Lazy route components are the baseline; a new convention-routed app may use `build.filenameBasedRouting` on vue-router v5. Chromium Speculation Rules prefetch or prerender likely next documents; they complement and never replace service-worker precache — speculation accelerates online navigation, the service worker guarantees offline and repeat visits. Service-worker-controlled prefetch now traverses the fetch handler.

Use same-document View Transitions for route and shared-element changes. Motion, easing, and reduced-motion behaviour are `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/70-motion-contract.md`; which modern CSS features are safe at which Baseline tier is `references/72-modern-css-baseline-tiers.md` in the same skill, and Quasar's own browser floor does not block them (`references/20-v3-config-and-features.md`). Web Vitals and Lighthouse scoring are `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/41-lighthouse-and-web-vitals.md`; emitting a vitals sample in production is `references/36-client-observability-contract.md`. Render and asset budgets are `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/45-render-and-asset-budgets.md`; the Quasar-side list and bundle budgets are `references/70-guardrails-a11y-performance-monorepo.md`.

## 4. Auth, offline, and gates

OTP autofill and device signals: `references/40-webotp-and-device-trust.md`. Step-up challenges and permission hints: `references/41-step-up-and-permission-hints.md`. Permission-gated recording, camera, geolocation, notification, and sensor primers and recovery: `references/45-browser-apis-and-permissions.md`. Token storage, refresh, and protected routes: `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/21-ssr-auth-and-session-patterns.md`; trust doctrine: `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). After a successful OTP, offer passkey enrollment; passkeys are Baseline across engines and are the modern trusted-device primitive.

Offline boundary: the service worker owns asset and navigation caching (`references/30-service-worker-excellence.md`). IndexedDB owns drafts, progress, outbox rows, and cursors — `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/70-cache-and-drafts.md`, `references/71-browser-outbox.md`, `references/95-alaa-integration-playbook.md`. Downloaded media is `/alaa-shaka-player` (`$alaa-shaka-player`), `references/50-offline-and-in-app-download.md`. Keep the three layers separate and separately testable; the route-by-route matrix is `references/34-frontend-failure-and-degradation.md` §3.

## 5. Before calling it done

Every modern feature here is progressive enhancement over a baseline that works without it. Before finishing: Vue and TypeScript review through `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`); verification through `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/50-qa-and-verification.md`; reduced-motion and accessibility checks for anything that animates; and, after any service-worker change, the five-point install-update-offline verification in `references/32-pwa-injectmanifest-guard.md` §6 plus an updated `references/37-pwa-operations-record.md`.

Search: `mode choice`, `SPA vs SSR`, `beforeinstallprompt`, `Richer Install UI`, `standalone`, `display-mode`, `speculation rules`, `view transitions`, `filenameBasedRouting`, `progressive enhancement`.
