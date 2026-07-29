# Transactions, complexity budgets, and query patterns

## Complexity budgets

Every read and write path states the bound it holds as its input grows, in the comment above it and in the
feature's decision record. The doctrine — finding a bound from the system rather than assuming it, and
catching the N+1 family — is `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`). This
file states the bounds IndexedDB itself imposes.

`n` records in the store, `k` records the caller needs, `d` distinct keys in an index, `i` indexes.

| Operation | Bound | The trap |
|---|---|---|
| `store.get(key)` | `O(log n)`, one round trip | none |
| `store.getAll()` no argument | `O(n)` reads, `O(n)` memory | the whole store in memory; never on a store that grows with a user's history |
| `store.getAll(range, count)` | `O(log n + count)` | the `count` argument is not optional in review |
| `index.getAll(range, count)` | `O(log d + count)` | an index over an absent field is `O(1)` and always empty |
| cursor over a range, stopping at `k` | `O(log n + k)` | a cursor that continues past what it needs is `O(n)` with extra steps |
| cursor over the whole store, filtering in JS | `O(n)` | every one of these is an index that was not created |
| `store.count(range)` | `O(log n + matching)` | not free; never per rendered row |
| `put` into a store with `i` indexes | `O(i · log n)` | every index is maintained on every write |
| `n` puts in one transaction | one commit | correct |
| `n` puts in `n` transactions | `n` commits | the most common performance defect in this domain |

**Budgets this fleet holds.** Use a measured number where the path is measured; these until then.

- **No read on a user-facing route is `O(n)` in a store that grows with the user's history.** Learning
  state, drafts, outbox rows and cache entries all grow.
- **No view issues more than one transaction per render.** A read per list row is the N+1 family; the fix
  is one ranged read plus an in-memory join.
- **A logout purge is `O(matching + log n)` per store, never `O(n)`.** Every user-scoped store carries an
  index whose first segment is `accountKey`. A purge that full-scans is a *security* operation that may not
  finish before the device changes hands — `62-poisoning-and-purge.md`.
- **A cleanup sweep processes at most `cleanupBatchSize` records per pass**, default **500**, yielding
  between passes. **A bulk write chunks at `writeChunkSize` records per transaction**, default **200**,
  lower for large records. Both are configuration named in `/alaa-services-contract`
  (`$alaa-services-contract`).

## Transaction rules

- `readonly` for reads; `readwrite` serialises against every other `readwrite` on the same store.
- Name every store an atomic operation touches in one transaction. Two transactions have no atomicity
  between them.
- **Await transaction completion, not request success.** A request can succeed on a transaction that later
  aborts. `txDone` in `examples/idb-core.ts`.
- **No `await` of non-IndexedDB work inside an open transaction.**

```ts
// Bad — the transaction goes inactive during the fetch.
const tx = db.transaction('drafts', 'readwrite');
const store = tx.objectStore('drafts');
await fetch('/api/user');
store.put(record);                       // TransactionInactiveError

// Good — gather, then open, then queue synchronously.
const user = await fetchUserBeforeTransaction();
const tx2 = db.transaction('drafts', 'readwrite');
tx2.objectStore('drafts').put({ ...record, userId: user.id });
await txDone(tx2);
```

Awaiting one IndexedDB request inside its own transaction is legal — the request keeps the transaction
alive — but is discouraged here, because the microtask timing is engine-sensitive and one accidental
non-IDB await in the same chain breaks it.

## Bulk writes

```ts
const tx = db.transaction('api_cache_entries', 'readwrite');
const store = tx.objectStore('api_cache_entries');
for (const item of items) store.put(item);
await txDone(tx);
```

Beyond `writeChunkSize`, chunk and yield between chunks, show progress when user-visible, and stop at
`softStop` (`30-quota-model-and-budgets.md`).

## Index design

An index costs a write on every `put` and storage proportional to the field. Create one for: a filter a
user-facing route issues; `accountKey` as the first segment of every user-scoped store, for the purge
budget above; outbox scheduling `['status', 'nextAttemptAt']`; LRU cleanup `['dataClass', 'lastAccessedAt']`;
TTL cleanup `expiresAt`; conflict detection `['entityId', 'serverRevision']`.

Do not create one for a rarely queried field, a high-churn field, a large text field, or a field cheaply
derivable from an existing index.

**Before creating an index, read the record type and confirm every segment of the key path is a declared
field on it.** A key path naming an absent field produces a permanently empty index and no error —
`40-schema-and-migrations.md`.

## Compound keys and ranges

```ts
index.openCursor(IDBKeyRange.bound([accountKey, from], [accountKey, to]));   // one account, a time window
index.openCursor(IDBKeyRange.bound([accountKey], [accountKey, []]));         // everything under one prefix
```

The empty array sorts after every other key type, which is what makes the second form correct. That is the
range the logout purge and every per-account listing use.

Local cursor pagination is this skill's ground. The **contract** of a paged API — page size, continuation
token shape, ordering stability — is `/alaa-keyset-pagination` (`$alaa-keyset-pagination`); do not invent a
second one for the local mirror of a server-paged collection.

## Record shape

```ts
type BaseLocalRecord = {
  id: string;
  schema: number;          // validated on read; 62-poisoning-and-purge.md
  accountKey?: string;     // required on every user-scoped store
  createdAt: string;       // ISO 8601
  updatedAt: string;
};
```

Cache and outbox records add `expiresAt`, `lastAccessedAt`, `bytesApprox`, `serverRevision`,
`clientMutationId`. Store dates as ISO strings, not `Date`: they compare correctly as index keys, survive
structured clone unambiguously, and are readable in DevTools.

**Any user-entered text that will be stored or compared is normalized before it is written**, so the stored
form and the compared form cannot diverge. The form is `/alaa-input-normalization`
(`$alaa-input-normalization`); do not fold in this layer. Domain identifiers come from
`/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`); `crypto.randomUUID()` is acceptable only
for a value that never leaves the device, such as a throwaway test database name.

Structured clone drops functions, DOM nodes and prototype-dependent class instances. Store plain objects.
A `Blob` survives, subject to the 1 MB rule in `10-indexeddb-mental-model-and-boundaries.md`.

## Durability

`relaxed` (Chromium default since Chrome 121) commits before the write reaches disk; `strict` flushes and is
slower. Feature-detect the transaction options object and fall back to the engine default. Use `strict` only
for a migration checkpoint or a handoff record whose loss on power failure would be unrecoverable.
Durability is not a substitute for server sync: a strict write on an evicted origin is gone just the same.

## Workers

IndexedDB is available in dedicated, shared and service workers. Move heavy import and export, batch
normalisation, local index rebuilds and outbox serialisation there.

**Move compression or encryption to a worker when one main-thread invocation exceeds 16 ms measured on the
lowest-capability lane in `assets/browser-test-matrix.yaml`.** Below that the message-passing cost is not
repaid. `navigator.storage.persist()` is not available in workers (MDN, read 2026-07-28): request it from
the window and read the result from the `capabilities` store.

## Anti-patterns

`store.getAll()` with no bound on a growing store; one transaction per record in a batch; a network call
inside a transaction; treating request success as transaction success; a cursor filtering in JavaScript
where an index would answer; speculative indexes, each taxing every write; `localStorage` as a large-value
fallback.
