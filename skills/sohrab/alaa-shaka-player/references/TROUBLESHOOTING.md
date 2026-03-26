# Troubleshooting

## SSR errors
Symptoms:
- `window is not defined`
- `HTMLMediaElement is not defined`

Fix:
- import Shaka dynamically
- initialize only in the browser
- avoid server-side execution of media code

## Vue reactivity problems
Symptoms:
- strange proxy-related behavior
- non-obvious player failures

Fix:
- keep the Shaka instance non-reactive

## HLS live oddities
Symptoms:
- long delays between playlist refreshes
- buffering after each live chunk
- duplicate segment fetches after seeks or stream switches

Fix:
- verify the current Shaka release first
- inspect live-HLS config before adding custom hacks
- check the upstream watchlist for open stream-switch and live-manifest issues

## Memory leaks
Symptoms:
- growing memory after route changes
- old network activity continuing after unmount
- duplicate event handling

Fix:
- destroy the player
- remove listeners
- clear timers
- avoid creating duplicate wrappers on remount

## Subtitle issues
Symptoms:
- external subtitles do not show
- wrong default track

Fix:
- add text tracks through the player API
- make selection rules explicit in the UI

## Ad session gets stuck
Symptoms:
- the ad never starts
- content never resumes

Fix:
- add a watchdog timeout
- force recovery into the content path

## DRM and FairPlay problems
Symptoms:
- FairPlay works on one Safari path but stalls on another
- license requests fire but encrypted playback never starts
- `src=` playback behaves differently from MSE playback

Fix:
- review the current FairPlay tutorial and watchlist items
- keep provider-specific request or response filters isolated
- do not assume legacy Apple Media Keys and Modern EME paths behave the same

## Diagnostics workflow

When the failure is not obvious:

- reproduce on a minimal stream first
- raise Shaka log level when using the debug build
- capture network retries, HTTP status, and wrapper-emitted events
- save visual QA for UI symptoms; prefer headless evidence for retry or DRM logic
