# Failure And Load As Design Inputs

`SKILL.md` owns one rule: every dependency is classified during design, and a design with an unclassified
dependency is unfinished. This file says how to derive the dependency list so it is not derived from
memory, what each row carries, and what load figures the design states. Read it during step 5.

Doctrine is not here. `/alaa-reliability-sla` (`$alaa-reliability-sla`) owns the gate-versus-contributor
discrimination rule, deadlines, retries, backoff, breakers, bulkheads, admission and shedding, degradation,
idempotency, error budgets, and the evidence each mechanism demands. `/alaa-services-contract`
(`$alaa-services-contract`) `references/22-failure-load-and-deprecation-contract.md` owns the Ala values.
This file states no number and no doctrine, so nothing here can drift out of agreement with either.

## Derive the dependency list

Do not write the list from memory; derive it, so that two agents designing the same subsystem produce the
same rows:

1. every outbound interface enumerated in step 3 — synchronous calls, events emitted, jobs enqueued;
2. every component that owns a datum this design reads, from the ownership table in step 4;
3. every store the design writes to or reads from, including caches and search indexes;
4. every broker, queue, or topic on a path;
5. every external provider;
6. every platform component the request already traverses — gateway, auth, authorization, and any sidecar —
   which are dependencies of this design even though this design did not add them, because their failure
   reaches this design's journeys.

The sixth source is the one an agent working from its own plan will miss, and it is where the fleet's
shared failure modes live.

## What each row carries

| Column | Content | Why the row is unreviewable without it |
|---|---|---|
| Dependency | The component, store, broker, or provider | — |
| Classification | Gate, required contributor, or optional contributor, per `/alaa-reliability-sla` | A reviewer cannot tell whether its failure is an outage or a degradation |
| Caller-visible failure | What the caller of this subsystem sees when it fails, in the vocabulary of the error surface from step 3 | The failure is otherwise mapped by whichever exception escapes first |
| Assumed load | The request rate and the concurrency this design assumes it will send | Nothing can size a pool, a cap, or a quota |
| Source of bounds | The contract value cited, or the derivation recorded per `/alaa-reliability-sla` | A value with no source is re-tuned by guess at the next incident |

An unclassified row blocks the design. When the classification cannot be made from the code and the
repository's documentation, that is a blocked stop and it belongs to `/alaa-reliability-sla`, which owns
what to do when a dependency cannot be classified.

## State the load the design assumes

Three figures, per entry point, and each is an input the design is built against rather than a check
performed afterwards:

1. **Assumed peak** — the request rate and concurrency at the busiest realistic minute, with where the
   figure came from: a measurement, a projection from a business input, or an assumption marked as one.
2. **Growth horizon** — the multiple of that peak the design must survive without a redesign, and over what
   period. A design with no horizon is implicitly designed for today's traffic.
3. **The first resource to saturate** at the assumed peak times the horizon — a connection pool, a single
   partition, a lock, a single-threaded consumer, an external quota, a disk.

**The design names the resource that saturates first, because a design that names none has not been
examined under load**, and the first one found in production is found by an incident rather than by a
reviewer. Naming it also tells the implementation lane which number to measure.

A figure marked as an assumption is legitimate and a missing figure is not. An assumption can be checked
against production later; silence cannot.

## New failure modes need signals

Every failure mode this design introduces names the signal that will make it diagnosable in production
without a code change. Name the failure mode and the question an operator will ask; the signal's design,
its requirement level, its cardinality budget, and its alert belong to `/alaa-observability-soc`
(`$alaa-observability-soc`). A failure mode with no named signal is a failure mode whose first diagnosis is
a code deploy.

## Anti-patterns

- a dependency table written after implementation, when every call site has already chosen its own
  behaviour and the table merely records what was done;
- "we will add retries and timeouts" recorded as the failure design, which names no dependency, no
  classification, and no caller-visible outcome;
- classifying a dependency by how important it feels rather than by what its failure lets through — the
  discrimination rule is `/alaa-reliability-sla`'s and it is about consequence, not importance;
- a load figure copied from another service because the two look similar;
- an assumed peak stated with no growth horizon, which designs for the day the design was written;
- restating a timeout or pool value from the platform contract into the record, which creates a second copy
  that drifts the next time the contract changes.
