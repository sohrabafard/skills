For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
