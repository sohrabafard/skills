# Metric time, joins and sample flags

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

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
