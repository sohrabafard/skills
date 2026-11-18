# Source map and freshness

Official ClickHouse documentation and the behaviour of the floor binary outrank blogs, talks, issue
threads, forum answers, and this skill. When they disagree with this file, this file is wrong;
correct it.

Use a community source only to form a hypothesis about an observed failure. Confirm it against a
page below or against evidence from the server in front of you before it becomes a recommendation,
and say which one confirmed it.

## Fetch a current page before you answer when the task involves

a ClickHouse version number or the word "latest"; ClickHouse Cloud versus self-managed behaviour; a
default value this file does not list; merge-tree settings; object or tiered storage; async inserts;
lightweight deletes or updates; mutations; projections; materialized views; TTL; replication or
Keeper; security, roles, or grants; or a system table or setting this skill does not name.

## Release evidence

**Floor: ClickHouse 26.8.39.19, the 26.8 LTS line.** The owner set it on 2026-11-18 and supports no
server below it. Image `clickhouse/clickhouse-server:26.8.39-alpine`, digest
`sha256:96e3f95c3110fd50626c3f45e060aa4ad5ca0f1169cd00c89d6aaf5a946c85f9`, pulled and cached in the
fleet registry on that date. The floor includes the fix for CVE-2026-116366, first shipped on this
line in 26.8.36.3.

On 2026-11-18 the [official packages index](https://packages.clickhouse.com/) listed 26.8.39.19 at
the head of the LTS channel and 26.10.5.57 at the head of the stable channel. Recheck the channels
when you select a version. A patch release on the 26.8 line replaces the floor only by an owner
decision recorded here with its date.

## Defaults at the floor

Read on 2026-11-18 from `system.settings`, `system.merge_tree_settings` and
`system.server_settings` of the floor image with `clickhouse local`. A profile, a table `SETTINGS`
clause or a `compatibility` value overrides each one, so read the effective value on the target.

| Setting | Default | Kind |
| --- | --- | --- |
| `async_insert`, `wait_for_async_insert` | `1`, `1` | query |
| `async_insert_busy_timeout_max_ms`, `async_insert_max_data_size` | `200`, `10485760` | query |
| `deduplicate_insert`, `deduplicate_blocks_in_dependent_materialized_views` | `enable`, `1` | query |
| `non_replicated_deduplication_window` | `0`, which disables deduplication | merge-tree |
| `replicated_deduplication_window`, `replicated_deduplication_window_seconds` | `10000` blocks, `3600` s | merge-tree |
| `replicated_deduplication_window_for_async_inserts`, `…_seconds_for_async_inserts` | `10000` blocks, `604800` s | merge-tree |
| `insert_quorum`, `insert_quorum_parallel`, `select_sequential_consistency` | `0`, `1`, `0` | query |
| `max_execution_time`, `max_result_rows` | `0`, `0`: no limit | query |
| `result_overflow_mode`, `timeout_overflow_mode` | `throw`, `throw` | query |
| `parts_to_delay_insert`, `parts_to_throw_insert`, `max_parts_in_total` | `1000`, `3000`, `100000` | merge-tree |
| `max_bytes_to_merge_at_max_space_in_pool` | `161061273600` (150 GiB) | merge-tree |
| `allow_dimensions_outside_sorting_key` | `0` | merge-tree |
| `materialized_views_populate_atomically` | `1` | query |
| `lightweight_deletes_sync`, `mutations_sync` | `2`, `0` | query |
| `lightweight_mutation_projection_mode`, `deduplicate_merge_projection_mode` | `throw`, `throw` | merge-tree |
| `max_insert_threads` | `auto` | query |
| `default_replica_path`, `default_replica_name` | `/clickhouse/tables/{uuid}/{shard}`, `{replica}` | server |
| `distributed_ddl_output_mode` | `throw` | query |

The floor binary lists every `Replicated*MergeTree` engine and the `Replicated` database engine. It
lists no `SharedMergeTree`; that engine is ClickHouse Cloud only.

## Releases past the floor

Before a server moves past the 26.8 line, read every release note from the deployed version to the
target in the [official 2026 changelog](https://clickhouse.com/docs/resources/changelogs/oss/2026).
Inventory the deployed schema, settings, grants, backup and restore requirements, and client and
server versions. Prove each applicable change on a disposable instance with
`80-proof-and-validation.md`. Checks already known, reviewed 2026-11-04:

| Line | Check before the upgrade |
| --- | --- |
| 26.9, 2026-09-21 | Retire legacy analyzer configuration. Migrate CatBoost calls in stored keys, indexes, expressions and views, and remove old model privileges from every grant store and access backup. Replace removed `WINDOW VIEW` syntax. Implicit MergeTree column compression becomes size-dependent at write time; verify network codec and column compression separately. If a persisted key, index or TTL uses a tuple subcolumn extracted from `Variant`, `Dynamic`, `Nullable(Tuple)` or an untyped JSON path, preserve its prior type before the first startup with `allow_nullable_tuple_in_extracted_subcolumns=0` or the documented default-profile compatibility setting; a late change does not reattach detached parts. Check the `Enum8` log-column migration for collectors. `REFRESH … APPEND INCREMENTAL` becomes available for one plain MergeTree source; check its block-number and block-offset settings and prove refresh progress and reconciliation after a failed refresh before you choose it. |
| 26.10, 2026-10-22 | Enable the analyzer on every old node before mixed-version queries. Check named-collection overrides, SQL-user login constraints, definer grants and the package seccomp policy before startup; effective settings constraints can refuse a login, so prove login and grants for the migration, writer and reader identities. Check bucketed `system.metric_log`, renamed span-log metadata and rotated tables against collectors. Review join spill thresholds, aggregate and array result semantics, and expression skip indexes on merging engines. `input_format_null_as_default=0` rejects JSON null for a non-nullable numeric column, and `ALTER ADD/MODIFY COLUMN` honours `data_type_default_nullable`. Query-time `FINAL` on `SummingMergeTree` keeps rows whose summed columns are all zero, while merges still remove them; filter after summing if the result contract excludes all-zero groups. A TTL reset recomputes dependent `MATERIALIZED` columns; an undefined result can block the TTL merge. Mutation validation is unconditional. `--ignore-error` can report SQL failures on stderr and still exit successfully. |

## Claims this skill states, and the source of each

Rows without a date were reviewed 2026-07-26. Re-read and date the source before you rely on a
version-sensitive claim.

| Claim | Source |
| --- | --- |
| `readonly=2` allows reads and setting changes and no DDL; a non-`POST` HTTP request runs read-only (2026-11-18) | https://clickhouse.com/docs/operations/settings/permissions-for-queries |
| filter-first primary-key columns; "4-5 [keys are] typically sufficient" | https://clickhouse.com/docs/best-practices/choosing-a-primary-key |
| partitioning is a data-management technique; "fewer than 100 - 1,000 distinct values"; parts never merge across partitions | https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key |
| a `Nullable` column "creates a separate column of `UInt8` type"; `LowCardinality` suits "fewer than approximately 10,000 unique values" | https://clickhouse.com/docs/best-practices/select-data-types |
| "at least 1,000 rows, and ideally between 10,000–100,000 rows"; "around one insert query per second" | https://clickhouse.com/docs/optimize/bulk-inserts |
| `wait_for_async_insert=0` gives "no guarantee the data will be persisted" | https://clickhouse.com/docs/optimize/asynchronous-inserts |
| plain `MergeTree` deduplicates nothing until its window is positive; a retry must repeat the same data, order and settings; dependent views deduplicate (2026-11-18) | https://clickhouse.com/docs/guides/developer/deduplicating-inserts-on-retries |
| view security, definer privileges, partial insert failure, atomic population prerequisites (2026-11-04) | https://clickhouse.com/docs/reference/statements/create/view |
| native-client environment credentials (2026-11-04) | https://clickhouse.com/docs/concepts/features/interfaces/client |
| per-replica mutation completion and `finish_time` (2026-11-04) | https://clickhouse.com/docs/reference/system-tables/mutations |
| mutations "rewrite entire data parts", "can't be rolled back once submitted" | https://clickhouse.com/docs/best-practices/avoid-mutations |
| `OPTIMIZE FINAL` merges "all active parts into a single part", ignores the merge-size safeguard, and suits only "finalizing data before freezing a table or exporting" | https://clickhouse.com/docs/best-practices/avoid-optimize-final |
| projection and materialized-view capabilities and limits | https://clickhouse.com/docs/managing-data/materialized-views-versus-projections |
| lightweight `DELETE` marks rows through `_row_exists` and removes them at a later merge | https://clickhouse.com/docs/guides/developer/lightweight-delete |
| overflow mode `break` will "stop executing the query and return the partial result, as if the source data ran out" | https://clickhouse.com/docs/operations/settings/query-complexity |
| without Keeper "you can't create replicated tables, and any existing replicated tables will be read-only"; an `INSERT` throws while Keeper is unavailable and `SELECT` does not use it; which statements replicate; conversion by `ATTACH TABLE … AS REPLICATED` or the `convert_to_replicated` flag; default engine arguments (2026-11-18) | https://clickhouse.com/docs/engines/table-engines/mergetree-family/replication |
| Keeper runs standalone or "as an internal part of the ClickHouse server"; a 3-node cluster keeps working "if only 1 node crashes" (2026-11-18) | https://clickhouse.com/docs/guides/sre/keeper/clickhouse-keeper |
| the `Replicated` database replicates metadata only (2026-11-18) | https://clickhouse.com/docs/engines/database-engines/replicated |
| HTTP query parameters, credential headers, session rules, and "a HTTP 200 response code doesn't guarantee that a query was successful" (2026-11-18) | https://clickhouse.com/docs/interfaces/http |
| ClickHouse maintains no listed PHP client (2026-11-18) | https://clickhouse.com/docs/interfaces/third-party/client-libraries |
| quorum inserts and `select_sequential_consistency` requiring `insert_quorum_parallel` off (2026-11-18) | setting descriptions in `system.settings` of the floor binary |

## Stated without an official source

- That a materialized view does not fire for parts a replica fetches, and that two Keeper voters
  survive no loss, follow from the engine's insert-trigger and majority-quorum design. Neither was
  read from a page on 2026-11-18. Confirm the first on a disposable two-replica instance before a
  design depends on it.
- Observed on the floor binary on 2026-11-18 with `clickhouse local`: a repeated synchronous insert
  into a plain `MergeTree` table doubled the rows without a window and did not with
  `non_replicated_deduplication_window = 100`. Whether the window also covers an asynchronous insert
  into a plain `MergeTree` table is unverified; the description of `deduplicate_insert` names
  `Replicated*` tables. Do not state it either way.
- Whether `result_overflow_mode = break` can return slightly more rows than `max_result_rows` is
  unverified; do not state it either way.

## General landing pages

- Best-practices index: https://clickhouse.com/docs/best-practices
- MergeTree engine family: https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree
- Data-skipping indexes: https://clickhouse.com/docs/optimize/skipping-indexes
- Query optimization: https://clickhouse.com/docs/optimize/query-optimization
- System tables: https://clickhouse.com/docs/operations/system-tables
- Changelog: https://clickhouse.com/docs/whats-new/changelog

## Repository sources this skill reads

`alaa-go-chi` for the Go read lane (`chkit/`, `configkit/keys.go`, `docs/CONSUMERS.md`), read at
commit `6abc1d4` on 2026-11-18. The ingest-pipeline repository `wa` for the data model
(`<repo>/clickhouse/ddl/`, `<repo>/vector/`, `<repo>/docs/DECISIONS.md`), read at commit `953dc32`
on 2026-11-18: the sink batch values, and decision sections 1, 3, 5, 10, 15.1, 29, 30 and 31. `wa`
moves faster than this skill; re-read a cited section before you repeat it. Read the source file,
never a summary of it. A decision log records what a team chose, and the code records what runs;
where they differ, the code is the fact and the difference is the finding.
