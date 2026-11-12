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

## Keys added or changed in 5.3

Defaults: `lib/util/player_configuration.js` at tag v5.3.4. Docs: `externs/shaka/player.js` at the same tag.
PR numbers: `https://github.com/shaka-project/shaka-player/blob/v5.3.4/CHANGELOG.md`. All `verified`, read 2026-11-12.
5.3.0 reports no breaking change (CHANGELOG at v5.3.4). The 5.2.x text elsewhere in this file stays valid unless a row below says otherwise.

| Key | 5.3.4 default | Rule |
|---|---|---|
| `streaming.useNativeHlsForFairPlay` | **`false`**. It was `true` in 5.2.13. | PR #10699 (5.3.0) changed it. The code takes effect only on the WebKit engine with `drm.servers['com.apple.fps']` or `['com.apple.fps.1_0']` set. Safari then prefers MSE over native HLS. Set the value explicitly. Never rely on the default. |
| `streaming.fallbackToNativeHlsOnMseError` | `false`. Apple browsers set `true` (`lib/device/apple_browser.js`, `adjustConfig`). That override is applied only in `PlayerConfiguration.createDefault`, so a later `player.configure()` value wins (`lib/util/player_configuration.js` at v5.3.4, `verified`, read 2026-11-12). | PR #10699. On error 4040 or 4041 for an HLS load, when the browser can play native HLS (`canPlayType` is not empty), Shaka retries that one load with native HLS (`lib/player.js` at v5.3.4, `verified`). The retry does not change `preferNativeHls`. When a stream depends on a request filter, read `40-networking-engine-and-filters.md`, section "Native HLS playlist and segment requests skip request filters", before you leave this key on. |
| `abr.allowAudioFallback` | `true` | PR #10689. See `24-adaptive-bitrate-and-restrictions.md`. |
| `drm.keepDrmEngineOnDetach` | `false` | PR #10530. `true` keeps MediaKeys and sessions across `detach()` and `unload()`. A later `attach()` and `load()` of the same asset reuses them. A different asset negotiates DRM as before. Read `45-drm.md` for session handling. |
| `queue.autoPlayNext` | `true` | PR #10503. `true` keeps the old behaviour: advance at the end of an item and preload the next. `false` stops at the end of the item and preloads nothing. `repeatMode` is independent. |
| `cmcd.includeInRequests` | `[]` | PR #10590. Tokens (externs at v5.3.4, `verified`, read 2026-11-12): `'segment'`, which also covers init segments, `'init'`, `'mpd'`, `'mpdpatch'`, `'xlink'`, `'mpdlink'`, `'steering'`, `'callback'`, or `'*'`. `[]` keeps the historical set: manifests, media and init segments, sidecar text, licence, key, certificate and timing requests. |
| `cmcd.applyParametersFromManifest` | `true` | PR #10590. CMCD parameters that a DASH manifest signals can switch CMCD on for that presentation. They override `version`, `useHeaders`, `includeKeys`, `includeInRequests`, `contentId` and `sessionId`. Set `false` to ignore the signal. Header mode from a manifest causes CORS preflights. |

**Conflict C9, `useNativeHlsForFairPlay`.** The externs doc at v5.3.4 says "Defaults to `true`". The code says `false`. Follow the code and see `05-provenance-and-freshness.md`. `22-streaming-formats-and-native-hls.md` states both values with their versions.

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
| `cmcd.*`, `queue.*` | CMCD reporting; queue advance (rows above) | this file |
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
      // Explicit on purpose: the default changed from true to false in 5.3 (C9 above).
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
