# Finding the Current SigNoz Docs Page

Read this when the answer is a documentation page rather than a query, or when two sources disagree.

## Source precedence, strongest first

1. **The target install** — `SHOW TABLES`, `DESCRIBE TABLE`, `SELECT version()`,
   `GET /api/v1/version`. A live schema outranks every document: the document describes a release,
   the install is the fact.
2. **SigNoz source** — the schema migrator in `signoz-otel-collector`, `query-service` in
   `SigNoz/signoz`. Outranks the docs, because the migrator is what created the tables. Cite the file
   and the symbol, never a line number: line numbers move between reads.
3. **Official SigNoz and OpenTelemetry documentation.** Authoritative for surface behaviour,
   dashboard variables and the documented query idioms.
4. **Community material** — issues, Stack Overflow, blogs. Use it to recognise an observed failure,
   never to establish a schema, a macro or a UI capability.

When tiers 2 and 3 conflict, state both and name which you followed. When tier 3 conflicts with
itself, reading more cannot resolve it — see the alert-surface case in `query-language-routing.md`
for the pattern that does. Every factual claim added to this skill carries its source and the date it
was read; a claim with no date is treated as unverified.

## Fetch a current source rather than answering from memory when the task mentions

a table, column, macro or variable name; the words latest or current; a SigNoz version or upgrade; a
live query failing on the target; a histogram or a metric-reduction rule; a query destined for a
production panel; or a ClickHouse function this skill's examples do not already use.

This file lists no navigation menu on purpose. SigNoz reorganises its docs tree between minor
releases, so a curated table of twenty URLs is stale the month after it is written and gives no signal
when it goes stale. What survives a reorganisation is the method plus the few URLs that have outlived
every rename. `python3 scripts/check-signoz-links.py --skill-dir .` is what turns "these links still
work" from a belief into an exit code.

## The six URLs that carry schema and surface facts

These are the pages this skill's factual claims rest on. Each was fetched and its content quoted on
the date beside it. Fetch the page again before contradicting it.

| Page | URL | Last read |
|---|---|---|
| Logs ClickHouse schema and variables | https://signoz.io/docs/userguide/logs_clickhouse_queries/ | 2026-07-29 |
| Traces ClickHouse schema and variables | https://signoz.io/docs/userguide/writing-clickhouse-traces-query/ | 2026-07-29 |
| Metrics ClickHouse schema and variables | https://signoz.io/docs/userguide/write-a-metrics-clickhouse-query/ | 2026-07-29 |
| ClickHouse query surface, and the contradiction | https://signoz.io/docs/operate/clickhouse/clickhouse-queries/ | 2026-07-30 |
| Log-based alerts, the other side of that contradiction | https://signoz.io/docs/alerts-management/log-based-alerts/ | 2026-07-30 |
| Missing spans | https://signoz.io/docs/userguide/traces/ | 2026-07-30 |

## Finding any other page

Search rather than guessing a path, because a guessed SigNoz docs path returns a soft 404 that
renders like a real page:

```
site:signoz.io/docs signoz <topic>
site:signoz.io/docs signoz <language> instrumentation
site:signoz.io/docs signoz <platform> logs
site:signoz.io/docs signoz query builder <topic>
```

Prefer the narrow page that finishes the task over the broad page that mentions the topic, and the
current product-area page over a legacy guide when both rank. Return one best page and at most two
alternates, and only alternates that change the setup path.

Some environments fetch a SigNoz docs page cleanly as markdown by sending `Accept: text/markdown`.
Use it when it works; otherwise cite the canonical HTML URL.

## Cloud versus self-hosted, which changes the answer

A SigNoz Cloud target expects an OTLP endpoint of the shape `https://ingest.REGION.signoz.cloud:443`
and an ingestion-key header. A self-hosted target uses its own endpoint and no ingestion key. The
instrumentation guides are otherwise the same, so decide this before quoting any endpoint or header,
and never copy a Cloud ingestion header into a self-hosted answer.

## Which log path to recommend

Decide the collection path before opening any language guide, because the language guide assumes a
path.

- Logs that must correlate with traces: a logger bridge or SDK path carrying `trace_id` and
  `span_id` into the record.
- Logs already on a file or stdout: file collection through the Collector, which survives an
  application restart that an in-process exporter does not.
- Container, Kubernetes, host or syslog records: the Collector receiver for that source, never in-app
  SDK logging for records the runtime already emits.
- An existing FluentBit, Fluentd, Logstash or Vector pipeline: forward from it rather than replace it.
  A second collection path produces every record twice, which costs money and breaks counts — and
  Kubernetes auto-collection plus SDK logging on one service is that same mistake. Name one owner for
  a service's logs.

Prefer the Collector whenever the requirement is retries, batching, redaction, routing, fan-out,
centralised credentials, or filtering before data leaves the environment.

Whether a log record may leave the environment at all, and what must be redacted before it does, is
decided by `/alaa-observability-soc` (`$alaa-observability-soc`), not here.
