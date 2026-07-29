# Integration with the `client` repository

## What is already there, read 2026-07-28

Read it before designing a new layer.

| File | What it is |
|---|---|
| `src/storage/browserKeyValueStorage.ts` | the generic facade: IndexedDB-first key-value store behind `BrowserKeyValueStorage<TRecord>`, with a `localStorage` fallback and a no-op for SSR |
| `src/sdk/browserResponseCache.ts` | the L2 response cache on that facade, entry-capped, `localStorage` fallback deliberately disabled |
| `src/content-show/waOutboxStorage.ts` | watch-analytics outbox records, TTL-bounded and capped per record |
| `src/content-show/useContentShowWaOutbox.ts` | the flush composable |
| `src/stores/authPermissions.ts` | the unverified UI authorization snapshot — **in memory, never persisted** (`61-authority-boundary.md`) |

Two properties are correct and must not be regressed: **the response cache has no `localStorage`
fallback**, deliberately, because pushing a cached API payload into a synchronous, size-limited,
always-readable store is a worse trade than missing the cache; and **the permission snapshot is never
written to storage**, being derived from the session and recomputed when a new token arrives.

Three live gaps, each an instance of a rule in this pack, none fixed by this skill:

- `browserKeyValueStorage.ts` calls `store.getAll()` with no bound and filters the whole result by key
  prefix in JavaScript — `O(n)` in the store's size on every `list()`
  (`50-transactions-performance-and-query-patterns.md`). Acceptable while the stores are small; not
  acceptable as a draft or offline-media store grows.
- No application path calls `navigator.storage.estimate()` or `persist()`, and no application code handles
  `QuotaExceededError`; the only quota handling in the tree is inside Workbox. A feature storing anything
  the user is asked to rely on needs both (`30-…`, `31-…`).
- Nothing uses `BroadcastChannel` or `navigator.locks`, so multi-tab coordination is absent, and
  `openKeyValueDb` rejects on `blocked` rather than surfacing the reload UX (`41-…`).

## Names are not this skill's to mint

Every database, store, index, configuration key and event **name** is a value, and values are
`/alaa-services-contract` (`$alaa-services-contract`). Register a new one there before the code using it
merges. The names below are what the repository already has, recorded so a new feature matches rather than
invents.

```text
existing databases:  alaa.content-show.wa-outbox   (store: outbox)
                     client-response-cache          (store: responses)
```

`accountKey` composition is one registered value and one only. The repository composes a content-show scope
key as `accountKey|scopeKey` by string join; **a delimiter-joined identifier has no escaping rule, so no
segment may contain the delimiter.** If a segment could, encode it — `/alaa-crockford-base32-codecs`
(`$alaa-crockford-base32-codecs`) — rather than choosing a rarer delimiter.

## What storage may not do

The gateway and auth path is the trust boundary: storage code never owns bearer attachment, refresh,
trusted-header handling or route composition (`/alaa-trust-gateway-auth`, `$alaa-trust-gateway-auth`).
Every protected call from storage-backed sync goes through the application's SDK client, never a
service-local route, an authorization sidecar or a policy engine. The backend owns identity, content truth,
entitlement and analytics ingestion; the device holds a cache, a buffer and unsent work.

## Where a storage module goes

```text
src/storage/
  browserKeyValueStorage.ts     # exists
  capabilities.ts               # the probe and the persisted tier
  quota.ts                      # estimate, persistence request, budget thresholds from config
  migrations.ts                 # version branches and the journal
  stores/                       # one module per store, exposing domain methods only
  sync/outbox-runner.ts  sync/reaper.ts
  testing/fixtures.ts
```

Expose domain methods, never a raw `IDBDatabase`, outside `src/storage/`. File size, naming and composition
are `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`); Vue and Quasar integration is
`/alaa-frontend-developer` (`$alaa-frontend-developer`).

## When a storage change needs an ADR

Write one from `assets/alaa-indexeddb-adr.md` when any holds: the feature stores more than 50 MB per
account; it stores user-generated unsynced work; the product will tell the user something is available
offline; it stores anything classified `pii_moderate_high`; the change is a destructive migration; local
data affects what the user is shown about access, billing or entitlement; or the feature adds a second
database or a named storage bucket.

## Consumers, and the file that owns each seam

| Consumer | This skill owns | The other side |
|---|---|---|
| request caching | the IndexedDB record, its TTL, validator, budget and cleanup — `70-cache-and-drafts.md` | service worker, Cache API, Workbox, Background Sync: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/30-service-worker-excellence.md` |
| the browser outbox | the row, its states, the claim, the reaper, the bounds — `71-browser-outbox.md` | the server-side outbox, its three row states, dedupe and DLQ replay: `/alaa-async-messaging` (`$alaa-async-messaging`), `references/20-publishing-and-the-outbox.md` |
| in-app download | quota, persistence, eviction, concurrency, partial-download detection — `72-offline-media-store.md` | what the player stores, fetches and licenses: `/alaa-shaka-player` (`$alaa-shaka-player`) |
