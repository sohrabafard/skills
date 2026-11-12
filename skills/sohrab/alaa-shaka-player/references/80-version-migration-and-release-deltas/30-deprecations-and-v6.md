For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Deprecated right now in 5.x

| Deprecated | Mechanism | Removal |
|---|---|---|
| `new shaka.Player(mediaElement)` | `shaka.log.alwaysWarn('Please migrate from initializing Player with a mediaElement; use the attach method instead.')` (L1138) | not announced |
| `preferredAudioLanguage`, `preferredAudioRole`, `preferredAudioLabel`, `preferredAudioChannelCount`, `preferSpatialAudio`, `preferredAudioCodecs` | `Player.convertLegacyPreferences_()` warns and converts (L9467–9520) | **v6.0** |
| `preferredTextLanguage`, `preferredTextRole`, `preferForcedSubs`, `preferredTextFormats` | same → `preferredText` (L9520–9560) | **v6.0** |
| `preferredVideoLabel`, `preferredVideoRole`, `preferredVideoHdrLevel`, `preferredVideoLayout`, `preferredVideoCodecs` | same → `preferredVideo` | **v6.0** |
| `ui.showMenusOnTheRight` (UI config) | `ui/ui.js` calls `shaka.Deprecate.deprecateFeature(6, ...)`, warns, then deletes the key. Menus now open next to the button that opens them. | **v6.0** (new in 5.3.0, #10708) |
| `manifest.msf.useFetchCatalog`, `manifest.msf.subscribeFilterType` (experimental MSF build) | deprecated for v6 in 5.3 and absent from the 5.3.4 typedefs | **v6.0** (new in 5.3.0) |

Sources, `verified`, read 2026-11-12: `ui/ui.js` and the `dist/shaka-player.ui.d.ts` typedef diff of the
`shaka-player@5.2.13` and `@5.3.4` tarballs; release tag page
`https://github.com/shaka-project/shaka-player/releases/tag/v5.3.0`. The three 5.3 keys are also absent from
the 5.3.4 typedefs. Setting `ui.showMenusOnTheRight` is a TypeScript error on the 5.3.4 typedefs (5.3.0 typedefs
not read; the key was deprecated in 5.3.0, #10708). At runtime it only logs a deprecation warning and is deleted,
so it has no effect. `docs/tutorials/upgrade.md` is byte-identical at `v5.2.13` and `v5.3.4`: its v6.0 section
still covers only the preference arrays. Other 5.2.13 deprecations are unchanged in 5.3.4:
`manifest.dash.disableXlinkProcessing`, `textDisplayer.captionsUpdatePeriod`, `SkipNextButton` and
`SkipPreviousButton` (use `SkipQueueButton`), `RewindButton` and `FastForwardButton` (use
`TrickPlayButton`), `Controls.setLastTouchEventTime`.

**The asymmetry that matters for a TypeScript codebase:** the legacy `preferred*` keys still *work* at runtime
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
