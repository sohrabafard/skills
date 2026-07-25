# SOC Evidence and Egress

Load when the task designs a security-event catalog, forwards events to a customer SOC or SIEM, or collects evidence
during an incident.

Event names and machine-readable codes belong to `/alaa-services-contract` (`$alaa-services-contract` in Codex),
`references/20-…`, in its event and code naming contract. This file owns which events must exist, what each entry must
define, and what blocks an egress design.

## The security-event catalog

Every service maintains a catalog of its security-relevant events. Each entry defines all of:

- the event name and its paired code, taken from the contract
- severity, and the strength from the rubric in `10-signal-model.md`
- the required fields, beyond the mandatory correlation set in `20-instrumentation-gates.md`
- the detection intent — what an analyst is trying to catch with it, in one sentence
- the owner of the dashboard or saved query that reads it
- the alerting rule where one applies, meeting the gate in `40-alerting-slo-retention.md`
- the runbook link
- the retention period, which for catalog events is the security-event default in `40-alerting-slo-retention.md`

Gate: an event forwarded to a SOC has a name from the contract. Where the contract does not yet name it, add it there in
the same change, before the forward exists. A locally invented event name breaks every cross-service SOC rule the moment
a second service emits the same concept under a different name, and the break is invisible to the service that caused it.

Coverage floor: the catalog covers, at minimum, failed authentication, invalid or rejected credentials and tokens,
invalid request identity or trust context, authorization denial, rate-limit rejection, input-validation rejection,
suspicious or anomalous resource access, and readiness failure. A service that produces one of these outcomes and does
not emit a catalog event for it has an evidence gap, and the gap is a finding.

## Security-event semantics

Beyond the mandatory correlation fields, every security or audit event carries:

- event category and event action, so rules can match a class without enumerating names
- the decision, from a bounded set: allow, deny, challenge, error, or audit-only
- the policy or rule identifier that produced the decision
- an actor reference that satisfies the classification gate in `80-review-gates.md` — a hashed or tokenized identifier
  where correlation is required, never a raw identifier that the gate classifies as sensitive
- the target resource type and a safe target reference
- the source system and the trust boundary the request crossed
- a reason code, and a remediation hint where one exists
- the catalog schema version, so a consumer can tell a missing field from a field that never existed in that version

Reason for the schema version: a SOC rule written against version 1 and evaluated against version 2 fails silently by
matching nothing, and a security control that silently matches nothing is worse than one that is absent, because it is
believed.

## SOC and SIEM egress

Forwarding is a filtered fan-out branch — a Vector sink or a Collector exporter — that selects only the catalog events
the customer's rule set names, and forwards those. It is never an inline dependency: a SOC endpoint that is down or slow
must not slow, block, or degrade the SigNoz path or application traffic.

Raw application logs are never forwarded wholesale. Wholesale forwarding exports every field the application happens to
log today plus every field it adds tomorrow, which makes the privacy invariant unenforceable at the boundary where it
matters most.

From the customer, request exactly three things: the SOC endpoint, the required format and protocol, and the rule or
event set. Their rules become filter conditions in the pipeline config. Common ingestion shapes are syslog RFC5424, CEF,
or LEEF over TCP with TLS, OTLP, and Kafka or HTTP.

**An egress design is blocked until all of these are defined.** Each is here because its absence has a specific silent
failure mode.

| Requirement | Silent failure if absent |
|---|---|
| catalog and schema version | the customer's rules match nothing and nobody notices |
| tenant routing and isolation rule | one customer receives another customer's events |
| redaction or transformation applied before egress | sensitive data leaves the boundary irreversibly |
| transport security and endpoint authentication | security evidence travels in the clear |
| credential storage and a rotation owner | delivery stops at expiry, months later, with no alert |
| retry, replay, dead-letter, and drop behaviour | evidence is dropped during the incident it was collected for |
| delivery-failure alerting with a named owner | the branch is dead and the dashboards do not show it |
| a test event and a replay-safe verification procedure | nobody can prove the branch works without a real incident |

## Incident evidence collection

Collect evidence that separates an application fault from an infrastructure or upstream fault. Guessing between those two
is what makes incidents long.

- the exact time window, in UTC, with the boundary that defined it
- request IDs and trace IDs for representative failing requests, and for a comparable succeeding one
- response status and machine-readable code
- health and readiness output at the time
- database connectivity, timeout, and pool evidence
- upstream gateway error patterns
- queue depth, consumer lag, and consumer health
- worker restarts and memory trend
- Collector and sidecar exporter queue depth and send-failure counts, to rule out telemetry loss being mistaken for a
  traffic drop
- the saved query or panel that shows each of the above, so a second responder reproduces the view rather than the search
- Sentry issue IDs where exception grouping is part of the story

A succeeding request from the same window is not optional: without it, every difference between the failing request and
your mental model reads as a cause.

For security-relevant incidents, confirm that one controlled failure produces correlated metric, trace, log, alert, and
SOC evidence — the drill in `80-review-gates.md`. An evidence chain first exercised during a real incident is an evidence
chain nobody has tested.
