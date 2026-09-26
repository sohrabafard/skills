# Choosing the Query Surface

Read this before deciding whether an answer is Query Builder syntax, dashboard-panel SQL, or an
alert rule.

## The surfaces, and the one that is not settled

- **Logs, Traces and Metrics Explorer:** Query Builder and search syntax. Raw SQL is not the answer
  here unless the user says they will move the result into a dashboard panel.
- **Dashboard panel:** Query Builder when it can express the panel; ClickHouse SQL for the panels it
  cannot — custom joins, window functions, regex extraction over log bodies, aggregations outside
  builder syntax. This surface is confirmed by the vendor and by every worked example in this skill.
- **Alert rule:** Query Builder. **Whether this surface also accepts ClickHouse SQL is unconfirmed**
  and is settled by the test below, not by an assumption.

## Why the alert surface is unconfirmed

Public docs still disagree at the refresh date in `90-versions.md`: the
[ClickHouse overview](https://signoz.io/docs/operate/clickhouse/clickhouse-queries/)
mentions alerts in its introduction but limits SQL to dashboards in its notice; the
[log alert guide](https://signoz.io/docs/alerts-management/log-based-alerts/) offers SQL.
These describe public product surfaces, not the deployed capability.

## Released alert API lifecycle

Read the dated release and route evidence in `90-versions.md` before selecting an API.
History, rule CRUD, notification channels and query languages are separate contracts.
History migration proves neither SQL-alert support nor rule-list removal.

The [official history migration guide](https://signoz.io/docs/alerts-management/migrate-alert-history-api-v1-to-v2/)
deprecates four v1 POST history endpoints for security reasons. Its table says removed,
but the reviewed release still registers them; no removal release is confirmed.
Prefer supported v2 history on a version-matched target. Do not fall back to deprecated
v1 after a 401/403 or 404; resolve authorization, endpoint and version evidence first.
Retain legacy request shapes only when documenting an existing older consumer.

Migration changes: `stats`, `timeline`, `top_contributors`, `overall_status` move from
POST bodies to GET query parameters under `/api/v2/rules/{id}/history/`; `{id}` is a UUID.
Use millisecond `start`/`end`; timeline uses URL-encoded `filterExpression`, `inactive`
instead of `normal`, and `cursor` from `nextCursor` instead of offsets. Response changes
include `ruleId`, structured labels, numeric resolution seconds and optional related links.
The new `filter_keys`/`filter_values` endpoints use `startUnixMilli`/`endUnixMilli`.
Do not reuse timeline parameters for them. Validate request and response contracts
against the target release; the guide describes Viewer access, not every deployment's policy.

## Authorized deployment discovery

No network probe is authorized by loading this skill. Use supplied sanitized, version-matched
evidence first. If live discovery is explicitly authorized:

1. Read the release-matched rule-list API. The reviewed release still registers
   `GET /api/v1/rules`; paginate according to that release. Persisted SQL can survive an
   upgrade even when current saves reject it; treat it only as a discovery lead. Keep
   the surface unconfirmed without current version-matched acceptance evidence for
   that alert type. An empty list proves nothing.
2. Observe the rule editor and record which alert types expose a ClickHouse tab.
   A visible tab alone does not prove backend acceptance.
3. Saving or deleting a probe rule requires separate explicit authorization and an
   isolated notification-safe target. Do not assume a trivially true or disabled rule
   cannot notify. If that authority or environment is absent, stop at unconfirmed.

Record deployment identity, application version, alert types, timestamp, method and
sanitized acceptance evidence in `assets/alert-surface.json`. Keep secrets and customer
payloads out. A result applies only to that target and those alert types, not all installs.
A changed or unknown target identity/version invalidates the record. Public release notes
never set its status to `dashboards-and-alerts`.
The SQL checker reads the recorded status only; it does not verify deployment identity,
version, age or per-alert-type applicability. Bind those facts to current authorized evidence
before using the record; missing or stale evidence requires the unconfirmed fallback even
if the checker accepts a recorded status.

## What to do while the status is `unconfirmed`

Deliver the query in its dashboard-panel form, name the Query Builder path that would express the
same alert, and say the ClickHouse alert surface is unconfirmed on this install. Do not label the
SQL as alert SQL. `python3 scripts/check-signoz-sql.py --sql FILE --surface alert` reports finding
`S11` while the record says anything other than `dashboards-and-alerts`.

## Query Builder, when it is the answer

Service, operation and status filters; log body search and simple log aggregations; span filtering,
grouping and percentile charts; metric temporal plus spatial aggregation; and any ratio, which is a
formula rather than hand-written arithmetic. Do not answer a Query Builder question with ClickHouse
SQL unless the user asked for SQL or the panel needs what the builder cannot express. Choose the
metric aggregation from the metric's `type` read out of `distributed_metadata`, never from its name.

Name dashboard variables for what they select — `service_name`, `env`, `operation`, `status_code`.
Do not convert one into a ClickHouse macro unless the signal's reference confirms the exact spelling,
and preserve that signal's default time variables exactly as its reference gives them.

## Field ambiguity

Read `90-versions.md` for Query Builder context precedence; raw SQL names its context explicitly.
The same key can arrive as a resource attribute, a span or log attribute, and a top-level column,
and the three do not agree. Resolve it in this order:

1. Use the top-level or materialized column when the signal's reference lists one, because that
   column is what the collector populated and is the only one covered by an index.
2. Ask the install which contexts the key actually appears in. `signoz_metadata` carries
   `distributed_attributes_metadata` with `data_source`, `resource_attributes` and `attributes`,
   verified in the schema migrator on 2026-07-30; `mapKeys(resource_attributes)` versus
   `mapKeys(attributes)` on that table answers the question in one query instead of a doc page.
   Confirm the table exists first — `scripts/check-signoz-schema.py` probes for it.
3. Fix the instrumentation when one key is genuinely sent in two contexts. A query-side workaround
   leaves every future query wrong.
