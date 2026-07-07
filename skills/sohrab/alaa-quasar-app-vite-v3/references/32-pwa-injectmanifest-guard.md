# PWA InjectManifest Guard

Use this file when the task changes a custom service worker, the PWA update lifecycle, offline fallback behavior, or any InjectManifest contract in a Quasar app.

Load this file together with `31-ssr-pwa-and-security.md`, not instead of it.

## File location depends on the app-vite line

- `@quasar/app-vite` v3: the custom SW lives at `src-pwa/sw/custom-sw.{js,ts}` (config key `sourceFiles.pwaServiceWorker`, default `'src-pwa/sw/custom-sw'`).
- `@quasar/app-vite` v2: the custom SW lives at `src-pwa/custom-sw.{js,ts}`.

✅ Do — open the SW at the path that matches the installed app-vite major before editing.

❌ Don't — create a new `src-pwa/custom-sw.js` in a v3 repo; the CLI looks under `src-pwa/sw/`, so your changes would be ignored.

## Why this file exists

The generic SSR/PWA reference is enough for conceptual questions. It is not enough when the task can accidentally cause:

- stale deploys
- broken update flow
- hydration drift from cached HTML
- offline fallback regressions
- remote asset path regressions

## Hard invariants

- Keep exactly one `self.__WB_MANIFEST` in the custom service worker.
- Treat HTML navigation caching as a high-risk change in SSR apps.
- Do not change update flow, waiting-worker behavior, or offline fallback semantics implicitly.
- Do not change asset-base or placeholder replacement variables casually in a repo that already has a SW contract.

## Change-boundary checklist

Before editing, write down:

- what must stay unchanged
- what exact behavior is being changed
- how install, update, and offline navigation will be verified
- what the rollback boundary is

## Safe changes

- update-notification UI that uses the existing SW flow
- offline-page content changes without strategy changes
- manifest/icon metadata updates
- logging or observability tweaks that do not change caching behavior

## High-risk changes

- changing navigation strategy
- broadening runtime caching
- changing cache names or versioning semantics
- changing remote asset resolution
- removing or altering skip-waiting / controller-change orchestration

## Verification minimum

- first install
- update flow with an already-installed worker
- offline navigation fallback
- normal online navigation
- remote asset loading, if the repo serves assets remotely

## Search terms

- `InjectManifest`, `self.__WB_MANIFEST`, `skipWaiting`, `clientsClaim`, `controllerchange`, `offline fallback`, `navigation caching`
