# The Storage Buckets API

Read this when a design says "storage bucket", or when one data class on the device must outlive another
under storage pressure.

## What it is

By default an origin has one bucket and eviction is all-or-nothing across it: IndexedDB, Cache API and OPFS
go together. The Storage Buckets API lets an origin create several named buckets, each with its own
persistence, durability and eviction disposition, so the browser can delete the prefetch bucket and keep the
drafts bucket.

```ts
const drafts = await navigator.storageBuckets.open('drafts', {
  persisted: true,      // false is the default
  durability: 'strict', // 'relaxed' is the default
});
const request = drafts.indexedDB.open('alaa-client-storage', 3);
```

- `persisted` — `false` (default) or `true`; whether the bucket survives storage pressure.
- `durability` — `'relaxed'` (default) or `'strict'`. A relaxed bucket may forget writes completed in the
  last few seconds when power is lost; strict minimises that and is slower.
- `StorageBucket.indexedDB` is the shipped storage surface. Cache API and File API integration are described
  in the explainer as intended, not shipped.

Chrome for Developers, read 2026-07-28. An `expires` option is
`not documented (searched 2026-07-28)`; treat it as absent.

## Support, and what follows

Chromium 122+ (Chrome, Edge), Opera 108+, Samsung Internet 26+. **Absent in every version of Firefox and in
every version of Safari and iOS Safari.** caniuse 70.28% global, read 2026-07-28.

1. **Never make a bucket a requirement.** Every feature works with the default bucket. A design that only
   holds together when eviction is per-bucket fails for half the fleet's users.
2. **Feature-detect and fall through.**

   ```ts
   const bucket = 'storageBuckets' in navigator
     ? await navigator.storageBuckets.open(name, { persisted, durability })
     : null;
   const idb = bucket?.indexedDB ?? indexedDB;
   ```

3. **The same records must be findable in both shapes.** Store name, key path and record shape are
   identical whether a named bucket or the default one opened the database; the only difference is which
   `IDBFactory` was used. A migration that runs in one and not the other is the failure this prevents.

## When a bucket earns its complexity

Only when both hold: two data classes on the device have genuinely different survival requirements — an
unsent draft versus a refetchable prefetch — and the budget file records both; and losing the lower class
silently is acceptable while losing the higher one is not.

Otherwise use one bucket and the cleanup ladder in `31-quota-exceeded-and-cleanup.md`, which achieves the
same ordering under application control and works everywhere.

## What a bucket does not change

The origin's total quota — buckets partition eviction priority, not capacity
(`30-quota-model-and-budgets.md`). The security model — every bucket in the origin is readable by every
script in it, so `61-authority-boundary.md` applies to all of them unchanged. The user's ability to clear
site data, which removes every bucket.
