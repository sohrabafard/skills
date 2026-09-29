For exact version provenance and live-source authority, use [authority and API lookup](../05-authority-and-api-lookup.md); do not infer an unrecorded verification date from this split.

## 4. Canonical v2 -> v3 delta table

This is the only complete statement of the delta set in this pack. Migration sequence and failure recovery: `references/10-v2-to-v3-migration.md`. Executable shapes: `references/22-cli-cookbook-and-examples.md`. Env semantics: `references/20-v3-config-and-features.md`.

| Area | v2 | v3 |
| --- | --- | --- |
| Wrappers | `#q-app/wrappers` (`defineConfig`, `defineBoot`, `defineRouter`, `defineStore`, `defineSsrMiddleware`, `definePreFetch`) | `#q-app` |
| Config file | `.js` `.mjs` `.ts` `.cjs` `.cts` `.mts` | `.js` or `.ts` only |
| Constants | `process.env.{DEV,PROD,DEBUGGING,MODE,TARGET,CLIENT,SERVER}` | `import.meta.env.QUASAR_{DEV,PROD,DEBUG,MODE,TARGET,CLIENT,SERVER}` plus `QUASAR_<MODE>_MODE` flags |
| `index.html` | `<%= process.env.MY_VAR %>` | `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%` |
| Env config | `build.envFolder`, `build.envFiles`, `build.envFilter` | `build.env.{folder,file,filter,clientPrefix,backendPrefix}`; `clientPrefix` defaults `'QCLI_'` |
| Defines | `build.rawDefine`; `build.env` value injection | `build.define`; `build.defineEnv` |
| Options API | `build.vueOptionsAPI` defaults `true` | defaults `false` |
| Removed build keys | `build.analyze`, `build.polyfillModulePreload`, `cordova.noIosLegacyBuildFlag` | use `rollup-plugin-visualizer` through `build.vitePlugins` |
| Aliases | `src/`, `app/`, `components/`, `layouts/`, `pages/`, `assets/`, `boot/`, `stores/` | sole `@/` -> `/src`; templates use `~@/assets/...` |
| Renamed hooks | `ssr.extendPackageJson`, `pwa.extendManifestJson`, `pwa.injectPwaMetaTags`, `pwa.extendGenerateSWOptions`, `pwa.extendInjectManifestOptions`, `electron.extendPackageJson` | `ssr.extendSSRPackageJson`, `pwa.extendPWAManifestJson`, `pwa.injectPWAMetaTags`, `pwa.extendPWAGenerateSWOptions`, `pwa.extendPWAInjectManifestOptions`, `electron.extendElectronPackageJson` |
| SSR | Express scaffold; `serve.error()` | Hono/Express/Fastify/Koa; `serve.devError()`; `/src-ssr/server-assets` + `resolve.serverAssets()`; webserver built by Rolldown |
| PWA | custom SW in `/src-pwa/` | custom SW in `/src-pwa/sw/`; `/src-pwa/sw/tsconfig.json` extends `../../.quasar/tsconfig.pwa-sw.json`; ESLint glob `src-pwa/sw/**/*.ts` |
| BEX | — | `/src-bex/package.json` with `"type": "module"`; default target `chrome` |
| Capacitor | `capacitor.config.json`; Capacitor <= 4 supported | `capacitor.config.ts`/`.js` via `defineCapacitorConfig()` from `'@quasar/app-vite/capacitor'`; Capacitor <= 4 dropped; the `capacitor` config section loses `appName`, `version`, `description` |
| Electron | packager <= 18 | packager >= 19; preload is `.cjs`; `quasarRuntime` from `#q-app/electron/preload`; `registerQuasarRuntime` from `#q-app/electron/main`; assets in `/src-electron/electron-assets` |
| Boot redirects | thrown `{ url }` or Promise-carried redirect | call `redirect()` and return immediately |
| App Extensions | v2 Index API | `api.compatibleWith('@quasar/app-vite', '^3.0.0')`; `quasar <ext-id> <cmd>` -> `quasar run <ext-id> <cmd>` |
| Mode isolation | shared install | dependencies install under `/src-<mode>`; pnpm v11 needs `allowBuilds` for `rolldown` and friends plus an empty per-mode `pnpm-workspace.yaml` |
| Extend hooks | esbuild configs | `extendSSRWebserverConf`, `extendElectronMainConf`, `extendElectronPreloadConf` receive Rolldown configs; every `extendX()` may be async or return a merge object; `ctx.logger` is available |
| TypeScript | scattered `.d.ts`, `src-pwa/tsconfig.json`, `declare namespace NodeJS` | one root `/env.d.ts` declaring `interface ImportMetaEnv`; `quasar prepare` regenerates `.quasar/` tsconfigs |
| CLI | — | `--no-color` on every command; `quasar build --no-summary`; BEX `-t/--target` defaults `chrome` |
