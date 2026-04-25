---
name: alaa-signoz-clickhouse-docs
description: Use this skill when the user needs the right SigNoz docs page or a docs-grounded answer about OpenTelemetry instrumentation, migration, log collection, Collector setup, query builder behavior, dashboard variables, search syntax, field ambiguity, missing spans, traces, logs, or SigNoz troubleshooting. Also use it when the user needs a SigNoz ClickHouse dashboard query over traces or logs, or when an existing SigNoz query or trace-quality issue needs to be fixed. Do not use it for generic ClickHouse outside SigNoz, PromQL-only metrics work, or non-SigNoz observability unless the task depends on SigNoz docs or SigNoz table conventions.
---

# Alaa SigNoz ClickHouse Docs

This skill merges two jobs that often belong together:

1. find the best official SigNoz docs page and answer from it
2. write or repair SigNoz ClickHouse queries for dashboard panels over logs or traces

Keep the flow simple. First classify the task, then load only the smallest reference file that fits.

## Quick start

1. Read `references/source-map.md` when the task mentions latest/current schemas, migration, instrumentation versions, Collector versions, query-builder behavior, field ambiguity, or broken live queries.
2. If the task is broad, read `references/00-topic-map.md` first.
3. Classify the task as one of these modes:
   - docs lookup or docs-grounded answer
   - ClickHouse query writing or query repair
   - missing-spans or trace-quality troubleshooting
   - mixed task: docs first, then query
4. Read only the reference files for that mode.
5. Give a direct answer, not a long research diary.

## When NOT to use

- Do not use for generic ClickHouse work outside SigNoz schemas.
- Do not use for PromQL-only metrics tasks.
- Do not use for observability design that does not depend on SigNoz docs or tables.

## Mode 1: Docs lookup or docs-grounded answer

Use official `signoz.io/docs` pages as the source of truth.

### How to search

- Start with `references/docs-routing.md`.
- If the topic is instrumentation, migration, or collector setup, also read `references/instrumentation-routing.md`.
- If the topic is log ingestion, also read `references/log-collection-routing.md`.
- If the topic is query builder, search syntax, field ambiguity, or variables, also read `references/query-language-routing.md`.
- If the topic is "missing spans", parent spans, broken trace trees, or traceparent propagation, also read `references/observability-guardrails.md` and `references/clickhouse-traces-reference.md`.

### Retrieval rules

- Prefer official SigNoz docs over blogs, issues, or third-party posts.
- Treat community posts, Stack Overflow, and issue threads as troubleshooting-only unless SigNoz or OpenTelemetry docs confirm the guidance.
- If your environment can request markdown, prefer the docs page with `Accept: text/markdown`.
- If markdown fetch is not available, open the normal docs page and cite the canonical URL.
- Fetch only the top 1 to 3 pages that directly help with the task.
- If two pages overlap, prefer the more specific page and prefer the newer product-area page over an older generic page.
- If the user asked for “the right page”, return the single best page first and add only the most useful alternate pages.

### Output rules for docs tasks

- Lead with the best page.
- Say why that page is the best fit in one or two short sentences.
- Add alternates only when they change the setup path, platform, or troubleshooting path.
- Keep the answer grounded in the fetched page content.

## Mode 2: ClickHouse query writing or query repair

First detect the signal.

- Logs: log volume, severity, body text, container logs, structured fields
- Traces: spans, latency, error spans, HTTP operations, DB operations, service breakdowns

Then read exactly one reference:

- Logs: `references/clickhouse-logs-reference.md`
- Traces: `references/clickhouse-traces-reference.md`

Also read `references/observability-guardrails.md` if the query depends on service identity, trace-log correlation, field ambiguity, or instrumentation quality.

## Mode 2.5: Missing-spans or trace-quality troubleshooting

Use this mode when SigNoz shows "This trace has missing spans", when server spans have unexpected parent span IDs, or when the task mentions parent spans or `traceparent` propagation.

1. Open the official SigNoz traces page: `https://signoz.io/docs/userguide/traces/#missing-spans`.
2. Use SigNoz MCP first for live evidence:
   - search recent traces for the service
   - inspect `parent_span_id`, `span_id`, `trace_id`, `name`, and `spanKind`
   - group by operation and parent span id when the pattern is unclear
3. If ClickHouse access is available, use the missing-parent anti-join in `references/clickhouse-traces-reference.md`.
4. If the problem is in a Laravel or PHP service, pair with the repo/PHP/Laravel skills before editing code.
5. Fix instrumentation at the source:
   - preserve a valid inbound `traceparent` for propagation
   - never generate a fake `traceparent` and then extract it as an OpenTelemetry parent
   - for missing or invalid inbound context, start the request server span as a root span
   - when possible, use the actual started span context for response/log correlation
   - use generated fallback `traceparent` values only when telemetry is disabled or fail-open behavior prevents reading the real span context
6. Verify with both local tests and live SigNoz/ClickHouse evidence. A direct request with no inbound `traceparent` should produce a server/root span with an empty parent span id, not a random missing parent.

### Query writing rules

- Use distributed tables, not local tables.
- Use the correct SigNoz time variables for the signal.
- Add the `ts_bucket_start` filter with the `- 1800` start offset.
- Add the resource-filter CTE only when filtering on resource attributes.
- Use `GLOBAL IN` for the resource fingerprint subquery.
- Prefer indexed or pre-extracted columns over map access when they exist.
- Return the right shape for the panel:
  - timeseries: `ts`, `value`
  - value widget: one row with `value`
  - table: labeled columns for grouped breakdowns
- Keep placeholders explicit when exact field names are unknown, for example `{{service_name}}` or `{{attribute_key}}`.
- If a query is broken, explain the issue briefly, then give the corrected query.

### Output rules for query tasks

- State the panel type and any important assumptions.
- Give the final SQL in one block.
- Add one short note about variables, placeholders, or known limits only if needed.

## Mode 3: Mixed task

For tasks like “find the right instrumentation guide and then write a dashboard query”, do this in order:

1. locate the official docs page
2. extract the setup choice that matters
3. write the query with the correct signal and schema
4. keep the final answer compact and task-focused

## Instrumentation and data-quality guardrails

When the docs do not fully answer a design tradeoff, use `references/observability-guardrails.md`.

Use those guardrails especially for:

- choosing between SDK, Collector, and file-based log collection
- deciding where `service.name` belongs
- keeping `trace_id` queryable in logs
- avoiding high-cardinality metric labels
- fixing field ambiguity at the instrumentation source instead of hiding it in queries

## Pairing rules

If the user wants actual code changes in an application:

- use this skill to choose the official SigNoz path and the right telemetry rules
- then pair with the repo or language skill that will edit the code

## Subagent Strategy

If multi-agent support is available and the task is broad, split it like this:

- one read-only agent for official docs page selection
- one read-only agent for ClickHouse query drafting or repair
- merge the outputs into one final answer

Do not spawn extra agents for simple single-page lookups or one small query.

## Failure handling

- If the exact docs page is unclear, return the best starting page plus the next best narrow page.
- If the user does not give enough detail for a query, make the smallest safe assumption and use clear placeholders.
- If the task is actually about SigNoz search syntax or Query Builder, do not answer with ClickHouse unless the user explicitly asks for SQL.
- If the task is generic ClickHouse with no SigNoz context, do not use this skill.
