# Histogram quantiles and exponential layouts

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.
For cumulative bucket rates, use the [counter-rate procedure](60-counter-rate.md) for resets and inner aggregation.

### Histogram p99

For a classic `_bucket` histogram with an `le` label. Confirm the bucket metric's name and unit from
`distributed_metadata` first; a p99 labelled milliseconds that is actually seconds is a wrong answer
that renders convincingly.

```sql
-- raw-scan-ok: window <= 6h. A bucket histogram multiplies series by its bucket count, so the
-- raw window here is shorter than for a plain counter. Beyond 6h read samples_v4_agg_5m.
SELECT
  ts,
  histogramQuantile(arrayMap(x -> toFloat64(x), groupArray(le)), groupArray(bucket_rate), 0.99) AS value
FROM
(
  SELECT le, ts, sum(bucket_rate) AS bucket_rate
  FROM {{bucket_rate_inner_query}}
  /* {{bucket_rate_inner_query}} is the pattern in 60-counter-rate.md, with three changes:
     read {{histogram_bucket_metric_name}} instead of {{metric_name}};
     add `JSONExtractString(labels, 'le') AS le` to the fingerprint sub-select and carry `le`
       through every level;
     partition the window by `fingerprint, le` instead of `fingerprint`.
     It is not repeated here because one rate pattern stated twice drifts. */
  GROUP BY le, ts
)
GROUP BY ts
ORDER BY ts ASC;
```

## Exponential histograms

`signoz_metrics.distributed_exp_hist` exists — it is confirmed in the schema migrator, which alters
it, though its `CREATE` is not in the current migrations file. So the answer is no longer "this
cannot be written". It is:

```sql
DESCRIBE TABLE signoz_metrics.distributed_exp_hist;
```

Read the column layout from the target, write the query against what you read, and state in the
answer that the layout came from this install rather than from documentation. Do not guess a
sketch-encoding column layout: the scale-and-bucket-offset representation differs between collector
versions, and a wrong reading produces a plausible quantile rather than an error.
