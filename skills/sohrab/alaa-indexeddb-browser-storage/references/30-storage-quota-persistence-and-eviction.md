# Storage quota, persistence, and eviction

## Key principle

IndexedDB has no fixed universal size limit. It shares the browser's origin storage management with other APIs such as Cache API and OPFS. Quota and eviction depend on browser engine, OS, device free space, persistence mode, user interaction, privacy mode, and embedder.

Design as if local data can disappear, then improve reliability where browser capabilities allow.

## Storage bucket model

Quota is usually calculated for an origin or storage bucket, not only one IndexedDB database.

This means:

- IndexedDB, Cache API, OPFS, and other origin storage compete for space.
- Eviction can delete all data for an origin at once.
- Clearing site data clears IndexedDB too.
- Separate apps under the same origin/path may compete unless separated by origin.
- Cross-origin iframes may be partitioned and get smaller/different quotas.

## Best-effort vs persistent

Default storage is best-effort:

- No prompt is usually shown.
- Data persists while under quota and device storage is sufficient.
- Browser may evict under pressure.

Persistent storage:

- Request with `navigator.storage.persist()` where supported.
- Check with `navigator.storage.persisted()` where supported.
- In Firefox, a user prompt may appear.
- In many Chromium/Safari cases, the browser decides automatically based on user interaction/history.
- Persistent means browser should not silently evict; user can still delete data.

## Browser quota notes researched 2026-06-29

Treat these as planning estimates, not promises.

| Browser/engine | Planning note |
|---|---|
| Firefox | Best-effort quota is the smaller of 10% total disk size or 10 GiB group limit. Persistent storage can allow up to 50% of disk, capped at 8 TiB, and avoids group limit. |
| Chromium/Chrome/Edge | Origin may use up to about 60% of total disk in persistent and best-effort modes; actual reachable storage may be lower because quota is privacy-padded and disk free space matters. Browser-wide storage may have a broader cap. |
| Safari/WebKit modern | Starting macOS 14/iOS 17, WebKit browser apps may allow around 60% of total disk per origin; embedded non-browser apps around 15%; browser-wide overall quota around 80%, embedded around 20%. Cross-origin frames get a fraction of main-frame quota. |
| Earlier Safari | Initial origin quota may be around 1 GiB before user permission prompt. Do not assume large quota on older Safari. |
| Private/incognito | Quota can be reduced; data usually deleted when private session ends. |

## Required quota workflow

Before storing large or durable data:

1. Estimate current usage and quota:

```ts
const estimate = await navigator.storage?.estimate?.();
```

2. Classify data into buckets:

- critical unsynced user data
- resumable outbox
- drafts
- cache metadata
- refetchable cache
- large binary/resource metadata

3. Assign budgets:

```text
critical unsynced: never evict automatically without server sync/user warning
outbox: hard cap by item count and byte estimate
cache: LRU/TTL cleanup first
prefetch: disabled under low storage
```

4. Request persistence only after user intent:

- user enables offline mode
- user creates durable local drafts
- user has repeated app engagement
- data loss would be user-visible

5. Handle denial gracefully.

6. On every write path, handle quota errors and trigger cleanup.

## Storage budgets

Use a budget table per feature:

| Data class | Example budget | Cleanup rule |
|---|---:|---|
| Feature flags/config cache | < 2 MB | TTL replace |
| Learning state | < 20 MB | Per-user latest N courses |
| Drafts | < 50 MB | User-visible, never silent-delete unsynced |
| Analytics outbox | 10–100 MB or item-count bounded | Batch retry, drop only low-value telemetry after policy |
| Metadata cache | 50–500 MB | LRU + TTL |
| Large resource metadata | Small; raw file elsewhere | LRU and policy-based |

Budget by percentage too:

```text
softStop = min(200MB, 5% of estimated quota)
hardStop = min(500MB, 10% of estimated quota)
```

Adjust numbers to product reality and device class.

## QuotaExceededError handling

Every storage write should be inside a path that can catch and classify quota errors.

Response order:

1. Stop optional prefetch/cache writes.
2. Run LRU/TTL cleanup for refetchable cache.
3. Retry the write once after cleanup.
4. If still failing, reduce feature tier.
5. Preserve unsynced user data ahead of refetchable data.
6. Show user-facing storage guidance only when action is needed.
7. Log a non-PII telemetry event.

Never swallow quota errors silently for user-generated unsynced data.

## Eviction resilience

The app must survive complete origin-storage loss.

On app boot:

- Detect DB missing or schema fresh install.
- Recreate schema.
- Rehydrate from server when online.
- Mark local-only unsynced features as unavailable until the user resumes.
- Do not assume local entitlements or access grants remain valid.
- Resync caches incrementally.

## Safari/WebKit proactive eviction

Safari/WebKit can proactively evict script-created data for origins without recent user interaction when cross-site tracking prevention is enabled. Practical response:

- Do not promise indefinite offline availability on Safari without testing and clear UX.
- Keep server as source of truth.
- Encourage real user interaction before storing important local data.
- Use persistent storage where supported, but still test.
- On return after inactivity, validate local storage and repair state.

## Private/incognito behavior

Private mode can make storage available but ephemeral.

Rules:

- Run a write/read/delete probe.
- Do not promise persistence.
- Keep budgets tiny.
- Avoid “download/offline available later” language.
- Show a subtle warning only for features that rely on persistence.

## Cleanup design

Maintain a `storage_items` or per-store metadata index for cleanup:

```ts
type StorageItemMeta = {
  id: string;
  store: string;
  accountKey: string;
  bytesApprox: number;
  dataClass: 'critical' | 'draft' | 'outbox' | 'cache' | 'prefetch';
  createdAt: string;
  updatedAt: string;
  lastAccessedAt: string;
  expiresAt?: string;
  refetchable: boolean;
};
```

Cleanup order:

1. Expired refetchable cache.
2. Old prefetch data.
3. LRU metadata cache.
4. Completed outbox events.
5. Failed low-priority telemetry after retention policy.
6. Never silent-delete unsynced user drafts.

## User-facing UX

For storage-heavy features, provide:

- “Storage used” estimate.
- “Clear offline data/cache” action.
- Per-feature delete controls.
- Explanation that browser/private mode/site-data clearing can remove local data.
- Re-download/re-sync affordance.

## Observability

Log these locally and/or server-side without PII payloads:

- capability tier
- estimated usage/quota bucketed, not exact if privacy-sensitive
- persistence requested/granted/denied
- quota exceeded
- cleanup count/bytes estimate
- DB open failures
- DB missing after previous use
- migration duration/errors
- outbox backlog size and oldest age
