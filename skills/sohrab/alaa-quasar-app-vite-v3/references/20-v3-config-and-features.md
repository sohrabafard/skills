# app-vite v3 config, env, and capabilities

You are about to edit `quasar.config` `build.env`, `build.define`, or `build.defineEnv`, or to decide whether a value may reach the browser. This file owns the **env contract** and the v3 capability surface. Cookbook shapes are `references/22-cli-cookbook-and-examples.md`; every version number is `references/80-upstream-deltas-and-live-checks.md`; the v2 -> v3 delta table is §4 of that file.

## Capabilities added by v3

- Rolldown replaces esbuild for all `/src-*` builds; mode builds parallelize; the CLI dependency tree shrank. `extendSSRWebserverConf`, `extendElectronMainConf`, and `extendElectronPreloadConf` receive Rolldown configs.
- Vite 8 and typed `import.meta.env`.
- Dotenv hot reload without a server restart; env is usable inside `quasar.config`; `build.env.clientPrefix` enforces the client/backend split.
- `build.filenameBasedRouting: boolean | VueRouterVitePluginOptions` on vue-router v5.
- SSR mode-add selects Hono, Express, Fastify, or Koa, with TypeScript, better serverless support, `/src-ssr/server-assets/`, and SSG groundwork.
- Per-mode `/src-<mode>/package.json`; the Electron dist needs no separate install; cleaner Capacitor handling.
- `ctx.logger`; async or merge-returning `extendX()`; `build.extendTsConfig()`; smarter config and dotenv reloads; `--no-color`; `quasar build --no-summary`.

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
- Type custom variables once, in the root `/env.d.ts`, on `interface ImportMetaEnv`.
- `index.html`: `<%= importMetaEnv.MY_VAR %>` or `%MY_VAR%`.
- `.env` and `.env.local` load by default; mode and dev/prod suffixes exist. Verify the full default list live on quasar.dev.

✅ `clientPrefix` is a security boundary: a secret gets no client prefix. ❌ Never port a v2 `build.env: { API_KEY: ... }` directly; in v3 `build.env` configures dotenv, it does not inject values.

- **`build.define` auto-`JSON.stringify`s non-strings; wrap only a genuine string literal.** `define: { __BUILD_ID__: JSON.stringify(String(Date.now())) }` double-stringifies and emits a quoted string. The worked pair is `references/22-cli-cookbook-and-examples.md`.
- **`build.defineEnv` always stringifies and always prefixes `import.meta.env.`.** It is the v3 replacement for v2 `build.env` value injection, not for `build.rawDefine`.
- **Access env directly and statically.** Never destructure `import.meta.env`, never index it with a computed key, and never log the whole object: build-time replacement rewrites literal member reads only, so anything else resolves to `undefined` in production while working in dev.

## Config validation and runtime configuration

- **Validate every environment value the app requires at startup, and fail loudly when one is missing.** Do the check once, in a boot file, and throw with the variable's name. A value read as `undefined` deep in a component surfaces as a broken feature hours later; a boot-time throw surfaces as a build or first-load failure with a name in it.
- **A value that must change without a rebuild is not a `define` and not a `.env` variable.** Both are baked into the bundle at build time. Fetch such a value from a small runtime endpoint before the app renders its first authenticated view, treat the fetch as a failure path per `references/34-frontend-failure-and-degradation.md` §2, and give it a default that keeps the app usable when the fetch fails.
- **The same variable name never means two things across modes.** If SSR and SPA need different values, they get different names.

## Sharp edges

- `build.vueOptionsAPI` defaults **false**; set it `true` only when application or dependency code uses the Options API.
- After a boot `redirect()`, return immediately. Never throw `{ url }` and never carry the redirect through a Promise.
- Only `@/` remains. `build.alias` plus `ctx.appPaths` may bridge temporarily and is recorded as migration debt in `references/11-review-and-upgrade-checklist.md` §4.
- `quasar.config` supports only `.js` and `.ts`.
- App Extensions require `api.compatibleWith('@quasar/app-vite', '^3.0.0')`, and run as `quasar run <ext-id> <cmd>`.
- pnpm v11 `allowBuilds` must include `rolldown` and its siblings; an empty per-mode `pnpm-workspace.yaml` forces local installs.
- Follow the lockfile's package manager; never switch during Quasar work.

## Quasar UI feature notes

- 2.18: QTable `table-row-style-fn`, `table-row-class-fn`, `grid-style-fn`, `grid-class-fn`; QMenu/QBtnDropdown `no-esc-dismiss`; `evt.qAvoidFocus`; pure-CSS icons.
- 2.19: Baseline widely-available floor — Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+; `date/getMinDate` and `getMaxDate` return `Date`, a behaviour change.
- 2.20: `Cookies` uses `Max-Age`; QPopupProxy no longer emits `update:modelValue` from `useAnchor()`.
- 2.21: QTable `getCellValue(colName, row)`.
- 2.22 and 2.23 are not yet read here — see `references/80-upstream-deltas-and-live-checks.md` §5 before asserting anything about them.

That browser floor puts Quasar's supported range above the Baseline tiers owned by `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/72-modern-css-baseline-tiers.md`. Read which CSS features sit in which tier there; this skill states only that the Quasar floor does not block them.

## Depth routing

Mode structure and deltas: `references/35-platform-modes.md`. SSR, hydration, request isolation, and auth: `references/31-ssr-pwa-and-security.md`. Service workers: `references/30-service-worker-excellence.md`. Migration: `references/10-v2-to-v3-migration.md`. Exact shapes: `references/22-cli-cookbook-and-examples.md`.

Search: `build.env`, `clientPrefix`, `backendPrefix`, `defineEnv`, `build.define`, `rawDefine`, `import.meta.env`, `env.d.ts`, `ImportMetaEnv`, `dotenv`, `vueOptionsAPI`, `filenameBasedRouting`, `allowBuilds`, `runtime config`, `fail fast on missing env`.
