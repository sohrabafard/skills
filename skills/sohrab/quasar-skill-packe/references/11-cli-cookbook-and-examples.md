# CLI Cookbook and Examples

Use this file when the agent already knows the topic but needs the exact Quasar-shaped wiring for `quasar.config`, boot files, routing bootstrap, or Vite extension points.

Only load this file when example shape matters. Do not load it for purely conceptual Quasar questions.

## Why this file exists

The model usually understands Vite, Vue Router, and app bootstrap concepts. It is still worth giving examples when:

- Quasar wraps the API in a specific function shape
- server/client mode selection is easy to get subtly wrong
- boot-file registration, redirect behavior, or Vite extension points need exact syntax
- a bad example would create SSR drift, broken startup order, or hard-to-debug config mistakes

## High-value playbooks

### `quasar.config` base shape

- Prefer `defineConfig(ctx => ({ ... }))`.
- Keep mode-specific branching inside the config function instead of duplicating whole objects.
- Use this when the task is about `boot`, `build`, `ssr`, `pwa`, aliases, env files, or plugin wiring.

```js
import { defineConfig } from '#q-app/wrappers'

export default defineConfig((ctx) => ({
  boot: [
    'axios',
    ctx.mode.pwa ? 'pwa-update' : ''
  ].filter(Boolean),

  build: {
    envFolder: 'env',
    envFiles: ['.env', '.env.local']
  }
}))
```

- Good search terms:
  - `defineConfig ctx`, `ctx.mode`, `ctx.dev`, `ctx.prod`, `envFolder`, `envFiles`

### Boot file registration and mode targeting

- Prefer boot files for startup wiring that should happen before the root app mounts.
- Use boot entries with `{ path, server, client }` when the same boot file should be scoped to one side only.
- Keep auth headers, SSR-only request state, and sensitive redirects on the server side.

```js
boot: [
  'axios',
  {
    server: false,
    path: 'analytics'
  },
  {
    client: false,
    path: 'ssr-auth'
  }
]
```

- Good search terms:
  - `boot path server false`, `boot path client false`, `boot order`, `startup code`

### Boot file function shape

- Prefer `defineBoot(({ app, router, store, ssrContext, redirect }) => { ... })`.
- `ssrContext` only exists on the server.
- `redirect()` should receive a router location or absolute URL, not a manually prefixed `publicPath`.

```js
import { defineBoot } from '#q-app/wrappers'

export default defineBoot(({ app, router, store, ssrContext, redirect }) => {
  if (ssrContext) {
    // server-only bootstrap work
  }

  const shouldRedirect = false

  if (shouldRedirect) {
    redirect({ path: '/login' })
  }
})
```

- Good search terms:
  - `defineBoot`, `ssrContext`, `redirect path`, `router boot`, `store boot`

### `extendViteConf` vs `vitePlugins`

- Prefer `build.vitePlugins` for straightforward plugin registration.
- Prefer `build.extendViteConf` when the plugin application depends on client/server or mode-specific logic, or when you need to merge config rather than just register a plugin.
- Prefer returning an override object when possible; mutate directly only when necessary.

```js
build: {
  extendViteConf (viteConf, { isServer, isClient }) {
    return {
      resolve: {
        dedupe: ['vue', 'quasar']
      }
    }
  }
}
```

```js
build: {
  vitePlugins: [
    ['some-plugin', { /* options */ }, { server: false }],
    ['other-plugin', { /* options */ }, { client: false }]
  ]
}
```

- Good search terms:
  - `extendViteConf`, `vitePlugins`, `isServer`, `isClient`, `dedupe`, `mode filter`

### Router/layout ownership

- Prefer the layout file to own `<router-view />` and the page file to own `<q-page>`.
- Prefer route-driven layout selection over conditionally swapping layout shells inside page components.
- Pair with `41-component-usage-atlas.md` when the issue is really about `QLayout`, `QDrawer`, or `QPageContainer`.

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

- Good search terms:
  - `routing with layouts and pages`, `router-view`, `children routes`, `layout route shell`

## What usually does NOT need examples

- Generic descriptions of what Vite or Vue Router are
- obvious one-line config explanations with no Quasar-specific shape
- broad upgrade notes that are better handled in `70-upstream-deltas-and-live-checks.md`

## Notes

- Examples in this file are intentionally small. They exist to prevent shape mistakes, not to replace the Quasar docs.
- Pair this file with `20-ssr-pwa-and-security.md` whenever boot or routing logic can affect SSR, auth, or hydration.
