# Topic map

Load the smallest file that answers the task. One hop deep; each file names its own "Also load" pairings. Detect the installed `@quasar/app-vite` major before using any config/env/alias shape.

| Task shape | Load |
|---|---|
| Exact component/directive/plugin props, events, slots, methods, values, or options for the installed project | `05-authority-and-api-lookup.md` + run `scripts/query-installed-quasar-api.mjs` |
| Migrate an app from v2 to v3 (plan or execute) | `10-v2-to-v3-migration.md` + `11-review-and-upgrade-checklist.md` |
| Maintain a repo still on v2 (env, aliases, boot, routing, Pinia) | `12-v2-maintenance-playbook.md` |
| Review-answer style, correct/wrong examples | `13-examples-review-style.md` |
| v3 capability map, env contract, version truth, Quasar UI 2.18–2.21 features | `20-v3-config-and-features.md` |
| quasar.config structure, aliases, extendViteConf, env files, proxies, lazy loading, upgrades | `21-cli-vite-and-config.md` |
| Exact config/boot/env/alias code shape for either line | `22-cli-cookbook-and-examples.md` |
| Service worker, offline, caching strategies, update UX, SW performance/debugging, push/badging/background sync | `30-service-worker-excellence.md` |
| SSR, hydration, ssrContext, preFetch, auth cookies, SEO, GenerateSW vs InjectManifest | `31-ssr-pwa-and-security.md` |
| Changing a custom SW / InjectManifest boundaries | `32-pwa-injectmanifest-guard.md` |
| SSR mental model, request isolation, register-sw hooks, SSR+PWA takeover | `33-ssr-pwa-playbook.md` |
| SPA vs SSR vs PWA vs BEX vs Capacitor vs Cordova vs Electron | `35-platform-modes.md` |
| SMS OTP autofill, WebOTP, fingerprinting, device trust, passkeys | `40-webotp-and-device-trust.md` |
| Browser device APIs + permissions: audio recording, camera, geolocation, notifications, clipboard, wake lock, sensors; priming UX, denial recovery, permission testing, Capacitor split | `45-browser-apis-and-permissions.md` |
| Mode selection, install UX, perceived performance, modern experience | `50-modern-experience.md` |
| Which component to use / component families | `60-components-and-layouts.md` |
| Component intent, alternatives, gotchas, and search terms | `61-component-usage-atlas.md` |
| Layout shells, `view`, drawers, routing-with-layouts | `62-layout-patterns-and-examples.md` |
| QImg, placeholders, responsive image delivery | `63-image-delivery-and-placeholders.md` |
| Plugins, composables, directives, options, utils | `64-plugins-composables-directives-options-utils.md` (+ atlases `65`, `66`) |
| A11y, performance audit, monorepo packaging, tree-shaking | `70-guardrails-a11y-performance-monorepo.md` |
| Testing extensions, test layers, CI validation | `75-testing-ci-playbook.md` |
| Latest versions, v2-vs-v3 split table, Vite 8 / Router 5 / Vue 3.5 notes | `80-upstream-deltas-and-live-checks.md` |
| Old `quasar-*` skill names | `85-legacy-skill-coverage.md` |
| Maintaining this skill | `90-maintenance-and-live-checks.md` + `91-agent-authoring-and-dual-runtime.md` |

Search terms → file:

- `quasar describe`, exact props/events/slots/methods/options, installed API, App Extension API, source drift → `05`
- `#q-app`, `import.meta.env`, `QUASAR_MODE`, `build.env`, `clientPrefix`, `defineEnv`, `vueOptionsAPI`, `filenameBasedRouting`, `Rolldown`, `Hono`, `server-assets` → `20`, `22`
- `#q-app/wrappers`, `envFolder`, `rawDefine`, `extendManifestJson`, `redirect`, `quasar prepare`, `compatibleWith`, `defineCapacitorConfig`, legacy aliases → `10`, `12`, `22`
- `__WB_MANIFEST`, `InjectManifest`, `NetworkFirst`, `StaleWhileRevalidate`, `ExpirationPlugin`, `BackgroundSyncPlugin`, `skipWaiting`, `controllerchange`, `navigation preload`, `addRoutes`, `setAppBadge`, `declarative web push`, `kill-switch` → `30`, `32`
- `ssrContext`, `preFetch`, `useMeta`, `useHydration`, `hydration mismatch`, `QNoSsr` → `31`, `33`
- `OTPCredential`, `one-time-code`, `otp-credentials`, `@domain #code`, `FingerprintJS`, `BotD`, `device ID`, `passkey`, `WebAuthn` → `40`
- `getUserMedia`, `MediaRecorder`, `isTypeSupported`, `permissions.query`, `Permissions-Policy`, `requestPermission`, `geolocation`, `watchPosition`, `wakeLock`, `clipboard`, `DeviceMotionEvent`, `SpeechRecognition`, `getDisplayMedia`, priming, permission prompt, `<permission>`/`<geolocation>` element → `45`
- `QTable`, `QImg`, `QDialog`, `QSelect`, `QUploader`, `QLayout`, `view`, drawers → `61`, `62`, `63`
- `Notify`, `Dialog`, `Screen`, `ClosePopup`, `Ripple`, `date`, `dom`, `uid` → `64`–`66`
- `BEX Bridge`, Capacitor, Cordova, Electron preload → `35`
- `beforeinstallprompt`, `screenshots`, `speculation rules`, `view transitions`, mode choice → `50`

Cross-skill ownership (route out, don't duplicate):

- Broad frontend engineering (SSR auth/session, data shaping, perf/Web Vitals, QA) and modern CSS/motion → `$alaa-frontend-developer`
- Clean-code gates for any Vue/TS code produced → `$alaa-vue-typescript-clean-code`
- IndexedDB, offline data, outbox → `$alaa-indexeddb-browser-storage`
- `packages/*` boundaries → `$alaa-mono-package`; CI/Docker/deploy → `$alaa-frontend-devops`; gateway auth → `$alaa-trust-gateway-auth`
