# QA checklist

## Mode selection
- headless for API calls, retries, analytics, auth filters, event emission, and recovery logic
- visual browser mode for controls, captions, overlays, ads, accessibility, focus order, and responsive UX

## Browser matrix
- Chrome
- Edge
- Firefox
- Safari
- Android Chrome
- Android WebView, if relevant
- iOS Safari
- WKWebView, if relevant

## Playback basics
- load
- play
- pause
- seek
- replay
- playback rate
- startup offset through `updateStartTime`
- subtitle toggle
- subtitle delay, if exposed
- track switching
- structured audio, text, and video preference fallback order

## Network behavior
- throttled bandwidth
- token expiration
- network interruption
- recovery and retry behavior
- signed URL refresh or license header refresh

## Ads
- pre-roll
- mid-roll
- post-roll
- ad-playing state
- interstitial preload state
- ad failure recovery
- resume behavior

## Analytics
- heartbeat cadence
- hidden tab policy
- event integrity
- QoE capture

## Overlays and markers
- quiz timing
- seek policy
- chapter images and chapter URI behavior, if used
- marker add, remove, jump, and share

## Conductor and playlist
- correct item selection
- correct startup offset
- end-to-next behavior
- source switch recovery

## Lifecycle safety
- route changes
- repeated mount and unmount
- timer cleanup
- event listener cleanup
- memory growth checks

## Visual UX checks
- loading and empty states
- control contrast and hit targets
- captions readability
- overlay stacking and dismiss behavior
- keyboard or remote navigation where relevant

## Headless evidence
- emitted event order
- retry or auth refresh path
- analytics heartbeat cadence
- wrapper teardown integrity
