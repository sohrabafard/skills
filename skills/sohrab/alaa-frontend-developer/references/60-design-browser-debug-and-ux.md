# Design, Browser Debug, and UX

Use this file for repo-safe UI design specs, state coverage, accessibility, responsive behavior, and browser-debug decision flow.

## When to open this file

- new screen or flow design
- UI redesign with implementation constraints
- accessibility or responsive review
- browser-based debugging after browser usage is allowed
- offline or update-facing UI changes that should not alter service-worker strategy

## Implementation-safe design deliverables

Define:

- information architecture
- component plan
- state coverage:
  - default
  - hover
  - active
  - disabled
  - loading
  - error
  - empty
  - partial-data when relevant
- responsive behavior
- accessibility expectations
- short, implementable copy
- edge cases for slow network, offline, long content, and partial data

## SSR-aware UI rules

- avoid designs that require pre-hydration DOM measurement
- prefer CSS-driven initial layout over JavaScript-driven first render
- if client-only measurement is unavoidable, define:
  - the stable SSR placeholder
  - when hydration enhances it
  - how the transition avoids visible mismatch

## Concrete UX and accessibility checks

- headings and landmarks are meaningful
- keyboard flow is explicit
- dialogs, drawers, and menus have clear focus entry and exit
- form labels, helper text, and errors are associated correctly
- motion does not hide state changes or create layout thrash
- responsive specs mention overflow, truncation, spacing, and tap targets

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

- strong visual thesis or art direction:
  - Keep this skill focused on frontend implementation constraints; treat pure art direction as outside the Sohrab pack unless a separate design skill is explicitly available in the session.
- exact Quasar component or layout choice:
  - Pair with `$quasar-skill-packe`
- browser execution:
  - Pair with `$playwright` or `$playwright-interactive`
