# v2 -> v3 migration playbook (@quasar/app-vite)

Scope: migrating a production Quasar CLI (Vite) app from `@quasar/app-vite` v2 to v3. Verified 2026-07-08 against the official quasar.dev upgrade guide, quasar.config docs, GitHub release notes, and npm metadata. v3.0.1 is stable (published 2026-07-07); v2.6.2 is the last v2 stable.

Also load: `20-v3-config-and-features.md` (target-state config shapes); `22-cli-cookbook-and-examples.md` for exact per-surface code shapes; `11-review-and-upgrade-checklist.md` for the verified delta checklist and repo-scan template; `12-v2-maintenance-playbook.md` for the v2-era semantics you are migrating away from; `$alaa-workflow` when the migration is large enough to need plan/state artifacts.

## 0. Preconditions — check before touching anything

- Node: v3.0.1 requires `^22.22.0 || ^24 || ^26 || ^28 || ^30`. Verify CI images and Dockerfiles too, not just the dev machine.
- Peer floor: `quasar ^2.16.0`, `vue ^3.2.29`, **`vue-router >= 5`** (v5 is required — this is its own sub-migration if the app is on v4), `pinia ^2 || ^3`, `workbox-build >= 7`, `typescript >= 5`, `@capacitor/cli >= 5`.
- App Extensions: the v3 AE engine only accepts extensions declaring `api.compatibleWith('@quasar/app-vite', '^3.0.0')`. Inventory every AE (including `@quasar/testing-*`) and confirm a v3-compatible release exists before scheduling the migration; testing-extension v3 compatibility was UNVERIFIED at research time — check each AE's changelog live.
- Capacitor repos: migrate `capacitor.config.json` to `capacitor.config.ts`/`.js` with `defineCapacitorConfig` from `'@quasar/app-vite/capacitor'` BEFORE the upgrade (json support is dropped).
- Recommended companion bump: `@quasar/extras` v2 (ESM-only; drops FontAwesome v5/v6, Ionicons v5–7, MDI v3–6 — audit icon usage first).

✅ Do — run the migration on a branch with a written checklist, and treat vue-router 4 -> 5 and @quasar/extras 1 -> 2 as separate commits from the app-vite bump.

❌ Don't — bump `@quasar/app-vite` opportunistically inside an unrelated dependency-update PR; the env/alias/import changes touch app code, not just the lockfile.

## 1. Official sequence

1. `package.json`: `"@quasar/app-vite": "^3.0.0"`, `"vue-router": "^5.0.6"` (and other peers as needed).
2. Install with the repo's package manager (respect the lockfile; do not switch managers).
3. Apply the code/config changes below.
4. `quasar prepare`, then restart the IDE/TS server.
5. `quasar dev` per mode you ship, then `quasar build` per mode; fix issues mode by mode.

## 2. Mechanical changes (safe global edits)

| v2 | v3 |
|---|---|
| `import { defineConfig } from '#q-app/wrappers'` (and all `#q-app/wrappers` imports) | `'#q-app'` |
| `process.env.MY_VAR` in app code | `import.meta.env.MY_VAR` |
| `process.env.MODE` / `process.env.DEV` / `process.env.PROD` / `process.env.DEBUGGING` / `process.env.CLIENT` / `process.env.SERVER` | `import.meta.env.QUASAR_MODE` / `QUASAR_DEV` / `QUASAR_PROD` / `QUASAR_DEBUG` / `QUASAR_CLIENT` / `QUASAR_SERVER` |
| Mode checks like `process.env.MODE === 'pwa'` | `import.meta.env.QUASAR_PWA_MODE` (per-mode booleans: `QUASAR_SPA_MODE`, `QUASAR_SSR_MODE`, `QUASAR_ELECTRON_MODE`, `QUASAR_BEX_MODE`, `QUASAR_CAPACITOR_MODE`, `QUASAR_CORDOVA_MODE`) |
| `<%= process.env.MY_VAR %>` in `index.html` | `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%` |
| Legacy aliases `src/`, `app/`, `components/`, `layouts/`, `pages/`, `assets/`, `boot/`, `stores/` | single `@/` -> `/src` (templates: `~@/assets/...`) |
| `quasar.config.cjs` / `.mjs` / `.cts` / `.mts` | `.js` or `.ts` only |

Alias note: prefer rewriting imports to `@/`. Only restore legacy aliases via `build.alias` + `ctx.appPaths` as a temporary, documented bridge — leaving them permanently hides migration debt.

## 3. quasar.config changes

- Env: delete `build.env` (v2 injection object), `build.rawDefine`, `build.envFolder`, `build.envFiles`, `build.envFilter`. Replace with the v3 `build.env` object: `{ clientPrefix (default 'QCLI_'), backendPrefix, folder, file, filter }` plus `build.define` (JSON.stringify'ed values) and `build.defineEnv` sugar. Only vars matching `clientPrefix` reach client code — treat everything with that prefix as public.
- `build.vueOptionsAPI` now defaults to **false** — set `true` explicitly if any code or dependency uses the Options API, or components will silently break.
- Removed keys: `build.polyfillModulePreload`, `build.analyze` (wire `rollup-plugin-visualizer` through `build.vitePlugins` instead), `cordova.noIosLegacyBuildFlag`.
- Hook renames: `ssr.extendPackageJson` -> `ssr.extendSSRPackageJson`; `pwa.extendManifestJson` -> `pwa.extendPWAManifestJson`; `pwa.injectPwaMetaTags` -> `pwa.injectPWAMetaTags`; `pwa.extendGenerateSWOptions` -> `pwa.extendPWAGenerateSWOptions`; `pwa.extendInjectManifestOptions` -> `pwa.extendPWAInjectManifestOptions`; `electron.extendPackageJson` -> `electron.extendElectronPackageJson`.
- `extendSSRWebserverConf`, `extendElectronMainConf`, `extendElectronPreloadConf` now receive **Rolldown** configs (was esbuild) — port any esbuild-specific options.
- All `extendX()` methods may be async and may return objects to merge; `ctx.logger` is available inside quasar.config.

## 4. Per-mode changes

- **Boot files**: `redirect()` must be called and returned from immediately; throwing `{ url }` or returning a Promise carrying it no longer works.
- **SSR**: pick the webserver (Hono/Express/Fastify/Koa) — re-adding the mode is the clean path; `serve.error()` -> `serve.devError()`; new `/src-ssr/server-assets/` folder for runtime assets (`resolve.serverAssets()`); webserver builds via Rolldown.
- **PWA**: move `custom-sw.{js,ts}` into `/src-pwa/sw/`; TS: `/src-pwa/sw/tsconfig.json` extending `"../../.quasar/tsconfig.pwa-sw.json"`; update ESLint globs to `src-pwa/sw/**/*.ts`; `sourceFiles` defaults are now `pwaRegisterServiceWorker: 'src-pwa/register-sw'`, `pwaServiceWorker: 'src-pwa/custom-sw'` (file physically under `src-pwa/sw/`). See `30-service-worker-excellence.md` for what the SW itself should do.
- **Capacitor**: config file migration (see preconditions); quasar.config `capacitor` section loses `appName`, `version`, `description`.
- **Electron**: icons move to `/src-electron/electron-assets/icons`; use `resolveElectronAssetsPath('icons/icon.png')` and `registerQuasarRuntime` from `#q-app/electron/main`, `quasarRuntime` from `#q-app/electron/preload`; `preload: path.join(import.meta.dirname, 'electron-preload.cjs')`; `mainWindow.loadURL(import.meta.env.QUASAR_APP_URL)`.
- **Mode dependency isolation**: per-mode `package.json` under `/src-<mode>/` (`"type": "module"`); `src-capacitor/package.json` is no longer auto-rewritten. pnpm v11: allow `rolldown` (and esbuild/lightningcss) in `allowBuilds`, add empty `/src-<mode>/pnpm-workspace.yaml` files.

## 5. TypeScript

One `/env.d.ts` at project root declares custom vars on `interface ImportMetaEnv`; delete `declare namespace NodeJS { interface ProcessEnv ... }` blocks, scattered `.d.ts`, and the old `src-pwa/tsconfig.json`. `quasar prepare` regenerates `.quasar/` tsconfigs.

## 6. CLI deltas

`--no-color` on all commands; `quasar build --no-summary`; App Extension commands only as `quasar run <ext-id> <cmd>` (bare `quasar <ext-id> <cmd>` removed); BEX `-t/--target` defaults to `chrome`.

## 7. Validation gate (per mode you ship)

1. `quasar prepare` succeeds; IDE/TS has no `import.meta.env` type errors.
2. `quasar dev` boots; env hot-reload works (edit `.env`, observe reload without restart).
3. `quasar build` succeeds; for SSR also boot the production server; for PWA verify the SW registers and precache manifest looks sane; Capacitor/Cordova `www` output is clean (the v3.0.1 fix targeted exactly this).
4. Lint/typecheck/unit suites pass; grep for leftovers: `process.env.`, `#q-app/wrappers`, legacy alias imports, `envFolder`, `rawDefine`, `extendManifestJson`.
5. Report what was migrated, what was validated with which commands, and any AE still blocking.

✅ Do — migrate and validate one mode at a time (SPA first, then SSR/PWA/native), committing per step.

❌ Don't — declare the migration done when `quasar dev` runs for SPA only; the breaking changes concentrate in SSR/PWA/Electron/Capacitor surfaces.

## 8. Rollback posture

Keep the pre-migration lockfile and branch until every shipped mode passes validation. If a blocker forces a pause, pin `@quasar/app-vite@^2` (v2.6.2) — an unpinned `latest` install now pulls v3.
