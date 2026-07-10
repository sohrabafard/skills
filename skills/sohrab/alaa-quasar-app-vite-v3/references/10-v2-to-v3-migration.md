# v2 -> v3 migration playbook (`@quasar/app-vite`)

Production Quasar CLI (Vite) migration. Verified 2026-07-08 against official upgrade/config docs, releases, and npm: v3.0.1 stable (2026-07-07); v2.6.2 last v2 stable.

Also load: `20-v3-config-and-features.md` (target shapes), `22-cli-cookbook-and-examples.md` (exact shapes), `11-review-and-upgrade-checklist.md` (canonical deltas/scan), `12-v2-maintenance-playbook.md` (source semantics), and `$alaa-workflow` when plan/state artifacts are warranted.

## 0. Preconditions

- Node v3.0.1: `^22.22.0 || ^24 || ^26 || ^28 || ^30`; verify developer, CI, and Docker runtimes.
- Peers: `quasar ^2.16.0`, `vue ^3.2.29`, **`vue-router >= 5`** (v4 -> v5 is a sub-migration), `pinia ^2 || ^3`, `workbox-build >= 7`, `typescript >= 5`, `@capacitor/cli >= 5`.
- Inventory every App Extension, including `@quasar/testing-*`; v3 accepts only `api.compatibleWith('@quasar/app-vite', '^3.0.0')`. Confirm compatible releases before scheduling; testing-extension v3 support was UNVERIFIED at research time, so check each changelog live.
- Before upgrade, Capacitor repos must replace `capacitor.config.json` (dropped) with `capacitor.config.ts`/`.js` using `defineCapacitorConfig` from `'@quasar/app-vite/capacitor'`.
- Recommended separate bump: `@quasar/extras` v2 is ESM-only and drops FontAwesome v5/v6, Ionicons v5–7, MDI v3–6; audit icons first.

✅ Branch with a written checklist; keep vue-router 4 -> 5 and extras 1 -> 2 as separate commits from app-vite. ❌ Never hide the app-vite bump in unrelated dependency work: env/alias/import changes affect app code.

## 1. Sequence

1. Set `"@quasar/app-vite": "^3.0.0"`, `"vue-router": "^5.0.6"`, and required peers in `package.json`.
2. Install with the lockfile's package manager; never switch.
3. Apply changes below.
4. Run `quasar prepare`; restart IDE/TS server.
5. Run `quasar dev`, then `quasar build`, for every shipped mode; fix mode by mode.

## 2. Mechanical edits

| v2 | v3 |
|---|---|
| all `#q-app/wrappers` imports | `#q-app` |
| app `process.env.MY_VAR` | `import.meta.env.MY_VAR` |
| `process.env.MODE`, `process.env.DEV`, `process.env.PROD`, `process.env.DEBUGGING`, `process.env.CLIENT`, `process.env.SERVER` | `import.meta.env.QUASAR_MODE`, `import.meta.env.QUASAR_DEV`, `import.meta.env.QUASAR_PROD`, `import.meta.env.QUASAR_DEBUG`, `import.meta.env.QUASAR_CLIENT`, `import.meta.env.QUASAR_SERVER` |
| `process.env.MODE === 'pwa'`-style checks | `import.meta.env.QUASAR_PWA_MODE`; also `QUASAR_SPA_MODE`, `QUASAR_SSR_MODE`, `QUASAR_ELECTRON_MODE`, `QUASAR_BEX_MODE`, `QUASAR_CAPACITOR_MODE`, `QUASAR_CORDOVA_MODE` |
| `index.html`: `<%= process.env.MY_VAR %>` | `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%` |
| `src/`, `app/`, `components/`, `layouts/`, `pages/`, `assets/`, `boot/`, `stores/` | sole `@/` -> `/src`; templates use `~@/assets/...` |
| `quasar.config.cjs/.mjs/.cts/.mts` | `.js` or `.ts` only |

Prefer rewriting aliases to `@/`. A temporary `build.alias` + `ctx.appPaths` bridge must be documented migration debt; permanent restoration hides debt.

## 3. `quasar.config`

- Delete v2 `build.env` injection, `build.rawDefine`, `build.envFolder`, `build.envFiles`, `build.envFilter`. Use v3 `build.env: { clientPrefix: 'QCLI_', backendPrefix, folder, file, filter }`, `build.define` (non-strings auto-`JSON.stringify`; wrap string literals), and `build.defineEnv` sugar. Only `clientPrefix` vars reach client code; all are public.
- `build.vueOptionsAPI` defaults **false**; set `true` if any app/dependency code uses Options API.
- Remove `build.polyfillModulePreload`, `build.analyze` (use `rollup-plugin-visualizer` via `build.vitePlugins`), and `cordova.noIosLegacyBuildFlag`.
- Rename: `ssr.extendPackageJson` -> `ssr.extendSSRPackageJson`; `pwa.extendManifestJson` -> `pwa.extendPWAManifestJson`; `pwa.injectPwaMetaTags` -> `pwa.injectPWAMetaTags`; `pwa.extendGenerateSWOptions` -> `pwa.extendPWAGenerateSWOptions`; `pwa.extendInjectManifestOptions` -> `pwa.extendPWAInjectManifestOptions`; `electron.extendPackageJson` -> `electron.extendElectronPackageJson`.
- `extendSSRWebserverConf`, `extendElectronMainConf`, `extendElectronPreloadConf` now receive Rolldown, not esbuild configs; port esbuild options. Every `extendX()` may be async/return a merge object; `ctx.logger` is available.

## 4. Mode changes

- **Boot:** call `redirect()` and return immediately; thrown `{ url }` or Promise-carried redirects no longer work.
- **SSR:** choose Hono/Express/Fastify/Koa; re-add mode for the clean path. `serve.error()` -> `serve.devError()`; runtime assets use `/src-ssr/server-assets/` + `resolve.serverAssets()`; webserver builds use Rolldown.
- **PWA:** move `custom-sw.{js,ts}` to `/src-pwa/sw/`; TS adds `/src-pwa/sw/tsconfig.json` extending `"../../.quasar/tsconfig.pwa-sw.json"`; ESLint uses `src-pwa/sw/**/*.ts`. `sourceFiles` defaults: `pwaRegisterServiceWorker: 'src-pwa/register-sw'`, `pwaServiceWorker: 'src-pwa/custom-sw'` although the file is under `src-pwa/sw/`. SW behavior: `30-service-worker-excellence.md`.
- **Capacitor:** migrate config as above; the quasar.config `capacitor` section loses `appName`, `version`, `description`.
- **Electron:** icons -> `/src-electron/electron-assets/icons`; use `resolveElectronAssetsPath('icons/icon.png')`, `registerQuasarRuntime` from `#q-app/electron/main`, `quasarRuntime` from `#q-app/electron/preload`; `preload: path.join(import.meta.dirname, 'electron-preload.cjs')`; `mainWindow.loadURL(import.meta.env.QUASAR_APP_URL)`.
- **Isolation:** each `/src-<mode>/package.json` uses `"type": "module"`; `src-capacitor/package.json` is no longer auto-rewritten. pnpm v11: allow `rolldown`, esbuild, lightningcss in `allowBuilds`; add empty `/src-<mode>/pnpm-workspace.yaml`.

## 5. TypeScript and CLI

Use one root `/env.d.ts` declaring custom `interface ImportMetaEnv`; delete `declare namespace NodeJS { interface ProcessEnv ... }`, scattered `.d.ts`, and old `src-pwa/tsconfig.json`. `quasar prepare` regenerates `.quasar/` tsconfigs.

CLI: `--no-color` on every command; `quasar build --no-summary`; AE commands only `quasar run <ext-id> <cmd>` (`quasar <ext-id> <cmd>` removed); BEX `-t/--target` defaults `chrome`.

## 6. Per-shipped-mode gate

1. `quasar prepare`; no IDE/TS `import.meta.env` errors.
2. `quasar dev`; edit `.env` and prove hot reload without restart.
3. `quasar build`; also start production SSR, inspect PWA registration/precache, and verify clean Capacitor/Cordova `www` output (the v3.0.1 fix target).
4. Pass lint/typecheck/unit; grep `process.env.`, `#q-app/wrappers`, legacy aliases, `envFolder`, `rawDefine`, `extendManifestJson`.
5. Report migrated scope, exact commands/results, and blocking AEs.

✅ Migrate/validate/commit SPA, then SSR/PWA/native separately. ❌ SPA dev alone never proves completion; major breaks cluster in SSR/PWA/Electron/Capacitor.

## 7. Rollback

Retain pre-migration lockfile/branch until every shipped mode passes. If paused, pin `@quasar/app-vite@^2` (v2.6.2); unpinned `latest` now resolves v3.
