# Docs Routing

Use this file to choose the best official SigNoz docs page quickly.

All links below are official `signoz.io/docs` pages that were useful and reachable when this skill was built.

## Core entry pages

| Need | Best starting page | Use it when | Notes |
|---|---|---|---|
| Instrument an app with OpenTelemetry | `https://signoz.io/docs/instrumentation/overview/` | The user wants a modern guided start for traces and APM | Good first stop for quick orientation and next steps |
| Jump straight to language or framework guides | `https://signoz.io/docs/instrumentation/` | The user already knows the language or framework they need | Good directory-style hub |
| Migrate an already-instrumented app to SigNoz | `https://signoz.io/docs/migration/migrate-from-opentelemetry-to-signoz/` | The app already uses OpenTelemetry and only the backend is changing | Especially useful for endpoint and header changes |
| Choose or understand the OpenTelemetry Collector | `https://signoz.io/docs/opentelemetry-collection-agents/opentelemetry-collector/why-to-use-collector/` | The user asks whether they should use a Collector | Good design-level page |
| Configure the Collector | `https://signoz.io/docs/opentelemetry-collection-agents/opentelemetry-collector/configuration/` | The user needs processor, receiver, exporter, or pipeline details | Use after the “why use collector” page |
| Choose a log-ingestion path | `https://signoz.io/docs/logs-management/send-logs/collection-methods/` | The user is unsure whether to use SDK, file, HTTP, or agent paths | Best decision page for logs |
| Browse log source guides | `https://signoz.io/docs/logs-management/send-logs-to-signoz/` | The user needs a platform, language, or collector-specific log guide | Broad log-ingestion hub |
| Logs Query Builder | `https://signoz.io/docs/userguide/logs_query_builder/` | The user wants SigNoz query UI behavior, not ClickHouse SQL | Good for log filtering, grouping, and body queries |
| Query Builder v5 | `https://signoz.io/docs/userguide/query-builder-v5/` | The user asks about the current structured query interface | Prefer this over older general Query Builder pages |
| Search syntax | `https://signoz.io/docs/userguide/search-syntax/` | The user asks how to filter logs, traces, or metrics in SigNoz search | Use with operators and field-context docs |
| Field ambiguity and type handling | `https://signoz.io/docs/userguide/field-context-data-types/` | The user sees ambiguous fields or type issues | Useful for `resource.` vs `attribute.` questions |
| Dashboard variables | `https://signoz.io/docs/userguide/manage-variables/` | The user wants reusable dashboard filters or template dashboards | Useful with panel authoring |
| Logs ClickHouse dashboard SQL | `https://signoz.io/docs/userguide/logs_clickhouse_queries/` | The user wants logs panel SQL | Main official schema page for logs |
| Traces ClickHouse dashboard SQL | `https://signoz.io/docs/userguide/writing-clickhouse-traces-query/` | The user wants traces panel SQL | Main official schema page for traces |

## Page selection rules

- Prefer the narrow page that finishes the task, not the broadest page that merely mentions the topic.
- Prefer current product-area pages over older legacy guides when both exist.
- When a question mixes setup and troubleshooting, fetch the setup page first, then the closest troubleshooting page.
- When the user asks for “the right docs page”, return one best page and at most two alternates.

## Good search patterns

Use these patterns if the right page is not obvious:

- `site:signoz.io/docs signoz <topic>`
- `site:signoz.io/docs signoz <language> instrumentation`
- `site:signoz.io/docs signoz <platform> logs`
- `site:signoz.io/docs signoz query builder <topic>`
- `site:signoz.io/docs signoz clickhouse <logs|traces>`

## Markdown fetch note

Some environments can fetch SigNoz docs cleanly as markdown by requesting the docs page with `Accept: text/markdown`.
If that is available, prefer it.
If not, use the canonical HTML docs page and cite the page URL.
