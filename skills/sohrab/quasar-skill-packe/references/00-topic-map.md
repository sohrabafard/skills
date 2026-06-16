# Topic Map

Start here when the user mentions Quasar but the exact surface is not obvious.

## Before config/CLI/mode work: detect the app-vite line

For any `quasar.config`, boot, env, alias, SSR, PWA, BEX, Electron, or Capacitor task, read `@quasar/app-vite` in `package.json` first. v2 and v3 have different import paths, config extensions, env keys, and aliases. The split table is in `70-upstream-deltas-and-live-checks.md`. Picking the wrong line produces code that does not run.

## Fast entry points

| If the task mentions...                                                                                                          | Read first                                           | Also load                                                                                         |
|----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `quasar.config`, boot files, routing, Pinia, aliases, env files, proxying, lazy loading, or build commands                       | `10-cli-vite-and-config.md` and `11-cli-cookbook-and-examples.md` | `20-ssr-pwa-and-security.md` if SSR/PWA is in scope                                               |
| SSR, hydration, `ssrContext`, middleware, `preFetch`, cookie auth, SEO, offline, or service worker                               | `20-ssr-pwa-and-security.md`                         | `21-pwa-injectmanifest-guard.md` for custom SW / InjectManifest changes; `10-cli-vite-and-config.md` |
| SPA, BEX, Capacitor, Cordova, or Electron                                                                                        | `30-platform-modes.md`                               | `10-cli-vite-and-config.md`                                                                       |
| A component or layout name such as `QTable`, `QDialog`, `QDrawer`, `QImg`, `QPage`, or `QLayout`                                 | `40-components-and-layouts.md` and `41-component-usage-atlas.md` | `60-guardrails-a11y-performance-monorepo.md`, and `20-ssr-pwa-and-security.md` for universal apps |
| A layout-specific term such as `view`, `QPageContainer`, `containerized layout`, `mini mode`, or `routing with layouts`         | `42-layout-patterns-and-examples.md`                 | `10-cli-vite-and-config.md`, `20-ssr-pwa-and-security.md`                                        |
| An image-delivery term such as `placeholder-src`, `srcset`, `sizes`, or deterministic `w/h` resizing                            | `43-image-delivery-and-placeholders.md`              | `41-component-usage-atlas.md`, `20-ssr-pwa-and-security.md`                                      |
| A plugin, composable, directive, option, or util such as `Notify`, `Loading`, `useMeta`, `useHydration`, `v-ripple`, or `Screen` | `50-plugins-composables-directives-options-utils.md` and `52-api-usage-atlas.md`; add `51-directive-usage-atlas.md` for directives | `20-ssr-pwa-and-security.md` for SSR-sensitive APIs                                               |
| Performance, a11y, packaging, peer deps, tree-shaking, monorepo contracts, or large list rendering                               | `60-guardrails-a11y-performance-monorepo.md`         | the feature-specific reference                                                                    |
| Upgrade, migration, "latest", or toolchain breakage after dependency changes                                                     | `70-upstream-deltas-and-live-checks.md`              | the affected feature reference                                                                    |

## Search aliases

Search these exact terms before using broad guesses:

- Config and build:
  - `extendViteConf`, `vitePlugins`, `viteVuePluginOptions`, `envFolder`, `envFiles`, `htmlMinifyOptions`, `yarn.lock`
- app-vite v3 surfaces:
  - `#q-app`, `build.env.folder`, `build.env.clientPrefix`, `defineEnv`, `import.meta.env.QUASAR_`, `@/ alias`, `src-pwa/sw`, `serve.devError`, `defineCapacitorConfig`
- SSR and hydration:
  - `ssrContext`, `defineSsrMiddleware`, `useHydration`, `useId`, `QNoSsr`, `preFetch`
- PWA:
  - `InjectManifest`, `GenerateSW`, `skipWaiting`, `clientsClaim`, `controllerchange`
- Platform modes:
  - `BEX Bridge`, `content scripts`, `background script`, `Capacitor`, `Cordova`, `preload`
- UI:
  - exact Quasar symbol names such as `QTable`, `QVirtualScroll`, `QImg`, `QDialog`, `QMenu`, `QUploader`
- Layout:
  - `view`, `containerized layout`, `QPageContainer`, `mini mode`, `overlay mode`
- Image delivery:
  - `placeholder-src`, `srcset`, `sizes`, `responsive candidates`, `ratio`, `w/h`
- APIs:
  - `useMeta`, `useHydration`, `useDialogPluginComponent`, `Screen`, `Notify`, `date`, `dom`
- Cross-cutting:
  - `peerDependencies`, `dedupe`, `tree-shaking`, `reduced motion`, `focus return`

## Fallback rules

- If the user names an old `quasar-*` skill directly, open `80-legacy-skill-coverage.md`.
- If the task spans config plus UI plus SSR, load `10`, `20`, and the feature-specific file.
- If the problem looks like a build or upgrade regression in a Quasar app, load `70` before proposing fixes.
- If the repo is Yarn-based or contains `yarn.lock`, prefer Yarn for installs and project scripts even if upstream docs mention Bun or npm.
