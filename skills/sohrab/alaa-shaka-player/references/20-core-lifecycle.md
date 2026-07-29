# Core lifecycle

All rows `verified` at tag v5.2.3, read 2026-07-28, from `lib/player.js` unless stated.

## API surface

| Name | Signature / behaviour |
|---|---|
| `shaka.polyfill.installAll()` | Static. Call **before** creating a Player. 23 polyfill modules exist under `lib/polyfill/`; 20 self-register. |
| `shaka.Player.isBrowserSupported()` | Static → `boolean`. (L1332) |
| `shaka.Player.probeSupport(promptsOkay = true)` | Static, `async` → `shaka.extern.SupportType`. (L1375) |
| `new shaka.Player(mediaElement?, videoContainer = null, dependencyInjector?)` | **All three optional.** Passing `mediaElement` logs *"Please migrate from initializing Player with a mediaElement; use the attach method instead."* and calls `attach()` internally. (L726–736, L1137–1141; conflict C3) |
| `player.attach(mediaElement, initializeMediaSource = true)` | `async`. Detaches from a previous element first. (L1426) |
| `player.attachCanvas(canvas)` | LCEVC decoding only. |
| `player.detach(keepAdManager = false, isSwitchingContent = false)` | `async`. Calls `unload(false, …)` then releases the element. (L1490) |
| `player.load(assetUriOrPreloader, startTime = null, mimeType?)` | `async`. `startTime` may be a `number` **or a `Date`**. `null` → 0 for VOD, live edge for LIVE. Accepts a `PreloadManager` in place of a URI. **Unloads any previous stream itself.** (L1845) |
| `player.unload(initializeMediaSource = true, keepAdManager = false, isSwitchingContent = false)` | `async`. (L1551) |
| `player.destroy()` | `async`. Afterwards **every** method throws `LOAD_INTERRUPTED` (7000). (L1207, L9420) |
| `player.updateStartTime(startTime)` | `number \| Date`. **Required since v5.0** instead of setting `video.currentTime` during startup. Intended for the `manifestparsed` handler. (L1828) |
| `player.getLoadMode()` | → `shaka.Player.LoadMode` = `{DESTROYED: 0, NOT_LOADED: 1, MEDIA_SOURCE: 2, SRC_EQUALS: 3}` (L9645) |
| `player.getMediaElement()` / `getAssetUri()` / `getMimeType()` / `getManifestType()` | Accessors. |
| `player.releaseAllMutexes()` | Escape hatch for a stuck internal mutex. |
| `player.preload(uri, startTime, mimeType, config, throwOnPreloadNotSupported)` | `async` → `PreloadManager \| null`. `null` means the asset cannot be preloaded (raw media, Safari native HLS). The last flag was **added in 5.2.0**. |
| `player.unloadAndSavePreload()` / `detachAndSavePreload()` / `destroyAllPreloads()` | Preload lifecycle. |
| `shaka.Player.setAdManagerFactory(f)` / `setQueueManagerFactory(f)` / `registerSupportPlugin(name, cb)` | Statics; must run **before** constructing the Player. (L1297–1320) |

## Lifecycle events — exact strings

From `lib/util/fake_event.js` and the `@event` blocks in `lib/player.js`:

| Event | Meaning |
|---|---|
| `loading` | Load intent communicated. |
| `loaded` | Load finished. |
| `unloading` | Unload started, or load failed. Carries `isSwitchingContent: boolean`. **The last point at which `getStats()` still holds this session's counters.** |
| `manifestparsed` | Manifest parsed, before filtering. **Use this for `updateStartTime()`.** |
| `streaming` | Tracks known, no segment fetched yet. **Use this to configure per asset.** |
| `onstatechange` | Internal load-state machine; `state` string. |
| `error` | `event.detail` is a `shaka.util.Error`. |

## Media-element ownership and teardown

| Rule | Grade |
|---|---|
| The Player does **not** own the media element. `attach()` borrows it; `detach()` gives it back; no DOM removal is performed. | `inferred` from the `detach()` JSDoc (L1481–1490) |
| After `destroy()` the instance is dead: `loadMode_` becomes `DESTROYED` and `attach`/`load`/`detach` all throw `LOAD_INTERRUPTED` (7000). | `verified` (L1426–1430, L1490–1494, L1845–1849, `createAbortLoadError_()` L9420) |
| With the Shaka UI, `ui.destroy(forceDisconnect = false)` is the teardown entry point and disposes the Controls **and the Player the UI created**. | `verified` (`ui/ui.js`, `ui/controls.js`) |
| Blob URLs created for `src=` metadata playback are revoked on unload. | `verified` |

## Failure modes

| Code | Name | When |
|---|---|---|
| 7000 | `LOAD_INTERRUPTED` | Any call after `destroy()`, or a load aborted by another load. |
| 7001 | `OPERATION_ABORTED` | An abortable operation was cancelled. |
| 7002 | `NO_VIDEO_ELEMENT` | `load()` with nothing attached. |
| 7003 | `OBJECT_DESTROYED` | Use after destruction. |
| 7004 | `CONTENT_NOT_LOADED` | A method needing loaded content was called too early. |
| 7005 | `SRC_EQUALS_PRELOAD_NOT_SUPPORTED` | `preload()` under Safari native HLS. |
| 7006 | `PRELOAD_DESTROYED` | The `PreloadManager` was destroyed before use. |
| 7007 | `QUEUE_INDEX_OUT_OF_BOUNDS` | `QueueManager.playItem` past the end. |

Load-time failures **reject the `load()` promise** and never reach the `error` listener. You need both
paths — see `70-error-taxonomy-and-codes.md`.

## Working snippet — full lifecycle with correct teardown

```js
// 1. Polyfills first, before any Player exists.
shaka.polyfill.installAll();

if (!shaka.Player.isBrowserSupported()) {
  throw new Error('Shaka Player is not supported in this browser.');
}

const video = document.getElementById('video');

// 2. Construct with NO media element, then attach.
const player = new shaka.Player();
await player.attach(video);

// 3. Error handling is wired BEFORE loading.
player.addEventListener('error', (e) => onError(e.detail));

// 4. Per-asset work belongs on these two events, not after load() resolves.
player.addEventListener('manifestparsed', () => {
  // Never set video.currentTime here - use updateStartTime().
  if (player.isLive()) {
    player.updateStartTime(player.seekRange().end - 10);
  }
});
player.addEventListener('streaming', () => {
  // Tracks are known here and no segment has been fetched yet.
});

// 5. Flush telemetry while the counters still exist.
player.addEventListener('unloading', () => flushQoe(player.getStats()));

try {
  await player.load(manifestUri);         // load() unloads any previous stream itself
} catch (e) {
  onError(e);                              // load-time failures never reach the listener
}

// 6. Teardown, in this order.
async function teardown() {
  clearTimersAndIntervals();
  removeEveryListenerYouRegistered();     // player, <video>, and document
  await player.destroy();                 // destroy() implies unload(); the instance is now dead
  // The media element is NOT owned by the Player. Remove it from the DOM yourself if you want that.
}

function onError(error) {
  console.error('Shaka error', error.code, error.category, error.severity);
  // Do NOT log the whole error object: error.data for a network error carries the
  // failing URI and its query string. See 42-media-url-trust-and-presigned.md.
}
```

**Best practice.** Construct detached, `await attach()`, register `error` before `load()`, and on
teardown `await player.destroy()` exactly once and then drop the reference.
**Common mistake.** Reusing a Player after `destroy()`, or `new shaka.Player(video)` — the latter
still works but hides the async attach step, which is the step that fails on iOS Safari when the
element is not ready.
