# CLI Cookbook and Examples

Use this file when the agent already knows the topic but needs the exact Quasar-shaped wiring for `quasar.config`, boot files, routing bootstrap, env config, or Vite extension points.

Only load this file when example shape matters. Do not load it for purely conceptual Quasar questions.

## Table of contents

- Why this file exists
- Confirm the app-vite line before copying any example
- `quasar.config` base shape
- Env config (v2 vs v3)
- Boot file registration and function shape
- `extendViteConf` vs `vitePlugins`
- Router/layout ownership
- Path aliases (v2 vs v3)
- Yarn-first project workflow
- What usually does NOT need examples

## Why this file exists

The model usually understands Vite, Vue Router, and app bootstrap concepts. It is still worth giving examples when:

- Quasar wraps the API in a specific function shape
- server/client mode selection is easy to get subtly wrong
- boot-file registration, redirect behavior, or Vite extension points need exact syntax
- the v2 and v3 shapes differ and the wrong one will not run
- a bad example would create SSR drift, broken startup order, or hard-to-debug config mistakes

## Confirm the app-vite line before copying any example

The import path, config extensions, env keys, and aliases differ between `@quasar/app-vite` v2 (stable/production) and v3 (RC). Read `@quasar/app-vite` in `package.json` first. The split summary is in `70-upstream-deltas-and-live-checks.md`. For production, v2 is the default; treat v3 shapes as for repos already on the RC. For migration planning, v3-readiness, or the full upgrade playbook, use `$alaa-app-vite-quasar` — this file only carries the per-line code shapes.

✅ Do — pick the shape for the detected line.

```text
"package.json has @quasar/app-vite ^2.6.2 (stable) -> use `#q-app/wrappers`, build.envFolder, src/ alias."
"package.json has @quasar/app-vite ^3.0.0-rc.3 (RC) -> use `#q-app`, build.env.folder, @/ alias."
```

❌ Don't — emit a single shape from memory without checking, mix v2 and v3 keys in one config, or hand a production app v3 shapes when it is on stable v2.

## `quasar.config` base shape

- Prefer `defineConfig(ctx => ({ ... }))`.
- Keep mode-specific branching inside the config function instead of duplicating whole objects.
- Use `ctx.mode.*`, `ctx.dev`, `ctx.prod` instead of scattered branches.

✅ Do — v2 (`@quasar/app-vite` ^2, stable/production): import from `#q-app/wrappers`.

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

✅ Do — v3 (`@quasar/app-vite` ^3, RC): import from `#q-app`, `.js` or `.ts` file only.

```js
import { defineConfig } from '#q-app'

export default defineConfig((ctx) => ({
  boot: ['axios', ctx.mode.pwa ? 'pwa-update' : ''].filter(Boolean),
  build: {
    vueOptionsAPI: false, // v3 default; set true only if the app uses Options API
    env: {
      folder: 'env',
      file: ['.env', '.env.local']
    }
  }
}))
```

❌ Don't — use a `.cjs`/`.mjs` `quasar.config` on v3 (only `.js`/`.ts` are supported), and don't put `envFolder`/`envFiles` (v2) next to `build.env.*` (v3) in the same file.

- Good search terms:
  - `defineConfig`, `#q-app`, `ctx.mode`, `ctx.dev`, `ctx.prod`, `build.env.folder`, `envFolder`

## Env config (v2 vs v3)

The env surface changed shape in v3, including how client exposure is gated.

✅ Do — v2 (stable): point at env files with the flat keys, and use `build.env`/`build.rawDefine` for constants.

```js
build: {
  envFolder: 'env',
  envFiles: ['.env', '.env.local'],
  env: { FEATURE_X: ctx.prod ? 'on' : 'off' } // read as process.env.FEATURE_X
}
```

✅ Do — v3 (RC): nest under `build.env`, and expose client vars only through `clientPrefix`.

```js
build: {
  env: {
    folder: 'env',
    file: ['.env', '.env.local'],
    clientPrefix: 'QCLI_' // only QCLI_*-prefixed vars reach client code (default)
  },
  // define globals: non-string values are auto-stringified; wrap a string LITERAL yourself
  define: {
    __BUILD_TS__: Date.now(),                  // number -> Quasar JSON.stringifies it for you
    __APP_VERSION__: JSON.stringify('1.0.0')    // string literal -> wrap it (bare strings are raw expressions)
  },
  // sugar: always stringifies (even strings) and prefixes -> import.meta.env.FEATURE_X
  defineEnv: { FEATURE_X: ctx.prod ? 'on' : 'off' }
}
```

✅ Do — read Quasar constants by mode.

```js
// v3
if (import.meta.env.QUASAR_MODE === 'ssr') { /* ... */ }
// v2
if (process.env.MODE === 'ssr') { /* ... */ }
```

❌ Don't — keep `'QUASAR_'` as a client prefix in v3 (the docs recommend against it because it collides with framework constants), and don't read `process.env.MODE` in v3 source (it is `import.meta.env.QUASAR_MODE` there).

❌ Don't — double-stringify a `build.define` value. `define: { __BUILD_ID__: JSON.stringify(String(Date.now())) }` is wrong: `Date.now()` is a number, which Quasar already auto-`JSON.stringify`s, so wrapping it bakes in quotes and emits a string literal instead of a number. Pass the number bare (`__BUILD_ID__: Date.now()`); only wrap genuine string literals.

- Good search terms:
  - `build.env.clientPrefix`, `defineEnv`, `import.meta.env.QUASAR_`, `dotenv`, `rawDefine` (legacy), `build.define stringify`

## Boot file registration and function shape

- Prefer boot files for startup wiring that should happen before the root app mounts.
- Use boot entries with `{ path, server, client }` when a boot file should be scoped to one side only.
- Keep auth headers, SSR-only request state, and sensitive redirects on the server side.

✅ Do — register with side-scoping when needed (same shape in v2 and v3).

```js
boot: [
  'axios',
  { path: 'analytics', server: false }, // client-only
  { path: 'ssr-auth', client: false }   // server-only
]
```

✅ Do — v2 boot function (stable/production): import from `#q-app/wrappers`, and return immediately after `redirect()`.

```js
import { defineBoot } from '#q-app/wrappers'

export default defineBoot(({ app, router, store, ssrContext, redirect }) => {
  if (ssrContext) {
    // server-only bootstrap work
  }

  if (shouldRedirect) {
    redirect({ path: '/login' })
    return // return right after redirect()
  }
})
```

✅ Do — v3 boot function (RC): identical idea, but import from `#q-app`; `urlPath`/`publicPath` are also provided.

```js
import { defineBoot } from '#q-app'

export default defineBoot(({ app, router, store, ssrContext, urlPath, publicPath, redirect }) => {
  if (!isAuthorized && !urlPath.startsWith('/login')) {
    redirect({ path: '/login' })
    return
  }
})
```

❌ Don't — call `redirect()` and keep running, throw to redirect, or hand it a manually `publicPath`-prefixed string. Pass a router location or absolute URL and return.

- Good search terms:
  - `defineBoot`, `ssrContext`, `urlPath`, `publicPath`, `redirect path`, `boot path server false`

## `extendViteConf` vs `vitePlugins`

- Prefer `build.vitePlugins` for straightforward plugin registration.
- Prefer `build.extendViteConf` when plugin application depends on client/server or mode-specific logic, or when you need to merge config.
- `extendViteConf` may mutate the passed config object or return a new object to be merged; both work.

✅ Do — return an override (clean) or scope a plugin to one side.

```js
build: {
  extendViteConf (viteConf, { isServer, isClient }) {
    return { resolve: { dedupe: ['vue', 'quasar'] } }
  },
  vitePlugins: [
    ['some-plugin', { /* options */ }, { server: false }],
    ['other-plugin', { /* options */ }, { client: false }]
  ]
}
```

❌ Don't — replace `viteConf.resolve.alias` wholesale (it drops Quasar's own aliases); merge into it or use `build.alias` instead. On Vite 8, don't reach for the object form of `manualChunks` (removed) — see `60-guardrails-a11y-performance-monorepo.md`.

- Good search terms:
  - `extendViteConf`, `vitePlugins`, `isServer`, `isClient`, `dedupe`, `build.alias`

## Router/layout ownership

- Prefer the layout file to own `<router-view />` and the page file to own `<q-page>`.
- Prefer route-driven layout selection over conditionally swapping layout shells inside page components.
- Pair with `41-component-usage-atlas.md` when the issue is really about `QLayout`, `QDrawer`, or `QPageContainer`.

✅ Do — nest pages under a layout route.

```js
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  }
]
```

❌ Don't — render two different layout shells conditionally inside one page component to fake navigation states the URL should own.

- Good search terms:
  - `routing with layouts and pages`, `router-view`, `children routes`, `layout route shell`

## Path aliases (v2 vs v3)

✅ Do — v2 (stable): use the legacy aliases.

```js
import MyWidget from 'components/MyWidget.vue'
import { useUserStore } from 'stores/user'
```

✅ Do — v3 (RC): use the single `@/` alias (points to `/src`).

```js
import MyWidget from '@/components/MyWidget.vue'
import { useUserStore } from '@/stores/user'
```

❌ Don't — write `components/...` or `stores/...` imports in a v3 repo (those aliases were removed; use `@/components/...`, `@/stores/...`), or `@/...` in a v2 repo that does not define it.

- Good search terms:
  - `@/ alias`, `path alias`, `boot/`, `stores/`, `@/../`

## Yarn-first project workflow

- In Quasar repos that use Yarn, prefer existing Yarn scripts for dev, build, and test flows instead of improvising with another package manager.
- Use raw `quasar ...` commands only when the repo intentionally calls the CLI directly or the user explicitly wants that form.

✅ Do — `yarn build` (or the repo's documented script) in a Yarn repo.

❌ Don't — switch to `bun install` / `pnpm dev` just because upstream Quasar supports them.

- Good search terms:
  - `yarn.lock`, `yarn workspace`, `yarn dev`, `quasar command through yarn`

## What usually does NOT need examples

- Generic descriptions of what Vite or Vue Router are
- obvious one-line config explanations with no Quasar-specific shape
- broad upgrade notes that are better handled in `70-upstream-deltas-and-live-checks.md`

## Notes

- Examples in this file are intentionally small. They exist to prevent shape mistakes, not to replace the Quasar docs.
- Pair this file with `20-ssr-pwa-and-security.md` whenever boot or routing logic can affect SSR, auth, or hydration.
