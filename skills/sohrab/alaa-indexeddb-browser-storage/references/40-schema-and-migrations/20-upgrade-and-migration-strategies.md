## The upgrade shape

```ts
request.onupgradeneeded = (event) => {
  const db = request.result;
  const tx = request.transaction!;
  const oldVersion = event.oldVersion;

  if (oldVersion < 1) {
    db.createObjectStore('meta', { keyPath: 'key' });
    db.createObjectStore('migration_journal', { keyPath: 'id' });
  }

  if (oldVersion < 2) {
    const outbox = db.createObjectStore('wa_outbox', { keyPath: 'id' });
    // Both segments must be declared fields on the record type.
    outbox.createIndex('byStatusNextAttemptAt', ['status', 'nextAttemptAt']);
  }

  tx.objectStore('meta').put({
    key: 'schemaVersion', value: event.newVersion, updatedAt: new Date().toISOString(),
  });
};
```

**An index whose key path names a field the record does not carry is silently empty.** IndexedDB does not
error: records lacking the key path are simply not indexed, so the query that index exists for returns
nothing forever. `BrowserOutboxItem` carries `nextAttemptAt`; an index over `['status', 'retryAt']` against
it would return an empty batch on every flush and the outbox would never drain, with no error anywhere.
**Before creating any index, read the record type and confirm every segment of the key path is a declared
field on it.** `scripts/capability_contract_conformance.py --check-indexes` asserts this across the pack's
examples.


## Migration strategies

**Additive — the default.** Create the new store or index; new code writes the new fields; old records are
transformed on read. Creating an index over existing rows still builds that index during the exclusive
upgrade; measure duration and quota failure on realistic storage sizes. An aborted upgrade preserves
the prior schema and rows; it does not make the upgrade cost-free.

**Lazy — for non-critical fields.** On read, detect the old shape, transform in memory, write the
normalised shape back in a short transaction outside the read. Count transformations and failures in
`migration_journal`; a lazy migration that never converges is one nobody is measuring.

**Shadow copy — for a change that cannot be additive.** Version `N` does only steps 1–3.

1. Create the new store in the upgrade transaction. Do not touch the old one.
2. After the open resolves, copy and transform in chunks outside the upgrade transaction, yielding between
   chunks.
3. Record progress in `migration_journal` after each chunk, so an interrupted copy resumes rather than
   restarts.
4. Switch reads to the new store only once the journal records the copy complete.
5. Delete the old store in version `N+1`, after telemetry shows the switch held.

A crash at any point leaves both stores intact and the journal states which is authoritative. That is the
property the split-transaction rule protects.
