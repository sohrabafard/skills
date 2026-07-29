# Topic map — the skill's only router

This file is the single routing surface of this skill. `SKILL.md` carries one pointer to it and no routing table. The family tables inside `60`, `64`, `35`, and `85` index symbols or legacy names within one topic; they do not route across the skill.

Load the smallest answer file plus the "also load" files its own header names. Before any config, env, alias, or mode shape: detect the installed `@quasar/app-vite` major (`references/80-upstream-deltas-and-live-checks.md` §3).

## 1. Symbol and error-string index — try this first

An exact symbol routes faster than a topic. Search the literal string you are holding.

| You are holding this literal string | Read |
| --- | --- |
| `quasar describe`, `--props`, `--slots`, `dist/api`, `web-types`, App Extension API | `05-authority-and-api-lookup.md` |
| `#q-app/wrappers`, `envFolder`, `rawDefine`, `extendManifestJson`, `quasar prepare`, `compatibleWith`, `defineCapacitorConfig` | `10-v2-to-v3-migration.md`, then `22-cli-cookbook-and-examples.md` |
| `#q-app`, `import.meta.env`, `QUASAR_MODE`, `build.env`, `clientPrefix`, `defineEnv`, `define`, `vueOptionsAPI`, `filenameBasedRouting` | `20-v3-config-and-features.md`, then `22-cli-cookbook-and-examples.md` |
| `extendViteConf`, `vitePlugins`, `build.alias`, `resolve.alias`, `rolldownOptions`, `manualChunks` | `21-cli-vite-and-config.md`, `70-guardrails-a11y-performance-monorepo.md` |
| `__WB_MANIFEST`, `InjectManifest`, `GenerateSW`, `NetworkFirst`, `StaleWhileRevalidate`, `ExpirationPlugin`, `BackgroundSyncPlugin`, `skipWaiting`, `clientsClaim`, `controllerchange`, `addRoutes`, `setAppBadge` | `30-service-worker-excellence.md`, `32-pwa-injectmanifest-guard.md` |
| `dist/ssr/index.js` returning 500, `setCatchHandler`, offline fallback page, "API unreachable" | `34-frontend-failure-and-degradation.md` |
| `sendBeacon`, `fetch(keepalive)`, `onunhandledrejection`, `web-vitals`, sampling rate | `36-client-observability-contract.md` |
| `ssrContext`, `preFetch`, `useMeta`, `useHydration`, `useId`, `data-allow-mismatch`, `QNoSsr`, hydration mismatch | `31-ssr-pwa-and-security.md` |
| `OTPCredential`, `one-time-code`, `otp-credentials`, `@domain #code`, `FingerprintJS`, `BotD`, passkey, WebAuthn | `40-webotp-and-device-trust.md` |
| `X-TOTP-VERIFIED-UNTIL`, `verified_until`, step-up, permission bitmap in the client | `41-step-up-and-permission-hints.md` |
| `getUserMedia`, `MediaRecorder`, `isTypeSupported`, `permissions.query`, `Permissions-Policy`, `requestPermission`, `watchPosition`, `wakeLock`, clipboard, `DeviceMotionEvent`, `getDisplayMedia`, `<geolocation>` | `45-browser-apis-and-permissions.md` |
| `beforeinstallprompt`, speculation rules, view transitions, `display-mode: standalone` | `50-modern-experience.md` |
| `QTable`, `QSelect`, `QUploader`, `QFile`, `QDialog`, `QVirtualScroll`, `QInfiniteScroll`, `QImg`, `QLayout`, `QDrawer`, `view=` | `61-component-usage-atlas.md`, `62-layout-patterns-and-examples.md`, `63-image-delivery-and-placeholders.md` |
| `Notify`, `Dialog`, `Loading`, `Screen`, `Platform`, `Cookies`, `ClosePopup`, `Ripple`, `Intersection`, `date`, `dom`, `uid` | `65-directive-usage-atlas.md`, `66-api-usage-atlas.md` |
| `sw.js` cache name, `SERVICE_WORKER_FILE`, update prompt copy, offline matrix | `37-pwa-operations-record.md` |
| `vue-tsc --noEmit`, `vitest run`, `cypress run`, `@quasar/testing-*` | `75-testing-ci-playbook.md` |
| a version number, `dist-tags`, `pinia` peer range, Node engines | `80-upstream-deltas-and-live-checks.md` |
| an old `quasar-*` skill name | `85-legacy-skill-coverage.md` |

## 2. Situation router

Each row states the observable situation you are in, not the destination's title.

| You are about to ... | Read |
| --- | --- |
| assert an exact prop, event, slot, method, directive value, or plugin option name | `05-authority-and-api-lookup.md` + run `scripts/query-installed-quasar-api.mjs` |
| plan or execute a v2 -> v3 upgrade, or recover from `quasar prepare`, a blocking App Extension, or a mode that builds but fails at runtime during one | `10-v2-to-v3-migration.md` |
| review a Quasar repo you did not write, or produce a migration-readiness assessment or plan document | `11-review-and-upgrade-checklist.md` |
| patch a repo whose `package.json` declares `@quasar/app-vite@^2` and that is not being migrated in this change | `12-v2-maintenance-playbook.md` |
| write a review comment, or choose between two shapes and need the correct/wrong pair to justify it | `13-examples-review-style.md` |
| edit `quasar.config` `build.env`, `define`, `defineEnv`, or decide whether a value may reach the browser | `20-v3-config-and-features.md` |
| add a Vite plugin, extend the Vite config, add an alias, configure a dev proxy, or change browser targets | `21-cli-vite-and-config.md` |
| write the literal text of a `quasar.config`, boot file, router bootstrap, env block, or `register-sw` file | `22-cli-cookbook-and-examples.md` |
| choose a caching strategy, write or edit `src-pwa/sw/custom-sw.*`, ship an update prompt, or debug a stale page after deploy | `30-service-worker-excellence.md` |
| render on the server: `ssrContext`, `preFetch`, cookie-to-header auth, SEO meta, or a hydration mismatch you must fix | `31-ssr-pwa-and-security.md` |
| open a file under `src-pwa/` at all, or change the InjectManifest contract | `32-pwa-injectmanifest-guard.md` first, then `30` |
| decide what the user sees when the SSR process returns 500, the API is unreachable, or the device is offline | `34-frontend-failure-and-degradation.md` |
| add or change a mode (`quasar dev -m ...`), or hit a "module not found" that appears in one mode only | `35-platform-modes.md` |
| send anything from the browser to a collector, log an unhandled error, or emit a web-vitals sample | `36-client-observability-contract.md` |
| ship a PWA change and hand it to whoever operates it | `37-pwa-operations-record.md` |
| build the SMS-OTP screen, wire `autocomplete="one-time-code"`, or add a device signal | `40-webotp-and-device-trust.md` |
| render a step-up challenge, read a TOTP verification timestamp, or gate UI on a permission bitmap | `41-step-up-and-permission-hints.md` |
| call an API the browser gates behind a prompt: microphone, camera, screen, geolocation, notifications, clipboard read, wake lock, sensors, Bluetooth/USB/NFC | `45-browser-apis-and-permissions.md` |
| choose SPA vs SSR vs PWA vs Capacitor for new work, or make first paint feel faster | `50-modern-experience.md` |
| have a component family in mind but not a symbol ("a table", "a picker", "an overlay") | `60-components-and-layouts.md` |
| choose between two Quasar components, or hit a component that behaves unexpectedly | `61-component-usage-atlas.md` |
| build or fix an app shell: `QLayout` `view`, drawers, containerized layout, nested routes | `62-layout-patterns-and-examples.md` |
| emit an image URL, a `srcset`, or a placeholder | `63-image-delivery-and-placeholders.md` |
| use a Quasar plugin, composable, directive, global option, or util and not know which file covers it | `64-plugins-composables-directives-options-utils.md` |
| write a `v-close-popup`, `v-intersection`, `v-ripple`, or touch directive | `65-directive-usage-atlas.md` |
| call `useMeta`, `useHydration`, `useDialogPluginComponent`, `useFormChild`, `Cookies`, `Screen`, `date`, or `dom` | `66-api-usage-atlas.md` |
| ship a data grid, a virtualized list, an overlay, an upload, or media — or explain a regression after a Vite upgrade | `70-guardrails-a11y-performance-monorepo.md` |
| add a test, change a test harness, or decide which commands prove this change | `75-testing-ci-playbook.md` |
| state a version number, a peer range, or a Node floor | `80-upstream-deltas-and-live-checks.md` |
| act on a request that names a retired `quasar-*` skill | `85-legacy-skill-coverage.md` |
| edit this skill's own files or scripts | `91-agent-authoring-and-dual-runtime.md` |

## 3. Route out — name the owner, do not restate its rules

Every row below is ground this skill does not own. Cite the owner; never restate its rule in this skill's voice.

| Ground | Owner |
| --- | --- |
| Vue and TypeScript code shape, composition patterns, TS type system and anti-patterns | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`), `references/22-typescript-type-system.md`, `references/24-typescript-project-and-antipatterns.md` |
| Broad non-Quasar frontend: SSR auth/session, data shaping, Web Vitals scoring, QA | `/alaa-frontend-developer` (`$alaa-frontend-developer`), `references/21-ssr-auth-and-session-patterns.md`, `references/41-lighthouse-and-web-vitals.md`, `references/50-qa-and-verification.md` |
| IndexedDB, quota, eviction, drafts, browser outbox, multi-tab locks, offline media store | `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/41-multitab-versionchange-and-locks.md`, `references/70-cache-and-drafts.md`, `references/71-browser-outbox.md`, `references/72-offline-media-store.md` |
| Video and audio playback, ABR, DRM, subtitles, in-app download, player analytics | `/alaa-shaka-player` (`$alaa-shaka-player`), `references/50-offline-and-in-app-download.md`, `references/11-vue-quasar-binding.md` |
| `packages/*`: entrypoints, exports maps, peer dependencies, dedupe, asset reachability | `/alaa-mono-package` (`$alaa-mono-package`), `references/20-peer-deps-dedupe-and-build-output.md`, `references/30-assets-css-and-ssr-client-assets.md` |
| Motion, transitions, reduced motion | `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/70-motion-contract.md` |
| Which modern CSS features are safe at which Baseline tier | `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/72-modern-css-baseline-tiers.md` |
| Digit and text normalization of any user input, fleet-wide | `/alaa-input-normalization` (`$alaa-input-normalization`), `references/20-browser-binding.md` |
| Timeout, retry, backoff, circuit breaking, idempotency, degradation doctrine | `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/10-deadlines-and-timeouts.md`, `references/20-retries.md`, `references/50-degradation.md` |
| Test design and the six proof levels | `/alaa-testing-strategy` (`$alaa-testing-strategy`), `references/20-layers.md`, `references/40-proof-strength.md` |
| Threat classes, review triggers, fail-closed doctrine, browser output trust | `/alaa-security-review` (`$alaa-security-review`), `references/20-untrusted-input.md`, `references/25-browser-trust-and-output.md` |
| Observability requirement levels, gates, sampling and retention budgets | `/alaa-observability-soc` (`$alaa-observability-soc`), `references/20-instrumentation-gates.md`, `references/30-quantitative-budgets.md` |
| Every field name, event name, metric name, and envelope key | `/alaa-services-contract` (`$alaa-services-contract`), `references/20-operational-and-observability-contract.md`, `references/24-metric-registry.md`, `references/60-frontend-sdk-consumption-contract.md` |
| Complexity budgets and structure choice | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`), `references/10-complexity-budget.md`, `references/30-choosing-a-structure.md` |
| Paginating any list endpoint, including QTable server pagination and QInfiniteScroll | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`), `references/40-wire-contract-limits-and-errors.md` |
| Trusted headers, token issuance, TOTP step-up trust semantics | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Permission bitmap contract and the canonical TypeScript decoder | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| Identifier codec the browser must match byte for byte | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
| Browser tus client behind `QUploader`, resume matching | `/tusd-upload-platform` (`$tusd-upload-platform`) |
| Presigned URLs and object storage | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`), `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`) |
| CI, Docker, and deploy execution for this frontend | `/alaa-frontend-devops` (`$alaa-frontend-devops`) |
| GitLab CI YAML expression | `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) |
| Reverse proxy in front of SSR | `/alaa-haproxy` (`$alaa-haproxy`) |
| Pre-implementation subsystem design | `/alaa-system-design` (`$alaa-system-design`) |
| The quality bar itself | `/alaa-project-constitution` (`$alaa-project-constitution`) |
| Model choice, effort, and thinking budgets | `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md` |
| Multi-phase plan and state artifacts | `/alaa-workflow` (`$alaa-workflow`) |
| Opt-in browser validation of a running app | `/playwright` (`$playwright`), `/playwright-interactive` (`$playwright-interactive`) |

Search: `topic map`, `routing`, `which file`, `symbol index`, `route out`, `owner`, `companion skill`.
