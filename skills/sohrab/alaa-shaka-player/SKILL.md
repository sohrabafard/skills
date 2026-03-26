---
name: alaa-shaka-player
description: "Use this skill when a task involves production Shaka Player work in Vue 3 + Quasar + Vite, including playback architecture, HLS or DASH, DRM, ads, overlays, analytics, or migration from another player. Do not use it for simple MP4-only playback or non-Vue stacks."
---




# Alaa Shaka Player

## Purpose

Use this skill to design, migrate, implement, review, or debug a production-grade
Shaka Player integration in Vue 3 + Quasar + Vite applications.

The default thesis is:

- Shaka is the playback engine.
- Vue + Quasar is the UI and product shell.
- Analytics, ads, overlays, markers, and conductor logic stay outside the core.

This keeps playback changes testable, UI work replaceable, and operational
failures easier to localize.

## Ownership and pairing

- `alaa-shaka-player` owns playback-engine architecture, Shaka-specific config,
  streaming and DRM caveats, player-module boundaries, and player-specific QA.
- Pair with `$alaa-frontend-developer` for SSR and hydration safety, browser-only
  guards, repo-safe Vue or Quasar implementation, API-shaping implications, and
  app-family conventions.
- Pair with `$frontend-skill` when the user asks for a premium or art-directed
  player shell, richer watch-page composition, stronger control hierarchy,
  poster or empty-state design, or broader UI or UX polish.
- Pair with `$playwright` for browser execution. Prefer headless runs for event,
  API, retry, analytics, and networking validation; prefer visual mode for
  layout, captions, overlays, ads, accessibility, focus states, and responsive
  QA.
- Use `$alaa-low-noise` when the task spans many player files, noisy logs, or a
  large browser matrix.
- Use `$openai-docs` only when the task is about Codex or OpenAI maintenance,
  skill authoring guidance, or workflow upgrades. Do not use it as the source of
  truth for Shaka behavior.

## Upstream baseline

As of **2026-03-26**:

- The Shaka Player releases page shows `v5.0.8` and `v4.16.24`, both released on
  **2026-03-23**.
- Recent fixes include HLS DTS and DTS-HD codec variant support, prevention of
  infinite manifest update delay, more tolerant duplicate segment detection, and
  several HLS, DASH, VTT, networking, and GC-pressure improvements.
- Open pull requests worth tracking for future skill updates:
  - `#9896` adds `BufferBasedAbrManager` for low-latency live streams
  - `#9864` addresses duplicate segment downloads during stream switching
  - `#9795` fixes FairPlay polyfill behavior for Safari `src=` playback

Do not hard-code `5.0.3` in new work. For version-sensitive tasks, always read
`references/UPSTREAM_WATCHLIST.md` before choosing a pinned version or
recommending a workaround.

## When to use

Use this skill when:

- You are migrating from Video.js or another player wrapper to Shaka.
- Your stack is Vue 3 + Quasar + Vite.
- HLS is primary, or DASH is present as a secondary or DRM path.
- The player needs one or more of:
  - adaptive bitrate and manual quality override
  - subtitles or alternate audio
  - FairPlay, Widevine, or other DRM integration
  - VAST or VMAP ads
  - watch-time analytics or QoE telemetry
  - quiz overlays, cuepoints, or timeline markers
  - playlist or schedule-driven playback
  - TV, set-top-box, or remote-control behavior

## When NOT to use

- A plain `<video>` tag is enough.
- The task is MP4-only with no engine-level streaming control.
- The project is not Vue 3 + Quasar + Vite.
- The real need is visual polish only and the playback engine is already settled.

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Apply `$alaa-low-noise` if the task is non-trivial.
3. Pair with `$alaa-frontend-developer` for any real implementation task in a
   Vue or Quasar app.
4. Read `references/README.md`.
5. Read `references/ARCHITECTURE.md` and
   `references/PATTERNS_AND_ANTI_PATTERNS.md`.
6. Read only the specialized references you actually need:
   - `HLS_NOTES.md`
   - `ABR_AND_TRACKS.md`
   - `ADS_VAST_VMAP.md`
   - `ANALYTICS_WATCHTIME.md`
   - `QUIZ_OVERLAY.md`
   - `TIMELINE_MARKERS.md`
   - `PLAYLIST.md`
   - `CONDUCTOR_SCHEDULE.md`
   - `TROUBLESHOOTING.md`
   - `QA_MODES.md`
   - `UPSTREAM_WATCHLIST.md`

## Inputs to collect before implementation

Collect these inputs before locking the architecture:

1. Playback inventory
   - HLS VOD
   - HLS live
   - DASH, if any
   - external text tracks
   - multiple audio tracks
   - DRM scheme and provider requirements

2. Platform matrix
   - Chrome, Edge, Firefox
   - Safari macOS
   - iOS Safari
   - Android Chrome or WebView
   - WKWebView, STB, or TV platforms, if relevant

3. Product feature inventory
   - Ads: VAST, VMAP, preroll, midroll, postroll
   - Quiz: required or optional, seek policy, scoring
   - Markers: notes, comments, bookmarks, deep links
   - Playlist or schedule-driven playback
   - analytics heartbeat contract and backend endpoints

4. Operational constraints
   - startup latency and rebuffer tolerance
   - mobile memory budget
   - token refresh and signed URL policy
   - retry and fallback policy
   - observability and incident-debug expectations

## Output expectations

The implementation should usually produce some combination of:

- a small player component such as `ShakaPlayer.vue`
- a non-reactive core wrapper such as `useShakaCore`
- separate services for analytics, ads, overlays, markers, or conductor logic
- a lab page or isolated demo surface for fast iteration
- a migration plan and QA checklist

Adapt names and file extensions to the host repo:

- Prefer `.js` plus JSDoc if the repo is JavaScript-first.
- Use `.ts` only if the repo already uses TypeScript or the user asks for it.

Do not force the example file names or TypeScript into a repo that does not use
them.

## Non-negotiable rules

1. Use the current basic usage shape.
   - Prefer `new shaka.Player()` and `await player.attach(videoEl)`.
   - Install polyfills before support checks.

2. Keep Shaka out of Vue reactivity.
   - Use a plain variable, closure state, or `markRaw` only if needed.
   - Never store the player inside reactive `ref()` or `reactive()` state.

3. Keep browser-only logic client-side.
   - Dynamically import Shaka in client code.
   - Initialize in `onMounted()` or another client-only path.
   - Never access media APIs during SSR.

4. Destroy aggressively and completely.
   - Destroy the player on unmount or route leave.
   - Remove listeners, timers, observers, and polling.
   - Abort outstanding app-level work.

5. Keep networking auth and retries explicit.
   - Register filters before `load()`.
   - Since request filters run on every attempt in v5.x, use that to refresh
     expired credentials safely.

6. Treat ads and product logic as optional modules.
   - Do not bury ad or analytics state inside the core wrapper.
   - A failed ad flow must not permanently block content playback.

7. Do not assume the latest issue discussion is already fixed.
   - Re-check current release notes before carrying forward a workaround.

## Recommended architecture

### Layer 1: Core playback wrapper

Responsibilities:

- dynamically import Shaka
- install polyfills
- check browser support
- create and attach the player
- register networking filters
- configure DRM, buffering, and telemetry hooks
- load sources
- forward errors, retries, and stats
- manage lifecycle and cleanup

This belongs in a wrapper such as `useShakaCore`.

### Layer 2: Product feature modules

Keep these separate from the playback core:

- `AnalyticsTracker`
  - watch-time heartbeat
  - interaction telemetry
  - QoE snapshots

- `QuizEngine`
  - cuepoint-driven quiz logic
  - pause and resume policy
  - seek policy enforcement

- `TimelineMarkers`
  - notes
  - comments
  - bookmarks
  - share links

- `PlaybackConductor`
  - schedule-based playback
  - wall-clock source switching
  - playlist fallback

- `AdsManager`
  - ad container setup
  - ad request orchestration
  - preroll, midroll, postroll handling
  - timeout and fail-open recovery

### Layer 3: UI layer

Use Vue + Quasar for:

- playback controls
- subtitles and track menus
- overlays
- marker interaction
- quiz flows
- stats and debug panels

If the user asks for a high-end watch experience, pair with `$frontend-skill`
instead of overloading the core wrapper with visual decisions.

## QA mode selection

Pick the lightest reliable QA mode for the request:

- API, event, retry, heartbeat, and auth-filter verification:
  use headless validation first
- controls layout, overlays, ad rendering, captions, focus, and breakpoints:
  use visual browser validation

Read `references/QA_MODES.md` before testing if the mode is not obvious.

## Multi-agent guidance

If multi-agent mode is explicitly enabled, split by concern:

- core
- ads
- analytics
- overlay
- conductor
- QA
- visual design, only when UI or UX polish is in scope

Keep roles narrow and merge results into one coherent architecture instead of
letting each agent invent its own player shape.

See:

- `prompts/MULTI_AGENT_PROMPT.md`
- `references/MULTI_AGENT_SETUP.md`
- `assets/config-examples/`

## Default implementation order

Follow this order unless the repo forces a different sequence:

1. verify current Shaka release and watchlist notes
2. create a safe lab page or isolated harness
3. implement the core wrapper
4. implement the player component
5. add a migration flag or adapter layer if replacing an old player
6. add analytics and track controls
7. add overlays and markers
8. add ads
9. add conductor or playlist logic
10. run the QA checklist
11. roll out gradually

## Skill file map

- `prompts/`
  - ready-to-use prompts for single-agent and multi-agent runs
- `references/`
  - targeted architecture, QA, and upstream runbooks
- `assets/templates/`
  - code templates
- `assets/config-examples/`
  - example multi-agent role configs
- `scripts/scaffold.sh`
  - helper to copy starter templates

## Installation note

This skill is distributed as a standalone folder. Keep it in a Codex-discoverable
skills location, typically `~/.codex/skills/alaa-shaka-player` or a repo-local
skills directory.

See `INSTALL.md` for concrete placement examples.
