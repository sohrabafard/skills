For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## 5.3.0 — what a 5.2.13 user does not have

Sources, `verified`, read 2026-11-12: release tag page `https://github.com/shaka-project/shaka-player/releases/tag/v5.3.0`;
`CHANGELOG.md` at tags `v5.3.4` and `v5.2.17` (`https://github.com/shaka-project/shaka-player/blob/v5.3.4/CHANGELOG.md`);
and the published npm tarballs `shaka-player@5.2.13` and `@5.3.4` (`lib/util/player_configuration.js`,
`ui/ui.js`, `lib/player.js`, `externs/shaka/player.js`, `dist/shaka-player.ui.d.ts`).

The 5.3.0 CHANGELOG section compares against `v5.2.0`, not `v5.2.13`. It repeats fixes that 5.2.1 to 5.2.13
already contain. Never copy a 5.3.0 line into a 5.2.13 upgrade note without the 5.2.x check. `v5.2.17` is the
reference for what 5.2.13 already has.

No release note declares a breaking change. The three 5.3 deprecations are in
[Deprecations and v6 spellings](./30-deprecations-and-v6.md).

This file lists each 5.3.0 change by key, version and PR. It states no default or behaviour. Each row names the
file that owns the rule. When a row applies to your change, read the file it names.

### Changed defaults and behaviour (act on these first)

| Key / behaviour | Since | PR | When it applies, read |
|---|---|---|---|
| `streaming.useNativeHlsForFairPlay` default | 5.3.0 | #10699 | You load HLS on WebKit with FairPlay: `15-configure-surface-and-safe-defaults.md`, "Keys added or changed in 5.3" |
| `streaming.fallbackToNativeHlsOnMseError` (new) | 5.3.0 | #10699 | You serve HLS to Apple browsers: `15-configure-surface-and-safe-defaults.md`, "Keys added or changed in 5.3" |
| `abr.allowAudioFallback` (new) | 5.3.0 | #10689 | You build an audio menu or an ABR policy: `24-adaptive-bitrate-and-restrictions.md`, "Audio fallback (5.3)" |
| `getAudioTracks()` contract and `audiotrackschanged` | 5.3.0 | #10689 | You build an audio track menu: `26-tracks-audio-video-text.md`, "Audio track contract (5.3)" |
| `queue.autoPlayNext` (new) | 5.3.0 | #10503 | You use the queue manager: `15-configure-surface-and-safe-defaults.md`, "Keys added or changed in 5.3" |
| `cmcd.applyParametersFromManifest`, `cmcd.includeInRequests` (new) | 5.3.0 | #10590 | You enable CMCD: `15-configure-surface-and-safe-defaults.md`, "Keys added or changed in 5.3" |
| `drm.keepDrmEngineOnDetach` (new) | 5.3.0 | #10530 | You detach or unload the player on a DRM asset: `15-configure-surface-and-safe-defaults.md`, "Keys added or changed in 5.3" |

Source for the rows above: CHANGELOG lines named by the PR numbers, `CHANGELOG.md` at tag `v5.3.4`, read 2026-11-12.
Defaults and semantics come from `lib/util/player_configuration.js` and `lib/player.js` in the `shaka-player@5.3.4`
npm tarball, read 2026-11-12, and are stated only in the owning files.

### New configuration keys

| Key | Since | PR | When it applies, read |
|---|---|---|---|
| `mediaSource.modifyPreselectionSegmentCallback` | 5.3.0 | #10344 | You play DASH Preselections. No capability file owns this key; no consumer action otherwise. |
| `ads.disableSVTA`, `ads.interstitialCooldown` | 5.3.0 | #10725, #10494 | You configure ads or interstitials: `55-ads-vast-vmap-and-ima.md`, "`ads.*` configuration" |
| `textDisplayer.fontFamily`, `fontColor`, `fontOpacity`, `backgroundColor`, `backgroundOpacity`, `characterEdgeStyle` | 5.3.0 (`fontFamily` accepts any CSS family from 5.3.1) | #10697, #10756 | You style captions: `28-subtitles-and-text-displayer.md`, "`textDisplayer.*` and related configuration" |
| UI `playbackRateSliderStep`, `seekButtonDistance`, `captionsStyleElements` | 5.3.0 | #10516, #10662, #10681, #10692, #10711 | You configure the UI: `65-ui-library-skin-and-localisation.md`, "UI changes in 5.3" |
| `AdvancedRequestType` gains `XLINK` and `LINKED_MPD` | 5.3.0 | #10596 | You write a request filter: `40-networking-engine-and-filters.md`, "`RequestType` and `AdvancedRequestType`" |

### New Player methods and events

| API | Since | PR | When it applies, read |
|---|---|---|---|
| `addSkipRange`, `removeSkipRange`, `clearSkipRanges`, `getSkipRanges` | 5.3.0 (behaviour aligned in 5.3.2) | #10338, #10753 | You skip intro or recap ranges: `30-playback-speed-seek-trickplay.md`, "Skip ranges" |
| `getAllScte35Events`, events `scte35added`, `scte35enter`, `scte35exit` | 5.3.0 | #10606 | You react to SCTE-35 messages: `55-ads-vast-vmap-and-ima.md`, "SCTE-35 messages" |

### New UI classes

`shaka.ui.MenuGroup` (with interface `shaka.extern.IUIMenuGroup`), `CaptionsSettingsGroup`, `TextStyleGroup`,
`TextStyleResetButton`, `SeekButton`, `AutoPlayNextButton`, and the subtitle style menus `TextFontFamily`,
`TextFontColor`, `TextFontOpacity`, `TextBackgroundColor`, `TextBackgroundOpacity`, `TextCharacterEdgeStyle`
(`dist/shaka-player.ui.d.ts` in the 5.3.4 tarball; the 5.2.13 `.d.ts` lacks them, read 2026-11-12). Source: PRs
#10662, #10681, #10692, #10711. `TextSize` and `TextPosition` already exist in 5.2.13 and are not new. New
locales: Azerbaijani and Breton (#10557, #10655). When you build a UI menu, read
`65-ui-library-skin-and-localisation.md`, "UI changes in 5.3".

### Removed

| Removed | Scope | PR / source |
|---|---|---|
| Error codes `DASH_INVALID_JSON` (4061), `MSF_NO_CATALOG` (4062) | marked `RETIRED` in `lib/util/error.js` | tarball diff; the PR for 4062 was not read; removal release: see the code catalog |
| DASH JSON format | experimental build only | #10705 |
| MoQT draft-14 and draft-16 | experimental build only | #10706 |
| `shaka.ads.SvtaAd` and its manager; type `AdTrackingInfo` | replaced by `svta_interstitial_parser.js` and `svta_interstitial_tracker.js` | #10725, tarball file list |
| `manifest.msf.subscribeFilterType`, `manifest.msf.useFetchCatalog`, `MsfFilterType` | deprecated for v6 and absent from the 5.3.4 typedefs; see the deprecations file | typedef diff; #10718 removes `subscribeFilterType`, the PR for `useFetchCatalog` was not read |

New error codes 4065-4071 (MSF, MKV): see `70-error-taxonomy-and-codes/20-complete-code-catalog.md`, "Changes in 5.3".

`inferred` from experimental-only scope: a client that uses the standard UI bundle without MSF, MKV or SVTA is not
affected by the removals. The UI bundle grew about 12% raw and 10% gzip; see
`12-bundling-and-vite-loading.md`, "Bundle size and CSP, 5.2.13 to 5.3.4".

### Other 5.3.0 additions (no consumer action)

DASH Preselections (#10344), DASH `subtitle` role and kind (#10441), TTML IMSC conformance (#10729), SSA
and Matroska text parsers (MKV is experimental-build only, #10667), AV1 in the TS transmuxer (#10603) and in CEA
extraction (#10509), IAMF for CMAF/MP4 (#10586), HLS AES key preload hints (#10715), `load(startTime)` and
`preload(startTime)` documentation rewritten (documentation only; behaviour change not proved), and a large
MSF/MoQT batch (`MsfVersion` gains DRAFT_18, 20, 21 and 22). The README lists the third-party plugin
`@hevcjs/shaka-plugin` (5.3.4 README); before you adopt any plugin, read `75-platform-and-browser-matrix.md`,
"Changes at 5.3.4".
