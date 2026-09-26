# Raw and rollup selection

Read the [signal prerequisites](../clickhouse-metrics-reference.md) before this topic.

## Choosing raw or rollup

A dashboard panel's time window is chosen by whoever views it, not by whoever wrote the SQL. A
30-day panel over `distributed_samples_v4` reads every sample in 30 days; the same panel over
`samples_v4_agg_30m` reads one row per fingerprint per 30 minutes. The ratio is the ratio of the
scrape interval to 30 minutes.

State the bound the panel must hold as its window grows, and pick the table from it. Whether a bound
is real, how to find it from the system rather than assume it, and what makes it a budget rather than
a preference are owned by
`/alaa-algorithms-data-structures` `references/10-complexity-budget.md`.
This file owns only which SigNoz table each answer reads.

The worked examples linked from the signal reference read raw `distributed_samples_v4`. Each carries the window bound under which
that is the right table, in a `-- raw-scan-ok:` comment; `check-signoz-sql.py` rule `S6` reports a
metrics query that reads the raw table and carries neither a rollup nor that bound.

The rollup columns are `last`, `min`, `max`, `sum`, `count` per `(env, temporality, metric_name,
fingerprint, unix_milli)`. For a gauge, `last` replaces `avg(value)`. For a cumulative counter,
`last` is the value to difference. `sum`/`count` gives a mean without reading samples.
