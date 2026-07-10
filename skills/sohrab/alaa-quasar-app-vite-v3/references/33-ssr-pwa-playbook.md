# SSR and PWA playbook

Use for SSR, hydration, SW/offline, SEO, cookies, request isolation, or deployment.

## 1. Universal SSR

SSR runs app code on the server, then hydrates it client-side. Guard browser-only APIs.

Wrong:

```ts
const token = localStorage.getItem('token')
const width = window.innerWidth
```

Vue-safe:

```ts
import { onMounted, ref } from 'vue'
const width = ref<number | null>(null)
onMounted(() => { width.value = window.innerWidth })
```

Quasar mode guard, v2 → v3 target:

```ts
if (process.env.CLIENT) localStorage.setItem('theme', 'dark')
if (import.meta.env.QUASAR_CLIENT) localStorage.setItem('theme', 'dark')
```

## 2. Request isolation

Never keep request/user/session state in mutable globals.

```ts
// Wrong: leaks across requests
let currentTenantId: string | null = null
export function setTenant(id: string) { currentTenantId = id }

// Correct: per-request factory
export function createTenantContext(initialTenantId?: string) {
  return { tenantId: initialTenantId ?? null }
}
```

Factories are also mandatory for services holding request-scoped auth headers/cookies.

## 3. SSR boot

`ssrContext` is optional outside SSR. App-vite v2 wrapper shown; v3 repos use `#q-app`:

```ts
import { defineBoot } from '#q-app/wrappers'

export default defineBoot(({ app, ssrContext }) => {
  const api = createApiClient({ cookies: ssrContext?.req?.headers?.cookie })
  app.provide('api', api)
})
```

Never read DOM on the server or retain the legacy `boot()` wrapper instead of `defineBoot`:

```ts
export default defineBoot(() => {
  const cookie = document.cookie // throws during SSR render
})
```

## 4. Hydration

Pre-hydration markup must match. Defer time/environment output:

```vue
<!-- Risky -->
<template><div>{{ new Date().toLocaleString() }}</div></template>
```

```vue
<!-- Safe -->
<template><div>{{ renderedTime ?? '...' }}</div></template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
const renderedTime = ref<string | null>(null)
onMounted(() => { renderedTime.value = new Date().toLocaleString() })
</script>
```

## 5. SEO/meta

On SEO-sensitive SSR pages use Quasar meta utilities or the repo SEO layer, never `document.title` in setup.

```ts
// Wrong
document.title = course.title

// Correct
useMeta(() => ({
  title: course.value?.title ?? 'Alaa',
  meta: { description: { name: 'description', content: course.value?.description ?? '' } }
}))
```

## 6. PWA/SW boundaries

PWA files live under `src-pwa/`. Newer app-vite keeps custom SW code in `src-pwa/sw/`; main-thread `register-sw.*` remains in `src-pwa/`.

```ts
// src-pwa/register-sw.ts (v2)
import { register } from 'register-service-worker'
register(process.env.SERVICE_WORKER_FILE, {
  updated() { /* show update UI through app event bus/store */ },
  offline() { /* notify cached mode */ }
})

// v3 target
register(import.meta.env.QUASAR_SERVICE_WORKER_FILE, {
  updated() {},
  offline() {}
})
```

SW code runs in WebWorker context; never use `window.location.reload()` or `document.querySelector('#app')` there.

## 7. Cache policy

For educational VOD apps:

- never cache authenticated APIs unless explicitly safe; never cache payment/order/profile endpoints;
- cache static/icon/font/public-shell assets;
- follow platform/CDN policy for video; never blindly precache large media;
- test new-build update, offline, stale shell, and logout/login.

## 8. SSR + PWA takeover

Do not enable this combination as an unrelated side effect. First confirm update UX, private-API cache exclusions, controlled hydration warnings, clear SSR deployment, and CI build commands.

## 9. Deployment checks

```bash
# SPA
<pm> quasar build
# PWA
<pm> quasar build -m pwa
# SSR
<pm> quasar build -m ssr
node dist/ssr/index.js
```

For SSR behind Nginx/HAProxy verify: health endpoint/process manager; forwarded headers; known gzip/brotli/static serving; explicit cache headers; server-only secrets.
