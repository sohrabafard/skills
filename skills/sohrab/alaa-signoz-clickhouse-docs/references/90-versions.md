# Versions, Drift, and How to Re-derive Them

Read this before stating any SigNoz, collector or ClickHouse version, and before using a ClickHouse
function whose availability you have not checked.

A version written in a file goes stale silently. Every pin below carries the command that produces
it again, so a reader who doubts the number can settle it in one command instead of trusting the
date.

## Pins, all re-derived on 2026-07-30

| Fact | Value | Re-derived by |
|---|---|---|
| SigNoz application image | `v0.135.0` | `curl -s https://raw.githubusercontent.com/SigNoz/charts/main/charts/signoz/Chart.yaml \| grep appVersion` |
| `signoz-otel-collector` image | `v0.144.6` | `curl -s https://raw.githubusercontent.com/SigNoz/charts/main/charts/signoz/values.yaml \| grep -n 'tag: v0'` |
| ClickHouse, as SigNoz ships it | `25.12.5` | `curl -s https://raw.githubusercontent.com/SigNoz/charts/main/charts/signoz/values.yaml \| grep -n 'tag: 25'` |
| ClickHouse, upstream latest | `26.7`, released 2026-07-22 | fetch `https://clickhouse.com/docs/whats-new/changelog` and read the top release heading |
| SigNoz version actually running on a target | ask the install | `curl -s BASE_URL/api/v1/version` |

One number was read on 2026-07-29 and **not** re-read on 2026-07-30: the latest dated entry on
`https://signoz.io/docs`'s public changelog was `v0.133.0`, 2026-07-15, which is behind the chart's
`v0.135.0`. Treat the chart as the shipped image and the changelog as the last publicly documented
release, and treat neither as the answer for a specific install.

**The install's own version outranks every pin here.** `GET /api/v1/version` is registered at
`pkg/query-service/app/http_handler.go:539` under `am.OpenAccess`, so it needs no credential. Read
it before you rely on any version-sensitive behaviour, including the alert-surface record in
`assets/alert-surface.json`, which expires when this number changes.

## The ClickHouse drift, and the rule it forces

SigNoz pins ClickHouse **25.12.5** while upstream ships **26.7** — seven minor versions apart — and
the vendor disclaims the gap in its own chart, at `values.yaml:201`:

> ClickHouse image tag to use. SigNoz is not always tested with the latest version of ClickHouse.
> Only override if you know what you are doing.

**Rule: before using a ClickHouse function, syntax or setting you have not seen in this skill's
examples, run `SELECT version()` on the target and confirm the feature exists on that build.**
Current ClickHouse documentation describes 26.x. A function introduced after 25.12 parses on
clickhouse.com and fails on the SigNoz-shipped server, and the failure arrives as a syntax error in
a dashboard panel rather than at authoring time.

This is the whole reason the rule exists: the docs an agent reads and the server it targets are not
the same version, and nothing in the panel editor warns about it.

## What else varies by deployment

These are not constants; they are defaults of one install. Read the target before hardcoding any of
them into an answer.

- **Database names.** `signoz_logs`, `signoz_traces`, `signoz_metrics`, `signoz_metadata` and
  `signoz_meter` are defaults. SigNoz's reader takes table and database names as options, so a
  self-hosted install can differ. `SHOW DATABASES` settles it.
- **The 1800-second bucket offset.** Every logs and traces example pairs the time filter with
  `ts_bucket_start BETWEEN $start_timestamp - 1800 AND $end_timestamp`. The `1800` is the width of a
  bucket in the current schema, not a law; it is also the exact margin by which the resource table's
  TTL exceeds the index table's, which is what makes the resource CTE safe at the edge of the
  window. If a future schema changes the bucket width, this literal changes with it.
- **Retention.** `signoz_index_v3` carries a 15-day TTL in the migrator
  (`toDateTime(timestamp) + toIntervalSecond(1296000)`) and an operator can change it. A query over a
  window longer than retention returns a partial answer with no error, so state the window you
  queried beside the result.

Run `python3 scripts/check-signoz-schema.py` after any SigNoz upgrade: a failure there is the
observable form of "this skill is stale". Fix the reference before fixing the query the upgrade broke.
