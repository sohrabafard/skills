# Load and concurrency — the Vue binding

**`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns complexity budgets, finding
the bound on a growing input, and the N+1 family.** **`/alaa-keyset-pagination`
(`$alaa-keyset-pagination`) owns the paging contract and the cursor.** **`/alaa-reliability-sla`
(`$alaa-reliability-sla`) and `/alaa-services-contract` (`$alaa-services-contract`) own the concurrency and
timeout values.** This file states where the Vue code sits and states no number.

Read it before wiring a `watch` on an input to a fetch, calling an API inside `v-for`, `map`, or
`Promise.all` over a list, adding a client cache, sizing a virtual-scroll window, or sorting or filtering a
list whose length is not a constant.

## The N+1 rule, in the UI

**A fetch, a permission check, or a store read inside a `v-for`, or inside a `map` over a list whose length
is not a constant, is the same defect as an N+1 query.** Two hundred rows each lazily loading a sub-resource
is two hundred requests, and the browser's per-origin connection limit turns that into a queue the user
experiences as the page hanging.

The binding: the component renders what it was given. Resolution is a batched call, a joined response, or a
single store read done once above the loop — owned by
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`); this skill owns the shape it lands
in, which is a prepared view model built by a mapper before render, not a lookup performed during render.

## Input-driven fetches

A `watch` on a text input that calls an API fires once per keystroke. Every such fetch is debounced, and
the previous in-flight request is aborted before the replacement starts
(`70-async-and-failure-binding.md`).

The binding:

- The debounce lives in the composable that owns the query, not in the template and not in the component,
  so it is present for every consumer of that composable and testable without a DOM.
- The debounce interval is a configured value, read from the app's config module, not a literal typed into
  a composable. The value is `/alaa-services-contract` (`$alaa-services-contract`).
- Debounce for "wait until they stop typing"; throttle for "at most once per interval" on a continuous
  stream such as scroll or resize. Choosing the wrong one produces either a stalled UI or the request storm
  you were preventing.
- The debounce timer is cleared on unmount, like any other side effect.

## A cap on parallel requests

**Fan-out from the browser is bounded.** When a change can issue more than a handful of requests at once —
a bulk action over selected rows, a dashboard of independent widgets, a batch upload — the requests run
through a bounded queue with a stated concurrency limit, not through a bare `Promise.all` over the whole
list.

`Promise.all` over an unbounded list issues every request immediately, and the failure is not the server's:
the browser queues them per origin, the last one's latency is the sum of the queue, and the user's
unrelated navigation request is stuck behind them. The concurrency limit is a value from
`/alaa-services-contract` (`$alaa-services-contract`); the queue is a small module in the transport layer.

`Promise.all` also rejects on the first failure and discards the rest. For a bulk action over rows, use
`Promise.allSettled` and report per-row outcomes — the denied ids stay selected
(`65-alaa-observed-patterns.md`).

## Cache lifetime and invalidation

A cache lives at the service or adapter layer as a decorator (`42-structural-patterns.md`). Three things
are stated wherever one exists, and a cache missing any of them is a finding:

- **Its key**, including user and tenant scope — non-negotiable, and the reason is
  `72-frontend-security-binding.md`.
- **Its lifetime**, as a configured value rather than a literal, and what a consumer sees while a stale
  entry is being refreshed.
- **Its invalidation**, explicitly on the writes that make it wrong. A cache the UI cannot invalidate turns
  a successful save into a screen that still shows the old value, and the user saves again.

Where the cache sits relative to a retry is a stacking-order decision with observable consequences
(`42-structural-patterns.md`), and the retry itself is
`/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Rendering large lists

**No unbounded `v-for`.** Any dataset that can grow uses server-side pagination, `QVirtualScroll` or
QTable's server-side mode, or another virtualization strategy. Choose deliberately: server-side pagination
when the backend can page and filter; virtualization for a large dataset already in memory; infinite scroll
only with a bounded in-memory window that discards what scrolled away.

The paging contract, cursor, and page-size value are
`/alaa-keyset-pagination` (`$alaa-keyset-pagination`) and
`/alaa-services-contract` (`$alaa-services-contract`).

Virtual-scroll window sizing follows from the viewport, not from taste: the window is the visible row count
plus an overscan margin, both configured. A window sized to "feel smooth" on the developer's machine is
sized for one screen height and one scroll speed.

## Per-render cost

A `computed` runs on every dependency change and its result is rendered synchronously. The binding:

- Sorting or filtering a list whose length is not a constant happens in a `computed`, never inline in a
  template, and never inside a `v-for` body — a template expression re-evaluates per item per render.
- A derivation whose cost grows with the list is computed once above the loop and passed down, not
  recomputed per row.
- A memo is added against a measurement, and the measurement is stated beside it. An unmeasured memo adds a
  cache with a lifetime nobody reasons about.
- The bound on the list — how large it can actually get — comes from
  `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`), and a growing path with no stated
  bound is a finding there before it is a finding here.

## Recursive structures

A recursive component (`42-structural-patterns.md`, Composite) carries a **numeric** depth bound and a cycle
guard whenever the data is server-shaped or user-shaped. Exceeding the bound renders a truncation the user
can see and reports it; it does not silently stop, and it does not recurse until the stack overflows and
takes the tab with it. The bound is a configured value, not a literal in the component.
