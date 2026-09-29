For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
