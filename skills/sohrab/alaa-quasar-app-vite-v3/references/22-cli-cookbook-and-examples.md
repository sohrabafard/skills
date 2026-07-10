# CLI cookbook and examples

Load only when exact Quasar shapes matter: `quasar.config`, boot, router bootstrap, env, Vite extensions. It prevents wrapper, side-selection, startup-order, SSR, and v2/v3 shape mistakes; use conceptual files otherwise.

## Contents

Line detection · config · env · boot · Vite extensions · router/layout · aliases · Yarn · when to skip examples.

## Detect the line first

Read `@quasar/app-vite` in `package.json`: v3 (stable since 3.0.1, 2026-07-07) and v2 (maintenance) differ in imports, config extensions, env, aliases. Split: `80-upstream-deltas-and-live-checks.md`; migration: `10-v2-to-v3-migration.md`. New apps use v3; unmigrated repos keep v2 shapes.

```text
@quasar/app-vite ^3.0.1 -> #q-app, build.env.folder, @/
@quasar/app-vite ^2.6.2 -> #q-app/wrappers, build.envFolder, src/
```

✅ Use the detected line. ❌ Never guess, mix line keys, or hand one line the other's shape.

## `quasar.config`

Prefer `defineConfig(ctx => ...)`, with `ctx.mode.*`, `ctx.dev`, `ctx.prod` inside one config—not duplicated objects.

v2:

```js
import { defineConfig } from '#q-app/wrappers'

export default defineConfig((ctx) => ({
  boot: ['axios', ctx.mode.pwa ? 'pwa-update' : ''].filter(Boolean),
  build: {
    envFolder: 'env',
    envFiles: ['.env', '.env.local']
  }
}))
```

v3 (`.js`/`.ts` only):

```js
import { defineConfig } from '#q-app'

export default defineConfig((ctx) => ({
  boot: ['axios', ctx.mode.pwa ? 'pwa-update' : ''].filter(Boolean),
  build: {
    vueOptionsAPI: false, // default; true only when Options API is used
    env: { folder: 'env', file: ['.env', '.env.local'] }
  }
}))
```

❌ On v3, no `.cjs`/`.mjs`; never mix v2 `envFolder/envFiles` with v3 `build.env.*`.

Search: `defineConfig`, `#q-app`, `ctx.mode`, `ctx.dev`, `ctx.prod`, `build.env.folder`, `envFolder`.

## Env: v2 vs v3

v2 flat files plus injected constants:

```js
build: {
  envFolder: 'env',
  envFiles: ['.env', '.env.local'],
  env: { FEATURE_X: ctx.prod ? 'on' : 'off' } // process.env.FEATURE_X
}
```

v3 nested env with client-prefix boundary:

```js
build: {
  env: {
    folder: 'env',
    file: ['.env', '.env.local'],
    clientPrefix: 'QCLI_' // only QCLI_* reaches client; this is the default
  },
  define: {
    __BUILD_TS__: Date.now(), // numbers auto-stringify
    __APP_VERSION__: JSON.stringify('1.0.0') // wrap genuine string literals
  },
  defineEnv: { FEATURE_X: ctx.prod ? 'on' : 'off' } // always stringifies -> import.meta.env.FEATURE_X
}
```

```js
// v3
if (import.meta.env.QUASAR_MODE === 'ssr') { /* ... */ }
// v2
if (process.env.MODE === 'ssr') { /* ... */ }
```

❌ Never use `'QUASAR_'` as v3 client prefix (framework collision), or `process.env.MODE` in v3 source.

❌ `define: { __BUILD_ID__: JSON.stringify(String(Date.now())) }` double-stringifies a number and emits a quoted string. Use `define: { __BUILD_ID__: Date.now() }`; wrap only real string literals. In v3, `build.rawDefine` became `build.define`, while v2 `build.env` injection became `build.defineEnv`.

Search: `build.env.clientPrefix`, `defineEnv`, `import.meta.env.QUASAR_`, `dotenv`, `rawDefine`, `build.define stringify`.

## Boot registration and function

Boot files are pre-mount startup wiring. Use `{ path, server, client }` for side scope; keep auth headers, SSR request state, and sensitive redirects server-side.

```js
boot: [
  'axios',
  { path: 'analytics', server: false },
  { path: 'ssr-auth', client: false }
]
```

v2; return immediately after redirect:

```js
import { defineBoot } from '#q-app/wrappers'

export default defineBoot(({ app, router, store, ssrContext, redirect }) => {
  if (ssrContext) { /* server bootstrap */ }
  if (shouldRedirect) {
    redirect({ path: '/login' })
    return
  }
})
```

v3; same rule, with `urlPath`/`publicPath`:

```js
import { defineBoot } from '#q-app'

export default defineBoot(({ app, router, store, ssrContext, urlPath, publicPath, redirect }) => {
  if (!isAuthorized && !urlPath.startsWith('/login')) {
    redirect({ path: '/login' })
    return
  }
})
```

❌ Never continue after `redirect()`, throw to redirect, or manually prefix a string with `publicPath`; pass a router location or absolute URL and return.

Search: `defineBoot`, `ssrContext`, `urlPath`, `publicPath`, `redirect path`, `boot path server false`.

## `extendViteConf` vs `vitePlugins`

Use `build.vitePlugins` for simple registration; use `build.extendViteConf` for client/server/mode logic or config merging. `extendViteConf` may mutate or return a merge object.

```js
build: {
  extendViteConf(viteConf, { isServer, isClient }) {
    return { resolve: { dedupe: ['vue', 'quasar'] } }
  },
  vitePlugins: [
    ['some-plugin', { /* options */ }, { server: false }],
    ['other-plugin', { /* options */ }, { client: false }]
  ]
}
```

❌ Never replace `viteConf.resolve.alias`; merge or use `build.alias`. Vite 8 removed object-form `manualChunks`; see `70-guardrails-a11y-performance-monorepo.md`.

Search: `extendViteConf`, `vitePlugins`, `isServer`, `isClient`, `dedupe`, `build.alias`.

## Router/layout ownership

Layouts own `<router-view />`; pages own `<q-page>`. Choose layouts by route, not conditional page shells. Pair `61-component-usage-atlas.md` for `QLayout`, `QDrawer`, `QPageContainer`.

```js
const routes = [{
  path: '/',
  component: () => import('layouts/MainLayout.vue'),
  children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
}]
```

❌ Do not render competing layout shells inside one page for states the URL should own.

Search: `routing with layouts and pages`, `router-view`, `children routes`, `layout route shell`.

## Aliases

```js
// v2 legacy aliases
import MyWidget from 'components/MyWidget.vue'
import { useUserStore } from 'stores/user'

// v3 sole @/ alias -> /src
import MyWidget from '@/components/MyWidget.vue'
import { useUserStore } from '@/stores/user'
```

❌ No legacy aliases in v3; no `@/` in v2 unless the repo defines it.

Search: `@/ alias`, `path alias`, `boot/`, `stores/`, `@/../`.

## Yarn-first workflow

In Yarn repos, use existing Yarn dev/build/test scripts. Use raw `quasar ...` only when the repo intentionally does or the user asks.

✅ `yarn build` or documented script. ❌ Never switch to `bun install`/`pnpm dev` merely because upstream supports them.

Search: `yarn.lock`, `yarn workspace`, `yarn dev`, `quasar command through yarn`.

## Skip examples for

Generic Vite/Vue Router explanations, obvious non-Quasar one-liners, or broad upgrade notes owned by `80-upstream-deltas-and-live-checks.md`.

Examples stay intentionally small to prevent shape mistakes, not replace official docs. Pair with `31-ssr-pwa-and-security.md` whenever boot/routing affects SSR, auth, or hydration.
