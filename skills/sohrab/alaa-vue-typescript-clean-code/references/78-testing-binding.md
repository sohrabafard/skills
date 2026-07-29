# Testing — the Vue binding

**`/alaa-testing-strategy` (`$alaa-testing-strategy`) owns test design**: what makes a test a test rather
than a replay of the happy path, which layer a behaviour belongs at, when to fake or stub or use the real
dependency, the six proof levels and which one a claim requires, and telling a flaky test from an
intermittent defect. This file states only which Vue artifact sits at which level, and what a test of each
artifact must fail on.

Read it before creating a `.spec.ts`, mounting a component, stubbing a store, faking a port, or claiming a
behaviour is proven.

## Where each Vue artifact sits

| What is being claimed | Level | The Vue shape |
|---|---|---|
| A mapper, formatter, validator, or failure-classification module is correct | 2 — unit | Plain function test, no Vue import, no mount |
| A composable's state transitions, guards, and teardown are correct | 2 — unit | Call it inside an `effectScope`, drive it directly, no component |
| A store's actions and derived state are correct | 2 — unit | `createTestingPinia` or a fresh Pinia, with the transport port faked |
| A component renders the right thing for a given state, and emits the right intent | 2 — unit | Vue Test Utils mount with props and a faked port; assert on emitted events and rendered text |
| A composable behaves correctly when its dependency times out, refuses, or answers wrongly | 2, with the fault injected at the port | The fake returns the failure; assert the classified outcome |
| A fake port behaves like the real adapter | 3 — parity | The same contract test runs against fake and adapter |
| A route, guard chain, and boot wiring behave in the shape they are deployed in | 5 — in-runtime | The app mounted with its real router and boot files |

A claim about anything the browser itself decides — layout, focus order, service-worker install, offline
behaviour — is not proven by a JSDOM mount. State the level you reached and what remains unproven;
`/alaa-testing-strategy` (`$alaa-testing-strategy`) owns the escalation rule, and browser verification is
`/alaa-frontend-developer` (`$alaa-frontend-developer`).

## What a composable's test must fail on

A test that passes against a broken implementation is not evidence. Every composable that ships carries a
test that **fails when the corresponding line is removed**:

- Remove the `onUnmounted` cleanup — the test fails. Assert the listener, timer, observer, or subscription
  is gone after unmount, not that some flag was set.
- Remove the teardown guard — the test fails. `scope.stop()`, then call every exposed function, and assert
  no transport call was made (`70-async-and-failure-binding.md`).
- Remove the abort on replacement — the test fails. Start two requests, resolve them out of order, and
  assert the stale one does not write state.
- Remove the in-flight dedupe — the test fails. Call the verb twice synchronously and assert exactly one
  transport call.
- Remove the failure classification — the test fails. Inject a definitive denial and assert no local
  mutation was applied.

Proving a control by removing it is the general rule and it belongs to
`/alaa-testing-strategy` (`$alaa-testing-strategy`); the five above are the Vue surfaces where it is not
optional, because each of them has shipped broken.

## Doubles at the Vue seams

Fake at the port the consumer defined, not at the library. A fake implementing your three-method `CourseApi`
is honest and short; a mocked Axios instance is a second implementation of Axios that drifts from the real
one, and its drift is invisible until production.

- Inject through the typed injection key or a parameter (`44-creational-and-async-idioms.md`). If a test
  needs to reach into module internals to substitute a dependency, the seam is missing — that is a design
  finding, not a test problem.
- Stub a child component only to isolate what you are asserting, never to make a failing assertion pass.
- Use fake timers for debounce and throttle tests, and advance them explicitly; a test that waits on a real
  interval is the flake you will chase later.
- A test that mounts the whole page to assert one formatting rule is testing at the wrong layer and will
  break for reasons unrelated to its claim.

## Reporting a test result

Report the command, the working directory, and the observed outcome, at the level that actually ran. A
claim reported at a level that was not reached is worse than no claim, because it removes the reviewer's
ability to decide whether to re-run it.

If a level is unreachable in this environment — no browser, no live service — say which level was reached,
which claim is therefore unproven, and what blocks it. `60-validation-gates.md` owns the command set.
