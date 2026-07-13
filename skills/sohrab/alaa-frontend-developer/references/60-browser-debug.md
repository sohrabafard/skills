# Browser Debug and SSR-Safe UI Implementation

Use this file for the browser-debug decision flow, browser evidence collection, and SSR-safe UI implementation constraints.

Design ownership moved: UI design specs, state coverage, UX/accessibility design checks, visual style, tokens, motion, and design review now live in `$alaa-ui-ux-design-system`. Load that skill for any visual-design decision; this file keeps only the engineering side.

## When to open this file

- browser-based debugging after browser usage is allowed
- implementing a design in a way that must stay SSR-safe
- offline or update-facing UI changes that should not alter service-worker strategy

## SSR-aware UI rules

- avoid designs that require pre-hydration DOM measurement
- prefer CSS-driven initial layout over JavaScript-driven first render
- if client-only measurement is unavoidable, define:
  - the stable SSR placeholder
  - when hydration enhances it
  - how the transition avoids visible mismatch

When a proposed design violates these rules, negotiate the design with `$alaa-ui-ux-design-system` guidance rather than breaking SSR to honor it.

## Browser-debug decision flow

Only move to browser debugging when:

- the user explicitly asks for browser validation, or
- a higher-priority repo rule requires real-browser reproduction, or
- static analysis is no longer trustworthy for the bug

Before opening the browser:

- write the expected behavior
- write the observed failure
- define the target route or URL
- define success criteria

## Browser-debug evidence checklist

Capture the smallest useful proof:

- one relevant console or hydration warning
- one failing request or key response detail when network matters
- one DOM, ARIA, or visual capture showing the wrong UI

Then:

- write one short root-cause hypothesis
- define the smallest patch that could prove or disprove it
- rerun the smallest reproduction after the fix

## Pairing guidance

- UI design specs, state coverage, UX and accessibility design review:
  - Pair with `$alaa-ui-ux-design-system`
- exact Quasar component or layout choice:
  - Pair with `$alaa-quasar-app-vite-v3`
- browser execution:
  - Pair with `$playwright` or `$playwright-interactive`
  - If MCP browser profiles are configured, use `playwright_visual` for visual QA and headed inspection.
  - Use `playwright_headless` only for non-visual browser reproduction, console/network evidence, or deterministic smoke checks.
  - Do not use `MCP_DOCKER` only to obtain headless browser behavior when the Playwright headless profile exists.
