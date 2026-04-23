# Upstream watchlist

Use this file before changing version pins, copying an old workaround, or
recommending a new player architecture.

## Current baseline

As of **2026-04-24**:

- GitHub releases API shows `v5.1.1` as the latest release, published **2026-04-20**.
- Older notes for `v5.0.8` and `v4.16.24` remain useful only when the target repo is pinned to those lines.

## Older fixes to remember when a repo is pinned to 5.0.8 or 4.16.24

- HLS: DTS and DTS-HD audio codec variants
- HLS: prevent infinite manifest update delay
- HLS: more tolerant duplicate segment detection
- HLS and DASH parsing: lower allocation and GC pressure
- Player and VTT parsing: reduced function churn and allocation pressure

Implication:

- Re-check whether a live-HLS, segment-duplication, or parser-performance issue
  still reproduces before shipping a custom workaround.

## Pull requests and issue notes to re-check

The PR numbers below were useful watch items in the earlier snapshot. Re-check
their current state before treating them as open, fixed, or released.

### `#9896` Buffer-based ABR for low-latency live

What it changes:

- adds `shaka.abr.BufferBasedAbrManager()`
- targets low-latency live where bandwidth estimation is unreliable
- switches quality based on buffer health relative to target latency

Implication:

- For low-latency live tasks, mention this upstream direction before building a
  custom ABR manager.

### `#9864` Duplicate segment downloads during stream switching

What it changes:

- addresses duplicate segment fetches caused by floating-point drift and segment
  discontinuities during seeks or variant switches

Implication:

- When users report AV sync slips or repeated segment downloads, verify the
  pinned Shaka version before implementing app-level drift hacks.

### `#9795` FairPlay polyfill fixes for Safari `src=` playback

What it changes:

- fixes `com.apple.fps` to `com.apple.fps.1_0` remapping in the legacy Apple
  media-keys polyfill
- removes a metadata-ready-state deadlock in `src=` mode

Implication:

- For Safari or FairPlay bugs, distinguish carefully between Modern EME,
  legacy Apple Media Keys, `src=` playback, and MSE playback.

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

## Maintenance rule

Whenever you update this skill:

1. re-check the releases page
2. scan open PRs for playback, HLS, ABR, DRM, or TV-platform items
3. update this watchlist before editing workflow guidance elsewhere
