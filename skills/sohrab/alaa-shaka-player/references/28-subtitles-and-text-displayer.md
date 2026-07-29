# Subtitles, captions and the TextDisplayer

All rows `verified` at v5.2.3, read 2026-07-28.

## Current position

Two built-in displayers. `shaka.text.NativeTextDisplayer` uses the browser's cue renderer via `<track>`
elements and is the default **without** the Shaka UI. `shaka.text.UITextDisplayer` renders into a DOM
container and is the default **with** the UI. `SimpleTextDisplayer` was replaced by
`NativeTextDisplayer` in v5.0. Three legacy formats (**LRC, SBV, SSA**) were removed in v5.0; SRT
survived, UTF-8 only.

## Supported formats

Registered parsers, from the `shaka.text.TextEngine.registerParser(...)` call sites in `lib/text/`:

| MIME type | Parser |
|---|---|
| `text/vtt`, `text/vtt; codecs="vtt"`, `text/vtt; codecs="wvtt"` | `vtt_text_parser.js` |
| `application/mp4; codecs="wvtt"` | `mp4_vtt_parser.js` |
| `application/ttml+xml` | `ttml_text_parser.js` |
| `application/mp4; codecs="stpp"` and the 9 `stpp.ttml.*` / `stpp.TTML.im1t` variants | `mp4_ttml_parser.js` |
| `text/srt` | `srt_text_parser.js` |

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

So: `fontScaleFactor` and `positionArea` are **silently inert under `NativeTextDisplayer`**. If your
caption styling does nothing, check `getTextDisplayer()` before changing CSS.

## `textDisplayer.*` and related configuration

| Key | Default | Note |
|---|---|---|
| `textDisplayer.fontScaleFactor` | `1` | **UITextDisplayer only.** |
| `textDisplayer.positionArea` | `''` (DEFAULT) | `DEFAULT`, `TOP_LEFT`, `TOP_CENTER`, `TOP_RIGHT`, `CENTER_LEFT`, `CENTER`, `CENTER_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_CENTER`, `BOTTOM_RIGHT`. **UITextDisplayer only.** |
| `textDisplayer.subtitleDelay` | `0` s | Positive = later. **New in 5.1.0.** UITextDisplayer applies it dynamically; NativeTextDisplayer rewrites cue timings at add time. |
| `textDisplayer.suspendRenderingWhenHidden` | `true`, **`false` on Tizen, WebOS, Hisense, Vizio** | Uses `IntersectionObserver` + `document.visibilityState`. **New in 5.2.0.** |
| `mediaSource.modifyCueCallback` | – | Per-cue edit hook. *"Works for MSE always and for `src=` only when you use UITextDisplayer."* |
| `accessibility.handleForcedSubtitlesAutomatically` | `true` | Forced-subtitle fallback in initial selection and on audio-language change. |

## Styling

| Mechanism | Note |
|---|---|
| `textDisplayer.fontScaleFactor` + `positionArea` | UITextDisplayer only. |
| UI config `captionsStyles: boolean`, `captionsFontScaleFactors: Array<number>`; UI buttons `captions-position`, `captions-size` | `ui/externs/ui.js` |
| 5.2.0: *"UI: Add live subtitle style preview on hover"*; `ui/text_style_preview.js` exists | |
| `player.addFont(name, url)` | Custom caption fonts. |
| Beyond that: a custom `TextDisplayer`. Upstream: *"Subtitles are rendered by the browser by default. Applications can create a text display plugin for customer rendering to go beyond browser-supported attributes."* | |
| **A caption-specific CSS custom-property list** | `not documented` — searched `docs/tutorials/ui-customization.md` (which documents `--shaka-*` for **controls only**) and `text-displayer.md` on 2026-07-28; none found. The `--shaka-*` variables do **not** style caption text. |

Typography, contrast and readability standards for captions belong to `/alaa-ui-ux-design-system`
(`$alaa-ui-ux-design-system`); this file owns only the mechanism that makes them reachable.

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
