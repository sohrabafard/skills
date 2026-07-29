# Live streaming and low latency

All rows `verified` at v5.2.3, read 2026-07-28, from `externs/shaka/player.js`
(`ManifestConfiguration`, `StreamingConfiguration`, `LiveSyncConfiguration`,
`DynamicTargetLatencyConfiguration`), cross-checked against `lib/util/player_configuration.js`.

## Detection API

| Method | Meaning |
|---|---|
| `player.isLive()` | Live presentation. |
| `player.isDynamic()` | Dynamic — live **or** in-progress recording. **New in v5.0.** `goToLive()` gates on this. |
| `player.isInProgress()` | In-progress recording (dynamic VOD). |
| `player.seekRange()` | `{start, end}` — the DVR window. `end` is the live edge. |
| `player.getSegmentAvailabilityDuration()` | Availability-window length. |
| `player.getPlayheadTimeAsDate()` / `getPresentationStartTimeAsDate()` | Wall-clock mapping. |
| `getStats().liveLatency` | *"The time between the capturing of a frame and the end user having it displayed on their screen. If nothing is loaded or the content is VOD, NaN."* |

## Latency configuration

| Key | Default | Note |
|---|---|---|
| `manifest.defaultPresentationDelay` | `0` s | `0` means "compute it": DASH → lower of `1.5 * minBufferTime` and `segmentAvailabilityDuration`; HLS → **3 segment durations**. Used when the MPD omits `suggestedPresentationDelay`. |
| `manifest.availabilityWindowOverride` | `NaN` | Enforced by the parser; a custom parser must honour it. |
| `manifest.updatePeriod` | `-1` s | DASH: overrides `minimumUpdatePeriod`. HLS: `<0` derives from segment length, `>0` overrides target duration. Changing it live triggers an immediate manifest download. |
| `manifest.continueLoadingWhenPaused` | `true` | Keep refreshing the live manifest while paused. |
| `manifest.raiseFatalErrorOnManifestUpdateRequestFailure` | `false` | |
| `manifest.hls.liveSegmentsDelay` | – | FAQ remedy for *"buffering after each chunk"* when the playlist has ≤3 chunks: `player.configure('manifest.hls.liveSegmentsDelay', 1)`. |
| `streaming.lowLatencyMode` | **`true`** | Applies a low-latency profile **only on streams that signal low latency**. |
| `streaming.liveSync.enabled` | `false` | Latency chasing by rate modulation. **Upstream warning: *"on some SmartTVs, if this is activated, it may not work or the sound may be lost when activated."*** |
| `streaming.liveSync.targetLatency` | `0.5` s | |
| `streaming.liveSync.targetLatencyTolerance` | `0.5` s | |
| `streaming.liveSync.maxPlaybackRate` | `1.1` | Recommended 1–2. |
| `streaming.liveSync.minPlaybackRate` | `0.95` | Recommended 0–1. |
| `streaming.liveSync.panicMode` | `false` | Hold `minPlaybackRate` after a rebuffer. |
| `streaming.liveSync.panicThreshold` | `60` s | |
| `streaming.liveSync.dynamicTargetLatency.enabled` | `false` | |
| `…dynamicTargetLatency.stabilityThreshold` | `60` | |
| `…dynamicTargetLatency.rebufferIncrement` | `0.5` | |
| `…dynamicTargetLatency.maxAttempts` | `10` | |
| `…dynamicTargetLatency.maxLatency` / `minLatency` | `4` / `1` | |
| `streaming.updateIntervalSeconds` | `1` s | Manifest-change polling. |
| `streaming.inaccurateManifestTolerance` | `2` s | Drift compensation. |
| `streaming.maxDisabledTime` | `30` s | How long a variant stays disabled after a `NETWORK HTTP_ERROR`. |

## What `lowLatencyMode: true` silently changes

When the manifest **is** low-latency (`docs/tutorials/config.md`):

`streaming.inaccurateManifestTolerance` → `0` · `streaming.segmentPrefetchLimit` → `2` ·
`streaming.updateIntervalSeconds` → `0.1` · `streaming.maxDisabledTime` → `1` ·
`streaming.retryParameters.baseDelay` → `100` · `manifest.dash.autoCorrectDrift` → `false` ·
`manifest.retryParameters.baseDelay` → `100` · `drm.retryParameters.baseDelay` → `100`.

**Override those with `player.configurationForLowLatency({...})`, not `configure()`.** Read them back
with `player.getConfigurationForLowLatency()`.

Low-latency transport support (`README.md`): HLS *"Low-latency streaming with partial segments,
preload hints, delta updates and blocking playlist reload"*; supported tags include
`#EXT-X-SERVER-CONTROL`, `#EXT-X-PART-INF:PART-TARGET`, `#EXT-X-PART`, `#EXT-X-SKIP`,
`#EXT-X-PRELOAD-HINT`.

## What is genuinely different on a live source

| Difference | Consequence |
|---|---|
| Default start position is the **live edge**, not `0`. | A "resume from last position" feature must branch on `isLive()`. |
| `getStats().completionPercent` is `NaN` for live. | Guard with `Number.isFinite` or your averages are wrong (`60-analytics-and-getstats.md`). |
| `addTextTrackAsync()` → 4033; `addThumbnailsTrack()` → 4045; `addChaptersTrack()` → 4055. | Side-loading anything is impossible; disable the UI affordance. |
| Offline `store()` on live → `CANNOT_STORE_LIVE_OFFLINE` (9005). | Hide the download button when `isLive()`. |
| **The default `streaming.failureCallback` retries automatically on live and never on VOD.** | Overriding it deletes that behaviour. See `35-unstable-networks-and-resilience.md`. |
| Time sync matters. The FAQ's first answer to *"live stream buffering forever"* is *"Check your time-sync."* | A client clock skewed against the packager produces an unfixable-looking stall. |
| The manifest keeps updating while paused unless `manifest.continueLoadingWhenPaused: false`. | A paused live tab still costs requests. |
| `manifestupdated` fires on every refresh. | The only correct trigger to recompute the DVR window. |

## Working snippet — a live configuration

```js
player.configure({
  manifest: {
    defaultPresentationDelay: 6,      // seconds behind the live edge; 0 = auto
    continueLoadingWhenPaused: true,
    retryParameters: {maxAttempts: 8, baseDelay: 500, backoffFactor: 2, fuzzFactor: 0.5},
  },
  streaming: {
    lowLatencyMode: true,             // default; the profile applies only if the stream supports it
    rebufferingGoal: 2,
    bufferingGoal: 10,
    bufferBehind: 30,
    safeSeekEndOffset: 2,             // helps live streams with gaps at the edge
    returnToEndOfLiveWindowWhenOutside: true,
    liveSync: {
      enabled: true,                  // OFF by default; known to misbehave on some smart TVs
      targetLatency: 3,
      targetLatencyTolerance: 0.5,
      maxPlaybackRate: 1.1,
      minPlaybackRate: 0.95,
      panicMode: true,
      panicThreshold: 60,
      dynamicTargetLatency: {enabled: true, minLatency: 2, maxLatency: 8},
    },
  },
});

// Tune the low-latency profile itself. NOT via configure(): those keys are re-derived.
player.configurationForLowLatency({
  streaming: {segmentPrefetchLimit: 3, updateIntervalSeconds: 0.1},
});

await player.load(liveUri);

if (player.isLive()) {
  // Recompute the window on every refresh - never cache it.
  player.addEventListener('manifestupdated', () => {
    const {start, end} = player.seekRange();
    renderDvrScrubber(start, end);
  });
}
```

**Best practice.** Never assume a fixed DVR window — recompute `seekRange()` on `manifestupdated` and
re-clamp your scrubber. On a smart TV, leave `liveSync.enabled` at `false` unless you have tested that
model, because upstream records sound loss on some of them.
**Common mistake.** Setting low-latency overrides with `player.configure(...)`. Those keys are
re-derived from the low-latency profile, so the override silently does nothing; it belongs in
`player.configurationForLowLatency(...)`.
