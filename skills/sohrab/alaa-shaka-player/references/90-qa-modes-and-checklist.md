# QA modes and the player checklist

Test design, the six proof levels, doubles, flake and what counts as evidence are owned by
`/alaa-testing-strategy` (`$alaa-testing-strategy`). This file states only which **player** facts each
mode can prove and what a player change must exercise.

## Mode selection

Pick the lightest mode that can actually prove the claim.

| Mode | Proves | Cannot prove |
|---|---|---|
| **Unit** (`vitest`, no browser) | Pure policy: the config builder and its range validation (`15-…`), track-row mapping (`26-…`), the QoE derivation and its `NaN` guards (`60-…`), the TTL assertion (`42-…`), schedule boundary selection (`37-…`) | Anything involving MSE, EME or a real network |
| **Component** (`@vue/test-utils` + a fake player) | Lifecycle ordering, teardown completeness, run-token behaviour on a fast source change, that the error path reaches the UI | Real playback |
| **Headless browser** (`/playwright`, `$playwright`) | Emitted event sequence, filter behaviour and per-attempt refresh, retry counts, teardown integrity, `getStats()` shape, offline `store()` flow | Anything visual |
| **Visual browser** (`/playwright`, `$playwright`) | Control layout, caption readability and position, overlay stacking, ad chrome, focus order, breakpoints, remote-control navigation | Event correctness |
| **Real device** | iOS Safari load mode, FairPlay, TV `stallSkip` behaviour, persistent-licence support | – |

A screenshot never proves event correctness, and an event log never proves caption readability.

## The eight failure scenarios every player change must survive

From `35-unstable-networks-and-resilience.md`. A player change that touches config, filters or the
error path proves all eight; one that touches only a menu proves the two that its area can break.

1. Manifest 404 → the load promise rejects and the UI shows a mapped message (not a raw code).
2. Segment 5xx mid-playback → retried within budget; playback resumes; the counter resets on `loaded`.
3. Segment timeout at low bandwidth → `stallTimeout`/`connectionTimeout` abandon the request rather
   than hanging until `timeout`.
4. Licence 401 mid-session → the request filter refreshes on the **retry attempt**, not on the next
   user action.
5. Device offline then online → **exactly one** `retryStreaming()` fires (Shaka's own listener), not two.
6. Every variant disabled by HTTP errors → the fatal `HTTP_ERROR` is handled, not swallowed.
7. `QUOTA_EXCEEDED_ERROR` (3017) on a long session → buffer settings recover it.
8. `VIDEO_ERROR` (3016) → MediaSource recovery fires and `mediasourcerecovered` is observed.

## Browser and device matrix

Chrome · Edge · Firefox · Safari macOS · **iOS Safari (its own row, always)** · Android Chrome ·
Android WebView (if shipped) · WKWebView (if shipped) · each TV or console target actually shipped to.

iOS Safari is not covered by Safari macOS: different load mode, different DRM, different text
capability, different preload behaviour (`75-platform-and-browser-matrix.md`).

## Functional checklist

**Playback** — load · play · pause · seek · replay · playback rate · start offset through
`updateStartTime` · trick play forward and back with `cancelTrickPlay` reached on every exit path.

**Tracks** — quality menu populated and manual selection sticks with ABR disabled · audio switch via
`selectAudioTrack` (**not** `selectAudioLanguage`) · subtitle on/off via `selectTextTrack` (**no**
`setTextTrackVisibility`) · **the user's audio and subtitle choice survives the next `load()`** ·
preference fallback order honoured.

**Text** — side-loaded track appears and is selectable · correct behaviour on live (4033 handled) and
in `src=` mode (2012 / 2013 handled) · `subtitleDelay` applies · caption size and position controls
reach the displayer actually in use.

**Network** — throttled bandwidth · token expiry mid-session · full interruption and recovery ·
signed-URL renewal inside the request filter · the eight scenarios above.

**DRM** — each key system on its supported browsers · server certificate present for FairPlay ·
licence wrapping round-trips · expiry surfaces through `getExpiration()` / `expirationupdated`.

**Offline** — capability probe · `navigator.storage.persist()` requested and its result recorded ·
track selection narrows the download · progress reported · abort works · quota refusal (9014) shows a
message · list distinguishes `isIncomplete` · playback of a stored asset with the network off ·
removal releases the licence.

**Ads** — pre-roll, mid-roll, post-roll · ad-playing state reaches the skin · skip button state from
`IAd` · **the watchdog resumes content when no ad arrives** · content resumes after every ad path.

**Live** — DVR window recomputed on `manifestupdated` · `goToLive()` · latency within the configured
tolerance · behaviour when the playhead falls out of the window.

**Analytics** — quantities emitted match `getStats()` · `NaN` fields are `null`, never `0` · a
snapshot is flushed on `unloading` and on `pagehide` · every wire name traced to
`/alaa-services-contract` (`$alaa-services-contract`) · an idempotency key is present.

**Lifecycle** — route change · repeated mount/unmount · timer cleanup · listener cleanup · no memory
growth across ten mounts · no network activity after unmount.

**Visual** — loading, empty and error states · control contrast and hit targets · caption readability
· overlay stacking and dismissal · keyboard and remote navigation · RTL layout with
`showMenusOnTheRight`. Design acceptance is `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`),
`references/90-quality-gates-and-review.md`.

## What "verified" means for a player change

A claim of verification names the mode, the scenario and the observation. "Tested in Chrome" is not a
claim. `/alaa-testing-strategy` (`$alaa-testing-strategy`), `references/80-evidence-and-reporting.md`
owns the reporting form; the player-specific minimum is:

- the emitted event sequence for the scenario, or the screenshot for a visual claim;
- the `getStats()` snapshot at the moment of interest;
- the Shaka error **code** for any failure path exercised;
- the browser and the value of `player.getLoadMode()` at the time.

**Best practice.** Run `scripts/check-shaka-api.mjs` in CI on every change that touches player code.
It costs one process and catches the class of bug — a call to an API removed two majors ago — that no
amount of visual QA finds, because an optional-chained removed method produces no error at all.
**Common mistake.** Doing a full visual pass when the defect is in a request filter, or concluding
event correctness from a screenshot. Both waste the expensive mode on a claim it cannot prove.
