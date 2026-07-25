# Deadlines And Timeouts

Read when a deadline, a timeout, a cancellation path, or a per-hop budget is added or changed. The rule that every request carries one ingress deadline, that every outbound call is explicitly bounded, and that a timeout cancels the work it abandons is in `SKILL.md`; this file is how to derive, propagate, and shape those bounds. The Ala values are in `/alaa-services-contract` (`$alaa-services-contract` in Codex) `references/22-failure-load-and-deprecation-contract.md`.

## Why a propagated deadline outranks per-call timeouts

A per-call timeout answers "how long will I wait for this hop?" A deadline answers "when does this request stop being worth serving?" Only the second question has an answer the user cares about, and only the second one composes.

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

Expiry is a cancellation, not just a return. On expiry:

- **Propagate the cancellation to the callee** by the mechanism the transport has — closing the connection, cancelling the RPC, cancelling the driver's query. A callee that keeps working holds the resource the timeout existed to free.
- **Release the caller's own resources** on the path out: the pool slot, the semaphore slot, the buffer. Releasing them in the success path only is the leak that turns a dependency's slow hour into the caller's exhausted pool.
- **Leave no partial effect** behind, or leave one that a later attempt can complete or discard by its key. A timeout in the middle of a multi-step write with no completion path is where reconciliation debt is created.
- **Report which bound expired** — connect, read, or total — because the three imply different causes and different retry legality.

A timeout whose only effect is that the caller stops waiting has not bounded anything except the caller's patience.

## Never set a timeout longer than the remaining budget

Every call site takes the smaller of its own configured timeout and `remaining`. When `remaining` will not cover the next attempt, the call is not made at all: the caller fails immediately with its dependency-unavailable outcome. Attempting it is strictly worse than not attempting it — it cannot produce a usable result, and it consumes the dependency's capacity during whatever incident caused the delay.

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

- Set a statement or query timeout on the driver, and set it from the request deadline rather than from a global default. A query the caller has abandoned still holds its locks until the server stops it.
- Give a cache client a timeout tighter than the origin it fronts. A cache slower than the thing it caches is a pure loss, and the request proceeds to the origin rather than wait.
- A lock, an advisory lock, or a lease is acquired with a timeout and held with an expiry. An unbounded acquire is a queue with no depth limit; a lock with no expiry survives the process that took it.
