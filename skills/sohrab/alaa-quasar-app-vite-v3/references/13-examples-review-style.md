# Review examples and anti-patterns

You are about to write a review comment, or you must choose between two shapes and need the correct/wrong pair that justifies the choice. Each section is a pair: the comment that lands, and the one that causes the failure.

## 1. CLI versus Vite plugin

Correct:

> This repository has `quasar.config.ts` and `@quasar/app-vite`, so it is a Quasar CLI app. Configure Vite through `quasar.config.ts`; do not install `@quasar/vite-plugin` or create `vite.config.ts`.

Wrong:

> Install `@quasar/vite-plugin` and configure `vite.config.ts`.

## 2. Versioning

Correct:

> The repository is on app-vite v2. Keep this patch lockfile-compatible and record the alias and env migration debt. v3 is stable, and it is scheduled separately through `references/10-v2-to-v3-migration.md`.

Wrong:

> v3 is stable, so I upgraded app-vite and vue-router in this patch.

That upgrade leaves imports, env, aliases, and mode folders untested behind a green lint run.

## 3. Aliases

Correct new import where `@/` exists:

```ts
import UserAvatar from '@/components/user/UserAvatar.vue'
```

Acceptable in a small v2 patch where `@/` does not exist:

```ts
import UserAvatar from 'components/user/UserAvatar.vue'
```

with the comment:

```md
V3 readiness: this alias moves to `@/components/...` in the alias migration.
```

Wrong where `@/` already exists:

```ts
import UserAvatar from 'components/user/UserAvatar.vue'
```

## 4. Env access

```ts
// correct v2
if (process.env.SERVER) { /* server only */ }
// correct v3
if (import.meta.env.QUASAR_SERVER) { /* server only */ }
```

Wrong in any build-time replacement system — each of these is `undefined` in a production build:

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

## 6. Boot boundary and request isolation

Wrong — a module-level token becomes one shared client for every SSR request:

```ts
// src/boot/user.ts
let token = localStorage.getItem('token')
export const api = axios.create({ headers: { Authorization: `Bearer ${token}` } })
```

Correct — a factory, wired from boot with a client- or server-safe token source:

```ts
// src/services/api/createApiClient.ts
export function createApiClient(options: { token?: string }) {
  return axios.create({
    headers: options.token ? { Authorization: `Bearer ${options.token}` } : undefined
  })
}
```

## 7. PWA cache policy

Wrong:

```ts
// Cache all API requests offline
urlPattern: /\/api\//,
handler: 'CacheFirst'
```

Correct:

```ts
// NetworkOnly for every credentialed request. Runtime-cache only public, static
// resources. Each cached endpoint is named explicitly in quasar.config with a
// justification and a logout-purge entry; see references/30-service-worker-excellence.md §7.
```

## 8. Test reporting

Correct:

> Added Vitest coverage for the pure `normalizeCourseTitle`; no end-to-end test because no user flow changed. `pnpm run test:unit` and `pnpm run typecheck` passed.

Wrong:

> No tests because this is small.

## 9. Final answer

Good:

```md
Done.

Changed:
- `src/services/api/createApiClient.ts`: moved API client creation into a factory.
- `src/boot/api.ts`: creates one client per app or per request.

Why safe on the detected line (app-vite v2):
- Preserves the existing `process.env.CLIENT` usage.
- Does not touch dependencies or the lockfile.

v3 readiness:
- New imports use `@/`.
- The remaining `process.env.*` guards are direct member reads and are codemod-friendly.

Validation:
- `pnpm run typecheck`: passed
- `pnpm run test:unit`: passed
- `pnpm run build`: not run, because ...
```

Bad:

> I refactored the code and it should be good now.

Search: `review comment`, `correct wrong pair`, `anti-pattern`, `vite.config in CLI app`, `alias migration debt`, `env destructure`, `request isolation`, `honest validation report`.
