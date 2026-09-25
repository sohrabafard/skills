# Deadlines And Timeouts

Read when a deadline, timeout, cancellation path, per-hop budget, or durable acceptance is added or changed. `SKILL.md` requires bounded calls; this file owns their execution context and the durable-work lifecycle. The Ala values are in `/alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md`.

## Decide which lifetime is bounded

**Persisted ownership, not receipt delivery, separates request-bound work from accepted work.** Identify the committed job, outbox row, or equivalent durable record that makes the service responsible. An application acceptance receipt reports that fact; it does not create it. Return acceptance only after persistence is known. If commit or receipt delivery is uncertain, reconcile by the same logical identity and idempotency key under `60-idempotency.md`; a timeout proves neither nonacceptance nor absence of an effect.

| Bound | Governs | Does not establish |
|---|---|---|
| Synchronous request deadline | How long the caller waits and request-bound work may continue | The lifetime of work already durably accepted |
| Processing-attempt timeout | One worker attempt and its resource use | Whole-job invalidity or rollback of an unknown effect |
| Business validity and cancellation | Whether accepted work may execute, as defined by its business owner | A universal expiry inferred from the HTTP deadline |
| Broker message TTL and queue expiry | Message residence and unused-queue lifetime respectively | Business disposition or retention obligations |
| Record retention | How long job, outbox, receipt, and deduplication evidence remains available under its owning contract | Permission to execute after business validity ends |

**After durable acceptance, caller timeout, disconnect, or a lost receipt cannot cancel or discard the job.** Carry correlation and stable identity into a separately bounded worker execution context, not the originating request's cancellation or expired deadline. This is no extension of the synchronous wait: that wait still ends on time.

For accepted work, require the business owner's explicit validity, cancellation, retry-exhaustion, terminal/reconciliation, and retention contract. Check validity and cancellation before execution or retry. An attempt timeout ends that attempt; further processing depends on that contract, with bounded attempts, backoff, retry budget, and concurrency. Expiry or cancellation takes the observable owner-defined disposition, with reconciliation for committed or uncertain effects; it promises no rollback.

**If a required lifecycle decision is missing, report the missing owner decision and block that design choice.** Do not infer deletion, indefinite execution, infinite retry, unlimited retention, or eventual success. Existing bounds remain binding while the gap is unresolved. A documented kit limitation is a gap to escalate through its owner, not proof that the bound exists.

Publisher confirms cover publishing to the broker; consumer acknowledgements cover deliveries to a consumer. Neither is an application acceptance receipt or a guarantee of business success. Broker mechanics, retry-queue TTL, acknowledgement ordering, and DLQ/replay stay with `/alaa-async-messaging`; idempotency retention stays with `60-idempotency.md` and its platform values owner. Broker distinctions verified 2026-09-26 against [RabbitMQ TTL](https://www.rabbitmq.com/docs/ttl) and [acknowledgements and confirms](https://www.rabbitmq.com/docs/confirms).

## Why a propagated deadline outranks per-call timeouts

For request-bound work, a per-call timeout answers "how long will I wait for this hop?" A deadline answers "when does this request stop being worth serving?" Only the second question has an answer the user cares about, and only the second one composes.

Three failures a set of per-call timeouts cannot prevent, and a deadline does:

1. **Summation.** Four sequential hops at two seconds each are all compliant and the request takes eight. No hop is at fault, and no hop can detect the problem, because a hop does not know what came before it.
2. **Dead work.** A caller that has already given up leaves the callee working. With per-call timeouts the callee cannot know, so it spends a pool slot, a worker, and a database transaction producing a result that will be discarded. Under a shared dependency this is how one impatient caller's traffic becomes every caller's saturation.
3. **Retry blindness.** A retry decision needs to know whether another attempt can finish in time. Without a deadline it can only count attempts, so it retries into a window that has already closed.

The deadline is therefore request-scoped state, set once at ingress from the route's target, carried in the same context that carries the request and trace identity, and read by every call site as `remaining`. A service that recomputes a deadline per hop has per-call timeouts with extra steps.

**A deadline arriving from an upstream caller is honoured, and never extended.** Take the smaller of the caller's remaining budget and this service's own route budget. Extending a caller's deadline means doing work whose result the caller has already stopped waiting for, which is the dead-work failure with a service boundary in front of it.

## Deriving a per-hop budget from an end-to-end target

Start from the target the user or the SLO states, then subtract before dividing.

1. **Subtract the service's own cost:** ingress middleware, deserialization, validation, serialization, and the response write. What remains is the dependency budget.
2. **Divide by the critical path, not by the dependency count.** Sequential hops share the budget; parallel hops each get the whole remaining budget, because they finish together. A request with one chain of three hops and a fan-out of six divides by three, not by nine. Getting this backwards produces timeouts so tight that a healthy fan-out fails.
3. **Reserve a tail for the failure response.** A request that spends its entire budget on the attempt has nothing left to produce an error body, emit its signals, and release its resources. Leave the remainder for that, or the timeout path itself times out.
4. **Check the derivation against the dependency's observed healthy p99.** A hop whose derived budget is below its healthy p99 will fail routinely, and the correct response is to change the design — remove the hop from the critical path, parallelise it, make it optional, or move the work behind an accepted-and-queued response. Raising the end-to-end target to fit a serial chain is the last option, not the first, because it is the user's latency being spent.
5. **A retried hop's budget covers its attempts and its waits, not one attempt.** Sizing a hop's budget for a single attempt and then retrying inside it guarantees the retry is cut off, which reads in production as "the retry never helps."

Record the derivation next to the value: the target, what was subtracted, the chain length, and the observation the p99 came from. The next person to change a hop needs to know which number moves.

## What a timeout must do to the in-flight work

On expiry of the applicable request or processing-attempt deadline:

- **Promptly signal cancellation to the callee** by the mechanism the transport supports — closing the connection, cancelling the RPC, cancelling the driver's query — and verify it stops cancellable work. Unstopped work still holds resources; a signal alone proves neither remote termination nor rollback.
- **Release the caller's own resources** on the path out: the pool slot, the semaphore slot, the buffer. Releasing them in the success path only is the leak that turns a dependency's slow hour into the caller's exhausted pool.
- **Reconcile partial or uncertain effects by stable identity.** Roll back when that is provable; otherwise use the operation's completion or disposition contract. A timeout in a multi-step write with no reconciliation path creates debt; it is never proof that nothing committed.
- **Report which bound expired** — connect, read, or total — because the three imply different causes and different retry legality.

A timeout that only stops waiting leaves attempt resource use unbounded. Apply the durable-work lifecycle above before deciding the job's fate; terminating an attempt is not cancelling accepted ownership.

## Never set a timeout longer than the remaining budget

Every call site takes the smaller of its configured timeout and `remaining` in the applicable execution context above. When `remaining` will not cover the next attempt, the call is not made: a waiting request fails immediately with its dependency-unavailable outcome; accepted work follows its bounded retry or disposition contract. An attempt outside its budget consumes capacity without a usable result.

This is also the stop condition that outranks the retry count. Attempts remaining in the budget do not authorise an attempt the deadline cannot cover.

## Connect, read, and total are three different bounds

Each answers a different question, and any one alone leaves a real failure unbounded.

| Bound | Bounds | Left unbounded without it |
|---|---|---|
| Connect | Establishing the transport: DNS, TCP, TLS | A black-holed destination or a full accept queue, where packets vanish and nothing ever answers |
| Read | The gap between bytes, or the wait for the first byte | A connection that opens and then goes silent |
| Total | The whole attempt, from initiation to the last byte | A response that trickles — each byte inside the read timeout, the response never finishing |

The trickle case is why a read timeout is not sufficient: a read timeout resets on every byte, so a callee sending one byte a second inside a one-second read timeout runs forever. Total is the bound the deadline actually maps onto.

Connect deserves its own value for a second reason: **a connect failure is proof the request never executed, and a read or total timeout is only the absence of information.** That difference decides retry legality, and it is lost if the code cannot tell the two apart. `20-retries.md` owns the consequence.

Two more bounds are timeouts in everything but name, and an unbounded version of either converts a slow dependency into an exhausted service: the wait to acquire a pooled connection, and the wait to acquire a bulkhead or semaphore slot. Bound both, and treat their expiry as the same dependency-unavailable outcome. `30-breakers-and-bulkheads.md` owns the sizing.

## The database and the cache are dependencies

Both are hops with a network between them and the caller, and both are routinely left unbounded because the client library defaults to no timeout or to one measured in minutes.

- Set a statement or query timeout on the driver from the applicable request or processing-attempt deadline rather than a global default. An abandoned query still holds its locks until the server stops it.
- Give a cache client a timeout tighter than the origin it fronts. A cache slower than the thing it caches is a pure loss, and the request proceeds to the origin rather than wait.
- A lock, an advisory lock, or a lease is acquired with a timeout and held with an expiry. An unbounded acquire is a queue with no depth limit; a lock with no expiry survives the process that took it.
