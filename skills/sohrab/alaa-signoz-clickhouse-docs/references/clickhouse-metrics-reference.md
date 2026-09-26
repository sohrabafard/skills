# ClickHouse Metrics Query Reference for SigNoz

Read this for raw SigNoz dashboard-panel SQL over metrics: request rate, error ratio, RED panels,
histogram quantiles, or a gauge.

All tables live in the `signoz_metrics` database. The rules that hold on every query are stated once
in `SKILL.md`; this file carries what is specific to metrics.

## First decision

Use Query Builder v5 for ordinary metric exploration. Reach for raw SQL only when the user asked for
SQL, gave existing SQL to repair, or needs a panel expression the builder cannot produce — a window
function, a cross-metric join, a custom quantile.

## Version-qualified metric semantics

The release ledger in `90-versions.md` records Delta-sum handling, normalized-metric
compatibility removal, typed label filtering and exponential-histogram query fixes.
Do not difference Delta samples as cumulative counters. Preserve stored label spelling and
JSON types; a Query Builder semantic alias does not prove the same raw SQL key exists.
A missing-label warning is a reason to inspect metadata, not to invent a filter or assume zero.
Use the target's reduced-table topology; a vendor local-table fix does not authorize a
single-shard panel on a distributed deployment. PromQL endpoint/provider changes concern a
separate API, not the milliseconds variables or SQL panel result shape below.

## Required query prerequisites

Before writing any metric query, read [table families](metrics/10-table-families.md), [time/joins/flags](metrics/20-time-flags.md), [metric metadata](metrics/30-metadata.md), and [raw/rollup selection](metrics/40-raw-or-rollup.md) for target evidence, units, temporality, joins and scan selection.

## Select the remaining topic

- When inspecting labels or charting gauges, read [fingerprints and gauges](metrics/50-gauge.md) for bounded lookup and aggregation.
- When computing a cumulative rate, read [counter rate](metrics/60-counter-rate.md) for reset handling and two-stage aggregation.
- When computing an error ratio, read [counter error ratio](metrics/70-error-ratio.md) for separately derived rates.
- When computing quantiles, read [histograms](metrics/80-histograms.md) for classic queries and the exponential-layout evidence gate.
- When repairing a query or evidence is missing, read [diagnosis and stopping conditions](metrics/90-repair.md) for symptom-specific fixes and blockers.
