# Continue WA2 after the ClickHouse checker delivery

Resume the consumer deploy workflow at WA2 (`alaa-9bbj.2`). Reconcile the current WA integration
HEAD and issue ownership before edits. Verify that the skills owner closed `alaa-dgp8` and
reconcile its delivery. Preserve the historical dependency. The WA2 owner determines remaining
workflow status after the WA schema work, reviews and documentation. WA2 and parent phase acceptance
remain consumer decisions. Preserve EO-59 and `alaa-orqe`. Follow the consumer plan at
`deploy:docs/_agent_plans/20261103-070000_wa-fleet-onboarding.md` for Phase 2 delivery, the phase
review boundary, final Phase 7, and rollout authority.

## Reproduce the checkpoint audit

Point `SKILLS_CHECKOUT` at a local skills source checkout. Before running the audit, verify that the
checker file in that checkout matches the SHA-256 recorded for reviewed commit
`c8681fe3776ba7bd94bd7d9d2c87c9b7cf0c3080` in the [source manifest](alaa-dgp8/cycle3-source.sha256).
Run from the WA checkout with Python 3.

```bash
python3 -B "${SKILLS_CHECKOUT:?set the skills source checkout}/skills/sohrab/clickhouse-performance-schema-ops/scripts/review_clickhouse_ddl.py" \
  clickhouse/ddl/001_init.sql clickhouse/ddl/002_agg.sql
```

At audited WA HEAD `3a86419f3244b6597b86ee24bf4781e3721d1d5d`, both SQL file hashes matched
checkpoint `cfa54adac0bea630beaa0ff2789ba772d016b37c`. The audit covers those bytes only.
Expected checkpoint exit is 2. Resolve the 32 findings and four proof gaps separately. Keep
unsupported real SQL in scope and review its effects rather than dropping it to force exit 0.
[Input hashes](checker-verification/cycle3/wa-inputs.tsv), [audit hash](checker-verification/cycle3/wa-comparison.sha256),
[baseline-to-final matrix](alaa-dgp8/wa-disposition.md).

## Complete WA-owned work

1. Resolve 18 Nullable findings, four raw key findings and seven effective aggregate sparse-index
   findings. Supply the complete DDL and writer bundle, including all real producers, backfills and
   rebuilds. For each shorter explicit aggregate `PRIMARY KEY`, pass actual target SQL using repeatable
   `--read-query FILE`. Use a supported single-target query with equality through every prefix member
   before the last, and equality or a one-sided range at the last. Prove pruning on the target.
   [Admitted proof and exit contract](../../skills/sohrab/clickhouse-performance-schema-ops/references/80-proof-and-validation.md).
2. Preserve full merge identity in `ORDER BY`. Add `object_type` to the identities for
   `watch_time_daily`, `views_daily` and `heatmap_10s`. Enum membership and unknown-value folding
   supply no functional-dependency proof. Resolve the two additive source ALTER proof gaps in
   `001_init.sql` at lines 280 and 331 and both `event_date` alias conflicts in `002_agg.sql` at
   lines 83 and 144 against the effective schema and settings.
3. Agree on replacement or rebuild with the schema owner. Metadata-only `MODIFY ORDER BY` cannot add
   the existing discriminator or change the primary key. Recompute from trustworthy pre-aggregation
   history or replay with proven coverage. Copying the corrupted rollup cannot recover its lost groups.
   Prove parity against source-grain measures by tenant, date, ID and `object_type`. Missing coverage
   or any per-type discrepancy blocks cutover. Prove a writer pause and drain or a disjoint live
   boundary, retain the old table, and record rollback limits before switching readers.
4. Verify the target server, effective compatibility and CREATE-time guard, deployed schema,
   MV definer grants, writer trigger and denial of direct target writes. The cached 24.8.14.39
   physical merge proof demonstrates legacy collapse with synthetic rows. Run target-specific
   proof for the actual engine and settings. [Fixture identity](checker-verification/cycle3/runtime-reuse.log),
   [ClickHouse version implications](alaa-te30/report.md#compatibility-and-handoff).
   If WA consumes the Vector upgrade, validate its actual configuration, secret providers and
   delivery paths against the selected runtime. [Vector migration notes](../../skills/sohrab/vector-rust-observability-pipelines/references/80-version-and-upgrade-deltas.md).

Record the skills and WA commits, input and evidence hashes, exact invocations and exits, finding
disposition, engine and image identity, effective settings, and the proof results. Reconcile
consumer review and documentation with the current HEAD before presenting Phase 2 evidence.
[Producer evidence index](README.md).
