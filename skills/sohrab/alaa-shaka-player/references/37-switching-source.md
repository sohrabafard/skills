# Switching source mid-session

All rows `verified` at v5.2.3, read 2026-07-28.

## `player.load(newUri)` **is** the switch

The `load()` JSDoc (L1840–1845): *"Loads a new stream. If another stream was already playing, first
unloads that stream."* You do **not** need to call `unload()` first, and you must not destroy the
Player to change source.

## The four sequences

**A — simplest.**
```js
await player.load(nextUri);   // implicit unload of the previous asset
```

**B — explicit, keeping the ad manager and MSE warm.**
```js
await player.unload(
    /* initializeMediaSource= */ true,   // keep MSE warm for the next load
    /* keepAdManager= */ true,           // do NOT tear down the ad manager
    /* isSwitchingContent= */ true);     // surfaces on the 'unloading' event
await player.load(nextUri);
```
`isSwitchingContent` appears as a boolean property on the `unloading` event, which is how a telemetry
module tells "user left" from "next episode".

**C — zero-gap, via the PreloadManager.**
```js
const next = await player.preload(nextUri);   // null if not preloadable
await (next ? player.load(next) : player.load(nextUri));
```
`preload()` returns `null` for raw media and on Safari native HLS (`SRC_EQUALS_PRELOAD_NOT_SUPPORTED`
7005 if you force it). 5.2.0 added the `throwOnPreloadNotSupported` flag.

**D — queue-driven.** `player.getQueueManager()` is auto-created; `insertItems([...])` then
`playItem(index)`. Each `QueueItem` may carry its own `config`, `startTime`, `mimeType`,
`preloadManager`, `extraText`, `extraThumbnail`, `extraChapter` and `metadata`. Out-of-range index →
`QUEUE_INDEX_OUT_OF_BOUNDS` (7007). 5.2.0 added M3U playlist loading to the queue and a `queue` UI
button.

## What survives the switch

| Thing | Survives `load()`? | Basis |
|---|---|---|
| The `Player` instance and the attached media element | **Yes** | `load()` does not detach |
| `player.configure()` values | **Yes** — only `resetConfiguration()` clears them | `lib/player.js` exports |
| Registered request/response filters | **Yes** — they live on the `NetworkingEngine`, owned by the Player | `inferred`; cleared only by `clearAllRequestFilters()` / `clearAllResponseFilters()` / `destroy()` |
| Registered custom UI elements and scheme plugins | **Yes** — static registries | `registerElement`, `registerScheme` are statics |
| `getStats()` counters | **No** — *"These values will reset when `load()` is called again."* | `shaka.extern.Stats` |
| Selected text track | **No** — reset from `config.preferredText[0]` on each load | L3087 |
| Selected variant / adaptation criteria | **No**, unless the load came from a `PreloadManager` carrying one | L2050–2058 |
| Ad manager | Destroyed unless `keepAdManager: true` | signatures |
| MediaSource | Re-initialised unless `initializeMediaSource: false` | unload tail |
| DRM sessions | Released on unload; persistent sessions survive only with `drm.persistentSessionOnlinePlayback: true` (*"prevents the session removal at playback stop, as-to be able to re-use it later"*) | `DrmConfiguration` |

Two of those rows are the whole reason this file exists: **stats are wiped and the user's subtitle
choice reverts**, silently, at every episode boundary.

## Working snippet — the recommended sequence

```js
async function switchTo(uri, {keepAds = false} = {}) {
  // 1. Persist the user's choices INTO CONFIG, or load() resets them.
  const activeAudio = player.getAudioTracks().find((t) => t.active);
  if (activeAudio) {
    player.configure('preferredAudio', [{
      language: activeAudio.language,
      role: activeAudio.roles[0] || '',
      label: activeAudio.label || '',
      channelCount: activeAudio.channelsCount || 0,
      codec: '',
      spatialAudio: !!activeAudio.spatialAudio,
    }]);
  }
  const activeText = player.getTextTracks().find((t) => t.active);
  if (activeText) {
    player.configure('preferredText',
        [{language: activeText.language, role: activeText.roles[0] || '',
          format: '', forced: !!activeText.forced}]);
  }

  // 2. Snapshot stats BEFORE they are wiped. There is no other way to recover them.
  flushQoe(player.getStats());

  // 3. Switch. load() unloads internally; the explicit unload is only for the flags.
  if (keepAds) {
    await player.unload(true, /* keepAdManager= */ true, /* isSwitchingContent= */ true);
  }
  await player.load(uri);
}

// A schedule or playlist driver MUST handle a failed load, or the channel goes dark.
async function playScheduled(item, fallbackUri) {
  try {
    await switchTo(item.uri);
  } catch (e) {
    reportPlaybackFailure(item.id, e.code);
    if (fallbackUri) await switchTo(fallbackUri);   // never leave the surface empty
  }
}
```

## Schedule- and playlist-driven switching

A wall-clock schedule that calls `load()` has four failure modes that a naive loop does not handle.
State each in the implementation:

| Failure | Requirement |
|---|---|
| The `load()` rejects (404, DRM, unsupported codec) | `try`/`catch` around **every** `load()`, and a fallback source. Marking the item "active" **before** the load resolves means it is never retried. |
| The client clock is skewed against the server | Compute boundaries against a server-supplied time, not `Date.now()` alone. Time skew is also the FAQ's first answer to a live stream that buffers forever (`32-live-and-low-latency.md`). |
| An unparseable timestamp | `new Date(badString)` yields `NaN`, and every comparison against `NaN` is `false`, so **nothing** is selected and the failure is silent. Validate at the boundary. |
| Re-deriving the whole schedule on a 1 Hz timer | Precompute a sorted array of epoch-millisecond boundaries once, then advance a cursor. Complexity budgets are `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`). |

**Best practice.** Snapshot `getStats()` on the `unloading` event rather than at your own call sites —
it fires for every path that ends a session, including the ones you did not write.
**Common mistake.** `await player.destroy(); player = new shaka.Player();` to change source. That
throws away the networking engine and therefore **every registered filter**, the ad manager, the whole
config, and the MSE instance, for no benefit. Use `load()`.
