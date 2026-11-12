# Subtitles, captions and the TextDisplayer

All rows `verified` at v5.2.3, read 2026-07-28, unless a row names a later version.
Rows marked 5.3.x are `verified` at v5.3.4 against the npm tarball and the CHANGELOG at that tag
(`https://github.com/shaka-project/shaka-player/blob/v5.3.4/CHANGELOG.md`), read 2026-11-12.

## Current position

Two built-in displayers. `shaka.text.NativeTextDisplayer` uses the browser's cue renderer via `<track>`
elements and is the default **without** the Shaka UI. `shaka.text.UITextDisplayer` renders into a DOM
container and is the default **with** the UI. `SimpleTextDisplayer` was replaced by
`NativeTextDisplayer` in v5.0. Three legacy formats (**LRC, SBV, SSA**) were removed in v5.0; SRT
survived, UTF-8 only.

5.3.x: `lib/text/native_text_displayer.js` and `lib/text/text_engine.js` are byte-identical in 5.2.13
and 5.3.4 (tarball diff, read 2026-11-12). The text-selection code in `lib/player.js`
(`selectTextTrack`, `getLoadMode`, the `textchanged` dispatcher) has no changed hunk. Do not expect an
upgrade to change native-cue behaviour.

## Supported formats

Registered parsers, from the `shaka.text.TextEngine.registerParser(...)` call sites in `lib/text/`:

| MIME type | Parser |
|---|---|
| `text/vtt`, `text/vtt; codecs="vtt"`, `text/vtt; codecs="wvtt"` | `vtt_text_parser.js` |
| `application/mp4; codecs="wvtt"` | `mp4_vtt_parser.js` |
| `application/ttml+xml` | `ttml_text_parser.js` |
| `application/mp4; codecs="stpp"` and the 9 `stpp.ttml.*` / `stpp.TTML.im1t` variants | `mp4_ttml_parser.js` |
| `text/srt` | `srt_text_parser.js` |
| `text/x-ssa` (**experimental build only**. The parser is missing from the 5.2.13 tarball and present in the 5.3.4 tarball, but registered only in `dist/shaka-player.experimental*.js`. It is not in the UI, compiled, dash or hls bundles, and no CHANGELOG entry names it, so "5.3.0" is `inferred` from the tarball diff. v5.0 had removed SSA from the standard build) | `ssa_text_parser.js` |

5.3.0 also adds `lib/text/matroska_text_parser.js` (registered as `text/x-matroska; codecs="..."` for the
SRT and ASS Matroska codecs, experimental bundles only; `matroska_text_parser.js` L262-265 in the 5.3.4
tarball, read 2026-11-12). It is not registered in the standard UI bundle. Upstream PR for the experimental
scope: `https://github.com/shaka-project/shaka-player/pull/10667`, read 2026-11-12.

CEA-608 and CEA-708 are supported embedded in MP4 and TS. 5.2.0 added *"CEA: Reveal paint-on and
roll-up captions character by character"*; 5.1.0 added raw CEA-608 packet extraction.

## Side-loading text

`addTextTrackAsync(uri, language, kind, mimeType?, codec?, label?, forced?)` → `Promise<TextTrack>`.
JSDoc (`lib/player.js` L7086–7103, verbatim): *"Adds the given text track to the loaded manifest.
`load()` must resolve before calling. The presentation must have a duration. This returns the created
track, which can immediately be selected by the application. **The track will not be automatically
selected.**"*

Constraints: fails on live with `CANNOT_ADD_EXTERNAL_TEXT_TO_LIVE_STREAM` (4033); fails in `src=` mode
with `CANNOT_ADD_EXTERNAL_TEXT_TO_SRC_EQUALS` (2012), WebVTT only via `TEXT_ONLY_WEBVTT_SRC_EQUALS`
(2013).

## Displayer choice — and why your styling is inert

| Fact | Evidence |
|---|---|
| The **default** `textDisplayFactory` picks `UITextDisplayer` only when `videoContainer_` is set **and** the video is not in `webkitDisplayingFullscreen` **and** `webkitPresentationMode` is `'inline'` (or absent). Otherwise `NativeTextDisplayer`. | `lib/player.js` `defaultConfig_()` L7743–7770 |
| The container comes from the Player constructor's 2nd argument or `player.setVideoContainer(el)`. The Shaka UI sets it automatically. | `docs/tutorials/text-displayer.md` |
| Changing `textDisplayFactory` during playback reloads the text tracks. It may also be re-invoked automatically when `webkitPresentationMode` changes, if `setVideoContainer` was called. | `externs/shaka/player.js` |
| `player.getTextDisplayer()` returns the live displayer. | L7798 |
| **v5.0 plugin breaking changes:** `TextDisplayer` plugins must implement `configure()`; `enableTextDisplayer` was removed from the plugin interface; built-in displayer constructors take a `shaka.Player` as their **only** parameter; `TextParser` plugins must implement `setManifestType()`. | `upgrade.md` v5.0 |

So: `fontScaleFactor`, `positionArea` and the 5.3.x style keys below are **silently inert under `NativeTextDisplayer`**. If your
caption styling does nothing, check `getTextDisplayer()` before changing CSS.

## `textDisplayer.*` and related configuration

| Key | Default | Note |
|---|---|---|
| `textDisplayer.fontScaleFactor` | `1` | **UITextDisplayer only.** |
| `textDisplayer.positionArea` | `''` (DEFAULT) | `DEFAULT`, `TOP_LEFT`, `TOP_CENTER`, `TOP_RIGHT`, `CENTER_LEFT`, `CENTER`, `CENTER_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_CENTER`, `BOTTOM_RIGHT`. **UITextDisplayer only.** |
| `textDisplayer.subtitleDelay` | `0` s | Positive = later. **New in 5.1.0.** UITextDisplayer applies it dynamically; NativeTextDisplayer rewrites cue timings at add time. |
| `textDisplayer.suspendRenderingWhenHidden` | `true`, **`false` on Tizen, WebOS, Hisense, Vizio** | Uses `IntersectionObserver` + `document.visibilityState`. **New in 5.2.0.** |
| `textDisplayer.fontFamily` | `shaka.config.FontFamily.DEFAULT` (`''`) | **UITextDisplayer only. New in 5.3.0** (#10697). 5.3.1 accepts any CSS font family (#10756). The enum values are `DEFAULT`, `MONOSPACED_SANS_SERIF`, `MONOSPACED_SERIF`, `PROPORTIONAL_SANS_SERIF`, `PROPORTIONAL_SERIF`. |
| `textDisplayer.fontColor`, `textDisplayer.backgroundColor` | `''` | **UITextDisplayer only. New in 5.3.0** (#10697). |
| `textDisplayer.fontOpacity`, `textDisplayer.backgroundOpacity` | `NaN` | **UITextDisplayer only. New in 5.3.0** (#10697). |
| `textDisplayer.characterEdgeStyle` | `shaka.config.CharacterEdgeStyle.DEFAULT` (`0`) | **UITextDisplayer only. New in 5.3.0** (#10697). Enum: `DEFAULT` 0, `NONE` 1, `DROP_SHADOW` 2, `RAISED` 3, `DEPRESSED` 4, `OUTLINE` 5. |
| `mediaSource.modifyCueCallback` | – | Per-cue edit hook. *"Works for MSE always and for `src=` only when you use UITextDisplayer."* |
| `accessibility.handleForcedSubtitlesAutomatically` | `true` | Forced-subtitle fallback in initial selection and on audio-language change. |

## Styling

| Mechanism | Note |
|---|---|
| `textDisplayer.fontScaleFactor` + `positionArea` | UITextDisplayer only. |
| UI config `captionsStyles: boolean`, `captionsFontScaleFactors: Array<number>`; UI buttons `captions-position`, `captions-size` | `ui/externs/ui.js` |
| 5.2.0: *"UI: Add live subtitle style preview on hover"*; `ui/text_style_preview.js` exists | |
| 5.3.x UI: the config key `captionsStyleElements` lists the caption style menus (font family, colour, size, background colour and opacity, character edge style, font opacity, position, reset). Default is the full list. | #10681, #10692, #10711, `ui/ui.js` at 5.3.4. UITextDisplayer only. |
| `player.addFont(name, url)` | Custom caption fonts. |
| Beyond that: a custom `TextDisplayer`. Upstream: *"Subtitles are rendered by the browser by default. Applications can create a text display plugin for customer rendering to go beyond browser-supported attributes."* | |
| **A caption-specific CSS custom-property list** | `not documented` — searched `docs/tutorials/ui-customization.md` (which documents `--shaka-*` for **controls only**) and `text-displayer.md` on 2026-07-28; none found. The `--shaka-*` variables do **not** style caption text. |

Typography, contrast and readability standards for captions belong to `/alaa-ui-ux-design-system`
(`$alaa-ui-ux-design-system`); this file owns only the mechanism that makes them reachable.

## Parsing and rendering fixes, 5.2.13 to 5.3.4

Sources: CHANGELOG at v5.3.4 and v5.2.17, read 2026-11-12. PR pages are
`https://github.com/shaka-project/shaka-player/pull/<number>`.

| Change | Release |
|---|---|
| WebVTT percentage `font-size` becomes `em` (#10727). A cue percentage is relative to the cell height, not to the inherited size. | 5.2.14, 5.3.0 |
| TTML: namespace-qualified elements (#10713). | 5.2.14, 5.3.0 |
| TTML: IMSC timing, region and style conformance (#10729); region units (#10778); default line height `normal` (#10835). | 5.3.0, 5.3.2, 5.3.3 |
| WebVTT: vertical cue anchoring (#10775) and cue box clamping (#10766). | 5.2.15, 5.3.2 |
| DASH text: keep the text timestamp offset when video sits in another Period (#10895). | 5.3.4 |
| Text: wrapped-line alignment on older browsers (#10851). | 5.2.17, 5.3.4 |
| UITextDisplayer: nested-cue font compounding (#10820). | 5.3.3 |
| `add*Track` relative-URI resolution (#10786); rule in `26-tracks-audio-video-text.md`, "Sidecar track URI resolution (5.3.3, 5.2.16)". | 5.2.16, 5.3.3 |

A row that lists a 5.2.x release is also in that 5.2 patch. A client on 5.2.13 gets #10727 and the other 5.2.14 to 5.2.17 rows by moving to 5.2.17 or to 5.3.

## Native-displayer failure modes (local observations)

Label: **local observation, not upstream.** Recorded 2026-11-12 on a standalone page in Chromium build 1247
(headless shell). The first case ran on Shaka 5.3.4. The second ran on Shaka 5.2.13 only (see its Evidence
line). No upstream issue or CHANGELOG entry describes either case
(CHANGELOG at v5.3.4 searched, read 2026-11-12). Re-prove each workaround on the Chromium build and
Shaka version you ship. Symptom routing is in `85-troubleshooting-by-symptom/20-playback-quality-and-captions.md`.

### First selection of a side-loaded data: track shows 0 cues

- **Symptom.** `load()` in MediaSource mode, then `addTextTrackAsync` with a WebVTT `data:` URI, then
  `selectTextTrack`. The browser track holds 0 cues. After a second `selectTextTrack` (reselect) it
  holds all 3 cues.
- **Cause.** Not proved. `createTrackNode_` sets `src = 'data:,WEBVTT'` and `mode = 'disabled'` on a
  fresh `<track>`. The first switch to `showing` or `hidden` appears to discard the cues appended in the
  same tick. `NativeTextDisplayer` and `TextEngine` did not change between 5.2.13 and 5.3.4, so the
  upgrade does not fix it.
- **Workaround.** Warm each idle track node once. Set its `mode` to `hidden`, then to `disabled`, in one
  synchronous tick. Run the warm-up for every idle node (`mode` `disabled`, `readyState` `NONE`) after
  the tracks are added and after each `textchanged` event (in a microtask). Result: 3 cues on the first
  selection.
- **Scope limits.** MediaSource load mode only. Warm each node once, not per selection. Never select a
  track in the warm-up.
- **Evidence.** One run on the page above. Other Chromium builds, other Shaka versions and non-`data:` side-load URIs are untested.

### Late HLS WebVTT selection stays at 0 cues

- **Symptom.** Segmented HLS WebVTT. The user selects the text track after all video is buffered. The
  track stays at 0 cues.
- **Cause.** `TextEngine` defers non-external text segments until a timestamp offset arrives. That
  offset comes from a later video append. With all video already buffered, no append follows.
- **Workaround.** Prime `TextEngine` right after `load()` resolves: call `selectTextTrack` on one text
  track, then `selectTextTrack(null)`. Never leave that track selected.
- **Scope limits.** MediaSource mode and segmented (non-external) HLS text only. Prime once, right after `load()`.
- **Evidence.** Reproduced on 5.2.13 only. For 5.3.4 this is **inferred** from identical `TextEngine` code. Re-prove on 5.3.4 before you drop the prime.

## Failure modes

`INVALID_TEXT_HEADER` 2000 · `INVALID_TEXT_CUE` 2001 · `UNABLE_TO_DETECT_ENCODING` 2003 ·
`BAD_ENCODING` 2004 · `INVALID_XML` 2005 · `INVALID_MP4_TTML` 2007 · `INVALID_MP4_VTT` 2008 ·
`UNABLE_TO_EXTRACT_CUE_START_TIME` 2009 · `INVALID_MP4_CEA` 2010 ·
`TEXT_COULD_NOT_GUESS_MIME_TYPE` 2011 · `CANNOT_ADD_EXTERNAL_TEXT_TO_SRC_EQUALS` 2012 ·
`TEXT_ONLY_WEBVTT_SRC_EQUALS` 2013 · `MISSING_TEXT_PLUGIN` 2014 ·
`CANNOT_ADD_EXTERNAL_TEXT_TO_LIVE_STREAM` 4033.

Category `TEXT` (2) is recoverable when `streaming.ignoreTextStreamFailures` is `true` — a broken
subtitle track then does not kill playback.

## Working snippet — side-load and style

```js
// UITextDisplayer is required for fontScaleFactor / positionArea to do anything.
player.setVideoContainer(document.getElementById('video_container'));
// (or: new shaka.Player(null, container); the Shaka UI does this for you)

player.configure({
  textDisplayer: {
    fontScaleFactor: 1.4,
    positionArea: shaka.config.PositionArea.BOTTOM_CENTER,
    subtitleDelay: 0,                  // seconds; positive delays subtitles (5.1.0+)
    suspendRenderingWhenHidden: true,  // saves CPU off-screen (5.2.0+)
  },
  accessibility: { handleForcedSubtitlesAutomatically: true },
  streaming: { ignoreTextStreamFailures: true },  // a bad subtitle must not kill playback
});

await player.load(manifestUri);   // MUST resolve before addTextTrackAsync

// Side-loading is not allowed on live (4033), nor in src= mode except WebVTT (2012 / 2013).
if (!player.isLive() &&
    player.getLoadMode() === shaka.Player.LoadMode.MEDIA_SOURCE) {
  const track = await player.addTextTrackAsync(
      'https://cdn.example.com/subs/fa.vtt',
      /* language= */ 'fa',
      /* kind= */ 'subtitle',
      /* mimeType= */ 'text/vtt',
      /* codec= */ undefined,
      /* label= */ 'Farsi',
      /* forced= */ false);
  // Not auto-selected. Selecting it also makes it visible - there is no
  // setTextTrackVisibility in v5.
  player.selectTextTrack(track);
}

// If the built-ins are not enough. v5.0: the constructor takes the Player as its ONLY parameter,
// and the plugin must implement configure().
player.configure('textDisplayFactory', (p) => new MyTextDisplayer(p));
```

**Best practice.** Call `setVideoContainer()` (or pass the container to the constructor) before you
expect any `textDisplayer.*` key to have an effect, and assert `getTextDisplayer()` in a test rather
than eyeballing the render.
**Common mistake.** Calling `addTextTrackAsync()` before `load()` resolves, or on a live stream. The
first is documented as required; the second throws 4033. A close third: styling captions with
`--shaka-*` variables, which cover controls only.
