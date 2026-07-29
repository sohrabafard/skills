# app-vite v2 maintenance playbook

You are about to patch a repository whose `package.json` declares `@quasar/app-vite@^2` and that is **not** being migrated in this change. Production correctness on the installed line wins over v3 readiness. When a migration is actually scheduled, the file is `references/10-v2-to-v3-migration.md`; the delta set is `references/80-upstream-deltas-and-live-checks.md` §4.

## 0. Posture

Use installed-line syntax. Reduce future migration surface instead of applying v3-only code. Record every deferral in the plan or the repository's docs. Keep abstractions small, testable, and tree-shakable. Preserve the existing architecture; make minimal, clean, validated changes and no broad rewrites.

```ts
if (process.env.CLIENT) { /* browser-only */ }
// V3 migration: this becomes import.meta.env.QUASAR_CLIENT.
```

Never write the uninjected v3 form into a v2 repository:

```ts
if (import.meta.env.QUASAR_CLIENT) { /* undefined on v2 */ }
```

- Use TypeScript only where the repository already does; never convert a JavaScript file without an agreed scope. Preserve lint and format configuration.
- Match the wrapper to the major: v2 is `#q-app/wrappers`, and it is not the older `quasar/wrappers`.
- Keep mode code in `src-pwa/`, `src-ssr/`, `src-capacitor/`, `src-electron/`, `src-bex/`.
- Boot files own initialisation, plugin registration, and cross-cutting wiring — not business logic. Where SSR exists or is planned, use request-scoped API-client factories rather than module globals.
- Keep the service worker isolated from the main thread; prefer behaviour tests to implementation snapshots.

## 1. Packages

Existing production stays on the installed v2 release unless a migration is explicit. Upgrade within v2 only after reading the release notes and validating.

```bash
cat package.json
pnpm why @quasar/app-vite || yarn why @quasar/app-vite || npm ls @quasar/app-vite
quasar info || pnpm quasar info
```

A Quasar CLI app declares the CLI:

```json
{ "devDependencies": { "@quasar/app-vite": "^2.6.2" } }
```

`@quasar/vite-plugin` embeds Quasar in an ordinary Vite app. It is not a CLI replacement, and finding it in a CLI app is a finding, not a style preference — see `references/13-examples-review-style.md` §1.

## 2. `quasar.config`

The Quasar CLI owns Vite. Do not add a `vite.config.ts` to a CLI app.

```ts
// correct v2: quasar.config.ts
import { defineConfig } from '#q-app/wrappers'

export default defineConfig(() => ({
  build: { extendViteConf (viteConf) { /* minimal Vite change */ } }
}))
```

```ts
// wrong in a Quasar CLI app: vite.config.ts
export default defineConfig({ plugins: [vue(), quasar()] })
```

A migration changes this import to `#q-app`. Do not make that change on v2.

## 3. Aliases

A v2 repository commonly has `src`, `app`, `components`, `layouts`, `pages`, `assets`, `boot`, `stores`.

**Use `@/` for a new import only if `quasar.config` already declares the `@` alias. Do not add that alias during an unrelated patch.**

```ts
// where @/ already exists
import MainLayout from '@/layouts/MainLayout.vue'
import { useUserStore } from '@/stores/user'
```

```ts
// avoid adding more legacy imports
import MainLayout from 'layouts/MainLayout.vue'
```

A large v2 repository may keep its old aliases; record them as migration debt in the plan and add no new ones.

## 4. Compile-time env

On v2, read `process.env` directly and statically:

```ts
if (process.env.PROD) { /* production */ }
if (process.env.CLIENT) { /* browser */ }
```

Never destructure it, index it with a computed key, or log the whole object — build-time replacement rewrites literal member reads only, so each of these resolves to `undefined` in a production build:

```ts
const { PROD } = process.env
const key = 'PROD'; process.env[key]
console.log(process.env)
```

**Client env is public.** No API secret, service credential, private token, or signing key belongs in it, on either line.

```env
# correct
QCLI_PUBLIC_API_BASE_URL=https://api.example.com
# wrong
QCLI_STRIPE_SECRET_KEY=sk_live_...
```

Git-ignore the real `.env`; maintain a committed `.env.example` with every key present and every value empty or dummy, so a missing variable is a review finding rather than a runtime surprise. The v3 env contract is `references/20-v3-config-and-features.md`.

## 5. Boot files

Use them for plugin registration, API wiring, i18n, router guards, and Quasar plugin initialisation. Avoid top-level user fetches, per-request singleton state, browser APIs on SSR paths, and unrelated business logic.

```ts
// v2 src/boot/api.ts
import { defineBoot } from '#q-app/wrappers'
import { createApiClient } from '@/services/api/createApiClient'

export default defineBoot(({ app, ssrContext }) => {
  app.config.globalProperties.$api = createApiClient({ ssrContext })
})
```

The full boot parameter set, on both lines, is `references/22-cli-cookbook-and-examples.md`.

## 6. Routing and state

Lazy-load layouts and pages unless local convention differs. Do not introduce filename-based routing into production v2; evaluate it during the migration.

Prefer Pinia. Keep user and request state inside store instances; on SSR the app, store, and router are per request; never read browser storage while a store module is being imported.

```ts
// wrong: leaks across SSR requests
let currentUser: User | null = null

// correct
export const useUserStore = defineStore('user', {
  state: () => ({ currentUser: null as User | null })
})
```

## 7. Components, assets, styles

- New code uses the Composition API unless Options-heavy consistency requires otherwise. Components present; composables, stores, and services orchestrate. Code shape is `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`).
- Centralize mode checks where compile-time replacement is safe.
- Where supported, prefer `<img src="~@/assets/logo.svg" alt="..." />`; add no new `~assets/...` imports.
- Component-local styling stays scoped, or uses CSS variables and Quasar Sass variables per repository convention, rather than global CSS.

## 8. Validation

```bash
<pm> run lint
<pm> run typecheck
<pm> run test:unit
<pm> run build
```

When the modes exist:

```bash
<pm> quasar build -m pwa
<pm> quasar build -m ssr
<pm> quasar build -m capacitor -T android
```

When the environment prevents a command, run the ones you can and state exactly which you skipped and why.

Search: `app-vite v2`, `#q-app/wrappers`, `process.env`, `legacy alias`, `env.example`, `boot file v2`, `pinia store per request`, `maintenance patch`.
