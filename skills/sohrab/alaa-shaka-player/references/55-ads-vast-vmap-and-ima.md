# Ads: VAST, VMAP, IMA, MediaTailor and interstitials

All rows `verified` at v5.2.3, read 2026-07-28. Sections marked 5.3 were read 2026-11-12 at v5.3.4.

## Read this first — an upstream tutorial is stale and an agent will copy it

`docs/tutorials/ad_monetization.md` §"Streaming with Client Side Ads Insertion" **still shows**
`adManager.initClientSide(container, video, adsRenderingSettings);`.

**That line does not work at 5.2.3.** `docs/tutorials/upgrade.md` §v5.0 states: *"Removed
`initClientSide`, `initServerSide`, `initMediaTailor` and `initInterstitial`, since those things are
now auto-initialized when necessary."* `externs/shaka/ads.js` confirms it — no such method exists.
Both documents ship at tag v5.2.3. **This is conflict C2 in `05-provenance-and-freshness.md`; the
externs are authoritative and the tutorial line is a documentation bug. Do not copy it.**

## Current position

Ads are handled by a pluggable manager implementing `shaka.extern.IAdManager`, obtained with
`player.getAdManager()`. **v5.0 removed all the `init*()` methods** and removed the `video` and
`player` parameters from **every** method; `setContainers` was added. Four insertion paths:
**client-side IMA**, **server-side IMA DAI**, **AWS Elemental MediaTailor**, and **interstitials**
(HLS `EXT-X-DATERANGE`, DASH MPD-alternate, or app-supplied custom).

## `shaka.extern.IAdManager` — the full surface

| Group | Methods |
|---|---|
| Lifecycle | `setLocale(locale)`, `setContainers(clientSideAdContainer, serverSideAdContainer)`, `configure(config)`, `release()`, `onAssetUnload()` |
| Client-side IMA | `requestClientSideAds(imaRequest, adsRenderingSettings)`, `updateClientSideAdsRenderingSettings(adsRenderingSettings)` |
| Server-side IMA DAI | `requestServerSideStream(imaRequest, backupUrl?) → Promise<string>`, `replaceServerSideAdTagParameters(adTagParameters)` |
| MediaTailor | `requestMediaTailorStream(url, adsParams, backupUrl?) → Promise<string>`, `addMediaTailorTrackingUrl(url)` |
| Interstitials | `addCustomInterstitial(interstitial)`, `addAdUrlInterstitial(url) → Promise`, `getInterstitialPlayer() → shaka.Player` |
| Utils | `getCuePoints() → Array<AdCuePoint>`, `getStats()`, `onManifestUpdated(isLive)`, `onHlsTimedMetadata(metadata, timestampOffset)`, `onCueMetadataChange(value)`, `onHLSMetadata(metadata)`, `onDASHMetadata(region)`, `getCurrentAd() → ?shaka.extern.IAd` |
| Factory | `shaka.extern.IAdManager.Factory = function(shaka.Player): !shaka.extern.IAdManager` |

`shaka.extern.IAd` (per-ad object): `needsSkipUI()`, `isClientRendering()`, `hasCustomClick()`,
`isUsingAnotherMediaElement()`, `getDuration()`, `getMinSuggestedDuration()`, `getRemainingTime()`,
`getTimeUntilSkippable()`, `isPaused()`, `isSkippable()`, `canSkipNow()`, `skip()`, `play()`,
`pause()`, `getVolume()`, `setVolume(v)`, `isMuted()`, `setMuted(m)`, `isLinear()`,
`resize(w, h)`, `getSequenceLength()`, `getPositionInSequence()`, `getTitle()`, `getDescription()`,
`getVastMediaBitrate()`, `getVastMediaHeight()`, `getVastMediaWidth()`, `getVastAdId()`, `getAdId()`,
`getCreativeAdId()`, `getAdvertiserName()`, `getMediaUrl()`, `getTimeOffset()`, `getPodIndex()`.

## Ad events — exact strings

All constants on `shaka.ads.Utils` (`lib/ads/ad_utils.js`):

| Constant → string | | Constant → string |
|---|---|---|
| `ADS_LOADED` → `ads-loaded` | | `AD_CLICKED` → `ad-clicked` |
| `AD_STARTED` → `ad-started` | | `AD_PROGRESS` → `ad-progress` |
| `AD_PLAYING` → `ad-playing` | | `AD_BUFFERING` → `ad-buffering` |
| `AD_FIRST_QUARTILE` → `ad-first-quartile` | | `AD_IMPRESSION` → `ad-impression` |
| `AD_MIDPOINT` → `ad-midpoint` | | `AD_DURATION_CHANGED` → `ad-duration-changed` |
| `AD_THIRD_QUARTILE` → `ad-third-quartile` | | `AD_CLOSED` → `ad-closed` |
| `AD_COMPLETE` → `ad-complete` | | `AD_LOADED` → `ad-loaded` |
| `AD_STOPPED` → `ad-stopped` | | `ALL_ADS_COMPLETED` → `all-ads-completed` |
| `AD_SKIPPED` → `ad-skipped` | | `AD_LINEAR_CHANGED` → `ad-linear-changed` |
| `AD_VOLUME_CHANGED` → `ad-volume-changed` | | `AD_METADATA` → `ad-metadata` |
| `AD_MUTED` → `ad-muted` | | `AD_RECOVERABLE_ERROR` → `ad-recoverable-error` |
| `AD_PAUSED` → `ad-paused` | | `AD_ERROR` → `ad-error` |
| `AD_RESUMED` → `ad-resumed` | | `AD_BREAK_READY` → `ad-break-ready` |
| `AD_SKIP_STATE_CHANGED` → `ad-skip-state-changed` | | `AD_BREAK_STARTED` → `ad-break-started` |
| `CUEPOINTS_CHANGED` → `ad-cue-points-changed` | | `AD_BREAK_ENDED` → `ad-break-ended` |
| `IMA_AD_MANAGER_LOADED` → `ima-ad-manager-loaded` | | `AD_INTERSTITIAL_PRELOAD` → `ad-interstitial-preload` |
| `IMA_STREAM_MANAGER_LOADED` → `ima-stream-manager-loaded` | | `AD_INTERSTITIAL_PRELOADED` → `ad-interstitial-preloaded` |
| `AD_INTERACTION` → `ad-interaction` | | `AD_CONTENT_PAUSE_REQUESTED` → `ad-content-pause-requested` |
| `AD_CONTENT_RESUME_REQUESTED` → `ad-content-resume-requested` | | `AD_CONTENT_ATTACH_REQUESTED` → `ad-content-attach-requested` |

Every Shaka ad event carries `e['originalEvent']` (the SDK event) and `e['sdkAdObject']` where
available. These are **Shaka's** event strings; the names your telemetry reports come from
`/alaa-services-contract` (`$alaa-services-contract`) and are not these.

## The four insertion paths

| Path | How | Requires |
|---|---|---|
| **VAST / VMAP, no IMA** | `adManager.addAdUrlInterstitial(vastOrVmapUrl)` | Nothing beyond Shaka. Malformed XML → `VAST_INVALID_XML` (10007). |
| **Client-side IMA** | `adManager.requestClientSideAds(new google.ima.AdsRequest(), adsRenderingSettings)` | `<script src="https://imasdk.googleapis.com/js/sdkloader/ima3.js">` — missing → `CS_IMA_SDK_MISSING` (10000). A client-side ad container div — missing → `CS_AD_CONTAINER_MISSING` (10008). |
| **Server-side IMA DAI** | `await adManager.requestServerSideStream(streamRequest, backupUrl)` → a manifest URL to `load()`; `replaceServerSideAdTagParameters(params)` for late params | `ima3_dai.js` — missing → `SS_IMA_SDK_MISSING` (10002). A Google Ad Manager account with streams hosted on GAM. Container missing → `SS_AD_CONTAINER_MISSING` (10009). Overlapping requests → `CURRENT_DAI_REQUEST_NOT_FINISHED` (10004). |
| **MediaTailor (SSAI)** | `await adManager.requestMediaTailorStream(url, adsParams, backupUrl)`; `addMediaTailorTrackingUrl(url)` | A MediaTailor session endpoint. Failure → `MEDIATAILOR_REQUEST_FAILED` (10010). |
| **HLS interstitials** | Automatic from `EXT-X-DATERANGE`. Disable with `ads.disableHLSInterstitial`. | – |
| **DASH interstitials** | Automatic (MPD alternate). Disable with `ads.disableDASHInterstitial`. | – |
| **Custom interstitials** | `adManager.addCustomInterstitial({...})`. Also drivable from SCTE-35 via `timelineregionadded` with `schemeIdUri === 'urn:scte:scte35:2014:xml+bin'`. | – |
| **Overlay interstitials** | Image, video (progressive or manifest), or website overlays. | – |

## SCTE-35 messages (new in 5.3.0)

Read 2026-11-12. Source: CHANGELOG at tag v5.3.4, "unify SCTE-35 handling across DASH, HLS and EMSG"
(#10606), `https://raw.githubusercontent.com/shaka-project/shaka-player/v5.3.4/CHANGELOG.md`. Details
come from `lib/player.js`, `lib/util/scte35.js`, `externs/shaka/scte35.js` and
`dist/shaka-player.ui.d.ts` in the `shaka-player@5.3.4` npm package.

Use this API to read ad-break signals without parsing manifests or `emsg` boxes yourself.
Live content can carry these signals too. `32-live-and-low-latency.md` points here.

| Name | Meaning |
|---|---|
| `player.getAllScte35Events()` | `(): shaka.extern.Scte35Event[]`. The messages kept on the presentation timeline. |
| `scte35added` | Fires as soon as the player finds a message. `detail` is the `Scte35Event`. |
| `scte35enter` | Fires when playback reaches a message. **A seek across a message does not fire it.** |
| `scte35exit` | Fires when playback leaves a message. A message with no duration is entered and left in the same poll. |

`shaka.extern.Scte35Event` fields: `schemeIdUri`, `startTime`, `endTime` (seconds; equals `startTime`
when the transport gives no duration), `id` (the transport id, not the splice or segmentation id
inside the payload), `source` (`'dash'`, `'hls'`, `'emsg'` or `'msf'`), `kind` (`'out'`, `'in'` or
`'cmd'` for HLS; `''` otherwise), `data` (`Uint8Array` with the full `splice_info_section`, or `null`),
`node` (the original XML, or `null`).

Rules:
- The player does not decode the payload. Decode the parts you need from `data` in your own code.
- Treat `data` and `node` as untrusted input from the origin. Validate lengths before you read them.
- Do not use `endTime` as an ad duration without checking `source` and `kind`. HLS `SCTE35-IN`
  applies at the end of the range that carries it.
- `timelineregionadded` still fires for DASH event-stream regions at 5.3.4 (`lib/dash/dash_parser.js`).
  The SCTE-35 row in the insertion table keeps working. New code reads `scte35added` instead.
- Not verified: how `scte35*` events interact with seeking back over a break on live content.

## Other 5.3 changes in this area

Read 2026-11-12, same CHANGELOG. Defaults come from `lib/util/player_configuration.js` in the 5.3.4 package.
The semantics of the first two keys are not read.

| Change | Default | PR |
|---|---|---|
| `ads.interstitialCooldown` added ("cooldown config for interstitial ad") | `0` | #10494 |
| `ads.disableSVTA` added | `false` | #10725 |
| `shaka.ads.SvtaAd` and `shaka.extern.AdTrackingInfo` removed. `AdInterstitial.uri` is `string \| null`. | n/a (typedef diff 5.2.13 to 5.3.4) | not mapped |
| Runtime skip ranges, released together with "MediaTailor played-ad-break skipping". The MediaTailor part was not read. For the API, see `30-playback-speed-seek-trickplay.md`, "Skip ranges". | n/a | #10338 |

`AdInterstitial` fields: `id`, `groupId`, `startTime`, `endTime`, `uri`, `mimeType`, `isSkippable`,
`skipOffset`, `skipFor`, `canJump`, `resumeOffset`, `playoutLimit`, `once`, `pre`, `post`,
`timelineRange`, `loop`, `overlay`, `displayOnBackground`, `currentVideo`, `background`,
`clickThroughUrl`, `resolutionTimeOffset`, and `tracking` (`shaka.extern.AdTrackingEvent`:
`impression`, `clickTracking`, `start`, `firstQuartile`, `midpoint`, `thirdQuartile`, `complete`,
`skip`, `error`, `resume`, `pause`, `mute`, `unmute` — each an `Array<string>` of beacon URLs).

## `ads.*` configuration

| Key | Default |
|---|---|
| `ads.customPlayheadTracker` | `false`; **`true` on Tizen, WebOS, Chromecast, Hisense, PS4, PS5, Xbox, Vizio** |
| `ads.skipPlayDetection` | `false`; **`true` on the same TV/console set** |
| `ads.supportsMultipleMediaElements` | `true`; **`false` on the same TV/console set** |
| `ads.disableHLSInterstitial` / `ads.disableDASHInterstitial` | `false` / `false` |
| `ads.allowPreloadOnDomElements` | `true` |
| `ads.allowStartInMiddleOfInterstitial` | `true` |
| `ads.disableTrackingEvents` | `false` (*"except when using IMA SDK"*) |
| `ads.disableSnapback` | `false` — normally, seeking past an unplayed break rewinds to it |
| `ads.interstitialPreloadAheadTime` | `10` s |
| `ads.disablePlayedLinearAdSkip` | `false` — **MediaTailor only** |
| `ads.disableTrackingForPlayedLinearAds` | `false` — MediaTailor only; meaningful only with the previous flag |

## What a skin must do

| Requirement | Note |
|---|---|
| Provide **two** containers and pass them via `adManager.setContainers(cs, ss)`. **With the Shaka UI this is automatic** — the tutorial repeats *"Note: If you are using Shaka UI this call is not necessary."* | Non-UI builds: *"you will also need to create a `<div>` over your video element to serve as an ad container."* |
| With the UI, get them from `controls.getClientSideAdContainer()` / `getServerSideAdContainer()`. | |
| Show/hide ad chrome with `controls.showAdUI()` / `controls.hideAdUI()`. | |
| Query state with `controls.getAd()` and `controls.getAdCuePoints()`. | |
| Draw break markers via UI config `seekBarColors.adBreaks`. | |
| Skip button: drive from `IAd.needsSkipUI()`, `isSkippable()`, `canSkipNow()`, `getTimeUntilSkippable()`, `skip()`. `ui/skip_ad_button.js` exists. | |
| Ad statistics panel: overflow/context-menu button `ad_statistics`, filtered by UI config `adStatisticsList`. `shaka.extern.AdsStats`: `loadTimes`, `averageLoadTime`, `started`, `overlayAds`, `playedCompletely`, `skipped`, `errors`. | |

## Fail-open is mandatory, and it needs a number

An ad path that fails must never hold content hostage. State the bound: **if no `ad-playing` event
arrives within `adTimeoutMs` of the ad request, cancel the ad, emit the ad-failure telemetry quantity,
and resume content.** `adTimeoutMs` is validated to the range 2000–30000 at construction; its value
comes from `/alaa-reliability-sla` (`$alaa-reliability-sla`), `references/50-degradation.md`. "Do not
leave the session stuck" is not a checkable condition; a watchdog with a bound is.

## Working snippet

```js
const adManager = player.getAdManager();

// Non-UI build only: you own the containers. With the Shaka UI this is automatic.
// adManager.setContainers(myCsDiv, mySsDiv);

adManager.configure({
  disableHLSInterstitial: false,
  disableDASHInterstitial: false,
  interstitialPreloadAheadTime: 10,
  disableSnapback: false,
});
// Equivalently: player.configure('ads.interstitialPreloadAheadTime', 10);

// ---- A. Plain VAST/VMAP. No IMA SDK required. ----
await adManager.addAdUrlInterstitial('https://ads.example.com/vmap.xml');

// ---- B. Client-side IMA (requires ima3.js on the page).
//         NOT initClientSide - that was removed in v5.0. See conflict C2. ----
const req = new google.ima.AdsRequest();
req.adTagUrl = 'https://pubads.g.doubleclick.net/gampad/ads?...&output=vast';
adManager.requestClientSideAds(req, /* adsRenderingSettings= */ null);

// ---- C. Server-side IMA DAI (requires ima3_dai.js) ----
const streamRequest = new google.ima.dai.api.VODStreamRequest();
streamRequest.contentSourceId = 'CONTENT_SOURCE_ID';
streamRequest.videoId = 'VIDEO_ID';
const manifestUrl = await adManager.requestServerSideStream(
    streamRequest, /* backupUrl= */ 'https://cdn.example.com/clean.m3u8');
await player.load(manifestUrl);

// ---- D. MediaTailor SSAI ----
const mtUrl = await adManager.requestMediaTailorStream(
    'https://mediatailor.example.com/v1/session/.../asset',
    {adsParams: {sectionId: 'homepage'}},
    'https://cdn.example.com/clean.m3u8');
await player.load(mtUrl);

// ---- E. MANDATORY fail-open watchdog. Bound from /alaa-reliability-sla. ----
const AD_TIMEOUT_MS = 12000;                       // validated range 2000..30000
function requestAdWithWatchdog(request) {
  let settled = false;
  const U = shaka.ads.Utils;
  const clear = () => { settled = true; clearTimeout(timer); off(); };
  const onPlaying = () => clear();
  const onError   = () => { clear(); resumeContent(); };

  adManager.addEventListener(U.AD_PLAYING, onPlaying);
  adManager.addEventListener(U.AD_ERROR, onError);
  const off = () => {
    adManager.removeEventListener(U.AD_PLAYING, onPlaying);
    adManager.removeEventListener(U.AD_ERROR, onError);
  };

  const timer = setTimeout(() => {
    if (settled) return;
    clear();
    reportAdFailure({ reason: 'timeout', timeoutMs: AD_TIMEOUT_MS });
    resumeContent();                               // content ALWAYS resumes
  }, AD_TIMEOUT_MS);

  adManager.requestClientSideAds(request, null);
}

// ---- F. Skin state, driven only by Shaka's unified ad events ----
const U = shaka.ads.Utils;
adManager.addEventListener(U.AD_STARTED, () => {
  const ad = adManager.getCurrentAd();
  controls.showAdUI();
  if (ad.needsSkipUI()) renderSkipButton(ad);
});
adManager.addEventListener(U.AD_SKIP_STATE_CHANGED, () => updateSkipButton());
adManager.addEventListener(U.AD_STOPPED,            () => controls.hideAdUI());
adManager.addEventListener(U.ALL_ADS_COMPLETED,     () => controls.hideAdUI());
adManager.addEventListener(U.CUEPOINTS_CHANGED,     () => drawMarkers(adManager.getCuePoints()));

// ---- G. Reach the raw IMA objects for SDK features Shaka does not expose ----
adManager.addEventListener(U.IMA_AD_MANAGER_LOADED,     (e) => { imaAdManager = e['imaAdManager']; });
adManager.addEventListener(U.IMA_STREAM_MANAGER_LOADED, (e) => { imaStreamMgr = e['imaStreamManager']; });

// ---- H. Replace the ad manager entirely. BEFORE constructing the Player. ----
// shaka.Player.setAdManagerFactory(() => new MyAdManager());
```

Ad error codes: `CS_IMA_SDK_MISSING` 10000 · `SS_IMA_SDK_MISSING` 10002 ·
`CURRENT_DAI_REQUEST_NOT_FINISHED` 10004 · `VAST_INVALID_XML` 10007 · `CS_AD_CONTAINER_MISSING` 10008 ·
`SS_AD_CONTAINER_MISSING` 10009 · `MEDIATAILOR_REQUEST_FAILED` 10010. Category `ADS` (10) fails
independently of content — that is the property the watchdog exists to preserve.

**Best practice.** Drive skin state exclusively from `shaka.ads.Utils` events plus
`adManager.getCurrentAd()`. That keeps one code path across IMA CS, IMA DAI, MediaTailor and
interstitials, which is the entire point of Shaka's unified ad events.
**Common mistake.** Copying `adManager.initClientSide(container, video, adsRenderingSettings)` out of
the current tutorial. It was removed in v5.0 and calling it throws (conflict C2).
