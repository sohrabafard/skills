# Local cache and drafts

The server owns the record. Local storage buys latency and survives a flaky network; it never becomes the
truth. The outbox is `71-browser-outbox.md`; offline media is `72-offline-media-store.md`.

## Read-through cache

This is the IndexedDB substrate for request caching. The service worker and Cache API side of the same job
is `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`),
`references/30-service-worker-excellence.md`.

**Which layer holds what.** The Cache API holds an HTTP `Request`/`Response` pair matched by URL — the
right home for a whole response the browser can replay. IndexedDB holds a parsed record addressable by key
and index — the one the application queries, filters and joins. **A response cached in both places has two
expiries and one of them will be wrong.** Choose one per endpoint and state which in the decision record.

```ts
type ApiCacheEntry<T> = {
  key: string;              // cacheKey + scope; the store's keyPath
  accountKey?: string;      // present whenever the response is user-scoped
  schema: number;
  urlFingerprint: string;
  value: T;
  etag?: string;
  serverRevision?: string;
  fetchedAt: string;
  expiresAt: string;        // indexed, for TTL cleanup
  lastAccessedAt: string;   // indexed with dataClass, for LRU cleanup
  bytesApprox: number;
};
```

What makes a cached record correct: a TTL on every entry **and** a server validator (`ETag`,
`serverRevision`, `updatedAt`) wherever the API offers one — a TTL with no validator means the cache is
wrong for exactly the TTL; `expiresAt` checked on read, not only by the sweep, because the sweep is
opportunistic and the read is the guarantee; validation on read per `62-poisoning-and-purge.md`;
`accountKey` on every user-scoped entry, or the next user on a shared device reads the previous user's
data; never a class `60-data-classification.md` forbids; never used to decide access
(`61-authority-boundary.md`). Stale-while-revalidate only where the product decided a stale render beats a
spinner — never for a price, a deadline, an entitlement or a submission state.

**Invalidation, layered.** TTL expiry; validator mismatch on revalidation; logout or account switch; a
domain event the application already receives; an application build or schema version change; the user's
explicit "clear local data".

**Bounds.** `apiCacheMaxEntries` and the byte cap come from the budget file
(`30-quota-model-and-budgets.md`); eviction within the cache is LRU by `lastAccessedAt`, then TTL.

## Drafts

User-generated unsynced work — the one class this pack never allows to be deleted silently.

- Key by `accountKey`, `targetType`, `targetId` and `draftType`, and index those segments so a route lists
  a user's drafts for one target in `O(log n + k)`.
- Save on a debounce, not per keystroke. `draftDebounceMs` default **750**, a configuration value named in
  `/alaa-services-contract` (`$alaa-services-contract`).
- Delete on submit **only after the server acknowledges**. A draft removed on optimistic submit is lost
  when the submit fails.
- On logout, ask before discarding or apply a retention policy the user has already seen
  (`62-poisoning-and-purge.md`).
- On a quota failure while saving a draft, **tell the user** (`31-quota-exceeded-and-cleanup.md`, class 1).
  A draft that silently failed to save is worse than one that never existed, because the user believes it
  is safe.
- Normalize user-entered text before storing so the stored and compared forms cannot diverge:
  `/alaa-input-normalization` (`$alaa-input-normalization`).

## Local state snapshots

Resume position, last-opened item, local progress. The server stays authoritative for anything that counts.
The snapshot exists so the UI renders instantly, and it is reconciled when the server response arrives.

| Entity | Conflict rule |
|---|---|
| analytics and watch events | idempotent append with an event id; the server dedupes |
| draft comment or answer | server revision wins; if the remote changed, show the user both |
| preferences | last write wins; low risk, simple UI |
| upload attachment state | server-authoritative state machine; the device holds only resume metadata |
| learning progress | the server's rule, usually maximum progress with event ordering |

## Offline wording

A contract with the user, checked in review.

| Say | When it is true |
|---|---|
| "Saved on this device" | the write completed and the transaction committed |
| "Will sync when online" | the item is in the outbox and a flush trigger exists |
| "Available offline on this device" | the asset is stored, verified present, and the tier supports playing it (`72-offline-media-store.md`) |
| "May be removed by your browser or by private browsing" | attached to any best-effort storage the user is invited to rely on |

Never say "downloaded" for a best-effort store without the removal sentence beside it, and never offer an
offline affordance at tier 0 or tier 1.

## Background jobs

Cleanup of expired cache, outbox flush, revalidation, compaction, lazy migration, storage-metadata
recomputation. Every one runs under a named Web Lock with `ifAvailable: true`, so several tabs and the
service worker do not all do it (`41-multitab-versionchange-and-locks.md`), is cancellable, and yields
between batches per `50-transactions-performance-and-query-patterns.md`.
