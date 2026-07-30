# Topic Map

The only router in this skill. Find the row whose situation matches yours and read that one file.
Read a second file only when its own row also matches.

| You are about to | Read |
|---|---|
| write or repair ClickHouse SQL over log records | `clickhouse-logs-reference.md` |
| write or repair ClickHouse SQL over spans | `clickhouse-traces-reference.md` |
| write or repair ClickHouse SQL over metric samples, a counter rate, an error ratio, or a histogram quantile | `clickhouse-metrics-reference.md` |
| decide whether a request belongs in Query Builder, a dashboard panel, or an alert rule, or promise a ClickHouse alert path | `query-language-routing.md` |
| explain or diagnose a trace SigNoz reports as having missing spans, or a span whose parent was never collected | `40-missing-spans.md` |
| answer what calls what, read the service dependency graph, or explain a missing edge in it | `50-service-topology.md` |
| state a SigNoz, collector or ClickHouse version, or judge whether a ClickHouse feature exists on the target | `90-versions.md` |
| find the current SigNoz docs page, or weigh a docs page against source, a blog post or a memory | `10-docs-navigation.md` |
| finalise a query that will be pasted into a production dashboard or alert | `validation-checklists.md` |

## Rows that are one situation, not two

**Missing spans start at `40-missing-spans.md` and stay there.** That file states the causes, the
instrumentation fix, and the anti-join, and it names the one query in
`clickhouse-traces-reference.md` you need if you have ClickHouse access. Do not start from the
traces reference for a missing-spans question: the anti-join tells you which spans are missing and
not why, and the why is what closes the ticket.

**A missing dependency-graph edge is a missing-spans question wearing a different hat.** Read
`50-service-topology.md` first for what the graph is a lower bound on, then `40-missing-spans.md`
for why a span never arrived.

**A docs question plus a SQL question is two tasks.** Answer the docs one from
`10-docs-navigation.md`, then the SQL one from the signal reference. Do not open a routing file to
answer a schema question — every schema fact this skill asserts lives in the three ClickHouse
references and is checked by `scripts/check-signoz-schema.py`.
