Version-sensitive claims in this topic depend on [Shaka provenance and freshness](../05-provenance-and-freshness.md).

## Playback starts, then breaks

| Symptom | Code / mechanism | Fix |
|---|---|---|
| Buffering forever on a live stream | – | The FAQ's first answer is **check your time-sync**. Then `manifest.hls.liveSegmentsDelay` if the playlist has ≤3 chunks. `32-…` |
| Buffering after every live chunk | – | `player.configure('manifest.hls.liveSegmentsDelay', 1)`. `32-…` |
| Playback dies on the first transient 5xx on a live stream | – | You overrode `streaming.failureCallback` and deleted Shaka's built-in live auto-retry. `35-…` |
| VOD gives up on a single failed segment | – | **On VOD every streaming failure is fatal by default.** VOD retry must be written. `35-…` |
| Everything stalls after several HTTP errors, then a fatal `HTTP_ERROR` | `maxDisabledTime` | Variants disabled by HTTP errors return after 30 s, but **if all get disabled the error becomes fatal**. `35-…` |
| Playhead frozen with data buffered | `stalldetected` | `streaming.stallSkip`; on TV platforms `0` is recommended (pause/play instead of seeking). `35-…` |
| A long session dies with a quota error | `QUOTA_EXCEEDED_ERROR` 3017 | MSE buffer quota, not IndexedDB. Lower `bufferBehind`/`bufferingGoal`; see `streaming.avoidEvictionOnQuotaExceededError`. `35-…` |
| Video element errors and recovers by itself | `VIDEO_ERROR` 3016 + `mediasourcerecovered` | `streaming.allowMediaSourceRecoveries` (default `true`), rate-limited by `minTimeBetweenRecoveries`. `35-…` |
| Playback breaks only after a network drop and return | – | Shaka already listens for `window 'online'` and calls `retryStreaming()`. **Adding your own listener double-fires.** `35-…` |
## Quality and tracks

| Symptom | Fix |
|---|---|
| HD takes 20+ seconds to appear | Shaka does not clear the buffer on adaptation, and needs up to 2 segments for an estimate. Lower `bufferingGoal`, raise `abr.defaultBandwidthEstimate` (with `useNetworkInformation: false`), or shorten segments. `24-…` |
| `abr.defaultBandwidthEstimate` has no effect | It is **ignored** while `abr.useNetworkInformation` is `true`, which is the default and true on most Chromium browsers. `24-…` |
| `selectVariantTrack()` is immediately overridden | ABR is still enabled. Shaka logs a warning about exactly this. `24-…` |
| `player.selectAudioLanguage is not a function` | **Removed in v5.0.** Use `selectAudioTrack()`. `26-…` |
| Audio-track selection silently does nothing | The call was optional-chained onto a removed method, so it never runs. `26-…`; run `scripts/check-shaka-api.mjs` |
| The user's subtitle or audio choice reverts at the next episode | `load()` resets text selection from `preferredText[0]`. Write the choice back into config. `26-…`, `37-…` |
| Cannot pick a variant on Safari | Native HLS (`SRC_EQUALS`) *"won't let you choose an explicit variant"*. Branch on `getLoadMode()`. `22-…` |
## Subtitles and captions

| Symptom | Code | Fix |
|---|---|---|
| Side-loaded subtitles never appear | 4033 (live), 2012 / 2013 (`src=`) | `addTextTrackAsync` requires `load()` to have resolved, forbids live, and in `src=` mode allows WebVTT only. `28-…` |
| Subtitles load but are not shown | – | Selecting a text track makes it visible; `setTextTrackVisibility` was removed in v5.0. `26-…` |
| `fontScaleFactor` / `positionArea` do nothing | – | They are **UITextDisplayer only**, and the default picks `NativeTextDisplayer` unless `setVideoContainer()` was called. Check `player.getTextDisplayer()`. `28-…` |
| `--shaka-*` variables do not style captions | – | They cover **controls only**. Caption styling goes through `textDisplayer.*`, the UI caption buttons, or a custom displayer. `28-…` |
| A broken subtitle track kills playback | category `TEXT` (2) | `streaming.ignoreTextStreamFailures: true`. `28-…` |
| Caption styling changes have no runtime effect | – | You shipped `controls.css`, which flattens the custom properties at build time. Ship `controls.modern.css`. `65-…` |
