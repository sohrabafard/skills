# Analytics, `getStats()` and QoE quantities

All rows `verified` at v5.2.3, read 2026-07-28.

## The seam — read this before naming anything

**This skill states which *quantities* playback can produce. It defines no name.** Every event name,
field name and metric name is requested from `/alaa-services-contract`
(`$alaa-services-contract`), `references/24-metric-registry.md` and
`references/20-operational-and-observability-contract.md`. Requirement levels and gates are
`/alaa-observability-soc` (`$alaa-observability-soc`). A payload shape invented in a player file is a
defect regardless of how reasonable it looks.

**Two pipeline facts bound any claim you make about a count.** The WA tables `wa_raw.events_raw` and
`wa_raw.watch_segments_raw` already exist with a settled schema, monthly partitions and `project_id`
first in `ORDER BY`.

- Sinks retry **20×** against a plain `MergeTree` with block deduplication **off**, so `count()` is an
  **upper** bound. A player event carrying no idempotency key makes over-count *structural*, not
  incidental.
- Vector's disk buffer sits on an `emptyDir` with one replica, so buffered events are **lost on pod
  replacement after clients were told `202`**, making `count()` also a **lower** bound.

So no dashboard built on these tables may state a playback count as exact. Emit an idempotency key
with every playback event (the key's **name** comes from the contract), and write the two bounds into
any figure derived from them.

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

## Events available for analytics

`buffering` (`buffering: boolean`) · `stalldetected` · `gapjumped` · `adaptation`
(`oldTrack`, `newTrack`; **automatic**) · `variantchanged` (**app-initiated**) · `textchanged` ·
`trackschanged` · `audiotrackschanged` · `audiotrackchanged` · `abrstatuschanged` (`newStatus`) ·
`error` (`detail`) · `statechanged` (`newstate`) · `onstatechange` (`state`) · `ratechange` ·
`loading` / `loaded` / `unloading` (`isSwitchingContent`) · `manifestparsed` / `streaming` /
`manifestupdated` · `downloadcompleted` (`requestType`, `request`, `context`, `response`) ·
`downloadfailed` (`requestType`, `request`, `context`, `error`, `httpResponseCode`, `aborted`) ·
`downloadheadersreceived` · `segmentappended` (`start`, `end`, `contentType`, `isMuxed`,
`isDependency`, **`mediaTimestamp`** new in 5.2.0, `null` if unparseable) · `mediaqualitychanged`
(only when `streaming.observeQualityChanges === true`) · `mediasourcerecovered` ·
`expirationupdated` / `keystatuschanged` / `drmsessionupdate` · `firstquartile` / `midpoint` /
`thirdquartile` / `complete` / `started` · and the specialised set `prft`, `emsg`, `metadata`,
`metadataadded`, `timelineregionadded`/`enter`/`exit`, `sessiondata`, `programinformation`,
`boundarycrossed`, `spatialvideoinfo`, `nospatialvideoinfo`, `canupdatestarttime`,
`configurationchanged`, `bufferappending`, `licenserenewal`.

`downloadfailed` is the best hook for CDN error telemetry — but record `requestType` and
`httpResponseCode`, **never `request.uris`**, which is a presigned credential
(`42-media-url-trust-and-presigned.md`).

## Deriving watch-time and QoE correctly

Shaka gives you the **inputs**, not a figure. There is **no derived QoE number, no watch-time metric
and no beaconing** in Shaka; aggregation, session identity and transport are the application's job
(`inferred` from the `Stats` `@description`). The ten rules that make a derivation correct rather than
approximately correct:

1. **`playTime` is already the watch time.** It excludes paused and buffering time. Do **not** compute
   it from wall-clock deltas — a wall-clock delta at 2× playback under-counts content time by half.
2. **Snapshot before every `load()`.** All counters reset. The `unloading` event is the last moment
   they exist.
3. **The last `stateHistory` entry has a growing `duration`.** Treat it as open; summing `duration`
   naively across a polled series double-counts.
4. **`timestamp` fields are seconds since epoch, not milliseconds.** Multiply by 1000 for `Date`.
5. **Many fields are `NaN`, not `0`.** `completionPercent` on live, `liveLatency` on VOD,
   `licenseTime` and `drmTimeSeconds` without DRM, decode counters on browsers that do not report
   them, and the three manifest fields in `src=` mode. Guard with `Number.isFinite`.
6. **Rebuffer ratio** = `bufferingTime / (playTime + bufferingTime)`. Startup buffering is included in
   `bufferingTime`; subtract the `loadLatency` window if you want a mid-stream ratio.
7. **Startup: use `timeToFirstFrame`, not `loadLatency`.** `loadLatency` stops at `loadedmetadata` and
   explicitly *"does NOT imply that playback can start"*. `timeToFirstFrame` is 5.2.0+ and unset for
   audio-only.
8. **Distinguish who switched.** `TrackChoice.fromAdaptation` separates ABR from user decisions;
   mixing them corrupts any quality-distribution metric.
9. **`streamBandwidth` incorporates `playbackRate`** — during trick play it is not the stream's
   nominal bitrate.
10. **Count errors from `nonFatalErrorCount` plus your `error` listener**, and network failures from
    `downloadfailed`, which gives `httpResponseCode` and `aborted`.

## Hidden-tab policy — a default, not a question

Hidden-tab time **does not accumulate** as watch time. `ignoreHiddenTab` is `true` unless a written
product requirement says otherwise; record which requirement changed it in the config comment. Note
that `playTime` keeps advancing while a hidden tab plays audio, so excluding it is your subtraction,
not Shaka's.

## Working snippet — a QoE quantity collector

```js
// Quantities only. Every NAME below is a local variable, not a wire field.
// Wire names come from /alaa-services-contract ($alaa-services-contract).
const q = { rebufferEvents: 0, rebufferMs: 0, abrSwitches: 0, userSwitches: 0, downloadFailures: [] };

let rebufferStartedAt = null;
player.addEventListener('buffering', (e) => {
  if (e.buffering) { rebufferStartedAt = performance.now(); q.rebufferEvents++; }
  else if (rebufferStartedAt !== null) {
    q.rebufferMs += performance.now() - rebufferStartedAt;
    rebufferStartedAt = null;
  }
});
player.addEventListener('adaptation',     () => q.abrSwitches++);
player.addEventListener('variantchanged', () => q.userSwitches++);
player.addEventListener('downloadfailed', (e) => {
  // requestType + status only. NEVER e.request.uris: it is a presigned credential.
  q.downloadFailures.push({ type: e.requestType, status: e.httpResponseCode, aborted: e.aborted });
});

const num = (v) => (Number.isFinite(v) ? v : null);   // NaN-safe: NaN is not 0

function snapshotQuantities() {
  const s = player.getStats();
  const playTime = num(s.playTime) ?? 0;
  const bufferingTime = num(s.bufferingTime) ?? 0;

  return {
    // --- startup ---
    loadLatencySeconds:      num(s.loadLatency),        // -> loadedmetadata only
    timeToFirstFrameSeconds: num(s.timeToFirstFrame),   // -> real first frame (5.2.0+)
    manifestTimeSeconds:     num(s.manifestTimeSeconds),
    drmTimeSeconds:          num(s.drmTimeSeconds),
    licenseTimeSeconds:      num(s.licenseTime),
    // --- watch time: playTime, NOT wall clock ---
    watchTimeSeconds: playTime,
    pauseTimeSeconds: num(s.pauseTime),
    bufferingTimeSeconds: bufferingTime,
    rebufferRatio: (playTime + bufferingTime) > 0
        ? bufferingTime / (playTime + bufferingTime) : null,
    rebufferEventCount: q.rebufferEvents,
    // --- quality ---
    widthPixels: num(s.width), heightPixels: num(s.height),
    currentCodecs: s.currentCodecs,
    streamBandwidthBps:    num(s.streamBandwidth),      // includes playbackRate
    estimatedBandwidthBps: num(s.estimatedBandwidth),
    decodedFrameCount: num(s.decodedFrames),
    droppedFrameCount: num(s.droppedFrames),
    corruptedFrameCount: num(s.corruptedFrames),
    abrSwitchCount: q.abrSwitches, userSwitchCount: q.userSwitches,
    // --- resilience ---
    gapsJumpedCount: num(s.gapsJumped),
    stallsDetectedCount: num(s.stallsDetected),
    nonFatalErrorCount: num(s.nonFatalErrorCount),
    downloadFailures: q.downloadFailures,
    // --- delivery ---
    bytesDownloaded: num(s.bytesDownloaded),
    maxSegmentDurationSeconds: num(s.maxSegmentDuration),
    // --- live / VOD ---
    liveLatencySeconds: num(s.liveLatency),             // NaN for VOD
    completionPercent:  num(s.completionPercent),       // NaN for live
    // --- histories: timestamps are SECONDS since epoch ---
    switchHistory: s.switchHistory.map((c) => ({
      atMs: c.timestamp * 1000, id: c.id, type: c.type,
      bandwidthBps: c.bandwidth, by: c.fromAdaptation ? 'abr' : 'app',
    })),
    stateHistory: s.stateHistory.map((h, i, arr) => ({
      atMs: h.timestamp * 1000, state: h.state, durationSeconds: h.duration,
      open: i === arr.length - 1,     // the LAST entry is still growing
    })),
  };
}

// Counters reset on load(). 'unloading' fires for every path that ends a session.
player.addEventListener('unloading', () => enqueue(snapshotQuantities()));
window.addEventListener('pagehide',  () => enqueue(snapshotQuantities()));
// 'pagehide' fires where 'visibilitychange'->hidden alone does not cover a closed tab.
```

Delivery to the backend needs an idempotency key per record and a buffer that survives a rejected
send. Do **not** zero an accumulator before the send resolves, or a single failure loses the interval
permanently. Field names, the key's name, and the endpoint all come from `/alaa-services-contract`.

**Best practice.** Use `playTime` for watch time and flush on `unloading`; that is the only point at
which you are guaranteed to see the session's final counters before they reset.
**Common mistake.** Treating `NaN` fields as `0` and shipping them. The resulting averages —
dropped-frame rate, live latency, completion percent — are silently wrong, and a dashboard cannot
tell the difference between "the browser did not report it" and "it was zero".
