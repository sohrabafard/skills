# ClickHouse and Vector skill deliveries, 2026-11-04

The reviewed source checkpoint is `c8681fe3776ba7bd94bd7d9d2c87c9b7cf0c3080`.
This archive covers two version-aware skill upgrades and the ClickHouse aggregate DDL checker.
Beads owns live task state. Return to the [upgrade history](../../outputs/README.md).

## Release and compatibility evidence

- **ClickHouse, alaa-te30, closed at `e446fe18`.** The November 4 channel check selected
  stable 26.10.3.7 (October 25) and LTS 26.8.36.3 (October 26). For the July documentation baseline
  without an engine pin, intervening 26.7–26.10 deltas, and migration guidance including merge
  guards and MV definer grants, read the [ClickHouse release ledger](alaa-te30/report.md).
- **Vector, alaa-a95j, closed at `efb08a44`.** For 0.61.0 (October 29), the upgrade path from
  the 0.58 documentation and 0.57 empirical baselines, and the strict cached 0.61.0 validation
  with secret-backend controls, read the [Vector acceptance evidence](alaa-a95j/README.md) and
  [version and migration notes](../../skills/sohrab/vector-rust-observability-pipelines/references/80-version-and-upgrade-deltas.md).
- For the accepted domain reviews and the ClickHouse backfill rerun note, read the
  [upgrade review record](upgrade-reviews.md). The upgrade freeze cleared six repository gates.
  [Command ledger](upgrade-verification/cycle1/final/commands.tsv).

## Checker and WA continuation

- **Checker, alaa-dgp8.** For the admitted SQL proof subset, read the
  [checker contract](../../skills/sohrab/clickhouse-performance-schema-ops/references/80-proof-and-validation.md).
  For the two repair cycles, the additional authorized quoted-name repair, and the final
  correctness, security, instruction and migration verdicts, read the [review record](checker-reviews.md).
- For the 24 passing CLI cases, two expected mutant failures and the unchanged WA audit,
  read the [independent command ledger](checker-verification/cycle3/commands.tsv) and
  [source manifest](alaa-dgp8/cycle3-source.sha256). The WA result is exit 2 with 32 findings
  and four proof gaps. The [finding matrix](alaa-dgp8/wa-disposition.md) maps all 29 prior findings.
- The cached ClickHouse 24.8.14.39 fixture ran with pull disabled, no network or published
  ports, and a 2 GiB memory limit. It converged to one active part per table. The correct
  key kept two groups with totals 5 and 18. The broken key merged them into one row totaling 23.
  A fresh SIGTERM probe exited 0 after confirming the runner exited 143 and its exact container
  was gone. Both proof inputs retained their hashes through the final checker repair. [Merge run](checker-verification/cycle1/live.log),
  [cancellation run](checker-verification/cycle2/cancellation.log), [reuse evidence](checker-verification/cycle3/runtime-reuse.log).
- To resume consumer work after the producer closes, use the [WA2 continuation](wa2-continuation.md)
  for the command, outstanding repairs, recovery proof and review boundary.

## Proof scope

The pre-existing Codex skill symlinks resolve to the changed first-party directories. This is
source visibility through existing links. Installer execution, fresh agent activation, a runtime
test on either selected ClickHouse 26.x channel, and consumer deployment were unrun. The Vector
checks exercised strict configuration validation against the cached image. Live relay and
delivery behavior require consumer runtime evidence.
