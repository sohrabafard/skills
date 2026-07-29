# Troubleshooting by symptom

Find the symptom. Each entry names the mechanism, then routes to the reference that owns it.
Where a Shaka error code exists for the symptom, it is given.

## The player never appears, or crashes on the server

| Symptom | Cause | Fix |
|---|---|---|
| `window is not defined`, `HTMLMediaElement is not defined`, `document is not defined` in an SSR build | Shaka imported at module top level | Dynamic `import()` inside `onMounted`. Nothing under `src/boot/` imports Shaka. `11-vue-quasar-binding.md` |
| `shaka is not defined` at runtime, or `shaka.ui is undefined` | Imported the package `main`, which is the **non-UI** build; or expected named ESM exports, which do not exist | Import `shaka-player/dist/shaka-player.ui.js` explicitly and unwrap `.default`. `12-bundling-and-vite-loading.md` |
| TypeScript accepts `shaka.ui.Overlay` but it is `undefined` at runtime | `"types"` resolves to the **non-UI** `.d.ts` (conflict C8) | Reference `dist/shaka-player.ui.d.ts` or add an ambient declaration. `12-…` |
| Proxy-shaped failures at load time; internal Shaka values are Proxies | The Player was made reactive | Hold it in a closure-scoped `let`. `11-vue-quasar-binding.md` |

## Playback fails to start

| Symptom | Code | Fix |
|---|---|---|
| `load()` rejects and nothing reaches the `error` listener | – | Load-time failures reject the promise. You need **both** paths. `70-error-taxonomy-and-codes.md` |
| Manifest 404 / 5xx | `BAD_HTTP_STATUS` 1001, `HTTP_ERROR` 1002 | Check `data[1]` (status) and `data[4]` (RequestType). Cancel a hopeless VOD 404 loop via the `retry` event. `35-…` |
| Manifest type not recognised | `UNABLE_TO_GUESS_MANIFEST_TYPE` 4000 | Pass `mimeType` to `load()`. `22-…` |
| `chunk demuxer append failed` on HLS | `HLS_COULD_NOT_GUESS_CODECS` 4025 nearby | HLS without `CODECS` makes Shaka guess `avc1.42E01E` + `mp4a.40.2`, breaking audio-only and video-only streams. Fix the manifest or tune `manifest.hls.*`. `22-…` |
| Nothing plays and the track list is empty | `RESTRICTIONS_CANNOT_BE_MET` 4012, `NO_VARIANTS` 4036 | A **top-level** `restrictions` is hard and removes tracks. Use `abr.restrictions`. `24-…` |
| Encrypted content fails on `http://` | `NO_WEB_CRYPTO_API` 4042, `REQUESTED_KEY_SYSTEM_CONFIG_UNAVAILABLE` 6001 | EME requires a secure origin. `75-…`, `45-drm.md` |
| CORS preflight fails after adding a header in a filter | `HTTP_ERROR` 1002 | The custom header must be in `Access-Control-Allow-Headers`. `40-…` |
| A filter throws | `REQUEST_FILTER_ERROR` 1006, `RESPONSE_FILTER_ERROR` 1007 | Wrap anything that can fail and decide deliberately whether to fail the request. `40-…` |

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

## DRM

| Symptom | Code | Fix |
|---|---|---|
| FairPlay works on one Safari path and stalls on another | – | Modern EME (`com.apple.fps`) and legacy Apple Media Keys (`com.apple.fps.1_0`) are different paths; MSE+CMAF works only with Modern EME and MSE+TS with neither. `45-…` |
| "Certificate" errors that a valid HTTPS cert does not fix | `INVALID_SERVER_CERTIFICATE` 6004 | The FAQ is explicit: this is the DRM provider's licence certificate, ***not*** the HTTPS certificate of the proxy. `45-…` |
| Licence requests fire but playback never starts | `LICENSE_RESPONSE_REJECTED` 6008 | *"Check the DevTools network tab for the response."* Verify the response filter unwrapping. `45-…` |
| Robustness settings appear ignored | – | Since v5.0 `videoRobustness` / `audioRobustness` are **`Array<string>`**; a bare string does not do what you expect. `45-…` |
| Licence 401 mid-session, and the retry sends the same expired token | – | The filter captured a token value instead of a getter. Filters run per attempt since v5.0. `40-…`, `42-…` |
| Widevine licence never auto-renews | – | `drm.renewalIntervalSec` is **PlayReady and FairPlay only**. `45-…` |
| No DRM at all in a locally built Chromium | – | *"Only official Chrome builds contain the Widevine CDM."* `75-…` |

## Offline download

| Symptom | Code | Fix |
|---|---|---|
| `store()` resolves to something that is not the content | – | `store()` returns an `IAbortableOperation`. Await `.promise`. `50-…` |
| Downloads return 401 while playback works | – | `Storage` has its **own** networking engine. `40-…`, `50-…` |
| The download is far larger than expected | – | `trackSelectionCallback` defaults to identity and stores everything. `50-…` |
| Download refused near the quota | `STORAGE_LIMIT_REACHED` 9014 | Shaka's default `downloadSizeCallback` caps at **95% of quota**, using a bitrate-derived estimate. `50-…` |
| A downloaded asset vanished | – | Shaka **never calls `navigator.storage.persist()`**, so it is best-effort storage. Eviction semantics: `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`), `references/32-eviction-and-recovery.md`. `50-…` |
| Storage does not open at all | `INDEXED_DB_INIT_TIMED_OUT` 9017, `INDEXED_DB_ERROR` 9001 | `StorageMechanismOpenTimeout` must be set **before** any other offline call. 9001 on Firefox is often a downgraded browser profile. `50-…` |
| An interrupted download cannot be removed | – | `offlineUri` is `null` while `isIncomplete`. **There is no resume API** and targeted deletion is awkward — open question 3. `50-…` |
| Downloaded content will not play without network | – | `usePersistentLicense` was `false`, or the platform does not support persistent licences (Android M62+ and Chromebooks; Chrome v64–v142 on Windows/Mac). `50-…` |
| The same asset downloaded twice | – | *"you'll download the same manifestUri twice"* — **no dedup.** Key downloads yourself. `50-…` |

## Ads

| Symptom | Code | Fix |
|---|---|---|
| `adManager.initClientSide is not a function` | – | Removed in v5.0. The current tutorial still shows it — **conflict C2**. `55-…` |
| Ads never load | `CS_IMA_SDK_MISSING` 10000, `SS_IMA_SDK_MISSING` 10002 | The IMA script tag is missing. `55-…` |
| The ad never starts and content never resumes | – | Fail-open needs a **watchdog with a bound**: no `ad-playing` within `adTimeoutMs` → cancel, report, resume. `55-…` |
| Ad UI does not render in a non-UI build | `CS_AD_CONTAINER_MISSING` 10008, `SS_AD_CONTAINER_MISSING` 10009 | Non-UI builds must create the ad `<div>` and call `setContainers`. `55-…` |

## Lifecycle and leaks

| Symptom | Fix |
|---|---|
| Memory grows after route changes; network activity continues after unmount | Clear timers, remove **every** listener, then `await player.destroy()`, and let `onBeforeUnmount` wait for it. `20-…` |
| Events fire twice | Two Players on one element — usually declarative UI setup (`video['ui']`) plus a manually constructed Player. `65-…` |
| Two callers can destroy the same player | The composable returned two lifecycle handles. Return one frozen object. `10-…` |
| Everything throws `LOAD_INTERRUPTED` (7000) | The Player was used after `destroy()`. It is dead; construct a new one. `20-…` |
| A custom UI element leaks | Since v4.0, `IUIElement` plugins must implement `release()`, not `destroy()`. `65-…` |
| Changing source loses all filters and config | You destroyed and reconstructed the Player. `load()` is the switch. `37-…` |

## Diagnostics workflow

1. Reproduce on a **minimal known-good stream** first; that separates "the player" from "this asset".
2. Load `dist/shaka-player.compiled.debug.js` in a lab page — the debug build retains logging and the
   uncompiled error `message` is `'Shaka Error CATEGORY.CODE_NAME (data)'` rather than a bare number.
3. Capture the emitted event sequence, `downloadfailed` payloads (**type and status, never the URI**)
   and `getStats()` at failure. Choose the evidence mode from `90-qa-modes-and-checklist.md`.
4. Check `05-provenance-and-freshness.md` before carrying forward any workaround: an open issue is a
   symptom, never a fixed behaviour.

**Best practice.** Start from the error **code**, not the message — the compiled build's message is
only `'Shaka Error <code>'`, so a symptom search on message text finds nothing.
**Common mistake.** Reaching for a custom workaround before checking whether the current release
already fixed it. `80-version-migration-and-release-deltas.md` lists the last two minors' fixes, and
5.2.1–5.2.3 alone repaired playhead position after an MSE reload, header isolation across retries, and
MSE append failure on variant switch.
