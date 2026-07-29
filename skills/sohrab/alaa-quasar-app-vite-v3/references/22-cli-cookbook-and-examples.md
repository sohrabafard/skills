# CLI cookbook — exact shapes

You are about to write the literal text of a `quasar.config`, a boot file, a router bootstrap, an env block, a Vite extension, or a `register-sw` file. Load this only when the exact shape matters; use the conceptual files otherwise. It exists to prevent wrapper, side-scoping, startup-order, SSR, and v2/v3 shape mistakes.

Detect the installed line first — `references/80-upstream-deltas-and-live-checks.md` §3.

✅ Use the detected line's shape. ❌ Never guess, mix keys from two lines, or hand one line the other's shape.

## `quasar.config`

Prefer one `defineConfig(ctx => ...)` using `ctx.mode.*`, `ctx.dev`, and `ctx.prod`, not duplicated objects.

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

v3 (`.js` or `.ts` only):

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

❌ On v3 there is no `.cjs` or `.mjs` config, and v2 `envFolder`/`envFiles` never mix with v3 `build.env.*`.

Search: `defineConfig`, `#q-app`, `ctx.mode`, `ctx.dev`, `ctx.prod`, `build.env.folder`, `envFolder`.

## Env: v2 versus v3

v2 — flat files plus injected constants:

```js
build: {
  envFolder: 'env',
  envFiles: ['.env', '.env.local'],
  env: { FEATURE_X: ctx.prod ? 'on' : 'off' } // process.env.FEATURE_X
}
```

v3 — nested env with the client-prefix boundary:

```js
build: {
  env: {
    folder: 'env',
    file: ['.env', '.env.local'],
    clientPrefix: 'QCLI_' // only QCLI_* reaches the client; this is the default
  },
  define: {
    __BUILD_TS__: Date.now(),                    // numbers auto-stringify
    __APP_VERSION__: JSON.stringify('1.0.0')     // wrap genuine string literals
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

❌ Never use `'QUASAR_'` as the v3 client prefix — it collides with the framework's own constants — and never read `process.env.MODE` in v3 source.

❌ `define: { __BUILD_ID__: JSON.stringify(String(Date.now())) }` double-stringifies a number and emits a quoted string. Use `define: { __BUILD_ID__: Date.now() }`; wrap only real string literals. The semantics are `references/20-v3-config-and-features.md`.

Search: `build.env.clientPrefix`, `defineEnv`, `import.meta.env.QUASAR_`, `dotenv`, `rawDefine`, `build.define stringify`.

## Boot registration and boot function

Boot files are pre-mount startup wiring. Use `{ path, server, client }` to scope a side, and keep auth headers, SSR request state, and sensitive redirects server-side.

```js
boot: [
  'axios',
  { path: 'analytics', server: false },
  { path: 'ssr-auth', client: false }
]
```

v2 — return immediately after `redirect()`:

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

v3 — same rule, with `urlPath` and `publicPath`:

```js
import { defineBoot } from '#q-app'

export default defineBoot(({ app, router, store, ssrContext, urlPath, publicPath, redirect }) => {
  if (!isAuthorized && !urlPath.startsWith('/login')) {
    redirect({ path: '/login' })
    return
  }
})
```

❌ Never continue after `redirect()`, never throw to redirect, and never hand-prefix a string with `publicPath`; pass a router location or an absolute URL and return.

Request-scoped API client, wired from boot — the shape that keeps one user's token out of another user's SSR response:

```js
import { defineBoot } from '#q-app'
import { createApiClient } from '@/services/api/createApiClient'

export default defineBoot(({ app, ssrContext }) => {
  const api = createApiClient({ cookie: ssrContext?.req?.headers?.cookie })
  app.provide('api', api)
})
```

Search: `defineBoot`, `ssrContext`, `urlPath`, `publicPath`, `redirect path`, `boot path server false`, `per-request api client`.

## `register-sw`

Main-thread registration stays directly under `src-pwa/`. The update UX lives here, never in `custom-sw`.

```ts
// src-pwa/register-sw.ts (v2)
import { register } from 'register-service-worker'
register(process.env.SERVICE_WORKER_FILE, {
  updated (registration) { /* surface the update prompt through the app store or notify layer */ },
  offline () { /* mark the app offline in the store */ }
})
```

```ts
// src-pwa/register-sw.ts (v3)
import { register } from 'register-service-worker'
register(import.meta.env.QUASAR_SERVICE_WORKER_FILE, {
  updated (registration) { /* ... */ },
  offline () { /* ... */ }
})
```

❌ Never call `window.location.reload()` or touch the DOM inside `custom-sw`; it runs in a worker with no `window` and no `document`. The reload-once guard and the `SKIP_WAITING` message belong here and in `custom-sw` respectively — `references/30-service-worker-excellence.md` §4.

Search: `register-sw`, `register-service-worker`, `SERVICE_WORKER_FILE`, `updated hook`, `offline hook`.

## `extendViteConf` versus `vitePlugins`

Use `build.vitePlugins` for simple registration; use `build.extendViteConf` for client/server/mode logic or config merging. `extendViteConf` may mutate or return a merge object.

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

❌ Never assign to `viteConf.resolve.alias`; merge, or use `build.alias`. Vite 8 removed object-form `manualChunks` — the replacement pair is `references/70-guardrails-a11y-performance-monorepo.md`.

Search: `extendViteConf`, `vitePlugins`, `isServer`, `isClient`, `dedupe`, `build.alias`.

## Router bootstrap

```js
const routes = [{
  path: '/',
  component: () => import('@/layouts/MainLayout.vue'),   // v3 alias; v2 uses 'layouts/MainLayout.vue'
  children: [{ path: '', component: () => import('@/pages/IndexPage.vue') }]
}]
```

Lazy-loaded route components are the default. Layout and page ownership — which component holds `QPageContainer` and `<router-view />` — is `references/62-layout-patterns-and-examples.md`.

Search: `routes`, `children routes`, `lazy route component`, `dynamic import`.

## Aliases

```js
// v2 legacy aliases
import MyWidget from 'components/MyWidget.vue'
import { useUserStore } from 'stores/user'

// v3 sole @/ alias -> /src
import MyWidget from '@/components/MyWidget.vue'
import { useUserStore } from '@/stores/user'
```

❌ No legacy alias in v3; no `@/` in v2 unless the repository already defines it.

Search: `@/ alias`, `path alias`, `boot/`, `stores/`, `@/../`.

## Yarn-first workflow

In a Yarn repository use the existing Yarn dev, build, and test scripts. Use a raw `quasar ...` command only when the repository already does or the user asks.

✅ `yarn build`, or the documented script. ❌ Never switch to `bun install` or `pnpm dev` because upstream supports them.

Search: `yarn.lock`, `yarn workspace`, `yarn dev`, `quasar command through yarn`.

## Skip this file for

Generic Vite or Vue Router explanations, obvious non-Quasar one-liners, and version or upgrade notes owned by `references/80-upstream-deltas-and-live-checks.md`. The examples here are deliberately small: they prevent shape mistakes, they do not replace official docs. Pair with `references/31-ssr-pwa-and-security.md` whenever boot or routing affects SSR, auth, or hydration.
