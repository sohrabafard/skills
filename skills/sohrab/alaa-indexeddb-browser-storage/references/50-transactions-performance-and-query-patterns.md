# Transactions, performance, and query patterns

## Performance model

IndexedDB is asynchronous and suitable for structured local storage, but it is not automatically fast. Performance depends on:

- transaction count
- record size
- number of indexes
- serialization/structured clone cost
- cursor vs bulk-read pattern
- main-thread pressure
- browser engine
- durability mode
- storage device and OS

Optimize by reducing round trips, indexing intentionally, batching writes, bounding reads, and moving heavy processing off the main thread.

## Transaction rules

- Use `readonly` for reads.
- Use `readwrite` only for writes.
- Include all stores needed for an atomic operation in one transaction.
- Keep transactions short.
- Avoid one transaction per record for batch writes.
- Do not wait for external async work inside a transaction.
- Always observe transaction completion/error, not just request success.

## Bulk writes

Bad:

```ts
for (const item of items) {
  const tx = db.transaction('api_cache_entries', 'readwrite');
  tx.objectStore('api_cache_entries').put(item);
  await txDone(tx);
}
```

Good:

```ts
const tx = db.transaction('api_cache_entries', 'readwrite');
const store = tx.objectStore('api_cache_entries');
for (const item of items) store.put(item);
await txDone(tx);
```

For very large batches, chunk:

```text
chunkSize = 100-1000 records depending on record size/device
yield between chunks
show progress if user-visible
stop when quota/battery/background constraints require
```

## Reads

### Use point reads for exact keys

```ts
store.get(id)
```

### Use indexes for common filters

```ts
store.index('byAccountUpdatedAt').openCursor(IDBKeyRange.bound([accountKey, from], [accountKey, to]))
```

### Use cursors for pagination/large reads

Cursors avoid loading everything into memory.

Use cursor when:

- result set may be large
- you need streaming/pagination
- you need fallback for older browsers
- you need to distinguish missing record from stored `undefined`

### Use `getAll`/`getAllKeys` only with bounds/count

Good:

```ts
index.getAll(range, 50)
```

Risky:

```ts
store.getAll() // may load a large store into memory
```

### `getAllRecords`

`getAllRecords()` can be faster by retrieving keys and values together, but it is experimental/limited. Only use behind feature detection with cursor or `getAll` + `getAllKeys` fallback.

## Index design

Indexes speed reads but slow writes and consume storage.

Create indexes for:

- filters used often
- sync scheduling (`status`, `retryAt`)
- account/project scoped queries
- LRU cleanup (`dataClass`, `lastAccessedAt`)
- TTL cleanup (`expiresAt`)
- conflict detection (`entityId`, `revision`)

Avoid indexes for:

- rarely queried fields
- high-churn volatile fields unless needed
- large text fields
- fields that can be computed cheaply from another index

## Compound key patterns

IndexedDB supports array keys. Use compound keys for multi-dimensional ordering.

Examples:

```ts
['accountKey', 'updatedAt']
['status', 'retryAt']
['dataClass', 'expiresAt']
['courseId', 'lessonId']
['entityType', 'entityId', 'clientMutationId']
```

Range query example:

```ts
IDBKeyRange.bound([accountKey, start], [accountKey, end])
```

## Record shape

Every durable record should have:

```ts
type BaseLocalRecord = {
  id: string;
  schema: number;
  accountKey?: string;
  createdAt: string;
  updatedAt: string;
};
```

For cache/outbox records add:

```ts
expiresAt?: string;
lastAccessedAt?: string;
bytesApprox?: number;
source?: 'server' | 'client' | 'derived';
serverRevision?: string | number;
clientMutationId?: string;
```

## Serialization and structured clone

Do not assume every JS value stores cleanly.

Avoid storing:

- class instances that rely on prototype methods
- functions
- DOM nodes
- large cyclic graphs unless intentionally supported/tested
- values that cannot be schema-validated later

Prefer plain JSON-like objects plus dates as ISO strings.

## Blob and large value policy

IndexedDB can store blobs, but large values amplify quota, serialization, and browser quirks.

Policy:

- Store metadata in IndexedDB.
- Use Cache API for HTTP response resources.
- Use OPFS for file-like content when supported and appropriate.
- If storing blobs in IDB is unavoidable, use strict budgets, test Safari/iOS, and implement cleanup.

## Durability mode

Modern IndexedDB supports durability hints:

- `relaxed`: better performance; commit event can happen before data is fully flushed to disk.
- `strict`: stronger flush behavior; slower; still not a magical guarantee against all failures.
- `default`: browser default.

Rules:

- Use default/relaxed for normal cache/outbox writes.
- Use strict only for critical migrations, handoff checkpoints, or local-only user data where the performance cost is justified.
- Feature-detect transaction options; fallback to default.
- Never use durability mode as a substitute for server sync.

## Workers

IndexedDB is available in workers in modern browsers. Use workers for:

- heavy import/export
- batch normalization
- local search index rebuilds
- compression/encryption work, if justified
- outbox serialization

Do not move logic to workers without considering:

- browser support in the target runtime
- message-passing cost
- cancellation
- versionchange handling
- test complexity

## Main-thread responsiveness

For UI apps:

- Avoid massive `getAll()` on startup.
- Lazy-load stores per route/feature.
- Use hydration/client-only guards in SSR environments.
- Debounce high-frequency writes.
- Batch progress events.
- Use `requestIdleCallback` only for optional cleanup and with fallback.
- Show a background status for long migrations or sync.

## Anti-patterns

- Storing the entire API response graph in one record without indexes.
- Loading full stores into memory on every route.
- Running network calls inside transactions.
- Treating request success as transaction success.
- Swallowing transaction errors.
- Creating too many indexes “just in case”.
- Using user-agent sniffing instead of feature detection.
- Using localStorage as a large IndexedDB fallback.
- Silent data loss for unsynced drafts.
