# Query tuning and the service read lane

## What a request-path query is allowed to do

`alaa-go-chi` `chkit/doc.go:20-24` states the read doctrine the kit enforces and the consumers
inherit. Restated as obligations on the SQL you write:

1. **Read a pre-aggregated rollup, never a raw event table, from a request path.** A raw table is
   sized by ingest volume; a rollup is sized by the answer. A request-path query against a raw table
   is a latency incident waiting for the table to grow.
2. **Bound the time range explicitly in the query text.** An absent upper or lower bound is an
   unbounded scan, and it is the one defect that gets worse every day without any code changing.
3. **Bound the tenant explicitly**, per `20-table-design.md` section 1.
4. **Expect no retry from the transport.** `chkit/doc.go:31-32`: "No hidden retries: a failed or
   timed-out query surfaces to the caller, which decides whether the read is retryable." The
   decision about what the handler does with that error is `70-failure-and-degradation.md`.
5. **Pass values as query arguments,** never by string-formatting them into the SQL.
   `chkit/client.go:100` and `:113` take `args ...any` for this. A tenant identifier concatenated
   into SQL is an injection point on the one predicate that separates tenants.

ClickHouse is not the source of truth for anything a request may not lose. `chkit/doc.go:19-21`:
"ClickHouse is an analytical read surface, never OLTP truth. PostgreSQL remains the durable source
of truth". Which store owns which fact: `/alaa-data-layer` (`$alaa-data-layer`).

## Diagnosing a slow query

Work from measurement, in this order. Skipping to step 4 is how a skip index gets added to a table
whose sort key was the problem.

1. **Get the read/return ratio.** From `system.query_log`, compare `read_rows` to `result_rows` and
   `read_bytes` to `result_bytes` for the exact query. A ratio of thousands means the engine read
   data it then discarded, and the fix is pruning, not compute.
2. **Check prefix alignment.** The sparse index prunes on a prefix of `ORDER BY`. List the query's
   equality and range predicates, line them up against the sort key from the left, and find the
   first sort-key column the query does not constrain. Everything after that point in the key is
   doing nothing for this query. If the very first column is unconstrained, the query reads the
   whole table.
3. **Check partition pruning.** A predicate on a column the partition expression is derived from
   lets whole partitions be skipped. On this pipeline the partition key is `toYYYYMM(event_date)`
   and `event_date` is `MATERIALIZED toDate(event_time)`, so a filter written on `event_time`
   prunes; a filter written only on `received_at` does not, because `received_at` is unrelated to
   the partition expression.
4. **Only then** consider a materialized column, a skip index, a projection, or a rollup, and pick
   using `50-mvs-projections-and-ttl.md`.

## Rewrites that pay, in order of how often they apply

- **Move the selective predicate into the query, not the application.** Filtering in Go after
  reading is the read/return ratio problem in its purest form.
- **Aggregate in ClickHouse, return rows to the service.** `chkit` bounds
  `max_result_rows` server-side precisely so a query that tries to stream a raw table into a service
  fails rather than succeeding slowly.
- **Replace a join with a precomputed column, a dictionary, or a rollup.** Joins in ClickHouse
  reward precomputation; a broad join filtered late reads both sides in full.
- **Use `FINAL` only where correctness requires it, and never as a habit.** `FINAL` at query time
  deduplicates for the read; `OPTIMIZE FINAL` rewrites the table and is a different, far more
  expensive thing (`60-operations-and-diagnostics.md`). A query that uses `FINAL` also forfeits
  projections, which "don't work with `FINAL` queries".
- **Cursor through large result sets by sort-key range, not by `OFFSET`.** Design and encoding of
  the cursor: `/alaa-keyset-pagination` (`$alaa-keyset-pagination`).

Complexity bounds and the choice of structure behind an aggregation:
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).

## Finding in the pipeline's verification queries, reported and not fixed

`samples/verification_queries.sql` in the ingest-pipeline repository contains eight verification
queries. Queries 1 through 6 carry no `project_id` predicate and no time bound; query 7 groups by
`project_id` but still scans every partition. As post-ingest sanity checks against a local
single-project database that is defensible, and their comment says so. The risk is that they are the
nearest thing to an example any future author will copy. Any query derived from that file for a
request path, a dashboard, or a scheduled job must gain both bounds before it is used. Reported to
the owning repository; not edited from here.

## Ad-hoc and dashboard queries

An interactive session and a dashboard are not exempt from the bounds above; they are exempt only
from the rollup rule, and only when a human is watching the query run. A scheduled dashboard refresh
is a request path with a slower clock: it needs the tenant predicate, the time bound, and a rollup,
because nobody is watching it degrade. Telemetry that makes that degradation visible:
`/alaa-observability-soc` (`$alaa-observability-soc`) `references/20-instrumentation-gates.md`.
