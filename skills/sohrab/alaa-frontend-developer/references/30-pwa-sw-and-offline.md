# PWA, Service Worker and Offline — the policy layer

This file decides what may change. It does not carry the mechanism. Workbox recipes, InjectManifest shape,
update-UX code, push and background sync are `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`)
`references/30-service-worker-excellence.md` and `references/32-pwa-injectmanifest-guard.md`; PWA
operational records are `references/37-pwa-operations-record.md` there.

**What is stored is a different owner from what is cached.** Any offline task that keeps data — a request
cache, a draft, an outbox, a downloaded media asset — belongs to `/alaa-indexeddb-browser-storage`
(`$alaa-indexeddb-browser-storage`): `references/70-cache-and-drafts.md`, `references/71-browser-outbox.md`,
`references/72-offline-media-store.md`, and `references/31-quota-exceeded-and-cleanup.md` when the write
fails. The service worker owns the Cache API and the network; that skill owns the database. Do not build a
persistence layer inside a service worker without reading it.

## Default stance

If the user did not ask for a service-worker strategy change, the strategy does not change. Limit the diff
to UI around offline, update and network status.

## Standard contract

Navigation HTML is network-only; offline navigation falls back to a controlled offline page; runtime
caching is narrowly scoped; the update flow uses `SKIP_WAITING`, `clientsClaim()` and exactly one reload
on `controllerchange`; a custom InjectManifest worker keeps exactly one `self.__WB_MANIFEST`. The
authoritative statement of those five mechanisms is the Quasar skill's file above — this list exists so
you can tell when a diff has left the contract. Repo-local rules win where they differ.

## Non-negotiables

- **Do not add or widen a runtime-cache route matcher.** A widening requires the four risk notes below,
  written in the merge request body: the rollback path, the stale-asset risk, the offline-regression risk,
  and the hydration risk.
- Do not change build-time placeholder variables or remote-asset path logic as a side effect.
- Do not break registration, lifecycle orchestration or manifest versioning.

## Failure classes

**The app reloads forever after an update.** The reload on `controllerchange` is unguarded, so the new
controller triggers a reload that activates another controller. Diagnose by checking for a
one-shot guard around the reload; the smallest fix is to make the guard exist. Escalate to the Quasar
skill only if the lifecycle itself is wrong.

**A chunk 404s after a deploy.** An old HTML document is asking for a hashed asset the new build no longer
emits. Either navigation HTML is being cached when it must be network-only, or the deploy removed the
previous build's assets. The frontend half is the caching strategy; the retention half is
`/alaa-frontend-devops` (`$alaa-frontend-devops`) `references/25-artifact-identity-and-provenance.md` and
`references/45-deploy-failure-playbook.md`.

**The offline page never appears.** Either the fallback was never precached, or the navigation handler
throws instead of falling back. A service-worker failure degrades to network or to the fallback; it never
throws an unhandled error into a navigation.

**`self.__WB_MANIFEST` appears twice, or not at all.** The build injects into a worker that already has an
injection point, or into none. This is a build-wiring failure — route to
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) `references/32-pwa-injectmanifest-guard.md`.

**Stored data is missing or the quota is exhausted.** Not a service-worker failure. Route to
`/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`)
`references/32-eviction-and-recovery.md`.

## What a UI must state when it is degraded

An offline or stale screen says which data is stale and what the user may still do. The design of that
state is `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/15-designed-failure-states.md`;
the behavioural contract is `46-resilience-and-degradation.md`.

## Verification

The install, update, offline-fallback and runtime-cache checks live with the rest of the verification
plan in `50-qa-and-verification.md`. They run against the production build; a dev-server run proves
nothing about a service worker.
