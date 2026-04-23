# Multi-agent prompt

Use this prompt when multi-agent mode is enabled and the task benefits from
parallel work.

Spawn one agent per track, wait for all of them, then consolidate the results
into a single implementation plan and file set.

Before spawning, verify the current Shaka release and open watchlist items so
agents do not build on stale assumptions.

## Agent tracks

1. **Core agent**
   - Implement the Shaka core wrapper
   - Handle attach, load, destroy, networking filters, and stats

2. **Ads agent**
   - Design an IMA-based ad manager
   - Support VAST and VMAP
   - Add pre-roll, mid-roll, post-roll, and fail-safe recovery

3. **Analytics agent**
   - Design watch-time heartbeat logic
   - Track user interactions
   - Capture QoE metrics and error reporting

4. **Overlay agent**
   - Implement quiz cuepoint logic
   - Implement timeline marker data flow and UI hooks

5. **Conductor agent**
   - Implement a TV-like playback conductor
   - Support wall-clock scheduling and source switching
   - Add sequential playlist fallback

6. **QA agent**
   - Build a browser and device test matrix
   - Split checks into headless API or event coverage and visual UI coverage
   - Focus on lifecycle leaks, route changes, Safari or iOS, STB platforms, and edge cases

7. **Visual design agent**
   - Only create this track when UI or UX polish is explicitly requested
   - Improve controls hierarchy, overlay behavior, empty states, and responsive composition
   - Keep visual decisions tied to concrete playback, accessibility, responsiveness, and frontend implementation constraints instead of inventing generic control bars

## Consolidated output
Return:

- a unified architecture
- a file tree
- the code files or templates
- a migration plan
- a QA checklist
- a rollout strategy
