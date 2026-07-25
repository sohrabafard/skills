# Topic Map

`SKILL.md` is always loaded. Every file below loads only when its condition is met. One file answers most tasks and two
is normal; loading all of them means the task was not scoped.

| Load | When the task |
|---|---|
| `10-signal-model.md` | changes any code path — the failure-mode enumeration rule binds there — or asks which of log, metric, trace, exception, profile, or SOC event answers a question, and at what strength |
| `20-instrumentation-gates.md` | adds or changes instrumentation, resource identity, trace propagation, exemplars, or the name, type, or meaning of an already-deployed field, event, code, or metric |
| `30-quantitative-budgets.md` | adds or changes a metric label, a histogram bucket set, or a sampling or profiling rate, or asks whether a signal is affordable |
| `40-alerting-slo-retention.md` | writes or reviews an alert, page, SLO, burn-rate rule, evaluation window, or retention setting |
| `50-telemetry-pipeline.md` | touches Collector or Vector topology, config, processor placement, buffering, resilience, or the choice of collection agent |
| `60-sentry-and-profiling.md` | enables, tunes, or reviews Sentry, or turns profiling on or off |
| `70-soc-evidence.md` | designs a security-event catalog, forwards events to a customer SOC or SIEM, or collects evidence during an incident |
| `80-review-gates.md` | issues a pass, pass-with-actions, or blocked verdict, or audits a service for production and observability readiness |
| `90-source-map.md` | makes a current or version-sensitive claim about OpenTelemetry, SigNoz, Sentry, Vector, Prometheus, or a semantic convention |

## Routing assertions

These four prompts must route as stated. If one routes elsewhere, the routing in this skill is broken and is the first
thing to fix.

1. "Which skill should write a p99 latency dashboard query in SigNoz ClickHouse?" — `/alaa-signoz-clickhouse-docs`
   (`$alaa-signoz-clickhouse-docs` in Codex). This skill only for the signal design behind the panel.
2. "Review this service's observability for production readiness." — this skill, with `80-review-gates.md` loaded.
3. "Can I add `user_id` as a metric label?" — this skill, `30-quantitative-budgets.md`: refused as unbounded and
   sensitive; the value goes to a span or log attribute under the classification gate and is reached through `trace_id`.
4. "Update this skill, or write a new skill, prompt, or agent definition." — `/alaa-prompting-guide`
   (`$alaa-prompting-guide`). This skill states no model, version, or effort fact, so a runtime change leaves nothing
   here to update.
