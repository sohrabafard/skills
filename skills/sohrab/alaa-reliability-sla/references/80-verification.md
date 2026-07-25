# Verification

Read before calling any mechanism in this skill done, and when a review must decide what evidence to accept. `SKILL.md` holds the binding rule: every mechanism has one test that fails when the mechanism is removed, and a mechanism never observed to fire is a hypothesis.

## What counts as evidence

Evidence is an **observed** outcome: a test that ran, an injection that ran, or a production incident whose signal was captured. Three things are not evidence, and each is accepted routinely:

- **The code.** A retry block, a breaker construction, or a timeout constant is a claim about behaviour. Configuration frequently does not reach the client it was written for, a library default silently overrides it, and a wrapper swallows the cancellation.
- **The configuration value.** A timeout in a config file proves the file contains a number.
- **A passing test that also passes without the mechanism.** A test that passes either way is measuring something else, and its green result is worse than no test because it is used as evidence. Proof by removal — the procedure that settles it — and the six levels a result may be reported at are owned by `/alaa-testing-strategy` (`$alaa-testing-strategy` in Codex); read it before accepting any row of the table below as verified, and report each observation at the level actually reached rather than the level it was meant to reach.

State the evidence as "this was injected, this was asserted, this was observed" — the three together. A review accepts nothing that omits the third.

## Inject at the boundary the mechanism guards

Fault injection goes at the caller's edge of the dependency — a stub, a fake, or a proxy the caller talks to — not inside the dependency's own implementation. The mechanism under test is the caller's, so the test must be able to produce failures the real dependency will not produce on demand, and must not require the real dependency at all.

The failure modes to inject, ordered by how often they are missed:

1. **Slow but succeeding.** The mode that exhausts pools and never trips a failure-rate breaker. Almost always missing from a test suite.
2. **Slow on the tail only** — the p99 is out of budget while the median is fine. This is what production actually does.
3. **Accepts the connection, then sends nothing.** Bounds the read timeout; a connection-refusal stub does not.
4. **Trickles the response** — bytes inside the read timeout, forever. The only way to prove a total timeout exists.
5. **Fails, then recovers.** Exercises the breaker's reset and half-open path, which is otherwise never executed.
6. **Succeeds, then fails mid-response**, after headers.
7. **Two identical requests arriving concurrently.** The idempotency case in `60-idempotency.md` section 6, and the case a sequential test cannot reach.
8. **Refuses the connection** and **resolves to nothing**. The cheapest modes, and usually the only ones present.

A suite that injects only mode 8 has tested error handling, not reliability.

## Evidence table, per mechanism

| Mechanism | Inject | Assert |
|---|---|---|
| Deadline propagation | A dependency that sleeps past the route budget | The request returns the dependency-unavailable outcome before its own deadline; the downstream call carried a timeout no larger than the remaining budget; no partial effect remains |
| Timeout cancels work | The same, with a stub that records cancellation | The stub observed a cancellation; the pool and semaphore gauges return to baseline; no work completed server-side after the caller gave up |
| Three distinct bounds | Modes 3 and 4 above | The connect, read, and total bounds each trip on their own mode, and the reported reason names which one |
| Retry legality | A stub failing the first attempts, then succeeding | Exactly one logical effect exists; the attempt count is within budget; the observed waits are **distributed rather than equal**, which is how a missing jitter is detected |
| One retrying layer | One logical caller call | The request count arriving at the stub is at most the owning layer's budget. A higher count is a nested retry, and this test is the only reliable way to find one |
| Non-retryable outcomes | A stub returning a client-error class | Zero retries were attempted |
| Retry budget | Sustained failures from one dependency | Retries stop while per-call attempts remain, and the retry share of traffic stays at or below the ceiling |
| Breaker trip | Failures at a rate above the trip condition, over the minimum volume | The next call fails immediately **with no network attempt**, which the stub proves by receiving nothing |
| Breaker on slow calls | Mode 1, with no errors at all | The breaker opens on the latency threshold. A suite missing this test has a breaker that cannot see the failure that matters most |
| Half-open bound | Failures, then recovery, with many callers waiting | At most the configured trial count and concurrency reach the stub in the half-open state |
| Bulkhead isolation | Mode 1 saturating one dependency's stub | **A route that does not use that dependency still succeeds.** This single assertion is what proves isolation, and it is the test almost nobody writes |
| Shedding | Concurrency driven past the admission limit | Excess requests are rejected with the shed outcome; admitted requests keep their latency inside the SLO, which is what distinguishes shedding from queueing; health and readiness still answer |
| Queue bounds | Arrival rate above service rate, sustained | Depth stops at the bound; items past the wait bound are dropped **before** being processed; memory is flat |
| Degradation, per optional dependency | Timeout, connection refusal, and error response — three separate runs | The documented status, the degradation marker naming the missing contribution, and the rest of the response complete |
| Degraded aggregate | Every optional dependency failing at once | The declared minimum set is enforced: above it a marked response, below it a clean failure |
| Cache absorbs a cache outage | The cache unreachable | The origin serves the request inside the deadline, and origin calls per key are one per instance, not one per caller |
| Cache never absorbs an origin outage | The origin unreachable, the cache warm | Stale is served only inside the maximum age, marked with its age, and refused past it |
| Idempotency, sequential | The same key twice, in sequence | One effect; the second response is byte-identical to the stored first, including its identifiers |
| Idempotency, concurrent | The same key on two requests **in flight at once** | One effect, and the second returns one of the two documented outcomes. Required on every route with a key, because this is the case the audit of this fleet found untested everywhere |
| Idempotency, conflict | The same key with a different fingerprint | The conflict outcome, and no effect |
| Idempotency, honest retry | The same key with a differing trace identifier and timestamp | A replay, not a conflict — proving the fingerprint excludes what legitimately varies |
| Idempotency store unavailable | The key store unreachable | The documented outcome, and no unrecorded effect |
| Lease expiry | A first request killed mid-operation | The key becomes claimable only after the lease, and exactly one claimant wins |
| Error budget | Synthetic bad events at a known rate | The SLI query returns the expected ratio and the burn-rate rule fires; the alert's no-data behaviour was observed. `/alaa-observability-soc` (`$alaa-observability-soc` in Codex) owns the query and alert authoring |

## Load testing asserts behaviour at saturation

A load test that reports maximum throughput has measured a number nobody operates at. Run sustained load **at and above** the admission limit and assert the behaviour there:

- the shed rate rises and the admitted requests' latency stays inside the SLO — the signature of shedding, as against a latency curve that grows without bound, which is the signature of queueing;
- pool, bulkhead, and queue gauges sit at their limits rather than above them, and memory is flat rather than growing;
- health and readiness answer throughout;
- error responses are the shed outcome rather than timeouts, crashes, or connection resets;
- and after the load stops, every gauge returns to baseline. A gauge that stays elevated is a leak that the timeout was supposed to prevent.

Run it once with a dependency in mode 1 as well. Load plus a healthy fleet tests capacity; load plus one slow dependency tests the isolation, and only the second resembles an incident.

## Production experiments

Fault injection in production is permitted with all four of these, and is otherwise not run: a written hypothesis naming the expected behaviour; a blast radius bounded to a stated share of traffic or a stated tenant set; an abort condition wired to the same burn-rate signal that pages, so the experiment stops itself; and a remaining error budget, since the budget is the permission to experiment.

An experiment whose hypothesis was wrong has produced the most valuable result available and is written up as such. An experiment run without an abort condition is an outage with a plan.

## What a review accepts, and what it records

A review accepts a mechanism as verified when it can name the test, the injected mode, the assertion, and the observation — and when removing the mechanism makes that test fail. It records every mechanism decided but unproven as a gap, at the severity the mechanism's absence would carry, because an unproven mechanism and an absent one behave identically in the incident that needs it.

`/alaa-services-contract` (`$alaa-services-contract`) owns the values these tests assert against, and `/alaa-observability-soc` (`$alaa-observability-soc`) owns the signals the assertions read. Neither is restated here.
