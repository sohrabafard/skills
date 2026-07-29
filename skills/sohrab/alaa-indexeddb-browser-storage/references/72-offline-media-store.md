# The offline media store

In-app download: the browser holds tens or hundreds of megabytes on the user's device until they remove it
or the browser does.

## The seam, stated once

**`/alaa-shaka-player` (`$alaa-shaka-player`) owns** what the player stores and in what form, how segments
and manifests are fetched, `shaka.offline.Storage` and its surface, `offline.trackSelectionCallback`,
download progress, and persistent DRM licences. Do not restate or re-derive any of it here.

**This skill owns** the substrate: how much room there is, whether it survives, the concurrency around it
while tabs are open, and what the application does when a stored asset is gone.

If the question is "what does the player call", it is the player skill. If it is "will it still be there
tomorrow", it is this one.

**The reciprocal pointer `alaa-shaka-player` should carry** on its offline-download reference:

> Quota, persistence, eviction, the multi-tab and service-worker concurrency around the offline store, and
> what the application does when a stored asset is evicted mid-session are
> `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`),
> `references/72-offline-media-store.md`. Shaka never calls `navigator.storage.persist()`, so an offline
> download sits in best-effort storage; the caller must request persistence itself and must ship the
> eviction-recovery path.

## Two upstream facts and what each obliges

Both researched at Shaka **v5.2.3**, read 2026-07-28, by the `alaa-shaka-player` lane.

### 1. Shaka never calls `navigator.storage.persist()`

The download therefore lands in **best-effort storage**: subject to the LRU eviction in
`32-eviction-and-recovery.md`, to the whole-browser ceiling, and on WebKit to deletion after seven days of
browser use without user interaction with the origin. **It can vanish with no warning and no event, while
the user believes they have it.** Four obligations, all the caller's:

1. **Request persistence when the user confirms the download, not after.** That confirmation is genuine
   user intent and the strongest signal the engines that judge by engagement will see. Then call
   `navigator.storage.persisted()` and store the answer.
2. **Branch the UI on that answer.** Granted: "Available offline on this device." Not granted: "Available
   offline on this device. Your browser may remove it if the device runs low on space." Never the first
   sentence alone for a best-effort store.
3. **Check free space against the asset size before starting**, using `navigator.storage.estimate()` and
   the offline-media cap in the budget file (`30-quota-model-and-budgets.md`). The estimate is approximate,
   so treat a margin below the asset size as insufficient rather than as a close call. A download that
   begins without room fails partway and leaves the partial state below.
4. **Never offer the affordance below tier 3** (`20-browser-compatibility-and-capability-tiers.md`).

### 2. Shaka provides no resume or repair API for an interrupted store

A `store()` interrupted by a closed tab, a terminated service worker, a lost network or a sleeping device
leaves whatever it wrote and offers no call to continue it. **Detecting a partial download is this skill's
problem; restarting it is the caller's.** The application writes the detection contract, because the player
will not:

```ts
type OfflineAssetRecord = {
  id: string;
  accountKey: string;
  schema: number;
  contentId: string;
  /** Written before store() begins, cleared only after store() resolves. */
  downloadState: 'requested' | 'storing' | 'complete';
  offlineUri?: string;      // the handle the player skill defines for a completed asset
  expectedBytes?: number;
  startedAt: string;
  completedAt?: string;
  lastVerifiedAt?: string;
  updatedAt: string;
};
```

- **Write `'storing'` in its own committed transaction before the download begins.** A record reading
  `'storing'` on the next boot is a partial download by definition; no other state produces it.
- **Write `'complete'` with the `offlineUri` only after the store call resolves.** A crash between the two
  leaves `'storing'`, which is the detectable state.
- **On boot, reconcile every `'storing'` record**: ask the player skill's list surface whether the asset
  exists; if not, delete the record and offer the download again; if so, follow that skill's guidance on
  what a partial store leaves.
- **Never present a `'storing'` record as available offline.** The user tapping it gets a playback error
  instead of an explanation.

## Eviction mid-session

The user downloaded content, opened the app, and the browser reclaimed the origin in between — or the
WebKit seven-day sweep fired.

**Detect before playback, never by playback error.** Before offering or starting offline playback, verify
the asset is still listed by the player's own store. A record in this database is not evidence the media is
on disk: eviction is all-or-nothing per origin so both normally go together, but a partial state, an
interrupted delete, or a user clearing one surface can desynchronise them.

When it is gone:

1. Delete the local record so the UI does not offer it again this session.
2. Tell the user in one sentence naming cause and remedy: "Your browser removed this download to free
   space. Download it again, or watch online now." Do not say "error"; nothing failed.
3. If the network is available, fall through to online playback in the same interaction. The user asked to
   watch; make that happen.
4. Emit the eviction event with the asset size bucketed. Frequent firing means the offline cap is too large
   for the device class — raising the persistence request will not fix it.

**Never re-download silently.** A hundred megabytes on a metered connection is the user's decision.

## Concurrency: a download runs while tabs are open

This is what makes `41-multitab-versionchange-and-locks.md` load-bearing here.

- **One download per asset, enforced by a named Web Lock** — `alaa:offline-download:<contentId>`. Two tabs
  starting the same download write the same segments twice, consume double the quota, and produce two
  records.
- **A download in or through the service worker holds no claim across an event boundary**, because the
  browser may terminate it. The `'storing'` record is what survives that termination.
- **A schema upgrade must not run while a download is in progress.** The upgrade blocks on every open
  connection and a download holds one for minutes. Broadcast `db-upgrade-starting`, let the download
  context finish its current transaction and close, and show the blocked UX otherwise — the download itself
  continues via the player's own connection, which is why the service worker opens with no version
  argument.
- **The offline store competes for the same quota as everything else.** A large download pushes the API
  cache and the outbox toward `softStop`. The ladder in `31-quota-exceeded-and-cleanup.md` frees
  refetchable data first and never frees an unsynced draft to make room for media.

## Budget

Capped per device in the feature's budget file by total bytes and by asset count, checked before each
download starts. The **metadata** records above are small and carry their own 5 MB cap
(`30-quota-model-and-budgets.md`); the media itself is sized by the player skill's track selection, and
this skill's contribution is the ceiling that selection must fit inside. Every value is named in
`/alaa-services-contract` (`$alaa-services-contract`).
