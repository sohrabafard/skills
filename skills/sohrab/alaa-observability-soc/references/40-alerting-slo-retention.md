# Alerting, SLOs, and Retention

Load when the task writes or reviews an alert, page, SLO, burn-rate rule, evaluation window, or retention setting.

## Reason about latency in percentiles

A percentile answers "what latency were the slowest X% of requests at or below?" p99 = 500 ms means the slowest 1% were
worse than 500 ms. An average hides exactly that: a service can look healthy on average while its p99 times out for one
request in a hundred, which at fleet traffic is thousands of users per hour. Define latency SLOs on percentiles, instrument
them as histograms, and never aggregate an average or a summary quantile across replicas.

| Percentile | Reads as | Use for |
|---|---|---|
| p50 | the typical experience | baseline health, capacity trend |
| p90 | the start of the slow tail | early warning on degradation |
| p95 | common SLO target | user-facing latency SLOs and alerts |
| p99 | the tail unlucky users feel | strict SLOs, bottleneck hunting |
| p99.9 | rare but real worst case | high-traffic services where 0.1% is still many requests |

When a percentile alert fires, do not stop at the number: follow the bucket's exemplar to the trace
(`20-instrumentation-gates.md`).

## Burn-rate alerting for a 99.99% SLA

At 99.99% availability the error budget is 0.01%: about 4.3 minutes per 30 days, or 52.6 minutes a year. A static
threshold cannot be tuned against a budget that small — set it loose and the budget is gone before the alert fires, set it
tight and it pages on every deploy. So: **every user-facing availability and latency SLO alerts on error-budget burn rate
over multiple windows, never on a bare error-rate threshold.**

Burn rate is the multiple of budget consumption relative to spending it evenly across the window. Burn rate 1 exhausts the
budget exactly at the end of 30 days; burn rate 14.4 exhausts 2% of it in one hour.

| Long window | Short confirmation window | Burn rate | Budget consumed | Action |
|---|---|---|---|---|
| 1 hour | 5 minutes | 14.4 | 2% | page |
| 6 hours | 30 minutes | 6 | 5% | page |
| 1 day | 2 hours | 3 | 10% | ticket |
| 3 days | 6 hours | 1 | 10% | ticket |

Rules:

- Both windows must be burning for the rule to fire, and the short window is one twelfth of the long one. The short
  window is what stops a 30-second blip from paging; the long window is what stops a slow leak from going unnoticed.
- At 99.99% the fast-burn rule must evaluate over a window of one hour or shorter. A 6-hour-only rule can consume the
  entire 30-day budget before it fires once.
- Alert on the symptom — the SLI a user experiences. Cause alerts (CPU, pool saturation, queue depth, a single
  dependency's error rate) are ticket severity at most, because a cause that is not yet hurting a user is not worth
  waking someone for, and pages on causes are what train operators to ignore pages.
- Static thresholds remain correct for signals that have no error budget: readiness flapping, certificate expiry,
  dead-letter arrival, Collector export failure, disk or queue buffer filling, absent data. Use them there and only there.
- Low-traffic exception: where the service receives too few events for one error to be distinguishable from the budget —
  at 99.99% and 100 requests an hour, a single error is a hundred times the hourly budget — burn-rate alerting produces
  pure noise. Use an absolute error-count threshold plus an absent-data alert, and record in the alert that this is why.
- Every alert declares its no-data behaviour explicitly. An SLO alert that silently resolves when the metric stops
  arriving converts a total outage into silence, which is the worst possible failure of an alerting system.

## Alert gate

An alert is production-ready only with all of these. An alert missing any one is a blocking finding, because a page that
lands on nobody, or lands with no next step, costs more than no page at all.

- a named owner and an escalation path
- severity, and the page-or-ticket decision, justified against the rules above
- the user or business impact in one sentence
- the exact query or signal source
- threshold or burn rate, evaluation window, and short confirmation window, each with its rationale
- minimum-data condition and explicit no-data behaviour
- the false positives expected, named — deploys, scheduled jobs, known noisy dependencies
- a runbook that opens with the first three checks and ends with the rollback or mitigation path
- links to the dashboard, the log and trace query, and the exemplar path to a representative trace

A dashboard that no alert and no runbook step references is decoration; either wire it into one or delete it, because an
unreferenced panel is where a stale query hides until an incident trusts it.

## Retention

Every signal class carries a written retention period set at the pipeline, and a change that introduces a signal class
states its retention in the same change. Retention that is never stated becomes whichever default the backend shipped
with, discovered during the incident that needed the data.

| Signal class | Default retention |
|---|---|
| structured request and operational logs | 30 days queryable |
| error and exception records | 90 days |
| traces, the tail-sampled kept set | 7 days |
| metrics | 15 days at raw resolution, 13 months downsampled |
| profiles | 7 days |
| security and audit catalog events | 400 days minimum |
| SOC or SIEM delivery logs on our side | 90 days; the forwarded copies are retained by the customer |

Rules:

- Retention shorter than the longest evaluation window of any alert reading that signal is a broken alert. A 3-day
  burn-rate window needs more than 3 days of the underlying signal, and metrics retention must exceed the longest
  downsampled comparison a runbook asks for.
- Security and audit events get 400 days because a compliance or breach question is routinely asked more than a year
  after the event, and a 90-day store answers it with "we do not know" — which is indistinguishable from "it happened".
- Retention longer than the default requires a named owner and a written storage-cost figure.
- Shortening or removing retention on security or audit catalog events requires explicit operator approval. An agent does
  not make that change on its own reasoning, however sound the cost argument.
