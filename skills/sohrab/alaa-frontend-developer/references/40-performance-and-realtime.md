# Performance Workflow and Realtime

The bottleneck workflow and the WebSocket/SSE lifecycle. The scoring model, the metric playbooks, the
budgets and the complexity thresholds are `41-lighthouse-and-web-vitals.md`.

## Bottleneck workflow

1. **Baseline.** Name the route, the device class, the network profile, and whether the case is SSR first
   load or client navigation. A measurement without those four is not comparable to anything.
2. **Pick the dominant bucket before optimizing.** Server and TTFB and SSR render time; client hydration,
   JavaScript execution and long tasks; network chunking, waterfalls and blocking assets; UI layout
   thrash, large DOM and heavy watchers.
3. **Apply the smallest measurable fix**, then re-measure the same profile and attribute the delta to the
   metric you targeted. A fix that cannot be attributed did not happen.

Typical wins: route-level code splitting; dynamic import for a heavy feature; fewer deep watchers; stable
computed inputs; virtualization above the threshold in `41-lighthouse-and-web-vitals.md`; image and font
loading changes that do not touch the SSR or service-worker contract.

## Realtime lifecycle

Never open a socket or an SSE stream at module scope. Never connect during an SSR render. Connect on the
client lifecycle; disconnect on unmount and on route teardown. States: `idle`, `connecting`, `open`,
`reconnecting`, `closed`, `error` — and the current state is readable by the UI.

## Reconnect

The retry policy — how many attempts, the base delay, the cap, the jitter shape, the total budget — is
owned by `/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/20-retries.md`. Take the values
from there; do not invent a curve locally. What this file requires of the client:

- Suspend reconnect attempts while `navigator.onLine === false`; resume on the `online` event.
- Cap total reconnect duration, and surface the `closed` state to the UI when the cap is hit rather than
  reconnecting silently forever.
- One reconnect loop per connection. A second loop created by a re-mounted component is the reconnect
  storm.

## Message handling

Parse JSON inside a `try`. Validate the message shape before it mutates UI state. An unknown message type
is ignored, not thrown on. A payload is never inserted as HTML — `25-frontend-security.md`.

**Backpressure.** A stream that produces faster than the UI can render must coalesce, not queue without
bound: keep the latest value per key, drop superseded frames, and batch renders on an animation frame. An
unbounded in-memory queue behind a live stream is a memory leak with a delay.

**Concurrency ceiling.** Cap the number of in-flight requests a screen may hold open, and abort the
previous request when a newer one supersedes it (`20-vue-js-ssr-patterns.md`). A list that fires one
request per row is the N+1 family — `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`) `references/40-call-in-a-loop.md` — and the client-side batching rule
is `45-api-and-data-shaping.md`.

## Connection telemetry

Emit one structured event per connect, disconnect and reconnect attempt, using the event names and log
fields defined by `/alaa-services-contract` (`$alaa-services-contract`)
`references/20-operational-and-observability-contract.md`. The required level and whether the event is
mandatory are set by `/alaa-observability-soc` (`$alaa-observability-soc`)
`references/20-instrumentation-gates.md`. The client-side wiring is `47-frontend-observability.md`. Never
put a message payload in a production log.

## Failure signatures

| Symptom | Usual cause |
|---|---|
| reconnect storm | no backoff, a duplicate listener, or two reconnect loops |
| memory growth after repeated navigation | a leaked listener or an undisconnected socket |
| poor INP or jank right after hydration | too much client work on the first route, or heavy watchers |
| a "slow load" that no perf fix improves | a missing chunk or an asset-path bug wearing a performance costume |
| the UI freezes under a burst of messages | no coalescing; see backpressure above |

## Verification

Connect and disconnect across route changes; reconnect after a network drop; no duplicate event handling
after navigating away and back; CPU and memory stable over time; one targeted measurement of the
bottleneck you actually changed. Recorded per `50-qa-and-verification.md`.
