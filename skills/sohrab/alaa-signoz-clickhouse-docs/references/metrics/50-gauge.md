# Metric fingerprints and gauges

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

### Fingerprints and labels for one metric

```sql
SELECT DISTINCT fingerprint, labels
FROM signoz_metrics.distributed_time_series_v4_1day
WHERE metric_name = {{metric_name}}
  AND unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
  AND unix_milli < {{.end_timestamp_ms}}
LIMIT 100;
```

### Gauge by service

```sql
-- raw-scan-ok: window <= 24h at a 60s scrape. Beyond 24h read samples_v4_agg_5m and take
-- `last` in place of avg(value). Beyond 30d read samples_v4_agg_30m.
SELECT
  toStartOfInterval(toDateTime(intDiv(s.unix_milli, 1000)), toIntervalSecond(60)) AS ts,
  avg(s.value) AS value
FROM signoz_metrics.distributed_samples_v4 AS s
INNER JOIN
(
  SELECT DISTINCT fingerprint
  FROM signoz_metrics.distributed_time_series_v4_1day
  WHERE metric_name = {{metric_name}}
    AND temporality = 'Unspecified'
    AND unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
    AND unix_milli < {{.end_timestamp_ms}}
    AND JSONExtractString(labels, 'service_name') = {{service_name}}
) AS series USING (fingerprint)
WHERE s.metric_name = {{metric_name}}
  AND bitAnd(s.flags, 1) = 0
  AND s.unix_milli >= {{.start_timestamp_ms}}
  AND s.unix_milli < {{.end_timestamp_ms}}
GROUP BY ts
ORDER BY ts ASC;
```
