# Authority and the change path

## Who may run DDL

**The ingest-pipeline repository owns the data model.** It holds `<repo>/clickhouse/ddl/`, the
`<repo>/vector/` topology whose sinks write those tables, and `<repo>/docs/DECISIONS.md`, which
ratifies each schema choice with its reason. On this fleet that repository is `wa`
(`15-fleet-clickhouse-boundary.md`). Every DDL right lives there: database and table creation,
column type, `ORDER BY`, `PARTITION BY`, engine, codec, and retention.

**A service on a read lane holds no DDL right.** For a Go service, `alaa-go-chi` enforces this in
three places:

- `chkit/config.go` pins `readonly`, `max_execution_time` and `max_result_rows` on every session,
  and records the `readonly=2` pin as a kit invariant that `Config` cannot weaken. The official
  meaning of `readonly=2` is that reads and setting changes are allowed and DDL is not.
- `chkit/client.go` exports `NewClient`, `Ping`, `Query`, `QueryRow`, `Close`, and `PoolStats`, and
  no `Exec`.
- `chkit/client_integration_test.go` issues a `CREATE TABLE` over the lane and fails if it succeeds.

The kit ships no ClickHouse schema: no table engine, no materialized view, no migration. A plan in
which the kit creates a rollup describes something that does not exist. Say so and route the request
to the ingest pipeline. A PHP service has no kit; `85-access-and-configuration.md` states how its
lane gets the same limits.

## Which deliverable each audience gets

| The requester is | Deliverable | Never |
| --- | --- | --- |
| the ingest-pipeline repository | DDL, the `<repo>/docs/DECISIONS.md` entry that ratifies it, and the output of `scripts/review_clickhouse_ddl.py` | a change to a consumer's code |
| a service on a read lane | a `SELECT` against an existing rollup, a written rollup request filed against the ingest pipeline that names the columns and grain, or a lane configuration change | DDL, an `ALTER`, a `TRUNCATE`, or an `OPTIMIZE` |

When you cannot tell which audience the task is in, ask which repository will hold the resulting
file, and stop until that is answered. DDL for a requester who cannot apply it wastes the review and
hides the real dependency.

## Reporting a defect in a table you do not own

State the file and line, the rule it violates, the failure the violation produces, and the replacement. Do
not edit the file, and do not open a change against the owning repository from inside this task.
That repository ratifies its schema in its own decision log, and an edit that skips the log is a
change the next reader cannot audit.

## Editing bootstrap DDL in place, and when that stops

`wa` edits its bootstrap DDL directly. It has no migration tool, no version table and no ordered
migration directory. That is safe only while both conditions hold:

1. Every statement in the DDL file is `CREATE … IF NOT EXISTS`, so the file reproduces the declared
   schema on a fresh database.
2. Every environment that holds rows can be dropped and re-ingested from the upstream source, or
   holds only rows the owner has written off.

`CREATE TABLE IF NOT EXISTS` does nothing when the table exists. A column added to the file after the
first deployment therefore never reaches a deployed table, and nothing errors. While condition 2
holds, a change to an existing table reaches a deployment only when the database is dropped and
recreated, because re-running the file leaves that table as it was. Dropping a database destroys
rows: do it on your own local instance only, and ask the table owner for explicit approval before
any shared environment. On `wa` the reset is `--re-init`, which `<repo>/docs/DECISIONS.md` sections
15.1 and 31 gate behind an environment flag and an interactive confirmation; an agent cannot run it
and asks the operator.

Direct editing ends at **the first environment whose rows cannot be re-ingested from the upstream
source.** By then these artifacts must exist:

- an ordered migration directory in which each file is applied exactly once and its application is
  recorded in a table inside the same ClickHouse instance;
- a CI check that compares the deployed schema with the declared schema and fails on a difference
  (`80-proof-and-validation.md`);
- a documented procedure for the changes ClickHouse cannot perform in place: a change of
  `ORDER BY`, of `PARTITION BY`, or of the type of a sort-key column. Each needs a new table and a
  data move, not an `ALTER`.

## Retention on this pipeline is decided: never delete

`<repo>/docs/DECISIONS.md` section 30 ratifies that WA analytics data is retained indefinitely, with
no TTL on either raw table, because historical heatmaps and growth rates need the retained
history. Do not add a TTL clause to a table on this pipeline, do not propose one, and do not report
its absence as a gap.

Do report the consequence the same decision names: stored data grows without a time limit. The
decision log still leaves backup and recovery of the stored rows to the reliability owner. TTL
mechanics for a pipeline whose owner decided differently: `50-mvs-projections-and-ttl.md`.
