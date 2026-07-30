# Authority and the change path

## The two audiences, and the evidence for each

**The ingest-pipeline repository** owns the ClickHouse data model. It is the repository that
contains a `<repo>/clickhouse/ddl/` directory creating the analytics database and its tables, a
`<repo>/vector/` topology whose sinks write into those tables, and a `<repo>/docs/DECISIONS.md` in
which each schema choice is ratified with its reason. **On this fleet that repository is `wa`**, and
it creates the `wa_raw` database with `wa_raw.events_raw` (`<repo>/clickhouse/ddl/001_init.sql:26`)
and `wa_raw.watch_segments_raw` (`:160`), plus the `wa_agg` rollups in
`<repo>/clickhouse/ddl/002_agg.sql`. Every DDL right lives there: database and table creation,
column type, `ORDER BY`, `PARTITION BY`, engine, codec, retention. What `wa` holds, and which
ClickHouse tables are outside this skill altogether: `15-fleet-clickhouse-boundary.md`.

**A kit consumer on the `chkit` read lane** holds no DDL right at all, and this is enforced in
three independent places in `alaa-go-chi`:

- `chkit/config.go:128-132` pins `Settings{"readonly": 2, "max_execution_time": …,
  "max_result_rows": …}` on every session. The official ClickHouse definition of `readonly=2` is
  "Read data and Change settings queries are allowed" — writes and DDL are not.
- `chkit/config.go:109-110` records the `readonly=2` pin as a kit invariant that "cannot be
  weakened through Config", so a consumer cannot opt out by configuration.
- `chkit/client.go` exports `NewClient`, `Ping`, `Query`, `QueryRow`, `Close`, and `PoolStats`, and
  no `Exec`. There is no method through which a consumer submits a statement that changes state.
- `chkit/client_integration_test.go:114-127` issues `CREATE TABLE chkit_it.should_not_exist (x
  UInt8) ENGINE = Memory` over the lane and calls `t.Fatal` if it succeeds. The prohibition is
  tested, not merely documented.

`chkit/doc.go:16-17` states the boundary in the kit's own words: "Rollup/materialized-view design
is owned by the ingest pipeline, not this package."

**The kit ships no ClickHouse schema surface whatsoever.** `alaa-go-chi` contains zero occurrences
of `MergeTree`, zero of `MATERIALIZED VIEW`, no ClickHouse `.sql` file, and no migration embed in
`chkit`. A plan that says "the kit will create the rollup" is describing something that does not
exist; say so and route the request to the ingest pipeline instead.

## Which deliverable each audience gets

| The requester is | Deliverable | Never |
| --- | --- | --- |
| the ingest-pipeline repository | DDL, plus the `<repo>/docs/DECISIONS.md` entry that ratifies it, plus the reviewer output from `scripts/review_clickhouse_ddl.py` | a change to a consumer's Go code |
| a kit consumer on the `chkit` lane | a `SELECT` against an existing rollup, a written rollup request filed against the ingest pipeline naming the columns and grain it needs, or a `chkit` configuration change | DDL, an `ALTER`, a `TRUNCATE`, or an `OPTIMIZE` |

When you cannot tell which one the task is in, ask which repository will hold the resulting file,
and stop until that is answered. Producing DDL for a requester who cannot apply it wastes the
review and hides the real dependency.

## Reporting a defect in a table you do not own

State the file and line, the rule it violates, the failure the violation produces, and the
replacement. Do not edit the file, and do not open a change against the owning repository from
inside this task; that repository ratifies its schema in its own decision log, and an edit that
skips the log is an unratified change that the next reader cannot audit.

## Editing bootstrap DDL in place, and when that stops being safe

`<repo>/clickhouse/ddl/001_init.sql:13` records the current rule for this pipeline: "This is
pre-publication bootstrap DDL; update directly instead of adding migrations." There is no migration
tool, no version table, and no ordered migration directory on this pipeline today.

That rule is safe only while both of the following hold, and both are checkable:

1. Every statement in the DDL file is `CREATE … IF NOT EXISTS`, so re-running the file against a
   fresh database reproduces the declared schema exactly.
2. Every environment that already holds rows can be dropped and re-ingested from the upstream
   source, or holds only rows the owner has written off.

The trap is condition 1 turning into a silent no-op: `CREATE TABLE IF NOT EXISTS` does nothing when
the table exists, so a column added to the file after the first deployment never reaches a
deployed environment, and the deployed table and the file disagree with no error anywhere. The
pipeline's own reset flag (`<repo>/docs/DECISIONS.md` section 15.1, "Local WA Database
Re-Initialization") exists because of exactly this, and it is scoped to local use.

The observable condition that ends direct editing: **the first environment whose rows cannot be
re-ingested from the upstream source.** From that environment onward, direct editing produces
undetectable drift.

By that point these must exist, and each is an artifact a reviewer can open:

- an ordered migration directory in which each file is applied exactly once and its application is
  recorded in a table inside the same ClickHouse instance;
- a check, run in CI, that compares the deployed column set from `system.columns` against the
  declared schema and fails the pipeline on a difference;
- a documented procedure for the change classes ClickHouse cannot perform in place — changing
  `ORDER BY`, changing `PARTITION BY`, changing a column's type in a sort key — which require
  creating a new table and moving data, not an `ALTER`.

## Retention on this pipeline is decided, and the decision is "never delete"

`<repo>/clickhouse/ddl/001_init.sql:9` still carries the original bootstrap note, "NO TTL by design
(retention policy is a later decision)", and that note is now out of date in one direction only:
`<repo>/docs/DECISIONS.md` section 30 ratifies that WA analytics data "is retained indefinitely. No
TTL on either table, permanently, and this is now a requirement rather than a deferred decision",
because the data is a commercial record and a settlement needs the full history. Section 2 records
the supersession in place.

So do not add a TTL clause to a table on this pipeline, do not propose one, and do not report its
absence as a gap — it is the ratified requirement. Do surface the consequence the same decision
names: storage grows without bound by construction, and the repository has no backup story for
either table, which its owner has assigned to the reliability owner rather than settled here. TTL
mechanics, for a pipeline whose owner has decided differently: `50-mvs-projections-and-ttl.md`.

## Single node today, cluster later

Both tables are `ENGINE = MergeTree` (`<repo>/clickhouse/ddl/001_init.sql:150` and `:249`), with
`ReplicatedMergeTree` templates present but commented out (`:152-155` and `:251-254`), and the
deployment is a single node with no ClickHouse Keeper. Verified against the official replication
documentation, these change at the transition and each is a work item, not a flag flip:

- Replication requires ClickHouse Keeper, or ZooKeeper 3.4.5 or newer, to be running and reachable
  before any replicated table is created.
- Replication is per table, not per server; a server can hold replicated and non-replicated tables
  at the same time, so a half-converted database is a reachable and silent state.
- `INSERT` and `ALTER` data are replicated, but `CREATE`, `DROP`, `ATTACH`, `DETACH`, and `RENAME`
  execute on one server and are not replicated. The DDL file must therefore be applied to every
  replica, or applied via `ON CLUSTER`.
- An existing `MergeTree` table converts with `ATTACH TABLE … AS REPLICATED`, so the data does not
  have to be re-ingested.
- The `{shard}` and `{replica}` macros in the commented templates must be defined in each server's
  configuration before the templates are uncommented, or table creation fails.

Deployment topology, node sizing, and Keeper placement: `/caas-arvan-kuber` (`$caas-arvan-kuber`)
and `/alaa-k8s-helm` (`$alaa-k8s-helm`).
