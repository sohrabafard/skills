# Playback speed, seeking and trick play

All rows `verified` at v5.2.3, read 2026-07-28, from `lib/player.js` and
`externs/shaka/player.js` unless stated.

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
