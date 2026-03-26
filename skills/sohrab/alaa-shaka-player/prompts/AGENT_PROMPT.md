# Single-agent prompt

Use this prompt when you want one coding agent to handle the full task.

You are implementing a **modular Shaka Player integration** in a **Vue 3 + Quasar + Vite** application.

## Goal
Replace Video.js or an existing player wrapper with a Shaka-based architecture that supports:

- HLS-first playback
- optional DASH support
- adaptive bitrate
- subtitles
- VAST or VMAP ads
- watch-time analytics
- interaction tracking
- quiz overlays during playback
- timeline markers for notes, comments, bookmarks, and share links
- playlist support
- TV-like schedule-based playback conductor

## Constraints
- Verify the current Shaka release before pinning a version or repeating an old workaround
- Use the current basic usage pattern: create the player first, then attach to the video element
- Keep the player instance out of Vue reactivity
- Keep all Shaka initialization client-only and SSR-safe
- Ensure full cleanup on unmount
- Keep the core wrapper small and move product logic into separate modules
- Choose the QA mode deliberately:
  - headless for API calls, retries, analytics, and event behavior
  - visual browser validation for controls, captions, ads, overlays, and responsive UX
- If the user explicitly wants a stronger player UI or premium watch-page UX, pair the implementation with the design rules from `$frontend-skill`
- For repo-safe Vue or Quasar implementation details, pair with `$alaa-frontend-developer`

## Deliverables
1. `ShakaPlayer.vue`
2. `useShakaCore.ts`
3. `AnalyticsTracker.ts`
4. `QuizEngine.ts`
5. `TimelineMarkers.ts`
6. `PlaybackConductor.ts`
7. `AdsManager.ts`
8. `PlayerLabPage.vue`
9. A migration plan and QA checklist

## Execution style
- Start with a short implementation plan
- Re-check release notes and the upstream watchlist before coding around a bug
- Work in small, testable steps
- Explain each file you add or change
- Prefer robust, maintainable structure over clever shortcuts
