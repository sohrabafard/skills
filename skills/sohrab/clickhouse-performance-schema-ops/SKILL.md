---
name: clickhouse-performance-schema-ops
description: "ClickHouse schema, topology, ingest, query, and operations policy for the Ala fleet on 26.8 LTS. Use when writing or reviewing a CREATE TABLE, ORDER BY, PARTITION BY, engine, or column type; when choosing single-node or Keeper-replicated operation, a Replicated engine, an insert quorum, or a deduplication window; when an insert path makes too many parts, a merge backlog, or duplicate rows on retry; when a query scans far more than it returns, needs FINAL, or must move onto a rollup; when choosing between a materialized view, a projection, a TTL, a mutation, and a partition drop; when a Vector sink, a Go chkit service, or a PHP service connects to ClickHouse or must handle it being unreachable; and when proving a ClickHouse change. Do not use it for Postgres, Redis, or store selection (/alaa-data-layer), Vector transform internals (/vector-rust-observability-pipelines), or SigNoz-owned tables (/alaa-signoz-clickhouse-docs)."
---

# ClickHouse Performance, Schema, Ingest, and Operations

Decide what a ClickHouse table must be, which topology it runs on, how rows reach it, what a query
may read, and what a service does while the analytical store is slow or gone.

## Version floor

Write SQL, settings and defaults for the floor release recorded in `references/90-source-map.md`
under "Release evidence". The owner supports no server below it. Add no compatibility branch for an
older server. Report a server or an image pin below the floor to its owning repository as a defect.

## Two audiences, opposite authority

Name the audience before you propose DDL, because the deliverable differs.

The **ingest-pipeline repository** owns the ClickHouse DDL directory and the Vector topology that
writes into it. On this fleet that repository is `wa`. It creates and alters every table and owns
column type, ordering, partitioning, retention, and engine.

A **service on a read lane** owns none of that and cannot apply DDL. A Go service reads through
`chkit` under a pinned `readonly=2`. A PHP service reads over HTTP under a server-side read-only
profile. Deliver to such a requester a query, a rollup request filed against the ingest pipeline, or
a lane configuration change. Never deliver DDL the requester cannot apply.

`references/10-authority-and-change-path.md` holds the evidence and the change path of each audience.

## Rules that hold on every task

1. Name the repository that owns every table you touch before you write SQL, because a read-lane
   service cannot apply DDL and a raw-table read is not a rollup read.
2. Name the topology mode the environment declares, `single-node` or `replicated`, before you choose
   an engine, a deduplication setting or a DDL path, because each mode fails differently and the
   environment declares the mode with no default. `references/25-topology-and-replication.md`
   decides what each mode requires.
3. Put the tenant column first in `ORDER BY` on every fleet-owned tenant-scoped table, and filter
   every query against one of those tables by it. Such a table or query without it scans every
   tenant's rows to answer one tenant's question. The rule stops at tables the fleet cannot
   alter; `references/15-fleet-clickhouse-boundary.md` names those and gives the reason.
4. Report, and do not edit, a defect in a table owned by another repository, because that
   repository ratifies its own schema and an outside edit is an unratified change.
5. Run `scripts/review_clickhouse_ddl.py` over every `CREATE TABLE` you write or review and paste
   its output into the answer, because a design argument no checker has read is an opinion.
   `references/80-proof-and-validation.md` gives the invocation and what each exit code obliges.
6. Verify a version-sensitive ClickHouse claim against `references/90-source-map.md` and record the
   source and the date you read it. Read a setting's effective value from the target server, because
   a default changes between releases and a profile can override it.
7. Take every metric, log-field, event, and error-code name from `/alaa-services-contract` and
   request registration there when the name you need is absent, because an invented name diverges
   across services.

## References

Route the task through `references/00-topic-map.md`, which maps the situation you are in to the one
file that answers it.

## Not owned here

`clickhouse-performance-schema-ops` owns what a ClickHouse table must be — engine, sorting key,
partitioning, TTL, compression — for tables the fleet controls.
`alaa-signoz-clickhouse-docs` owns how a SigNoz-owned table is queried, and states that those tables
are vendor-owned and read-only to the fleet.
`vector-rust-observability-pipelines` owns what the pipeline writes into a ClickHouse table and how
it behaves when that table is unreachable, and decides no schema.

- SigNoz panel SQL: `/alaa-signoz-clickhouse-docs`.
- Postgres schema, indexes, migrations, Redis, and store selection: `/alaa-data-layer`.
- Vector source, transform, sink, and buffer internals: `/vector-rust-observability-pipelines`.
- Server version, listeners, node count, Keeper placement, capacity and recovery of the shared
  instance: the infrastructure operator, under
  `/alaa-services-contract` `references/15-deployment-and-runtime-contract.md`.
- Model and effort: `/alaa-prompting-guide`.
- The ten-point quality bar: `/alaa-project-constitution` `references/quality-bar.md`.

Every other owner is named at the rule it governs inside `references/`.

## When NOT to use

- a `signoz_*` or other vendor-owned table whose engine, sorting key, partitioning or TTL the
  fleet cannot alter
- panel SQL written against a SigNoz-owned table
- Postgres or Redis schema, indexes, migrations, or the choice of which store holds a dataset
- Vector source, transform, sink, or buffer internals
- a task that touches no ClickHouse table, query, ingest path, topology, or client lane setting
