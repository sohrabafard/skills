For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
