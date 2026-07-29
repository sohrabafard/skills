# Proof and Tests — the frontend delta

Test design, the layer taxonomy, doubles, flake handling and the six proof levels belong to
`/alaa-testing-strategy` (`$alaa-testing-strategy`). Read `references/40-proof-strength.md` there to pick
the level, `references/20-layers.md` for the layer, and `references/30-doubles.md` before writing a stub.
The Vue-shaped mechanics — mounting, stubbing a store, faking a port — belong to
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) `references/78-testing-binding.md`.

This file carries only what is true because the app renders on a server and hydrates in a browser.

## The gate

A change is done when the proof level selected for its surface has been run and its output recorded. A
repo with no runner for that level is a blocking finding reported to the maintainer, not a waiver, and not
a reason to fall back to "it looked right".

## A test that cannot fail proves nothing

Before a frontend test counts, write down the plausible broken implementation it would catch. A snapshot
of the rendered DOM that passes against a component returning an empty fragment is not a test. An
assertion that a spinner appeared is not an assertion that data arrived.

## Which surface needs which boundary

| The change is | The boundary that must be crossed in the proof |
|---|---|
| pure presentation, props in and markup out | component render, no server |
| anything that reads or writes a store, a composable, or a router guard | component render with the real store, doubles only at the network port |
| anything that renders differently on server and client | an SSR render plus a hydration pass — the only place a mismatch is observable |
| a submit path, an auth flow, a route transition, or an offline path | end to end against a running build |
| a service-worker change | end to end against the production build; a dev-server run proves nothing about a service worker |

## The hydration-mismatch assertion

The mismatch is a console warning, not a thrown error, so a test that only asserts on the final DOM will
pass over it. Assert on the absence of the warning: render on the server, hydrate the same markup, and
fail the test if Vue emitted a hydration warning. Without that assertion, `10-contract-and-boundaries.md`
gate 1 has no runner.

## Contract mocks

A double for a backend endpoint is only evidence if its shape came from the contract rather than from the
handler being tested. Take response and error shapes from `/alaa-services-contract`
(`$alaa-services-contract`) `references/60-frontend-sdk-consumption-contract.md`. A mock the author
invented tests the author's belief about the API.

## Determinism inputs

Freeze time, locale and timezone in every test that renders a formatted value; see
`55-i18n-locale-and-rtl.md`. A test that passes in one timezone and fails in another is reporting a
production defect, not a flaky test.

## What this file does not decide

Coverage numbers, flake policy, test naming, and how many levels a release needs:
`/alaa-testing-strategy` (`$alaa-testing-strategy`). What is verified manually and what evidence is
captured: `50-qa-and-verification.md`.
