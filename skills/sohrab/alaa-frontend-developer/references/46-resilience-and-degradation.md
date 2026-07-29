# Resilience and Degradation — the client-side expression

The doctrine is not here. Deadlines, retry budgets, breakers, bulkheads, load shedding, degradation modes
and idempotency all belong to `/alaa-reliability-sla` (`$alaa-reliability-sla`):
`references/10-deadlines-and-timeouts.md`, `references/20-retries.md`,
`references/30-breakers-and-bulkheads.md`, `references/50-degradation.md`,
`references/60-idempotency.md`. Take the values from there. The Vue-shaped async and failure mechanics are
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`)
`references/70-async-and-failure-binding.md`.

This file states what a browser client must do so those policies are actually in force.

## Every request carries a deadline

A `fetch` with no timeout inherits the browser's, which is minutes. Attach an `AbortSignal` with the
deadline for that call class, from the reliability skill's table, and treat the abort as a first-class
outcome with its own UI state — not as an error the user reads as "something went wrong".

A deadline that is not configurable is a constant recompiled into the bundle; put the value where
`48-config-and-environment.md` can validate it at boot.

## Mutations carry an idempotency key

A create, a submit, a payment or any other non-repeatable action sends a client-generated idempotency key,
and **the same key is resent on every retry of that same user intent** — a new key per attempt is not
idempotency, it is duplicate submission with extra steps. The key is generated once when the intent is
formed, not when the request is issued. The header name and its semantics are
`/alaa-services-contract` (`$alaa-services-contract`) `references/10-core-service-contract.md`.

## Retry only what is safe to retry

Retry a read. Retry a mutation only when it carries an idempotency key and the failure is a transport
failure or an explicit retryable status. Never retry a `4xx` that means the request itself is wrong. The
attempt count, the backoff curve and the jitter are the reliability skill's; the client contributes
the abort on navigation away and the suspension while `navigator.onLine === false`.

## The three degraded states a screen must be able to show

| State | What the UI must do |
|---|---|
| **slow** — the deadline has not fired but the response is late | show progress tied to the specific action, keep the rest of the screen usable, offer cancel |
| **partial** — some of the data arrived, some failed | render what arrived, name what is missing and why, offer a retry scoped to the missing part; never blank the whole screen because one panel failed |
| **unavailable** — the dependency is down or the deadline fired | state what is unavailable, what still works, and what the user may do next; keep any locally held data readable |

A screen with only "loading" and "error" has no degraded behaviour. The visual design of these states is
`/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) `references/15-designed-failure-states.md`; the
Quasar-level failure and degradation surface is `/alaa-quasar-app-vite-v3`
(`$alaa-quasar-app-vite-v3`) `references/34-frontend-failure-and-degradation.md`.

## Offline is a degraded state, not an error

Reads fall back to whatever the app already holds, labelled as held rather than fresh. Writes are queued
rather than lost, and the queue is durable across a reload — which makes it a browser outbox, owned by
`/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`) `references/71-browser-outbox.md`,
with the server-side row-state vocabulary in `/alaa-async-messaging` (`$alaa-async-messaging`). Do not
build a second queue inside a component. The offline navigation shell is `30-pwa-sw-and-offline.md`.

## Failure must be observable

A degraded state that is only visible to the user is invisible to operations. Every deadline fired, retry
exhausted and degraded render emits an event per `47-frontend-observability.md`.

## Anti-patterns

An unbounded retry loop in a component. A retry that regenerates the idempotency key. A global error
banner that replaces the whole route because one panel failed. Swallowing an abort as a success. A
"temporary" hard-coded timeout. Optimistic UI with no reconciliation path when the write finally fails.
