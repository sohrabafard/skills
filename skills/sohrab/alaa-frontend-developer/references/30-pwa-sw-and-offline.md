# PWA, Service Worker, and Offline

Use this file for PWA-facing UI, service worker behavior, offline fallback, update flow, and safe SW change boundaries.

## Default stance

Prefer correctness and deploy safety over aggressive caching.

If the user did not explicitly request a service-worker strategy change:

- keep the current service-worker strategy intact
- limit changes to UI around offline, update, or network status when possible
- use exact Quasar/InjectManifest references from `$alaa-quasar-app-vite-v3` if Quasar config or build wiring is involved

When the user does request SW implementation depth (caching strategy design, Workbox recipes, update-UX code, SW performance, SW debugging, push/badging/background sync), pair with `$alaa-quasar-app-vite-v3` `references/30-service-worker-excellence.md`; this file stays the policy layer.

## Standard service-worker contract

Default app-family assumption:

- navigation HTML is network-only
- offline navigation falls back to a controlled offline page
- runtime caching is narrowly scoped, typically fonts only
- update flow uses `SKIP_WAITING`, `clientsClaim()`, and exactly one reload on `controllerchange`
- custom InjectManifest service workers must keep exactly one `self.__WB_MANIFEST`

If the repo-local contract differs, repo-local rules win.

## Non-negotiables for SW changes

- Do not silently broaden runtime caching for HTML, JS, CSS, images, workers, or APIs.
- Do not change build-time placeholder variables or remote-asset path logic unless explicitly requested.
- Do not break registration, lifecycle orchestration, or manifest versioning.

## Implementation workflow

### 1. Define the requested behavior

Write the requested behavior in plain English before editing:

- what should happen
- when it should happen
- what must remain unchanged

### 2. Define acceptance checks first

At minimum:

- install / first load
- update flow
- offline navigation fallback
- online regression
- remote assets when relevant

### 3. Pick the narrowest safe strategy

If a runtime strategy change is explicitly requested, document why the chosen strategy is safe for SSR:

- `NetworkOnly`
- `NetworkFirst`
- `StaleWhileRevalidate`
- `CacheFirst`

### 4. Patch minimally

- keep `self.__WB_MANIFEST` exactly once
- keep placeholder substitution intact
- do not broaden matchers beyond the requested scope
- ensure failures degrade to network or offline fallback instead of throwing unhandled errors

### 5. Record rollback

Every service-worker strategy change should include:

- rollback path
- stale-asset risk note
- offline regression risk note
- hydration risk note

## QA runbook

### Install / first load

- app loads normally
- service worker registers and activates
- no service-worker console errors

### Update flow

- new build produces a waiting worker
- app requests `SKIP_WAITING`
- `controllerchange` happens
- app reloads exactly once
- latest assets load without missing-chunk errors

### Offline fallback

- after at least one online load, disable network
- reload or direct-navigate
- offline fallback page appears
- no infinite reload loops

### Runtime cache smoke

- if fonts or another explicitly allowed runtime cache exist, confirm the expected cache entries appear
- navigation remains network-first or network-only as intended

## Pairing guidance

- Exact Quasar PWA/InjectManifest wiring:
  - Pair with `$alaa-quasar-app-vite-v3`
- Release and deployment artifact risk:
  - Pair with `$alaa-frontend-devops`
- QA runbook formalization:
  - Also load `50-qa-and-verification.md`
