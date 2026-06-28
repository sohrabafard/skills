# Migration: Shaka Player 5.0.8 to 5.1.11

Use this file when a repo was built with this skill while `v5.0.8` was the
latest covered baseline and now needs to move to `v5.1.11`.

## Evidence boundary

This guide is based on:

- official GitHub release notes for `v5.0.8` through `v5.1.11`
- the official Shaka Player upgrade guide
- generated Shaka API documentation for public config/API names

Do not derive migration requirements from source-code diffs alone. The GitHub
compare view can help navigate commits, but release notes and official docs are
the migration contract.

## Upgrade verdict

Moving from `v5.0.8` to `v5.1.11` is still within Shaka major version 5, so do
not expect a broad breaking rewrite. The main application-facing migration item
is the `v5.1` preference configuration change:

- old individual preference fields still work today
- they emit deprecation warnings
- they are documented as being removed in the next major version
- touched code should migrate to structured preference arrays now

## Required code audit

### 1. Package and bundle pin

- Confirm the app really runs `shaka-player@5.1.11` after the lockfile update.
- Confirm the app imports the same compiled/debug build path it already uses
  successfully under Vite.
- Re-test SSR guards and dynamic import paths; do not import Shaka in server
  code.

### 2. Preference configuration

Search for deprecated individual fields and replace them in touched code:

- `preferredAudioLanguage`
- `preferredAudioRole`
- `preferredAudioLabel`
- `preferredAudioChannelCount`
- `preferredAudioCodecs`
- `preferSpatialAudio`
- `preferredTextLanguage`
- `preferredTextRole`
- `preferredTextFormats`
- `preferForcedSubs`
- `preferredVideoLabel`
- `preferredVideoRole`
- `preferredVideoHdrLevel`
- `preferredVideoLayout`
- `preferredVideoCodecs`

Use:

- `preferredAudio`, an array of `shaka.extern.AudioPreference`
- `preferredText`, an array of `shaka.extern.TextPreference`
- `preferredVideo`, an array of `shaka.extern.VideoPreference`

Example shape:

```js
player.configure({
  preferredAudio: [
    { language: 'fa', channelCount: 2 },
    { language: 'en' },
  ],
  preferredText: [
    { language: 'fa', forced: false },
    { language: 'en' },
  ],
})
```

Preserve product behavior by converting fallback order intentionally instead of
flattening several old fields into one preference.

### 3. Track, subtitle, and chapter behavior

- Re-test external text tracks and `preferredText`; release notes include a fix
  for preferred text with external tracks.
- If the product has subtitle sync controls, consider using documented
  `subtitleDelay` instead of app-only cue rewriting.
- If the product has chapters, prefer `getChaptersAsync` and test
  `chaptersUri`, chapter images, chapter menu thumbnails, seek-bar hover
  images, and MediaSession chapter metadata.
- If the app still separates text-track selection from visibility, re-check the
  v5 upgrade guide: selecting a text track is now the visibility action.

### 4. Startup, seeking, and rate controls

- Keep using `player.updateStartTime()` for startup offsets before load instead
  of setting `video.currentTime` during startup.
- Re-test custom playback-rate menus. Current release notes clamp playback rate
  behavior to 16x.
- Re-test end-of-stream and near-end seeking for assets with slightly different
  audio/video durations.

### 5. Networking and authenticated playback

- Keep request filters registered before `load()`.
- Re-test expired-token flows because request filters run on retry attempts.
- If the app carries the same access token across requests, review documented
  `networking.commonAccessTokenHeaderName` before replacing a working custom
  filter.
- Re-test URLs with dots in query parameters and uppercase MIME types; both have
  release-note fixes after `v5.0.8`.

### 6. DRM and encrypted content

- Re-test loading a second asset after DRM playback; `v5.1.10` fixes a hang in
  that path.
- Re-test destroy/unmount during DRM key-status changes.
- Re-test PlayReady on Windows browsers, not only Edge.
- Re-test HLS SAMPLE-AES identity streams and track switching.
- For offline DRM, verify license requests happen only when persistent licenses
  are intended.

### 7. HLS, DASH, and live playback

- Remove or gate app-level workarounds for issues now covered by release notes,
  but only after local reproduction no longer shows the problem.
- Re-test LL-HLS live playlist updates, discontinuity sequences, long DVR
  startup, timeline sync, duplicate segment handling, and live window return.
- Re-test HLS `audio/x-mpegurl`, AC-4 immersive stereo detection, chapter
  images, `CAN-SKIP-DATERANGES`, external chapters, and SGAI streams if the
  product uses them.
- Re-test DASH startup and manifest parsing, especially large multi-period
  manifests and automatic XLink processing.

### 8. Ads and interstitials

- If ad analytics currently treats ad-break start as actual playback, switch the
  state machine to listen for real ad playback start where appropriate.
- Use `ad-playing` for "the ad actually started" behavior.
- Use `ad-interstitial-preloaded` for preload-aware UX when applicable.
- Read the `startedAt` data on `ad-break-started` when the product needs exact
  ad-break timing.
- Re-test HLS Interstitials, X-ASSET-LIST, X-PLAYOUT-LIMIT, `_HLS_start_offset`,
  ad marker alignment, pre-roll replay prevention, and single-media-element
  device behavior.

### 9. Shaka UI integration

- If using Shaka UI controls, re-test volume, mute, menus, touch seeking,
  chapter menus, and MediaSession.
- If using custom `controlPanelElements`, review whether `mute_volume` should
  replace separate mute and volume elements for smoother hover behavior.
- Consider documented UI options such as `showUIOnPaused`,
  `showMenusOnTheRight`, new track label formats, `mediaSession.allowAutoPiP`,
  chapter images, and menu placement.
- Re-test custom captions UI with the line-through styling fix in `v5.1.11`.

### 10. Telemetry and performance checks

- Re-baseline startup time, rebuffering, dropped frames, variant switches,
  parsing time, memory growth, and teardown.
- If the app uses a custom ABR manager, verify it still beats Shaka defaults.
  The 5.1 line gives ABR more low-latency and dropped-frame information.
- Re-test stats consumers for negative-time assumptions and QoE calculations.

## Newly available UX opportunities

After the migration, agents can consider these user-facing improvements:

- Audio/text/video preference fallback stacks:
  let users prefer a language, channel count, codec, forced-subtitle policy, or
  HDR/layout profile in priority order.
- Subtitle sync adjustment:
  expose a small subtitle timing offset control backed by `subtitleDelay`.
- Rich chapter navigation:
  show chapter thumbnails in menus, seek-bar hover previews, and MediaSession.
- Better ad state UX:
  distinguish "ad break scheduled", "interstitial preloaded", and "ad actually
  playing" for timers, overlays, analytics, and fail-open behavior.
- Low-latency live smoothing:
  use Shaka's improved ABR signals before writing a custom ABR manager.
- TV and device-targeted playback:
  evaluate TiVo OS, Titan OS, Titan HDR/screen-size detection, and remote-control
  behavior when those platforms are in scope.
- Improved mobile/player controls:
  use the newer UI controls for paused-state visibility, right-side menus,
  touch seeking, wheel volume, Auto PiP, and mute/volume hover behavior.
- Metadata-driven overlays:
  use public timeline/EMSG/ID3 region functions, raw CEA-608 extraction, and
  download event context for cuepoint overlays, diagnostics, and accessibility.
- Playlist and schedule polish:
  use queue item metadata to drive richer playlist cards and conductor state.
- Advanced streaming experiments:
  evaluate DASH JSON, automatic XLink processing, HLS skip dateranges, MSF/MoQT,
  and authorization-token support only when the product genuinely needs them.

## Validation checklist

Run the smallest meaningful local gate first, then expand:

- package lock confirms `shaka-player@5.1.11`
- no deprecation warnings for old preference fields in touched flows
- one HLS VOD path
- one HLS live or LL-HLS path if supported
- one DASH path if supported
- subtitles, external text, forced text, and manual subtitle delay if present
- audio, text, and video preference fallback order
- DRM load, destroy, and load-after-DRM
- token refresh on retry
- ad start, ad preload, ad failure, and resume
- Shaka UI controls if used
- route unmount/remount memory and listener cleanup
- Safari/iOS pass if HLS or FairPlay is in scope
