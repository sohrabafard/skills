# PWA InjectManifest guard

You are about to open a file under `src-pwa/`, change a custom service worker, change the update lifecycle or offline fallback, or touch any Quasar `InjectManifest` contract. Read this before `references/30-service-worker-excellence.md`, not instead of it, and pair it with `references/31-ssr-pwa-and-security.md` on SSR apps.

## 1. Versioned location — the single statement in this pack

| Line | Custom service-worker file | `sourceFiles.pwaServiceWorker` default |
| --- | --- | --- |
| `@quasar/app-vite` v3 | `src-pwa/sw/custom-sw.{js,ts}` | `'src-pwa/sw/custom-sw'` |
| `@quasar/app-vite` v2 | `src-pwa/custom-sw.{js,ts}` | `'src-pwa/custom-sw'` |

The v3 default is `'src-pwa/sw/custom-sw'`. Verified on 2026-07-28 by reading the installed CLI in the live `client` checkout — `node_modules/@quasar/app-vite/lib/quasar-config-file.js`, the `sourceFiles` defaults block — and confirmed against the `sourceFiles` comment block the v3 scaffold writes into `quasar.config.ts`. **No other file in this pack states this default; every other mention points here.** An agent that writes `'src-pwa/custom-sw'` into a v3 config, or creates `src-pwa/custom-sw.js` in a v3 repo, produces a service worker the CLI never reads: the build succeeds, the file is silently ignored, and every rule in it is absent from production.

Open the path matching the installed major, which you detect first per `references/80-upstream-deltas-and-live-checks.md` §3.

The registration file is separate and stays directly under `src-pwa/`: `sourceFiles.pwaRegisterServiceWorker` defaults to `'src-pwa/register-sw'` on both lines.

## 2. Mode gate — check before reviewing the file at all

`pwa.workboxMode` decides whether the custom service worker exists in the build:

- `'InjectManifest'` — the file at `sourceFiles.pwaServiceWorker` is bundled and shipped.
- `'GenerateSW'` — that file is **not built and not shipped**. Workbox generates the service worker from `quasar.config`, and every rule written in `custom-sw` is absent from production regardless of how correct it is.

A repository holding a `src-pwa/sw/custom-sw.ts` while `pwa.workboxMode` is `'GenerateSW'` has dead code that reads like shipped behaviour. Report the mismatch before reviewing the file's contents.

## 3. Invariants

- Keep exactly one `self.__WB_MANIFEST` in the custom service worker. Zero means nothing is precached; more than one fails the Workbox injection.
- HTML navigation caching is high risk in SSR apps: a cached shell and a server-rendered document disagree and surface as a hydration mismatch.
- Do not change the update flow, waiting-worker behaviour, or offline-fallback semantics as a side effect of another change.
- **Do not modify asset-base or placeholder-replacement variables in the same change as any other service-worker edit.** Change them alone, and record the before and after values in the change note required by §4.

## 4. Before editing, record

- the behaviour that must remain unchanged;
- the exact intended change;
- the install, update, and offline-navigation verification you will run;
- the rollback boundary.

When the change alters caching, update, or offline behaviour, it also updates `references/37-pwa-operations-record.md` in the same change.

## 5. Risk boundary

Safe while caching semantics are unchanged: update-notification UI built on the existing flow; offline-page copy; manifest and icon metadata; adding an emission that follows `references/36-client-observability-contract.md`.

High risk: navigation strategy; broader runtime caching; cache names or version semantics; remote asset resolution; removing or changing skip-waiting or `controllerchange` orchestration. The mechanics of those are `references/30-service-worker-excellence.md` §4.

## 6. Minimum verification — all five, every time

1. first install on a clean profile;
2. update with an already-installed worker present;
3. offline fallback navigation;
4. normal online navigation;
5. remote assets, when the repo serves any remotely.

Reporting fewer than five is reporting an incomplete verification. The automated form of 1-3 is `references/75-testing-ci-playbook.md`.

Search: `InjectManifest`, `GenerateSW`, `workboxMode`, `self.__WB_MANIFEST`, `sourceFiles`, `pwaServiceWorker`, `pwaRegisterServiceWorker`, `src-pwa/sw`, `skipWaiting`, `clientsClaim`, `controllerchange`, `offline fallback`, `navigation caching`.
