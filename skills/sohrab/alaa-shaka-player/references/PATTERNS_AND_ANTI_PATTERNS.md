# Patterns and anti-patterns

Read this file before implementing or reviewing a player architecture.

## Good patterns

### Engine-first composition

- keep Shaka in a dedicated wrapper
- expose a thin app-facing API
- let Vue or Quasar render the product shell around that API

### Product modules outside the core

- ads, analytics, quiz logic, markers, and conductor code should consume player
  events and wrapper outputs rather than mutate core internals directly

### Version-aware implementation

- verify the current Shaka release and watchlist before pinning a version or
  implementing a workaround

### Repo-adaptive output

- match the host repo's file extensions, naming, and testing stack
- prefer `.js` plus JSDoc in JavaScript-first repos

### Mode-aware QA

- headless for behavior
- visual for presentation

## Anti-patterns

### Reactive player object

- never put the player instance into Vue `ref()` or `reactive()` state

### SSR leakage

- never import or initialize Shaka in code that runs on the server

### Monolithic player component

- do not mix networking filters, analytics heartbeats, ads, overlays, and
  watch-page UI into one component file

### App-level hacks before release check

- do not build custom fixes for live-HLS or FairPlay bugs without checking the
  current release notes and watchlist first

### UI-first misrouting

- do not spend time on visual polish when the task is really about retries,
  token refresh, or wrapper lifecycle correctness

### Behavior hidden in DOM state

- do not treat CSS classes, DOM measurements, or timer side effects as the
  source of truth for ad, quiz, or marker state
