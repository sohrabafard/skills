# Offline and in-app download

All rows `verified` at v5.2.3, read 2026-07-28.

## The seam — read this before writing any code

**This skill owns:** what the player stores, how it is fetched and licensed, the
`shaka.offline.Storage` surface, `offline.trackSelectionCallback`, progress reporting, and storing
with a persistent DRM licence.

**`/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`) owns the storage substrate.**
Its reciprocal statement, carried here verbatim:

> Quota, persistence, eviction, the multi-tab and service-worker concurrency around the offline store,
> and what the application does when a stored asset is evicted mid-session are
> `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`),
> `references/72-offline-media-store.md`. Shaka never calls `navigator.storage.persist()`, so an
> offline download sits in best-effort storage; the caller must request persistence itself and must
> ship the eviction-recovery path.

Read `references/72-offline-media-store.md` there before shipping a download feature,
`references/32-eviction-and-recovery.md` for the recovery path, and
`references/41-multitab-versionchange-and-locks.md` if a service worker and a tab can both be active
during a download. Neither skill restates the other.

**The fact that joins them, and the consequence the consumer must handle:** Shaka's only use of
`navigator.storage` anywhere in `lib/` is **two `estimate()` calls** in
`lib/util/player_configuration.js`. **Shaka never calls `navigator.storage.persist()`.** Therefore a
downloaded asset lives in **best-effort** storage by default and the browser may evict it under
pressure, at any time, without notifying the player. Requesting persistent storage is the
application's job, and handling a mid-session eviction is the other skill's ground.

## Current position

`shaka.offline.Storage` wraps a pluggable storage muxer; in browsers the registered mechanism is
`'idb'`, backed by a **single IndexedDB database named `shaka_offline_db` at version 5**.

## API surface — including what does not exist

| Name | Signature |
|---|---|
| `new shaka.offline.Storage(player?)` | |
| `shaka.offline.Storage.support()` | Static → `shaka.extern.OfflineSupport` = `{basic: boolean, encrypted: Object<string,boolean>}` |
| `storage.configure(config, value?)` / `getConfiguration()` | Same two-form API as `player.configure`. |
| `storage.getNetworkingEngine()` | **Separate** engine from the Player's. |
| `storage.store(uri, appMetadata?, mimeType?, externalThumbnails?, externalText?)` | → **`IAbortableOperation<StoredContent>`**. Use `.promise`; cancel with `.abort()`. |
| `storage.list()` | → `Promise<Array<StoredContent>>` |
| `storage.remove(contentUri)` | *"This will also attempt to release the licenses, if any."* |
| `storage.removeEmeSessions()` | → `Promise<boolean>`. Cleans **orphaned persistent DRM sessions**. *"It should be called on application startup."* `true` = all removed. |
| `shaka.offline.Storage.deleteAll()` | Static, `async`. *"This should not be done in normal circumstances. Only do it when storage is rendered unusable, such as by a version mismatch. No business logic will be run, and licenses will not be released."* |
| `storage.destroy()` | |
| **`removeEmptyEpisodes()`** | **DOES NOT EXIST.** `not documented` — searched `grep -rn "removeEmptyEpisodes" .` over the whole v5.2.3 tree → zero matches. The `@export`ed `Storage` surface is exactly: `support`, `destroy`, `configure`, `getConfiguration`, `getNetworkingEngine`, `store`, `remove`, `removeEmeSessions`, `list`, `deleteAll`. The nearest real methods are `remove()` and `removeEmeSessions()`. |

## `offline.*` configuration

| Key | Default | Note |
|---|---|---|
| `offline.trackSelectionCallback` | identity, `async (tracks) => tracks` | **The identity default downloads every track.** Always replace it. |
| `offline.downloadSizeCallback` | quota-aware, see below | |
| `offline.progressCallback` | no-op stub | `function(StoredContent, number)`; progress is `0..1` |
| `offline.usePersistentLicense` | **`true`** | |
| `offline.numberOfParallelDownloads` | `5` | `0` = sequential per stream. *"normally browsers limit to 5 request in parallel, so putting a number higher than this will not help it download faster."* |

`shaka.extern.StoredContent`: `offlineUri: ?string` (**`null` while still downloading**),
`originalManifestUri`, `duration`, `size` (bytes), `expiration` (ms; `Infinity` if clear or never),
`tracks`, `appMetadata`, `isIncomplete: boolean`.

## The IndexedDB substrate — exact names

Read from `lib/offline/indexeddb/storage_mechanism.js`:

```js
DB_NAME            = 'shaka_offline_db';
VERSION            = 5;
V1_SEGMENT_STORE   = 'segment';      V1_MANIFEST_STORE  = 'manifest';
V2_SEGMENT_STORE   = 'segment-v2';   V2_MANIFEST_STORE  = 'manifest-v2';
V3_SEGMENT_STORE   = 'segment-v3';   V3_MANIFEST_STORE  = 'manifest-v3';
V5_SEGMENT_STORE   = 'segment-v5';   V5_MANIFEST_STORE  = 'manifest-v5';
SESSION_ID_STORE   = 'session-ids';
```

| Fact | Detail |
|---|---|
| Object stores created on upgrade to v5 | `segment-v5`, `manifest-v5`, `session-ids`, each `db.createObjectStore(name, {autoIncrement: true})` (L317–324) |
| Legacy stores read for migration | `segment`, `segment-v2`, `segment-v3`, `manifest`, `manifest-v2`, `manifest-v3` |
| Key generation | `autoIncrement: true` — **Shaka does not supply keys** |
| Mechanism registration | `shaka.offline.StorageMuxer.register('idb', …)`; returns `null` when `DeviceFactory.getDevice().supportsOfflineStorage()` is false |
| Open timeout | `shaka.offline.indexeddb.StorageMechanismOpenTimeout = 5` seconds. Settable to another number, or `false` to wait indefinitely. **Must be set before any other offline operation.** Timeout → `INDEXED_DB_INIT_TIMED_OUT` (9017) |
| Deletion | `deleteAll()` calls `window.indexedDB.deleteDatabase('shaka_offline_db')`, logs a warning on `onblocked`, rejects with `INDEXED_DB_ERROR` (9001) on error, and calls `event.preventDefault()` because *"Firefox will raise an error on the main thread unless we stop it here."* |

**Do not open `shaka_offline_db` yourself.** It is Shaka's private schema with no stable contract;
migrating it is Shaka's job. Your own application data belongs in your own database, and the rules for
that database are `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`).

## Quota interaction — precise

| Fact | Evidence |
|---|---|
| Shaka's **default `downloadSizeCallback`** is quota-aware: it calls `navigator.storage.estimate()` and returns `estimate.usage + sizeEstimate < estimate.quota * 0.95` — **"Limit to 95% of quota"**. If `navigator.storage.estimate` is absent it returns `true` unconditionally. | `lib/util/player_configuration.js` L278–286 |
| The size estimate passed to the callback is computed in `store()` as `Σ (track.bandwidth × duration / 8)` over the **chosen** tracks. It is a bitrate-derived estimate, **not** a measured byte count. | `lib/offline/storage.js` L811–816 |
| Callback returns `false` → `store()` rejects with **`STORAGE_LIMIT_REACHED` (9014)**. | L818–824 |
| Callback *throws* a non-Shaka error → converted to **`DOWNLOAD_SIZE_CALLBACK_ERROR` (9015)** with a warning. Shaka `Error`s are re-thrown unchanged. | L826–836 |
| **Shaka never calls `navigator.storage.persist()`.** | `grep -rn "navigator.storage" lib/` → exactly two hits, both `estimate()` |
| Guidance on persistence, eviction, or the Storage Standard's best-effort/persistent buckets | `not documented` — searched all 712 lines of `docs/tutorials/offline.md` and `README.md` on 2026-07-28; none found |
| Generic IndexedDB failure → **`INDEXED_DB_ERROR` (9001)**. Its doc names a real cause: *"On Firefox, one common source for UnknownError calls is reverting Firefox to an old version… The only way to fix this is to delete the storage data in your profile."* `error.data[0]` is the underlying error object. | `lib/util/error.js` L1139–1145 |

## Persistent licences — platform constraints

Verbatim from `docs/tutorials/offline.md` §"Protected Content":

> *"When storing protected content offline, there are some limitations based on browsers. Persistent
> licenses are only supported on **Android (M62+) and Chromebooks**. **Chrome v64 to v142** did
> support persistent licenses on Windows and Mac as well."*

> *"For other platforms, we offer the ability to disable the use of persistent licenses. If you choose
> to disable persistent licenses, you will get offline storage of protected content on all DRM-enabled
> browsers, at the cost of needing a network connection at playback time to retrieve licenses.
> Therefore, you should avoid this setting on browsers that support persistent licenses."*

The code comment on the `true` default: *"By default we use persistent licenses as forces errors to
surface if a platform does not support offline licenses rather than causing unexpected behaviours when
someone tries to plays downloaded content without a persistent license."*

Detect at runtime with `shaka.offline.Storage.support()` → `{basic, encrypted: {<keySystem>: bool}}`,
and set `drm.advanced.<keySystem>.persistentStateRequired = true` (`45-drm.md`).

## Interrupted downloads

| Question | Answer |
|---|---|
| Does an interrupted store leave a record? | **Yes.** `manifestDB.isIncomplete` is set `true` at creation and cleared only on completion. `StoredContent.isIncomplete` surfaces it; `offlineUri` is `null` while incomplete. |
| Is there a **resume** API? | **No.** `not documented` — searched the `@export`ed method list of `lib/offline/storage.js` and `grep -rn "resume\|repair" lib/offline/`; nothing relevant found. There is no `resume`, `repair` or `continue`. |
| Practical remedy | `list()`, filter `isIncomplete === true`, `remove(...)` — but `offlineUri` is `null` for these, which makes targeted removal awkward. `deleteAll()` is the blunt instrument. **This is open question 3 in `05-provenance-and-freshness.md`.** |
| Cancelling in progress | `store()` returns an `IAbortableOperation`; call `.abort()`. |
| Storing the same URI twice | *"If you call `storage.store` twice with the same manifestUri as input, you'll download the same manifestUri twice."* **No dedup — you must key downloads yourself.** |
| Config snapshotting | *"This snapshots the storage config at the time of the call, so it will not honor any changes to config mid-store operation."* |

## Storage error codes

`STORAGE_NOT_SUPPORTED` 9000 · `INDEXED_DB_ERROR` 9001 · `DEPRECATED_OPERATION_ABORTED` 9002 ·
`REQUESTED_ITEM_NOT_FOUND` 9003 · `MALFORMED_OFFLINE_URI` 9004 · `CANNOT_STORE_LIVE_OFFLINE` 9005 ·
`NO_INIT_DATA_FOR_OFFLINE` 9007 · `LOCAL_PLAYER_INSTANCE_REQUIRED` 9008 ·
`NEW_KEY_OPERATION_NOT_SUPPORTED` 9011 · `KEY_NOT_FOUND` 9012 · `MISSING_STORAGE_CELL` 9013 ·
`STORAGE_LIMIT_REACHED` 9014 · `DOWNLOAD_SIZE_CALLBACK_ERROR` 9015 ·
`MODIFY_OPERATION_NOT_SUPPORTED` 9016 · `INDEXED_DB_INIT_TIMED_OUT` 9017.

Distinct from these: MSE-side `QUOTA_EXCEEDED_ERROR` (3017), governed by
`streaming.avoidEvictionOnQuotaExceededError`. A `3017` is a playback-buffer problem, not a download
problem.

## Working snippet — a complete offline flow

```js
// ---- 0. Change the IndexedDB open timeout BEFORE any other offline call ----
shaka.offline.indexeddb.StorageMechanismOpenTimeout = 10;   // seconds; or false = wait forever

// ---- 1. Capability check ----
const support = await shaka.offline.Storage.support();
if (!support.basic) throw new Error('Offline storage unsupported here.');
const canPersistWidevine = support.encrypted['com.widevine.alpha'] === true;

// ---- 2. Ask the browser for PERSISTENT (non-evictable) storage.
//         Shaka does NOT do this: it only calls navigator.storage.estimate().
//         The eviction semantics behind this call are owned by
//         /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage). ----
if (navigator.storage && navigator.storage.persist) {
  const persisted = await navigator.storage.persist();
  recordStoragePersistence(persisted);   // false => the browser may evict this download
}

// ---- 3. Clean up orphaned DRM sessions on startup ----
const storage = new shaka.offline.Storage(player);
await storage.removeEmeSessions();

// ---- 4. Configure ----
storage.configure({
  offline: {
    numberOfParallelDownloads: 5,
    usePersistentLicense: canPersistWidevine,   // false => needs network at playback time
    trackSelectionCallback: async (tracks) => {
      // The DEFAULT is identity, which downloads everything. Always narrow.
      const video = tracks
          .filter((t) => t.type === 'variant' && t.height && t.height <= 720)
          .sort((a, b) => b.bandwidth - a.bandwidth)[0];
      const text = tracks.filter((t) => t.type === 'text' &&
                                        ['fa', 'en'].includes(t.language));
      return video ? [video, ...text] : tracks;
    },
    downloadSizeCallback: async (sizeEstimate) => {
      // Shaka's default caps at 95% of quota. Be stricter, and tell the user why.
      // NOTE: sizeEstimate is bitrate-derived, not measured.
      if (!navigator.storage || !navigator.storage.estimate) return true;
      const {usage, quota} = await navigator.storage.estimate();
      const ok = usage + sizeEstimate < quota * 0.80;
      if (!ok) showQuotaDialog({usage, quota, sizeEstimate});
      return ok;   // false => store() rejects with STORAGE_LIMIT_REACHED (9014)
    },
    progressCallback: (content, progress) => {
      updateProgressBar(content.originalManifestUri, progress);   // progress is 0..1
    },
  },
});

// ---- 5. Downloads use Storage's OWN networking engine. Sign with a getter. ----
storage.getNetworkingEngine().registerRequestFilter(async (type, request) => {
  request.headers['Authorization'] = 'Bearer ' + (await getToken());
});

// ---- 6. Store. Abortable. Note `.promise`. ----
if (player.isLive()) throw new Error('Live cannot be stored (9005).');
const op = storage.store(manifestUri, {title: 'Ep 1', downloadedAt: Date.now()});
cancelButton.onclick = () => op.abort();

let stored;
try {
  stored = await op.promise;             // NOT `await op` - that gives the operation, not the content
} catch (e) {
  const C = shaka.util.Error.Code;
  if (e.code === C.STORAGE_LIMIT_REACHED)          showQuotaDialog();        // 9014
  else if (e.code === C.CANNOT_STORE_LIVE_OFFLINE) showLiveNotDownloadable(); // 9005
  else if (e.code === C.INDEXED_DB_INIT_TIMED_OUT) showStorageUnavailable();  // 9017
  else if (e.code === C.INDEXED_DB_ERROR)          showStorageCorrupt();      // 9001
  else throw e;
}

// ---- 7. List, detect interrupted downloads, play, remove ----
const all = await storage.list();
const broken = all.filter((c) => c.isIncomplete);   // offlineUri is null for these; no resume API
await player.load(stored.offlineUri);               // the networking layer redirects to storage
await storage.remove(stored.offlineUri);

// ---- 8. Nuclear option, only for a corrupted or incompatible DB ----
// await shaka.offline.Storage.deleteAll();   // drops 'shaka_offline_db' entirely
```

## The routing line another lane should place

`alaa-indexeddb-browser-storage` already carries the row
*"store downloaded media for offline playback, or reason about a partial or evicted download →
`72-offline-media-store.md`"* in its `references/00-topic-map.md`. The line that file should carry to
reach **this** skill, and which it already states, is:

> `/alaa-shaka-player` (`$alaa-shaka-player`), `references/50-offline-and-in-app-download.md` owns what
> the player stores and in what form, how segments and manifests are fetched, `shaka.offline.Storage`
> and its surface, `offline.trackSelectionCallback`, download progress, and persistent DRM licences.
> Shaka writes a single IndexedDB database **`shaka_offline_db` at version 5**, with object stores
> `segment-v5`, `manifest-v5` and `session-ids`, all `autoIncrement: true`. Do not open that database
> directly: it is Shaka's private schema with no stable contract.

**Best practice.** Call `navigator.storage.persist()` yourself, record whether it was granted, and
check `navigator.storage.estimate()` in your own `downloadSizeCallback`. Shaka's 95%-of-quota default
is a guard rail, not a durability guarantee.
**Common mistake (three).** (a) `await storage.store(...)` without `.promise` — since v4.0 `store()`
returns an `IAbortableOperation`, so awaiting it directly does not give you the `StoredContent`. (b)
Registering auth filters on `player.getNetworkingEngine()` and finding downloads 401 — `Storage` has
its own engine. (c) Leaving `trackSelectionCallback` at its identity default, which downloads every
rendition of every language.
