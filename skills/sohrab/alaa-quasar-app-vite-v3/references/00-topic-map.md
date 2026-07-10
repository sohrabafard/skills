# Topic map

Load the smallest answer file, plus its one-hop “Also load” links. Detect installed `@quasar/app-vite` major before any config/env/alias shape.

| Task | Load |
|---|---|
| Exact installed component/directive/plugin props, events, slots, methods, values, options | `05-authority-and-api-lookup.md` + `scripts/query-installed-quasar-api.mjs` |
| v2 -> v3 plan/execute | `10-v2-to-v3-migration.md` + `11-review-and-upgrade-checklist.md` |
| Maintain v2 env/aliases/boot/routing/Pinia | `12-v2-maintenance-playbook.md` |
| Review style; correct/wrong examples | `13-examples-review-style.md` |
| v3 capabilities/env/version truth/Quasar UI 2.18–2.21 | `20-v3-config-and-features.md` |
| `quasar.config`, aliases, `extendViteConf`, env, proxies, lazy loading, upgrades | `21-cli-vite-and-config.md` |
| Exact config/boot/env/alias shapes, either line | `22-cli-cookbook-and-examples.md` |
| SW/offline/cache/update/performance/debug/push/badging/background sync | `30-service-worker-excellence.md` |
| SSR/hydration/`ssrContext`/`preFetch`/auth cookies/SEO/GenerateSW vs InjectManifest | `31-ssr-pwa-and-security.md` |
| Custom SW/InjectManifest boundary changes | `32-pwa-injectmanifest-guard.md` |
| SSR model/request isolation/register-sw/SSR+PWA takeover | `33-ssr-pwa-playbook.md` |
| SPA/SSR/PWA/BEX/Capacitor/Cordova/Electron choice | `35-platform-modes.md` |
| WebOTP/SMS autofill/fingerprinting/device trust/passkeys | `40-webotp-and-device-trust.md` |
| Browser APIs/permissions: audio, camera, geolocation, notifications, clipboard, wake lock, sensors; priming, denial recovery, tests, Capacitor split | `45-browser-apis-and-permissions.md` |
| Mode/install UX/perceived performance/modern experience | `50-modern-experience.md` |
| Component family choice | `60-components-and-layouts.md` |
| Component intent/alternatives/gotchas/search terms | `61-component-usage-atlas.md` |
| Layouts/`view`/drawers/route-owned layouts | `62-layout-patterns-and-examples.md` |
| QImg/placeholders/responsive delivery | `63-image-delivery-and-placeholders.md` |
| Plugins/composables/directives/options/utils | `64-plugins-composables-directives-options-utils.md` + atlases `65`, `66` |
| A11y/performance/monorepo/tree-shaking | `70-guardrails-a11y-performance-monorepo.md` |
| Testing extensions/layers/CI | `75-testing-ci-playbook.md` |
| Versions/v2-v3 split/Vite 8/Router 5/Vue 3.5 | `80-upstream-deltas-and-live-checks.md` |
| Old `quasar-*` skill names | `85-legacy-skill-coverage.md` |
| Skill maintenance | `90-maintenance-and-live-checks.md` + `91-agent-authoring-and-dual-runtime.md` |

## Search routing

- `quasar describe`, exact props/events/slots/methods/options, installed API, App Extension API, source drift -> `05`.
- `#q-app`, `import.meta.env`, `QUASAR_MODE`, `build.env`, `clientPrefix`, `defineEnv`, `vueOptionsAPI`, `filenameBasedRouting`, `Rolldown`, `Hono`, `server-assets` -> `20`, `22`.
- `#q-app/wrappers`, `envFolder`, `rawDefine`, `extendManifestJson`, `redirect`, `quasar prepare`, `compatibleWith`, `defineCapacitorConfig`, legacy aliases -> `10`, `12`, `22`.
- `__WB_MANIFEST`, `InjectManifest`, `NetworkFirst`, `StaleWhileRevalidate`, `ExpirationPlugin`, `BackgroundSyncPlugin`, `skipWaiting`, `controllerchange`, navigation preload, `addRoutes`, `setAppBadge`, declarative web push, `kill-switch` -> `30`, `32`.
- `ssrContext`, `preFetch`, `useMeta`, `useHydration`, hydration mismatch, `QNoSsr` -> `31`, `33`.
- `OTPCredential`, `one-time-code`, `otp-credentials`, `@domain #code`, `FingerprintJS`, `BotD`, device ID, passkey, WebAuthn -> `40`.
- `getUserMedia`, `MediaRecorder`, `isTypeSupported`, `permissions.query`, `Permissions-Policy`, `requestPermission`, geolocation, `watchPosition`, `wakeLock`, clipboard, `DeviceMotionEvent`, `SpeechRecognition`, `getDisplayMedia`, priming/prompt, `<permission>`/`<geolocation>` -> `45`.
- `QTable`, `QImg`, `QDialog`, `QSelect`, `QUploader`, `QLayout`, `view`, drawers -> `61`, `62`, `63`; `Notify`, `Dialog`, `Screen`, `ClosePopup`, `Ripple`, `date`, `dom`, `uid` -> `64`–`66`.
- BEX Bridge/Capacitor/Cordova/Electron preload -> `35`; `beforeinstallprompt`, screenshots, speculation rules, view transitions, mode choice -> `50`.

## Route out; do not duplicate

- Broad frontend (SSR auth/session, data shaping, Web Vitals/perf, QA) and CSS/motion -> `$alaa-frontend-developer`; any Vue/TS clean-code gates -> `$alaa-vue-typescript-clean-code`; IndexedDB/offline data/outbox -> `$alaa-indexeddb-browser-storage`.
- `packages/*` -> `$alaa-mono-package`; CI/Docker/deploy -> `$alaa-frontend-devops`; gateway auth -> `$alaa-trust-gateway-auth`.
