# Examples and Anti-patterns

Use these examples to guide concrete code review comments and implementation decisions.

## 1. Quasar CLI vs Vite plugin

Correct recommendation:

> This is a Quasar CLI app because it has `quasar.config.ts` and `@quasar/app-vite`. We should configure Vite through `quasar.config.ts`, not by installing `@quasar/vite-plugin` or creating `vite.config.ts`.

Wrong recommendation:

> Install `@quasar/vite-plugin` and configure it in `vite.config.ts`.

## 2. Version recommendation

Correct:

> The repo is on `@quasar/app-vite` v2. This change stays compatible with the current lockfile, and I will add a migration note for alias/env changes. v3 is the stable production line now — worth scheduling the migration as its own task via `10-v2-to-v3-migration.md`.

Wrong:

> v3 is stable now, so I upgraded `@quasar/app-vite` and `vue-router` in the same patch.

(The migration touches imports, env, aliases, and mode folders across the app; bundling it into an unrelated patch ships untested breaking changes.)

## 3. Alias migration

Correct new import when supported:

```ts
import UserAvatar from '@/components/user/UserAvatar.vue'
```

Acceptable temporary v2 compatibility when repo has not adopted `@/` and scope is small:

```ts
import UserAvatar from 'components/user/UserAvatar.vue'
```

But add note:

```md
V3 readiness: this old Quasar alias should be migrated to `@/components/...` in the dedicated alias migration.
```

Wrong:

```ts
// New code in a repo that already supports @/
import UserAvatar from 'components/user/UserAvatar.vue'
```

## 4. Env usage

Correct v2 direct access:

```ts
if (process.env.SERVER) {
  // server only
}
```

Correct v3 target:

```ts
if (import.meta.env.QUASAR_SERVER) {
  // server only
}
```

Wrong in any build-time replacement system:

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
    if (stored === 'dark' || stored === 'light') {
      theme.value = stored
    }
  })

  return { theme }
}
```

## 6. Boot file boundaries

Wrong:

```ts
// src/boot/user.ts
let token = localStorage.getItem('token')
export const api = axios.create({ headers: { Authorization: `Bearer ${token}` } })
```

Correct:

```ts
// src/services/api/createApiClient.ts
export function createApiClient(options: { token?: string }) {
  return axios.create({
    headers: options.token
      ? { Authorization: `Bearer ${options.token}` }
      : undefined
  })
}
```

Then wire it in boot with client/server-safe token sources.

## 7. PWA cache safety

Wrong Workbox-style intent:

```ts
// Cache all API requests for offline use
urlPattern: /\/api\//,
handler: 'CacheFirst'
```

Correct approach:

```ts
// Cache public/static resources only; explicitly exclude auth/payment/profile APIs.
// Any API runtime caching must be endpoint-specific and reviewed.
```

## 8. Testing output

Correct review comment:

> I added a Vitest test for `normalizeCourseTitle` because the changed function is pure. I did not add Cypress coverage because this change does not affect a user flow. Validation: `pnpm run test:unit` and `pnpm run typecheck` passed.

Wrong:

> I added no tests because this is a small change.

## 9. Codex/Claude final answer style

Good final response:

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

Bad final response:

```md
I refactored the code and it should be good now.
```
