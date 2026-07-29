# SSR, hydration, and the SSR/PWA security boundary

You are about to render on the server, read `ssrContext`, write `preFetch`, forward an auth cookie, set SEO meta, or fix a hydration mismatch. This file owns the SSR model. Pair `InjectManifest` work with `references/32-pwa-injectmanifest-guard.md`, and what the user sees when the render fails with `references/34-frontend-failure-and-degradation.md`.

## Scope

SSR runtime and setup including the v3 server choice; hydration determinism and the Vue 3.5 tools; `ssrContext`, middleware, `preFetch`, `QNoSsr`, `useHydration`, `useId`, `useMeta`; server cookie-to-header auth; the `GenerateSW`-versus-`InjectManifest` decision.

## app-vite v3 changes

Confirm the installed app-vite line first — `references/80-upstream-deltas-and-live-checks.md` §3. In v3:

- SSR scaffolding selects **Hono, Express, Fastify, or Koa** and adds `/src-ssr/server-assets`.
- The SSR middleware dev-error hook is **`serve.devError()`**, not the v2 `serve.error()`.
- The custom service worker moved to **`/src-pwa/sw/`**; the exact `sourceFiles` default is stated once, in `references/32-pwa-injectmanifest-guard.md`.

On v3, `src-pwa/sw/custom-sw.{js,ts}` and `serve.devError()` are correct; the v2 `/src-pwa/custom-sw` path and `serve.error()` are wrong and fail differently — the first silently, the second at build.

## SSR rules

- **Never read `window`, `document`, `localStorage`, `sessionStorage`, or `navigator` in `setup()` or in a render function.** It throws on the server or creates drift. Read them after mount.
- Keep server and client DOM deterministic: no `Date.now()`, no `Math.random()`, no unstable list order, no viewport-dependent SSR markup.
- `ssrContext` is server-only. Use it only in boot, router, store, and `preFetch` paths whose server build exposes it.
- Middleware matches the chosen Hono/Express/Fastify/Koa server, and the rendering middleware stays last in `ssr.middlewares`.
- Prefer stable markup plus client enhancement; moving a component to client-only does not fix a hydration design problem, it hides it.
- **Never keep request, user, or session state in a module-level mutable variable.** On the server one module instance serves every request, so a module global leaks one user's data into another user's response. Use a per-request factory for the app, the router, the store, and every API client. The exact factory and boot shapes are `references/22-cli-cookbook-and-examples.md`; the v2 form and the wrong form are `references/12-v2-maintenance-playbook.md` §6 and `references/13-examples-review-style.md` §6.

```js
import { onMounted, ref } from 'vue'
const width = ref(0)
onMounted(() => { width.value = window.innerWidth }) // client-only, post-hydration
```

```js
const width = window.innerWidth // crashes during SSR render
```

## Vue 3.5 hydration tools

- **`useId()`** matches server and client form and ARIA ids — the fix for id-mismatch warnings.
- **`data-allow-mismatch`** is for irreducible environment output such as a localized date, and may be scoped (`text`, `class`, `attribute`, ...). Fix determinism first; never apply it to a subtree to silence an unknown mismatch.

```js
import { useId } from 'vue'
const id = useId()
```

Hydration failure signatures — dev-only, deploy-only, second-request-only — are `references/70-guardrails-a11y-performance-monorepo.md`.

## Auth and security

- Token mapping and cookie-to-backend-header translation stay server-only. Never serialize a token into HTML or into client JavaScript.
- Client env exposure runs through `build.env.clientPrefix` (default `'QCLI_'`); a secret never carries a client prefix. The full env contract is `references/20-v3-config-and-features.md`.
- Boot files are side-scoped with `{ server: false }` / `{ client: false }`; auth header wiring and sensitive redirects stay on the server side.

```js
api.defaults.headers.common.Authorization = `Bearer ${tokenFromCookie}` // server-only, ssrContext present
```

```js
defineEnv: { QCLI_SESSION_TOKEN: token } // leaks the token into the client bundle
```

**Never bind user-controlled text to a `*-html` prop, to `Notify.create({ html: true })`, to `QEditor` output, or to a custom slot that renders markup, without passing it through the repository's sanitizer first.** If the repository has no sanitizer, render the value as text. The code pair is `references/66-api-usage-atlas.md`; the `client` repository's sanitizer is the `@alaa/sanitize-html` package. Threat classes and review triggers are `/alaa-security-review` (`$alaa-security-review`), `references/25-browser-trust-and-output.md`; upload transport is `/tusd-upload-platform` (`$tusd-upload-platform`).

**A Content-Security-Policy header is a server-owned control, not a Quasar config key.** An SSR app sets it in the SSR middleware or at the reverse proxy; a static SPA build sets it at the serving layer. Two Quasar-specific consequences: an inline `<script>` or inline style emitted by a plugin needs a nonce or a hash, and `build.define`-injected values appear in the bundle rather than inline, so they do not need one. The directive set and the reporting endpoint are `/alaa-security-review` (`$alaa-security-review`); the serving-layer wiring is `/alaa-frontend-devops` (`$alaa-frontend-devops`) and, for the proxy, `/alaa-haproxy` (`$alaa-haproxy`). Do not invent a policy in a Quasar file.

## PWA rules

Use `GenerateSW` for a conventional cache. Choose `InjectManifest` only for custom routing, web push, or tightly controlled offline behaviour. With `InjectManifest`:

- own `src-pwa/sw/` deliberately and keep exactly one `self.__WB_MANIFEST`;
- treat SSR HTML navigation caching as high risk;
- define the update flow, the waiting-worker handling, the reload semantics, and a testable offline fallback explicitly.

Never choose `InjectManifest` for a conventional cache and leave the boilerplate unmanaged; use `GenerateSW`.

## Also load

- Service-worker behaviour: `references/30-service-worker-excellence.md`; change safety: `references/32-pwa-injectmanifest-guard.md`.
- Render-failure response and degradation: `references/34-frontend-failure-and-degradation.md`.
- SSR UI regressions: `references/70-guardrails-a11y-performance-monorepo.md`.
- Components that touch browser APIs: `references/60-components-and-layouts.md` or `references/64-plugins-composables-directives-options-utils.md`.

## Couplings often missed

- A "hydration" failure may be stale service-worker-cached HTML or assets, not a determinism bug.
- `useMeta` and SEO depend on SSR timing and route data; the API is `references/66-api-usage-atlas.md`.
- `QNoSsr` and `useHydration` do not replace deterministic SSR.
- Upload, media, and scroll features usually need both a client-only guard and a PWA cache exclusion.

Search: `ssrContext`, `preFetch`, `defineSsrMiddleware`, `serve.devError`, `server-assets`, `hydration mismatch`, `useId`, `data-allow-mismatch`, `QNoSsr`, `useHydration`, `useMeta`, `clientPrefix`, `sanitize`, `CSP`, `nonce`, `request isolation`, `per-request factory`.
