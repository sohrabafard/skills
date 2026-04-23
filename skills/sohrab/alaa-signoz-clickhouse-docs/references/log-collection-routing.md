# Log Collection Routing

Use this file when the user asks how to send logs to SigNoz or which log-ingestion path to choose.

## First question: what kind of logs?

- Application logs from code you control
- Container or platform logs
- Cloud-service logs
- Logs already collected by another agent or pipeline

## Best decision page

Start with:

- `https://signoz.io/docs/logs-management/send-logs/collection-methods/`

Use it whenever the user is unsure between SDK, HTTP, file, Collector, or processor-based paths.

## Recommended path by situation

| Situation | Best default path | Best page |
|---|---|---|
| App logs and you need trace-log correlation | SDK or logger bridge that preserves trace context | Start with `collection-methods/`, then the exact language or logger page |
| App logs and you want a simple custom push path | HTTP logs API | `https://signoz.io/docs/userguide/send-logs-http/` |
| App logs written to file or stdout and you want reliability | File + OpenTelemetry Collector | `https://signoz.io/docs/userguide/collect_logs_from_file/` |
| Docker container logs | Collector with Docker log collection | `https://signoz.io/docs/userguide/collect_docker_logs/` |
| Kubernetes pod or container logs | Kubernetes agent or Collector-based path | Start from `send-logs-to-signoz/` and choose the k8s guide |
| Syslog or host logs | Collector receiver path | `https://signoz.io/docs/userguide/collecting_syslogs/` |
| FluentBit, Logstash, or another log processor already exists | Reuse that pipeline and forward to SigNoz | Use the exact integration page from the send-logs hub |
| Logger-specific app guidance, for example Zap | Use the exact logger page | Example: `https://signoz.io/docs/logs-management/send-logs/zap-to-signoz/` |

## Main hubs

- Broad log-ingestion hub:
  - `https://signoz.io/docs/logs-management/send-logs-to-signoz/`
- Application logs hub:
  - `https://signoz.io/docs/logs-management/send-logs/application-logs/`
- Logs management overview:
  - `https://signoz.io/docs/logs-management/overview/`

## Important routing rules

- Do not jump straight to a random language guide before deciding the collection path.
- If the user needs trace-log correlation, prefer a path that preserves or injects `trace_id` and `span_id` cleanly.
- If platform logs are already on disk or emitted by the runtime, prefer file or agent collection over in-app SDK logging.
- If the user already runs FluentBit, Fluentd, Logstash, Vector, or another collector, prefer integration over replacing the whole pipeline.
- If the user uses Kubernetes auto log collection and also wants SDK-based application logs, warn about duplicate collection and prefer one clear ownership path.

## What to say in the answer

- Name the recommended path in plain language.
- Give the best page first.
- Briefly explain the tradeoff: correlation, reliability, operational simplicity, or reuse of existing pipeline.
