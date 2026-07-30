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

The vendor contradicts itself on one page and across two pages, and all three statements were live
on 2026-07-30.

`https://signoz.io/docs/operate/clickhouse/clickhouse-queries/`, opening paragraph:

> You can write ClickHouse SQL queries directly to build custom dashboard panels and alerts when the
> visual Query Builder does not cover your use case.

The same page, further down:

> ClickHouse queries are only supported in **Dashboards**.

`https://signoz.io/docs/alerts-management/log-based-alerts/`:

> You can define your log query using **Query Builder** or **ClickHouse queries**.

No ordering of these sources resolves the question: the contradiction is inside a single page, so
"prefer the more specific page" and "prefer the more recent page" both return two answers. Reading
more documentation cannot settle it. Only the install can.

Picking a side is the expensive mistake in both directions. Assume alerts accept SQL and an agent
hands over a rule the surface rejects, which is a deliverable that cannot ship. Assume they do not
and an agent refuses work the install would have accepted, and pushes the user into a Query Builder
rewrite they did not need.

## The discovery test

Run it against this fleet's own SigNoz. Steps 1 and 2 are read-only; step 3 writes one throwaway
rule and deletes it.

1. **Read-only probe, settles a yes.** With any credential that can list alert rules,
   `GET /api/v1/rules` on the SigNoz API and look for a ClickHouse SQL string in the returned rule
   payloads. If an existing rule on this install already carries one, alerts accept ClickHouse SQL:
   record `dashboards-and-alerts` and stop. Finding none proves nothing — this fleet may simply
   never have written one — so continue to step 2.
2. **Observe the editor.** Open Alerts, then New Alert Rule, and for each alert type the install
   offers, record whether a **ClickHouse Query** tab appears beside the Query Builder tab. Record
   the alert types where it appears.
3. **Save one, because a rendered tab is not an accepted rule.** The vendor sentence "only supported
   in Dashboards" could describe a backend restriction that the frontend still draws. Where the tab
   appeared, enter a trivially true ClickHouse query, save the rule, and record whether the save
   succeeded or returned an error. Delete the rule afterwards. A saved rule is the observation that
   settles the question; a visible tab is not.

Record the outcome in `assets/alert-surface.json`, whose `status` is one of `unconfirmed`,
`dashboards-only`, or `dashboards-and-alerts`, together with the SigNoz version the observation was
made against.

**A recorded answer expires when the install's version changes.** `90-versions.md` gives the command
that reads the running version. When it differs from `signoz_version` in the record, treat the status
as `unconfirmed` again and rerun the test. This is what makes the record survive the vendor changing
its mind: the answer is dated evidence about one install, not a belief about the product.

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
