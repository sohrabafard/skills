For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## 5.2.x patch releases

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
