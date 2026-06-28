# VAST and VMAP ads

## Scope

This runbook covers client-side ad orchestration around Shaka, typically using
IMA for VAST or VMAP flows.

## Design principles

- ads should not permanently block content playback
- ad state should be explicit
- timeout and recovery should be first-class concerns

## Minimal ad flow

1. prepare the ad container
2. request ads
3. enter ad-playing state when the ad actually starts
4. exit ad state cleanly
5. resume content or continue to the next scheduled action

In Shaka 5.1+, prefer the documented ad events for precise state:

- `ad-playing` means the ad actually started
- `ad-interstitial-preloaded` can drive preload-aware UI
- `ad-break-started` includes `startedAt` timing data when available

## Support targets

This skill is built to support:

- pre-roll
- mid-roll
- post-roll
- VAST
- VMAP
- HLS Interstitials, including X-ASSET-LIST and start-offset behavior when the
  content uses it

## Platform cautions

- Safari and iOS autoplay policy can block ad starts unless muted or user-gesture
  requirements are satisfied.
- Ad blockers can break demo or debug environments, especially when testing
  uncompiled or ad-heavy builds.
- Keep ad orchestration separate from the playback core so ad failures do not
  corrupt content playback state.

## Required fail-safe

If an ad request fails, the ad response is empty, or the ad never starts,
resume the content path instead of leaving the session stuck.

## Anti-patterns

- blocking content indefinitely while waiting for an ad callback that may never arrive
- coupling content resume logic to DOM state instead of explicit ad state
- assuming browser autoplay policy behaves the same on Safari, iOS, and Chromium
