---
name: clickhouse-performance-schema-ops
description: "ClickHouse schema, ingest, query, and operations policy for the Ala fleet: the ingest-pipeline repository owns the DDL, and every kit consumer reads through a readonly=2 chkit lane that cannot execute DDL. Use when writing or reviewing a CREATE TABLE, ORDER BY, PARTITION BY, engine, or column type; when an insert path produces too many parts or a merge backlog; when a query scans far more than it returns, needs FINAL, or must move off a raw table onto a rollup; when choosing between a materialized view, a projection, a TTL, a mutation, and a partition drop; when deciding what a read-lane service does while ClickHouse is unreachable or a query trips max_execution_time or max_result_rows; and when proving a ClickHouse change before it ships. Do not use it for Postgres schema, indexes, migrations, Redis, or store selection, which belong to /alaa-data-layer, nor for Vector transform internals, which belong to /vector-rust-observability-pipelines."
---

# ClickHouse Performance, Schema, Ingest, and Operations

Decide what a ClickHouse table must be, how rows reach it, what a query is allowed to read, and
what a service does while the analytical store is slow or gone.

## Two audiences, opposite authority

Name the audience before proposing any DDL, because the deliverable differs. The **ingest-pipeline
repository** — the one that owns the ClickHouse DDL directory and the Vector topology writing into
it, and on this fleet that repository is `wa` — creates and alters every table and owns column
type, ordering, partitioning, retention, and engine. A **kit consumer on the `chkit` read lane**
owns none of that: every session is pinned to `readonly=2` as a kit invariant, the client exports
no `Exec`, and a kit integration test fails if a `CREATE TABLE` issued over that lane succeeds.
When the requester is a consumer, deliver a query, a rollup request filed against the ingest
pipeline, or a `chkit` configuration change, and never DDL the requester cannot apply. Source
evidence and the change path each audience follows: `references/10-authority-and-change-path.md`.

## Rules that hold on every task

1. Name the repository that owns every table you touch before writing SQL, because a consumer
   cannot apply DDL and a raw-table read is not a rollup read.
2. Put the tenant column first in `ORDER BY` on every fleet-owned tenant-scoped table, and filter
   every query against one of those tables by it, because such a table or query without it scans
   every tenant's rows to answer one tenant's question. The rule stops at tables the fleet cannot
   alter; `references/15-fleet-clickhouse-boundary.md` names those and gives the reason.
3. Report, and do not edit, a defect in a table owned by another repository, because that
   repository ratifies its own schema and an outside edit is an unratified change.
4. Run `scripts/review_clickhouse_ddl.py` over every `CREATE TABLE` you write or review and paste
   its output into the answer, because a design argument no checker has read is an opinion.
5. Verify a version-sensitive ClickHouse claim against the pages in `references/90-source-map.md`
   and record the URL and the date you read it, because a decision log records what a team chose,
   not what the engine does.
6. Take every metric, log-field, event, and error-code name from `/alaa-services-contract`
   (`$alaa-services-contract`) and request registration there when the name you need is absent,
   because an invented name diverges across services.

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

Which tables fall on which side of that line, and why a SigNoz query needs no tenant predicate:
`references/15-fleet-clickhouse-boundary.md`. SigNoz panel SQL itself: `/alaa-signoz-clickhouse-docs`
(`$alaa-signoz-clickhouse-docs`). Postgres schema, indexes, migrations, Redis, and store selection:
`/alaa-data-layer` (`$alaa-data-layer`). Vector source, transform, sink, and buffer internals:
`/vector-rust-observability-pipelines` (`$vector-rust-observability-pipelines`). Multi-agent plans:
`/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`), or `/alaa-codex-orchestrator`
(`$alaa-codex-orchestrator`) in Codex. Model and effort: `/alaa-prompting-guide`
(`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`. The ten-point quality bar:
`/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md`. Every other
owner is named at the rule it governs inside `references/`.
