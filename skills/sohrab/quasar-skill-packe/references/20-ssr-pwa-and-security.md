# SSR, PWA, and Security

Use this file for universal rendering, hydration parity, SSR middleware, SEO, service worker behavior, and server-side auth flows.

## Covers

- SSR setup and runtime behavior
- hydration mismatch avoidance
- `ssrContext`, SSR middleware, and `preFetch`
- QNoSsr, `useHydration`, `useId`, `useMeta`
- server-side auth flows such as cookie-to-header forwarding
- PWA mode, Workbox, `GenerateSW` vs `InjectManifest`, offline fallback, and update flow

## SSR rules

- Never use browser-only APIs during SSR render without a runtime guard.
- Keep server and client DOM output deterministic. Avoid `Date.now()`, `Math.random()`, unstable list order, and viewport-dependent branches in SSR-rendered markup.
- `ssrContext` exists only on the server side. Use it in boot/router/store/`preFetch` flows only where the server build exposes it.
- SSR middleware is Express-compatible middleware. Keep the rendering middleware last.
- Prefer stable markup plus client enhancement over client-only rendering as a workaround for hydration issues.

## Auth and security rules

- Keep token mapping server-side only.
- Do not serialize sensitive tokens into HTML or expose them to client JavaScript.
- When a Quasar SSR app reads auth cookies and forwards them to backend APIs, that translation belongs in server-only code.
- Any env variable, proxy, or auth header task should cross-check the config/build rules from `10-cli-vite-and-config.md`.

## PWA rules

Use `GenerateSW` when:

- you want the simplest service worker path
- your caching needs are conventional

Use `InjectManifest` when:

- you need custom routing logic
- you need service-worker-specific logic such as web push or carefully controlled offline behavior

For `InjectManifest`, keep these habits:

- own the service worker file intentionally
- keep exactly one `self.__WB_MANIFEST`
- treat HTML navigation caching as a high-risk change in SSR apps
- define update flow, waiting-worker handling, and reload semantics explicitly
- make offline fallback behavior testable

## Common "also load" cases

- Any service worker or PWA config change:
  - also read `70-upstream-deltas-and-live-checks.md`
- Any SSR UI issue:
  - also read `60-guardrails-a11y-performance-monorepo.md`
- Any component depending on browser APIs:
  - also read `40-components-and-layouts.md` or `50-plugins-composables-directives-options-utils.md`

## Easy-to-miss relationships

- Many "hydration bugs" are really stale service worker HTML or cached assets.
- `useMeta` and SEO work are often coupled to SSR timing and route data loading.
- `QNoSsr` and `useHydration` are not substitutes for fixing unstable SSR output.
- Upload, media, and scrolling features often need both client-only guards and PWA exclusions.
