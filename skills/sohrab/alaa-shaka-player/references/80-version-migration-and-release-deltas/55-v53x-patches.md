For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## 5.3.x patch releases

Source for every entry, `verified`, read 2026-11-12: `CHANGELOG.md` at tag `v5.3.4`
(`https://github.com/shaka-project/shaka-player/blob/v5.3.4/CHANGELOG.md`) and the tag page
`https://github.com/shaka-project/shaka-player/releases/tag/v<version>`. Features of 5.3.0 are in
[v5.3.0 features](./45-v530-features.md). Fixes marked "also 5.2.N" ship in that 5.2 patch with the same PR
number; see [v5.2.x patches](./50-v52x-patches.md).

**5.3.4** (2026-11-06, also 5.2.17 unless marked 5.3 only): destroy() interrupting load() or attach() no
longer leaks or hangs (#10928) · interrupted unload() no longer leaks a MediaSource (#10886) · failed
segment prefetches are not reused on retry (#10902) · TypeError fixes during unload (#10927) and a
segment-index release (#10885) · unhandled rejection on failed preload removed (#10913) · **5.3 only:**
DASH keeps the text timestamp offset when video is in another Period (#10895) · **5.3 only:** MediaSource
polyfill codec rejection works (#10868) · DASH PTO (#10881) and `minimumUpdatePeriod` 0 (#10919) ·
preload initial variant from the bandwidth estimate (#10827) · wrapped-line text alignment (#10851) ·
UI seek-bar preview follows the live range (#10924) · **5.3 only:** UI mouse-wheel seeking (#10880),
keyboard focus indicator over video (#10906), dismissible and hoverable tooltips (#10904) · **5.3 only:**
ads: mid-roll detection without presented frames (#10925), embedded slots excluded from the break count
(#10926) · **5.3 only:** MKV and MSF fixes (experimental builds).

**5.3.3** (2026-10-29, also 5.2.16 unless marked): `add*Track` resolves relative URIs against the page
(#10786) · **MediaSource reset when `changeType` fails (#10807)** · **playback position kept after a reset
(#10806)** · DRM sessions closed after a failed licence request (#10804) · HLS redundant variant URIs
(#10787) · preload Content Steering (#10826) · **5.3 only:** TTML paragraph line height defaults to
`normal` (#10835), UI nested-cue font-size compounding (#10820), "Default" style option translation
(#10805), SVTA pod linking (#10808).

**5.3.2** (2026-10-23, also 5.2.15 unless marked): **network outage ends with an error (#10784)** ·
`endNumber` (#10785) · CMCD query mode (#10764; #10779 is 5.3 only) · HLS live window (#10741) · WebVTT vertical cue
anchor (#10775) and box clamp (#10766) · **5.3 only:** skip-range API aligned with its documentation
(#10753), TTML region units (#10778), no Safari 8-12 MSE workarounds on PlayStation (#10794).

**5.3.1** (2026-10-19): any CSS font family is accepted in `textDisplayer.fontFamily` (#10756). 5.3 only.

### Consumer proof for the shared fixes

Run the matching scenario when the new pin contains the fix. The scenarios below cover fixes that also ship in 5.2.x. 5.3-only scenarios follow under "5.3-only proof".

- **#10784 outage ends in an error.** Cut the network during playback. Assert an `error` event arrives after the
  retry budget instead of endless variant switching, assert its `severity` is CRITICAL, and record its `code` (the
  error is the existing CRITICAL NETWORK error; see `35-unstable-networks-and-resilience.md`, "Changes since 5.2.13"). The app must own the
  recovery (user retry or reload). The retry budget stays in `35-unstable-networks-and-resilience.md`.
- **#10806, #10807 MSE reset.** Force a `changeType` failure (or another path that resets the MediaSource).
  Assert playback resumes at the previous position on a fresh MediaSource.
- **#10902 prefetch.** Fail a segment fetch, then retry. Assert the retry issues a new request.
- **#10886, #10928 teardown.** Call `destroy()` or `unload()` while `load()` or `attach()` is pending. Assert
  the call settles, no MediaSource or listener stays, and no new session opens.
- **#10786 relative track URIs.** Assert every sidecar track URL still resolves (rule: `26-tracks-audio-video-text.md`,
  "Sidecar track URI resolution (5.3.3, 5.2.16)").

### 5.3-only proof

- **#10895 text offset (5.3.4 only).** Play DASH with text and video in different Periods. Assert cue times
  match the video.

### Text path in 5.3.4

`lib/text/native_text_displayer.js` and `lib/text/text_engine.js` are byte-identical in `shaka-player@5.2.13` and
`@5.3.4` (npm tarball diff, `verified`, read 2026-11-12). No `CHANGELOG.md` entry that is new since 5.2.13 (5.2.14
to 5.2.17, and 5.3.0 to 5.3.4 without the lines repeated from 5.2.x) mentions the native displayer or the Chromium
first-selection cue loss. The 5.3.0 line #10678 is the 5.2.13 fix repeated. When you upgrade to 5.3.4 and the
repository carries a caption workaround, keep it and re-prove it. Evidence and procedures:
`28-subtitles-and-text-displayer.md`, "Native-displayer failure modes".
