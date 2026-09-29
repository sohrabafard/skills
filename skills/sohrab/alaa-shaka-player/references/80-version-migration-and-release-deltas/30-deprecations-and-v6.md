For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

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
