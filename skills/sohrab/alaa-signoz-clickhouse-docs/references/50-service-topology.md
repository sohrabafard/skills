# Service Topology and the Dependency Graph

Read this to answer what calls what, to read the service map, or to explain an edge that is not
there.

**This endpoint appears in no SigNoz documentation page.** Every fact below was read from SigNoz
source on 2026-07-30 and carries the command that re-derives it. That is why it is written down: an
undocumented dependency that lives only in one session's memory is lost when that session ends.

## The one rule this file exists to state

**The dependency graph is a lower bound on the true call graph.** Never conclude from a missing edge
that a call does not happen; conclude only that no trace recording it was collected in the window you
asked about. The reason is mechanical, not cautionary — see *How an edge is built*.

## The endpoint

`POST /api/v1/dependency_graph`, registered at
`pkg/query-service/app/http_handler.go:527` inside `am.ViewAccess(...)`, so a **viewer-level**
credential is enough to read the entire fleet's topology. Treat that as the access fact it is: a key
that can read this endpoint can enumerate every service and every database and broker they talk to.

Request body, from `GetServicesParams` at `pkg/query-service/model/queryParams.go:83`:

```json
{ "start": "<unix nanoseconds or RFC3339>", "end": "<same>", "tags": [] }
```

Response, an array of `ServiceMapDependencyResponseItem` from
`pkg/query-service/model/response.go:328`, with lowerCamel JSON keys:

```
parent, child, callCount, callRate, errorRate, p99, p95, p90, p75, p50
```

## The table behind it

`signoz_traces.distributed_dependency_graph_minutes_v2`, from
`pkg/query-service/app/clickhouseReader/options.go:27`:

```go
defaultDependencyGraphTable string = "distributed_dependency_graph_minutes_v2"
```

**Do not query the v1 name.** `distributed_dependency_graph_minutes` is dropped by
`traces_migrations.go:533`; on a current install it returns stale rows or none, and it fails without
an error you would notice.

## How an edge is built, and what that excludes

Three materialized views feed the table, all reading `signoz_traces.signoz_index_v3` and all
aggregating per minute into `(timestamp, src, dest, deployment_environment, k8s_cluster_name,
k8s_namespace_name)` with `quantilesState(0.5, 0.75, 0.9, 0.95, 0.99)(toFloat64(duration_nano))`,
`countIf(status_code = 2) AS error_count` and `count(*) AS total_count`.

**Service to service** — `dependency_graph_minutes_service_calls_mv_v2`, `traces_migrations.go:990`:

```sql
FROM signoz_traces.signoz_index_v3 AS A, signoz_traces.signoz_index_v3 AS B
WHERE (A.resource_string_service$$name != B.resource_string_service$$name)
  AND (A.span_id = B.parent_span_id)
```

An edge exists only when **both** spans were collected and the child's parent id matches the
parent's span id. A span that was sampled away, dropped in transit, or never exported erases the
edge — the same failure `40-missing-spans.md` diagnoses. That join is the entire reason the graph is
a lower bound.

**Service to database** — `dependency_graph_minutes_db_calls_mv_v2`, `traces_migrations.go:444`:

```sql
resource_string_service$$name AS src,
attribute_string_db$$system AS dest
...
WHERE (dest != '') AND (kind != 2)
```

The destination is the value of `db.system`, so **every PostgreSQL instance in the fleet collapses
into one node named for the engine**, not for the host, database or cluster. A graph showing one
`postgresql` node is not a claim that there is one database. `kind != 2` excludes SERVER spans, so
only the client side of a database call contributes.

**Service to broker** — `dependency_graph_minutes_messaging_calls_mv_v2`,
`traces_migrations.go:467`:

```sql
resource_string_service$$name AS src,
attribute_string_messaging$$system AS dest
```

Producer-to-broker edges **are** recorded, collapsed per messaging system in exactly the same way:
every RabbitMQ vhost, exchange and queue becomes one node named `rabbitmq`.

**There is no broker-to-consumer edge, and its absence is structural.** A consumer that starts a new
root span and attaches the producer's context as a span *link* rather than a parent produces no row
where `A.span_id = B.parent_span_id`, which is what the service-calls view requires. So an
asynchronous flow appears in the graph as producer to broker and stops there. Read a queue's
consumers from the consumer service's own spans, never from the dependency graph, and say which you
used.

## Re-derivation

```bash
curl -s https://raw.githubusercontent.com/SigNoz/signoz/main/pkg/query-service/app/http_handler.go \
  | grep -n 'dependency_graph'
curl -s https://raw.githubusercontent.com/SigNoz/signoz/main/pkg/query-service/app/clickhouseReader/options.go \
  | grep -n 'defaultDependencyGraphTable'
curl -s https://raw.githubusercontent.com/SigNoz/signoz/main/pkg/query-service/model/response.go \
  | grep -n -A12 'ServiceMapDependencyResponseItem'
curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/main/cmd/signozschemamigrator/schema_migrator/traces_migrations.go \
  | grep -n -A24 'dependency_graph_minutes_.*_mv_v2'
```

A line number here is a convenience, not the pin: `http_handler.go` moved this route from line 531 to
527 between two reads of the same repository. The route string and the constant name are stable; grep
for those.

## Answering with it

Name which of the three edge kinds carries the answer, give the window, and put the lower bound in
the same sentence as the result: *"in this window these callers were recorded; a caller with no
collected spans in the window would not appear."* Do not hand-write a self-join over
`distributed_signoz_index_v3` — the vendor already materialised it.
