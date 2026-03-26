# Architecture

## Design goal

Keep the Shaka integration understandable and maintainable by separating:

1. **Core playback engine**
2. **Product feature modules**
3. **UI layer**

This prevents the player wrapper from turning into an untestable monolith.

## Core playback layer

The core wrapper should do only the following:

- dynamically import Shaka
- install polyfills
- check browser support
- create the player
- attach it to the `<video>` element
- configure networking filters
- load sources
- expose errors and stats
- destroy cleanly

Recommended file:
- `useShakaCore.ts`

## Product feature modules

Each feature should be its own service or module.

### AnalyticsTracker
Owns:
- watch-time accumulation
- heartbeat cadence
- interaction event tracking
- QoE snapshots

### QuizEngine
Owns:
- cuepoint detection
- pause/resume logic
- quiz display hooks
- seek policy

### TimelineMarkers
Owns:
- notes
- comments
- bookmarks
- share timestamps
- marker lookup and persistence helpers

### PlaybackConductor
Owns:
- schedule evaluation against wall-clock time
- source switching
- offset mapping
- playlist fallback logic

### AdsManager
Owns:
- ad container setup
- ad request orchestration
- ad state transitions
- ad timeout and recovery

## UI layer

Use Vue + Quasar for:

- playback controls
- dialogs
- overlays
- stats panels
- marker interaction
- quiz flows

The UI layer should consume events and state from the core wrapper and feature
modules rather than embedding business logic in the template.

## Suggested in-app file structure

```text
src/
  components/player/
    ShakaPlayer.vue
  composables/player/
    useShakaCore.ts
  services/player/
    AnalyticsTracker.ts
    QuizEngine.ts
    TimelineMarkers.ts
    PlaybackConductor.ts
    AdsManager.ts
  pages/
    PlayerLabPage.vue
```

Adapt extensions and naming to the host repo. If the project is JavaScript-first,
use `.js` plus JSDoc rather than forcing `.ts`.

## Migration note

If you are migrating from Video.js, keep a temporary adapter or feature flag so
you can roll out the Shaka version safely instead of doing a hard cutover.
