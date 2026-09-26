# Cumulative counter error ratio

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

### Error ratio from cumulative counters

Two counter-rate queries — one filtered to the error status, one unfiltered — joined on `ts`. Take
the status label's name and its permitted values from
`/alaa-services-contract` rather than from this example, which shows
the shape only.

Use the [counter-rate procedure](60-counter-rate.md) for reset handling and each inner rate.

```sql
WITH
errors AS (
  /* the counter-rate pattern in 60-counter-rate.md, plus one bounded status-label filter */
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
