# Quasar app-vite v2 production + v3-ready playbook

Use for Alaa Quasar CLI + Vite repos still on v2 maintenance. Since v3.0.1 (2026-07-07), v3 is stable; readiness notes here are the worklist for a dedicated `10-v2-to-v3-migration.md` migration.

## Contents

Compatibility · packages · config · aliases · env · boot · routing/state · components/assets/styles · validation.

## 0. Compatibility and implementation

When v2 runtime and v3 readiness conflict, production correctness wins: use installed-line syntax; reduce future surface instead of applying v3-only code; record unsafe deferrals in docs/plans; keep abstractions small, testable, tree-shakable.

```ts
if (process.env.CLIENT) { /* browser-only */ }
// V3 migration: use import.meta.env.QUASAR_CLIENT.
```

Never use the uninjected v3 form in v2:

```ts
if (import.meta.env.QUASAR_CLIENT) { /* may break v2 */ }
```

Rules:

- Prefer TS only when the repo does; never convert JS without scope. Preserve lint/format.
- Match wrapper to major: v2 `#q-app/wrappers`, v3 `#q-app`.
- Keep modes in `src-pwa/`, `src-ssr/`, `src-capacitor/`, `src-electron/`, `src-bex/`.
- Boot files own init/plugin/cross-cutting wiring, not business logic. For current/potential SSR, prefer request-scoped API-client factories over mutable globals.
- Isolate SW from main thread; prefer behavior tests to implementation snapshots.
- Preserve architecture; make minimal, clean, validated changes—no broad rewrites.

## 1. Packages

Existing production stays on installed v2 unless migration is explicit. Upgrade within v2 only after release-note review and validation.

```bash
cat package.json
pnpm why @quasar/app-vite || yarn why @quasar/app-vite || npm ls @quasar/app-vite
quasar info || pnpm quasar info || npx quasar info
```

Quasar CLI app—correct:

```json
{ "devDependencies": { "@quasar/app-vite": "^2.6.2" } }
```

Not a CLI replacement—wrong unless this is plain Vue/Vite:

```json
{ "devDependencies": { "@quasar/vite-plugin": "latest" } }
```

`@quasar/vite-plugin` embeds Quasar in ordinary Vite; it does not replace app CLI.

## 2. `quasar.config`

Quasar CLI owns Vite; do not add `vite.config.ts` unless this is not a CLI app.

```ts
// correct v2: quasar.config.ts
import { defineConfig } from '#q-app/wrappers'

export default defineConfig(() => ({
  build: { extendViteConf(viteConf) { /* minimal Vite change */ } }
}))
```

```ts
// wrong in Quasar CLI: vite.config.ts
export default defineConfig({ plugins: [vue(), quasar()] })
```

Migration may change the import to `#q-app`; never do so on v2 unless installed support and validation prove it.

## 3. Aliases

v2 commonly has `src`, `app`, `components`, `layouts`, `pages`, `assets`, `boot`, `stores`. Prefer `@/` for new imports only when already supported or safely added in v2:

```ts
import MainLayout from '@/layouts/MainLayout.vue'
import LoginPage from '@/pages/auth/LoginPage.vue'
import { useUserStore } from '@/stores/user'
```

Avoid adding legacy imports:

```ts
import MainLayout from 'layouts/MainLayout.vue'
import LoginPage from 'pages/auth/LoginPage.vue'
import { useUserStore } from 'stores/user'
```

Large v2 repos may keep old aliases temporarily; mark migration debt and add no more.

## 4. Compile-time env

On v2, use direct static access:

```ts
if (process.env.PROD) { /* production */ }
if (process.env.CLIENT) { /* browser */ }
```

Never destructure, dynamically index, or log the object; replacements/tree-shaking/runtime can fail:

```ts
const { PROD } = process.env
const key = 'PROD'; process.env[key]
console.log(process.env)
```

Migration target: Quasar constants move to `import.meta.env.QUASAR_*`.

```ts
if (import.meta.env.QUASAR_PROD) { /* production */ }
if (import.meta.env.QUASAR_CLIENT) { /* browser */ }
```

Client env is public: never include API secrets, service credentials, private tokens, signing keys.

```env
# correct
QCLI_PUBLIC_API_BASE_URL=https://api.example.com
# wrong
QCLI_STRIPE_SECRET_KEY=sk_live_...
QCLI_DB_PASSWORD=...
```

Git-ignore real `.env`; maintain `.env.example`/`.env.template` with empty/dummy values.

## 5. Boot files

Use for plugin registration, API wiring, i18n, router guards, Quasar plugin init. Avoid top-level user fetches, per-request singleton state, SSR browser APIs, and unrelated business logic.

```ts
// v2 src/boot/api.ts
import { defineBoot } from '#q-app/wrappers'
import { createApiClient } from '@/services/api/createApiClient'

export default defineBoot(({ app, ssrContext }) => {
  app.config.globalProperties.$api = createApiClient({ ssrContext })
})
```

v2 uses `#q-app/wrappers`, not legacy `quasar/wrappers`; migration uses `#q-app`, never early. `22-cli-cookbook-and-examples.md` documents `app`, `router`, `store`, `ssrContext`, `redirect`, plus v3 `urlPath`/`publicPath`.

## 6. Routing and state

Lazy-load traditional layouts/pages unless local convention differs:

```ts
const routes = [{
  path: '/',
  component: () => import('@/layouts/MainLayout.vue'),
  children: [{ path: '', component: () => import('@/pages/IndexPage.vue') }]
}]
```

Do not introduce filename routing in production v2 unless explicit and installed versions support it; evaluate during v3 migration.

Prefer Pinia. Keep user/request state in store instances; SSR app/store/router must be per request; never read browser storage during store import.

```ts
// wrong: leaks across SSR requests
let currentUser: User | null = null

// correct
export const useUserStore = defineStore('user', {
  state: () => ({ currentUser: null as User | null })
})
```

## 7. Components, assets, styles

- New code uses Composition API unless Options-heavy consistency requires otherwise; components present, composables/stores/services orchestrate.
- Centralize mode checks where compile-time safe; use `q-page`, `q-layout`, `q-form`, `q-table` idiomatically while keeping business components independent where practical.
- When supported, prefer `<img src="~@/assets/logo.svg" alt="Alaa" />`; avoid new `~assets/...`.
- Component-local concerns stay scoped/CSS-variable/Quasar-Sass-based per convention, not global CSS.

## 8. Validation

```bash
<pm> run lint
<pm> run typecheck
<pm> run test:unit
<pm> run build
```

When relevant modes exist:

```bash
<pm> quasar build -m pwa
<pm> quasar build -m ssr
<pm> quasar build -m capacitor -T android
```

When constrained, run only relevant commands and state exactly what was skipped.
