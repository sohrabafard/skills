# Full guide: Alaa IndexedDB Browser Storage

Generated from references on 2026-06-29. Prefer loading smaller reference files during agent execution.


---

<!-- source: references/00-topic-map.md -->


# Topic map

Load the smallest reference that answers the current task. Do not load the full guide unless necessary.

## Decision/routing

| Need | Load |
|---|---|
| Authoritative source order, freshness, current browser claims | `05-source-priority-and-freshness.md` |
| Decide whether IndexedDB is the right storage API | `10-indexeddb-mental-model-and-boundaries.md` |
| Browser/version compatibility, progressive enhancement, feature probes | `20-browser-compatibility-and-capability-tiers.md` |
| Quotas, persistent storage, eviction, private mode, cleanup budgets | `30-storage-quota-persistence-and-eviction.md` |
| DB schema, object stores, migrations, multi-tab upgrade safety | `40-schema-versioning-migrations-and-concurrency.md` |
| Transactions, performance, indexes, read/write patterns, durability | `50-transactions-performance-and-query-patterns.md` |
| Security, privacy, auth-token, PII, logout purge, shared device | `60-security-privacy-and-data-classification.md` |
| Offline sync, outbox, drafts, local cache, conflict handling | `70-offline-sync-outbox-cache-patterns.md` |
| Testing, DevTools, instrumentation, release readiness | `80-testing-debugging-and-observability.md` |
| Agent workflow, prompt patterns, output templates | `90-agent-workflows-prompts-and-output-contracts.md` |
| Alaa integration and service-boundary mapping | `95-alaa-integration-playbook.md` |
| Source map and maintenance schedule | `99-sources-and-maintenance.md` |

## Code examples

| Example | Purpose |
|---|---|
| `examples/browser-capabilities.ts` | Runtime capability detection and probes |
| `examples/idb-core.ts` | Low-level Promise wrappers, open/upgrade, transaction helpers |
| `examples/migration-pattern.ts` | Versioned schema/migration pattern |
| `examples/quota-manager.ts` | Storage estimate, persistence request, budget checks |
| `examples/outbox-pattern.ts` | Idempotent offline outbox sync pattern |
| `examples/alaa-client-storage.ts` | App-level storage facade and store naming |
| `examples/fallback-memory-store.ts` | Minimal fallback when IDB is unavailable |
| `examples/vitest-idb-pattern.test.ts` | Unit-test pattern with fake IndexedDB style APIs |
| `examples/playwright-quota-smoke.spec.ts` | Browser smoke tests for storage behavior |

## Templates/assets

| Asset | Purpose |
|---|---|
| `assets/indexeddb-decision-record-template.md` | ADR template for a storage feature |
| `assets/indexeddb-feature-plan-template.md` | Implementation plan skeleton |
| `assets/storage-budget-policy-template.md` | Quota/budget cleanup policy |
| `assets/browser-test-matrix.yaml` | Cross-browser manual/automated test matrix |
| `assets/data-classification-policy.yaml` | Storage security classification template |
| `assets/capability-tier-contract.json` | Capability tier contract |
| `assets/alaa-indexeddb-adr.md` | Alaa-specific ADR starter |


---

<!-- source: references/05-source-priority-and-freshness.md -->


# Source priority and freshness

## Research policy

Browser storage behavior changes by browser engine, browser version, operating system, privacy mode, storage pressure, and embedder. For any task that asks for current limits, version support, Safari/iOS behavior, experimental APIs, or “latest” behavior, refresh sources before implementation.

## Source hierarchy

Use this order:

1. W3C/WHATWG specs for API semantics and terminology.
2. MDN Web Docs for cross-browser API behavior, compatibility, quota/eviction guides, and security notes.
3. Browser-vendor docs for engine-specific policy:
   - Chrome Developers / Chromium docs.
   - WebKit blog / WebKit bugs for Safari/WebKit.
   - Firefox/MDN/Bugzilla for Gecko-specific behavior.
4. Can I Use / Browser Compatibility Data for support tables and usage share.
5. Official library docs for wrappers (`idb`, Dexie, localForage, RxDB) when the task uses those libraries.
6. Issue trackers and community reports for bug symptoms only. Treat them as signals, not final truth, unless reproduced.

## Freshness gates

Refresh official sources when any of these are true:

- User asks for browser versions, current quotas, Safari/iOS behavior, storage persistence, experimental APIs, or “latest”.
- Source data is older than 6 months for compatibility/quota claims.
- The feature involves large offline storage, persistent storage, private mode, embedded webview, third-party iframe, or mobile Safari.
- The code will be released to production across broad browsers.
- A browser-specific workaround is proposed.

## What to record after research

For each browser-sensitive decision, record:

- Research date.
- Sources checked.
- Browser/OS versions or channels.
- Whether the claim is official, compatibility-data-backed, or empirical.
- Fallback behavior if the claim is wrong.
- Tests required to confirm in the target environment.

## Never overfit to one source

Do not implement a rule just because one blog post says so. Convert any community-reported bug into a test or feature probe. If official docs and empirical behavior conflict, document the conflict, prefer feature detection, and add a runtime fallback.

## Skill-authoring compatibility

This pack follows agent-skill best practices:

- Keep `SKILL.md` routing-first and concise.
- Put heavy context into `references/`.
- Put deterministic reusable code in `scripts/` or `examples/`.
- Use explicit workflows, checklists, and output contracts.
- Prefer source-linked maintenance notes over model-memory claims.


---

<!-- source: references/10-indexeddb-mental-model-and-boundaries.md -->


# IndexedDB mental model and boundaries

## What IndexedDB is

IndexedDB is a browser-provided, asynchronous, transactional, object-oriented database scoped to an origin. It stores structured-clone-compatible JavaScript values, including objects and blobs, inside object stores keyed by primary keys and optional indexes.

Think of it as:

```text
Origin: https://app.example
└── Browser-managed storage bucket
    ├── IndexedDB databases
    │   ├── object stores
    │   ├── indexes
    │   └── records
    ├── Cache API entries
    ├── OPFS files
    └── other origin storage
```

IndexedDB is not SQL. It has no joins, no server-grade query planner, no global transactions across origins, no permission model inside one origin, and no guarantee that data survives user deletion or browser eviction.

## Core constructs

- Database: named database with integer version.
- Object store: keyed collection of records; key can be inline via keyPath or out-of-line.
- Index: secondary lookup structure over one key path or array key path.
- Transaction: readonly/readwrite/versionchange scope over one or more object stores.
- Request: asynchronous operation with success/error events.
- Cursor: streaming iteration over keys/values/ranges.
- Structured clone: serialization mechanism; not all JS values are storable.
- Origin: scheme + host + port boundary; quota generally applies to the origin/bucket, not a single DB.

## What IndexedDB is good for

Use IndexedDB for:

- Durable-ish app data that is too large or structured for `localStorage`.
- Offline state, drafts, local user progress, and pending sync outbox.
- Metadata catalogs for cached resources.
- Queryable local collections with indexes.
- App-state snapshots that can be refetched or resynced.
- Cross-worker/main-window storage coordination when designed carefully.

## What IndexedDB is not good for

Do not use IndexedDB for:

- Access tokens, refresh tokens, session secrets, payment secrets, or private keys that become dangerous if JavaScript can read them.
- Source-of-truth entitlement, authorization, billing, identity, or irreversible business truth.
- Large raw files when Cache API or OPFS is a better abstraction.
- Full-text search without an index/search layer.
- Analytics data lake replacement.
- Highly relational query workloads that need joins and server-side constraints.
- Guaranteed write-on-unload behavior.

## Storage API decision framework

| Need | Preferred API | Notes |
|---|---|---|
| Structured records, indexes, offline state, outbox | IndexedDB | Primary focus of this skill |
| Static network resources and HTTP response caching | Cache API | Usually via Service Worker |
| File-like large binary content | OPFS or Cache API | Use IndexedDB for metadata when needed |
| Small tab-scoped values | sessionStorage | Synchronous; keep tiny |
| Small cross-navigation non-sensitive strings | localStorage only if unavoidable | Synchronous; blocks main thread; tiny only |
| Server/client request state | Cookies | Keep minimal; cookies are sent with requests |
| Credentials/session authority | HttpOnly secure cookies/server session | Not IndexedDB |

## Source-of-truth rule

Before creating an IndexedDB object store, answer:

1. Can this data be reconstructed from the server?
2. What is the user-visible harm if it disappears?
3. Is there a resync path?
4. Is the backend still authoritative?
5. Is the data safe to expose to any script running in the origin?

If the answer to 5 is no, do not store it in IndexedDB without a security review.

## Progressive enhancement principle

Design for consistent core behavior:

- Baseline browsers get core functionality and safe degradation.
- Modern browsers get persistent-storage requests, better quota estimates, improved bulk APIs, background sync, workers, or OPFS where applicable.
- Powerful devices get larger local budgets, larger prefetch windows, and better local search/indexing.
- Low-end or private-mode environments get smaller budgets, fewer retained records, and clear UX about reduced offline reliability.

## Agent design default

When a user asks for an IndexedDB feature, the agent should produce a decision record before code:

```text
Feature:
Data classes:
Source of truth:
Required lifetime:
Object stores:
Indexes:
Quota budget:
Eviction recovery:
Security posture:
Browser capability tiers:
Migration plan:
Test matrix:
```


---

<!-- source: references/20-browser-compatibility-and-capability-tiers.md -->


# Browser compatibility and capability tiers

## Compatibility stance

IndexedDB is widely available in modern browsers, but feature depth, quota policy, persistence, private mode behavior, transaction timing, and embedded webview behavior differ.

Use this policy:

1. Feature-detect at runtime.
2. Probe by opening and writing to a tiny test DB when reliability matters.
3. Prefer capability tiers over browser names.
4. Use user-agent/version checks only as a last-resort workaround for a reproduced engine bug.
5. Keep a server-resync or graceful-degradation path.

## Browser family notes researched 2026-06-29

| Browser/engine | Practical guidance |
|---|---|
| Chromium: Chrome, Edge, many Android browsers | Strong IndexedDB support. Quota is large but not guaranteed. Chrome changed default readwrite durability to relaxed from Chrome 121. Chrome has ongoing storage optimizations; do not depend on exact internal storage format. |
| Firefox/Gecko | Strong support. Firefox has relaxed durability guarantees since Firefox 40. Persistent storage can change quota behavior significantly. Test ESR if enterprise users matter. |
| Safari/WebKit | Support exists, but WebKit storage policy, proactive eviction, iOS behavior, and embedded WKWebView limits require special testing. Safari 17/iOS 17 introduced updated quota and Storage API support. Earlier Safari versions may use an initial 1 GiB prompt behavior. |
| iOS/iPadOS browsers | Historically WebKit-based for all third-party browsers; EU iOS 17.4+ may allow alternate engines. Treat actual engine behavior as runtime-detected, not brand-detected. |
| Embedded webviews | Quotas and persistence may be smaller than browser apps. Test Capacitor/WKWebView/Android WebView separately from mobile browser. |
| Private/incognito modes | Quotas may be smaller; data usually disappears when the private session ends. Always detect and degrade. |
| Old IE/legacy Edge | Do not build new features around them. If required, run a separate compatibility review and use a minimal fallback. |

## Capability tiers

### Tier 0 — No reliable local DB

Conditions:

- `indexedDB` missing.
- Opening/writing a tiny test DB fails.
- Private mode or policy blocks storage.
- User/browser clears storage aggressively.

Allowed UX:

- In-memory session state only.
- Server-first operations.
- No offline promise.
- Small non-sensitive fallback only when explicitly accepted.

### Tier 1 — Core IndexedDB

Required capabilities:

- Open DB.
- Create object stores/indexes in upgrade transaction.
- Read/write simple structured-clone records.
- Use cursors and key ranges.
- Handle transaction errors.

Allowed UX:

- Drafts, preferences, small local caches, resumable UI state.
- Conservative outbox with clear retry limits.
- Small, evictable offline metadata.

### Tier 2 — Modern storage management

Additional capabilities:

- `navigator.storage.estimate()`.
- `navigator.storage.persist()` and `navigator.storage.persisted()` when available.
- `getAll` / `getAllKeys` or equivalent fallback.
- Better multi-tab coordination with `BroadcastChannel` or similar.

Allowed UX:

- User-visible storage budgets.
- Persistent-storage request after user demonstrates intent.
- More reliable offline-critical state.
- LRU cleanup with estimated free space.

### Tier 3 — Enhanced offline/local-first

Additional capabilities may include:

- Workers for heavy serialization/query processing.
- OPFS or Cache API for large file/resource storage.
- Background Sync / Periodic Sync when supported.
- `navigator.locks`, `BroadcastChannel`, or robust app-level coordination.
- Larger device/storage budget based on runtime estimates.

Allowed UX:

- Rich offline mode.
- Larger prefetch/caches.
- Faster local search/index refresh.
- Better background sync and resumability.

## API feature guidance

| Feature | Rule |
|---|---|
| `indexedDB` global | Check existence, then perform real open/write probe. |
| `IDBObjectStore.getAll()` | Use for bounded reads; fallback to cursor. |
| `IDBObjectStore.getAllKeys()` | Widely available in modern browsers; fallback to cursor for old/buggy environments. |
| `IDBObjectStore.getAllRecords()` | Experimental/limited; never require it for production. Use only behind feature detection. |
| `IDBTransaction.durability` / transaction options | Feature-detect. Default behavior differs historically. Use `strict` sparingly for critical migrations/checkpoints. |
| `indexedDB.databases()` | Nice-to-have for diagnostics/cleanup, not required. Feature-detect. |
| `IDBDatabase.close()` | Always close stale connections on `versionchange`. |
| `IDBTransaction.commit()` | Feature-detect; do not require. Let auto-commit work. |

## Runtime feature probe contract

Every serious feature should expose a capability object like:

```ts
interface BrowserStorageCapabilities {
  indexedDb: 'unavailable' | 'core' | 'modern';
  testedWrite: boolean;
  estimate: boolean;
  persist: boolean;
  persisted: boolean | 'unknown';
  getAll: boolean;
  getAllKeys: boolean;
  getAllRecords: boolean;
  transactionDurability: boolean;
  databases: boolean;
  broadcastChannel: boolean;
  workerIdb: boolean | 'unknown';
  privateModeLikely: boolean | 'unknown';
}
```

Use `examples/browser-capabilities.ts` as the implementation starting point.

## Version handling rules

- Document minimum browser policy per product release, but execute by capability.
- For iOS/Safari, test real devices or a trusted device cloud for offline-critical flows.
- For Android WebView/Capacitor, test the embedded runtime, not just Chrome mobile.
- For Firefox ESR or enterprise browsers, include at least one ESR lane when B2B/school environments matter.
- For private/incognito, do not promise persistence.
- If using a new API such as `getAllRecords`, implement a fallback in the same PR.

## Progressive enhancement examples

| Feature | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Learning progress cache | Last open page only | Course-level recent state | Larger local timeline/search |
| Draft answers | Save drafts | Persist request after repeated use | Background sync and conflict UI |
| Analytics outbox | Small bounded queue | Quota-aware queue and batch sync | Worker-based serialization and backoff |
| Content metadata cache | TTL cache | ETag/If-None-Match + storage budget | Prefetch with user/device-aware limits |
| Attachments/upload metadata | Resume state only | Cleanup + retry telemetry | Worker/OPFS integration when appropriate |


---

<!-- source: references/30-storage-quota-persistence-and-eviction.md -->


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


---

<!-- source: references/40-schema-versioning-migrations-and-concurrency.md -->


# Schema versioning, migrations, and concurrency

## Non-negotiable migration rules

- All object store and index creation/deletion happens inside `onupgradeneeded` / upgrade transaction.
- Database version is a positive integer. Do not use semantic strings directly as IndexedDB versions.
- Migrations must be deterministic, idempotent where possible, and tested from every supported old schema.
- Do not perform network calls during upgrade transactions.
- Do not run long application logic in upgrade transactions.
- Never split a destructive migration into “clear in one transaction, refill in another” unless the empty state is acceptable after crash. Prefer a single transaction or a recoverable shadow-copy pattern.
- Keep old connections cooperative: close on `versionchange`; handle new open `blocked` event with UI or reload prompt.

## DB naming policy

Prefer one app DB per origin/app family, with account/project keys inside records:

```text
DB name: alaa-client-storage
DB version: integer
Record namespace: accountKey = projectId:userId or anonymous-session
```

Benefits:

- Fewer DBs to upgrade.
- Less risk of many stale per-user DBs.
- Easier global cleanup and telemetry.

Use separate DBs only when there is a concrete reason:

- Strong deletion boundary per user.
- Third-party library owns its own schema.
- Very large independent storage domain with separate lifecycle.

## Object store naming

Use stable, plural, domain-specific names:

```text
meta
storage_items
capabilities
api_cache_entries
learning_state
wa_outbox
drafts
upload_resume_state
notification_state
sync_cursors
migration_journal
```

Avoid generic names like `data`, `cache`, or `items` unless scoped by a DB used by one feature only.

## Schema metadata

Keep a `meta` store:

```ts
type DbMeta = {
  key: string;
  value: unknown;
  updatedAt: string;
};
```

Suggested keys:

- `schemaVersion`
- `appBuildId`
- `lastSuccessfulOpenAt`
- `lastMigrationFrom`
- `lastMigrationTo`
- `lastCleanupAt`
- `capabilitySnapshot`

## Upgrade pattern

Use explicit old-version branches:

```ts
request.onupgradeneeded = (event) => {
  const db = request.result;
  const tx = request.transaction!;
  const oldVersion = event.oldVersion;

  if (oldVersion < 1) {
    db.createObjectStore('meta', { keyPath: 'key' });
    db.createObjectStore('learning_state', { keyPath: 'id' });
  }

  if (oldVersion < 2) {
    const outbox = db.createObjectStore('wa_outbox', { keyPath: 'id' });
    outbox.createIndex('byStatusRetryAt', ['status', 'retryAt']);
  }

  if (oldVersion < 3) {
    const drafts = db.createObjectStore('drafts', { keyPath: 'id' });
    drafts.createIndex('byAccountUpdatedAt', ['accountKey', 'updatedAt']);
  }
};
```

## Data migration strategy

### Safe additive migration

Best case:

- Create new store/index.
- New code writes new fields.
- Old records are migrated lazily when read or during background maintenance.

### Shadow-copy migration

For risky schema changes:

1. Create new store.
2. Copy/transform records in chunks after open, not necessarily inside upgrade.
3. Mark migration status in `migration_journal`.
4. Switch reads after successful copy.
5. Delete old store in a later schema version after telemetry confirms success.

### Lazy migration

For non-critical fields:

- On read, detect old record shape.
- Transform in memory.
- Write back normalized shape in a short transaction.
- Track migration count and errors.

## Multi-tab/versionchange handling

Every connection must attach:

```ts
db.onversionchange = () => {
  db.close();
  notifyUserOrReload('A new version is available. Please refresh.');
};

db.onclose = () => {
  markStorageUnavailableOrReopen();
};
```

Open requests should attach:

```ts
request.onblocked = () => {
  showUpgradeBlockedMessage();
};
```

Use `BroadcastChannel` where available:

```text
channel: alaa-storage
messages:
- db-upgrade-starting
- db-upgrade-blocked
- db-upgrade-complete
- storage-cleared
- logout-purge
```

Fallback to `storage` events or polling only when necessary.

## Transaction lifetime discipline

IndexedDB transactions auto-commit when control returns to the event loop and there are no pending requests. Some engines, especially WebKit/Safari, are stricter about transaction inactivity. Therefore:

- Do not hold a transaction open across unrelated `await`s.
- Do not call network, timers, crypto import, compression, or UI APIs inside an active transaction and then resume using it.
- Gather data before opening a transaction.
- Queue all IDB requests synchronously inside the transaction scope.
- Await transaction completion after scheduling requests.

Bad:

```ts
const tx = db.transaction('drafts', 'readwrite');
const store = tx.objectStore('drafts');
await fetch('/api/user');
store.put(record); // may throw TransactionInactiveError
```

Good:

```ts
const user = await fetchUserBeforeTransaction();
const tx = db.transaction('drafts', 'readwrite');
tx.objectStore('drafts').put({ ...record, userId: user.id });
await txDone(tx);
```

## Concurrency and locking

IndexedDB serializes conflicting transactions, but application-level invariants still need design.

Rules:

- Use one transaction for related writes across stores.
- Use idempotency keys for outbox writes.
- Use monotonic revision or `updatedAt` for conflict detection.
- Avoid read-modify-write across separate transactions when correctness matters.
- For cross-tab singleton sync jobs, use `navigator.locks` if available, otherwise a lease record with expiry and owner ID.

Lease record example:

```ts
type StorageLease = {
  key: string;
  ownerId: string;
  expiresAt: number;
  heartbeatAt: number;
};
```

## Upgrade tests

For every schema version:

- Fresh install opens successfully.
- Upgrade from previous version succeeds.
- Upgrade from oldest supported version succeeds.
- Upgrade with a second tab open triggers `blocked` UX.
- Old tab receives `versionchange` and closes.
- Failed migration leaves recoverable state.
- User reload during migration does not corrupt critical data.
- Private mode and quota-limited mode fail gracefully.


---

<!-- source: references/50-transactions-performance-and-query-patterns.md -->


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


---

<!-- source: references/60-security-privacy-and-data-classification.md -->


# Security, privacy, and data classification

## Security model

IndexedDB is same-origin browser storage. Any JavaScript that runs in the origin can generally access that origin's IndexedDB unless the application has created a stronger isolation boundary.

Therefore:

- IndexedDB is not a secure secret store.
- XSS can read/modify IndexedDB.
- Malicious or compromised third-party scripts running in the origin can access it.
- Browser extensions, devtools, local malware, or shared-device users may expose data depending on environment.
- Client-side encryption only helps if keys are not available to attacker-controlled JavaScript.

## Never store

Do not store in IndexedDB:

- access tokens
- refresh tokens
- session secrets
- password-equivalent values
- payment credentials
- private keys that unlock server resources
- entitlement authority or grant truth
- unredacted high-risk PII unless specifically approved
- server signing secrets or API keys

Use server-side sessions, token-mediating backends, HttpOnly/Secure/SameSite cookies, short-lived server-issued URLs, and gateway-side authorization instead.

## Data classification

| Class | Examples | IndexedDB policy |
|---|---|---|
| Public cache | public course list, thumbnails metadata, static config | Allowed with TTL and versioning |
| User-private low risk | UI preferences, last-opened lesson, local filters | Allowed; purge on logout/account switch |
| User-generated unsynced | drafts, pending answers, comments before submit | Allowed with user-visible recovery and sync |
| Analytics/outbox | watch events, UX events, retry queue | Allowed if minimized, bounded, and idempotent |
| PII moderate/high | names, contact info, school info, support content | Minimize, encrypt only with meaningful key model, TTL, purge controls, security review |
| Secrets/credentials | tokens, passwords, session authority | Forbidden |
| Authorization truth | entitlements, paid access grants | Cache display hints only; never authoritative |

## Alaa auth boundary

For Alaa-style architecture:

- Authentication and profile truth belong to server/auth services.
- Gateway/trusted backend path verifies tokens and injects trusted context.
- Client storage may cache display state, but backend remains authoritative.
- Entitlement decisions must be revalidated server-side.
- IndexedDB may store `entitlementSnapshot` only as non-authoritative UX cache with TTL and server revision.

## Token-storage rule

If a task asks “can we put token in IndexedDB?” answer:

```text
No for access/refresh/session tokens. IndexedDB is readable by JavaScript in the origin; XSS turns it into token exfiltration. Use HttpOnly Secure SameSite cookies or a token-mediating backend/session design. Store only non-secret session display metadata if needed.
```

## Logout and account switch

On logout/account switch:

1. Stop sync loops.
2. Flush or discard according to data class.
3. Purge user-scoped stores or records by `accountKey`.
4. Clear in-memory caches.
5. Broadcast `logout-purge` to other tabs.
6. Close/reopen storage connections if needed.
7. Confirm no user-private records remain for the previous account.

Do not delete unsynced drafts silently unless the user explicitly chooses discard or policy says guest data is ephemeral.

## Shared devices

For students, schools, labs, family devices, or public computers:

- Provide “clear local data” controls.
- Purge on logout by default for user-private data.
- Avoid storing sensitive PII offline.
- Keep local previews minimal.
- Consider separate “remember on this device” consent for durable local data.
- Show warning in private/incognito or unmanaged shared-device flows only when user action matters.

## Local encryption

Client-side encryption can help for some local-at-rest threats, but not for XSS if the decryption key is available to JavaScript.

Use encryption only after answering:

- Where is the key generated?
- Where is the key stored?
- Can XSS read the key?
- Can the server recover data?
- What happens on password reset/device loss?
- Is encryption solving a real threat or just adding complexity?

Acceptable patterns:

- User-supplied passphrase not stored locally, for optional private notes.
- Platform-bound credentials/WebAuthn-derived flows after security review.
- Server-encrypted payloads cached locally where client cannot decrypt until authorized.

Do not claim local encryption makes token storage safe.

## Third-party scripts

Because scripts in the origin can access storage:

- Minimize third-party scripts on pages that access sensitive local data.
- Use CSP and Trusted Types where possible.
- Audit analytics/tag managers.
- Avoid giving untrusted scripts same-origin execution.
- Isolate untrusted content in sandboxed/cross-origin iframes.
- Validate all records read from IndexedDB; treat local storage as attacker-modifiable.

## Storage poisoning

IndexedDB data can be stale or maliciously modified.

Protect by:

- Schema-validating records before use.
- Treating cache records as untrusted input.
- Verifying server revisions/signatures when used for important UI.
- Expiring sensitive caches.
- Avoiding direct HTML injection from cached records.
- Keeping a `schema` field in records.

## Privacy and compliance

For user data stored locally:

- Minimize fields.
- Set retention/TTL.
- Provide local deletion controls.
- Include storage in privacy documentation.
- Ensure logout/account deletion clears local data on next app open where feasible.
- Do not log raw local payloads.
- Use bucketed telemetry for sizes and counts.

## Security review checklist

Before approving a new IndexedDB store:

- [ ] Data class identified.
- [ ] Source of truth identified.
- [ ] No tokens/secrets/authority stored.
- [ ] Record schema validated on read.
- [ ] TTL/retention defined.
- [ ] Logout/account-switch purge defined.
- [ ] Quota cleanup policy defined.
- [ ] XSS/third-party script exposure considered.
- [ ] User-visible recovery for unsynced data.
- [ ] Tests cover malicious/stale/old schema records.


---

<!-- source: references/70-offline-sync-outbox-cache-patterns.md -->


# Offline sync, outbox, cache, and drafts

## Golden rule

IndexedDB is a local reliability layer, not the product's source of truth. Server services own canonical data. Client storage improves UX under flaky networks, tab reloads, and low-latency reads.

## Pattern catalog

### 1. Read-through cache

Use for server data that can be refetched.

Record:

```ts
type ApiCacheEntry<T> = {
  key: string;
  accountKey?: string;
  urlFingerprint: string;
  value: T;
  etag?: string;
  serverRevision?: string;
  fetchedAt: string;
  expiresAt: string;
  lastAccessedAt: string;
  bytesApprox: number;
};
```

Rules:

- Use TTL and server validators (`ETag`, revision, `updatedAt`) when available.
- Do not cache sensitive payloads without data-classification approval.
- Invalidate by domain event or version when possible.
- On stale cache, show stale-while-revalidate only when UX accepts it.

### 2. Write-behind outbox

Use for events or user actions that must survive offline/retry.

Record:

```ts
type OutboxItem = {
  id: string;
  accountKey: string;
  endpointKey: string;
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body: unknown;
  idempotencyKey: string;
  status: 'pending' | 'inflight' | 'done' | 'failed' | 'dead';
  priority: 'critical' | 'normal' | 'low';
  attempts: number;
  nextAttemptAt: string;
  createdAt: string;
  updatedAt: string;
  lastError?: string;
  expiresAt?: string;
};
```

Rules:

- Every network mutation must be idempotent or have a client mutation ID.
- Never enqueue secrets.
- Keep queue bounded by item count, bytes, and age.
- Sync outside the transaction that reads queue items.
- Mark item state in a short transaction before and after network call.
- Use backoff with jitter.
- Use server conflict response to resolve, not blind overwrite.

### 3. Local draft

Use for user-generated unsent work.

Rules:

- Drafts are user-visible and protected from silent deletion.
- Include `accountKey`, `entityType`, `entityId`, `draftType`, and `updatedAt`.
- Purge on submit success only after server acknowledgment.
- On logout, ask before discarding unsynced drafts or bind them to a guest/account policy.

### 4. Learning state snapshot

Use for local resume/progress UI.

Rules:

- Backend remains source of truth for learning progress when submitted.
- Store local snapshot for instant resume.
- Enqueue progress events to outbox if network fails.
- Resolve server/client conflicts by monotonic progress policy and server rules.

### 5. Upload resume metadata

Use for resumable upload state metadata only.

Rules:

- Store upload session ID, target domain, file fingerprint, offset, status, and expiry.
- Do not make the upload service own target domain authorization.
- Target service must still claim/attach uploaded asset server-side.
- Purge expired/completed upload metadata.

## Sync lifecycle

Trigger sync on:

- app boot
- network `online`
- visibility change to visible
- successful auth/session refresh
- route entering relevant area
- manual retry
- background sync where available and tested

Do not depend only on background sync; browser support varies.

## Outbox sync algorithm

```text
1. Acquire sync lease for account/scope.
2. Read next due items by status + nextAttemptAt.
3. Mark batch as inflight with syncRunId.
4. Commit transaction.
5. Send network requests with idempotency keys.
6. For each result:
   - success -> mark done, store server ack/revision
   - retryable error -> pending with backoff
   - conflict -> failed/conflict and create UI resolution task
   - unauthorized -> pause account sync and require auth refresh
   - forbidden -> dead/failed after server confirmation
7. Release lease.
8. Emit metrics.
```

## Conflict resolution

Define per entity:

| Entity | Recommended strategy |
|---|---|
| Analytics/watch events | Idempotent append with event IDs; server dedupe |
| Draft answer/comment | Server revision + user conflict UI if remote changed |
| Preferences | Last-write-wins acceptable if low risk |
| Upload attach | Server-authoritative state machine |
| Learning progress | Server rule, often max progress with event ordering |

## Cache invalidation

Use layered invalidation:

- TTL expiration.
- Server revision/ETag mismatch.
- User logout/account switch.
- App build/storage schema version change.
- Domain event: course changed, comment updated, ticket status changed.
- Manual “clear local data”.

## Offline UX wording

Use precise UX language:

- “Saved on this device” for local drafts.
- “Will sync when online” for outbox-backed items.
- “Available offline on this device” only after persistence and storage checks if the content is truly usable offline.
- “May be removed by browser storage settings/private mode” for best-effort storage-heavy features.

## Data loss policy

- Refetchable cache may be deleted automatically.
- Completed telemetry may be compacted/deleted after upload.
- Low-priority telemetry may be dropped after retention/backlog limits if product accepts it.
- User-generated unsynced drafts must not be silently deleted.
- If local data cannot be saved due to quota, tell the user before they rely on it.

## Background jobs

Optional jobs:

- cleanup expired cache
- flush outbox
- revalidate stale cache
- compact completed outbox
- lazy migrate old records
- recompute storage metadata

Run jobs opportunistically and cancel safely. Use leases to avoid multiple tabs doing the same expensive work.


---

<!-- source: references/80-testing-debugging-and-observability.md -->


# Testing, debugging, and observability

## Test layers

### Unit tests

Use for:

- schema adapters
- record validation
- outbox state transitions
- quota error classification
- cleanup ordering
- migration functions

`fake-indexeddb`-style tests are useful but not enough. They do not reproduce Safari/WebKit quota/transaction timing/private mode behavior.

### Integration tests in real browsers

Use Playwright/WebDriver/BrowserStack/Sauce/real devices for:

- DB open/upgrade
- multi-tab `blocked`/`versionchange`
- private/incognito behavior
- quota/low-storage simulation where possible
- Safari/WebKit behavior
- mobile webviews/Capacitor if applicable

### Manual/device tests

Required for high-value offline or quota-heavy features:

- iOS Safari real device
- iPadOS if target users use tablets
- Android Chrome/Android WebView
- Firefox ESR if enterprise/school deployments matter
- low-end Android with constrained storage
- private/incognito sessions

## Core test matrix

Every IndexedDB feature should test:

- Fresh install.
- Existing DB same version.
- Upgrade from each supported old version.
- Upgrade blocked by old tab.
- Old tab receives `versionchange` and closes.
- DB unavailable/open failure.
- Quota exceeded during optional cache write.
- Quota exceeded during user draft save.
- Storage cleared between app sessions.
- Offline write then online sync.
- Unauthorized/expired session during sync.
- Logout/account switch purge.
- Stale/malicious old record validation.
- Private mode or ephemeral storage.
- Low-end performance with realistic record counts.

## Browser debug tools

Chrome/Edge:

- DevTools → Application → IndexedDB.
- DevTools → Application → Storage / Clear site data.
- `navigator.storage.estimate()` from console.

Firefox:

- DevTools → Storage Inspector.
- Test persistent permission prompt behavior.

Safari/WebKit:

- Safari Web Inspector → Storage.
- Test on real iOS/iPadOS when the feature depends on persistence or large quota.
- Validate behavior after app inactivity where relevant.

## Storage observability events

Emit privacy-safe telemetry:

```ts
type StorageTelemetryEvent =
  | { name: 'idb_open_success'; dbVersion: number; durationMs: number; capabilityTier: string }
  | { name: 'idb_open_error'; errorName: string; phase: 'open' | 'upgrade' | 'probe' }
  | { name: 'idb_upgrade_blocked'; fromVersion: number; toVersion: number }
  | { name: 'idb_upgrade_success'; fromVersion: number; toVersion: number; durationMs: number }
  | { name: 'storage_quota_estimate'; usageBucket: string; quotaBucket: string; persisted: boolean | 'unknown' }
  | { name: 'storage_quota_exceeded'; dataClass: string; operation: string }
  | { name: 'storage_cleanup_run'; deletedCount: number; bytesBucket: string; reason: string }
  | { name: 'outbox_backlog'; countBucket: string; oldestAgeBucket: string }
  | { name: 'outbox_sync_result'; successCount: number; retryCount: number; failCount: number };
```

Do not log raw record payloads, PII, tokens, URLs with sensitive query strings, or exact large storage estimates if fingerprinting/privacy risk matters.

## Performance budgets

Define per feature:

- DB open budget on app boot.
- Route-level read budget.
- Write debounce interval.
- Max transaction duration.
- Max records read per UI interaction.
- Migration duration threshold.
- Outbox sync batch size.

Example:

```text
DB open: < 100ms p75, < 500ms p95 on target devices
Route cache read: < 50ms p75 for recent learning state
Outbox flush batch: 25-100 items depending on payload size
Migration blocking: no user-blocking migration > 2s without progress/retry UX
```

## Failure-mode tests

Simulate:

- Transaction abort due to duplicate unique index.
- `QuotaExceededError` on write.
- Browser reload during outbox sync.
- Network success but local mark-done fails.
- Local mark-inflight succeeds but network never starts.
- Server accepts idempotency key twice.
- `onblocked` because another tab is open.
- DB deleted while app tab is open.

## Release checklist

Before shipping:

- [ ] Storage decision record exists.
- [ ] Data classification approved.
- [ ] Object stores/indexes documented.
- [ ] Feature detection implemented.
- [ ] Quota estimate and quota error paths tested.
- [ ] Cleanup policy implemented for refetchable data.
- [ ] Logout/account switch purge tested.
- [ ] Multi-tab upgrade behavior tested.
- [ ] Safari/iOS or WebKit test completed if supported.
- [ ] Private/incognito behavior checked.
- [ ] Unit tests cover migrations and stale records.
- [ ] Browser tests cover the user-critical flow.
- [ ] Observability events added without PII.
- [ ] User-visible copy is accurate about persistence/offline reliability.

## Debugging decision tree

```text
Problem: data missing
  -> Was storage cleared/evicted? Check meta lastSuccessfulOpenAt and server sync state.
  -> Is accountKey different? Check logout/account switch.
  -> Is schema version fresh? Check migration logs.
  -> Is private mode active? Check capability/probe.
  -> Did cleanup remove it? Check storage_items/audit event.

Problem: transaction inactive
  -> Did code await unrelated async work inside transaction?
  -> Is Safari/WebKit involved?
  -> Are IDB requests queued synchronously?

Problem: quota exceeded
  -> Estimate usage/quota.
  -> Identify data class.
  -> Cleanup refetchable cache first.
  -> Retry once.
  -> Reduce capability tier.

Problem: upgrade hangs
  -> Another tab has old connection.
  -> Ensure old tabs close on versionchange.
  -> Show blocked reload message.

Problem: slow route
  -> Avoid full-store getAll.
  -> Use index/range/cursor/count.
  -> Batch/debounce writes.
  -> Move heavy work to worker.
```


---

<!-- source: references/90-agent-workflows-prompts-and-output-contracts.md -->


# Agent workflows, prompt patterns, and output contracts

## Agent behavior principles

For GPT-style and Claude-style coding agents:

- Use precise role, scope, and stop criteria.
- Gather enough context, then act; do not over-search once the path is clear.
- Use progressive disclosure: load only relevant reference files.
- Prefer checklists and decision records for complex storage work.
- Make assumptions explicit when a detail is missing and not blocking.
- Verify code changes with tests or deterministic checks.
- For current browser/version facts, refresh official sources and cite/record them.
- Never hide uncertainty about browser-specific behavior; convert uncertainty into feature detection and tests.

## Default task workflow

For any IndexedDB feature request:

```text
1. Classify the feature.
2. Identify data classes and source of truth.
3. Select capability tiers and fallback behavior.
4. Design schema/object stores/indexes.
5. Define quota budget and cleanup policy.
6. Define security/privacy rules.
7. Define migration/multi-tab plan.
8. Define sync/offline/conflict behavior if relevant.
9. Implement with short transactions and feature detection.
10. Test with unit + browser matrix.
11. Add observability and operational notes.
```

## Output contract: architecture answer

Use this structure:

```markdown
## تصمیم

## داده‌ها و منبع حقیقت

## سطح قابلیت مرورگر و fallback

## طراحی IndexedDB

### DB
### Object stores
### Indexes
### Record schemas

## Quota / persistence / eviction

## امنیت و حریم خصوصی

## Migration و multi-tab

## Sync / conflict / recovery

## تست و observability

## ریسک‌ها و تصمیم‌های باز
```

## Output contract: code review

```markdown
## نتیجه review

## ایرادهای قطعی

## ریسک‌های browser compatibility

## ریسک‌های quota/eviction

## ریسک‌های security/privacy

## مشکلات migration/concurrency

## پیشنهاد patch

## تست‌های لازم
```

## Output contract: implementation plan

```markdown
## Goal

## Assumptions

## Files to change

## Schema changes

## Capability detection

## Write/read paths

## Cleanup and quota handling

## Migration path

## Tests

## Rollout and telemetry
```

## Prompt pattern: feature design

```text
Use $alaa-indexeddb-browser-storage.
Design an IndexedDB feature for [feature].
Constraints:
- supported browsers: [list]
- data classes: [draft/cache/outbox/etc]
- offline requirement: [none/basic/critical]
- sensitive data: [yes/no]
- expected records/bytes: [estimate]
Return a decision record, schema, quota plan, fallback tiers, security notes, and test matrix. Do not write implementation code unless necessary.
```

## Prompt pattern: implementation

```text
Use $alaa-indexeddb-browser-storage.
Implement [feature] in this repo.
Before editing, inspect current storage utilities and AGENTS.md.
Use feature detection, short transactions, quota handling, and migration-safe schema changes.
Do not store tokens/secrets.
Add or update tests for fresh install, upgrade, quota error, and unavailable storage.
Summarize files changed and remaining risks.
```

## Prompt pattern: browser compatibility audit

```text
Use $alaa-indexeddb-browser-storage.
Audit this IndexedDB code for Chrome/Edge, Firefox, Safari/iOS, private mode, and embedded webview differences.
Search official sources if making current compatibility claims.
Return: capability gaps, fallback plan, test matrix, and recommended code changes.
```

## Prompt pattern: quota/resilience audit

```text
Use $alaa-indexeddb-browser-storage.
Audit storage quota and eviction resilience for [feature].
Check budgets, cleanup order, QuotaExceededError handling, persistence request timing, private-mode behavior, and user-visible recovery.
Return concrete patch suggestions and tests.
```

## Prompt pattern: security audit

```text
Use $alaa-indexeddb-browser-storage.
Review local browser storage for secrets, PII, entitlement authority, cache poisoning, logout purge, shared-device risk, and XSS exposure.
Return must-fix issues, acceptable data classes, and a revised storage policy.
```

## Clarification policy

Ask clarifying questions only when a missing detail changes the safety or architecture materially, such as:

- whether data is secret/PII
- whether offline persistence is critical
- required browser support including Safari/iOS/webview
- expected data volume
- whether server has idempotency/conflict APIs

If not blocking, proceed with explicit assumptions and mark them as assumptions.

## Agent anti-patterns

- Jumping straight to Dexie/raw IDB code without data classification.
- Assuming IndexedDB quota is “unlimited”.
- Assuming `navigator.storage.estimate()` is exact.
- Promising offline durability in private mode.
- Implementing a feature only tested in Chrome.
- Storing auth tokens because “IndexedDB is not localStorage”.
- Using user-agent checks as primary logic.
- Ignoring `blocked`/`versionchange`.
- Running fetch inside a transaction.
- Treating local entitlement cache as authoritative.
- Omitting cleanup and quota tests.

## Review rubric

Score each from 0 to 2:

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Source of truth | unclear | partially defined | server/client boundaries explicit |
| Security | secrets/PII risk | partial controls | classification + purge + validation |
| Compatibility | Chrome-only | some fallback | capability tiers + tests |
| Quota | ignored | catches errors | budgets + cleanup + UX |
| Migration | ad hoc | upgrade works one path | tested multi-version + blocked handling |
| Transactions | unsafe awaits | mostly safe | short, batched, transaction-complete-aware |
| Offline/sync | fragile | retry basic | idempotent, bounded, conflict-aware |
| Observability | none | errors only | privacy-safe metrics and runbooks |

Require score 2 for security and quota before production storage-heavy rollout.


---

<!-- source: references/95-alaa-integration-playbook.md -->


# Alaa integration playbook

## Architectural alignment

Alaa-style client storage must respect platform service ownership:

- Client applications call public routes through the gateway.
- Gateway/auth paths remain the trust boundary for identity and protected access.
- `auth` owns identity/profile/session truth.
- `content` owns course/set/content learning-content truth.
- legacy playback/domain responsibilities may still exist during migration.
- `wa` owns watch/analytics ingestion.
- `tusd` owns resumable upload transfer lifecycle, while target services own domain attachment.
- Comments, tickets, notifications, and other domains own their own state.

IndexedDB should improve frontend resilience and UX, not replace these service boundaries.

## Recommended Alaa client DB

```text
DB: alaa-client-storage
Version: integer
Namespace: accountKey = projectId:userId or anonymous-session
```

Suggested stores:

| Store | Owner concept | Use |
|---|---|---|
| `meta` | client storage | schema/capability metadata |
| `storage_items` | client storage | quota cleanup metadata |
| `api_cache_entries` | gateway-backed APIs | TTL/ETag/revision cache metadata |
| `learning_state` | content/learning UX | local resume, last viewed, local progress snapshot |
| `wa_outbox` | wa | watch/analytics events waiting for ingestion |
| `drafts` | comment/ticket/quiz/etc | unsynced user drafts |
| `upload_resume_state` | tusd + target service | upload session metadata and cleanup |
| `notification_state` | notification/realtime | local read/unread display cache |
| `sync_cursors` | client sync | per-service cursors/checkpoints |
| `capabilities` | client storage | runtime feature probe result |

## Use cases

### Learning state

Store:

- courseId, setId, contentId, lessonId
- local position/progress snapshot
- last opened timestamp
- server revision when available
- sync status

Rules:

- The backend remains source of truth for official progress.
- Local state can make resume instant.
- Conflicts follow server progress rules.
- Purge on logout/account switch.

### Watch analytics outbox

Store events when offline or network fails:

```ts
type WatchAnalyticsOutboxItem = {
  id: string;
  accountKey: string;
  eventType: string;
  contentId: string;
  occurredAt: string;
  body: unknown;
  idempotencyKey: string;
  status: 'pending' | 'inflight' | 'done' | 'failed' | 'dead';
  attempts: number;
  nextAttemptAt: string;
};
```

Rules:

- Use idempotency keys.
- Bound queue by count/age/bytes.
- Drop only according to analytics retention policy.
- Never block learning UI on low-priority event flush.
- Do not store unnecessary PII in event payload.

### API/cache metadata

For course/content metadata:

- Cache only server-shaped DTOs or normalized records.
- Use TTL and server validators.
- Do not cache access authority as truth.
- Invalidate when project/account/content revision changes.

### Drafts

For comments, tickets, quiz answers, support messages:

- Save local drafts with explicit accountKey and target entity.
- Never silently delete unsynced drafts.
- On submit success, delete only after server acknowledgment.
- On account switch/logout, apply user-visible policy.

### Upload resume metadata

For resumable uploads:

- Store upload URL/session ID, target service, local file fingerprint, offset, expiresAt.
- Target service must authorize/claim attachment server-side.
- Cleanup expired/completed sessions.
- Do not store full sensitive attachments in IndexedDB unless reviewed.

### Notifications/realtime

For local notification state:

- Cache read/unread and last delivered cursor for UX.
- Server remains source of truth.
- Reconcile on app boot and reconnect.
- Use IndexedDB to avoid losing local read interactions under flaky network.

## Alaa security rules

- Do not store auth tokens in IndexedDB.
- Do not trust client-cached entitlement for protected access.
- All protected API calls go through the gateway/session model.
- Any local record read from IndexedDB must be treated as untrusted input.
- User-scoped data must include accountKey and be purged on logout/account switch.

## Recommended package boundary

Create a frontend package/module such as:

```text
src/storage/
  index.ts
  db.ts
  capabilities.ts
  quota.ts
  schemas.ts
  migrations.ts
  stores/
    learning-state.ts
    wa-outbox.ts
    drafts.ts
    api-cache.ts
    upload-resume-state.ts
  sync/
    outbox-runner.ts
    leases.ts
  testing/
    fixtures.ts
```

Expose only domain-safe methods:

```ts
storage.learningState.save(snapshot)
storage.learningState.getLast(accountKey)
storage.waOutbox.enqueue(event)
storage.waOutbox.flush({ signal })
storage.drafts.save(draft)
storage.drafts.listByTarget(accountKey, target)
storage.quota.getStatus()
storage.clearUserData(accountKey)
```

Avoid exposing raw `IDBDatabase` to feature code unless the storage module itself is being developed.

## Implementation sequence

1. Add storage capability probe.
2. Add storage facade and schema v1.
3. Add data classification and accountKey enforcement.
4. Implement one low-risk store first, e.g., learning state or drafts.
5. Add quota metadata and cleanup.
6. Add outbox pattern for analytics/events.
7. Add multi-tab upgrade UX.
8. Add real browser tests, including Safari/iOS if target users require it.
9. Add privacy-safe telemetry.
10. Expand to more features only after reliability evidence.

## Alaa-specific ADR trigger

Create an ADR when:

- feature stores more than 50 MB per user/device
- feature stores user-generated unsynced data
- feature relies on offline mode
- feature stores moderate/high PII
- feature needs Safari/iOS parity
- feature needs background sync
- schema migration is destructive
- local data affects billing/access/entitlement UI

Use `assets/alaa-indexeddb-adr.md`.


---

<!-- source: references/99-sources-and-maintenance.md -->


# Sources and maintenance

Last researched: 2026-06-29.

## Authoritative sources consulted

### IndexedDB API and semantics

- MDN IndexedDB API: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API
- MDN Using IndexedDB: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- W3C Indexed Database API 3.0: https://www.w3.org/TR/IndexedDB/

### Browser storage quota, persistence, and eviction

- MDN Storage quotas and eviction criteria: https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
- web.dev Storage for the web: https://web.dev/articles/storage-for-the-web
- WebKit Updates to Storage Policy: https://webkit.org/blog/14403/updates-to-storage-policy/

### Browser support and newer/experimental APIs

- Can I Use IndexedDB API: https://caniuse.com/mdn-api_indexeddb
- MDN Window.indexedDB: https://developer.mozilla.org/en-US/docs/Web/API/Window/indexedDB
- MDN IDBTransaction.durability: https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability
- Chrome Developers: IndexedDB default durability mode change: https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed
- Chrome Developers: More efficient IndexedDB storage in Chrome: https://developer.chrome.com/docs/chromium/indexeddb-storage-improvements
- MDN IDBObjectStore.getAllKeys: https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAllKeys
- MDN IDBObjectStore.getAllRecords: https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAllRecords

### Skill/prompt authoring sources

- OpenAI Prompt engineering guide: https://developers.openai.com/api/docs/guides/prompt-engineering
- OpenAI GPT-5 prompting guide: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
- Anthropic Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Claims embedded in this skill

- IndexedDB is a low-level async API for significant structured client-side data, including files/blobs; it uses indexes and follows same-origin policy.
- Browser storage quotas and eviction differ between browsers and apply at origin/storage-bucket level.
- Best-effort storage is default; persistent storage can be requested with the Storage API where supported.
- Private browsing modes may apply different quotas and usually delete stored data at session end.
- Firefox, Chromium, and WebKit have different quota rules.
- Safari/WebKit has proactive eviction behavior under tracking-prevention conditions and different browser-app vs embedded-app quotas in modern versions.
- `navigator.storage.estimate()` is an estimate, not an exact guarantee.
- `QuotaExceededError` must be handled.
- `getAllRecords()` is experimental/limited and must not be required for production.
- Chrome changed IndexedDB default readwrite durability to relaxed from Chrome 121.
- Skills should be concise, well-structured, and route heavy context to references.

## Maintenance schedule

Refresh this pack when:

- every 6 months for browser compatibility/quota facts
- Safari/iOS/WebKit releases change storage policy
- Chrome/Edge/Firefox change durability/quota/storage-bucket behavior
- IndexedDB 3.0 or related APIs reach new Baseline status
- Alaa frontend architecture changes storage ownership or service boundaries
- a production incident reveals a browser-specific IndexedDB failure

## Maintenance workflow

1. Search official sources first.
2. Update source list with date.
3. Update compatibility and quota references.
4. Update examples if API recommendations change.
5. Run `python scripts/validate_skill_pack.py`.
6. Run a grep for prohibited storage of secrets in examples.
7. Test the skill on realistic prompts:
   - design an outbox
   - fix a migration bug
   - audit quota handling
   - review token storage proposal
   - plan Safari/iOS offline support

## Known uncertainty

Browser vendors intentionally pad/alter quota estimates to reduce fingerprinting. Exact storage capacity cannot be guaranteed by documentation alone. Agents should design probes, fallback tiers, and cleanup paths instead of promising exact byte availability.
