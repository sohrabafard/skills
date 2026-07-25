# Backpressure, Admission Control, And Load Shedding

Read when a route saturates, a queue grows, an in-flight limit is chosen, or a rate limit and a concurrency limit are being confused for each other. `SKILL.md` holds the binding rules: every queue is bounded in depth and in wait, synchronous product traffic sheds while work that must survive is accepted and queued, and health, readiness, and liveness are never shed. This file is the decision procedure, the arithmetic behind it, and the ordering. `/alaa-services-contract` (`$alaa-services-contract` in Codex) `references/22-failure-load-and-deprecation-contract.md` states this platform's instance of these rules with its in-flight defaults, status codes, and event names.

## The decision: shed or queue

Two questions decide it, in this order.

1. **Is someone waiting for this right now?** A caller holding an open connection with a deadline is waiting. A caller that already received an acknowledgement is not.
2. **Does losing this work have a cost the system cannot recover?** A read, a search, a page render can be re-requested. An accepted payment, an audit record, a state transition cannot.

- Waiting, recoverable → **shed**. Reject now, cheaply, with a signal the client can act on. The caller learns immediately and can retry or degrade.
- Not waiting, unrecoverable → **queue**, durably, with a bounded depth and an owner.
- Waiting **and** unrecoverable → **change the interface, not the limit.** Accept the work, persist it, return a receipt, and complete it asynchronously. This is the only correct answer, and the failure mode of getting it wrong is a request that waits for capacity while holding a resource — which is the queue-at-ingress failure below.
- Neither waiting nor unrecoverable → drop it and count the drop. Prefetches, speculative work, and telemetry batches live here.

The reason shedding beats queueing for a waiting caller: **a queue does not add capacity, it converts rejection into latency.** The caller's deadline does not move because work was queued, so a queued request either completes in time — meaning there was capacity and the queue was unnecessary — or completes after the caller has left, meaning the capacity was spent producing a result nobody reads. Shedding gives the caller the one piece of information it can act on: not now.

## Why an unbounded queue is a latency bomb

The arithmetic is not subtle. Wait time is depth divided by service rate. While arrivals exceed the service rate, depth grows monotonically, so **every item's wait grows without bound** — and the system reports success on all of them, after the deadline, forever. It looks healthy on error rate and is completely broken.

Worse than the latency: the capacity is spent twice. The queued item is processed, its result discarded because the caller is gone, and the caller's retry is processed too. An overloaded system with an unbounded queue therefore gets *further* behind under retry pressure, which is why this failure does not self-correct.

Bounding the depth is only half. The other half is **checking the deadline at dequeue, not only at enqueue**: an item whose caller has already gone is dropped before it is processed, not after. Doing the work first and discovering the caller left afterwards is the exact waste the bound was meant to prevent.

A bounded queue that is persistently full is not a tuning problem. It is the signal that arrival rate exceeds service rate, and the answers are more capacity, less work per item, or shedding earlier — never a larger bound.

## Choosing what to shed first

Shed in decreasing order of cheapness and increasing order of value to the caller's outcome. The order below is the default, and a route may only move within it for a recorded reason.

1. **Work whose deadline has already expired.** Free to shed, since it cannot produce a usable result. Sheddable at any queue or admission point.
2. **Retries before first attempts.** A retry's originator has already been served an answer or has already failed; a first attempt's originator has received nothing. Shedding retries preferentially also directly counters the amplification in `20-retries.md`, and it needs the request to be identifiable as a retry — which is one more reason a retry carries the same idempotency key.
3. **Declared low-criticality classes**: background, batch, prefetch, warm-up, analytics, and anything a human is not watching. This requires the classes to be declared per route **before** overload, because during overload every route's owner believes theirs is critical.
4. **Within one class, newest first.** Under sustained overload the oldest queued item has the highest chance of a caller that has already left, so serving newest-first completes more useful requests than first-in-first-out does. This applies only to a queue in overload; a queue operating normally serves in order, because newest-first starves the oldest item indefinitely and that is only acceptable when the alternative is serving nobody in time.

A route that declares no class is treated as the default interactive class. That way an operator who never classifies gets uniform shedding rather than an accidental priority order that nobody chose.

Shedding must be **cheap and early**: at admission, before the request has acquired a pooled connection, deserialized a large body, or taken a bulkhead slot. A shed decision made after the expensive part has run has already spent the capacity it was protecting.

Tell the client the truth: a distinct rejection status with a retry hint, and a distinct event, so a shed is never confused with a dependency failure or an application error in a dashboard. `/alaa-services-contract` (`$alaa-services-contract`) owns the code and event names; `/alaa-observability-soc` (`$alaa-observability-soc`) owns their requirement level.

## Health, readiness, and liveness

These endpoints are exempt from shedding, and the exemption has a mechanical consequence beyond "do not shed them": **their handlers must not contend for the resource the product path is saturating.** A readiness handler that waits for a pooled connection is shed by resource exhaustion whether or not the admission limiter spared it.

The failure this prevents, in sequence: an overloaded instance fails or delays its readiness probe, the orchestrator removes it from rotation, the same total load lands on fewer instances, they saturate faster, and the deployment enters a restart loop. Overload has become an outage, and every instance is now failing a probe it could have answered.

Concretely: probe handlers run outside the product concurrency limiter and outside the product connection pool; a readiness check that must consult a dependency uses its own bounded, short-timeout path; and readiness reports the instance's ability to accept new work, not the health of every dependency it might use. `/alaa-services-contract` (`$alaa-services-contract`) owns the endpoint shapes and which dependencies appear in them.

## Concurrency limit versus rate limit

They bound different quantities, and using one for the other's job is a common and expensive substitution.

| | Concurrency limit | Rate limit |
|---|---|---|
| Bounds | Simultaneous in-flight work | Arrivals per unit time |
| Bounds resource use | Yes — in-flight work is what holds memory, slots, and connections | No |
| Reacts to latency | Yes, automatically: as the system slows, the same limit admits fewer per second | No: when latency triples, the same rate triples in-flight work |
| Needs tuning when capacity changes | Rarely — it is expressed in the unit that actually runs out | Every time throughput changes |
| Right for | Protecting a resource: a pool, a worker set, a dependency | Enforcing a contract: a quota, a per-tenant fair share, abuse control, a paid tier |

**Protect a resource with a concurrency limit. Enforce a contract with a rate limit.** Most services need both, at different places: a per-tenant rate limit at the edge for fairness and abuse, and per-instance concurrency limits — global for admission, per dependency for isolation — for protection.

The self-adjusting property is the reason the concurrency limit is the primary protection: it is the only one of the two that tightens automatically when the system gets slower, which is precisely when it needs to.

Adaptive concurrency limits, which infer the limit from observed latency and throughput rather than from a constant, are the right default where the platform's library supports them, because the correct constant changes with every deploy and every dependency's capacity change. A static limit is acceptable and is set from the worker count, since admitting more concurrent requests than there are workers to serve them creates a queue whether or not one was declared.

## Backpressure is propagation, not buffering

Backpressure means the limit reaches the producer, so the producer slows down. Buffering means the limit is hidden from the producer, so it does not.

Applied by direction of control:

- **A synchronous caller** is given the rejection. Its retry budget and its breaker then reduce its send rate. That is the whole mechanism, and it works only if the rejection is fast and distinguishable.
- **A streaming or long-lived connection** stops reading from the socket, so the transport's own flow control stalls the sender. Reading into an application buffer to "keep the connection healthy" moves an unbounded queue inside the process.
- **A queue consumer** lowers its prefetch or stops acknowledging, so the broker stops delivering. Increasing prefetch to "keep the consumer busy" moves the broker's bounded queue into the consumer's memory, where it has no bound and no durability. `/alaa-async-messaging` (`$alaa-async-messaging`) and `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`) own prefetch, acknowledgement, and dead-letter mechanics.
- **A producer that cannot be slowed** — a third-party webhook, a fixed-rate sensor feed — is admitted to a durable bounded buffer and shed at the buffer's edge, and the shed is a recorded event rather than a silent overwrite. There is no configuration that makes an unslowable producer safe without a bound.

An in-process channel or buffer between stages of one service is a queue and takes the same two bounds, depth and wait. Unbounded internal channels are where a bounded ingress limit leaks: the request is admitted, hands work to an unbounded internal stage, and the memory the admission limit was protecting is consumed anyway.
