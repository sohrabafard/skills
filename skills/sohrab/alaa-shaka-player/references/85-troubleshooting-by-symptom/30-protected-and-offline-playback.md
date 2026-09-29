Version-sensitive claims in this topic depend on [Shaka provenance and freshness](../05-provenance-and-freshness.md).

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
| A downloaded asset vanished | – | Shaka **never calls `navigator.storage.persist()`**, so it is best-effort storage. Eviction semantics: `/alaa-indexeddb-browser-storage`, `references/32-eviction-and-recovery.md`. `50-…` |
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
