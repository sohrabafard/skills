# Topic map

Match the situation you are in, read that one file, and return.

| You are about to | Read |
| --- | --- |
| propose, write, or apply a `CREATE TABLE`, an `ALTER TABLE`, or a schema migration, or you do not yet know whether the requester may run DDL | `10-authority-and-change-path.md` |
| decide whether a ClickHouse table is this skill's to design, tell a fleet-owned table from a vendor-owned `signoz_*` table, or resolve a rule that another ClickHouse skill states differently | `15-fleet-clickhouse-boundary.md` |
| choose a column type, an `ORDER BY`, a `PARTITION BY`, a primary key, a compression codec, or a MergeTree engine variant | `20-table-design.md` |
| choose an engine for the declared topology mode, add a replica, place Keeper, set an insert quorum, apply DDL to more than one node, or diagnose a read-only or lagging replica | `25-topology-and-replication.md` |
| change how rows reach a table, or you see a rising part count, a `TOO_MANY_PARTS` error, a merge backlog, or duplicate rows after a retried insert | `30-ingest-and-parts.md` |
| write, review, or speed up a query that reads a ClickHouse table from a service, a dashboard, or an ad-hoc session | `40-query-tuning-and-read-lane.md` |
| add a rollup, an alternate layout, a retention rule, or a delete, and must choose among a materialized view, a projection, a TTL, a mutation, and a partition drop | `50-mvs-projections-and-ttl.md` |
| diagnose a running server: a slow query, a stuck mutation, unexplained disk growth, or merges that do not finish | `60-operations-and-diagnostics.md` |
| decide what a service returns while ClickHouse is unreachable or a query trips `max_execution_time` or `max_result_rows`, or pick a readiness severity for the ClickHouse check | `70-failure-and-degradation.md` |
| ship a ClickHouse change and must state what proves it | `80-proof-and-validation.md` |
| connect a Vector sink, a Go service or a PHP service, or set an endpoint, credential, grant, timeout, pool bound, or per-query limit | `85-access-and-configuration.md` |
| choose a release, plan an upgrade past the floor, or repeat a version-sensitive claim, a setting name or a default value | `90-source-map.md` |
