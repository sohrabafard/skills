# Retries

Read when a retry is added, removed, or found nested inside another retry. `SKILL.md` holds the three rules that bind without reading this file: a retry is legal only when repeating the call cannot produce a second effect, exactly one layer in a chain retries a given logical call, and every backoff is exponential with full jitter. This file is the classification, the arithmetic, and the audit. The Ala attempt count, backoff base, and cap are in `/alaa-services-contract` (`$alaa-services-contract` in Codex) `references/22-failure-load-and-deprecation-contract.md`.

## The four preconditions, checked in this order

A retry is written only when all four hold. Check them in order, because each is cheaper to evaluate than the next and the first failure ends the question.

1. **The outcome is in a retryable class.** See the table below. A retry of a non-retryable outcome is a second identical failure plus its latency.
2. **The remaining deadline covers another attempt and its wait.** If it does not, the correct behaviour is to stop now rather than to attempt and be cut off. `10-deadlines-and-timeouts.md` owns this bound.
3. **Repeating the effect is safe** — the operation is naturally idempotent, or it carries an idempotency key the receiver honours. `60-idempotency.md` owns what "honours" means, and a route with no idempotency guarantee is retried zero times, not once.
4. **This is the layer that owns the retry**, and every layer below has its retry count explicitly at zero.

A retry written without step 3 is not a reliability mechanism. It is a duplicate generator that fires precisely during incidents, which is when duplicates are hardest to detect and most expensive to reconcile.

## Which outcomes are retryable

The classification turns on one question: **does this outcome prove the request did not take effect?**

| Outcome | Retryable | Why |
|---|---|---|
| DNS failure, TCP connect refused, connect timeout, TLS handshake failure | Yes, without an idempotency key | The request was never delivered, so a second attempt cannot duplicate anything |
| Connection reset before the request was fully written | Yes, without a key | The server cannot have processed a request it did not receive in full |
| Read or total timeout after the request was sent | Only with an idempotency key | The server may have completed the work and lost the response |
| Connection reset after the request was written | Only with a key | Same: no information about what executed |
| `502`, `503`, `504` from a proxy or gateway | Only with a key, unless the operation is naturally idempotent | The request may have reached the origin |
| `429` or `503` carrying a retry hint | Yes, after waiting exactly the hint | The server has stated when it will accept work; guessing shorter is the amplification the hint exists to prevent |
| Any other `4xx` | No | The request is wrong, and an identical request will be wrong again. Retrying it converts a client defect into load |
| `501`, `505`, and other permanent server refusals | No | The condition is a property of the request or the deployment, not of this moment |
| An application-level failure inside a `200` | No, unless the payload names the failure as transient | A retry decision made from a status code alone is wrong on any API that reports failure in the body |
| A broker publish nack or a closed channel | Yes, with a key or from a durable outbox row | The message was not accepted, and the outbox makes the repeat safe |

**A connect refusal and a timeout are not the same event and must not share a code path.** A refusal is a proof of non-execution: retrying it duplicates nothing, so it is retryable on any operation, including one with no idempotency key. A timeout is the absence of information: the server may have committed the write and failed to answer, so retrying it without a key is a coin flip on duplication. Code that catches a generic transport exception and retries has lost the distinction, and the observable consequence is duplicates that appear only when the dependency is slow.

## The backoff curve

Full jitter is `sleep = uniform(0, min(base * 2^(attempt - 1), cap))`. Three properties matter and all three come from the shape rather than from the numbers:

- **The exponent** gives a failing dependency geometrically more room with each attempt, so a caller that cannot succeed stops contributing load quickly.
- **The cap** keeps the last wait inside a human's and a caller's patience. Without it the third or fourth wait exceeds any request deadline, so the retry is cut off and the exponent bought nothing.
- **The uniform draw from zero** decorrelates callers. This is the property that is not optional: N callers failing on the same dependency at the same instant, waiting the same computed delay, retry in the same instant. The dependency then receives its entire failed load again as a spike, at the exact moment it is trying to recover, which reproduces the failure and produces a standing oscillation that reads in dashboards as flapping. Adding a small random percentage to a fixed delay does not fix this, because the arrivals stay clustered; the draw must span the whole window.

Two shapes to reject on sight: a fixed delay, which synchronises every caller by construction, and a zero or immediate first retry, which sends the second attempt while the condition that failed the first is still true.

**Retry the same logical call, not the same request object.** Regenerate whatever must be fresh — the deadline-derived per-attempt timeout, the trace span — and preserve byte-for-byte whatever must be stable, above all the idempotency key. A new key per attempt is a new operation, not a retry.

## Retry budgets, not attempt counts

An attempt count bounds one call. It does not bound the fleet, and the fleet is what breaks a dependency.

The arithmetic: with two retries permitted per call, a dependency failing every request receives three times its normal load — during its own outage. Whatever capacity it needed to recover, the callers just spent. This is why a per-call count is a necessary bound and never a sufficient one.

A retry budget bounds retries as **a fraction of successful requests over a rolling window**, measured per client instance per dependency. Below the fraction, retries proceed. Above it, retries stop entirely and the first failure is returned to the caller, even though attempts remain in the per-call count. The question the fraction answers is "how much extra load may we add to a dependency that is already failing?" — and the answer is small, because the extra load is only useful for the failures that are genuinely transient, and a dependency failing more than a few percent of requests is not having transient failures.

Two properties make the budget work: it is measured against **successes**, so a fully failing dependency drives the allowance to zero rather than to a constant fraction of a growing failure count; and it is **per dependency**, so one broken dependency does not spend the allowance that another one's transient blips need.

The budget also gives an operator one number to read during an incident: retries as a share of traffic. A dependency whose retry share is at the ceiling is being amplified by its callers, and the mitigation is to lower the callers' budget, not to add capacity.

## Amplification across layers

Retries multiply. Three layers each attempting three times sends up to twenty-seven requests for one logical call, and each layer's operator sees a compliant retry policy in their own code.

Where the layers hide, in the order they are usually missed:

1. The client library's own default, which is frequently nonzero and undocumented at the call site.
2. A service mesh, sidecar, or proxy retry policy.
3. The application's explicit retry.
4. The caller's retry, one service up.
5. A queue consumer redelivering after a failure, which is a retry of the whole handler including its outbound calls.
6. A human or a UI pressing the button again, which is the layer with no budget at all and the reason idempotency keys exist.

The audit is mechanical and belongs in a test rather than in a code reading: **count the requests that arrive at a stubbed dependency for one logical caller call.** More than the owning layer's budget means a layer you did not know about is retrying. `80-verification.md` owns the test.

The owning layer is the one that holds the idempotency key and the deadline, because it is the only layer that can decide whether a repeat is safe and whether time remains. That is normally the application call site, not the library and not the proxy.

## How retries compose with the other mechanisms

- **Breaker first.** A retry inside an open circuit is not a retry; the breaker's whole purpose is that the call is not attempted. Check the breaker, then retry inside the closed state, and count every attempt — not every logical call — toward the breaker's failure rate, so a retrying caller trips the breaker sooner rather than later. `30-breakers-and-bulkheads.md` owns the states.
- **Bulkhead per attempt.** Each attempt takes a slot. A retry loop that holds one slot across all attempts and their waits occupies the isolation budget while doing nothing.
- **Deadline over count**, always, per `10-deadlines-and-timeouts.md`.
- **Signal per attempt and per exhaustion.** A failed attempt and an exhausted budget are different events, and only the second one is a request-level failure. Collapsing them makes retry amplification invisible. `/alaa-observability-soc` (`$alaa-observability-soc`) owns the signal shape; `/alaa-services-contract` (`$alaa-services-contract`) owns the event and code names.

## Hedged requests are not retries, and need their own permission

A hedge sends a second attempt before the first has failed, to cut tail latency. It duplicates by design, so it is permitted only on an operation that is naturally idempotent and read-only, only above a latency threshold derived from the healthy p99 rather than on every call, and only under a budget of the same shape as the retry budget. The first response wins and the loser is cancelled. On a write path, a hedge is a duplicate generator with a latency justification, and is never used.
