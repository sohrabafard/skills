---
name: alaa-reliability-sla
description: "Reliability doctrine for services under a 99.99%+ SLA: request deadlines and timeouts, retries with jittered backoff and retry budgets, circuit breakers and bulkheads, admission control and load shedding, graceful degradation, the idempotency contract, error budgets and SLOs, and the fault injection that proves each mechanism fired. Use when adding or reviewing an outbound call, a retry, a timeout, a pool bound, a cache fallback, a shedding decision, a repeatable write, or an SLO; when a dependency is slow, flapping, or gone; and when deciding what a request does with a failing dependency. Do not use for exact Ala timeout, retry, pool, or shed values, which are /alaa-services-contract. Route whether a caller may act, and any control that must fail closed, to /alaa-security-review; burn-rate alert authoring to /alaa-observability-soc; broker prefetch, acknowledgement, and DLQ mechanics to /alaa-async-messaging."
---

# Alaa Reliability SLA

Decide and review what a service does when a dependency is slow, flapping, overloaded, or gone, so every service in the fleet does the same thing under the same failure. Uniformity is the deliverable: a fleet where each caller invents its own retry curve cannot be debugged, because no operator can predict what any caller will do to any callee during an incident.

This skill owns doctrine — why a mechanism exists, how to choose its shape, what defeats it, and what evidence proves it ran. It owns no Ala value. Every timeout, retry count, pool bound, acquire wait, and shed threshold this platform ships lives in `/alaa-services-contract`, `references/22-failure-load-and-deprecation-contract.md`. Read that file for the value and this skill for the reason. This skill states no number, because a number restated in two files drifts in one of them and the reader cannot tell which.

## When this applies

Any change that adds or alters an outbound call, a timeout or deadline, a retry, a connection or worker pool bound, a circuit breaker, a bulkhead, a queue, an admission or shedding decision, a cache used as a fallback, a write a caller may repeat, or an SLO — and any diagnosis of a slow, flapping, or unavailable dependency.

It does not apply to a change that makes no outbound call, holds no shared resource, and alters no failure path.

## The discrimination rule: fail closed, or fail open

Before choosing a timeout fallback, retry, cache or degraded path, classify the dependency through
/alaa-security-review's `Fail-closed versus fail-open, and which doctrine applies` section. It owns
the discriminator and every "cannot decide" state. Gates still need bounds; this skill's retry,
cache, stale-serve and degradation rules never substitute for a gate's answer.

A contributor degrades, sheds, drops or serves without the contribution and records the loss; its
failure must not turn a visibility incident into a product outage. Before disposing of durably
accepted work, apply `references/10-deadlines-and-timeouts.md`: fail-open releases no accepted obligation.
If classification is unresolved, treat the dependency as a gate and report it: a wrongly opened gate
can permit a breach that remains invisible, while a wrongly gated contributor visibly costs availability.

## Non-negotiables

1. Every synchronous request carries one deadline, computed at ingress and honoured to completion. Per-call timeouts alone bound no request, because N sequential hops each inside its own timeout sum past any end-to-end target.
2. Every outbound call — HTTP, database, cache, broker, internal RPC — is constructed with an explicit timeout and takes a slot from a bounded pool. An unbounded call is a defect against a healthy dependency, because health is not a property the call site can rely on.
3. A timeout promptly initiates cancellation of the attempt and releases caller-held resources. Cancellation, ambiguous effects, and durable ownership follow `references/10-deadlines-and-timeouts.md`; stopping an HTTP wait alone neither proves rollback nor cancels an accepted job.
4. A retry is legal only when repeating the call cannot produce a second effect. There is no third option: either the effect is idempotent, or the call is not retried.
5. Exactly one layer in a call chain retries a given logical call. Every other layer, including a client library whose default is nonzero, sets its retry count to zero explicitly, and the code records which layer owns the retry.
6. Every backoff is exponential with full jitter. A fixed delay and a zero delay are both forbidden, and equal delays across callers are the mechanism that turns one blip into a standing herd.
7. Every queue has bounded capacity and bounded waiting under an explicit policy. Caller-bound stale work is dropped before processing; accepted work follows the lifecycle in `references/10-deadlines-and-timeouts.md`, not a blanket expiry/drop rule.
8. Synchronous product traffic is shed, never queued behind a capacity wait; work that must survive gains persisted ownership before an application acceptance receipt. `references/40-admission-and-shedding.md` decides admission around that boundary. Health, readiness, and liveness endpoints are never shed and never contend for the pool product traffic is saturating.
9. Every dependency is declared required or optional before it fails, in the code and in the route's documentation. An undeclared dependency behaves as required, because that is what the code does when it fails.
10. A degraded response says it is degraded, in a machine-readable field naming the missing contribution. A silent degradation is indistinguishable from real data, so it gets cached, aggregated, and discovered in a customer report weeks later.
11. A degraded path with no automated test that exercises it is not a degraded path. It is untested error handling that will run for the first time during an incident.
12. Every mechanism above has one test that fails when the mechanism is removed. A mechanism never observed to fire is a hypothesis, and its presence in the code is not evidence.

## Procedure for a dependency call or a load path

Walk this in order. Each step names the reference that owns its detail.

1. **Classify.** Gate or contributor; if contributor, required or optional. Record it where the code reads it. (`50-degradation.md`)
2. **Bound.** Identify request-bound or durably accepted work and select its execution context; set connect, read, and total as three distinct limits; take a slot from a per-dependency concurrency cap sized strictly below the shared pool. (`references/10-deadlines-and-timeouts.md`, `30-breakers-and-bulkheads.md`)
3. **Decide retry legality** before writing any retry: is the effect repeatable, is the outcome class retryable, does the applicable execution budget cover another attempt, and is this the one retrying layer? For accepted work, check its owner-defined validity and cancellation too. Any "no" means no retry at this layer. (`20-retries.md`, `60-idempotency.md`)
4. **Decide the breaker.** The trip condition as a rate over a minimum volume, the open duration, the bounded half-open probe, and what a request receives while the breaker is open. (`30-breakers-and-bulkheads.md`)
5. **Decide the failure response.** A gate refuses. A required contributor fails the request promptly rather than spending the whole deadline. An optional contributor degrades, marks the response, and emits the signal. (`50-degradation.md`)
6. **Decide admission.** The in-flight limit, the shed order, and what is never shed. (`40-admission-and-shedding.md`)
7. **Take the values from the platform contract**, never from judgment at the keyboard. Where the contract has no value for this workload, derive it by the method below and record the derivation beside the value.
8. **Write the evidence.** One test per mechanism decided above. (`80-verification.md`)

## Choosing a value the platform contract does not give you

Every value answers a stated question, and the question fixes the method. Record the number, its question, its method, and the observation it came from, next to the value — a value with no recorded derivation is re-tuned by guess at the next incident.

| Value | The question it answers | Method |
|---|---|---|
| A per-hop timeout | Past what latency is this answer worthless to the caller? | The smaller of the caller's remaining budget and the dependency's observed healthy p99 plus headroom |
| A retry budget | How much extra load may we add to a dependency that is already failing? | A fraction of successful traffic over a window, not a per-call count alone |
| A concurrency cap | How many calls can be stuck here before the rest of this service starves? | Strictly less than the shared pool it draws from, so exhaustion is impossible by construction |
| A breaker trip condition | At what failure rate does calling cost more than stopping? | A failure rate over a minimum request volume, with slow calls counted as failures |
| A queue depth and wait | How much work can be held, and when is it still valid to execute? | Derive capacity from workload; bound caller-bound wait by the request deadline, and accepted-work wait by its owner-defined lifecycle in `references/10-deadlines-and-timeouts.md` |
| An SLO target | What does a user experience as broken? | A predicate on one event at the closest point to the user the service can observe |

## Output contract

Return these, in this order, for every design, review, or diagnosis:

```text
Decision: pass | pass-with-actions | blocked
Scope: routes, dependencies, and load paths examined
Classification: each dependency -> gate | required contributor | optional contributor, and where it is declared
Bounds: request or attempt deadline source, per-hop timeouts, pools and caps, and the contract value each came from
Durable work: persisted ownership boundary, validity/cancellation/disposition owner, retention, and unknown-acceptance reconciliation
Failure behaviour: per dependency -> what the request returns, and what the caller sees
Retries: which layer retries, the outcome classes, the backoff shape, the budget
Breakers and shedding: trip and reset conditions, in-flight limit, shed order, never-shed list
Idempotency: key source, scope, storage and constraint, concurrent-duplicate branch, store-unavailable branch
Error budget: the SLI predicate, the SLO, the window, and what exhaustion obliges
Evidence: per mechanism -> the test or injection run, and what was observed
Gaps: mechanisms decided but unproven, and values with no recorded derivation
```

## Stop conditions

Stop successfully when every dependency in scope is classified, bounded, and has a decided failure response; every mechanism has a test that fails without it; and every value traces to the platform contract or to a recorded derivation.

Stop and report blocked when: a dependency cannot be classified as gate or contributor from the code and the repository's documentation; a required value is absent from the platform contract and the workload data needed to derive it does not exist; a required durable-work lifecycle decision is missing under `references/10-deadlines-and-timeouts.md`; a route's idempotency guarantee cannot be placed in the same transactional store as its effect and no reconciliation path exists; or a mechanism cannot be tested without a production experiment the user has not authorized.

## When NOT to use

- You need the exact Ala number — a timeout, a retry count, a pool bound, a shed threshold. This skill
  states no Ala value; it states why a mechanism exists and how to choose its shape.
- The path makes no outbound call, holds no pool, and has no defined behaviour when a dependency fails.
- The question is whether an actor is permitted to act at all, or a control that must fail closed for
  security rather than availability reasons. The routing table below names each owner.

## Reference routing

Before selecting mechanism detail or diagnosis, read `references/00-topic-map.md`; it selects only
the references whose conditions apply. Loading the whole tree means the task was not scoped.

## What this skill does not own

- `/alaa-services-contract` owns every Ala value and the wire behaviour that carries it: the per-hop timeout table, the retry budget, the pool bounds and acquire wait, the shed threshold, the response codes and event names, and the deprecation procedure for any of them — `references/22-failure-load-and-deprecation-contract.md`. Point at it for the number; never copy one here.
- `/alaa-security-review` owns every control that decides whether a caller may act, the full definition of "cannot reach a decision", and the fail-closed doctrine. This skill owns fail-open and degradation for availability, split by the discrimination rule above.
- `/alaa-observability-soc` owns the telemetry plane's own reliability, the signals that prove these mechanisms fired, and burn-rate alerting arithmetic including the multi-window table — `references/40-alerting-slo-retention.md`. This skill owns the behaviour; that skill owns the signal and the alert.
- `/alaa-async-messaging` and `/alaa-laravel-job-rabbitmq` own broker prefetch, acknowledgement, consumer concurrency, and dead-letter mechanics. This skill owns the request-side idempotency contract and the shed-versus-queue decision that sends work to a broker at all.
- `/alaa-data-layer` owns pool mechanics inside a driver, transaction and isolation semantics, and the index that a uniqueness constraint compiles to. This skill owns why the constraint must exist and where it must live.
- `/alaa-controlled-ops` owns the bulk-operation approval lifecycle and its dry-run hashes. This skill owns the general replay-versus-conflict contract that lifecycle instantiates.
- The per-language skills own idiom — which library, which construct, which annotation. This skill owns the decision the idiom expresses.
- `/alaa-prompting-guide` owns model/effort capability evidence and runtime mechanics; the runtime orchestrator owns actual task allocation for every authority role. This skill names no model.

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
