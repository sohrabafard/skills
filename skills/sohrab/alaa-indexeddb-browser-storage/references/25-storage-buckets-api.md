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
// Demonstration schema version; consumer names/versions require registration before adoption.
const request = drafts.indexedDB.open('alaa-client-storage', 4);
```

- `persisted` — `false` (default) or `true`; whether the bucket survives storage pressure.
- `durability` — `'relaxed'` (default) or `'strict'`. A relaxed bucket may forget writes completed in the
  last few seconds when power is lost; strict minimises that and is slower.
- `StorageBucket.indexedDB`, `caches` and `getDirectory()` are recorded as supported from Chrome 122
  in [MDN BCD](https://github.com/mdn/browser-compat-data/blob/main/api/StorageBucket.json), read
  2026-09-29. Probe each surface used; the Chrome introduction's IndexedDB-only note is stale.

The [WICG draft](https://wicg.github.io/storage-buckets/), read 2026-09-29, defines `expires`
on `open()` and `expires()`/`setExpires()` on a bucket. The earlier unsuccessful search is not
absence evidence. Expiration can remove a persistent bucket too; never apply it to unsynced drafts.
`persisted: true` requests persistence: check `await bucket.persisted()` before promising it.
The draft omits the Chrome introduction's `durability` option; verify that option against the
target implementation rather than assuming a portable durability guarantee.

## Support, and what follows

MDN BCD read 2026-09-29 lists Chrome 122+, with Firefox and Safari `version_added: false`;
that is a dated compatibility observation, not a prediction about future versions or embedded runtimes.
The former 70.28% figure was a caniuse snapshot on 2026-07-28, not this fleet's user share.

1. **Never make a bucket a requirement.** Every feature works with the default bucket. A design that only
   holds together only when eviction is per-bucket is not portable.
2. **Feature-detect and fall through.**

   ```ts
   // For a new/refetchable store only; existing draft locations must be reconciled first.
   let idb = globalThis.indexedDB;
   try {
     if (typeof navigator !== 'undefined' && 'storageBuckets' in navigator) {
       const bucket = await navigator.storageBuckets.open(name, { persisted });
       idb = bucket.indexedDB;
     }
   } catch {
     // Report bucket unavailability without payloads; the default store still needs a write probe.
   }
   ```

3. **The two factories address separate databases even with identical names.** Keep schema and migration
   logic compatible with both, but never assume records move when capabilities change. Record the chosen
   location; reconcile or migrate existing unsynced work before changing it. A failed bucket open must
   not silently present an empty default database as if the user's drafts disappeared. If IndexedDB
   itself is unavailable, use the tier-0 recovery in `20-browser-compatibility-and-capability-tiers.md`.

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
