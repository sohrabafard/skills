# Failure behaviour and degradation

A ClickHouse read ends in one of four ways, and each needs a decided answer before the code ships:
it returns, it returns late, it returns an error, or it returns fewer rows than exist. The last one
looks like success.

## The bounds a read runs inside

Every read lane applies four bounds. The Go lane's are below; a PHP lane reproduces the same four
(`85-access-and-configuration.md`).

| Bound | Where on the Go lane | What trips it |
| --- | --- | --- |
| dial timeout | `configkit` lane key `CLICKHOUSE_DIAL_TIMEOUT` | connection establishment |
| call timeout | `chkit` `Config.CallTimeout`, a context deadline through row consumption | the whole call, client-side |
| `max_execution_time` | `chkit` `Config.Settings`, a session setting | the query, server-side |
| `max_result_rows` | `chkit` `Config.Settings`, a session setting | the result size, server-side |

The server applies no execution-time limit and no result-row limit by default. A lane that sends
neither has neither.

Set the call timeout above `max_execution_time`. The server-side bound returns a ClickHouse error
that names the limit. The client deadline returns only a cancellation, and when it fires first, the
server-side diagnosis is lost.

## A result over `max_result_rows` must throw

An overflow-mode setting is `throw`, the default, or `break`, which will "stop executing the query
and return the partial result, as if the source data ran out". `chkit` sets no overflow mode, and a
PHP lane sets none, so a query over the cap fails loudly. Treat a proposal to set `result_overflow_mode = break`
or `timeout_overflow_mode = break` on a request path as a change that needs an explicit argument:
under `break` the handler cannot tell a truncated result from a complete one.

A query that trips `max_result_rows` is wrong. Aggregate server-side, narrow the time window, or
page by sort-key range (`/alaa-keyset-pagination`).

## No hidden retries

The lane surfaces a failed or timed-out query to the caller. The handler decides from the error
class:

| The error says | Retry? | Because |
| --- | --- | --- |
| dial or connection failure | at most once, on a fresh deadline, and only while the caller's own deadline has room | the query never ran |
| client-side deadline exceeded | no | the caller has no time budget left |
| `max_execution_time` exceeded | no | the same query exceeds it again |
| `max_result_rows` exceeded | no | the result size is a property of the query |
| `TOO_MANY_SIMULTANEOUS_QUERIES` or a memory limit | no immediate retry; shed | a retry adds load to an overloaded server |

Retry budgets, backoff, breakers, and load shedding: `/alaa-reliability-sla`
`references/20-retries.md`, `references/30-breakers-and-bulkheads.md`, and
`references/40-admission-and-shedding.md`.

## Readiness severity

`chkit` makes readiness severity a caller parameter. Apply one test: **do the service's primary
documented endpoints still return correct responses with ClickHouse absent?**

- If any primary endpoint cannot, register `SeverityRequired`. Draining the pod is right, because a
  pod that answers wrongly is worse than a pod out of rotation. `wa-api` does this; its read surface
  is the analytics store.
- If every primary endpoint still answers correctly and only an optional enrichment is lost,
  register `SeverityDegraded`. Then specify the degraded response: which field is omitted, what the
  client sees in its place, and which telemetry records the skip.

Write the reason in a comment beside the registration, because the constant does not carry it.

## What a consumer does while ClickHouse is unreachable

1. **Fail at boot when the lane is unconfigured.** On the Go lane a blank `CLICKHOUSE_ADDR` makes
   `NewClient` return `ErrNoClickHouseAddr`.
2. **Never substitute a fabricated value for an analytics number.** A zero, an empty series, or a
   stale cached figure shown as current turns an outage into a wrong answer nobody reports. Return
   the error, or return the response with the analytics field explicitly absent and a stated reason.
3. **Never fall back to a raw event table because the rollup is missing.** That turns an analytics
   outage into a load event on the whole server.
4. **Never fall back to Postgres for an answer Postgres does not hold.** Which store owns which
   fact: `/alaa-data-layer`.
5. **Losing ClickHouse must not change owned state.** A write path that depends on an analytics read
   is the defect.

In `replicated` mode a lagging replica returns an older answer with no error. State the staleness a
response accepts: `25-topology-and-replication.md`.

Degradation doctrine: `/alaa-reliability-sla` `references/50-degradation.md`. Every platform value
this skill does not state, such as timeout numbers, error budgets and load ceilings:
`/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`.

## On the ingest side

Trace how the producer sees delivery, backpressure and failure with `30-ingest-and-parts.md`.
Observe buffer fill before saturation, and prove duplicate handling on retry. Instrumentation:
`/alaa-observability-soc` `references/20-instrumentation-gates.md`.
