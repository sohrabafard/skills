# Observability and the Runtime API

## What this file owns

The **directive half**: how a signal is emitted, where the exporter binds, what the Runtime API
exposes, how a log line is assembled. It does not own which signals are required, what alerts on
them, or what they are called.

- **Which signal is required and what gates on it** — `/alaa-observability-soc`.
- **Every shared name and value** — the log field names, the metric catalog, `OTEL_*` names and
  defaults — `/alaa-services-contract`.

## Operator routes

When changing request logs, read [Logging](60-observability-and-runtime/10-logging.md) for the log-format fields, interpretation and collector boundary.
When enabling scraping, read [Prometheus](60-observability-and-runtime/20-prometheus.md) for the build prerequisite, exposition parameters and listener reachability.
When administering HAProxy, read [Runtime API](60-observability-and-runtime/30-runtime-api.md) for socket privileges, commands and protected access.
When counters must survive reload, read [Persistent stats](60-observability-and-runtime/40-persistent-stats.md) for shared-memory scope, mounts and experimental branch differences.
When adding tracing, read [Tracing](60-observability-and-runtime/50-tracing.md) for component/build selection and observability policy ownership.
