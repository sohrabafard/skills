# Baseline Proposal: <one-line title>

<!--
Filename: YYYY-MM-DD-<kebab-slug>.md  (authoring date, real date from the environment)
Location: <consumer-repo>/docs/kit-change-requests/
          (design-phase or audit-originated: <kit-repo>/docs/change-requests/ directly)
One file per proposed baseline. Fully self-contained.
A baseline proposal asks the kit to OWN something new so consumers can stop (or never start) writing it locally.
-->

```yaml
type: baseline-proposal
date: YYYY-MM-DD
proposing_service: <news | notif | entitlement-api | tusd | platform-audit>
proposing_repo: <repo path/URL>
proposed_home: <existing kit package | new package name, e.g. rediskit>
consumers_needing_it_now: [<service>, ...]
consumers_predicted: [<service>: <evidence — arch-doc §>, ...]
severity: blocking | high | normal
interim_implementation: none | KIT-WRAP at <file:line> | duplicated at <serviceA file, serviceB file>
status: filed
```

## 1. The capability (one paragraph)

<What the kit would own, stated as behavior. E.g. "A shared provider-webhook signature-verification middleware
for ProviderFacing routes, parameterized by scheme.">

## 2. Evidence it is baseline, not domain

<The rule of two, made concrete: where does this logic exist or is it designed to exist, per consumer, with
file:line or arch-doc § citations? If only one consumer needs it today, why is it still platform-shaped
(security-sensitive, contract-adjacent, predicted by a designed service)? Check first that the framework/kit
docs have not already RULED it service-local (e.g. the two Redis shapes) — if they have, present the new
evidence that reopens the question, or do not file.>

## 3. Proposed kit contract

<Public API sketch (Go signatures / middleware shape / DDL / env keys with defaults / metric names following
kit naming rules / error codes). What contracttest should assert. What stays configurable per service vs fixed
by contract.>

## 4. What each consumer deletes or stops writing

<Per consumer: the local code this retires (file paths for existing code, arch-doc § for designed code). This is
the payoff line the kit owner weighs the maintenance cost against.>

## 5. Migration and compatibility

<How existing local implementations converge onto the kit version: additive adoption, expand-contract for any
DDL, deprecation window if replacing something. Idempotency / security / observability notes.>

## 6. Alternatives

<Stay-local-forever, wrap-per-service, a third design. Why the kit should own it anyway — or the honest case
that it shouldn't, if you're filing to get a recorded negative decision.>

<!-- Kit owner appends "## Kit decision — YYYY-MM-DD" here after intake. -->
