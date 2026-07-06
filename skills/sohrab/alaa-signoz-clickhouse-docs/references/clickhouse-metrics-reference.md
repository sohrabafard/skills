# ClickHouse Metrics Query Reference for SigNoz

Use this file when the user asks for raw SigNoz ClickHouse SQL over metrics, such as request rate, error rate, service RED panels, histogram quantiles, p99 latency, or a metrics dashboard/alert query.

## First decision

Prefer Query Builder v5 for ordinary metric exploration and alerts. Use raw ClickHouse SQL when the user explicitly asks for SQL, gives existing SQL to repair, or needs a dashboard/alert expression that Query Builder cannot express.

## Current table family

Current SigNoz metrics docs describe the `signoz_metrics` database with a samples table and time-series label/fingerprint tables:

- `signoz_metrics.distributed_samples_v4`
- `signoz_metrics.distributed_time_series_v4`
- `signoz_metrics.distributed_time_series_v4_6hrs`
- `signoz_metrics.distributed_time_series_v4_1day`

The docs warn that schemas can change. If the query will run in production, verify the current table/column names from docs or live ClickHouse before finalizing.

## Important columns

### `distributed_samples_v4`

- `env`
- `temporality`: `Unspecified`, `Cumulative`, or `Delta`
- `metric_name`
- `fingerprint`
- `unix_milli`
- `value`

### time-series tables

- `env`
- `temporality`
- `metric_name`
- `description`
- `unit`
- `type`: `Sum`, `Gauge`, `Histogram`, or `ExponentialHistogram`
- `is_monotonic`
- `fingerprint`
- `unix_milli`
- `labels` as JSON string

## Non-negotiable patterns

### 1. Use the two-step metric query shape

1. Query the time-series table to filter by labels and get `fingerprint` values.
2. Join samples by `fingerprint`, `metric_name`, and bounded time range.

This reduces scans because the time-series tables are smaller than the sample table.

### 2. Use metric time variables

Use SigNoz metric dashboard defaults unless current docs or the dashboard proves otherwise:

- `{{.start_timestamp_ms}}`
- `{{.end_timestamp_ms}}`

For time-series label tables, align the start to the table granularity when using the 1-day table:

```sql
intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
```

### 3. Return the graph shape

Time-series graph queries must return:

- `ts` as `DateTime`
- `value` as a numeric column

### 4. Do not infer metric type blindly

Before writing rate or quantile math, confirm:

- metric name
- temporality
- type (`Sum`, `Gauge`, `Histogram`, `ExponentialHistogram`)
- label keys used for service/status/route/operation
- units

### 5. Keep label access bounded

Use `JSONExtractString(labels, '<key>')` for label filters. Use only bounded labels for grouping. Do not group by raw URL, user ID, trace ID, request ID, email, phone, token, or payload-derived values.

## Schema discovery helper

Use when docs and live schema may differ:

```sql
SHOW DATABASES LIKE 'signoz_metrics';
SHOW TABLES FROM signoz_metrics;
DESCRIBE TABLE signoz_metrics.distributed_samples_v4;
DESCRIBE TABLE signoz_metrics.distributed_time_series_v4_1day;
```

For metric inventory:

```sql
SELECT
  metric_name,
  any(type) AS metric_type,
  any(temporality) AS temporality,
  countDistinct(fingerprint) AS series
FROM signoz_metrics.distributed_time_series_v4_1day
WHERE unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
  AND unix_milli < {{.end_timestamp_ms}}
GROUP BY metric_name
ORDER BY series DESC
LIMIT 100;
```

## Common query patterns

### Fingerprints and labels for one metric

```sql
SELECT DISTINCT
  fingerprint,
  labels
FROM signoz_metrics.distributed_time_series_v4_1day
WHERE metric_name = {{metric_name}}
  AND unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
  AND unix_milli < {{.end_timestamp_ms}}
LIMIT 100;
```

### Gauge value by service

Use for gauges where `value` is already the observed value.

```sql
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
  AND s.unix_milli >= {{.start_timestamp_ms}}
  AND s.unix_milli < {{.end_timestamp_ms}}
GROUP BY ts
ORDER BY ts ASC;
```

### Counter request rate for a service

Use for cumulative monotonic counters. Replace the metric and label names with the ones verified in your environment.

```sql
SELECT
  ts,
  sum(rate_value) AS value
FROM
(
  SELECT
    ts,
    if(isNaN(per_series_rate), 0, per_series_rate) AS rate_value
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

### Error rate percentage from cumulative counters

Use two counter-rate queries: one filtered to error status and one unfiltered total, then join by `ts`.

```sql
WITH
errors AS (
  /* Build this CTE from the counter request-rate pattern.
     Add a bounded status label filter such as:
     JSONExtractString(labels, 'status_code') = 'STATUS_CODE_ERROR' */
  SELECT ts, sum(rate_value) AS value FROM {{error_rate_inner_query}} GROUP BY ts
),
total AS (
  /* Same metric and service filter, without the error-status filter. */
  SELECT ts, sum(rate_value) AS value FROM {{total_rate_inner_query}} GROUP BY ts
)
SELECT
  errors.ts AS ts,
  (errors.value * 100) / nullIf(total.value, 0) AS value
FROM errors
INNER JOIN total ON errors.ts = total.ts
ORDER BY ts ASC;
```

### Histogram p99 latency for a service

Use only after confirming the histogram metric name and `le` label. Prefer Query Builder if the histogram schema or unit is uncertain.

```sql
SELECT
  ts,
  histogramQuantile(arrayMap(x -> toFloat64(x), groupArray(le)), groupArray(bucket_rate), 0.99) AS value
FROM
(
  SELECT
    le,
    ts,
    sum(bucket_rate) AS bucket_rate
  FROM
  (
    SELECT
      le,
      ts,
      if(isNaN(per_series_rate), 0, per_series_rate) AS bucket_rate
    FROM
    (
      SELECT
        le,
        ts,
        if(
          (bucket_value - lagInFrame(bucket_value, 1, 0) OVER bucket_window) < 0,
          nan,
          (bucket_value - lagInFrame(bucket_value, 1, 0) OVER bucket_window)
          / nullIf(dateDiff('second', lagInFrame(ts, 1, ts) OVER bucket_window, ts), 0)
        ) AS per_series_rate
      FROM
      (
        SELECT
          s.fingerprint,
          series.le AS le,
          toStartOfInterval(toDateTime(intDiv(s.unix_milli, 1000)), toIntervalSecond(60)) AS ts,
          max(s.value) AS bucket_value
        FROM signoz_metrics.distributed_samples_v4 AS s
        INNER JOIN
        (
          SELECT DISTINCT
            fingerprint,
            JSONExtractString(labels, 'le') AS le
          FROM signoz_metrics.distributed_time_series_v4_1day
          WHERE metric_name = {{histogram_bucket_metric_name}}
            AND temporality = 'Cumulative'
            AND unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000
            AND unix_milli < {{.end_timestamp_ms}}
            AND JSONExtractString(labels, 'service_name') = {{service_name}}
        ) AS series USING (fingerprint)
        WHERE s.metric_name = {{histogram_bucket_metric_name}}
          AND s.unix_milli >= {{.start_timestamp_ms}}
          AND s.unix_milli < {{.end_timestamp_ms}}
        GROUP BY s.fingerprint, series.le, ts
        ORDER BY s.fingerprint ASC, series.le ASC, ts ASC
      )
      WINDOW bucket_window AS (PARTITION BY fingerprint, le ORDER BY fingerprint ASC, le ASC, ts ASC)
    )
  )
  GROUP BY le, ts
)
GROUP BY ts
ORDER BY ts ASC;
```

## Query repair checklist

- Does the query use `signoz_metrics` tables, not logs/traces table families?
- Does it use metric time variables in milliseconds?
- Does it filter samples by `unix_milli`?
- Does it use a time-series table to reduce fingerprints before scanning samples?
- Does it match `temporality` and metric type?
- Does the output have `ts` as `DateTime` and `value` as numeric for graphs?
- Are label filters bounded and safe?
- Are divide-by-zero and counter reset cases handled?
- Is the histogram unit clear before labeling p99 latency in ms/s?

## When to refuse to finalize without schema inspection

Do not finalize raw metrics SQL when:

- the user asks for production dashboard/alert SQL and the metric name/table family is unknown
- the query depends on histogram/exponential-histogram internals not confirmed by docs or live schema
- the user asks to group by a high-cardinality or sensitive label
- the table names in the user’s environment differ from the current reference
