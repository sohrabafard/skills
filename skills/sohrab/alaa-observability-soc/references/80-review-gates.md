# Review Gates and Readiness

Load when the task issues a verdict, or audits a service for production and observability readiness.

The output shape is the contract in `SKILL.md`. This file defines what each verdict means, the classification gate that
every emitted field passes, and the evidence a readiness claim requires.

## Verdicts

| Verdict | Meaning |
|---|---|
| pass | every mandatory requirement level in `20-instrumentation-gates.md` is satisfied, and evidence was observed for each |
| pass-with-actions | every mandatory level is satisfied; the open items are improvements, each with an owner and a stated deadline |
| blocked | at least one mandatory level is unsatisfied, or a gate below is unmet |

A finding that would let an incident go undiagnosed, or let sensitive data leave the boundary, is **blocked**, never
pass-with-actions. Downgrading it to an action item moves the decision to whoever reads the ticket last, which in practice
is nobody. Say what is blocked, say the smallest change that unblocks it, and stop.

## Classification gate

A telemetry change is not ready until every field it emits is classified into one of three:

- **Public or operational:** service name, route template, status code, error code, environment, version, bounded
  component or dependency name.
- **Internal but safe:** tenant or project identifier where policy permits, hashed actor identifier, request ID, trace
  and span IDs, rule and code names, feature-flag names.
- **Sensitive:** email, phone, national ID, address, access or refresh token, API key, password, session ID, cookie, raw
  JWT, raw request or response body, file content, payment data, health data, any customer-private text.

Rules:

- No sensitive field enters a metric label, log body, span attribute, Sentry context or breadcrumb, alert annotation, or
  SOC payload. This is the platform invariant, and this gate is where it is enforced field by field.
- Prefer a route template over a raw path, and a machine-readable error code over an exception message, because an
  exception message frequently contains the user input that caused it.
- Hash or tokenize an actor or customer identifier only where correlation genuinely requires it and the hashing strategy
  is approved. An unapproved hash gives false confidence: a low-cardinality salt-free hash of a phone number is
  reversible by enumeration.
- When a field's class is unclear, redact it and emit a stable internal reference an authorised human can resolve in the
  source system. An unclassified field shipped is a decision made by default.

## Readiness evidence

A service is observability-ready only when the evidence exists in the repository, its tests, or live telemetry. "It is
instrumented" is a claim; a query result is evidence.

| Area | Evidence required |
|---|---|
| traces | inbound server spans, outbound dependency spans, error status set on failures, operation names from route templates, propagation observed across one async hop |
| metrics | request rate, error rate, latency histogram with the platform bucket set, the percentile panels or their queries, and saturation metrics where the service owns a resource |
| logs | structured JSON, UTC timestamps, the mandatory correlation set, bounded event names, result and error codes, no sensitive field present |
| exemplars | which of the two exemplar branches in `20-instrumentation-gates.md` applies to this service, named; if the exemption branch, the named owner and the written trace-linking workflow |
| budgets | the worst-case series number from `30-quantitative-budgets.md`, the sampling decision in force, and the retention set for each signal class |
| alerts | the service's SLO and error signals each meet the alert gate in `40-alerting-slo-retention.md`, with owner and runbook |
| pipeline | config validates with the component's own command, self-telemetry visible, queues and retries monitored, and every remote hop has either persistent buffering or an explicitly accepted loss profile |
| SOC | the catalog covers the floor in `70-soc-evidence.md`, and any egress branch meets the egress gate |
| drill | one controlled failure produces correlated metric, trace, log, and alert evidence, plus SOC evidence where the event is security-relevant |

The drill is the row that fails most often and matters most: it is the only row that tests the chain rather than its
links. Run it before the verdict, not after.

## Gates owned elsewhere in this skill

Do not restate these; load the file and apply it.

| Question | File |
|---|---|
| Does this change enumerate the failure modes it introduces? | `10-signal-model.md` |
| Does the instrumentation meet its requirement level? | `20-instrumentation-gates.md` |
| Can this label, bucket set, or sample rate be afforded? | `30-quantitative-budgets.md` |
| Is this alert or retention setting production-ready? | `40-alerting-slo-retention.md` |
| Is the pipeline topology and config correct? | `50-telemetry-pipeline.md` |
| Is Sentry or profiling configured within policy? | `60-sentry-and-profiling.md` |
| Is the security catalog and any egress branch safe? | `70-soc-evidence.md` |

## Authority limits

Never authorise, and never perform on your own reasoning: a destructive change to production telemetry storage, deletion
or shortening of security or audit retention, exposure of a secret, an external SOC or SIEM egress activation, a deploy, or
a push. Each requires explicit operator permission, requested with the specific action named. Propose, do not proceed.
