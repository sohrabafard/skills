# Cumulative counter rate

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

### Counter request rate for a service

For a cumulative monotonic counter. `lagInFrame` differences consecutive samples per series, and the
`nan` guard drops the negative step a counter reset produces.

```sql
-- raw-scan-ok: window <= 24h. Beyond that, difference `last` from samples_v4_agg_5m instead:
-- the rate has coarser resolution; verify reset handling and actual rows scanned on the target.
SELECT ts, sum(rate_value) AS value
FROM
(
  SELECT ts, if(isNaN(per_series_rate), 0, per_series_rate) AS rate_value
  FROM
  (
    SELECT
      ts,
      if(
        (per_series_value - lagInFrame(per_series_value, 1, 0) OVER rate_window) < 0,
        nan,
        (per_series_value - lagInFrame(per_series_value, 1, 0) OVER rate_window)
        / nullIf(dateDiff('second', lagInFrame(ts, 1, ts) OVER rate_window, ts), 0)
      ) AS per_series_rate
    FROM
    (
      SELECT
        s.fingerprint,
        toStartOfInterval(toDateTime(intDiv(s.unix_milli, 1000)), toIntervalSecond(60)) AS ts,
        max(s.value) AS per_series_value
      FROM signoz_metrics.distributed_samples_v4 AS s
      INNER JOIN
      (
        SELECT DISTINCT fingerprint
        FROM signoz_metrics.distributed_time_series_v4_1day
        WHERE metric_name = {{metric_name}}
          AND temporality = 'Cumulative'
          AND unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
          AND unix_milli < {{.end_timestamp_ms}}
          AND JSONExtractString(labels, 'service_name') = {{service_name}}
      ) AS series USING (fingerprint)
      WHERE s.metric_name = {{metric_name}}
        AND bitAnd(s.flags, 1) = 0
        AND s.unix_milli >= {{.start_timestamp_ms}}
        AND s.unix_milli < {{.end_timestamp_ms}}
      GROUP BY s.fingerprint, ts
      ORDER BY s.fingerprint ASC, ts ASC
    )
    WINDOW rate_window AS (PARTITION BY fingerprint ORDER BY fingerprint ASC, ts ASC)
  )
)
GROUP BY ts
ORDER BY ts ASC;
```
