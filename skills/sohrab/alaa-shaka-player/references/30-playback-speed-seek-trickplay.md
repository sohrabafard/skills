# Playback speed, seeking and trick play

All rows `verified` at v5.2.3, read 2026-07-28, from `lib/player.js` and
`externs/shaka/player.js` unless stated. The skip-range section was read 2026-11-12 at v5.3.4.

## Current position

Ordinary rate changes go through the media element (`video.playbackRate`); Shaka observes them.
**Trick play is a different mechanism**: `player.trickPlay(rate)` may drive the playhead by repeated
seeking on a timer while the element's own `playbackRate` stays at `0`, and it can also switch to a
dedicated trick-mode track.

## API surface

| Name | Notes |
|---|---|
| `video.playbackRate` | Normal rate control. |
| `player.getPlaybackRate()` | The **effective** rate, including trick play. |
| `player.trickPlay(rate, useTrickPlayTrack = true)` | *"Enable trick play to skip through content without playing by repeatedly seeking. For example, a rate of 2.5 would result in 2.5 seconds of content being skipped every second. A negative rate will result in moving backwards."* (L5504–5517) |
| `player.cancelTrickPlay()` | Restores the default rate, re-enables ABR rate notification, drops the trick-play track, clears trick-play listeners. (L5561) |
| `player.useTrickPlayTrackIfAvailable(on)` | Toggle the dedicated trick-mode track without changing rate. **MSE mode only.** (L5290) |
| `player.seekRange()` | → `{start, end}`. |
| `player.goToLive()` | Sets `video.currentTime = seekRange().end`. Warns *"goToLive is for live streams!"* if `!isDynamic()`. (L5315) |
| `player.updateStartTime(startTime)` | The supported way to set a start position during load. (L1828) |

## Trick-play behaviour

| Behaviour | Note |
|---|---|
| **`rate = 0` is rejected.** Logs *"A trick play rate of 0 is unsupported!"* and returns. `0` is used internally for buffering. | L5517–5527 |
| No-op if content is not loaded or is still loading. *"Wait until `load` has completed before calling."* | JSDoc |
| **Auto-cancels** when the playhead reaches either end of the seekable range. | JSDoc |
| In `MEDIA_SOURCE` mode it calls `abrManager_.playbackRateChanged(rate)` and `useTrickPlayTrackIfAvailable(useTrickPlayTrack && rate != 1)`. | L5535–5541 |
| When trick play falls back to **manual seeking** (rewind, or unsupported rates), the element's `playbackRate` stays `0` and a timer advances the playhead, so the browser fires **no native `ratechange`** — **Shaka dispatches `ratechange` itself.** | L5544–5560 |
| DASH trick-mode tracks are supported. *"Multiple trick mode tracks for the same resolution at varying framerates or bitrates"* are **not**. | `README.md` |
| HLS I-frame-only playlists back trick play and thumbnails. | `README.md` |

Drive UI state from the `ratechange` event, not from your own flag — Shaka synthesises that event
precisely when the native one cannot fire.

## Seek ranges and clamps

| Key / method | Default | Note |
|---|---|---|
| `player.seekRange()` in `src=`/remote mode | – | Derived from `video.seekable`, then clamped by `playRangeStart`/`playRangeEnd`. Returns `{start: 0, end: 0}` when nothing is seekable. (L5490–5508) |
| `playRangeStart` / `playRangeEnd` | `0` / `Infinity` | Clamp both playback and seeking. |
| `streaming.durationBackoff` | `1` s | Prevents seeking to exactly `duration`. Upstream: *"We recommend using the default value unless you have a good reason not to."* |
| `streaming.safeSeekOffset` | `5` s | Added when repositioning after falling out of the availability window or a seek. |
| `streaming.safeSeekEndOffset` | `0` | Added when repositioning after falling out of the seekable **end**; *"helpful for live stream with a lot of GAP"*. |
| `streaming.startAtSegmentBoundary` | `false` | Snaps start time back to a segment boundary. *"This can put us further from the live edge."* |
| `streaming.returnToEndOfLiveWindowWhenOutside` | `false` | If the playhead falls behind the window start, jump to the **end** instead of the start. |

UI keyboard/touch seek: `keyboardSeekDistance` (arrows, 5 s), `keyboardLargeSeekDistance`
(PageUp/Down, 60 s), `seekOnTaps` + `tapSeekDistance`.

UI rate config: `playbackRates` (default `[1, 1.25, 1.5, 2, 3]`), `fastForwardRates` (`[2, 4, 8, 1]`),
`rewindRates` (`[-1, -2, -4, -8]`), `playbackRateSliderMin` (`0.5`), `playbackRateSliderMax` (`3`).
When you set a seek-button distance or a rate-slider step (new in 5.3), read
`65-ui-library-skin-and-localisation.md`, section "UI changes in 5.3".

## Skip ranges (new in 5.3.0)

The rules below describe 5.3.4. #10753 (released in 5.3.2) changed the behaviour to match the JSDoc, so
5.3.0 and 5.3.1 may behave differently. The skill does not cover those versions.

Read 2026-11-12. Signatures come from `dist/shaka-player.ui.d.ts` in the `shaka-player@5.3.4` npm package.
Behaviour comes from the JSDoc in `lib/player.js` of the same package. The release notes list the
feature as "Runtime skip ranges + MediaTailor played-ad-break skipping" (#10338) and a follow-up fix,
"Align skip range API behavior with its documentation" (#10753). Both are in the CHANGELOG at tag v5.3.4,
`https://raw.githubusercontent.com/shaka-project/shaka-player/v5.3.4/CHANGELOG.md`.

| Method | Signature at 5.3.4 |
|---|---|
| `player.addSkipRange(start, end)` | `(start: number, end: number): boolean` |
| `player.removeSkipRange(start, end)` | `(start: number, end: number): void` |
| `player.clearSkipRanges()` | `(): void` |
| `player.getSkipRanges()` | `(): shaka.extern.BufferedRange[]`, a sorted list of disjoint `{start, end}` objects. It returns a copy. |

Rules:
- Support is **VOD, MediaSource, segments mode (DASH and HLS) only**. Live content, sequence mode and
  `src=` playback are not supported. `addSkipRange` returns `false` for them and logs a warning.
- `addSkipRange` returns `false` for an empty or reversed interval. After `load()` it also returns
  `false` for unsupported content.
- The range is half-open: `[start, end)`. Its segments are not fetched or buffered. Buffering continues
  from `end`. Gap jumping moves the playhead across.
- Both ends **must line up with segment boundaries** of the video stream (the audio stream for
  audio-only content). If they do not, the player keeps the range in the list, never skips it,
  and logs a warning. A `true` return does not prove the skip will happen.
- A range that touches or overlaps an existing range merges with it.
- A range that is already buffered is accepted. It takes effect only when that span is no longer buffered.
- You may call `addSkipRange` before `load()`. The player queues the range and checks it again when
  streaming starts. Use this to skip a preroll before it buffers. Before `load()`, the call checks
  only the interval.
- `removeSkipRange` subtracts an interval. Removing part of a range trims it. Removing the middle
  splits it in two. It is not an exact-match delete.
- A removed range behind the playhead is not fetched again until the user seeks back across it.
- `clearSkipRanges` removes all ranges and fetches them again.
- `unload()` clears the skip ranges (`lib/player.js`, package 5.3.4). Add the ranges again for each new
  asset. Source reading (`lib/player.js`, 5.3.4, not runtime-tested): `load()` runs its internal
  unload only when an asset is already loaded, and `unload()` clears all skip ranges. Ranges queued
  before the first `load()` are re-applied when streaming starts. Ranges added while another asset is
  loaded apply to that asset and are cleared by the next `load()`. To queue ranges for a new asset,
  call `unload()` first or add them after `load()` resolves. Confirm with `getSkipRanges()` after
  `load()` resolves.

## Timeline markers, chapters and deep links

Chapters come from `getChaptersTracks()` / `getChaptersAsync(language)` (`getChapters` was replaced in
v5.0) and `addChaptersTrack(uri, language, mimeType)` — the last fails on live with
`CANNOT_ADD_EXTERNAL_CHAPTERS_TO_LIVE_STREAM` (4055). Thumbnails come from `getImageTracks()`,
`getAllThumbnails(trackId)` and `getThumbnails(trackId, time)`;
`addThumbnailsTrack(uri, mimeType)` fails on live with 4045.

A share link of the form `/watch/<id>?t=123.4` is a URL contract, not a player concern — but **if
`<id>` ever resolves to a presigned asset, that share link is a transferred read grant**. Read
`42-media-url-trust-and-presigned.md` before generating one.

## Working snippet

```js
// --- Ordinary rate ---
video.playbackRate = 1.5;
player.addEventListener('ratechange', () => {
  // The ONLY correct source for UI rate state: Shaka synthesises this event
  // during timer-driven trick play, where the native one never fires.
  renderRate(player.getPlaybackRate());
});

// --- Trick play: fast forward at 8x, using the trick-mode track if present ---
await player.load(uri);            // trickPlay() is a no-op before this resolves
try {
  player.trickPlay(8, /* useTrickPlayTrack= */ true);
  await userReleasesFastForwardButton();
} finally {
  player.cancelTrickPlay();        // ALWAYS paired, even on an exception
}

// --- Rewind. Negative rates almost always fall back to timer-driven seeking. ---
player.trickPlay(-4);
player.cancelTrickPlay();

// --- Live edge ---
if (player.isLive()) {
  const {start, end} = player.seekRange();
  renderDvrWindow(end - start);
  player.goToLive();               // jumps to seekRange().end
}

// --- Clamp the playable window (a preview or a licensed excerpt) ---
player.configure({playRangeStart: 30, playRangeEnd: 90});

// --- Start position: NEVER video.currentTime during startup ---
player.addEventListener('manifestparsed', () => {
  player.updateStartTime(resumePositionSeconds);   // required since v5.0
});
```

**Best practice.** Pair `trickPlay()` with `cancelTrickPlay()` in a `finally`, and clamp any rate the
user can reach to the values you actually put in the UI's `playbackRates` list — a rate outside it has
no menu row to return from.
**Common mistake.** `player.trickPlay(0)` to pause. It is explicitly rejected and logs a warning; use
`video.pause()`. Second: setting `video.currentTime` during startup instead of
`player.updateStartTime()`, which v5.0 made the required path.
