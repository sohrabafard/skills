# Source map and freshness

Official ClickHouse documentation outranks blogs, conference talks, issue threads, Stack Overflow
answers, and this skill. When the two disagree, the documentation wins and this file is wrong and
must be corrected.

## Fetch a current page before answering when the task involves

a ClickHouse version number or the word "latest"; ClickHouse Cloud versus self-managed behaviour; a
default value for any setting; merge-tree settings; object storage or tiered storage; async inserts;
lightweight deletes; mutations; projections; materialized views; TTL; replication or Keeper;
security, roles, or grants; or any system table or setting this skill does not name. Defaults and
engine behaviour change between releases, and a number quoted without a date is a number nobody can
audit.

## Claims this skill states, and the page that carries each one

Every row was fetched and read on **2026-07-26**. Re-read the page before repeating the claim if
that date is more than a release cycle old; record the new date here when you do.

| Claim used in this skill | Page |
| --- | --- |
| `readonly=2` means "Read data and Change settings queries are allowed"; DDL is not among them | https://clickhouse.com/docs/operations/settings/permissions-for-queries |
| primary-key columns are chosen filter-first, correlation helps compression, and "4-5 [keys are] typically sufficient" | https://clickhouse.com/docs/best-practices/choosing-a-primary-key |
| partitioning "is primarily a data management technique and not a query optimization tool"; "fewer than 100 - 1,000 distinct values" is usually optimal; parts are never merged across partitions; `parts_to_throw_insert` and `max_parts_in_total` are the thresholds | https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key |
| a `Nullable` column "creates a separate column of `UInt8` type" that "has to be processed every time", and "almost always negatively affects performance"; `LowCardinality` suits "fewer than approximately 10,000 unique values" | https://clickhouse.com/docs/best-practices/select-data-types |
| insert "at least 1,000 rows, and ideally between 10,000–100,000 rows"; keep "around one insert query per second" | https://clickhouse.com/docs/optimize/bulk-inserts |
| async inserts suit many producers sending small payloads when client-side batching is not feasible; `wait_for_async_insert=0` gives "no guarantee the data will be persisted" | https://clickhouse.com/docs/optimize/asynchronous-inserts |
| block deduplication is "enabled by default" for `*ReplicatedMergeTree` and not for non-replicated engines, where `non_replicated_deduplication_window` controls it; `insert_deduplication_token` replaces the data hash | https://clickhouse.com/docs/concepts/features/operations/insert/deduplicating-inserts-on-retries |
| mutations "rewrite entire data parts affected by the change", "can't be rolled back once submitted", and `ReplacingMergeTree` or `CollapsingMergeTree` are the recommended alternatives | https://clickhouse.com/docs/best-practices/avoid-mutations |
| `OPTIMIZE FINAL` merges "all active parts into a single part", ignores the ~150 GB merge safeguard, and is sanctioned only for "finalizing data before freezing a table or exporting" | https://clickhouse.com/docs/best-practices/avoid-optimize-final |
| projections are optimizer-selected and auto-maintained but cannot join, filter their definition, chain, serve `FINAL`, or run on non-MergeTree; materialized views can filter, join, chain, and target any engine but "don't automatically react to `UPDATE` or `DELETE`" | https://clickhouse.com/docs/managing-data/materialized-views-versus-projections |
| lightweight `DELETE` is "implemented as a mutation that marks rows as deleted", uses the hidden `_row_exists` column, removes rows physically only "during the next merge", and is synchronous by default | https://clickhouse.com/docs/guides/developer/lightweight-delete |
| an overflow-mode setting is `throw` (default, raises an exception) or `break` ("stop executing the query and return the partial result, as if the source data ran out") | https://clickhouse.com/docs/operations/settings/query-complexity |
| `ReplicatedMergeTree` needs ClickHouse Keeper or ZooKeeper 3.4.5+; replication is per table; `CREATE`, `DROP`, `ATTACH`, `DETACH`, `RENAME` are not replicated; `ATTACH TABLE … AS REPLICATED` converts an existing table | https://clickhouse.com/docs/engines/table-engines/mergetree-family/replication |

## Unverified, and marked as such

- The exact default values of `max_execution_time`, `max_result_rows`, `result_overflow_mode`, and
  `timeout_overflow_mode` were **not** obtainable from the query-complexity page as fetched on
  2026-07-26; only the overflow-mode semantics were. Read the effective values from
  `system.settings` on the target server rather than quoting a default.
- Whether `result_overflow_mode = break` can return slightly more rows than `max_result_rows`
  because results are produced in whole blocks is **unverified**; do not state it either way.

## General landing pages

- Best-practices index: https://clickhouse.com/docs/best-practices
- MergeTree engine family: https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
- Data-skipping indexes: https://clickhouse.com/docs/optimize/skipping-indexes
- Query optimization: https://clickhouse.com/docs/optimize/query-optimization
- System tables: https://clickhouse.com/docs/operations/system-tables
- Changelog: https://clickhouse.com/docs/whats-new/changelog

## Repository sources this skill reads

`alaa-go-chi` for the consumer read lane (its `chkit/`, `configkit/keys.go`, and `docs/CONSUMERS.md`),
and the ingest-pipeline repository `wa` for the data model (`<repo>/clickhouse/ddl/`,
`<repo>/vector/`, `<repo>/docs/DECISIONS.md`, `<repo>/samples/`). Read the source file, never a summary of it: a decision log records what a team chose,
and the code records what runs. Where they differ, the code is the fact and the difference is the
finding.

## Community sources

Usable to form a hypothesis about an observed failure, and for nothing else. Confirm against a page
above or against evidence from the cluster in front of you before any of it becomes a
recommendation, and say which one confirmed it.
