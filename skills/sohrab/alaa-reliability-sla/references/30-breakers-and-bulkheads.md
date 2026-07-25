# Circuit Breakers And Bulkheads

Read when a dependency flaps, when one slow dependency exhausts a resource other routes need, or when a breaker is added or tuned. `SKILL.md` holds the binding rules on bounded pools and cancellation; this file is the state machine, the threshold derivation, and the isolation sizing. The Ala pool bounds and acquire waits are in `/alaa-services-contract` (`$alaa-services-contract` in Codex) `references/22-failure-load-and-deprecation-contract.md`.

## A breaker protects the caller

**The breaker exists so the caller stops spending its own resources on a dependency that is not answering.** Relieving the callee is a side effect. Two consequences follow, and both are commonly inverted:

- The thresholds come from **the caller's cost of waiting**, not from the callee's capacity. The question is "at what failure rate does calling cost me more than not calling?", and the cost is the caller's threads, pool slots, deadline, and the requests it could have served instead.
- The breaker lives **in the caller**, one instance per caller process, and it is not a shared service. A remote breaker is another dependency on the failure path, and a fleet-shared breaker state means one instance's local network problem opens the circuit for every instance.

**A timeout alone does not bound resource use.** With a three-second timeout and five hundred requests a second, fifteen hundred requests can be simultaneously in flight against one dead dependency, each holding a slot. The timeout bounds each request's wait; only a breaker and a bulkhead bound the total. That arithmetic is the reason both exist on top of timeouts rather than instead of them.

## Granularity: one breaker per dependency per operation class

A breaker's scope is the smallest unit whose failures are correlated and whose consequences are shared. In practice: per dependency, and split further per operation class when one class can fail while another succeeds — reads versus writes, a cheap lookup versus an expensive report, one shard versus another.

Scope too wide and a single broken endpoint opens the circuit for healthy ones, turning a partial failure into a total one. Scope too narrow — per URL with an identifier in it, per tenant — and no scope ever accumulates enough volume for its rate to be meaningful, so the breaker never trips and never protects anything. The test for a correct scope: **the failures inside it are correlated, and there is enough traffic in the window for a rate to mean something.**

## The three states, and what each does to a request

| State | What a request does | What the state is counting |
|---|---|---|
| Closed | The call is attempted, bounded by the deadline and a bulkhead slot | Outcomes over a rolling window, evaluated against the trip condition |
| Open | The call is **not attempted**. The caller immediately takes its failure path — the degraded response, or its dependency-unavailable outcome | Elapsed time until the open duration ends |
| Half-open | A bounded number of trial calls are attempted; every other request is treated exactly as in open | The trial outcomes only |

Rules the state machine must satisfy:

- **Open fails immediately.** A request in the open state does not wait, does not sleep until the breaker closes, and is never parked in a queue for the reset. Parking requests reproduces the exhaustion the breaker exists to prevent, with a different queue holding it.
- **Open is a first-class outcome, not an error to be hidden.** The caller's failure path is chosen by the dependency's classification: a gate refuses, a required contributor fails the request, an optional contributor degrades. `50-degradation.md` owns that path.
- **Half-open admits by count and concurrency, never by time.** A time-based half-open window admits every arriving request for its duration, which is the unbounded probe.
- **Any failure in half-open reopens immediately**, and the reopened duration is at least the previous one. Successes close the breaker only after the full trial count has succeeded; one success is not evidence of recovery.

## Deriving the trip condition from observed behaviour

Four inputs, each with a method:

1. **A failure rate, never an absolute count.** A count trips on ordinary noise on a low-traffic instance and never trips on a high-traffic one. Derive the rate from the dependency's observed healthy failure rate, set clearly above it, and below the rate at which continuing to call is worse than stopping.
2. **A minimum request volume in the window, evaluated before the rate is.** Without it, the first two failed requests after an idle period are a 100% failure rate and the breaker opens on nothing. Derive the minimum from the window length and the route's low-traffic-period rate, so an ordinary quiet hour cannot satisfy it with noise.
3. **A latency threshold that counts slow calls as failures.** A dependency answering at ten times its normal latency exhausts a caller exactly as a dependency returning errors does, and it does it while reporting success. Derive the threshold from the healthy p99 with headroom, or from the per-hop budget in `10-deadlines-and-timeouts.md` — whichever is smaller, because a call slower than its budget is already useless.
4. **A window shape.** A rolling window of counts or a time-decayed rate, long enough that one unlucky burst does not trip it and short enough that the breaker reacts inside the incident. Derive it from the dependency's observed blip duration: the window is longer than a blip that recovers on its own.

Which outcomes count as failures: transport failures, timeouts, and the callee's own overload and unavailability responses. Do **not** count the callee's rejections of a bad request — a `4xx` means the caller sent something wrong, and letting a client defect open the circuit removes a healthy dependency for every other caller. Do **not** count a request the breaker itself rejected, which would make an open breaker self-sustaining.

## Deriving the reset condition

The open duration is at least the dependency's observed time to actually recover — a process restart, a failover, a pool refill, a deploy rollback — because probing sooner cannot succeed and each probe is a request the recovering dependency serves instead of recovering.

**Randomise the open duration per instance.** With a fixed duration every instance in the fleet probes in the same second, so the recovering dependency's first moment of availability receives the whole fleet's probe traffic. The same decorrelation argument as jitter in `20-retries.md`, applied to a different clock.

The trial count in half-open is small and fixed, and its concurrency is capped at a value the recovering dependency can serve while still recovering. The failure this prevents is specific: every caller that has been failing fast for a minute has capacity available, so an unbounded half-open sends all of it at once and knocks the dependency down again. The resulting alternation between open and overloaded is indistinguishable from the dependency flapping on its own, which is why it survives so long undiagnosed.

## Bulkheads: per-dependency isolation

A bulkhead is a concurrency cap on calls to one dependency, held for the duration of an attempt, with an immediate rejection when full. It answers a question a breaker cannot: **how many calls can be stuck here before the rest of this service starves?**

Why it is required in addition to a breaker: a breaker acts on the *rate* of failures, and the failure mode that kills a service is a dependency that is slow while still succeeding. Nothing fails, the breaker stays closed, and every worker ends up waiting on the same dependency. Requests to unrelated routes then fail with no relation to the traffic on the slow route, which is the symptom that makes this the hardest failure in the fleet to diagnose from the outside.

Sizing method:

- Give each dependency a cap **strictly below the shared resource it draws from** — the worker count, the connection pool, the thread pool — so that the sum of the caps of the routes that may saturate together leaves the shared resource with slack. Exhaustion then becomes impossible by construction rather than unlikely by observation.
- Derive each cap from the dependency's share of concurrent traffic at peak plus headroom, not from an even split. An even split starves the hot dependency and wastes the cold one's allowance.
- **Bound the wait for a slot** and treat expiry as the dependency-unavailable outcome. An unbounded wait for a bulkhead slot is a queue with no depth limit, which is the failure the bulkhead was installed to prevent.
- **A queue in front of a bulkhead is capacity for a burst, not for sustained overload**, and is bounded in depth and in wait like any other queue — `40-admission-and-shedding.md`.

Isolate at the pool level too, not only in application code. Separate connection pools for calls with different failure profiles — interactive product queries versus reporting or batch, product traffic versus background workers — so a long-running consumer cannot drain the pool the request path needs. `/alaa-data-layer` (`$alaa-data-layer`) owns the driver mechanics; the decision to split, and where, is here.

## The observable that proves it

A bulkhead and a breaker are only correct if their limits are visible: the in-use and available slots per dependency, the breaker's state and its transitions, and the count of calls rejected by each. A service that caps a resource without exporting its utilisation has no way to know whether the cap is right, and will discover it during the incident. `/alaa-observability-soc` (`$alaa-observability-soc`) owns which signals are required and at what level; `/alaa-services-contract` (`$alaa-services-contract`) owns their names.
