# PWA InjectManifest guard

Use when changing a custom SW, PWA update lifecycle, offline fallback, or any Quasar InjectManifest contract. Load with—not instead of—`31-ssr-pwa-and-security.md`.

## Versioned location

- `@quasar/app-vite` v3: `src-pwa/sw/custom-sw.{js,ts}`; `sourceFiles.pwaServiceWorker` defaults to `'src-pwa/sw/custom-sw'`.
- v2: `src-pwa/custom-sw.{js,ts}`.

Open the path matching the installed major. Never create `src-pwa/custom-sw.js` in v3: the CLI reads `src-pwa/sw/`, so that edit is ignored.

## Risks and invariants

Conceptual SSR/PWA guidance alone does not prevent stale deploys, broken updates, cached-HTML hydration drift, offline fallback regressions, or remote-asset path regressions.

- Keep exactly one `self.__WB_MANIFEST` in the custom SW.
- HTML navigation caching is high risk in SSR apps.
- Never implicitly change update flow, waiting-worker behavior, or offline fallback semantics.
- Preserve established asset-base and placeholder-replacement variables unless intentionally changing the SW contract.

## Before editing

Record:

- behavior that must remain unchanged;
- exact intended change;
- install/update/offline-navigation verification;
- rollback boundary.

## Risk boundary

Safe when caching semantics stay unchanged: update-notification UI using the existing flow; offline-page copy; manifest/icon metadata; logging/observability.

High risk: navigation strategy; broader runtime caching; cache names/version semantics; remote asset resolution; removal/change of skip-waiting or controller-change orchestration.

## Minimum verification

- first install;
- update with an already-installed worker;
- offline fallback navigation;
- normal online navigation;
- remote assets when the repo serves them remotely.

Search: `InjectManifest`, `self.__WB_MANIFEST`, `skipWaiting`, `clientsClaim`, `controllerchange`, `offline fallback`, `navigation caching`.
