# Streaming formats and the native-HLS fallback

All rows `verified` at v5.2.3, read 2026-07-28.

## Current position

DASH and HLS are the two first-class manifest formats. **MSS (Microsoft Smooth Streaming) was removed
in v5.0 and does not exist in 5.2.3.** A third, experimental format — **MSF (MOQT Streaming Format)
over Media-over-QUIC** — ships only in the `experimental` build and does **not** support VOD.

| Format | VOD | Live | Event | In-progress recording | Source |
|---|---|---|---|---|---|
| DASH | Y | Y | – | Y | `README.md` manifest matrix |
| HLS | Y | Y | Y | – | same |
| MSS | **removed in v5.0** | | | | `upgrade.md` v5.0; `lib/mss/` absent; `// RETIRED: 'MSS': 5,` in `lib/net/networking_engine.js` |
| MSF / MoQT | **no** (`MSF_VOD_CONTENT_NOT_SUPPORTED` 4058) | Y | | | `README.md` |

## `useNativeHlsOnSafari` no longer exists

Removed in v5.0 and split into two narrower switches:

| Key | Default | Meaning |
|---|---|---|
| `streaming.useNativeHlsForFairPlay` | **`true`** | Desktop Safari has both MSE and native HLS. Keep `true` for FairPlay. Upstream warning: *"Where single-key DRM streams work fine, multi-keys streams is showing unexpected behaviours (stall, audio playing with video freezes, …). Use with care."* |
| `streaming.preferNativeHls` | `false` | Prefer native HLS on **any** browser when possible. |
| `streaming.preferNativeDash` | `false` | Prefer native DASH when possible. |

Carrying `streaming.useNativeHlsOnSafari` forward from a v4 codebase is a **silent no-op**: Shaka's
config validator warns about the unknown field, but the intent is lost.

## What changes under native playback (`LoadMode.SRC_EQUALS`)

| Consequence | Error code |
|---|---|
| `player.preload()` resolves to `null` — nothing to preload. | `SRC_EQUALS_PRELOAD_NOT_SUPPORTED` 7005 |
| `getStats().manifestSizeBytes`, `.manifestPeriodCount`, `.manifestGapCount` are `NaN`. | – |
| Adding external text throws; only WebVTT works at all. | `CANNOT_ADD_EXTERNAL_TEXT_TO_SRC_EQUALS` 2012, `TEXT_ONLY_WEBVTT_SRC_EQUALS` 2013 |
| `selectVariantTrack()` degrades: Safari native HLS *"won't let you choose an explicit variant, though you can choose audio languages this way"* (`lib/player.js` `selectSrcEqualsMode()`). | – |

## Where DASH and HLS actually differ in Shaka

| Difference | Detail |
|---|---|
| Period model | DASH: real multi-period, flattened into one timeline. HLS: `manifestPeriodCount` is **always 1**. |
| Gap accounting | DASH `manifestGapCount` = inter-period discontinuities. HLS = count of `EXT-X-GAP` + `GAP=YES`. |
| Manifest size stat | DASH: latest MPD. HLS: last downloaded **media playlist**, not the multivariant. |
| Sequence mode | **Changed in 5.2.0: "HLS: Disable sequenceMode by default."** Previously HLS used MSE sequence mode by default. |
| Presentation delay default | DASH: lower of `1.5 * minBufferTime` and `segmentAvailabilityDuration`. HLS: **3 segment durations**. |
| Update period | Same key `manifest.updatePeriod` (default `-1`); DASH overrides `minimumUpdatePeriod`, HLS overrides target duration. |
| Codec guessing | HLS without `CODECS` → Shaka guesses `avc1.42E01E` video + `mp4a.40.2` audio, **which breaks audio-only and video-only streams**. Tunable under `manifest.hls`. Symptom: `chunk demuxer append failed`. |
| Transmuxing | HLS MPEG-2 TS must be transmuxed to fMP4 (`12-bundling-and-vite-loading.md`). DASH normally does not. |
| DRM | FairPlay is HLS-only in practice on Safari; DASH supports Widevine/PlayReady/FairPlay/WisePlay/ClearKey. |
| Parser config | `manifest.dash.*`, `manifest.hls.*`, `manifest.msf.*` are separate sub-objects. |

## Manifest failure codes worth recognising

`UNABLE_TO_GUESS_MANIFEST_TYPE` 4000 · `DASH_INVALID_XML` 4001 · `DASH_NO_SEGMENT_INFO` 4002 ·
`HLS_PLAYLIST_HEADER_MISSING` 4015 · `INVALID_HLS_TAG` 4016 · `HLS_INVALID_PLAYLIST_HIERARCHY` 4017 ·
`HLS_REQUIRED_ATTRIBUTE_MISSING` 4023 · `HLS_REQUIRED_TAG_MISSING` 4024 ·
`HLS_COULD_NOT_GUESS_CODECS` 4025 · `CONTENT_UNSUPPORTED_BY_BROWSER` 4032 · `NO_VARIANTS` 4036 ·
`HLS_EMPTY_MEDIA_PLAYLIST` 4053 · `HLS_MSE_ENCRYPTED_MP2T_NOT_SUPPORTED` 4040. Full list in
`70-error-taxonomy-and-codes.md`.

## Working snippet — force MSE, and fall back consciously

```js
player.configure({
  streaming: {
    // Force MSE even on Safari for non-FairPlay content:
    preferNativeHls: false,
    preferNativeDash: false,
    // But let FairPlay use Apple's native pipeline (the recommended default):
    useNativeHlsForFairPlay: true,
  },
});

await player.load(uri);

// Branch on the ACTUAL mode. Never on user-agent.
if (player.getLoadMode() === shaka.Player.LoadMode.SRC_EQUALS) {
  // Native path. Disable in your UI, because these will not work here:
  //  - side-loading non-WebVTT text  (2012 / 2013)
  //  - preload()                     (returns null / 7005)
  //  - explicit variant selection
  // And do not report manifestSizeBytes / manifestPeriodCount / manifestGapCount:
  // they are NaN, not 0.
  disableAdvancedTrackMenu();
}
```

```js
// HLS with no CODECS attribute and audio-only or video-only renditions:
// override Shaka's guess rather than shipping the "chunk demuxer append failed" symptom.
player.configure('manifest.hls', {
  // Inspect manifest.hls.* in getConfiguration() for the current key set at your version
  // before setting anything here; the sub-object has grown across 5.x.
});
```

**Best practice.** Branch on `player.getLoadMode()` after `load()` resolves, and drive UI capability
from that single value. It is the only correct signal for "can this session side-load text, preload,
or pick a variant".
**Common mistake.** Assuming Safari means native HLS. Desktop Safari has both MSE and native HLS, and
which one you get depends on `preferNativeHls`, `useNativeHlsForFairPlay` and whether the content is
FairPlay-protected — not on the browser name.
