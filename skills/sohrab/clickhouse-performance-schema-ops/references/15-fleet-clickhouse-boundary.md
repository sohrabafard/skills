# Which ClickHouse tables this skill designs

Three skills in this fleet touch ClickHouse. `SKILL.md` states the line between them once, under
"Not owned here", in the words all three skills use. This file applies it.

Ask one question: **which repository can change this table's `CREATE TABLE`?** If a repository in
this fleet can, every rule in this skill applies to the table. If a vendor owns it, no schema rule
of this skill applies, and only `40-query-tuning-and-read-lane.md` does.

## The ingest-pipeline repository is `wa`

Wherever this skill says "the ingest pipeline", it means `wa`, which holds:

| In `wa` | What it is |
| --- | --- |
| `<repo>/clickhouse/ddl/` | the `wa_raw` raw tables and the `wa_agg` rollup tables with the materialized views that fill them |
| `<repo>/vector/wa-vector.yaml` | the topology whose ClickHouse sinks write `wa_raw` |
| `<repo>/docs/DECISIONS.md` | the log that ratifies every schema choice with its reason |
| `<repo>/wa-api/` | the Go read service, which reads `wa_agg` and never `wa_raw` |

`wa` holds the fleet's only Vector deployment and the only ClickHouse in which the fleet designs
tables. File every finding about these tables against `wa`; do not edit them from another
repository (`10-authority-and-change-path.md`).

## SigNoz tables are outside this skill

SigNoz creates and versions its own `signoz_logs`, `signoz_traces` and `signoz_metrics` databases.
The fleet cannot alter their engine, sorting key, partitioning, TTL or compression. Raise a defect in
one with the vendor. How such a table is queried: `/alaa-signoz-clickhouse-docs`.

That skill also owns the SigNoz tenancy rule, an exception that applies only to vendor-owned
`signoz_*` tables. Keep the `project_id` predicate in every query against `wa_raw` and `wa_agg`,
because those tables hold the rows of all tenants with no other boundary between them.

## The seam with the pipeline skill

`/vector-rust-observability-pipelines` owns the sink's batching, buffering, acknowledgement chain
and retry behaviour, and what the pipeline does while the table is unreachable. It decides no
schema. This skill owns the engine, the sorting key, the partition key, the TTL, the codecs and the
table settings. It decides no sink configuration.

**A writer cannot make an insert exact by retrying it more carefully. The table decides exactness,
through its engine and its deduplication settings** (`20-table-design.md` section 6,
`30-ingest-and-parts.md`). When a pipeline owner asks for exactly-once delivery, the answer is an
engine and settings change filed against the table owner, not a retry count. Report the
duplicate-row consequence of a sink setting to the pipeline owner; never propose a sink setting from
this skill.

`<repo>/docs/DECISIONS.md` section 29 ratifies WA ingest as best-effort analytics telemetry. Rows
can be lost, and an insert whose response was lost can repeat. Raw and derived counts and sums are
approximate and are excluded from billing and contractual settlement. Never present a number from
these tables as exact, and do not design exactness into the ingest path against that decision. The
same section keeps table-side deduplication and rebuild choices separate; they stay the table
owner's decision. A duplicated raw insert inflates a rollup measure that a materialized view
already wrote, and no read-side rewrite corrects it.

Retry, backoff and timeout reasoning for producers: `/alaa-reliability-sla`. The Ala values those
mechanisms use: `/alaa-services-contract`
`references/22-failure-load-and-deprecation-contract.md`.
