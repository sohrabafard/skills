# QA and Verification

Use this file to define or run the smallest set of checks that gives high confidence for frontend changes.

## Risk model

Prioritize in this order:

1. SSR and hydration correctness
2. auth and protected-route behavior
3. critical user flows
4. PWA update and offline behavior
5. accessibility regressions
6. performance regressions on key routes

## Verification workflow

### 1. Discover available checks

- inspect the root `package.json`
- if a workspace package is touched, inspect the relevant `packages/*/package.json`
- do not invent commands; use the repo's real scripts

### 2. Select checks by change surface

- UI-only change:
  - lint and relevant tests if available
- SSR or hydration change:
  - add SSR build or equivalent hydration sanity check
- PWA or service-worker change:
  - add install, update, and offline smoke checks
- build, config, package, or deploy-affecting change:
  - add a full build and artifact-path checks

### 3. Run the smallest meaningful set first

- prefer targeted checks before full-suite checks
- if output is long, capture it to a repo-local artifact and summarize the key result
- if commands cannot run, provide a precise manual plan

### 4. Gate browser automation

- Browser automation is not the default frontend QA path.
- Use browser tooling only when the user explicitly asks for browser, Playwright, visual, or responsive validation; a higher-priority repo rule requires it; or static source/log/test evidence is no longer trustworthy for a browser-only bug.
- When the browser is not allowed, rely on source inspection, tests, logs, static DOM/CSS reasoning, and already-provided screenshots or artifacts.
- Before opening the browser after a static pass, state the target route or URL and the success criterion.

## Mandatory SSR and hydration checks

- no SSR crashes on first load
- no hydration warnings in the browser console
- no client-only branch causing different initial DOM
- no repeated API calls caused by SSR/client drift
- stable list keys and stable formatted output

## PWA checks

- install / first load works without service-worker errors
- update flow triggers exactly one reload and loads latest assets
- offline navigation shows the intended fallback without loops
- allowed runtime cache entries appear only where expected

## Accessibility smoke

- keyboard navigation across primary flows
- dialog, drawer, and menu focus behavior
- form labels, helper text, and errors are understandable
- visible controls remain reachable at the intended viewport sizes

## Evidence to capture

Prefer the smallest evidence set that proves the result:

- command and exit code
- one or two key output lines for failures
- screenshot or console evidence when a browser check matters
- explicit note of what was not run and why

## Release-readiness check

Before calling a task done, confirm:

- the changed path works
- the original failure path no longer fails
- no new SSR, PWA, or asset-contract regressions were introduced
- the verification performed is proportional to the risk of the change

## Pairing guidance

- Browser execution or UI evidence collection:
  - Pair with `$playwright` or `$playwright-interactive`
  - If MCP browser profiles are configured, use `playwright_headless` for deterministic headless smoke checks, console checks, snapshots, and non-visual reproductions.
  - Use `playwright_visual` for headed visual QA, screenshot review, layout inspection, responsive checks, and anything where seeing the rendered page matters.
  - Do not route to `MCP_DOCKER` only because the check is headless; reserve it for Docker-specific isolation or Docker MCP features.
- Service-worker runbook changes:
  - Also load `30-pwa-sw-and-offline.md`
- Performance-sensitive verification:
  - Also load `40-performance-and-realtime.md`
