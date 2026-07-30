# ClickHouse Metrics Query Reference for SigNoz

Read this for raw SigNoz dashboard-panel SQL over metrics: request rate, error ratio, RED panels,
histogram quantiles, or a gauge.

All tables live in the `signoz_metrics` database. The rules that hold on every query are stated once
in `SKILL.md`; this file carries what is specific to metrics.

## First decision

Use Query Builder v5 for ordinary metric exploration. Reach for raw SQL only when the user asked for
SQL, gave existing SQL to repair, or needs a panel expression the builder cannot produce — a window
function, a cross-metric join, a custom quantile.

## Table families, and when each is the right one

Verified against the SigNoz schema migrator on 2026-07-30. Re-derive with:

```bash
curl -s https://raw.githubusercontent.com/SigNoz/signoz-otel-collector/main/cmd/signozschemamigrator/schema_migrator/metrics_migrations.go \
  | grep -o 'Table: *"[a-z0-9_]*"' | sort -u
```

| Read this | When |
|---|---|
| `distributed_samples_v4` | raw sample values, and the window is short enough that a raw scan is the right cost — see *Choosing raw or rollup* |
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

## Time variables

`{{.start_timestamp_ms}}` and `{{.end_timestamp_ms}}`, both in **milliseconds** — not the second or
nanosecond variables the logs and traces surfaces use. Filter samples on `unix_milli`.

When reading a lower-granularity time-series table, align the start down to that table's bucket or
the first bucket is dropped:

```sql
unix_milli >= intDiv({{.start_timestamp_ms}}, 86400000) * 86400000   -- the 1-day table
```

## The two-step shape

Filter labels on a time-series table to get `fingerprint` values, then join samples by `fingerprint`
inside a bounded time range. The time-series tables are far smaller than the sample table, so this
is what keeps the sample scan narrow.

## The `flags` column

`samples_v4` and `exp_hist` carry `flags UInt32 DEFAULT 0`. SigNoz's own rollup views filter it:

```sql
WHERE bitAnd(flags, 1) = 0
```

Bit 0 marks a data point the vendor's aggregation excludes. Apply the same filter in any query whose
result is compared against a SigNoz-rendered panel, or the two disagree by exactly the excluded
points and the difference looks like a query bug.

## Confirming a metric before doing rate or quantile maths

Do not infer a metric's temporality, type or unit from its name. Ask the install:

```sql
SELECT DISTINCT
  metric_name, type, temporality, unit, is_monotonic, description
FROM signoz_metrics.distributed_metadata
WHERE metric_name = {{metric_name}};
```

and for its label keys:

```sql
SELECT DISTINCT attr_name, attr_datatype
FROM signoz_metrics.distributed_metadata
WHERE metric_name = {{metric_name}}
ORDER BY attr_name;
```

`distributed_metadata` holds one row per metric per attribute value, with `first_reported_unix_milli`
and `last_reported_unix_milli`, so it also answers "is this metric still being reported". Check
`distributed_updated_metadata` too when the answer looks wrong: a unit edited in the UI lives there
and overrides the reported one.

This replaces the instruction to "confirm temporality, type and units" with the query that confirms
them. A rule with no method is not followed.

## Choosing raw or rollup

A dashboard panel's time window is chosen by whoever views it, not by whoever wrote the SQL. A
30-day panel over `distributed_samples_v4` reads every sample in 30 days; the same panel over
`samples_v4_agg_30m` reads one row per fingerprint per 30 minutes. The ratio is the ratio of the
scrape interval to 30 minutes.

State the bound the panel must hold as its window grows, and pick the table from it. Whether a bound
is real, how to find it from the system rather than assume it, and what makes it a budget rather than
a preference are owned by
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) `references/10-complexity-budget.md`.
This file owns only which SigNoz table each answer reads.

Every example below reads raw `distributed_samples_v4`. Each carries the window bound under which
that is the right table, in a `-- raw-scan-ok:` comment; `check-signoz-sql.py` rule `S6` reports a
metrics query that reads the raw table and carries neither a rollup nor that bound.

The rollup columns are `last`, `min`, `max`, `sum`, `count` per `(env, temporality, metric_name,
fingerprint, unix_milli)`. For a gauge, `last` replaces `avg(value)`. For a cumulative counter,
`last` is the value to difference. `sum`/`count` gives a mean without reading samples.

## Worked queries

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

### Counter request rate for a service

For a cumulative monotonic counter. `lagInFrame` differences consecutive samples per series, and the
`nan` guard drops the negative step a counter reset produces.

```sql
-- raw-scan-ok: window <= 24h. Beyond that, difference `last` from samples_v4_agg_5m instead:
-- the rate is the same quantity at coarser resolution, and the scan is 1/300th the rows.
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

### Error ratio from cumulative counters

Two counter-rate queries — one filtered to the error status, one unfiltered — joined on `ts`. Take
the status label's name and its permitted values from
`/alaa-services-contract` (`$alaa-services-contract`) rather than from this example, which shows
the shape only.

```sql
WITH
errors AS (
  /* the counter-rate pattern above, plus one bounded status-label filter */
  SELECT ts, sum(rate_value) AS value FROM {{error_rate_inner_query}} GROUP BY ts
),
total AS (
  /* the same metric and service filter, without the status filter */
  SELECT ts, sum(rate_value) AS value FROM {{total_rate_inner_query}} GROUP BY ts
)
SELECT
  errors.ts AS ts,
  (errors.value * 100) / nullIf(total.value, 0) AS value
FROM errors
INNER JOIN total ON errors.ts = total.ts
ORDER BY ts ASC;
```

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
  /* {{bucket_rate_inner_query}} is the counter-rate pattern above, with three changes:
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

## Repairing a metrics query, by symptom

| Symptom | Most likely cause | Smallest fix |
|---|---|---|
| no rows at all | time unit mismatch, or a fingerprint window narrower than the sample window | filter samples on `unix_milli` in **milliseconds**; align the time-series start down to that table's bucket |
| rate is negative or spikes | counter reset, or a `Delta` metric differenced as if `Cumulative` | read `temporality` from `distributed_metadata`; keep the `nan` guard; do not difference a `Delta` series |
| p99 is wrong by orders of magnitude | histogram unit is seconds and the panel says milliseconds | read `unit` from `distributed_metadata` before labelling the axis |
| result disagrees with the SigNoz panel | missing `bitAnd(flags, 1) = 0` | add the flags filter |
| the join returns nothing for a reduced metric | joined on `fingerprint` where the reduced family uses `reduced_fingerprint` | check `distributed_metric_reduction_rules`, then join on `reduced_fingerprint` |
| the query times out on a long window | raw sample scan where a rollup exists | see *Choosing raw or rollup* |
| the metric is not in `distributed_time_series_v4` | it is reduced, or it stopped reporting | check `distributed_metadata.last_reported_unix_milli` |

## When to stop and say so

- The metric name is unknown and the query is destined for a production panel: read
  `distributed_metadata` first; if it is unreachable, name that as the blocker instead of guessing a
  name.
- The install's table set differs from the families above: run the `SHOW TABLES` probes, then answer
  against what exists, and say which table you used.
