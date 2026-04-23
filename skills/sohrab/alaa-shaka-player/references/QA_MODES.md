# QA modes

Choose the lightest reliable validation mode for the user's actual request.

## Headless mode

Use headless validation when the task is mainly about:

- manifest load success
- request or response filters
- token refresh and retry behavior
- analytics heartbeat cadence
- player wrapper events
- cleanup and teardown integrity
- playlist or conductor logic

Preferred evidence:

- emitted event sequence
- targeted network traces
- logged retry or auth-refresh outcomes
- assertions on wrapper state or emitted callbacks

Do not default to a visual browser run if the user only needs API, retry, or
event correctness.

## Visual mode

Use visual browser validation when the task is mainly about:

- control layout or hierarchy
- captions readability
- overlays, quizzes, and marker popovers
- ad rendering and resume behavior
- loading, empty, and error states
- responsive breakpoints
- keyboard, focus, touch, or remote-control behavior

Preferred evidence:

- screenshots
- viewport-by-viewport notes
- accessibility and focus observations
- before or after comparisons for layout-sensitive fixes

## Companion skill routing

- Browser mechanics: pair with `$playwright` or `$playwright-interactive`
- Repo-safe Vue or Quasar implementation: pair with `$alaa-frontend-developer`
- Premium UI or stronger watch-page art direction: keep this skill focused on playback, frontend implementation, accessibility, responsiveness, and QA constraints; treat pure art direction as outside the Sohrab pack unless a separate design skill is explicitly available in the session.

## Anti-patterns

- doing a full visual pass when the bug is purely in request filters or analytics
- concluding event correctness from a screenshot alone
- skipping visual QA after changing caption layout, overlay stacking, or control spacing
