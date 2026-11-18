# Proving a ClickHouse change

An artifact that someone else can re-run proves a ClickHouse change; a design argument does not.
Proof strength: `/alaa-testing-strategy` `references/40-proof-strength.md`. This file states which
proof each change class needs and what evidence to paste.

## Gate 0: the checker, on every `CREATE TABLE`

Supply every target declaration and every writer in one invocation. Check the completeness of that
bundle yourself against grants, producers, backfills and operator rebuilds. Pass the real target
read SQL for each shorter aggregate sparse key you propose; omit `--read-query` when there is none.

```bash
python3 -B "$SKILL_DIR/scripts/review_clickhouse_ddl.py" tables.sql writers.sql \
  --read-query reader.sql --read-query another-reader.sql
```

Record each command, exit code and finding. Exit 0 clears the admitted mechanical checks. Exit 1
obliges you to resolve every finding before the DDL is applied. Exit 2 obliges you to resolve the
invalid input or the unavailable proof before acceptance; findings printed with exit 2 still apply.
`--help` lists the checks and what the tool does not check.

### What the checker admits as aggregate proof

The checker reads SQL and executes none. It compares merge identity and effective sparse index for
`AggregatingMergeTree` and `ReplicatedAggregatingMergeTree`. Outside the subset below it returns
CH011 and refuses proof; review the actual SQL and its effects yourself, and never recast a
production query into a shape the checker accepts.

- **Input.** Semicolon-delimited UTF-8 SQL with at least one checkable table declaration and
  explicit engine names. Identifiers are bare ASCII, or the same names in double quotes or
  backticks, and are case-sensitive. Qualify tables consistently, and keep names unique across
  tables and materialized views. A bare name that could bind a qualified declaration with the same
  basename is rejected. A dot never occurs inside one quoted identifier.
- **Keys.** Aggregate keys are bare columns, single or in a parenthesized list, with a trailing
  `PRIMARY KEY` clause for an explicit prefix. Inline and computed keys need separate review.
- **Writers.** Each writer is `CREATE MATERIALIZED VIEW … TO target AS SELECT … FROM source
  [WHERE …] GROUP BY …`. Group by bare columns, or by explicit `SELECT … AS name` aliases that
  resolve to stored target columns without ambiguity. Supply the source declaration for a computed
  grouping alias; a source column with the same name makes the binding ambiguous. Nested queries,
  joins, wildcards, grouping expressions and ordinals need separate proof.
- **Bundle.** An aggregate bundle may hold simple `CREATE DATABASE`, the two checked aggregate
  engines, local `MergeTree` tables, supported materialized views and direct inserts into declared
  local `MergeTree` targets. Other declared engines can forward writes and need separate proof.
  Schema or session mutations, `PARALLEL WITH`, table functions and direct aggregate writes return
  CH011.
- **Reads.** A read is one `SELECT` from the named target with `WHERE` or `PREWHERE`. Each predicate
  compares a bare target column with a string, a number or a `{name:Type}` parameter whose type is
  a bare name such as `UInt32`; `DateTime64(3)` and `Identifier` are outside the grammar. Join
  predicates with `AND`. Use equality on every index member before the last, and equality or a
  one-sided range on the last. One statement must qualify on its own. Outputs are `*`, bare columns,
  or explicit `AS` outputs over atoms or one function call over atoms. Trailing `GROUP BY` and
  `ORDER BY` name columns, and `LIMIT` holds one non-negative integer. Implicit aliases, aliases of
  target columns, disjunctions, nested queries and joins refuse proof.

The checker cannot find missing SQL, validate general ClickHouse syntax, or establish effective
permissions, deployment equivalence, pruning or merge behaviour. Its rules are lexical and do not
depend on the server version. The server-side guard for aggregate dimensions: `20-table-design.md`
section 6.

## Proof required, by change class

| Change | Minimum proof | Evidence to paste |
| --- | --- | --- |
| a column added or retyped on a table an ingest path writes | a row sent through the real ingest path arrives with the value populated, **and** a payload in the previous shape still inserts without error | the two `SELECT` results, before and after |
| a change of `ORDER BY`, `PARTITION BY`, or the type of a sort-key column | for a change that needs replacement: create the new table, backfill one full partition, and prove per-key parity, from pre-aggregation inputs if the previous key lost dimensions. Metadata-only `MODIFY ORDER BY` covers a narrow new-column case and leaves the primary key unchanged; verify the [official limits](https://clickhouse.com/docs/reference/statements/alter/order-by) | row counts and a grouped aggregate from both tables, plus `read_rows` for the target query on each |
| a new materialized view or rollup | backfill exactly one partition, compare its aggregates with the same aggregate computed from the source, then insert one new batch and show it lands in both | the two aggregate results and the post-insert delta |
| a query rewrite for performance | the same result set, and lower `read_rows` and `read_bytes` for the same predicates and window | the two `system.query_log` rows |
| an engine change to a deduplicating or collapsing engine | a fixture with a known duplicate or a known cancelling pair, read with and without `FINAL` | both result sets |
| a deduplication window or an insert quorum | the same insert replayed through the real writer after a lost acknowledgement; the row count in the source and the aggregates in every view target stay unchanged | the counts before and after the replay |
| a table that moves to `Replicated*`, or a replica that is added | per-partition row counts and one grouped aggregate equal on every replica, and `system.replicas` shows no read-only replica and an empty queue | the per-replica results |
| a settings change (`max_result_rows`, `max_execution_time`, a timeout) | a test that trips the new bound on purpose and asserts the error class the handler branches on | the test and its failing-path output |
| a new consumer query on a read lane | an automated test against a disposable ClickHouse at the floor that asserts the tenant predicate is present and the time range is bounded | the test run output |

`alaa-go-chi` already runs integration tests against a disposable ClickHouse
(`chkit/client_integration_test.go`). A consumer-side query test has somewhere to run; a missing
harness is no reason to skip the proof.

## Recovering a rollup that lost dimensions

Recompute the affected range from trustworthy pre-aggregation history or from replay. Prove coverage
before the backfill, and compare the recomputed measures by tenant, date, identifier and
discriminator against source-grain results, because the damaged rollup no longer holds the original
groups. Missing history or a per-type discrepancy blocks the cutover. Verify the live boundary with
a writer pause and drain, or with a proved disjoint range (`50-mvs-projections-and-ttl.md`). Keep the
old table and declare the rollback limits before you switch readers. Neither an engine upgrade nor a
switch back recreates lost history.

## Compare bytes read, not wall time

For a performance claim, the evidence is `read_rows` and `read_bytes` from `system.query_log`. Wall
time moves with page-cache state, concurrent load and the replica that answered. Bytes read is the
quantity the schema and the query control, and it reproduces.

## Prove the deployed schema matches the declared schema

`CREATE TABLE IF NOT EXISTS` does nothing against an existing table, so a DDL file and a deployed
table can disagree with no error. After every schema change, compare the name, type and default of
every column in `system.columns` with the DDL file, on every replica. Paste the difference, or the
empty difference.

A repository that owns ClickHouse DDL runs that comparison in CI. Copy the shape of `wa`'s schema
job in `<repo>/.gitlab-ci.yml`. Each assertion exists because the weaker version passed something
wrong:

| Assert this | The weaker version, and what it misses |
| --- | --- |
| after the DDL is applied, diff `system.columns` **name and type** against a schema artifact derived from the commit under test | a column count: a `MODIFY COLUMN` mutation killed mid-flight leaves the same count with the wrong type |
| `count() FROM system.mutations WHERE is_done = 0` is zero for the database | the DDL client's exit code: the client can abort on its receive timeout while the mutation runs on, and the re-run returns at once as a metadata no-op |
| the DDL file and every bundled copy of it are byte-identical | trust that two copies were edited together: an operator who applies the packaged copy creates a different table |
| the writer's rollout job depends on the schema job | ordering by convention: a writer rolled out before its schema has its new fields dropped in silence, because the sink skips unknown fields |

Derive the expected schema from the commit under test, never from a previous run, so a drifted
expectation cannot approve itself. Assert every credential and input the job needs as present, never
default one to empty, so a missing value exits non-zero.

## State the rollback before you apply

Some reverses are not the mirror of the forward operation. Write down the one that applies first:

| Forward change | Reverse |
| --- | --- |
| add a column | drop the column; storage returns as parts merge, not at once |
| add a materialized view | drop the view; drop the rows already in its target table separately |
| add a projection | drop the projection; the base table is untouched |
| add a TTL | remove the TTL expression; rows it deleted return only by re-ingest |
| new table plus copy, to change a sort key | keep the old table until parity passed and the switched read path was observed |
| convert a table to `Replicated*` | none in place; keep a verified backup or the re-ingest path |
| a mutation | **none.** Recovery is re-ingest or a backup restore; name both before you submit it |

A change whose reverse is "restore from backup" needs the backup verified before the change.

## Where this proof is recorded

Schema changes belong to the ingest-pipeline repository. Put the change, its reason and the pasted
proof in that repository's decision log in the same effort, so the next reader can tell a deliberate
choice from an accident. Design-before-code obligations: `/alaa-system-design`. The quality bar the
finished change clears: `/alaa-project-constitution` `references/quality-bar.md`.
