# Tracks: video, audio and text; language and role selection

All rows `verified` at v5.2.3, read 2026-07-28. **Read the removals first — three names that are still
widely written produce a `TypeError` at 5.2.3.**

## Removed in v5.0 — do not write these

| Name | Status | Replacement | Evidence |
|---|---|---|---|
| `getAudioLanguages()` | **REMOVED in v5.0** | `getAudioTracks()` | `upgrade.md` v5.0: *"`getAudioLanguages` and `getAudioLanguagesAndRoles` have been removed; instead, use the new `getAudioTracks` API (Deprecated in v4.14)"*; `grep -rn "getAudioLanguagesAndRoles" lib/ ui/` → no matches |
| `getAudioLanguagesAndRoles()` | **REMOVED in v5.0** | `getAudioTracks()` | same |
| `selectAudioLanguage()` | **REMOVED in v5.0** | `selectAudioTrack(track, safeMargin)` | same |
| `setTextTrackVisibility()` | **REMOVED in v5.0** | `selectTextTrack()` — selecting now makes a track visible; there is no separate visibility control | `upgrade.md` v5.0 |
| `getTextLanguagesAndRoles()` | Not present | `getTextTracks()` | grep → no matches |
| `getChapters()` | Replaced in v5.0 | `getChaptersAsync(language)` | `upgrade.md` v5.0 |
| `addTextTrack()` (non-async) | Removed in v4.0 | `addTextTrackAsync(...)` | `upgrade.md` v4.0 |
| `shaka.extern.LanguageRole` | Typedef still declared, **referenced nowhere** in `lib/` or `ui/`. Dead type. | – | `externs/shaka/player.js` L3366; grep → no matches |

**Code that calls `player.selectAudioLanguage(...)` against 5.2.3 throws
`TypeError: player.selectAudioLanguage is not a function`.** Optional-chaining it
(`player.selectAudioLanguage?.(...)`) does not fix the bug — it converts a loud failure into a silent
one where audio selection never happens. `scripts/check-shaka-api.mjs` finds both spellings.

## API surface

| Method | Signature |
|---|---|
| `getVariantTracks()` | → `Array<shaka.extern.Track>` |
| `selectVariantTrack(track, clearBuffer = false, safeMargin = 0)` | |
| `getAudioTracks()` | → `Array<shaka.extern.AudioTrack>` |
| `selectAudioTrack(audioTrack, safeMargin = 0)` | *"Select an audio track compatible with the current video track. If the player has not loaded any content, this will be a no-op."* |
| `getVideoTracks()` | → `Array<shaka.extern.VideoTrack>` |
| `selectVideoTrack(videoTrack, clearBuffer = false, safeMargin = 0)` | |
| `getTextTracks()` | → `Array<shaka.extern.TextTrack>` |
| `selectTextTrack(track)` | Selecting also makes visible. |
| `getImageTracks()` / `getAllThumbnails(trackId)` / `getThumbnails(trackId, time)` | Thumbnails. |
| `getChaptersTracks()` / `getChaptersAsync(language)` | Chapters. |
| `addTextTrackAsync(uri, language, kind, mimeType?, codec?, label?, forced?)` | → `Promise<TextTrack>` |
| `addThumbnailsTrack(uri, mimeType)` / `addChaptersTrack(uri, language, mimeType)` | |

## Track shapes

`shaka.extern.Track` (variant) — `id`, `active`, `type`, `bandwidth`, `language`, `label`,
`videoLabel`, `kind`, `width`, `height`, `frameRate`, `pixelAspectRatio`, `hdr`, `colorGamut`,
`videoLayout`, `mimeType`, `audioMimeType`, `videoMimeType`, `codecs`, `audioCodec`, `videoCodec`,
`primary`, `roles`, `audioRoles`, `videoRoles`, **`audioLanguage`, `videoLanguage` (new in 5.2.0)**,
`accessibilityPurpose`, `forced`, `videoId`, `audioId`, `audioGroupId`, `channelsCount`,
`audioSamplingRate`, `tilesLayout`, `audioBandwidth`, `videoBandwidth`, `spatialAudio`,
`originalVideoId`, `originalAudioId`, `originalTextId`, `originalImageId`, `originalLanguage`.

`shaka.extern.AudioTrack` — `active`, `language`, `label`, `mimeType`, `codecs`, `primary`, `roles`,
`accessibilityPurpose`, `channelsCount`, `audioSamplingRate`, `spatialAudio`, `originalLanguage`.
**Note: no `id` field.** Key your menu rows on `language` + `roles[0]` + `label`, not on an id.

`shaka.extern.TextTrack` — `id`, `active`, `type`, `bandwidth`, `language`, `label`, `kind`
(`'caption'` | `'subtitle'`), `mimeType`, `codecs`, `primary`, `roles`, `accessibilityPurpose`,
`forced`, `originalTextId`, `originalLanguage`.

Language normalisation: *"language part is always lowercase and translated to ISO-639-1 when possible,
locale part is always uppercase, i.e. `'en-US'`"*; `'und'` when absent. `originalLanguage` preserves
the raw manifest string — display that if the user must recognise it, match on `language`.

## Roles

`roles` is `Array<string>` (`'main'`, `'caption'`, `'commentary'`, …). Variant tracks additionally
expose `audioRoles` and `videoRoles` separately. Preference by role goes through
`preferredAudio[].role`, `preferredText[].role`, `preferredVideo[].role`. `preferredVariantRole` was
renamed `preferredAudioRole` in v5.0 and then folded into `preferredAudio[].role` (deprecated v5.1,
removed v6.0). `accessibilityPurpose` carries the DASH accessibility descriptor.
5.2.0 UI change: *"Disambiguate video tracks with the same role by language."*

## How selections are remembered — the mechanics most implementations get wrong

| Fact | Evidence |
|---|---|
| `selectVariantTrack()` **back-propagates** the chosen track's language/role/label/channelCount/codec into an in-session `AudioPreference` + `VideoPreference`, calls `currentAdaptationSetCriteria_.configure(...)`, then `updateAbrManagerVariants_()`. An explicit workaround for issue #1299. | `lib/player.js` L6148–6200 |
| `selectTextTrack()` writes `this.currentTextLanguage_ = stream.language`. | L5987–5988 |
| **On every `load()`, `currentTextLanguage_` / `currentTextRole_` / `currentTextForced_` are RESET from `config_.preferredText[0]`.** | L3087–3094 |
| Therefore **selections survive within one loaded asset, not across `load()`.** To persist a user's language choice you must write it into `preferredAudio` / `preferredText` yourself. | `inferred` from the rows above |
| `currentAdaptationSetCriteria_` is carried across a load only when it came from a `PreloadManager`. | L2050–2058 |
| Language and preference config changes take effect **on the next `load()`**, not immediately. | `docs/tutorials/config.md` |

## The v6-ready preference spelling

`shaka.extern.AudioPreference`: `language` (`''`), `role` (`''`), `label` (`''`), `channelCount` (`0`),
`codec` (`''`), `spatialAudio` (`false`).
`shaka.extern.TextPreference`: `language`, `role`, `format`, `forced`.
`shaka.extern.VideoPreference`: `language`, `label`, `role`, `codec`, `hdrLevel`, `layout`.
Defaults: `preferredAudio: []`, `preferredText: []`, `preferredVideo: [{hdrLevel: 'AUTO'}]`.

Semantics (verbatim): *"Entries are tried in order; the first entry that matches available tracks is
used. Within an entry, all specified (non-empty/non-zero) fields must match (AND logic). Unspecified
fields (empty string, 0, or undefined) are ignored (match anything)."*

## Working snippet — selection that actually persists

```js
// Priority-ordered preferences. v6-ready spelling; works from 5.1 on.
player.configure({
  preferredAudio: [
    {language: 'fa', channelCount: 6},   // Persian 5.1 if it exists
    {language: 'fa'},                    // else any Persian
    {language: 'en'},                    // else English
  ],
  preferredText: [
    {language: 'fa'},
    {language: 'en', forced: true},
  ],
});

await player.load(uri);

const audioTracks = player.getAudioTracks();   // shaka.extern.AudioTrack[]  (no `id` field)
const textTracks  = player.getTextTracks();    // shaka.extern.TextTrack[]

// Immediate action. safeMargin keeps 4s of the old audio to avoid a rebuffer.
const commentary = audioTracks.find((t) => t.roles.includes('commentary'));
if (commentary) player.selectAudioTrack(commentary, /* safeMargin= */ 4);

// Selecting a text track makes it visible. There is NO setTextTrackVisibility in v5.
const fa = textTracks.find((t) => t.language === 'fa' && !t.forced);
if (fa) player.selectTextTrack(fa);

// DURABLE state: write the choice back, or the next load() resets it.
function rememberAudio(track) {
  player.configure('preferredAudio', [{
    language: track.language,
    role: track.roles[0] || '',
    label: track.label || '',
    channelCount: track.channelsCount || 0,
    codec: '',
    spatialAudio: track.spatialAudio || false,
  }]);
}

// Re-render menus from these; do not poll.
player.addEventListener('trackschanged',       () => renderMenus());
player.addEventListener('audiotrackschanged',  () => renderAudioMenu());
player.addEventListener('audiotrackchanged',   () => highlightActiveAudio());
player.addEventListener('textchanged',         () => highlightActiveText());
```

Event strings `trackschanged`, `audiotrackschanged`, `audiotrackchanged`, `textchanged` are
`verified` from `lib/util/fake_event.js`.

## Failure modes

`RESTRICTIONS_CANNOT_BE_MET` 4012 (hard restrictions removed every track) · `NO_VARIANTS` 4036 ·
`CANNOT_ADD_EXTERNAL_TEXT_TO_LIVE_STREAM` 4033 · `CANNOT_ADD_EXTERNAL_TEXT_TO_SRC_EQUALS` 2012 ·
`TEXT_ONLY_WEBVTT_SRC_EQUALS` 2013.

**Best practice.** Treat `preferredAudio`/`preferredText` as the durable state and
`selectAudioTrack`/`selectTextTrack` as the immediate action; write **both** when the user picks a
language. Map Shaka's track objects into your own plain rows before they reach Vue reactivity.
**Common mistake.** Expecting `selectTextTrack()` to survive the next `load()`. It will not — `load()`
resets `currentTextLanguage_` from `config.preferredText[0]`, so the user's subtitle choice silently
reverts at the next episode.
