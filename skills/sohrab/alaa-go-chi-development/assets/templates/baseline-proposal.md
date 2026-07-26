# Baseline Proposal: <one-line title>

<!--
Filename: YYYY-MM-DD-<kebab-slug>.md, real authoring date. One platform-shaped capability per file.
A baseline proposal asks the kit to OWN something new so consumers stop, or never start, writing it locally.
Location and phase fields: same rules as kit-change-request.md. Preserve forever; decisions append.
-->

```yaml
type: baseline-proposal
date: YYYY-MM-DD
proposing_service: <service | platform-audit | kit-owner>
proposing_repo: <path/URL | kit repo>
proposed_home: <existing kit package | new package name, e.g. webhookkit>
kit_version_observed: <immutable version/commit>
consumers_needing_it_now: [<service>, ...]   # only where the consumer-impact-claim cell permits; otherwise the marker string
consumers_predicted: [<service>: <evidence — arch-doc §>, ...]
severity: blocking | high | normal
interim_implementation: none | KIT-WRAP at <file:line, date> | duplicated at <serviceA file, serviceB file>
status: proposed
kit_phase: <phase name exactly as the read returned it>
phase_record: <docs/change-requests/... path the read named>
```

## 1. The capability

<What the kit would own, stated as behaviour. E.g. "A shared provider-webhook signature-verification middleware
for ProviderFacing routes, parameterized by scheme.">

## 2. Evidence that it is baseline, not domain

<Why the mechanics are shared and what stays domain-owned. Make the test in references/10- concrete: would a
second service have to change this code's behaviour — not its types, names, or wiring — before it could use it?
Cite file:line or arch-doc §. If only one service needs it today, say why it is still platform-shaped:
security-sensitive, contract-adjacent, or named in a fleet contract. Check first that no recorded decision already
ruled it service-local at this granularity — the rediskit precedent promoted the shared transport and left the
domain cache shapes local; if a decision covers it, present the new evidence that reopens it, or do not file.
Inspecting a consumer for proof requires the consumer-repo-read cell.>

## 3. Proposed kit contract

<Public API sketch: Go signatures, middleware shape, DDL, env keys with defaults, metric names per the kit naming
rules, error codes. What contracttest should assert. What stays configurable per service versus fixed by contract.>

## 4. Security, reliability, and operations

<Trust and privacy; idempotency and data truth; bounded concurrency and resources; observability; migration and
rollback; capacity.>

## 5. Adoption impact

<Governed by the consumer-impact-claim cell. Where it forbids the claim, motivate from kit design goals and record
the marker string. Where it permits: per consumer, the local code this retires — file paths, or arch-doc § for
designed code — and how existing local implementations converge: additive adoption, expand-contract for DDL, or a
deprecation window if it replaces something.>

## 6. Alternatives

<Stay-local-forever, wrap-per-service, a third design. Why the kit should own it anyway — or the honest case that
it should not, if you are filing for a recorded negative decision.>

<!-- Kit owner appends "## Kit decision — YYYY-MM-DD" after intake. -->
