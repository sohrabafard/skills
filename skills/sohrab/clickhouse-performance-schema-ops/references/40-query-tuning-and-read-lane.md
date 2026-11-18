# Query tuning and the service read lane

## What a request-path query may do

`alaa-go-chi` `chkit/doc.go` states the read doctrine for the Go lane. The same obligations bind a
PHP lane and every other service that reads ClickHouse:

1. **Read a pre-aggregated rollup, never a raw event table, from a request path.** Ingest volume
   sizes a raw table; the answer sizes a rollup.
2. **Bound the time range in the query text,** with a lower and an upper bound. An unbounded scan
   gets slower every day with no code change.
3. **Bound the tenant in the query text** (`20-table-design.md` section 1).
4. **Expect no retry from the transport.** A failed or timed-out query surfaces to the caller, and
   the caller decides: `70-failure-and-degradation.md`.
5. **Bind values as query parameters; never format them into the SQL.** A tenant identifier
   concatenated into SQL is an injection point on the one predicate that separates tenants. The
   binding form of each lane: `85-access-and-configuration.md`.

ClickHouse is an analytical read surface and never the source of truth for a fact a request may not
lose. Which store owns which fact: `/alaa-data-layer`.

## Diagnosing a slow query

Work in this order. A skip index added before step 2 hides a sort-key problem.

1. **Get the read/return ratio.** In `system.query_log`, compare `read_rows` with `result_rows` and
   `read_bytes` with `result_bytes` for the exact query. A ratio in the thousands means the engine
   read data and discarded it. The fix is pruning.
2. **Check prefix alignment.** Line the query's equality and range predicates up against the sort
   key from the left. The first sort-key column the query does not constrain ends the pruning. If
   the first column is unconstrained, the query reads the whole table.
3. **Check partition pruning.** Only a predicate on a column the partition expression derives from
   skips partitions. A filter on the event time prunes a table partitioned by the event date; a
   filter on an unrelated timestamp such as a receive time does not.
4. **Only then** choose a materialized column, a skip index, a projection, or a rollup with
   `50-mvs-projections-and-ttl.md`.

## Rewrites

- Filter and aggregate in ClickHouse, and return only the answer. The lane's `max_result_rows` exists
  so that a query that streams a table into a service fails.
- Replace a join with a precomputed column, a dictionary, or a rollup.
- Use `FINAL` only where correctness needs it. A query with `FINAL` also forfeits projections.
  `OPTIMIZE … FINAL` is a different operation: `60-operations-and-diagnostics.md`.
- Page a large result by sort-key range, never by `OFFSET`: `/alaa-keyset-pagination`.

Complexity bounds behind an aggregation: `/alaa-algorithms-data-structures`.

## Ad-hoc, dashboard and verification queries

An interactive session is exempt from the rollup rule only, and only while a person watches the
query run. It keeps the tenant predicate and the time bound. A scheduled dashboard refresh is a
request path: it needs the tenant predicate, the time bound and a rollup, because nobody watches it
degrade. A verification query written for a local single-tenant database gains both bounds before
anyone reuses it for a request path, a dashboard or a scheduled job. Telemetry that shows the
degradation: `/alaa-observability-soc` `references/20-instrumentation-gates.md`.
