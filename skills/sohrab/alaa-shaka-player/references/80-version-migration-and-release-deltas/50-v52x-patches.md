For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## 5.2.x patch releases

Source for the 5.2.13 to 5.2.17 entries below: the release tag page and `CHANGELOG.md` at tag `v5.2.17`
(`https://github.com/shaka-project/shaka-player/blob/v5.2.17/CHANGELOG.md`), `verified`, read 2026-11-12.
The tag page URL is `https://github.com/shaka-project/shaka-player/releases/tag/v<version>`.
Every fix in 5.2.14, 5.2.15, 5.2.16 and 5.2.17 also ships, with the same PR number, in 5.3.0, 5.3.2, 5.3.3 and 5.3.4 respectively. Each 5.3 release also carries fixes that its 5.2 line lacks, and 5.2.15 to 5.2.17 list fixes (#10765, #10842, #10844, #10916) that the matching 5.3 entries in this skill do not list, so read both entries.

**5.2.17** (2026-11-06): destroy() interrupting load() or attach() no longer leaks or hangs (#10928) ·
interrupted unload() no longer leaks a MediaSource (#10886) · no TypeError when a stream fails during
unload (#10927) · no unhandled rejection when a preload fails (#10913) · failed segment prefetches are
not reused on retry (#10902) · TypeError fix when the segment index is released during a switch
(#10885) · DASH: PTO timeline adjustment applied once (#10881), no continuous manifest updates when
`minimumUpdatePeriod` is 0 (#10919) · preload picks the initial variant from the bandwidth estimate
(#10827) · wrapped-line text alignment on older browsers (#10851) · UI seek-bar preview follows the
live seek range (#10924) · faster large-buffer comparison (#10916).

**5.2.16** (2026-10-29): `add*Track` methods resolve relative URIs against the page (#10786) ·
MediaSource reset when `changeType` fails (#10807) · playback position kept after a MediaSource reset
(#10806) · DRM sessions dropped after a failed licence request are closed (#10804) · HLS falls back to
redundant variant URIs when a media playlist fails (#10787) · preload keeps Content Steering updating
(#10826) · no unhandled rejections when unloading during an ad (#10842) · Opus rejected on 1st-gen
Chromecast (#10844).

**5.2.15** (2026-10-23): **a network outage now ends with an error instead of switching variants
forever (#10784)** · DASH `SegmentTemplate@endNumber` honoured (#10785) · CMCD query mode keeps
relative request URIs working (#10764) · HLS live window anchored to the playlist (#10741) ·
multiplexed MP4 plays with `forceTransmux` (#10765) · WebVTT vertical cues anchor to the correct edge
(#10775) and cue boxes clamp to the space the anchor leaves (#10766).

**5.2.14** (2026-10-16): WebVTT percentage font sizes stay relative to the subtitle size (#10727) ·
TTML namespace-qualified elements (#10713) · CEA caption continuity for split muxed content (#10734) ·
DASH stall fix when a fixed-duration segment lookup rounds up (#10717) · codec probing survives a
throwing transmuxer plugin (#10735).

**5.2.13** (2026-10-09): ABR keeps the whole ladder when each quality has its own audio group
(#10672) · prefetch cache cleared for init segments and aborted requests (#10587) · DASH: captions
survive a Period timeline that ends early (#10649), no freeze when live Period IDs reappear (#10641) ·
a manifest ClearKey licence URL no longer overrides `drm.servers` (#10659) · corrupted cbcs ClearKey
playback fixed (#10695) · HLS switch from muxed audio to a separate TS audio rendition (#10661) ·
`crossBoundaryStrategy` kept across loads (#10660) and boundary crossing continues when the playhead
overshoots (#10676) · preload prefetches the segment that holds the start time (#10702) · live
segment availability enforced on the presentation timeline (#10617) · WebVTT: REGION blocks and
WebVTT-in-MP4 regions parsed (#10677), regions rendered by the native text displayer (#10678) and by
the UI displayer (#10679), subtitles shown in fMP4 HLS with absolute cue times (#10688) · UI: swipe
hides controls (#10664), seek-bar previews stay in bounds (#10714), rate decimal separators unified
(#10693).

**Consumer proof for 5.2.13 to 5.2.17.** When the target pin contains any of #10784, #10786, #10806, #10807,
#10886, #10902 or #10928 and the installed pin does not, run the matching scenario in
[v5.3.x patches](./55-v53x-patches.md#consumer-proof-for-the-shared-fixes).

**5.2.12** (2026-09-25), [official release](https://github.com/shaka-project/shaka-player/releases/tag/v5.2.12),
read 2026-09-29: fixes low-latency segment loss after successful retries, wedged-player destruction,
DRM session creation during teardown, DASH key-ID discovery from init segments, MP4 WebVTT fragment
parsing and CEA-708 pen opacity.

Before upgrading a consumer, read every intervening patch from its installed pin; this list is not
an exhaustive 5.2.4-5.2.11 audit. Reproduce the applicable retry/recovery, concurrent teardown/DRM,
missing-manifest-key-ID and multi-fragment caption scenarios. Assert segment continuity, settled
destruction with no new sessions, playable encrypted media and complete/readable captions. Use the
proof modes in `90-qa-modes-and-checklist.md`; release notes are not consumer runtime proof.

**5.2.3** (2026-07-27) — single fix: *"Reset media source before switching variant on MSE append
failure (#10380)."*

**5.2.2** (2026-07-20) — *"Fix duplicate error code 4058 (#10372)"* · MSF draft-16 negotiation and
empty-catalog skipping · MSF bandwidth per group · **"net: isolate headers across retry attempts
(#10361)"** · *"Prevent `screen.orientation` methods from being garbage collected on Safari
(#10364)"* · a shaka-bot glob-expansion security fix · transmux falls back to the main thread when
the worker fails · UI context-menu and rate-slider touch fixes on mobile.

**5.2.1** (2026-07-14) — *"Restore correct playhead position after MediaSource reload (#10335)"* ·
transmux worker device registration · transmux main-thread fallback on worker timeout · thumbnail
preview scaling · rate menu clipping on narrow screens · **"UI: Scope form element font inheritance
to the player container (#10353)"**.
