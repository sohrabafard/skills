# Version migration and release deltas

Sources for everything below: `.../blob/v5.2.3/CHANGELOG.md` and
`.../blob/v5.2.3/docs/tutorials/upgrade.md`, both `verified`, read 2026-07-28.
Release dates: **5.2.3** 2026-07-27 · **5.2.2** 2026-07-20 · **5.2.1** 2026-07-14 ·
**5.2.0** 2026-07-10 · **5.1.0** 2026-04-15 · **5.0.0** 2026-02-06.

## Which migrations are real

Shaka has followed semantic versioning since v3.0: *"Upgrading from any v3 release to a newer v3
release should be backward compatible. The same is true of all major version numbers."*

| Transition | Real migration? |
|---|---|
| `5.0.x → 5.1.x`, `5.1.x → 5.2.x` | **No.** Minor bumps, backward compatible by policy. `upgrade.md` has no `## v5.2` section because no breaking change was made. |
| **`v4.16 LTS → v5.x`** | **Yes.** A large `## v5.0` section exists. This is §"v4 → v5" below. v4.16 is LTS until **2027-01-31**. |
| **`v5.x → v6.0`** | **Yes, and already announced.** Deprecated in v5.1, removed in v6.0. Write the v6 spelling today. |

## v4 → v5: the breaking changes most likely to bite

**Config renames and removals**

- `streaming.forceTransmuxTS` → `streaming.forceTransmux` (now also AAC, MP3, AC-3, EC-3)
- `manifest.dash.manifestPreprocessor` → `manifest.dash.manifestPreprocessorTXml`, now receiving
  `shaka.externs.xml.Node`; `getAttribute()` / `textContent` results *"must now be decoded if they
  might contain escape sequences"* — use `shaka.util.StringUtils.htmlUnescape`
- **`streaming.useNativeHlsOnSafari` removed** → `streaming.useNativeHlsForFairPlay` or
  `streaming.preferNativeHls` (`22-streaming-formats-and-native-hls.md`)
- `mediaSource.sourceBufferExtraFeatures` → `mediaSource.addExtraFeaturesToSourceBuffer` callback
- `streaming.liveSyncMinLatency` / `liveSyncMaxLatency` removed → `streaming.liveSync.targetLatency`
- All flat `streaming.liveSync*` options removed → the `streaming.liveSync` **object**
- `useSafariBehaviorForLive`, `parsePrftBox`, `autoShowText`, `removeLatencyFromFirstPacketTime` removed
- **`videoRobustness` / `audioRobustness` are now arrays of strings only** (`45-drm.md`)
- `streaming.forceHTTP` → `networking.forceHTTP`; `streaming.forceHTTPS` → `networking.forceHTTPS`;
  `streaming.minBytesForProgressEvents` → `networking.minBytesForProgressEvents`
- `manifest.dash.enableAudioGroups` → `manifest.enableAudioGroups`
- `preferredVariantRole` → `preferredAudioRole` (then folded into `preferredAudio[].role`)
- `streaming.speechToText` → `accessibility.speechToText`

**UI config**

- `doubleClickForFullscreen` now defaults **true on mobile**
- `preferDocumentPictureInPicture` → `documentPictureInPicture.enabled`
- `customContextMenu` now defaults **true on desktop**
- `addBigPlayButton` removed → `bigButtons`
- `airplay` button removed → `remote`

**Player API**

- Constructor no longer takes `mediaElement` *(conflict C3 — the code still accepts it with a warning)*
- `TimelineRegionInfo.eventElement` → `eventNode` (`shaka.externs.xml.Node`)
- **`getAudioLanguages`, `getAudioLanguagesAndRoles`, `selectAudioLanguage` removed** →
  `getAudioTracks` / `selectAudioTrack`
- `shaka.util.FairPlayUtils` → `shaka.drm.FairPlay`
- `getChapters` → `getChaptersAsync`
- **`setTextTrackVisibility` removed**; selecting a text track makes it visible
- **"Apps must call `updateStartTime` instead of setting the media element's `currentTime` directly
  during startup."**

**Plugins** — `TextDisplayer` plugins must implement `configure()`; `enableTextDisplayer` removed;
built-in displayer constructors take a `shaka.Player` as their only parameter; `SimpleTextDisplayer`
replaced by `NativeTextDisplayer`; `TextParser` plugins must implement `setManifestType()`;
`Transmuxer.transmux()` gained three new parameters.

**Ad manager** — `setContainers` added; `video`/`player` params removed from **all** methods;
`initClientSide`, `initServerSide`, `initMediaTailor`, `initInterstitial`, `onDashTimedMetadata`
removed (`55-ads-vast-vmap-and-ima.md`, conflict C2).

**Other removals** — **MSS discontinued**; legacy subtitle formats **LRC, SBV, SSA** removed.

**Initial track selection** — with `autoShowText` gone, the initial text track is chosen *exclusively*
from `preferredTextLanguage`/`preferredTextRole` (now `preferredText`). *"The app may choose not to
pass preferences and instead rely on the tracks API… along with its own business logic."*

## Deprecated right now in 5.x

| Deprecated | Mechanism | Removal |
|---|---|---|
| `new shaka.Player(mediaElement)` | `shaka.log.alwaysWarn('Please migrate from initializing Player with a mediaElement; use the attach method instead.')` (L1138) | not announced |
| `preferredAudioLanguage`, `preferredAudioRole`, `preferredAudioLabel`, `preferredAudioChannelCount`, `preferSpatialAudio`, `preferredAudioCodecs` | `Player.convertLegacyPreferences_()` warns and converts (L9467–9520) | **v6.0** |
| `preferredTextLanguage`, `preferredTextRole`, `preferForcedSubs`, `preferredTextFormats` | same → `preferredText` (L9520–9560) | **v6.0** |
| `preferredVideoLabel`, `preferredVideoRole`, `preferredVideoHdrLevel`, `preferredVideoLayout`, `preferredVideoCodecs` | same → `preferredVideo` | **v6.0** |

**The asymmetry that matters for a TypeScript codebase:** these legacy keys still *work* at runtime
via the shim, but they are **absent from the `shaka.extern.PlayerConfiguration` typedef**, so on the
shipped `.d.ts` they are already type errors. A TS repository cannot use them even today.

## v6.0 — write this spelling now

```js
// Old (deprecated, still works with a warning):
player.configure('preferredAudioLanguage', 'ko');
player.configure('preferredAudioChannelCount', 6);

// New:
player.configure('preferredAudio', [
  {language: 'ko', channelCount: 6},
  {language: 'ko'},
  {language: 'en'},
]);
```

`preferForcedSubs` becomes the `forced` field:
`player.configure('preferredText', [{language: 'en', forced: true}])`.

## 5.2.0 — what is new

**Core:** metadata extraction for `src=` playback · a `requestVideoFrameCallback` polyfill ·
ID3v1 and ID3v2.3 support · **`throwOnPreloadNotSupported` flag on `preload()`** ·
**`timeToFirstFrame` in stats** · **`audioLanguage` and `videoLanguage` exposed on tracks** ·
`mediaTimestamp` on `segmentappended` · repair of broken I-frame-only MP4 segments ·
`goog.Uri` replaced with the native `URL` API · **transmux in a worker** ·
ClearKey playback in Safari through WebCrypto.

**DASH:** `urn:mpeg:dash:event:callback:2015` beacons on region enter · Linked Periods via
`ImportedMPD` (DASH 6th ed.) · Essential/SupplementalProperty at MPD and Period level ·
`RequestParam` (`urlparam:2025`) and `urlparam:2016` URL parameters.

**HLS:** encrypted MSE playback with legacy Apple MediaKeys · **`sequenceMode` disabled by default** ·
`timelineregionadded` for `EXT-X-DATERANGE` tags · accurate playhead date across `PROGRAM-DATE-TIME`
discontinuities · `EXT-X-STREAM-INF` with both AUDIO and VIDEO attributes.

**Ads:** replaying already-played linear ads in MediaTailor · deferred HLS interstitial asset-list
resolution. **Net/CMCD:** vendored `@svta/cml-cmcd`; MIME mappings for CMAF and Opus.
**MSF:** accessibility parsing in the catalog (CEA-608/708), `catalogPreprocessor`, LoC support,
bandwidth estimate for ABR. **CEA:** paint-on and roll-up captions revealed character by character.
**Queue:** M3U playlist loading. **Cast:** `setContentAlbumName`; dynamic event proxying.

**UI (large batch):** always-visible skip buttons for the big-button layout · fisheye VR projection ·
live subtitle style preview on hover · **modern CSS theme support using CSS custom properties** ·
**new `play_pause_buffering` button** · **`QueueButton`** · wheel support and `setStep` on
`RangeElement` · custom `format`/`imageQuality` in `takeScreenshot` and `copyVideoFrameToClipboard` ·
consolidated skip / trick-play / statistics base classes · video tracks disambiguated by language ·
accessibility improvements · ID3 TPE1/TALB → MediaSession · modernised statistics panel ·
redesigned Document PiP placeholder · smaller SVG icon paths · "Generated"/"Translated" labels for
HLS `public.machine-generated` tracks · `customTrackLabel` · Document PiP for audio-only ·
embedded APIC artwork in MediaSession · repeat modes in the loop button with `QueueManager` ·
**`UITextDisplayer.suspendRenderingWhenHidden`** · playback-rate menu with slider and preset pills ·
**UI language used to display language names**.

**5.2.0 has no BREAKING CHANGES section** (`verified` — `grep -n "BREAKING"` over the 5.2.0 block
returned nothing).

## 5.2.x patch releases

**5.2.3** (2026-07-27) — single fix: *"Reset media source before switching variant on MSE append
failure (#10380)."*

**5.2.2** (2026-07-20) — *"Fix duplicate error code 4058 (#10372)"* · MSF draft-16 negotiation and
empty-catalog skipping · MSF bandwidth per group · **"net: isolate headers across retry attempts
(#10361)"** · *"Prevent `screen.orientation` methods from being garbage collected on Safari
(#10364)"* · a shaka-bot glob-expansion security fix · transmux falls back to the main thread when
the worker fails · UI context-menu and rate-slider touch fixes on mobile.

**5.2.1** (2026-07-14) — *"Restore correct playhead position after MediaSource reload (#10335)"* ·
transmux worker device registration · transmux main-thread fallback on worker timeout · thumbnail
preview scaling · rate menu clipping on narrow screens · **"UI: Scope form element font inheritance
to the player container (#10353)"**.

## 5.1.0 — what changed

**New:** ABR informed whether the stream is low latency · **dropped-frame monitoring influencing ABR
decisions** (the origin of `abr.droppedFrames` and `abr.advanced.droppedFrames*`) · basic TiVo OS and
Titan OS support, with HDR and screen-size detection on Titan OS · `clampAppendWindowToDuration` ·
**`subtitleDelay`** · `net.commonAccessTokenHeaderName` · `emsgregions` / `timelineregions` as public
functions · **`requestType` and `context` on download events** · DASH JSON format · automatic XLink
processing · HLS `CAN-SKIP-DATERANGES` and chapter images · `_HLS_start_offset` for `X-ASSET-LIST` in
HLS interstitials · `ad-interstitial-preloaded` · **`ad-playing`** · `startedAt` on
`ad-break-started` · raw CEA-608 packet extraction · MSF `authorizationToken`, CMSF contentProtection,
FETCH catalog, MoQT draft-16, configurable subscribe filter · queue item metadata · `fastSeek` for
MediaSession `seekTo` · `mediaSession.allowAutoPiP` · **`TrackLabelFormat.LABEL_OR_LANGUAGE` and
`LANGUAGE_OR_LABEL`** · `showMenusOnTheRight` · `showUIOnPaused` · chapter images in MediaSession ·
volume adjustment via mouse wheel · modernised watermark.

**Removed / narrowed:** `com.widevine.alpha.experiment` from `probeSupport` · testing of MSS support ·
MSF minimum segment availability duration · redundant base64/XML conversions in PlayReady.

**Deprecated:** the whole individual-preference config family, for removal in v6.0.

## Upgrade procedure

1. Read `05-provenance-and-freshness.md` and confirm the current release.
2. Run `scripts/check-shaka-api.mjs --repo <path>` — it reports every call site using an API removed
   or deprecated between the installed version and current.
3. Fix each finding against the section above. **An optional-chained call to a removed method is still
   a finding** — it converts a loud failure into a silent one.
4. Change the pin to an exact version and record the release URL and date in
   `05-provenance-and-freshness.md`.
5. Re-run the QA matrix in `90-qa-modes-and-checklist.md`, with iOS Safari as its own row.

**Best practice.** Pin an exact version. Three vendor endpoints disagreed about "latest" on
2026-07-28 (conflict C1), so `npm i shaka-player@latest` may not give you what the release page shows.
**Common mistake.** Treating `5.0.x → 5.1.x` as a breaking migration and writing shims for it. There
is nothing to shim; the cliffs are v4 → v5 and the announced v5 → v6.
