# Baseline Proposal: <one-line title>

<!--
Filename: YYYY-MM-DD-<kebab-slug>.md (real authoring date). One platform-shaped capability per file.
A baseline proposal asks the kit to OWN something new so consumers stop (or never start) writing it locally.
Location: same rules as kit-change-request.md. Preserve forever; decisions append.
-->

```yaml
type: baseline-proposal
date: YYYY-MM-DD
proposing_service: <service | platform-audit | kit-owner>
proposing_repo: <path/URL | kit repo>
proposed_home: <existing kit package | new package name, e.g. webhookkit>
kit_version_observed: <immutable version/commit>
consumers_needing_it_now: [<service>, ...]          # after reactivation; during kit-first: kit-design rationale
consumers_predicted: [<service>: <evidence — arch-doc §>, ...]
severity: blocking | high | normal
interim_implementation: none | KIT-WRAP at <file:line, date> | duplicated at <serviceA file, serviceB file>
status: proposed
```

## 1. The capability

<What the kit would own, stated as behavior. E.g. "A shared provider-webhook signature-verification middleware for
ProviderFacing routes, parameterized by scheme.">

## 2. Evidence it is baseline, not domain

<Why the mechanics are shared/platform-shaped and what stays domain-owned. The rule of two, made concrete, with
file:line or arch-doc § citations. If only one consumer needs it today, why is it still platform-shaped
(security-sensitive, contract-adjacent, predicted by a designed service)? Check first that a recorded decision has
not already ruled it service-local at this granularity (the Redis precedent: shared transport promoted to
rediskit, domain cache shapes ruled local) — if it has, present the new evidence that reopens the question, or do
not file. During kit-first, do not inspect consumers as proof.>

## 3. Proposed kit contract

<Public API sketch (Go signatures / middleware shape / DDL / env keys with defaults / metric names per kit naming
rules / error codes). What contracttest should assert. What stays configurable per service vs fixed by contract.>

## 4. Security, reliability, and operations

<Trust/privacy; idempotency/data truth; bounded concurrency/resources; observability; migration/rollback;
capacity.>

## 5. Adoption impact (phase-aware)

<During kit-first: all consumers NOT_ASSESSED_KIT_FIRST; motivate from kit design goals. After reactivation: per
consumer, the local code this retires (file paths, or arch-doc § for designed code) and how existing local
implementations converge — additive adoption, expand-contract for DDL, deprecation window if replacing something.>

## 6. Alternatives

<Stay-local-forever, wrap-per-service, a third design. Why the kit should own it anyway — or the honest case that
it shouldn't, if filing for a recorded negative decision.>

<!-- Kit owner appends "## Kit decision — YYYY-MM-DD" after intake. -->
