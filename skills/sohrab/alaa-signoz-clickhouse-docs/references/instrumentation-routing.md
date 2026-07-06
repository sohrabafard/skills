# Instrumentation Routing

Use this file when the user asks about OpenTelemetry instrumentation, migration, Collector setup, or how to get telemetry into SigNoz.

## Decision flow

### 1. Is the app already instrumented with OpenTelemetry?

- Yes:
  - Start with `https://signoz.io/docs/migration/migrate-from-opentelemetry-to-signoz/`
  - Then fetch the language-specific SigNoz instrumentation page only if the user needs SDK syntax examples
- No:
  - Start with `https://signoz.io/docs/instrumentation/overview/`
  - Then open the matching language or framework page from `https://signoz.io/docs/instrumentation/`

### 2. Does the user need application instrumentation or collection infrastructure?

- Application instrumentation:
  - Use the instrumentation pages first
  - Prefer the exact language or framework page
- Collection infrastructure, routing, or processing:
  - Start with `https://signoz.io/docs/opentelemetry-collection-agents/get-started/`
  - Then use Collector configuration pages

### 3. Is the target SigNoz Cloud or Self-Hosted?

- Cloud:
  - Expect an OTLP endpoint like `https://ingest.<region>.signoz.cloud:443`
  - Expect an ingestion key header
- Self-Hosted:
  - The setup is similar, but the endpoint changes and the Cloud ingestion key header is removed
  - Use the same core instrumentation guides and adapt the endpoint/auth details

### 4. Does the user need traces only, or traces plus logs?

- Traces or APM only:
  - Use the language instrumentation page
- Traces plus logs from application code:
  - Use the instrumentation page for traces
  - Then use `log-collection-routing.md` for the best log path
- Platform or infrastructure logs:
  - Do not default to SDK logging
  - Route through Collector or the platform-specific logs guide

## When to prefer the Collector

Prefer the Collector when the user needs any of these:

- one place for retries, batching, redaction, routing, or fan-out
- platform or infrastructure log collection
- multiple telemetry sources
- centralized credentials and export rules
- filtering or cost control before data leaves the environment

Good pages:

- Why use Collector:
  - `https://signoz.io/docs/opentelemetry-collection-agents/opentelemetry-collector/why-to-use-collector/`
- Collector configuration:
  - `https://signoz.io/docs/opentelemetry-collection-agents/opentelemetry-collector/configuration/`

## Helpful language and framework anchors

Use `https://signoz.io/docs/instrumentation/` when you need the exact language page. Common choices visible from the docs hub include:

- Node.js
- Python
- Java / Spring Boot
- Go
- PHP
- Laravel
- .NET
- Ruby
- Next.js
- React
- Cloudflare Workers

## Answering rules

- For a vague “How do I instrument this?” question, give the single best starting page plus the exact next page.
- For migration questions, lead with the migration page, not the fresh-install quickstart.
- For mixed traces and logs questions, decide the traces path and log path separately.
- If the user is confused by field ambiguity later, route them to `query-language-routing.md` and tell them to fix the instrumentation source rather than only changing the query.

## Current-doc freshness note

SigNoz instrumentation and Collector pages move. Recheck official docs when endpoint syntax, ingestion headers, language SDK versions, auto-instrumentation packages, migration behavior, or Cloud/Self-Host differences affect the answer.
