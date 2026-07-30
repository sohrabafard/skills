# Which ClickHouse tables this skill designs, and which it does not

Read this before applying any rule in this skill to a table, and whenever you are holding a second
ClickHouse skill and cannot tell which one answers the question in front of you.

## Applying the three-way boundary

Three skills in this fleet touch ClickHouse. The line between them is stated once, in `SKILL.md`
under "Not owned here", in the same words all three skills use; it is not restated here. This file
applies it.

Apply it by asking one question: **which repository can change this table's `CREATE TABLE`?** If a
repository in this fleet can, every rule in this skill applies to that table. If a vendor owns it,
none of this skill's schema rules apply and only `40-query-tuning-and-read-lane.md` does.

## The ingest-pipeline repository is `wa`

The "Two audiences" section of `SKILL.md` assigns the ClickHouse DDL directory and the Vector
topology writing into it to "the ingest-pipeline repository". **On this fleet that repository is
`wa`.** Wherever this skill says "the ingest pipeline", it means `wa`, which holds:

| In `wa` | What it is |
| --- | --- |
| `<repo>/clickhouse/ddl/001_init.sql` | the `wa_raw` raw tables `events_raw` and `watch_segments_raw` |
| `<repo>/clickhouse/ddl/002_agg.sql` | the `wa_agg` rollup tables and the materialized views that fill them |
| `<repo>/vector/wa-vector.yaml` | the topology whose two ClickHouse sinks write `wa_raw` |
| `<repo>/docs/DECISIONS.md` | the log in which every schema choice is ratified with its reason |
| `<repo>/wa-api/` | the Go read service, which reads `wa_agg` and never `wa_raw` |

`wa` holds the fleet's only Vector deployment and the only ClickHouse in which the fleet designs
tables. Every "reported, not fixed" finding elsewhere in this skill is a finding in `wa`, and every
one of them is filed against `wa` rather than edited from here
(`10-authority-and-change-path.md`).

## SigNoz's tables are outside this skill's scope

SigNoz creates and versions its own `signoz_logs`, `signoz_traces` and `signoz_metrics` databases.
The fleet owns none of their engine, sorting key, partitioning, TTL or compression and cannot alter
any of them, so a defect in one is raised with the vendor rather than repaired with an `ALTER`.
`20-table-design.md`, `30-ingest-and-parts.md`, `50-mvs-projections-and-ttl.md` and
`80-proof-and-validation.md` do not apply to a `signoz_*` table. How such a table is queried:
`/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`).

### The tenant-predicate rule does not transfer to SigNoz, and this is the reason

`SKILL.md` rule 2 and `20-table-design.md` section 1 require the tenant column first in `ORDER BY`
and a tenant predicate on every query. **That rule governs tables this fleet's own ingest pipeline
owns; it does not transfer to `signoz_*` tables.** It does not transfer because of how the platform
owner has decided SigNoz tenancy works, not because anybody forgot:

- All tenants report into one shared SigNoz.
- Everyone with access to that SigNoz is authorised to see every tenant's telemetry, because seeing
  it is how they fix it. There is no tenant to isolate from another inside that instance.
- A project whose telemetry must not be shared gets a **separate SigNoz address, selected by an
  environment variable**. The isolation boundary is the address, not a `WHERE` clause.

Two obligations follow, and they point in opposite directions:

1. A SigNoz query carrying no tenant predicate is correct as written. Do not add one to satisfy this
   skill's rule, and do not report its absence as a defect.
2. The SigNoz posture is not a licence to drop `project_id` from a `wa_raw` or `wa_agg` query. Those
   tables hold every tenant's rows in one instance with no second address separating them, so there
   the predicate is the only isolation that exists.

## What the pipeline side owns, so the seam has two agreed ends

`/vector-rust-observability-pipelines` (`$vector-rust-observability-pipelines`) owns the sink's
batching, its buffering, its acknowledgement chain, its retry behaviour, and what the pipeline does
while the table is unreachable. It decides no schema. This skill owns the engine, the sorting key,
the partition key, the TTL, the compression codecs, and the table settings. It decides no sink
configuration.

The seam matters most where the two look like one problem. **A writer cannot make an insert exact by
retrying it more carefully; exactness is decided at the table, by the engine and its deduplication
settings** — the rule is in `20-table-design.md` section 6 and the mechanics are in
`30-ingest-and-parts.md`. When a pipeline owner asks for exactly-once delivery, the answer is an
engine and settings change filed against the table owner, not a retry count.

Retry, backoff and timeout *reasoning* for the producers: `/alaa-reliability-sla`
(`$alaa-reliability-sla`). The Ala *values* those mechanisms use: `/alaa-services-contract`
(`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md`.

## The worked instance: `wa`, measured at commit `5bbe3c2`

Re-derive the commit with `git -C <wa checkout> rev-parse --short HEAD` and re-read any line this
section cites before repeating it; `wa` moves faster than this file.

**Decided here, and both are currently open against `<repo>/docs/DECISIONS.md` §29, which ratifies
that counts and sums from `wa_raw` must be exact because they are billed on:**

- The **engine**. Both raw tables are plain `ENGINE = MergeTree`
  (`<repo>/clickhouse/ddl/001_init.sql:150` and `:249`), and the topology is a single node with no
  ClickHouse Keeper, so `ReplicatedMergeTree` is unavailable today. The rule and the available
  setting: `20-table-design.md` section 6 and `30-ingest-and-parts.md`.
- The **sorting key**. `object_type` is a `GROUP BY` dimension in three materialized views but is in
  no target `ORDER BY`. The rule and the evidence: `20-table-design.md` section 3.

**Not decided here.** `retry_attempts: 20` on both sinks, the disk buffer that holds undelivered
events, and the source-side acknowledgement that decides what the client is told, all belong to the
pipeline skill named above. Reporting the duplicate-row consequence to that owner is correct;
proposing a sink setting from this skill is not.

**Where this skill's scope ends on the read side.** `<repo>/wa-api/` queries only `wa_agg.*` through
the fleet's shared `chkit` client, honouring `chkit/doc.go`'s prohibition on reading raw event
tables from a request path. Nine sites under
`<repo>/wa-api/internal/infrastructure/chstats/` sum `watched_wall_ms` with a plain `sum()`. That
column is a `SimpleAggregateFunction(sum, UInt64)` a materialized view wrote from raw rows
(`<repo>/clickhouse/ddl/002_agg.sql:68`), so a duplicated raw insert inflates a billed quantity and
no rewrite on the read side corrects it. That is why the engine decision above is a correctness
decision and not a tuning one.

Remediation for this instance is filed as RFCs inside `wa`. This file teaches the rule; those
documents fix the instance, and this skill does not restate them.
