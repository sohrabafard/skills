For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## `getStats()` — every field

`shaka.extern.Stats`. Overall `@description`: *"Contains statistics and information about the current
state of the player. This is meant for applications that want to log quality-of-experience (QoE) or
other stats. **These values will reset when `load()` is called again.**"*

| Field | Meaning / `NaN` conditions |
|---|---|
| `width`, `height` | Current video track dimensions. `NaN` if nothing loaded or audio-only. |
| `streamBandwidth` | Total bit/s required by current streams. **Takes `playbackRate` into account.** `NaN` if nothing loaded. |
| `currentCodecs` | Current codec string. |
| `decodedFrames`, `droppedFrames`, `corruptedFrames` | `NaN` if the browser does not report them. |
| `estimatedBandwidth` | Current estimate, bit/s. `NaN` if none. |
| `completionPercent` | Greatest completion percent experienced (a high-water mark). **`NaN` if nothing loaded or the stream is live.** |
| `loadLatency` | Seconds, `load()` → `loadedmetadata`. *"does NOT imply that playback can start."* |
| `timeToFirstFrame` | Seconds, `load()` → first frame presented. **New in 5.2.0.** Uses `requestVideoFrameCallback` when available (actual render), else falls back to `loadeddata` (decode). **Not set for audio-only.** |
| `manifestTimeSeconds` | Manifest download + parse time. |
| `drmTimeSeconds` | Time to fetch the first DRM key and load it into the CDM. `NaN` if no DRM. |
| `playTime` | **Seconds in the `playing` state. This is the watch time.** |
| `pauseTime` | Seconds in `paused`. |
| `bufferingTime` | Seconds in `buffering`. |
| `licenseTime` | Seconds on licence requests this session. `NaN` if no DRM. |
| `liveLatency` | Capture-to-display latency. **`NaN` for VOD.** |
| `maxSegmentDuration` | Presentation's max segment duration. |
| `gapsJumped` | Total gaps jumped. `NaN` if nothing loaded. |
| `stallsDetected` | Total stalls seen. `NaN` if nothing loaded. |
| `manifestSizeBytes` | DASH: latest MPD. HLS: last downloaded media playlist. **`NaN` in `src=` mode.** |
| `bytesDownloaded` | Bytes downloaded during playback. |
| `nonFatalErrorCount` | Count of non-fatal errors. |
| `manifestPeriodCount` | DASH: `<Period>` count. HLS: always `1`. **`NaN` in `src=` mode.** |
| `manifestGapCount` | DASH: inter-period discontinuities. HLS: `EXT-X-GAP` + `GAP=YES` count. **`NaN` in `src=` mode.** |
| `switchHistory` | `Array<shaka.extern.TrackChoice>` |
| `stateHistory` | `Array<shaka.extern.StateChange>` |

`shaka.extern.TrackChoice`: `timestamp` (**seconds since epoch**, i.e. `Date.now() / 1000`), `id`,
`type` (`'variant'` | `'text'`), `fromAdaptation` (`true` = AbrManager, `false` = app
`selectTrack`), `bandwidth` (`null` for text).

`shaka.extern.StateChange`: `timestamp` (seconds since epoch), `state`
(`'buffering'` | `'playing'` | `'paused'` | `'ended'`), `duration` (seconds; ***"If this is the last
entry in the list, the player is still in this state, so the duration will continue to increase."***).

Also: `player.getBufferedInfo()` → `{total, audio, video, text}`, each an `Array<{start, end}>`; and
`player.getBufferFullness()`.


## `shaka.util.StateHistory` is not a public API

| Fact | Basis |
|---|---|
| The class exists in `lib/util/state_history.js`, `@final`, *"used to track the time spent in arbitrary states"*. | `verified` |
| It is **not exported** — the file has no `@export` anywhere. Sibling internals `shaka.util.SwitchHistory` and `shaka.util.Stats` are likewise unexported. | `verified`, `grep -n "@export" lib/util/state_history.js lib/util/stats.js` → no matches |
| **Consequence:** in a compiled build the symbol is renamed or absent. Applications must use `getStats().stateHistory`, the exported view of the same data. | `inferred` |
