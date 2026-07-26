# The event seam — where a domain event is emitted, and what carries it

This skill owns two decisions and no others: **which layer emits a domain event**, and **at which moment relative to the transaction**. Delivery semantics, broker topology, retry and DLQ mechanics belong to `/alaa-async-messaging` (`$alaa-async-messaging`); retry and idempotency doctrine to `/alaa-reliability-sla` (`$alaa-reliability-sla`), with every value in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; event and code names to `/alaa-services-contract` (`$alaa-services-contract`).

## The emission point

**A domain event is emitted from a Service.** The Service is where the invariant was enforced and the authorization decision was made, so it is the only layer that knows the event is true. A Controller that emits has published a fact before any invariant checked it; a Repository that emits publishes on a write that a Service may still roll back.

**A domain event is emitted after the transaction that made it true commits.** An event emitted inside the transaction is observable to a consumer that then reads a row the transaction has not committed — or, when the transaction rolls back, describes something that never happened. This ordering defect does not reproduce under low load and does not appear in any single-file review; it appears as a consumer reading a row that does not exist yet.

The two mechanisms that satisfy this, and no third:

- The event row is written **inside** the business transaction and published **after** commit by a separate reader — the outbox below.
- The dispatch is deferred to after commit by the framework's commit-aware behaviour, when the event needs no durability. That mechanism, and the connection setting behind it, are `/alaa-async-messaging`'s (`$alaa-async-messaging`) — `references/queues-best-practices.md`.

Emitting with neither is an ordering defect, not a style choice.

## Listeners

- A listener performs the side effect; the Service performs the domain change.
- **A listener that performs network or filesystem I/O implements `ShouldQueue`.** A synchronous listener may not make an HTTP call, publish to a broker, or write a file, because it runs inside the request: its latency lands on the caller's deadline and its failure fails a request whose domain change already succeeded. Deadline values are in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
- The listener's name states the side effect, so a reader of the provider's event map can see what a change triggers without opening each class.

## The outbox

**When a domain event must reach a consumer at least once, it is written to a durable outbox row in the same database transaction as the business change, and a separate worker publishes from that row.** This is not conditional on an outbox already existing in the repository. A change that introduces such an event either introduces the outbox, or the route is documented as not durable and the event is declared best-effort — those are the only two outcomes, and choosing silently produces the first while delivering the second.

What this skill fixes about it:

- **The Service writes the row**, in its own transaction, next to the business change. A listener that writes the row outside that transaction has reintroduced the ordering defect above.
- **The publisher is safe under concurrent workers.** Rows are claimed inside a transaction with a row-level lock that skips already-locked rows (`SELECT … FOR UPDATE SKIP LOCKED`). A claim built as `SELECT` followed by `UPDATE … WHERE status = pending`, without the lock, publishes the same row from two workers under concurrency. Isolation and lock semantics are `/alaa-data-layer`'s (`$alaa-data-layer`).
- **The row outlives the publish attempt.** It is not deleted before the broker acknowledges.

Not owned here, and not restated here: the state set and its transitions, the retry policy and its backoff, the idempotency key's construction, and the dead-letter path. `/alaa-async-messaging` owns the mechanics, `/alaa-reliability-sla` the doctrine, and the contract file above every number. Observability of the transitions is `references/60-telemetry-surfaces.md`; what a stuck row means and the smallest safe action is `references/50-failure-recovery.md`.

For what the caller sees when the broker is unreachable, read `references/40-degraded-mode.md`.

## Observers, and realtime

- An Observer reacts to a model change and may emit an event for a mechanical consequence. A user-initiated action's event comes from the Service, so that one action does not produce two events from two layers.
- Broadcasting is a driver behind a stable interface. No domain class names a driver, so removing or swapping the transport touches one binding.

## Authorization denials

A denial is a signal, not a domain event, and its surface is defined in `references/60-telemetry-surfaces.md`.
