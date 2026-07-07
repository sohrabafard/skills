# SSR, PWA, and Security

Use this file for universal rendering, hydration parity, SSR middleware, SEO, service worker behavior, and server-side auth flows.

For exact InjectManifest guardrails, change boundaries, and update/offline verification structure, pair this file with `32-pwa-injectmanifest-guard.md`.

## Covers

- SSR setup and runtime behavior (including the v3 server-framework choice)
- hydration mismatch avoidance, including Vue 3.5 hydration tools
- `ssrContext`, SSR middleware, and `preFetch`
- QNoSsr, `useHydration`, `useId`, `useMeta`
- server-side auth flows such as cookie-to-header forwarding
- PWA mode, Workbox, `GenerateSW` vs `InjectManifest`, offline fallback, and update flow

## app-vite v3 SSR/PWA structure changes

Confirm the app-vite line first (see `70-...`). In `@quasar/app-vite` v3:

- SSR scaffolding asks which server to use: **Hono, Express, Fastify, or Koa**, and adds `/src-ssr/server-assets`.
- The SSR middleware dev-error hook renamed: **`serve.error()` -> `serve.devError()`**.
- The custom service worker moved to **`/src-pwa/sw/`** (config key `sourceFiles.pwaServiceWorker` defaults to `'src-pwa/sw/custom-sw'`).

✅ Do — in a v3 repo, edit the custom SW at `src-pwa/sw/custom-sw.{js,ts}` and use `serve.devError()` in SSR middleware.

❌ Don't — assume the v2 `/src-pwa/custom-sw` path or `serve.error()` in a v3 repo; the file and hook moved.

## SSR rules

- Never use browser-only APIs during SSR render without a runtime guard.
- Keep server and client DOM output deterministic. Avoid `Date.now()`, `Math.random()`, unstable list order, and viewport-dependent branches in SSR-rendered markup.
- `ssrContext` exists only on the server side. Use it in boot/router/store/`preFetch` flows only where the server build exposes it.
- SSR middleware is Express/Hono/Fastify/Koa-compatible middleware depending on the chosen server. Keep the rendering middleware last.
- Prefer stable markup plus client enhancement over client-only rendering as a workaround for hydration issues.

✅ Do — guard browser-only work to after mount and keep SSR markup stable.

```js
import { onMounted, ref } from 'vue'
const width = ref(0)
onMounted(() => { width.value = window.innerWidth }) // client-only, post-hydration
```

❌ Don't — read `window`/`document`/`localStorage` in `setup()` or in render; it throws on the server or produces server/client drift.

```js
const width = window.innerWidth // crashes during SSR render
```

## Vue 3.5 hydration tools

Vue 3.5 (current `3.5.39`) ships the right primitives for the mismatches Quasar apps hit most:

- Use **`useId()`** for form/aria ids so server and client agree. This is the correct fix for "id mismatch" hydration warnings.
- Use **`data-allow-mismatch`** only for genuinely environment-dependent output (e.g. localized dates), optionally scoped (`text`, `class`, `attribute`, ...).

✅ Do — generate stable ids with `useId()` for a custom labeled control.

```js
import { useId } from 'vue'
const id = useId()
```

❌ Don't — paper over a real non-deterministic render with `data-allow-mismatch` everywhere; fix the determinism first, then allow only the irreducible difference.

## Auth and security rules

- Keep token mapping server-side only.
- Do not serialize sensitive tokens into HTML or expose them to client JavaScript.
- When a Quasar SSR app reads auth cookies and forwards them to backend APIs, that translation belongs in server-only code.
- In v3, remember client env exposure is gated by `build.env.clientPrefix` (default `'QCLI_'`). Do not give a secret a client-exposed prefix.
- Any env variable, proxy, or auth header task should cross-check the config/build rules from `21-cli-vite-and-config.md`.
- Treat `*-html` props, `QEditor`, upload surfaces, and custom slot rendering as content-safety boundaries, not just UI details.

✅ Do — forward an auth cookie to the backend from server-only middleware/boot.

```js
// server-side only (ssrContext present)
api.defaults.headers.common.Authorization = `Bearer ${tokenFromCookie}`
```

❌ Don't — inline a token into the rendered HTML or a client-prefixed env var.

```js
// leaks the secret to every browser
defineEnv: { QCLI_SESSION_TOKEN: token }
```

## PWA rules

Use `GenerateSW` when:

- you want the simplest service worker path
- your caching needs are conventional

Use `InjectManifest` when:

- you need custom routing logic
- you need service-worker-specific logic such as web push or carefully controlled offline behavior

For `InjectManifest`, keep these habits:

- own the service worker file intentionally (in v3 it lives under `src-pwa/sw/`)
- keep exactly one `self.__WB_MANIFEST`
- treat HTML navigation caching as a high-risk change in SSR apps
- define update flow, waiting-worker handling, and reload semantics explicitly
- make offline fallback behavior testable

✅ Do — choose `InjectManifest` and own one `self.__WB_MANIFEST` when you need custom SW logic.

❌ Don't — pick `InjectManifest` for a conventional cache and then leave the SW boilerplate unmanaged; `GenerateSW` is the right default there.

## Common "also load" cases

- Any service worker or PWA config change:
  - also read `32-pwa-injectmanifest-guard.md` and `80-upstream-deltas-and-live-checks.md`
- Any SSR UI issue:
  - also read `70-guardrails-a11y-performance-monorepo.md`
- Any component depending on browser APIs:
  - also read `60-components-and-layouts.md` or `64-plugins-composables-directives-options-utils.md`

## Easy-to-miss relationships

- Many "hydration bugs" are really stale service worker HTML or cached assets.
- `useMeta` and SEO work are often coupled to SSR timing and route data loading.
- `QNoSsr` and `useHydration` are not substitutes for fixing unstable SSR output.
- Upload, media, and scrolling features often need both client-only guards and PWA exclusions.
