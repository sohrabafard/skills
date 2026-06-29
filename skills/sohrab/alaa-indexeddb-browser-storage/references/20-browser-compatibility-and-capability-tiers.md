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
