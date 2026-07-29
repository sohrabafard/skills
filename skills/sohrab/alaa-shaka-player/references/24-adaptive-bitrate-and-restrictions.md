# Adaptive bitrate and restrictions

All rows `verified` at v5.2.3, read 2026-07-28, from `externs/shaka/player.js`
(`AbrConfiguration`, `AdvancedAbrConfiguration`, `Restrictions`) cross-checked against
`lib/util/player_configuration.js`.

## Current position

ABR is on by default, driven by a pluggable `AbrManager`. Bandwidth estimation is a dual half-life
EWMA, optionally superseded by the browser's Network Information API. Restrictions exist at **two
levels with different semantics** and confusing them is the most common ABR bug.

## `abr.*` configuration

| Key | Default | Note |
|---|---|---|
| `abr.enabled` | `true` | |
| `abr.useNetworkInformation` | `true` | |
| `abr.defaultBandwidthEstimate` | `1e6` bit/s | **Only used when `useNetworkInformation` is `false` or the API is absent.** |
| `abr.preferNetworkInformationBandwidth` | `false` | `true` → never estimate, always trust the browser. |
| `abr.restrictions` | see below | **Soft.** |
| `abr.switchInterval` | `8` s | |
| `abr.bandwidthUpgradeTarget` | `0.85` | |
| `abr.bandwidthDowngradeTarget` | `0.95` | |
| `abr.restrictToElementSize` | `false` | Needs `ResizeObserver`; behaves as `false` without it. |
| `abr.restrictToScreenSize` | `false` | |
| `abr.ignoreDevicePixelRatio` | `false` | |
| `abr.clearBufferSwitch` | `false` | |
| `abr.safeMarginSwitch` | `0` s | The typedef prose says "Defaults to `o`" — a typo. Conflict C7. |
| `abr.cacheLoadThreshold` | `5` ms | Below this a response is treated as cached and excluded from estimation. |
| `abr.minTimeToSwitch` | `0`, **`0.5` on Apple browsers** | First load only. |
| `abr.droppedFrames` | `true` | Dropped-frame protection, added in 5.1.0. |
| `abr.advanced.minTotalBytes` | `128e3` | |
| `abr.advanced.minBytes` | `16e3` | |
| `abr.advanced.fastHalfLife` | `2` s | |
| `abr.advanced.slowHalfLife` | `5` s | |
| `abr.advanced.droppedFramesThreshold` | `0.15` | |
| `abr.advanced.droppedFramesInterval` | `2` s | |
| `abr.advanced.droppedFramesBanDuration` | `30` s | |
| `abrFactory` | `SimpleAbrManager` | |
| `adaptationSetCriteriaFactory` | default criteria | |

## Soft versus hard restrictions

Both `abr.restrictions` and top-level `restrictions` use the identical `shaka.extern.Restrictions`
shape: `minWidth 0` / `maxWidth Infinity`, `minHeight 0` / `maxHeight Infinity`,
`minPixels 0` / `maxPixels Infinity`, `minFrameRate 0` / `maxFrameRate Infinity`,
`minBandwidth 0` / `maxBandwidth Infinity`, `minChannelsCount 0` / `maxChannelsCount Infinity`.

| Level | Semantics (upstream, verbatim) |
|---|---|
| `abr.restrictions` | **Soft.** *"Any track that fails to meet these restrictions will not be selected automatically, but will still appear in the track list and can still be selected via `selectVariantTrack()`. If no tracks meet these restrictions, AbrManager should not fail, but choose a low-res or low-bandwidth variant instead."* |
| top-level `restrictions` | **Hard.** *"Any track that fails to meet these restrictions will not appear in the track list. If no tracks meet these restrictions, playback will fail."* → `RESTRICTIONS_CANNOT_BE_MET` (4012). |

Note: `abr.restrictions.maxHeight` is **not literally `Infinity`** at runtime —
`player_configuration.js` seeds it from a device-derived `abrMaxHeight`. Read
`player.getConfiguration()` if you need the effective value on a given device.

Runtime hardware cap: `player.setMaxHardwareResolution(width, height)` (L7604); disable detection
entirely with top-level `ignoreHardwareResolution: true`.

## Events that report an adaptation

| Event | Fires when | Properties |
|---|---|---|
| `adaptation` | **Automatic** adaptation changed the active tracks. Does **not** fire for app-initiated switches. | `oldTrack`, `newTrack` |
| `variantchanged` | **App-initiated** change (`selectVariantTrack`, `selectAudioTrack`, `selectVideoTrack`). Does **not** fire for automatic adaptation. | `oldTrack`, `newTrack` |
| `abrstatuschanged` | ABR toggled. | `newStatus: boolean` |
| `mediaqualitychanged` | Only when `streaming.observeQualityChanges` is `true` (default `false`). | `shaka.extern.MediaQualityInfo` |
| `trackschanged` | Track list changed, including because restrictions changed. | – |

Mixing `adaptation` and `variantchanged` into one counter corrupts any quality-distribution metric.
`getStats().switchHistory[].fromAdaptation` is the same distinction after the fact.

## "Why does HD take so long?" — upstream's own answer

From `docs/tutorials/faq.md` (`verified`): Shaka does **not** clear already-buffered content on
adaptation. *"This means that if you want to see the results of a new decision sooner, you should have
a less aggressive buffering goal."* Also: *"It may take up to 2 segments before Shaka Player has
enough information to form a bandwidth estimate"* — with 10 s segments that is 20 s at low quality
before the first decision. The three levers: lower `streaming.bufferingGoal`, raise
`abr.defaultBandwidthEstimate` (and turn `useNetworkInformation` off, or it is ignored), or shorten
segments at the packager.

This is the direct trade-off against `35-unstable-networks-and-resilience.md`, which wants a **large**
`bufferingGoal`. Pick one deliberately and record which requirement decided it.

## `AbrManager` plugin interface

`shaka.extern.AbrManager` (`externs/shaka/abr_manager.js`): `constructor()`,
`init(switchCallback, disableStreamCallback)`, `stop()`, `release()`,
`setVariants(variants, isLowLatency)`, `chooseVariant(preferFastSwitching)`, `enable()`, `disable()`,
`segmentDownloaded(deltaTimeMs, numBytes, allowSwitch, request, context)`, `trySuggestStreams()`,
`getBandwidthEstimate()`, `playbackRateChanged(rate)`, `setMediaElement(mediaElement)`,
`setCmsdManager(cmsdManager)`, `configure(config)`.

## Working snippet — cap, floor, manual selection

```js
// --- Cap and floor via SOFT restrictions: tracks stay in the list ---
player.configure({
  abr: {
    enabled: true,
    restrictions: {
      maxHeight: 720,           // never auto-select above 720p
      minHeight: 360,           // never auto-select below 360p
      maxBandwidth: 3_000_000,  // bit/s
    },
    // Make the first decision less pessimistic on a cold start:
    defaultBandwidthEstimate: 2_000_000,
    useNetworkInformation: false,  // otherwise defaultBandwidthEstimate is IGNORED
    switchInterval: 4,             // react to a new estimate sooner
  },
});

// --- HARD restriction: tracks disappear; can fail playback with 4012 ---
// player.configure('restrictions.maxHeight', 1080);

// --- Disable ABR and pin a variant by hand ---
player.configure('abr.enabled', false);
const target = player.getVariantTracks()
    .filter((t) => t.height <= 720)
    .sort((a, b) => b.bandwidth - a.bandwidth)[0];
// clearBuffer=true makes the change visible immediately at the cost of a possible stall;
// safeMargin keeps this many seconds of the old quality to avoid a rebuffer.
player.selectVariantTrack(target, /* clearBuffer= */ true, /* safeMargin= */ 4);

// --- Separate the two kinds of switch ---
player.addEventListener('adaptation',     (e) => countAbrSwitch(e.oldTrack, e.newTrack));
player.addEventListener('variantchanged', (e) => countUserSwitch(e.oldTrack, e.newTrack));
```

**Best practice.** Cap quality with `abr.restrictions` (soft), not top-level `restrictions` (hard) —
the hard version can make playback fail outright with 4012 on a device whose track list is smaller
than you assumed.
**Common mistake (two).** (a) Setting `abr.defaultBandwidthEstimate` with `abr.useNetworkInformation`
left at `true`: ignored on most Chromium browsers. (b) Calling `selectVariantTrack()` with ABR still
enabled — Shaka logs *"Changing tracks while abr manager is enabled will likely result in the selected
track being overridden. Consider disabling abr before calling selectVariantTrack()."*
