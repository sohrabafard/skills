# Async and failure — the Vue binding

**`/alaa-reliability-sla` (`$alaa-reliability-sla`) owns this doctrine**: deadlines and timeouts, retry
counts and backoff shape, retry budgets, breakers, bulkheads, shedding, degradation, and the idempotency
contract. **`/alaa-services-contract` (`$alaa-services-contract`) owns every number** — the timeout value,
the retry ceiling, the pool bound. This file states only where the Vue code that obeys them lives, and it
states no number.

Read it before writing `await` in a component or composable, an `AbortController`, a submit handler, a
`catch` block, or anything named `retry`.

## Where each concern lives

| Concern | Its only home in a Vue app |
|---|---|
| Retry, backoff, timeout | The transport adapter or the HTTP client's interceptor chain |
| Abort signal creation and disposal | The composable that owns the request's lifetime |
| In-flight dedupe by action key | The composable or store action that exposes the verb |
| Failure classification | A pure policy module with no Vue import, unit-testable without a network |
| User-facing wording for a failure | The UI edge — a Notify or Dialog call in a component or a UI facade |

**A retry never lives in a component, a template, or a store action.** A component that retries has two
retry policies the moment the transport layer gains one, and neither is visible to the other: the effective
attempt count becomes the product of the two, and no operator can predict it during an incident.

## What a composable exposing an async verb must expose

Every one of these, or the surface is incomplete:

- an in-flight indicator that is true for the whole window, from before the request starts to after
  `finally` runs;
- the failure, in a typed domain-error shape — not the caught value, not a string;
- a way to cancel, wired to the same `AbortController` the request used;
- a result or state the caller can branch on exhaustively, which in practice means the `AsyncState<T>` union
  in `22-typescript-type-system.md`.

## Cancellation and the stale-response race

Create the `AbortController` in the composable that owns the request's lifetime. Abort it on unmount, and
abort the previous one before starting a replacement request for the same logical query.

Without this, the slower of two in-flight requests wins, and the user sees results for a search they have
already changed. The symptom is intermittent and does not reproduce on a fast connection, which is why the
rule is structural rather than something to test for.

An abort is not a failure: `if (isAbortError(error)) return` comes first in every `catch`, before any state
is written, so a cancelled request never sets an error state the user sees.

## Double-fire safety

`SKILL.md` states the invariant. Its shape here:

- One pending promise per action key, held by the composable that owns the verb. A second call with the same
  key returns the pending promise or is refused; it does not start a second request.
- The trigger is disabled for the whole in-flight window and re-enabled only in `finally`, so it is
  re-enabled on the failure path too.
- Whether the request also carries an idempotency key, and what that key contains, is
  `/alaa-reliability-sla` (`$alaa-reliability-sla`). Do not invent one.

The disabled trigger alone is not sufficient: a fast double-click can land before the disable renders. The
dedupe is the mechanism, and the disable is the affordance.

## Failure classification before any fallback

Classify before you fall back, in a pure module. The binding: a **definitive denial** surfaces a message and
does not apply the local mutation, does not retry, and never resolves as success; a **transient transport
failure** may take the degraded path the owner defines. Which codes are which is
`/alaa-reliability-sla` (`$alaa-reliability-sla`); that a denial is a security event and not a transport
event is `/alaa-security-review` (`$alaa-security-review`).

The reason the classification module is Vue-free: it must be provable at unit level with the response as
input, and a policy that can only be exercised by mounting a component is a policy nobody tests.

## Teardown guards on every exposed surface

**Every async surface a composable exposes fails closed after scope disposal — the read controllers as well
as the action controllers.** An `execute` or `refresh` called after `scope.stop()` rejects or returns
without touching the network; a `reset` or `abort` becomes a no-op. A retained reference outliving the
component is normal in a keep-alive route or a captured callback, and the failure it produces — a request
against a disposed scope writing into refs nobody renders — is invisible in development.

The test that proves it: call `scope.stop()`, then call each exposed function, and assert no transport call
was made. `78-testing-binding.md` states the proof level.

## Error surfacing

Errors surface through Quasar Notify or Dialog only at UI edges, never from inside a service or an adapter.
A service that notifies cannot be reused in a background flow, cannot be tested without a Quasar install,
and produces duplicate toasts as soon as two callers exist.

What is logged or reported when a failure happens, and with which correlation identifier, is
`74-observability-binding.md`.
