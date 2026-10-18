# Verification and Release

The smallest set of checks that gives high confidence for a frontend change, the evidence it produces, and
what must be written down when it ships.

Which proof level a surface requires, and how tests are designed, is `/alaa-testing-strategy` `references/40-proof-strength.md`; the frontend delta is
`05-proof-and-tests.md`.

## Risk order

SSR and hydration correctness; auth and protected-route behaviour; critical user flows; PWA update and
offline behaviour; accessibility regressions; performance regressions on key routes.

## Workflow

1. **Discover the real checks.** Read the root `package.json`, and the relevant `packages/*/package.json`
   when a workspace package is touched. Do not invent a command.
2. **Select the proof level from `/alaa-testing-strategy` for the change
   surface and run it.** If the repo has no runner for that level, that is a blocking finding reported to
   the maintainer — not a waiver, and not a reason to substitute a weaker check.
3. **Run the smallest meaningful set first.** Targeted before full-suite. Capture long output to a
   repo-local artifact and summarize the deciding line.
4. **When a command cannot run, write the manual plan** — exact route, exact action, exact expected
   result — rather than asserting the change is fine.

## SSR and hydration checks

| Applies when | Required proof |
|---|---|
| SSR exists and the change affects server render, initial markup/data, boot, routing, auth or locale/timezone output | No first-load crash; no hydration warning or client-only initial-DOM drift; no duplicate SSR/client request; stable list keys; affected formatted output stays deterministic across timezones (`55-i18n-locale-and-rtl.md`). |

Select proof for the changed surface through `05-proof-and-tests.md`. A static-only change with no
affected SSR path does not trigger these runtime checks; an owed check with no runner remains blocked.

## Service-worker verification

When PWA exists and a change affects its worker, registration, cache/asset base, update flow or offline
behavior, run `alaa-quasar-app-vite-v3 references/75-testing-ci-playbook.md` section 3: automated regressions
and the complete manual runbook. It owns applicability and scenarios; use the production build.

## Accessibility smoke

Keyboard navigation across the primary flow; focus behaviour in dialogs, drawers and menus; labels,
helper text and errors that make sense read aloud; every visible control reachable at the intended
viewport sizes. The full design and accessibility gates are `/alaa-ui-ux-design-system` `references/85-accessibility-patterns.md` and
`references/90-quality-gates-and-review.md`.

## Evidence

The smallest set that proves the result: the command and its exit code; one or two deciding output lines
on failure; a console or network capture when a browser check mattered; and an explicit note of what was
not run and why. Browser evidence discipline is `60-browser-debug.md`.

## Release readiness

Before calling a task done: the changed path works; the original failure no longer reproduces; no new
SSR, PWA, asset-contract or budget regression; and the verification performed is proportional to the risk.

## The release note

Every change that reaches a user ships with three sentences, in the merge request body and in whatever
release record the repo keeps:

1. **What shipped** — the user-visible behaviour that is now different, named by route or component.
2. **How it is operated** — the configuration values it reads, the flag that gates it, and what an
   operator must do to turn it off (`48-config-and-environment.md`).
3. **How it fails** — the degraded states it can enter and what the user sees in each
   (`46-resilience-and-degradation.md`), plus the signal that shows it failing
   (`47-frontend-observability.md`).

A change that cannot answer the third sentence has not been designed for failure, which is a finding
before it is a documentation gap. Annotation-level documentation inside the code is
`/alaa-frontend-doc-annotations`
`references/10-annotation-boundaries.md`.

## Pairing

Browser execution and profile choice: `70-companion-skill-routing.md`. Service-worker policy:
`30-pwa-sw-and-offline.md`. Performance measurement: `41-lighthouse-and-web-vitals.md`.
