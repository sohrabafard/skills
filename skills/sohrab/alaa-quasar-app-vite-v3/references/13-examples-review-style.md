# Review examples and anti-patterns

Use for concrete review comments and implementation decisions.

## Contents

CLI/plugin · versioning · aliases · env · SSR composable · boot · PWA cache · test reporting · final answer.

## 1. CLI vs Vite plugin

Correct:

> This has `quasar.config.ts` and `@quasar/app-vite`, so it is a Quasar CLI app. Configure Vite through `quasar.config.ts`; do not install `@quasar/vite-plugin` or create `vite.config.ts`.

Wrong:

> Install `@quasar/vite-plugin` and configure `vite.config.ts`.

## 2. Versioning

Correct:

> The repo is on app-vite v2. Keep this patch lockfile-compatible and note alias/env migration debt. v3 is stable, but schedule it separately via `10-v2-to-v3-migration.md`.

Wrong:

> v3 is stable, so I upgraded app-vite and vue-router in this patch.

That unrelated upgrade leaves imports, env, aliases, and mode folders untested.

## 3. Aliases

Correct new import when supported:

```ts
import UserAvatar from '@/components/user/UserAvatar.vue'
```

Acceptable for a small v2 patch lacking `@/`:

```ts
import UserAvatar from 'components/user/UserAvatar.vue'
```

Add:

```md
V3 readiness: migrate this alias to `@/components/...` in the dedicated alias migration.
```

Wrong where `@/` already exists:

```ts
import UserAvatar from 'components/user/UserAvatar.vue'
```

## 4. Env

```ts
// correct v2
if (process.env.SERVER) { /* server only */ }
// correct v3
if (import.meta.env.QUASAR_SERVER) { /* server only */ }
```

Wrong in build-time replacement systems:

```ts
const env = process.env
const isServer = env.SERVER
const key = 'SERVER'
if (process.env[key]) {}
```

## 5. SSR-safe composable

Wrong:

```ts
export function usePreferredTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
```

Correct:

```ts
import { onMounted, ref } from 'vue'

export function usePreferredTheme() {
  const theme = ref<'light' | 'dark'>('light')
  onMounted(() => {
    const stored = localStorage.getItem('theme')
    if (stored === 'dark' || stored === 'light') theme.value = stored
  })
  return { theme }
}
```

## 6. Boot boundary

Wrong:

```ts
// src/boot/user.ts
let token = localStorage.getItem('token')
export const api = axios.create({ headers: { Authorization: `Bearer ${token}` } })
```

Correct factory, then wire it in boot from client/server-safe token sources:

```ts
// src/services/api/createApiClient.ts
export function createApiClient(options: { token?: string }) {
  return axios.create({
    headers: options.token ? { Authorization: `Bearer ${options.token}` } : undefined
  })
}
```

## 7. PWA cache

Wrong:

```ts
// Cache all API requests offline
urlPattern: /\/api\//,
handler: 'CacheFirst'
```

Correct:

```ts
// Cache only public/static resources; explicitly exclude auth/payment/profile.
// Review API runtime caching endpoint by endpoint.
```

## 8. Test reporting

Correct:

> Added Vitest coverage for pure `normalizeCourseTitle`; Cypress is unnecessary because no user flow changed. `pnpm run test:unit` and `pnpm run typecheck` passed.

Wrong:

> No tests because this is small.

## 9. Codex/Claude final answer

Good:

```md
Done.

Changed:
- `src/services/api/createApiClient.ts`: moved API client creation into a factory.
- `src/boot/api.ts`: creates one client per app/request.

Why safe for app-vite v2:
- Preserves existing `process.env.CLIENT` usage.
- Does not touch dependencies or lockfile.

v3-readiness:
- New imports use `@/`.
- Remaining `process.env.*` guards are direct and easy to codemod during v3 migration.

Validation:
- `pnpm run typecheck`: passed
- `pnpm run test:unit`: passed
- `pnpm run build`: not run because ...
```

Bad:

> I refactored the code and it should be good now.
