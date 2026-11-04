# Proving a ClickHouse change

A ClickHouse change is not proved by a design argument. It is proved by an artifact somebody else
can re-run. What makes an artifact a test rather than a demonstration, and how strong a given proof
is: `/alaa-testing-strategy` `references/40-proof-strength.md`. This file
says which proof each change class needs and what evidence to paste.

## Gate 0: the reviewer, on every `CREATE TABLE`

Run the bundled checker from source with Python 3. Supply every target declaration and writer in
one invocation. Independently check bundle completeness against grants, producers, backfills and
operator rebuilds. Pass real target read SQL for each proposed shorter aggregate sparse key.

```bash
python3 -B "$SKILL_DIR/scripts/review_clickhouse_ddl.py" tables.sql writers.sql \
  --read-query reader.sql --read-query another-reader.sql
```

Omit `--read-query` when there is no shorter explicit aggregate key to justify. The option is
repeatable. Record each command, exit and finding. Exit 0 clears the admitted mechanical checks.
Exit 1 requires resolution of the findings. Exit 2 requires resolution of invalid input or unavailable
proof before acceptance. Findings printed with exit 2 still apply.

### Aggregate proof admitted by the checker

The checker compares merge identity and effective sparse index for `AggregatingMergeTree` and
`ReplicatedAggregatingMergeTree`. Supply explicit engine names. The checker accepts bare ASCII
identifiers or the same names in double quotes or backticks. Object names are case-sensitive.
Use consistent table qualification and unique names across tables and materialized views,
including declarations with `IF NOT EXISTS`. Reject a bare name that could bind a qualified
declaration with the same basename. Dots may separate identifiers but may not occur inside one
quoted identifier. Supply semicolon-delimited UTF-8 SQL and at least
one checkable table declaration. It reads SQL without executing it.

- Declare aggregate keys as bare columns, singly or as a parenthesized list. Use a trailing
  `PRIMARY KEY` clause for an explicit prefix. Inline and computed keys require separate review.
- Supply each writer as `CREATE MATERIALIZED VIEW … TO target AS SELECT … FROM source
  [WHERE …] GROUP BY …`. Use bare grouping columns or explicit, unambiguous `SELECT … AS name`
  aliases that resolve to stored target columns. Supply the source declaration for computed grouping
  aliases. A source column with the same name makes the binding ambiguous. Nested queries, joins,
  wildcards, grouping expressions and ordinals require separate proof.
- In an aggregate bundle, admit simple `CREATE DATABASE`, the two checked aggregate engines,
  local `MergeTree` tables, supported materialized views and direct inserts into declared local
  `MergeTree` targets. Other declared engines may forward writes and need separate proof.
  Schema or session mutations, `PARALLEL WITH`, table functions and direct aggregate writes return
  CH011. Review the actual SQL and its effects before accepting proof outside this subset.
- Supply a read as one `SELECT` from the named target, with `WHERE` or `PREWHERE`. Each supported
  predicate compares a bare target column to a string, number or `{name:Type}` parameter with a
  bare type name such as `UInt32`. Compound types such as `DateTime64(3)` and `Identifier` are
  outside the admitted grammar. Join the predicates with `AND`. Use equality for every index member before the last, and equality or a
  one-sided range comparison for the last. One statement must qualify on its own. The checker
  reports its file and line. Use `*`, bare column names or explicit `AS` outputs over atoms or
  a single function call over atoms. Atoms are bare names or the literals and parameters above.
  Trailing GROUP BY and ORDER BY may name columns, with optional ASC or DESC in ORDER BY.
  LIMIT may contain one non-negative integer. Implicit aliases, unrecognized identifier quoting
  or escapes, target-column aliases anywhere, disjunctions, nested queries and joins refuse proof.

The checker cannot discover missing SQL, validate general ClickHouse syntax or establish effective
permissions, deployment equivalence, pruning or merge behavior. It refuses unsupported proof
instead of certifying the bundle. Do not recast a query into invented evidence for a production path.

### Version scope

The lexical rules are version-independent. The disposable merge fixture uses cached ClickHouse
24.8.14.39 and synthetic rows. It compares grouped parity before merging and checks physical
rows and active parts after `OPTIMIZE FINAL`. For newer versions and effective compatibility
settings, use the CREATE-time guard guidance in `20-table-design.md` section 6.

## Proof required, by change class

| Change | Minimum proof | Evidence to paste |
| --- | --- | --- |
| adding or retyping a column on a table an ingest path writes | a row sent through the real ingest path arrives with the value populated, **and** a payload in the previous shape still inserts without error | the two `SELECT` results, before and after |
| changing `ORDER BY`, `PARTITION BY`, or a sort-key column's type | for changes requiring replacement, create the new table, backfill one full partition, and prove per-key parity. Use pre-aggregation inputs if the previous key lost dimensions. Metadata-only `MODIFY ORDER BY` supports a narrow new-column case and leaves the primary key unchanged. Verify the [official limits](https://clickhouse.com/docs/reference/statements/alter/order-by). | row counts and a grouped aggregate from both tables, plus `read_rows` for the target query on each |
| a new materialized view or rollup | backfill exactly one partition, compare its aggregates to the same aggregate computed from the source, then insert one new batch and show it lands in both | the two aggregate results and the post-insert delta |
| a query rewrite for performance | same result set, and lower `read_rows` and `read_bytes` for the same predicates and window | the two `system.query_log` rows |
| an engine change to a deduplicating or collapsing engine | a fixture containing a known duplicate or a known cancelling pair, read both with and without `FINAL` | both result sets |
| a settings change (`max_result_rows`, `max_execution_time`, a timeout) | a test that deliberately trips the new bound and asserts the error class the handler branches on | the test and its failing-path output |
| a new consumer query on the `chkit` lane | an automated test against a disposable ClickHouse, asserting the tenant predicate is present and the time range is bounded | the test run output |

`alaa-go-chi` already runs integration tests against a disposable ClickHouse
(`chkit/client_integration_test.go`), and `docs/CONSUMERS.md:23` records `wa-api` as passing
contract tests "local + disposable ClickHouse". A consumer-side query test has somewhere to run;
absence of a harness is not a reason to skip the proof.

## Recovering a rollup that lost dimensions

Recompute the affected range from trustworthy pre-aggregation history or replay. Prove coverage
before backfill and compare the recomputed measures by tenant, date, ID and discriminator. Compare
against source-grain results, because the damaged rollup no longer contains the original groups.
Missing history or a per-type discrepancy blocks cutover. Verify the live boundary with a writer
pause and drain or a proved disjoint range. Preserve the old table and declare rollback limits
before switching readers. Neither an engine upgrade nor switching back recreates lost history.
Use `50-mvs-projections-and-ttl.md` for live/backfill cutover.

## Compare bytes read, not wall time

For any performance claim, the number that belongs in the evidence is `read_rows` and `read_bytes`
from `system.query_log`. Wall time moves with page cache state, with concurrent load, and with which
replica answered. Bytes read is the quantity the schema and the query control, and it reproduces.

## Prove the deployed schema matches the declared schema

Because `CREATE TABLE IF NOT EXISTS` is a no-op against an existing table
(`10-authority-and-change-path.md`), a DDL file and a deployed table can disagree silently. After
any schema change, query `system.columns` for the table and compare the name, type, and default of
every column against the DDL file. Paste the difference, or paste the empty difference.

### What that check must assert once it runs in CI, and what a weaker one lets through

A gate that reports "converged" when it has not is worse than no gate, because a pipeline built on
it treats an unverified apply as a pass. `wa`'s schema job is the strongest shape in the fleet
today; copy it into any repository that owns ClickHouse DDL. Each assertion below exists because the
weaker version beside it passed something wrong.

| Assert this | The weaker version, and what it misses |
| --- | --- |
| after applying the DDL, diff `system.columns` **name and type** against a schema artifact derived from the commit under test (`<repo>/.gitlab-ci.yml:440-451`) | comparing column *counts*: a `MODIFY COLUMN` mutation killed mid-flight leaves the same count with the wrong type, and the count-only gate reports success |
| assert `count() FROM system.mutations WHERE is_done = 0` is zero for the database (`<repo>/.gitlab-ci.yml:453-455`) | trusting the DDL client's exit code: the client can abort on its own receive timeout while the mutation keeps running server-side, and the re-run then returns instantly as a metadata no-op |
| require the DDL file and every bundled copy of it to be byte-identical (`ddl_bundle_sync`, `<repo>/.gitlab-ci.yml:217-222`) | assuming two copies were edited together: an operator who applies the packaged copy then creates a different table from the one the repository declares |
| make the writer's rollout job depend on the schema job (`<repo>/.gitlab-ci.yml:472-477`) | ordering by convention: a writer rolled out ahead of its schema has its new fields discarded in silence, because the sink sets `skip_unknown_fields: true` (`<repo>/vector/wa-vector.yaml:635` and `:677`) |

Two properties make the first two assertions mean anything, and both are worth reproducing by name.
The expected schema is derived from the commit under test rather than carried over from a previous
run, so a drifted expectation cannot approve itself. And every credential and input the job needs is
asserted present rather than defaulted to an empty value, so a missing one exits non-zero instead of
applying as somebody else or asserting against nothing.

A repository whose only schema check is "the DDL applied without an error" has no gate; it has a log
line.

## State the rollback before applying, not after

Every ClickHouse change has a reverse, and some reverses are not the mirror of the forward
operation. Write down which one applies before touching anything:

| Forward change | Reverse |
| --- | --- |
| add a column | drop the column; storage returns as parts merge, not immediately |
| add a materialized view | drop the view; rows already written to its target table remain and must be dropped separately |
| add a projection | drop the projection; the base table is untouched |
| add a TTL | remove the TTL expression — but rows the TTL already deleted are gone and can only come back from re-ingestion |
| new table plus copy, to change a sort key | keep the old table until the parity check has passed and the read path has been switched and observed |
| a mutation (`ALTER … UPDATE` / `DELETE`) | **none.** Verified: mutations "can't be rolled back once submitted". The only recovery is re-ingestion or a backup restore, so name both before submitting |

A change whose reverse is "restore from backup" needs the backup verified before the change, not
assumed.

## Where this proof is recorded

Schema changes belong to the ingest-pipeline repository, so the evidence goes where that repository
keeps its decisions: the change, its reason, and the pasted proof, in the same effort. A schema
change merged without its decision entry leaves the next reader unable to tell a deliberate choice
from an accident. Design-before-code obligations and who may write:
`/alaa-system-design` (`$alaa-system-design`). The ten-point bar the finished change clears:
`/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md`.
