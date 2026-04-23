
# Official-first source map

Use this map before giving version-sensitive ClickHouse schema, ingest, query, or operations guidance. Official ClickHouse docs and the target cluster's observed settings outrank examples, blogs, issue threads, Stack Overflow, and other community material.

## Primary sources

- ClickHouse best practices overview:
  https://clickhouse.com/docs/best-practices
- MergeTree table engine family:
  https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
- Choosing a primary key:
  https://clickhouse.com/docs/best-practices/choosing-a-primary-key
- Choosing a partitioning key:
  https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key
- Choosing data types:
  https://clickhouse.com/docs/best-practices/select-data-types
- Data skipping indexes:
  https://clickhouse.com/docs/optimize/skipping-indexes
- Async inserts:
  https://clickhouse.com/docs/optimize/asynchronous-inserts
- Bulk inserts:
  https://clickhouse.com/docs/optimize/bulk-inserts
- Avoid mutations:
  https://clickhouse.com/docs/best-practices/avoid-mutations
- Avoid OPTIMIZE FINAL:
  https://clickhouse.com/docs/best-practices/avoid-optimize-final
- Materialized views vs projections:
  https://clickhouse.com/docs/managing-data/materialized-views-versus-projections
- Query optimization:
  https://clickhouse.com/docs/optimize/query-optimization
- System tables:
  https://clickhouse.com/docs/operations/system-tables
- Releases and changelog:
  https://clickhouse.com/docs/whats-new/changelog

## Freshness triggers

Fetch current official docs when the task mentions `latest`, ClickHouse version numbers, Cloud vs self-managed behavior, MergeTree settings, object storage, async inserts, lightweight deletes, mutations, projections, materialized views, TTL, security, table engine behavior, or a system table/setting not present in local references.

## Troubleshooting-only sources

Use Stack Overflow, GitHub issues, forum posts, and community blogs only to troubleshoot observed failures or collect hypotheses. Confirm schema design, settings, engine behavior, and operational recommendations against ClickHouse docs or live cluster evidence.
