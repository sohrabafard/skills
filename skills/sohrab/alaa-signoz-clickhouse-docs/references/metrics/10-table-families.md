# Metric table families

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

## Table families, and when each is the right one

Baseline checked on 2026-07-30; released source evidence refreshed in `../90-versions.md`.
Re-derive with the target `COLLECTOR_TAG` selected there:

```bash
curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/COLLECTOR_TAG/cmd/signozschemamigrator/schema_migrator/metrics_migrations.go \
  | grep -o 'Table: *"[a-z0-9_]*"' | sort -u
```

| Read this | When |
|---|---|
| `distributed_samples_v4` | raw sample values, and the window is short enough that a raw scan is the right cost — see [raw or rollup selection](40-raw-or-rollup.md) |
| `samples_v4_agg_5m` | 5-minute pre-aggregated `last`/`min`/`max`/`sum`/`count` per fingerprint |
| `samples_v4_agg_30m` | 30-minute pre-aggregated, same columns, built from the 5-minute rollup |
| `distributed_time_series_v4` | label and fingerprint lookup at full resolution |
| `distributed_time_series_v4_6hrs` / `_1day` / `_1week` | label and fingerprint lookup over a longer window at lower granularity |
| `distributed_metadata` | confirming a metric's temporality, type, unit, description, and label keys |
| `distributed_updated_metadata` | metadata a user has edited in the UI, which overrides the reported values |
| `distributed_exp_hist` | exponential-histogram data points |
| `distributed_samples_v4_reduced_{last,sum}_{60s,5m,30m}` | series that a metric-reduction rule has aggregated; **the join key is `reduced_fingerprint`, not `fingerprint`** |
| `distributed_time_series_v4_reduced` / `_reduced_1day` | label lookup for reduced series |
| `distributed_metric_reduction_rules` | which metrics are being reduced, and therefore which family a metric lives in |

Two of these have a shape this skill cannot state from source: the `CREATE` for `samples_v4_agg_5m`,
`samples_v4_agg_30m` and `exp_hist` is not in the current `metrics_migrations.go` — only the
materialized views that write them are — and **no `distributed_` variant of the two rollups appears
in that file at all.** So before a panel reads a rollup, confirm what the install actually has:

```sql
SHOW TABLES FROM signoz_metrics LIKE '%agg_%';
SHOW TABLES FROM signoz_metrics LIKE '%exp_hist%';
DESCRIBE TABLE signoz_metrics.samples_v4_agg_5m;
```

`python3 scripts/check-signoz-schema.py` probes for each of them and reports which are present. On a
clustered install with no distributed rollup, the raw table is the only table a panel can read, and
the correct answer says so rather than emitting SQL against a table that is not there.
