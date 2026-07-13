# app-vite v3 config, capabilities, versions

Owns v3 capability/config differences, not cookbook shapes (use `22-cli-cookbook-and-examples.md`). Verified 2026-07-08 against Quasar docs/releases/npm.

## Version snapshot: 2026-07-10

Refresh: `node scripts/check-upstream-versions.mjs`.

| Package | Stable/published | Note |
|---|---|---|
| `@quasar/app-vite` | **3.0.1**, 2026-07-07 | Stable/`latest`; 3.0.0 landed 2026-07-06 |
| app-vite v2 | 2.6.2, 2026-06-03 | Maintenance ~until 2027-06 |
| `quasar` | 2.21.1, 2026-07-06 | UI framework |
| `@quasar/extras` | 2.0.2, 2026-07-02 | ESM-only; icon cuts require audit |
| `vite` | 8.1.4, 2026-07-09 | v3 depends on `vite ^8.1.3` |
| `vue` | 3.5.39, 2026-06-25 | 3.6 beta |
| `vue-router` | 5.1.0, 2026-05-28 | v5 required |
| `pinia` | 3.0.4, 2025-11-05 | `^2 || ^3` |
| `workbox-build` | 7.4.1, 2026-05-04 | `>= 7` |

v3 Node: `^22.22.0 || ^24 || ^26 || ^28 || ^30`.

## Capabilities

- Rolldown replaces esbuild for all `/src-*` builds; mode builds parallelize, architecture is redesigned, CLI deps shrink. `extendSSRWebserverConf`, `extendElectronMainConf`, `extendElectronPreloadConf` now receive Rolldown configs.
- Vite 8 and typed `import.meta.env`.
- Dotenv hot reload without server restart; env is usable in `quasar.config`; `build.env.clientPrefix` (default `'QCLI_'`) enforces client/backend split.
- `build.filenameBasedRouting: boolean | VueRouterVitePluginOptions` on vue-router v5.
- SSR mode-add selects Hono/Express/Fastify/Koa, with TS, better serverless support, `/src-ssr/server-assets/`, and SSG groundwork.
- Per-mode `/src-<mode>/package.json`; Electron dist needs no separate install; cleaner Capacitor handling.
- `ctx.logger`; async/merge-returning `extendX()`; `build.extendTsConfig()`; smarter config/dotenv reloads; `--no-color`; `quasar build --no-summary`.

## Env contract

```ts
import { defineConfig } from '#q-app'

export default defineConfig(() => ({
  build: {
    env: {
      clientPrefix: 'QCLI_', // QCLI_* is PUBLIC; never secret
      // folder defaults appPaths.appDir; file/filter support layouts
    },
    define: { __BUILD_FLAG__: JSON.stringify('value') }, // wrap string literal
    defineEnv: { SOME_DEFINE: 'my-string' }, // -> import.meta.env.SOME_DEFINE
  },
}))
```

- App code reads `import.meta.env.QCLI_*`, `QUASAR_MODE`, `QUASAR_DEV`, `QUASAR_PROD`, `QUASAR_DEBUG`, `QUASAR_CLIENT`, `QUASAR_SERVER`, plus `QUASAR_SPA_MODE`, `QUASAR_PWA_MODE`, `QUASAR_SSR_MODE`, `QUASAR_ELECTRON_MODE`, `QUASAR_BEX_MODE`, `QUASAR_CAPACITOR_MODE`, `QUASAR_CORDOVA_MODE`.
- Type custom vars once in root `/env.d.ts` on `interface ImportMetaEnv`.
- `index.html`: `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%`.
- `.env` and `.env.local` load by default; mode/dev-prod suffixes exist. Verify the full default list live on quasar.dev.

✅ `clientPrefix` is a security boundary: secrets get no client prefix. ❌ Never port v2 `build.env: { API_KEY: ... }` directly; v3 `build.env` configures dotenv, not value injection.

## Sharp edges

- `build.vueOptionsAPI` defaults **false**; set `true` for any legacy/dependency Options API.
- After boot `redirect()`, return immediately; never throw `{ url }` or carry via Promise.
- Only `@/` remains. `build.alias` + `ctx.appPaths` may bridge temporarily, documented as debt.
- `quasar.config` supports only `.js`/`.ts`.
- AEs require `api.compatibleWith('@quasar/app-vite', '^3.0.0')`; run `quasar run <ext-id> <cmd>`.
- pnpm v11 `allowBuilds` must include `rolldown` and friends; empty per-mode `pnpm-workspace.yaml` forces local installs.
- Follow lockfile package manager; never switch during Quasar work.

## Depth routing

- Mode structure/deltas: `references/35-platform-modes.md`; SSR/hydration/request isolation/auth: `$alaa-frontend-developer` + `references/31-ssr-pwa-and-security.md`; PWA/SW: `30-service-worker-excellence.md`; migration: `10-v2-to-v3-migration.md`; cookbook shapes: `references/22-cli-cookbook-and-examples.md`.

## Quasar UI 2.18–2.21

- 2.18: QTable `table-row-style-fn`, `table-row-class-fn`, `grid-style-fn`, `grid-class-fn`; QMenu/QBtnDropdown `no-esc-dismiss`; `evt.qAvoidFocus`; pure-CSS icons.
- 2.19: Rolldown/lightningcss/oxlint modernization; Baseline widely-available floor (Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+); `date/getMinDate`/`getMaxDate` return `Date` (behavior change).
- 2.20: smaller/faster build; `Cookies` uses Max-Age; QPopupProxy no longer emits `update:modelValue` from `useAnchor()`.
- 2.21: QTable `getCellValue(colName, row)`; 2.21.1 fixes Safari page-scroll loss after QDialog close via CSS.

The browser floor puts `$alaa-ui-ux-design-system` `references/70-motion-and-modern-css.md` Tier 1–2 inside Quasar support; use freely in v3.
