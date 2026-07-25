# Instrumentation Gates

Load when a change adds or alters instrumentation, resource identity, trace propagation, exemplars, or the name, type, or
meaning of a field, event, code, or metric that is already deployed.

Every name and value referenced here belongs to `/alaa-services-contract` (`$alaa-services-contract` in Codex):
`references/20-operational-and-observability-contract.md` for headers, event and code names, and the structured log field
contract; `references/21-alaa-platform-observability-directive.md` for resource attributes, OTLP env variables and their
defaults, metric families, label allow and deny lists, and package choices. This file states which of them bind, when,
and why. The platform invariants in `SKILL.md` also bind and are not restated here.

## Requirement levels

| Subject | Level | Reason the level is this high |
|---|---|---|
| W3C trace context propagated across every HTTP, RPC, queue, and worker hop | mandatory | one unpropagated hop truncates every trace crossing it, so the loss is fleet-wide, not local |
| stable resource identity on every signal | mandatory | see Resource identity below |
| `trace_id` queryable as its own field in logs and OTLP log records | mandatory | see Trace queryability below |
| the contract's baseline metric catalog, in full, for every family that applies | mandatory | a fleet dashboard breaks on the first service that names things differently, and the break stays invisible until an incident |
| the contract's correlation field set on every log, span, alert notification, and SOC event | mandatory, one exemption | see Correlation fields below |
| OpenTelemetry semantic conventions for HTTP, database, messaging, RPC, exceptions, logs, and resources | mandatory where a convention exists | an invented attribute name is invisible to every query, dashboard, and backend feature that expects the convention |
| structured JSON as the primary production log shape | mandatory | free-form text cannot be filtered by field, so it is unqueryable at fleet scale |
| profiles | opt-in per service, under the rate ceiling in `30-quantitative-budgets.md` | continuous profiling costs runtime and storage on every service to answer a question most services are not asking |

A service failing a mandatory level carries a **blocked** verdict, not an action item — see `80-review-gates.md`.

## Exemplars: the requirement level, stated once

Every service with a latency SLO emits latency histograms carrying exemplars, so an operator moving from a red percentile
panel to a concrete `trace_id` takes one step and no judgment. This is the only cardinality-safe bridge between the two
signals: a `trace_id` metric label would create one series per request and take the metrics backend down for every service
sharing it, while an exemplar rides inside the metric point and costs no series.

Exactly one exemption exists. A service whose metrics stack cannot carry exemplars end to end ships only when all three
hold:

1. a named human owns the gap — a role is not a name;
2. a written trace-linking workflow exists that gets an operator from a percentile spike to a concrete `trace_id`, naming
   the query, the join key, and the tool at each step, with no step that requires guessing a time window;
3. the readiness evidence records which of the two branches applies to this service, by name, so the next reviewer does
   not re-litigate it.

A service with a latency SLO, no exemplars, and no recorded workflow is not production-ready. There is no third state:
"exemplars where they add value" is not a requirement level, and a repo or skill phrasing it that way is wrong.

Enabling requirements: instrument latency as histograms and record exemplars on them; expose metrics as OpenMetrics with
exemplar storage enabled on the scrape path, or emit OTLP metrics carrying exemplars on the push path. Bucket boundaries
are in `30-quantitative-budgets.md`.

The Collector's span-metrics connector complements this by deriving rate, error, and duration metrics from traces, so the
metric and the trace already share service and operation identity. It serves the service-map view; it does not substitute
for exemplars, because it produces no per-request link.

The workflow this exists to serve: open the latency panel, find the slow bucket, follow that bucket's exemplar `trace_id`,
open the trace, read the span tree, fix the slowest span at its source, confirm the percentile recovers. To write the
SigNoz query for the panel or the exemplar lookup, hand off to `/alaa-signoz-clickhouse-docs` (`$alaa-signoz-clickhouse-docs`).

## Resource identity

Resource identity is the join key for every cross-signal and cross-service query. A log, a span, and a metric that
disagree about which service or environment produced them cannot be correlated at all, and `trace_id` does not rescue it:
a trace covers one request, while capacity, SLO, and cost questions are asked per service per environment.

Gate: resource identity resolves once at process start from deployment config, never per request and never defaulted to a
literal in source. A service whose identity or environment differs between its logs, metrics, and spans is a blocking
finding, because every fleet dashboard silently under-counts it.

## Trace queryability

Gate: an operator never parses the propagation header to find a trace during an incident. The header is the carrier; the
trace identifier is a first-class field in structured logs and OTLP log records, derived once at the request or job
boundary. A pipeline that builds OTLP log payloads by hand — Vector included — maps the native trace context fields
rather than leaving them empty.

Reason: incident queries are written under time pressure, and a query needing a substring extraction before it can filter
is a query that gets written wrong, or not at all.

## Correlation fields

The contract's correlation field set is mandatory on every service-level log record, span, alert notification, and SOC
event. Not best-effort: the request contract makes each field available at the boundary where the signal is produced, so
"not available" means the boundary was skipped, and the skipped boundary is itself the defect.

One exemption: a signal produced outside any request or job boundary — process start, a crash handler, a scrape-time
gauge — carries every field that exists at that point and **records which fields are absent, inside the record itself**,
using the field the contract names for that purpose; where the contract names none, add it there in the same change. An
absent field that is not recorded is a defect, because a silently missing correlation field is indistinguishable from
broken propagation, and an operator will spend the incident debugging the wrong system.

Security and audit events carry the additional semantics in `70-soc-evidence.md`.

## Changing a name, type, or meaning that is already deployed

Follow this procedure and no other, for any field, event, code, metric, or label already emitted in an environment a human
or an alert reads.

1. Add the new name alongside the old one and emit both.
2. Update every consumer of the old name — dashboards, alerts, saved queries, runbooks, SOC filter conditions, downstream
   pipelines — and record the list in the change.
3. Keep both running for at least the longest retention window of any consumer in that list, so no alert ever evaluates
   across a gap. Windows are in `40-alerting-slo-retention.md`.
4. Remove the old name in a separate change that cites the list from step 2.

Skipping step 3 blinds every alert whose evaluation window spans the cutover, and does so silently: the alert keeps
evaluating and keeps returning no data. The names themselves are the contract's to choose; this is how a chosen name
changes.

## Trace instrumentation floor

Traces cover at least the inbound request; the request pipeline and trusted-context normalization; outbound dependency
calls; significant database operations or query groups; cache calls; queue publish and consume; worker and scheduled jobs;
and any authorization or validation decision whose outcome an operator would need to explain. Retry, timeout, and
cancellation paths are visible as spans or span events, because an invisible retry looks identical to a slow dependency.

Attribute gates:

- Span and route identity use the templated route or a stable operation name, never a path containing live identifiers. A
  raw path produces one operation name per identifier value, which destroys every per-route aggregate.
- Real identifiers appear as span or log attributes only where they change what an operator can diagnose and the
  classification gate in `80-review-gates.md` permits the value. They never appear as metric labels.
- Query text is represented by a stable fingerprint, never raw SQL, which carries both user input and unbounded
  cardinality.
- Failures set span status and record the exception on the span. A span returning without status on a failed operation
  reports that failure as a success to every service-map and error-rate view.

## Export switches

Flush-on-operation is a verification switch, not a steady state: enabling it in a production environment requires a named
owner and a stated end time, and a service found running it without both is a blocking finding. Its default value is the
contract's; do not restate it here or in a repo doc.

Per-request structured logging stays unsampled where the service contract requires one record per request. Only trace
export is sampled, under `30-quantitative-budgets.md`.
