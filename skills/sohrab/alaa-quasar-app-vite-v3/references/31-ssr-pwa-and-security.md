# SSR, PWA, and security

Use for universal rendering, hydration parity, SSR middleware/SEO/auth, and SW/PWA behavior. Pair InjectManifest work with `32-pwa-injectmanifest-guard.md`.

## Scope

- SSR runtime/setup (including v3 server choice), hydration avoidance/Vue 3.5 tools, `ssrContext`, middleware, `preFetch`, QNoSsr, `useHydration`, `useId`, `useMeta`
- server cookie-to-header auth
- PWA/Workbox, `GenerateSW` vs `InjectManifest`, offline fallback, updates

## app-vite v3 changes

First confirm the app-vite line (`70-...`). In `@quasar/app-vite` v3:

- SSR scaffolding selects **Hono, Express, Fastify, or Koa** and adds `/src-ssr/server-assets`.
- SSR middleware dev-error hook: **`serve.error()` → `serve.devError()`**.
- Custom SW moved to **`/src-pwa/sw/`**; `sourceFiles.pwaServiceWorker` defaults to `'src-pwa/sw/custom-sw'`.

Use `src-pwa/sw/custom-sw.{js,ts}` and `serve.devError()` in v3; the v2 `/src-pwa/custom-sw` path and `serve.error()` are wrong.

## SSR rules

- Guard browser-only APIs during SSR; use them after mount.
- Keep server/client DOM deterministic: no `Date.now()`, `Math.random()`, unstable list order, or viewport-dependent SSR markup.
- `ssrContext` is server-only; use it only in boot/router/store/`preFetch` paths whose server build exposes it.
- Middleware matches the chosen Express/Hono/Fastify/Koa server; rendering middleware stays last.
- Prefer stable markup plus client enhancement; client-only rendering does not fix hydration design.

```js
import { onMounted, ref } from 'vue'
const width = ref(0)
onMounted(() => { width.value = window.innerWidth }) // client-only, post-hydration
```

Never read `window`/`document`/`localStorage` in `setup()` or render; it throws server-side or creates drift:

```js
const width = window.innerWidth // crashes during SSR render
```

## Vue 3.5 hydration tools

Vue 3.5 (current `3.5.39`) provides:

- **`useId()`** for matching server/client form/ARIA IDs—the fix for ID mismatch warnings.
- **`data-allow-mismatch`** only for irreducible environment output such as localized dates; optionally scope it (`text`, `class`, `attribute`, ...). Fix determinism before allowing a mismatch; never apply it broadly.

```js
import { useId } from 'vue'
const id = useId()
```

## Auth/security

- Token mapping and cookie→backend-header translation stay server-only. Never serialize sensitive tokens into HTML or client JavaScript.
- v3 client env exposure uses `build.env.clientPrefix` (default `'QCLI_'`); secrets must not use a client prefix.
- For env/proxy/auth-header tasks, cross-check `21-cli-vite-and-config.md`.
- `*-html` props, `QEditor`, uploads, and custom slot rendering are content-safety boundaries.

Correct server-only forwarding (`ssrContext` present):

```js
api.defaults.headers.common.Authorization = `Bearer ${tokenFromCookie}`
```

Never leak a token through rendered HTML or client-prefixed env:

```js
defineEnv: { QCLI_SESSION_TOKEN: token }
```

## PWA rules

Use `GenerateSW` for the simplest conventional cache. Use `InjectManifest` only for custom routing, web push, or tightly controlled offline behavior. With InjectManifest:

- intentionally own v3 `src-pwa/sw/` and exactly one `self.__WB_MANIFEST`;
- treat SSR HTML navigation caching as high risk;
- explicitly define update flow, waiting-worker handling, reload semantics, and testable offline fallback.

Never choose InjectManifest for a conventional cache and leave boilerplate unmanaged; use `GenerateSW`.

## Also load

- SW/PWA config: `32-pwa-injectmanifest-guard.md` + `80-upstream-deltas-and-live-checks.md`
- SSR UI: `70-guardrails-a11y-performance-monorepo.md`
- components using browser APIs: `60-components-and-layouts.md` or `64-plugins-composables-directives-options-utils.md`

## Couplings often missed

- “Hydration” failures may be stale SW-cached HTML/assets.
- `useMeta`/SEO often depends on SSR timing and route data.
- `QNoSsr`/`useHydration` do not replace deterministic SSR.
- Upload/media/scroll features often need both client-only guards and PWA exclusions.
