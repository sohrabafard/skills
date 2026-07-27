# Failure behaviour and degradation

Every ClickHouse read has four ways to end and each needs a decided answer before the code ships:
it returns, it returns late, it returns an error, or it returns fewer rows than exist. The last one
is the dangerous one, because it looks exactly like success.

## The bounds a read runs inside

`alaa-go-chi` `chkit` applies four bounds and each one has an owner:

| Bound | Where | What trips it |
| --- | --- | --- |
| `DialTimeout` | `configkit` lane key `CLICKHOUSE_DIAL_TIMEOUT`, default `5s` | connection establishment |
| `CallTimeout` | `chkit` `Config.CallTimeout` (context deadline per call, through row consumption) | the whole call, client-side |
| `max_execution_time` | `chkit` `Config.Settings`, sent as a session setting | the query, server-side |
| `max_result_rows` | `chkit` `Config.Settings`, sent as a session setting | the result size, server-side |

Set `CallTimeout` above `max_execution_time`. The server-side bound produces a ClickHouse error
naming the limit; the client-side deadline produces a context cancellation that says only that time
ran out. When the client deadline fires first, every server-side diagnosis is thrown away.

## Exceeding `max_result_rows` throws — unless someone changes the overflow mode

Verified against the official query-complexity documentation: an overflow-mode setting takes one of
two values — `throw`, which throws an exception and is the default, and `break`, which will "stop
executing the query and return the partial result, as if the source data ran out".

`chkit` sets `max_result_rows` and does not set `result_overflow_mode`, so the default `throw`
applies and a query over the cap fails loudly. Keep it that way, and treat any proposal to set
`result_overflow_mode = break` or `timeout_overflow_mode = break` on a request path as a change that
must be argued explicitly: under `break` a truncated result is returned with no error, no flag, and
no way for the handler to tell it apart from a complete one. A dashboard fed by `break` shows a
smaller number and no incident.

If a query is tripping `max_result_rows`, the query is wrong. Aggregate server-side, narrow the time
window, or page by sort-key range (`/alaa-keyset-pagination`, `$alaa-keyset-pagination`).

## No hidden retries

`chkit/doc.go:31-32`: "No hidden retries: a failed or timed-out query surfaces to the caller, which
decides whether the read is retryable." So the handler decides, and the decision is made from the
error class:

| The error says | Retry? | Because |
| --- | --- | --- |
| dial or connection failure | at most once, on a fresh deadline, and only if the caller's own deadline has room | the query never ran |
| context deadline exceeded (client-side) | no | the caller has no time budget left to spend |
| `max_execution_time` exceeded | no | the same query will exceed it again |
| `max_result_rows` exceeded | no | the result size is a property of the query |
| `TOO_MANY_SIMULTANEOUS_QUERIES` or memory limit | no immediate retry; shed instead | retrying adds load to an overloaded server |

Retry budgets, backoff shape, breakers, and load shedding are doctrine, not mechanics:
`/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/20-retries.md`,
`references/30-breakers-and-bulkheads.md`, and `references/40-admission-and-shedding.md`.

## Readiness severity is a decision this skill makes decidable

`chkit/readiness.go:15-19` makes severity a caller parameter and states the intent: a service whose
read surface **is** ClickHouse rollups registers `SeverityRequired`, while a service that only
decorates responses with analytics registers `SeverityDegraded`, "so a ClickHouse blip degrades the
pod instead of draining it". Unlike Redis, which the kit always treats as degraded because it is
never truth, ClickHouse can be either.

Apply one test. **Ask whether the service's primary documented endpoints still return correct
responses with ClickHouse absent.**

- If any primary endpoint cannot answer correctly without ClickHouse, register `SeverityRequired`.
  Draining the pod is right, because a pod that answers wrongly is worse than a pod removed from
  rotation. `alaa-go-chi` `docs/CONSUMERS.md:23` records `wa-api` doing exactly this: "chkit
  (`CLICKHOUSE_*` lane, ReadyCheck Required)" — its read surface is the analytics store.
- If every primary endpoint still answers correctly and only an optional enrichment is lost,
  register `SeverityDegraded`, and then the degraded response must be specified: which field is
  omitted, what the client sees in its place, and which telemetry records that the enrichment was
  skipped.

Whichever you register, write the reason in a comment next to the registration, because the next
reader cannot recover the test's answer from the constant.

## What a consumer does while ClickHouse is unreachable

1. **Fail at boot, not at first query, when the lane is unconfigured.** `chkit/doc.go:34-37`: the
   lane is absent when `CLICKHOUSE_ADDR` is blank and `NewClient` then returns
   `ErrNoClickHouseAddr`, "so a service that wires chkit without configuring the lane fails at boot
   instead of at first query."
2. **Never substitute a fabricated value for an analytics number.** A zero, an empty series, or a
   stale cached figure rendered as if current turns an outage into a wrong answer that nobody
   reports. Return the error, or return the response with the analytics field explicitly absent and
   a stated reason.
3. **Never fall back to a raw event table because the rollup is missing.** That converts an
   analytics outage into a cluster-wide load event.
4. **Never fall back to Postgres for an analytics answer that Postgres does not hold.** Which store
   owns which fact: `/alaa-data-layer` (`$alaa-data-layer`).
5. **Losing ClickHouse must not change owned state.** `chkit/doc.go:20-21`: "losing ClickHouse
   degrades analytics, never correctness of owned state." If a write path depends on an analytics
   read, that dependency is the defect.

Degradation doctrine — what a partial response is allowed to look like, and how a client is told:
`/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/50-degradation.md`. Every platform
value this skill does not state — timeout numbers, error budgets, load ceilings:
`/alaa-services-contract` (`$alaa-services-contract`)
`references/22-failure-load-and-deprecation-contract.md`.

## On the ingest side

The write path fails differently, because the Vector topology stands between the producer and
ClickHouse: acknowledged batches sit in a blocking disk buffer while the sink retries, so
unavailability appears as a filling buffer and backpressure at the HTTP source, not as an error to
the producer. Two obligations follow: the buffer's fill level must be visible in telemetry before an
outage, not after, and the retry behaviour means duplicate rows are possible on recovery
(`30-ingest-and-parts.md`). What to instrument and at what level: `/alaa-observability-soc`
(`$alaa-observability-soc`) `references/20-instrumentation-gates.md`; buffer and acknowledgement
semantics themselves: `/vector-rust-observability-pipelines`
(`$vector-rust-observability-pipelines`).
