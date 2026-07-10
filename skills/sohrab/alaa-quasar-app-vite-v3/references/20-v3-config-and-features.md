# app-vite v3: config surface, new capabilities, and version truth

Scope: what `@quasar/app-vite` v3 gives you and the config shapes that differ from everything written in the v2 era. Verified 2026-07-08 against quasar.dev docs, GitHub release notes, and npm metadata. For exact per-surface code shapes (full quasar.config examples, boot files, components), route to `references/22-cli-cookbook-and-examples.md` — this file owns the v3 capability map, not a second cookbook.

## Version truth (snapshot 2026-07-10 — refresh with `node scripts/check-upstream-versions.mjs`)

| Package | Stable | Published | Note |
|---|---|---|---|
| `@quasar/app-vite` | **3.0.1** | 2026-07-07 | Stable v3 line; holds npm `latest`. v3.0.0 landed 2026-07-06. |
| `@quasar/app-vite` v2 | 2.6.2 | 2026-06-03 | Maintenance line (~until 2027-06); for repos not yet migrated. |
| `quasar` | 2.21.1 | 2026-07-06 | UI framework. |
| `@quasar/extras` | 2.0.2 | 2026-07-02 | ESM-only; icon-lib cuts — audit before bumping. |
| `vite` | 8.1.4 | 2026-07-09 | v3 depends on `vite ^8.1.3`. |
| `vue` | 3.5.39 | 2026-06-25 | 3.6 still beta. |
| `vue-router` | 5.1.0 | 2026-05-28 | v5 is required by app-vite v3. |
| `pinia` | 3.0.4 | 2025-11-05 | `^2 || ^3` accepted. |
| `workbox-build` | 7.4.1 | 2026-05-04 | `>= 7` peer. |

Node engines for v3: `^22.22.0 || ^24 || ^26 || ^28 || ^30`.

## What v3 actually buys you

- **Rolldown replaces esbuild** for all `/src-*` builds, with mode builds parallelized: faster builds, redesigned build architecture, fewer CLI dependencies. `extendSSRWebserverConf` / `extendElectronMainConf` / `extendElectronPreloadConf` take Rolldown configs now.
- **Vite 8** under the hood, with Vite-native typed env (`import.meta.env`).
- **Env DX**: dotenv files hot-reload without a dev-server restart, env values are usable inside `quasar.config` itself, and the client/backend split is enforced by prefix (`build.env.clientPrefix`, default `'QCLI_'`).
- **First-class filename-based routing**: `build.filenameBasedRouting: boolean | VueRouterVitePluginOptions` on vue-router v5.
- **SSR**: choose the webserver at mode-add time — **Hono, Express, Fastify, or Koa** — with proper TS integration, improved serverless support, `/src-ssr/server-assets/` for runtime assets, and SSG groundwork.
- **Mode dependency isolation**: per-mode `package.json` under `/src-<mode>/`; Electron dist no longer needs its own install; cleaner Capacitor handling.
- **DX extras**: `ctx.logger` in quasar.config, async `extendX()` hooks that may return mergeable objects, `build.extendTsConfig()`, smarter dev reloads on config/dotenv changes, `--no-color`, `quasar build --no-summary`.

## The env contract (highest-frequency v3 surface)

```ts
// quasar.config.ts
import { defineConfig } from '#q-app'

export default defineConfig((ctx) => ({
  build: {
    env: {
      // Only vars with this prefix are exposed to client code. Everything
      // QCLI_-prefixed is PUBLIC by definition — never a secret.
      clientPrefix: 'QCLI_',
      // folder default: appPaths.appDir; file/filter available for layouts
    },
    define: { __BUILD_FLAG__: JSON.stringify('value') }, // must be stringify-ed
    defineEnv: { SOME_DEFINE: 'my-string' },             // sugar -> import.meta.env.SOME_DEFINE
  },
}))
```

- App code reads `import.meta.env.QCLI_*` plus built-ins: `QUASAR_MODE`, `QUASAR_DEV`, `QUASAR_PROD`, `QUASAR_DEBUG`, `QUASAR_CLIENT`, `QUASAR_SERVER`, and per-mode booleans (`QUASAR_SPA_MODE`, `QUASAR_PWA_MODE`, `QUASAR_SSR_MODE`, `QUASAR_ELECTRON_MODE`, `QUASAR_BEX_MODE`, `QUASAR_CAPACITOR_MODE`, `QUASAR_CORDOVA_MODE`).
- Custom vars are typed once in root `/env.d.ts` on `interface ImportMetaEnv`.
- `index.html` templating: `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%`.
- `.env` and `.env.local` load by default; mode/dev-prod suffixed files are supported (exact default-loaded list beyond those two: verify live on quasar.dev).

✅ Do — treat `clientPrefix` as a security boundary: server-only secrets get a non-client prefix (or none) and never appear in client bundles.

❌ Don't — port a v2 `build.env: { API_KEY: ... }` injection object straight across; in v3 that key has a completely different meaning (dotenv behavior config, not value injection).

## Sharp edges to check in every v3 repo

- `build.vueOptionsAPI` defaults to **false**. Any Options-API dependency (or legacy component) silently breaks until you set it to `true`.
- Boot `redirect()`: call and return immediately; no thrown `{ url }`, no Promise-carried redirect.
- Only `@/` alias exists. `build.alias` + `ctx.appPaths` can bridge legacy aliases, but that is migration debt, not a target state.
- `quasar.config` only `.js`/`.ts`.
- App Extensions must declare `api.compatibleWith('@quasar/app-vite', '^3.0.0')`; run AEs via `quasar run <ext-id> <cmd>`.
- pnpm v11: `rolldown` (and friends) must be in `allowBuilds`; per-mode empty `pnpm-workspace.yaml` files force local installs.
- Package-manager rule: match the repo's lockfile; never switch managers as part of a Quasar task.

## Mode notes (route for depth)

- SPA/SSR/PWA/BEX/Capacitor/Cordova/Electron structure and per-mode v3 deltas: `references/35-platform-modes.md`.
- SSR engineering (hydration, request isolation, auth): `$alaa-frontend-developer` + `references/31-ssr-pwa-and-security.md`.
- PWA/service worker implementation: this skill's `30-service-worker-excellence.md`.
- Migration from v2: this skill's `10-v2-to-v3-migration.md`.

## Quasar UI recent-features digest (2.18 -> 2.21)

- 2.18: QTable `table-row-style-fn`/`table-row-class-fn`/`grid-style-fn`/`grid-class-fn`; QMenu/QBtnDropdown `no-esc-dismiss`; `evt.qAvoidFocus`; pure-CSS icon support.
- 2.19: toolchain modernization (rolldown/lightningcss/oxlint); **browser targets raised to Baseline widely-available (Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+)**; `date/getMinDate`/`getMaxDate` now return `Date` objects (behavior change).
- 2.20: smaller/faster UI build; `Cookies` uses Max-Age; QPopupProxy stops emitting `update:modelValue` from `useAnchor()`.
- 2.21: QTable instance `getCellValue(colName, row)`; 2.21.1 fixes Safari page-scroll loss after closing QDialog via CSS.

The raised browser floor matters: it means the modern CSS features in `$alaa-frontend-developer` `references/25-modern-css-and-motion.md` Tier 1–2 are inside Quasar's own support matrix — use them freely in v3 apps.
