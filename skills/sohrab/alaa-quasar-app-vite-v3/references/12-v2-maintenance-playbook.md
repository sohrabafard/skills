# Quasar app-vite v2 Production + v3-Ready Playbook

Use this reference when working on a Quasar CLI with Vite project for Alaa that is **still on the app-vite v2 maintenance line**. Since `3.0.1` (2026-07-07) v3 is the stable production line: the "v3 migration notes" this playbook teaches you to leave behind are no longer future hedges — they are the exact worklist for a migration scheduled via `10-v2-to-v3-migration.md`.

## 0. Compatibility policy and agent implementation rules

Some v3-ready changes conflict with a v2 runtime. When they conflict, **production correctness wins**.

- On app-vite v2, use syntax that actually works on that repo; prepare for v3 by reducing migration surface, not by prematurely applying v3-only syntax.
- Add a v3 migration note in docs/plans when a change cannot be made safely on v2.
- Keep new abstractions small, testable, and tree-shaking-friendly.

Correct for v2 production (and the v3 migration note to leave behind):

```ts
if (process.env.CLIENT) { /* browser-only */ }
// V3 migration note: becomes `import.meta.env.QUASAR_CLIENT` during the app-vite v3 migration.
```

Wrong on a v2 repo (the v3 form is not injected, so it can break production):

```ts
if (import.meta.env.QUASAR_CLIENT) { /* may break v2 */ }
```

Agent implementation rules:

- Prefer TypeScript if the repo uses it; do not convert a JS repo without explicit scope. Preserve existing lint/format conventions.
- Use the wrapper import that matches the installed app-vite major (`#q-app/wrappers` on v2, `#q-app` on v3).
- Keep mode-specific code in its official folder: PWA `src-pwa/`, SSR `src-ssr/`, Capacitor `src-capacitor/`, Electron `src-electron/`, BEX `src-bex/`.
- Boot files only for init/plugin wiring/cross-cutting services. Prefer per-request API-client factories over mutable global singletons when SSR exists or may exist.
- Keep service-worker code isolated from main-thread code. Prefer behavior-focused tests over implementation-detail snapshots.
- No broad rewrites: preserve local architecture; make minimal, clean, validated changes.

## 1. Package and dependency policy

### Production default

For existing production apps, stay on the installed `@quasar/app-vite` v2 line unless the user explicitly asks for migration. Prefer the latest patch/minor in the v2 line only after reading release notes and running validation.

Recommended check sequence:

```bash
cat package.json
pnpm why @quasar/app-vite || yarn why @quasar/app-vite || npm ls @quasar/app-vite
quasar info || pnpm quasar info || npx quasar info
```

### Do not confuse these packages

Correct inside Quasar CLI project:

```json
{
  "devDependencies": {
    "@quasar/app-vite": "^2.6.2"
  }
}
```

Wrong inside Quasar CLI project when the project is not plain Vue/Vite:

```json
{
  "devDependencies": {
    "@quasar/vite-plugin": "latest"
  }
}
```

`@quasar/vite-plugin` is for embedding Quasar into a normal Vite app. It is not a replacement for the app CLI package in a Quasar CLI project.

## 2. quasar.config rules

Quasar CLI owns the Vite config. Do not create `vite.config.ts` unless the repository is not a Quasar CLI app.

Correct:

```ts
// quasar.config.ts
import { defineConfig } from '#q-app/wrappers'

export default defineConfig((ctx) => ({
  build: {
    extendViteConf(viteConf) {
      // minimal Vite-level change here
    }
  }
}))
```

For app-vite v3 migration this import may become `#q-app`. Do not change it in a v2 repo unless the current installed app-vite version supports it and validation passes.

Wrong:

```ts
// vite.config.ts in a Quasar CLI app
export default defineConfig({
  plugins: [vue(), quasar()]
})
```

## 3. Alias policy

### v2 reality

Existing app-vite v2 projects often use Quasar folder aliases:

- `src`
- `app`
- `components`
- `layouts`
- `pages`
- `assets`
- `boot`
- `stores`

### v3-ready direction

For new source imports, prefer `@/` if supported by the repo or if safely added as an alias in v2:

```ts
import MainLayout from '@/layouts/MainLayout.vue'
import LoginPage from '@/pages/auth/LoginPage.vue'
import { useUserStore } from '@/stores/user'
```

Avoid new code with old aliases:

```ts
import MainLayout from 'layouts/MainLayout.vue'
import LoginPage from 'pages/auth/LoginPage.vue'
import { useUserStore } from 'stores/user'
```

### Temporary bridge

If v2 codebase is large, you may temporarily keep old aliases to avoid a big-bang migration. Mark this as migration debt and do not add more old-style imports.

## 4. Environment variables and compile-time constants

### v2-compatible rule

If the project is app-vite v2 and it already uses `process.env`, use direct static access only:

```ts
if (process.env.PROD) {
  // production-only logic
}

if (process.env.CLIENT) {
  // browser-only logic
}
```

Wrong in v2:

```ts
const { PROD } = process.env
const key = 'PROD'
process.env[key]
console.log(process.env)
```

These patterns are not statically replaceable and may break tree-shaking or runtime behavior.

### v3 migration target

During app-vite v3 migration, Quasar constants move to `import.meta.env.QUASAR_*`:

```ts
if (import.meta.env.QUASAR_PROD) {
  // production-only logic
}

if (import.meta.env.QUASAR_CLIENT) {
  // browser-only logic
}
```

Use the repository version to decide what to write today.

### Public/private env rule

Client-exposed env vars are public. Never place API secrets, service credentials, private tokens, or signing keys in client env.

Correct:

```env
QCLI_PUBLIC_API_BASE_URL=https://api.example.com
```

Wrong:

```env
QCLI_STRIPE_SECRET_KEY=sk_live_...
QCLI_DB_PASSWORD=...
```

Always keep real `.env` files out of git and maintain `.env.example` or `.env.template` with empty/dummy values.

## 5. Boot files

Use boot files for:

- registering plugins
- wiring API clients
- configuring i18n
- router guards
- Quasar plugin initialization

Avoid:

- fetching user-specific data at module top level
- storing per-request state in module singletons
- browser-only API access during SSR
- large unrelated business logic

Correct (app-vite v2 — the production line):

```ts
// src/boot/api.ts
import { defineBoot } from '#q-app/wrappers'
import { createApiClient } from '@/services/api/createApiClient'

export default defineBoot(({ app, ssrContext }) => {
  const api = createApiClient({ ssrContext })
  app.config.globalProperties.$api = api
})
```

In app-vite v2 the wrapper is `#q-app/wrappers` (not the legacy `quasar/wrappers`). During the v3 migration the import becomes `#q-app` — do not switch it on a v2 repo. The boot params (`app`, `router`, `store`, `ssrContext`, `redirect`, and in v3 also `urlPath`/`publicPath`) are documented in `22-cli-cookbook-and-examples.md`.

## 6. Routing and code-splitting

For traditional route files, lazy-load pages/layouts unless the repo's convention says otherwise:

```ts
const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('@/pages/IndexPage.vue') }
    ]
  }
]
```

Do not introduce filename-based routing in a production v2 app unless explicitly requested and supported by the installed versions. Treat filename-based routing as a v3 evaluation/migration topic.

## 7. Pinia/state policy

- Prefer Pinia for shared state.
- Store user/request-specific state in store instances, not module-level mutable variables.
- For SSR, ensure each request gets isolated app/store/router instances.
- Do not access browser storage at store module import time.

Wrong:

```ts
// module-level user data leaks across SSR requests
let currentUser: User | null = null
```

Correct:

```ts
export const useUserStore = defineStore('user', {
  state: () => ({ currentUser: null as User | null })
})
```

## 8. Components and composables

- Use Composition API for new code unless the repo is Options API-heavy and consistency requires otherwise.
- Keep components focused: presentation in components, data orchestration in composables/stores/services.
- Avoid hardcoding Quasar mode checks throughout UI; centralize where it remains compile-time safe.
- Use Quasar components idiomatically (`q-page`, `q-layout`, `q-form`, `q-table`) but keep business components independent where possible.

## 9. Assets and styles

For v3-ready imports, prefer `@/assets` paths when the repo supports it:

```vue
<template>
  <img src="~@/assets/logo.svg" alt="Alaa" />
</template>
```

Avoid new `~assets/...` references when preparing for v3.

Do not add global CSS for component-local concerns. Use scoped styles, CSS variables, or Quasar Sass variables according to project convention.

## 10. Validation checklist

Minimum validation after code changes:

```bash
<pm> run lint
<pm> run typecheck
<pm> run test:unit
<pm> run build
```

If modes exist:

```bash
<pm> quasar build -m pwa
<pm> quasar build -m ssr
<pm> quasar build -m capacitor -T android
```

Run only relevant commands when time/tooling is limited, and report exactly what was not run.
