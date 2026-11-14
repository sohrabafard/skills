# Topic Map

Read before selecting mechanism detail or diagnosis. It routes only; every rule lives in the file named beside it, and the always-binding rules live in `SKILL.md`. It also names the owners outside this skill and the known anti-patterns.

## By what the task is doing

| The task | Read |
|---|---|
| Adds or changes an outbound call of any kind | `10-deadlines-and-timeouts.md`, then `30-breakers-and-bulkheads.md` for the isolation slot |
| Adds, removes, or tunes a retry | `20-retries.md`, and `60-idempotency.md` before declaring the retry legal |
| Adds an end-to-end latency target, splits one across hops, or changes cancellation, per-hop budgets or a durable-acceptance lifecycle | `10-deadlines-and-timeouts.md` |
| Adds a circuit breaker, or one dependency is exhausting a shared pool | `30-breakers-and-bulkheads.md` |
| Adds a queue, an in-flight limit, a rate limit or a shed decision; a route saturates, a queue grows, or rate and concurrency limits are confused | `40-admission-and-shedding.md` |
| Makes a response partial, adds a fallback, or uses a cache to survive an outage | `50-degradation.md` |
| Adds a state-changing route a caller may repeat, makes a retry legal, or designs a key store | `60-idempotency.md` |
| Defines or challenges an SLI, SLO, error budget, or release gate | `70-error-budgets-and-slos.md` |
| Is about to be called done, or must decide what evidence a review accepts | `80-verification.md` |

## By symptom, when diagnosing

| Symptom | Most likely mechanism | Read |
|---|---|---|
| A request exceeded its target while every hop stayed inside its own timeout | No propagated deadline; the hops summed | `10-deadlines-and-timeouts.md` |
| One dependency's incident made every route on the service fail | No per-dependency isolation; the shared pool drained | `30-breakers-and-bulkheads.md` |
| A dependency's load rose during its own outage | Retry amplification, or an unbounded half-open probe | `20-retries.md`, `30-breakers-and-bulkheads.md` |
| Latency grew without bound but almost nothing errored | Work was queued where shedding was required | `40-admission-and-shedding.md` |
| The service was removed from rotation while it was merely busy | A shed or blocked readiness path | `40-admission-and-shedding.md` |
| A duplicate record appeared under load and not in testing | Two concurrent requests carrying the same key | `60-idempotency.md` |
| Clients cached a partial answer as if it were complete | An unmarked degraded response | `50-degradation.md` |
| A stale value was served through an outage of the system that owns the truth | A cache absorbing the wrong outage | `50-degradation.md` |
| An alert fired only after the month's budget was already gone | A static threshold where a burn rate belonged | `70-error-budgets-and-slos.md` |
| The mechanism was in the code and did not run | It was never exercised | `80-verification.md` |

## Where the values are

No file in this skill states an Ala timeout, retry count, pool bound, acquire wait, shed threshold, response code, or event name. All of those are in `/alaa-services-contract`, `references/22-failure-load-and-deprecation-contract.md`. When a rule here needs a number, read that file for it.

## Owned by another skill

- `/alaa-services-contract` owns every Ala value and the wire behaviour that carries it: the per-hop timeout table, the retry budget, the pool bounds and acquire wait, the shed threshold, the response codes and event names, and the deprecation procedure for any of them — `references/22-failure-load-and-deprecation-contract.md`. Point at it for the number; never copy one here.
- `/alaa-security-review` owns every control that decides whether a caller may act, the full definition of "cannot reach a decision", and the fail-closed doctrine. This skill owns fail-open and degradation for availability, split by the discrimination rule in `SKILL.md`.
- `/alaa-observability-soc` owns the telemetry plane's own reliability, the signals that prove these mechanisms fired, and burn-rate alerting arithmetic including the multi-window table — `references/40-alerting-slo-retention.md`. This skill owns the behaviour; that skill owns the signal and the alert.
- `/alaa-async-messaging` and `/alaa-laravel-job-rabbitmq` own broker prefetch, acknowledgement, consumer concurrency, and dead-letter mechanics. This skill owns the request-side idempotency contract and the shed-versus-queue decision that sends work to a broker at all.
- `/alaa-data-layer` owns pool mechanics inside a driver, transaction and isolation semantics, and the index that a uniqueness constraint compiles to. This skill owns why the constraint must exist and where it must live.
- `/alaa-controlled-ops` owns the bulk-operation approval lifecycle and its dry-run hashes. This skill owns the general replay-versus-conflict contract that lifecycle instantiates.
- The per-language skills own idiom — which library, which construct, which annotation. This skill owns the decision the idiom expresses.
- `/alaa-prompting-guide` owns model and effort capability evidence and runtime mechanics; the runtime orchestrator owns actual task allocation for every authority role. This skill names no model.

## Anti-patterns

- setting a per-call timeout with no request deadline above it, so a chain of compliant hops still misses the target;
- a timeout longer than the caller's remaining budget, which spends the callee's capacity on a result nobody will read;
- retrying at three layers and calling it defence in depth, when it is a load multiplier of the product of the counts;
- a rate limit installed to protect a resource, which it does not bound, instead of a concurrency limit, which does;
- one global circuit breaker, which turns one broken endpoint into a total outage;
- an unbounded half-open probe, which knocks the recovering dependency down at the instant it becomes reachable;
- a stale cached value served for an authoritative-source outage with no maximum age and no marker;
- checking whether an idempotency key exists and then writing, which two concurrent requests both pass;
- returning a fresh identifier for a replayed key, which has created a second resource under a key the caller believes is unique;
- an error budget with no consequence, which is a dashboard, or a budget never consumed, which is unpurchased velocity and a mis-set SLO.
