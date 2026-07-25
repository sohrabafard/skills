# Signal Model

Load when a change touches any code path, or when the task asks which signal answers a question and at what strength.

## Tool roles

OpenTelemetry is the instrumentation contract, not a dashboard: it standardises what a service emits and how context
propagates. SigNoz is the operational backend for traces, logs, metrics, dashboards, and alerts. Prometheus-compatible
metrics carry health, SLO math, and alerting. Sentry is a focused exception, release, and source-map tool, never a second
backend — the split and its gates are in `60-sentry-and-profiling.md`. Where signals travel between the service and the
backend is in `50-telemetry-pipeline.md`.

## Start from the diff, not from the question

Before a change is approved, enumerate the failure modes the change introduces, and name three things for each:

1. the signal that would show it — metric family, log event, or span;
2. the exact query an operator would run to see it, in the tool they would run it in;
3. whether it gets an alert, and at which strength from the rubric below, or is diagnostic-only.

A failure mode with no named signal is an undiagnosable failure mode, and the change is not done. "Existing telemetry
covers it" is a valid answer only when you name the existing signal and the query — an unnamed claim of coverage is how
a blind spot ships. Record the result in the `Failure modes introduced` field of the output contract, one line per mode.

Read the diff and check it against each class below. The list is the floor, not the ceiling.

| What the diff adds | Failure modes to enumerate |
|---|---|
| a call to another service or external system | timeout, connection refused, TLS failure, slow but succeeding, wrong or partial answer, retry amplification |
| a write | partial commit, duplicate on retry, lost update, constraint violation under concurrency |
| a cache | stale read, stampede at expiry, unbounded growth, key scope leaking across tenants |
| a queue producer or consumer | backlog growth, consumer lag, poison message, retry exhaustion, dead-letter arrival, out-of-order delivery |
| an authorization or validation decision | deny storm from one caller, silent allow on a missing rule, decision latency |
| a config knob | unset, invalid value, valid but outside the safe range, drift between replicas |
| concurrency — a pool, lock, or worker | pool exhaustion, lock contention, deadlock, thread or goroutine leak |
| a new route or job | never invoked, invoked far above forecast, error rate diverging from the service average |
| a new dependency on time or ordering | clock skew, expiry evaluated in the wrong zone, out-of-order state transition |

Where the failure mode concerns product-traffic *behaviour* rather than its *visibility* — how the pool should behave
once exhausted, whether to shed load — the behaviour belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla` in
Codex) and only the visibility belongs here. Name both owners in the change so neither half is dropped.

## Signal strength rubric

Choosing the strength is a separate decision from choosing the signal, and the weaker choice is the default: every
strength above `log only` costs either an operator's attention or a retention commitment.

| Strength | Bind it when |
|---|---|
| log only | needed for forensics or debugging, not actionable on its own |
| metric | durable trend, SLO math, or alerting on rate, error, duration, or saturation |
| alert | a human must investigate within a stated response window |
| page | urgent enough to interrupt an operator immediately |
| SOC event | security or audit evidence that must be retained, routed, or shared with a customer SOC |

## Which signal answers which question

| Question | Primary signal | Secondary |
|---|---|---|
| What happened, in detail? | logs | span attributes |
| Is the service healthy? | metrics | readiness logs |
| Should a human be alerted? | metrics plus an alert rule | logs plus runbook |
| Where did one request go? | traces | logs filtered by `trace_id` |
| Which code crashed? | exceptions | logs and traces |
| Which errors are new since the deploy? | Sentry issues and releases | SigNoz dashboards |
| Which service or dependency is slow? | traces plus latency histograms | logs |
| Is the queue backing up? | queue metrics | worker logs and traces |
| Why is this code expensive? | profiles | traces and metrics |

Rules:

- Logs carry detail and forensic context; they are never the instrument for a trend.
- Metrics carry health, trends, SLOs, and alerts; a metric is never the place to look up one request.
- Traces carry one request or one job journey end to end, and are the primary bottleneck tool.
- Exceptions carry code failures with stack traces.
- Profiles carry the cost of code, and only under the rate ceiling in `30-quantitative-budgets.md`.
- Averages answer no question in this table. Latency reasoning is percentile-based; see `40-alerting-slo-retention.md`.

## Order of work

Follow this order. Each step exists because skipping it produces a signal nobody can use.

1. Enumerate the failure modes the diff introduces, per the rule above.
2. Pick the primary signal and its strength for each mode.
3. Inventory what already exists — signal names, fields, dashboards, alerts, runbooks — before adding anything, so the
   change extends the fleet's shape instead of forking it.
4. Fix the signal contract: fields and semantics from `/alaa-services-contract` (`$alaa-services-contract`), and from
   this skill the requirement level, cardinality, sampling, retention, and named owner.
5. Decide the path: stdout, OTLP to the local sidecar, Prometheus scrape, SOC branch. See `50-telemetry-pipeline.md`.
6. Change implementation, dashboards, alerts, and runbooks in the same commit, because a dashboard that references a
   field the code no longer emits reads as an outage during the next incident.
7. Validate end to end: emit, ship, receive, query, alert. Report what you observed, not what you configured.
8. Report the remaining blind spots by name.
