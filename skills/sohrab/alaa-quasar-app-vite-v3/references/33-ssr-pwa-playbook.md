# SSR and PWA Playbook

Use this reference when the task touches SSR, hydration, service workers, offline behavior, SEO, cookies, request isolation, or deployment.

## 1. SSR mental model

SSR executes parts of the app on the server, then hydrates on the client. Code must be universal unless explicitly guarded.

### Browser-only APIs

Wrong:

```ts
const token = localStorage.getItem('token')
const width = window.innerWidth
```

Correct in Vue component:

```ts
import { onMounted, ref } from 'vue'

const width = ref<number | null>(null)

onMounted(() => {
  width.value = window.innerWidth
})
```

Correct with Quasar mode guard in v2:

```ts
if (process.env.CLIENT) {
  localStorage.setItem('theme', 'dark')
}
```

Correct target after v3 migration:

```ts
if (import.meta.env.QUASAR_CLIENT) {
  localStorage.setItem('theme', 'dark')
}
```

## 2. Request isolation

Never keep request/user/session state in global mutable variables.

Wrong:

```ts
let currentTenantId: string | null = null

export function setTenant(id: string) {
  currentTenantId = id
}
```

Correct:

```ts
export function createTenantContext(initialTenantId?: string) {
  return {
    tenantId: initialTenantId ?? null
  }
}
```

Use factories for services that may contain request-scoped auth headers or cookies.

## 3. SSR boot files

Use `ssrContext` only when available. Do not assume it exists in SPA/PWA mode.

Correct (app-vite v2 wrapper; use `#q-app` in a v3 repo):

```ts
import { defineBoot } from '#q-app/wrappers'

export default defineBoot(({ app, ssrContext }) => {
  const api = createApiClient({
    cookies: ssrContext?.req?.headers?.cookie
  })

  app.provide('api', api)
})
```

Wrong (reads `document` on the server; also legacy `boot()` instead of `defineBoot`):

```ts
export default defineBoot(() => {
  const cookie = document.cookie // throws during SSR render
})
```

## 4. Hydration safety

Avoid markup that differs between server and client before hydration.

Risky:

```vue
<template>
  <div>{{ new Date().toLocaleString() }}</div>
</template>
```

Safer:

```vue
<template>
  <div>{{ renderedTime ?? '...' }}</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
const renderedTime = ref<string | null>(null)
onMounted(() => {
  renderedTime.value = new Date().toLocaleString()
})
</script>
```

## 5. SEO and meta

For SEO-sensitive SSR pages, use Quasar's meta utilities or the repo's existing SEO layer. Avoid directly mutating `document.title` in setup for SSR pages.

Wrong:

```ts
document.title = course.title
```

Correct pattern:

```ts
useMeta(() => ({
  title: course.value?.title ?? 'Alaa',
  meta: {
    description: {
      name: 'description',
      content: course.value?.description ?? ''
    }
  }
}))
```

## 6. PWA folder structure and service worker boundaries

PWA-specific files live under `src-pwa/`. In newer app-vite layouts, custom service worker code belongs under `src-pwa/sw/`, while `register-sw.*` stays in `src-pwa/` as app-space/main-thread code.

### Main-thread service-worker registration

Correct:

```ts
// src-pwa/register-sw.ts
import { register } from 'register-service-worker'

register(process.env.SERVICE_WORKER_FILE, {
  updated() {
    // show update UI through app event bus/store
  },
  offline() {
    // notify user that cached mode is active
  }
})
```

V3 migration target:

```ts
register(import.meta.env.QUASAR_SERVICE_WORKER_FILE, {
  updated() {},
  offline() {}
})
```

Wrong:

```ts
// service worker file
window.location.reload()
document.querySelector('#app')
```

The service worker runs in a WebWorker context and must not use DOM APIs.

## 7. Cache strategy

For educational VOD apps, be careful with aggressive caching:

- Do not cache authenticated API responses unless explicitly safe.
- Do not cache payment/order/user profile endpoints.
- Cache static assets, icon/font assets, and public shell assets.
- For video assets, follow the platform/CDN policy; do not blindly precache large media.
- Always test update behavior: new build available, offline mode, stale shell, logout/login.

## 8. SSR + PWA client takeover

SSR + PWA can be valuable, but it increases complexity. Do not enable it as a side effect of unrelated changes.

Before enabling SSR + PWA, confirm:

- service worker update UX exists
- cache exclusions for private APIs exist
- hydration warnings are under control
- SSR deployment process is clear
- build commands exist in CI

## 9. Deployment checks

SPA:

```bash
<pm> quasar build
```

PWA:

```bash
<pm> quasar build -m pwa
```

SSR:

```bash
<pm> quasar build -m ssr
node dist/ssr/index.js
```

For SSR production behind Nginx/HAProxy, confirm:

- health endpoint or process manager exists
- forwarded headers are handled correctly
- gzip/brotli/static asset serving behavior is known
- cache headers are explicit
- secrets are server-side only
