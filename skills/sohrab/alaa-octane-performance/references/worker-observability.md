# Worker observability contract

This skill contributes only the signals a long-lived worker uniquely produces. It names **no
field and no metric name** — those belong to `alaa-services-contract
references/24-metric-registry.md` — and **no requirement level** — that belongs to
`/alaa-observability-soc` (`$alaa-observability-soc`). On conflict, SOC decides whether a signal
is required and the contract decides what it is called. If the registry has no name for a signal
below, add one there rather than inventing a local name.

| Signal | Why it exists |
| --- | --- |
| Resident memory **per worker**, not averaged | RSS that tracks requests served is the headline symptom of an Invariant 2 violation. Averaged across workers, one leaking worker is invisible until it is OOM-killed. |
| Requests served **per worker** since boot | The denominator that makes the RSS series interpretable: bytes per request served is the leak slope. It also exposes uneven distribution across workers. |
| Worker restart count | Separates a `max_requests` recycle from a crash. A rise with no deploy and no recycle boundary is a crash loop (`references/worker-lifecycle-and-failure.md`). |
| Connections held, against the server's ceiling | The `workers × connections per worker` arithmetic in `references/full-guide.md` is unverifiable without it, and `connected_clients` rising with process uptime is the one observable that authorises a connection-lifecycle change. |
| Latency bucketed by worker age (requests served since boot) | The only signal that separates "this code is slow" from "this worker degrades as it ages". Without it, accumulation and load are indistinguishable in a latency graph. |

Emission rules owned here:

- Every signal above carries a worker identity label. Cardinality is bounded by worker count,
  which is bounded by `references/load-and-backpressure.md`.
- Worker age is emitted **bucketed**, never as a raw request counter in a label position.
- A change that alters worker count, `max_requests`, the driver, or connection lifecycle is not
  complete until these signals exist for it — a tuning value chosen from a signal nobody emits
  cannot be re-derived by the next person.

Whether profiling may be enabled at all, and at what sampling rate, is owned by
`/alaa-observability-soc` `references/60-sentry-and-profiling.md`. How to profile once permitted
is `references/diagnostic-drills.md`.
