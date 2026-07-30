# Proving a ClickHouse change

A ClickHouse change is not proved by a design argument. It is proved by an artifact somebody else
can re-run. What makes an artifact a test rather than a demonstration, and how strong a given proof
is: `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md`. This file
says which proof each change class needs and what evidence to paste.

## Gate 0: the reviewer, on every `CREATE TABLE`

Run `scripts/review_clickhouse_ddl.py` over the DDL and paste its output into the answer, including
the run that produced no findings. Its exit codes and what each one obliges you to do are in its
`--help`. It checks the mechanical rules from `20-table-design.md` and prints what it cannot check;
a clean run is a floor, not a pass.

## Proof required, by change class

| Change | Minimum proof | Evidence to paste |
| --- | --- | --- |
| adding or retyping a column on a table an ingest path writes | a row sent through the real ingest path arrives with the value populated, **and** a payload in the previous shape still inserts without error | the two `SELECT` results, before and after |
| changing `ORDER BY`, `PARTITION BY`, or a sort-key column's type | this cannot be done in place: create the new table, copy one full partition, and show per-key aggregate parity against the source | row counts and a grouped aggregate from both tables, plus `read_rows` for the target query on each |
| a new materialized view or rollup | backfill exactly one partition, compare its aggregates to the same aggregate computed from the source, then insert one new batch and show it lands in both | the two aggregate results and the post-insert delta |
| a query rewrite for performance | same result set, and lower `read_rows` and `read_bytes` for the same predicates and window | the two `system.query_log` rows |
| an engine change to a deduplicating or collapsing engine | a fixture containing a known duplicate or a known cancelling pair, read both with and without `FINAL` | both result sets |
| a settings change (`max_result_rows`, `max_execution_time`, a timeout) | a test that deliberately trips the new bound and asserts the error class the handler branches on | the test and its failing-path output |
| a new consumer query on the `chkit` lane | an automated test against a disposable ClickHouse, asserting the tenant predicate is present and the time range is bounded | the test run output |

`alaa-go-chi` already runs integration tests against a disposable ClickHouse
(`chkit/client_integration_test.go`), and `docs/CONSUMERS.md:23` records `wa-api` as passing
contract tests "local + disposable ClickHouse". A consumer-side query test has somewhere to run;
absence of a harness is not a reason to skip the proof.

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
