# Upstream watchlist

Use this file before changing version pins, copying an old workaround, or
recommending a new player architecture.

## Current baseline

As of **2026-06-28**:

- GitHub releases API shows `v5.1.11` as the latest checked release,
  published **2026-06-24**.
- Official Shaka upgrade docs list a `v5.1` migration item: individual
  preference config fields are deprecated in favor of structured
  `preferredAudio`, `preferredText`, and `preferredVideo` arrays.
- Older notes for `v5.0.8` and `v4.16.24` remain useful only when the target
  repo is pinned to those lines.
- For `v5.0.8` to `v5.1.11`, read
  `MIGRATION_5_0_8_TO_5_1_11.md` before changing application code.

## 5.1.11 release note highlights

- Text: `LINE_THROUGH` maps to valid CSS `line-through`.
- UI: `mute_volume` is available as a composite element to avoid hover jank
  between the mute button and volume bar.

## Patch-line fixes to re-check before app workarounds

- HLS and LL-HLS: live playlist refresh stalls, timeline sync gaps,
  discontinuity sequences, long DVR startup, MIME mapping for
  `audio/x-mpegurl`, and live playlist refresh performance.
- DASH and segment indexing: lazy segment reference creation, period parsing,
  binary search in hot paths, and lower allocation pressure.
- DRM: hangs after DRM playback, key-status teardown, SAMPLE-AES stalls, and
  PlayReady fixes across Windows browsers.
- Ads/UI: pre-roll replay prevention, ad marker alignment, mute/volume hover
  behavior, ad-state control updates, and context-menu closure.
- Text/captions: external preferred text tracks, text-region cache keys,
  TTML/CSS safety, VTT allocation pressure, and valid line-through styling.

Implication:

- Re-check whether the issue still reproduces on the pinned Shaka version before
  shipping an app-level workaround.

## 5.1 feature surfaces to consider

- Structured audio, text, and video preferences with fallback priority order.
- `subtitleDelay` for user-facing subtitle timing offset.
- Chapter images, external chapter URI support, and richer MediaSession chapter
  behavior.
- Ad events and interstitial metadata such as real ad playback start and
  preloaded interstitial signals.
- ABR behavior informed by low-latency mode and dropped frames.
- UI options for paused-state controls, right-side menus, track label formats,
  touch/seek behavior, MediaSession Auto PiP, chapter thumbnails, and
  mute/volume interaction.
- Platform and format support for TiVo OS, Titan OS, DASH JSON, automatic DASH
  XLink processing, HLS `CAN-SKIP-DATERANGES`, MoQT/MSF improvements, and queue
  item metadata.

## Pull requests and issue notes to re-check

Open PRs and issues are troubleshooting inputs only. Treat a note as fixed only
after it is confirmed in an official release note, official doc, or focused
local reproduction on the target version.

## Durable platform notes from official docs

- Basic usage still shows `new shaka.Player()` followed by `await player.attach(video)`.
- The FAQ still warns that Shaka Player must not be wrapped in a Vue reactive
  object.
- The FAQ still states that iOS support depends on Apple's native HLS path, so
  DASH parity should not be assumed on iOS.
- License request filters run on every attempt in v5.x, which is useful for
  token refresh on retries.
- FairPlay support differs between Modern EME and legacy Apple Media Keys, and
  provider-specific request or response filters are common.
- The official upgrade guide is the source of truth for removed, renamed, and
  deprecated public APIs.

## Maintenance rule

Whenever you update this skill:

1. re-check the releases page
2. check the official upgrade guide and generated API docs for documented public
   migration surfaces
3. scan open PRs only for watch items, not normative migration claims
4. update this watchlist before editing workflow guidance elsewhere
