# Topic map

Match the situation you are in, read that one file, and return. Reading a file you do not match
costs context and buys nothing.

| You are about to | Read |
| --- | --- |
| propose, write, or apply a `CREATE TABLE`, an `ALTER TABLE`, or a schema migration, or you do not yet know whether the requester is allowed to run DDL | `10-authority-and-change-path.md` |
| choose a column type, an `ORDER BY`, a `PARTITION BY`, a primary key, a compression codec, or a MergeTree engine variant | `20-table-design.md` |
| change how rows reach a table, or you are looking at a rising part count, a `TOO_MANY_PARTS` error, or a merge backlog | `30-ingest-and-parts.md` |
| write, review, or speed up a query that reads a ClickHouse table from a service, a dashboard, or an ad-hoc session | `40-query-tuning-and-read-lane.md` |
| add a rollup, an alternate layout, a retention rule, or a delete, and must choose among a materialized view, a projection, a TTL, a mutation, and a partition drop | `50-mvs-projections-and-ttl.md` |
| diagnose a running cluster: a slow query, a stuck mutation, unexplained disk growth, or merges that are not finishing | `60-operations-and-diagnostics.md` |
| decide what a service returns while ClickHouse is unreachable or a query trips `max_execution_time` or `max_result_rows`, or pick a readiness severity for the ClickHouse check | `70-failure-and-degradation.md` |
| ship a ClickHouse change and must state what proves it is correct | `80-proof-and-validation.md` |
| set an endpoint, credential, timeout, pool bound, or per-query limit, or you cannot find the environment key for one | `85-access-and-configuration.md` |
| repeat a version-sensitive claim about ClickHouse behaviour, a setting, or a default value | `90-source-map.md` |
