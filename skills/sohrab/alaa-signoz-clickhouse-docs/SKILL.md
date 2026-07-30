---
name: alaa-signoz-clickhouse-docs
description: "SigNoz ClickHouse SQL for dashboard panels over OpenTelemetry logs, traces and metrics, plus docs routing: the vendor-owned signoz_logs, signoz_traces and signoz_metrics tables, their sorting keys, the bucket-filter and resource-CTE idioms, rollup selection, missing-span diagnosis, and the service-topology read path. Use it to write or repair raw SigNoz panel SQL, to confirm a SigNoz table or column, to diagnose a trace with missing spans, or to choose the SigNoz docs page for a setup question. Do not use it to decide what a ClickHouse table must be, which /clickhouse-performance-schema-ops ($clickhouse-performance-schema-ops) owns; nor for telemetry requirement levels, cardinality ceilings or alert severity, which /alaa-observability-soc ($alaa-observability-soc) owns; nor for Vector pipeline config, which /vector-rust-observability-pipelines ($vector-rust-observability-pipelines) owns."
---

# SigNoz ClickHouse Docs and Query Reference

Write and repair raw ClickHouse SQL against SigNoz's vendor-owned tables, and route a SigNoz documentation question to the page that answers it.

## Three facts that decide every task here

**1. The SigNoz schema is vendor-owned and read-only to this fleet.** SigNoz's schema migrator creates and alters every table in `signoz_logs`, `signoz_traces`, `signoz_metrics`, `signoz_metadata` and `signoz_meter`, and the schema changes only when SigNoz is upgraded. Propose no `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `OPTIMIZE` or `SYSTEM` statement against a `signoz_*` table; report a schema defect to the vendor instead, because an unratified local change is overwritten by the next upgrade.

**2. A tenant predicate is not required on a SigNoz query.** All tenants report into one shared SigNoz, and everyone with access to that SigNoz is authorised to see every tenant's telemetry, because seeing it is how they fix it. A project whose telemetry must not be shared gets a separate SigNoz address selected by an environment variable, so the isolation is the address, not a `WHERE` clause. `clickhouse-performance-schema-ops` requires the tenant column first in `ORDER BY` and a tenant filter on every query; that rule governs tables the fleet's own ingest pipeline owns and does not transfer to `signoz_*` tables, because the fleet owns neither their sorting key nor their write path and cannot add a tenant column to either. Do not add a tenant predicate to a SigNoz query to satisfy that rule, and do not report its absence as a defect.

**3. The ClickHouse alert surface is unconfirmed, and this skill fails closed on it.** See the next section.

## The alert-surface gate

The vendor contradicts itself about whether a SigNoz alert rule accepts ClickHouse SQL, and both statements were live on 2026-07-30. Neither the vendor nor the owner has resolved it, so assume nothing and discover it. `references/query-language-routing.md` carries both quotes, both URLs, and the discovery test.

Read `assets/alert-surface.json` before answering any request for alert SQL. While its `status` is `unconfirmed`:

1. Run the discovery test in `references/query-language-routing.md` against this fleet's own SigNoz and record the result in `assets/alert-surface.json`. It needs one account that can open the alert-rule editor, and about one minute.
2. When the test cannot be run in this session, deliver the dashboard-panel form of the query and the Query Builder alert path, and state that the ClickHouse alert surface is unconfirmed on this install. Do not label SQL as alert SQL, because a rule the surface rejects is work that cannot ship.

`check-signoz-sql.py --surface alert` reports finding `S11` for exactly this case, so the gate is enforced rather than remembered.

## Rules that hold on every query

1. Name the signal before writing SQL — logs, traces, or metrics — and read only that signal's reference. Joining two `signoz_*` databases needs an explicit `JOIN ... ON`, a shared key and one time window, because the three families share no fingerprint space.
2. Bound every query in time with the variables that signal's reference names, and pair a logs or traces query with the `ts_bucket_start` predicate, because `ts_bucket_start` is the first column of the sorting key and a query without it reads every part in the partition.
3. Group only by a column whose distinct-value count is inside the ceiling that `/alaa-observability-soc` (`$alaa-observability-soc`) `references/30-quantitative-budgets.md` sets. That file states the number; this skill states none and enforces the denylist as `check-signoz-sql.py` rule `S7`.
4. Return the panel shape the widget expects: `ts` and `value` for a timeseries, one column named `value` for a value widget, labelled columns and a `LIMIT` for a table.
5. Keep an unknown value as an explicit placeholder — `{{service_name}}`, `{{metric_name}}`, `{{attribute_key}}` — rather than inventing one, and never put a credential, token or real customer payload in an example.
6. When the live schema cannot be reached, emit the query with a literal `-- UNVERIFIED SCHEMA: db.table` comment above it and name the command that verifies it. Never silently downgrade to this reference's assumption.

## References

Route the task through `references/00-topic-map.md`, which maps the situation you are in to the one file that answers it. It is the only router in this skill.

## Checkers

Run these from the skill directory. Exit `0` clean, `1` findings, `2` could not run; a `2` is never a pass. Each ships a red fixture reachable with `--self-test`.

- `python3 scripts/check-signoz-links.py --skill-dir .` — every URL in the skill resolves 200 and does not silently redirect to a docs index. Exits `2` when the network is unreachable, so a dead link can never read as clean.
- `python3 scripts/check-signoz-schema.py --describe-dir DIR` (or `--dsn URL`) — every table and column this skill claims is present on the target, and `signoz_index_v3` still sorts by `ts_bucket_start, resource_fingerprint` first. A finding here means this skill is stale against the installed SigNoz, not that your query is wrong: fix the reference first, then the query.
- `python3 scripts/check-signoz-sql.py --skill-dir .` — this skill's own examples obey the rules above. Add `--sql FILE` to check a query you are about to hand over.

## Not owned here

`clickhouse-performance-schema-ops` owns what a ClickHouse table must be — engine, sorting key, partitioning, TTL, compression — for tables the fleet controls.
`alaa-signoz-clickhouse-docs` owns how a SigNoz-owned table is queried, and states that those tables are vendor-owned and read-only to the fleet.
`vector-rust-observability-pipelines` owns what the pipeline writes into a ClickHouse table and how it behaves when that table is unreachable, and decides no schema.

Read-lane settings and scan-cost reasoning over `signoz_*` tables: `/clickhouse-performance-schema-ops` (`$clickhouse-performance-schema-ops`) `references/40-query-tuning-and-read-lane.md`. Telemetry requirement levels, gates and reasons: `/alaa-observability-soc` (`$alaa-observability-soc`). Who may hold a SigNoz credential, and what a saved panel executes with: `/alaa-security-review` (`$alaa-security-review`). Model and effort: `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`. Every other owner is named at the rule it governs inside `references/`.

## When NOT to use

- generic ClickHouse work outside the `signoz_*` databases
- deciding a table's engine, sorting key, partitioning or TTL, including for a `signoz_*` table
- PromQL-only questions that need no SigNoz docs routing
- observability design that does not depend on SigNoz schema, docs or UI behaviour
- SOC policy, Sentry role decisions, cardinality ceilings, exemplar architecture, Collector or Vector topology, and alert severity policy

## Output contract

For a docs task, return the one best page, why it fits, and only the alternates that change the setup path.

For a query task, return the panel type and signal, the assumptions and placeholders, the SQL in one block, and validation notes covering time bounds, table family, variables, resource filters, limits and any unresolved uncertainty. For a repair, name the defect, give the corrected query, and skip the research diary.

## Stop rules

Make the smallest safe assumption when a detail is missing. Ask only when the missing detail changes the signal, the table family, the time variables, the schema version, a production side effect, or what data is exposed. Never invent a SigNoz table, column, macro or UI capability; when the current docs or the live schema are required to answer, say so and name the command that would answer it.
