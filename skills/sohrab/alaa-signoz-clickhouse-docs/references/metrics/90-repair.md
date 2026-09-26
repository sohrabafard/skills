# Metric query diagnosis and stopping conditions

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

## Repairing a metrics query, by symptom

| Symptom | Most likely cause | Smallest fix |
|---|---|---|
| no rows at all | time unit mismatch, or a fingerprint window narrower than the sample window | filter samples on `unix_milli` in **milliseconds**; align the time-series start down to that table's bucket |
| rate is negative or spikes | counter reset, or a `Delta` metric differenced as if `Cumulative` | read `temporality` from `distributed_metadata`; keep the `nan` guard; do not difference a `Delta` series |
| p99 is wrong by orders of magnitude | histogram unit is seconds and the panel says milliseconds | read `unit` from `distributed_metadata` before labelling the axis |
| result disagrees with the SigNoz panel | missing `bitAnd(flags, 1) = 0` | add the flags filter |
| the join returns nothing for a reduced metric | joined on `fingerprint` where the reduced family uses `reduced_fingerprint` | check `distributed_metric_reduction_rules`, then join on `reduced_fingerprint` |
| the query times out on a long window | raw sample scan where a rollup exists | see [raw or rollup selection](40-raw-or-rollup.md) |
| the metric is not in `distributed_time_series_v4` | it is reduced, or it stopped reporting | check `distributed_metadata.last_reported_unix_milli` |

## When to stop and say so

- The metric name is unknown and the query is destined for a production panel: read
  `distributed_metadata` first; if it is unreachable, name that as the blocker instead of guessing a
  name.
- The install's table set differs from the [table families](10-table-families.md): run the `SHOW TABLES` probes, then answer
  against what exists, and say which table you used.
