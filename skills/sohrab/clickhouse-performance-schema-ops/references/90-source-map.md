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

## Release evidence

Snapshot verified **2026-11-04**. ClickHouse's [official packages index](https://packages.clickhouse.com/)
lists **26.10.3.7 stable** (released 2026-10-25) and **26.8.36.3 LTS** (released 2026-10-26)
as patched releases for CVE-2026-116366. The amd64 Debian channel indexes independently
place them at the head of their respective channels. Recheck the channels when selecting a
version. The previous skill recorded a documentation review on 2026-07-26 and no engine pin.
The 26.7 release on 2026-07-22 is the earliest review boundary for this snapshot.

| Line | Upgrade checks from the [official 2026 changelog](https://clickhouse.com/docs/resources/changelogs/oss/2026) |
| --- | --- |
| 26.7, 2026-07-22 | Recheck aggregate dimensions and the new `AggregatingMergeTree` creation guard in `20-table-design.md`. Audit old deduplication hash settings before startup. If an explicitly configured legacy hash must preserve in-flight retries, use an intermediate release supporting `compatible_double_hashes` through the effective retry window, then remove the legacy setting before crossing 26.7. Check stored definitions for removed snowflake conversion functions. Audit storage identities for S3 user SQL and rotated system-log metadata before rollback below 26.3. |
| 26.8 LTS, 2026-08-27 | Recheck `INSERT SELECT` backfill part count and resource use because `max_insert_threads` defaults to auto. Verify JSON numeric timestamps and response-format precedence if the ingest path depends on them. Check `system.users.valid_until` type and `system.mutations.finish_time` before reusing diagnostics. Rehearse patch-part compatibility before using lightweight updates with mixed versions or rollback. See `50-mvs-projections-and-ttl.md` for projection and materialized-view changes. |
| 26.9, 2026-09-21 | Retire legacy analyzer configuration. Migrate CatBoost calls in stored keys, indexes, expressions and views, and remove old model privileges from all grant stores and access backups. Replace removed `WINDOW VIEW` syntax. Verify network codec and column compression separately. If persisted keys, indexes or TTLs use tuple subcolumns extracted from Variant, Dynamic, Nullable(Tuple), or untyped JSON paths, preserve their prior type before first startup using `allow_nullable_tuple_in_extracted_subcolumns=0` or the documented default-profile compatibility setting. A late setting change does not reattach detached parts. Check the Enum8 log-column migration for collectors. |
| 26.10, 2026-10-22 | Enable the analyzer on all old nodes before mixed-version queries. Check named-collection overrides, SQL-user login constraints, definer grants and the package seccomp policy before startup. Check bucketed `system.metric_log`, renamed span-log metadata and rotated tables against collectors. Review join spill thresholds, aggregate/array result semantics, null parsing, column TTL dependencies, and expression skip indexes on merging engines. Mutation validation is unconditional. `--ignore-error` may report SQL failures on stderr and exit successfully. |

Use the release notes for the exact changed settings and prerequisites. Before a real upgrade,
inventory the deployed schema, settings, grants, backup/restore requirements and client/server
versions. Prove every applicable change on disposable instances using the procedure in
`80-proof-and-validation.md`.

**WA2 compatibility.** The handed-off WA2 fixture reports **24.8.14.39** and image digest
`sha256:1ffa82edee000a42c09313bd9f1293d94c570aee74babc1b3ca9983a35fa597b`.
That earlier observation is scoped to the recorded fixture. This review examined sources.
Use 24.8-compatible SQL and settings for that fixture, and keep newer defaults, metadata,
syntax and server protections outside its acceptance. In particular, do not rely on the
26.7 aggregate-dimension guard or post-24.8 insert-deduplication defaults. For a planned
upgrade from 24.8, review all intervening notes starting from its actual pin.

## Claims this skill states, and the page that carries each one

The original source review was **2026-07-26**. Rows marked 2026-11-04 were verified in the
release refresh. Re-read and date the owning page before relying on a version-sensitive claim.

| Claim used in this skill | Page |
| --- | --- |
| `readonly=2` means "Read data and Change settings queries are allowed"; DDL is not among them | https://clickhouse.com/docs/operations/settings/permissions-for-queries |
| primary-key columns are chosen filter-first, correlation helps compression, and "4-5 [keys are] typically sufficient" | https://clickhouse.com/docs/best-practices/choosing-a-primary-key |
| partitioning "is primarily a data management technique and not a query optimization tool"; "fewer than 100 - 1,000 distinct values" is usually optimal; parts are never merged across partitions; `parts_to_throw_insert` and `max_parts_in_total` are the thresholds | https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key |
| a `Nullable` column "creates a separate column of `UInt8` type" that "has to be processed every time", and "almost always negatively affects performance"; `LowCardinality` suits "fewer than approximately 10,000 unique values" | https://clickhouse.com/docs/best-practices/select-data-types |
| insert "at least 1,000 rows, and ideally between 10,000–100,000 rows"; keep "around one insert query per second" | https://clickhouse.com/docs/optimize/bulk-inserts |
| async inserts suit many producers sending small payloads when client-side batching is not feasible; `wait_for_async_insert=0` gives "no guarantee the data will be persisted" | https://clickhouse.com/docs/optimize/asynchronous-inserts |
| Retry identity, window limits and view replay (release transition reviewed 2026-11-04) | https://clickhouse.com/docs/guides/developer/deduplicating-inserts-on-retries and the 2026 changelog, 26.1, 26.3, 26.6 and 26.7 |
| Explicit view security, definer privileges, partial insert failure and atomic population prerequisites (2026-11-04) | https://clickhouse.com/docs/reference/statements/create/view |
| Native-client environment credentials (2026-11-04) | https://clickhouse.com/docs/concepts/features/interfaces/client and https://github.com/ClickHouse/ClickHouse/blob/v24.8.14.39-lts/programs/client/Client.cpp |
| Per-replica mutation completion and diagnostics (2026-11-04) | https://clickhouse.com/docs/reference/system-tables/mutations and the 2026 changelog, 26.8 |
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
