For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
