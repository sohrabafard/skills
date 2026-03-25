# Topic Map

Start here when the user mentions Quasar but the exact surface is not obvious.

## Fast entry points

| If the task mentions...                                                                                                          | Read first                                           | Also load                                                                                         |
|----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `quasar.config`, boot files, routing, Pinia, aliases, env files, proxying, lazy loading, or build commands                       | `10-cli-vite-and-config.md`                          | `20-ssr-pwa-and-security.md` if SSR/PWA is in scope                                               |
| SSR, hydration, `ssrContext`, middleware, `preFetch`, cookie auth, SEO, offline, or service worker                               | `20-ssr-pwa-and-security.md`                         | `10-cli-vite-and-config.md`                                                                       |
| SPA, BEX, Capacitor, Cordova, or Electron                                                                                        | `30-platform-modes.md`                               | `10-cli-vite-and-config.md`                                                                       |
| A component or layout name such as `QTable`, `QDialog`, `QDrawer`, `QImg`, `QPage`, or `QLayout`                                 | `40-components-and-layouts.md`                       | `60-guardrails-a11y-performance-monorepo.md`, and `20-ssr-pwa-and-security.md` for universal apps |
| A plugin, composable, directive, option, or util such as `Notify`, `Loading`, `useMeta`, `useHydration`, `v-ripple`, or `Screen` | `50-plugins-composables-directives-options-utils.md` | `20-ssr-pwa-and-security.md` for SSR-sensitive APIs                                               |
| Performance, a11y, packaging, peer deps, tree-shaking, monorepo contracts, or large list rendering                               | `60-guardrails-a11y-performance-monorepo.md`         | the feature-specific reference                                                                    |
| Upgrade, migration, "latest", or toolchain breakage after dependency changes                                                     | `70-upstream-deltas-and-live-checks.md`              | the affected feature reference                                                                    |

## Search aliases

Search these exact terms before using broad guesses:

- Config and build:
  - `extendViteConf`, `vitePlugins`, `viteVuePluginOptions`, `envFolder`, `envFiles`, `htmlMinifyOptions`
- SSR and hydration:
  - `ssrContext`, `defineSsrMiddleware`, `useHydration`, `useId`, `QNoSsr`, `preFetch`
- PWA:
  - `InjectManifest`, `GenerateSW`, `skipWaiting`, `clientsClaim`, `controllerchange`
- Platform modes:
  - `BEX Bridge`, `content scripts`, `background script`, `Capacitor`, `Cordova`, `preload`
- UI:
  - exact Quasar symbol names such as `QTable`, `QVirtualScroll`, `QImg`, `QDialog`, `QMenu`, `QUploader`
- Cross-cutting:
  - `peerDependencies`, `dedupe`, `tree-shaking`, `reduced motion`, `focus return`

## Fallback rules

- If the user names an old `quasar-*` skill directly, open `80-legacy-skill-coverage.md`.
- If the task spans config plus UI plus SSR, load `10`, `20`, and the feature-specific file.
- If the problem looks like a build or upgrade regression in a Quasar app, load `70` before proposing fixes.
