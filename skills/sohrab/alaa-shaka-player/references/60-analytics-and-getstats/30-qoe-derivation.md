For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
