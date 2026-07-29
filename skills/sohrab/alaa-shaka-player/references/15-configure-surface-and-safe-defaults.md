# The `player.configure()` surface and safe defaults

`configure()` is the capability this skill exists to wrap. Every non-default value you set must be
traceable to a reference file that justifies it.

## The two call forms

```js
player.configure({streaming: {bufferingGoal: 30}});     // object merge, deep
player.configure('streaming.bufferingGoal', 30);        // dotted path + value
player.configure('drm.advanced.com\\.apple\\.fps.serverCertificateUri', url);  // escaped dots
player.resetConfiguration();                            // back to computed defaults
player.getConfiguration();
```

Escape dots inside a key-system identifier with `\\.` — otherwise `com.apple.fps` is read as four
nested keys (`verified`, `docs/tutorials/fairplay.md`, read 2026-07-28).

## When a change takes effect

| Group | Effect |
|---|---|
| `streaming.*` buffering, retries, stall/gap | Immediate. |
| `abr.*` | Immediate; the next decision uses it. |
| `drm.*`, `manifest.*`, `preferred*` | **Next `load()` only.** Upstream: *"some will not have any effect until the next call to `load()` (such as DRM settings, manifest settings, and language settings)."* (`verified`, `docs/tutorials/config.md`) |
| Low-latency overrides | Not through `configure()` at all — see below. |

## The low-latency trap

`streaming.lowLatencyMode` defaults **`true`**. On a stream that signals low latency, Shaka silently
rewrites eight other defaults (`verified`, `docs/tutorials/config.md`):

`streaming.inaccurateManifestTolerance` → `0` · `streaming.segmentPrefetchLimit` → `2` ·
`streaming.updateIntervalSeconds` → `0.1` · `streaming.maxDisabledTime` → `1` ·
`streaming.retryParameters.baseDelay` → `100` · `manifest.dash.autoCorrectDrift` → `false` ·
`manifest.retryParameters.baseDelay` → `100` · `drm.retryParameters.baseDelay` → `100`.

Override those with **`player.configurationForLowLatency({...})`** and read them back with
`player.getConfigurationForLowLatency()`. `player.configure()` will not hold, because the low-latency
profile re-derives them.

## Config-key namespaces and where each is documented here

| Namespace | Governs | Reference |
|---|---|---|
| `streaming.*` | buffering, retries, stalls, gaps, prefetch, live sync, native-HLS preference | `35-`, `32-`, `22-` |
| `manifest.*`, `manifest.dash.*`, `manifest.hls.*` | parsing, presentation delay, update period, availability window | `22-`, `32-` |
| `abr.*`, `abr.advanced.*`, `restrictions.*` | adaptation and quality caps | `24-` |
| `drm.*`, `drm.advanced.*` | key systems, robustness, licences | `45-` |
| `offline.*` | download track selection, size guard, progress, persistent licences | `50-` |
| `ads.*` | interstitials, snapback, tracking, TV/console behaviour | `55-` |
| `textDisplayer.*`, `accessibility.*` | caption rendering and forced subtitles | `28-` |
| `networking.*` | `forceHTTP`, `forceHTTPS`, progress-event threshold, common access token | `40-` |
| `mediaSource.*` | transmux worker, source elements, cue callback, extra features | `12-`, `28-` |
| `preferredAudio`, `preferredText`, `preferredVideo` | durable language/role/codec preference | `26-` |
| `playRangeStart`, `playRangeEnd`, `ignoreHardwareResolution` | top-level clamps | `30-`, `24-` |

## Working snippet — a validated defaults module

Every value is named, bounded and traced. No magic numbers reach `configure()`.

```ts
/** Player tuning knobs. Every field has a stated range; out-of-range throws at construction,
 *  not silently at playback time. */
export interface PlayerTuning {
  /** Seconds fetched ahead of the playhead. 5..120. Higher survives longer outages
   *  but delays the visible effect of an ABR decision (24-adaptive-bitrate...). */
  readonly bufferAheadSeconds: number;
  /** Seconds that must be buffered before playback resumes. 0..30, and < bufferAheadSeconds. */
  readonly resumeAtSeconds: number;
  /** Attempts per request across manifest/segment/licence. 1..10.
   *  Shaka's own default is 2. Values come from /alaa-reliability-sla ($alaa-reliability-sla). */
  readonly requestAttempts: number;
  /** Overall per-request timeout, ms. 5000..60000. */
  readonly requestTimeoutMs: number;
  /** Hard ceiling on auto-selected height, px. 240..2160. Applied as a SOFT abr restriction. */
  readonly maxAutoHeight: number;
}

const RANGES: Record<keyof PlayerTuning, readonly [number, number]> = {
  bufferAheadSeconds: [5, 120],
  resumeAtSeconds: [0, 30],
  requestAttempts: [1, 10],
  requestTimeoutMs: [5_000, 60_000],
  maxAutoHeight: [240, 2160]
};

export const DEFAULT_TUNING: PlayerTuning = Object.freeze({
  bufferAheadSeconds: 30,
  resumeAtSeconds: 2,
  requestAttempts: 6,
  requestTimeoutMs: 20_000,
  maxAutoHeight: 1080
});

/** Validates at the boundary, then builds the Shaka config. Throws on a bad value. */
export function buildPlayerConfig(input: Partial<PlayerTuning> = {}): Record<string, unknown> {
  const t: PlayerTuning = { ...DEFAULT_TUNING, ...input };

  for (const key of Object.keys(RANGES) as (keyof PlayerTuning)[]) {
    const [min, max] = RANGES[key];
    const value = t[key];
    if (!Number.isFinite(value) || value < min || value > max) {
      throw new RangeError(`PlayerTuning.${key} must be in [${min}, ${max}]; received ${value}`);
    }
  }
  if (t.resumeAtSeconds >= t.bufferAheadSeconds) {
    // Upstream: "rebufferingGoal should always be less than bufferingGoal".
    throw new RangeError("resumeAtSeconds must be less than bufferAheadSeconds");
  }

  const retry = {
    maxAttempts: t.requestAttempts,
    baseDelay: 500,
    backoffFactor: 2,
    fuzzFactor: 0.5,            // keep at 0.5: it exists to stop client stampedes
    timeout: t.requestTimeoutMs,
    stallTimeout: 5_000,
    connectionTimeout: 8_000
  };

  return {
    // v6-ready spelling; the individual preferred* scalars are removed in v6.0.
    preferredAudio: [{ language: "fa" }, { language: "en" }],
    preferredText: [],
    preferredVideo: [{ hdrLevel: "AUTO" }],

    manifest: { retryParameters: { ...retry, maxAttempts: t.requestAttempts + 2 } },
    drm: { retryParameters: { ...retry, maxAttempts: Math.min(4, t.requestAttempts) } },

    streaming: {
      retryParameters: retry,
      bufferingGoal: t.bufferAheadSeconds,
      rebufferingGoal: t.resumeAtSeconds,
      bufferBehind: 30,
      // Branch on load mode at runtime, never on user-agent. See 22-streaming-formats...
      preferNativeHls: false,
      useNativeHlsForFairPlay: true
    },

    // SOFT cap: the track stays in the list and selectable by hand.
    // Top-level `restrictions` is HARD and can fail playback with 4012.
    abr: { enabled: true, restrictions: { maxHeight: t.maxAutoHeight } }
  };
}
```

**Best practice.** Configure once immediately after `attach()`, and configure **per asset** on the
`streaming` event, which fires after the tracks are known and before any segment is fetched. Use
`manifestparsed` for `updateStartTime()`.
**Common mistake.** Setting `abr.defaultBandwidthEstimate` while leaving `abr.useNetworkInformation`
at its default `true` — the estimate is then ignored wherever the Network Information API exists,
which is most Chromium browsers. Upstream documents this explicitly.
