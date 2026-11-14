---
name: alaa-laravel-job-rabbitmq
description: "Laravel queued jobs on RabbitMQ through vladimir-yuldashev/laravel-queue-rabbitmq: the queue:work versus rabbitmq:consume decision, config/queue.php driver keys, ack and nack policy, delivery limits and the crash-loop hazard, prefetch sizing, publisher confirms, worker recycling and graceful stop, and eight named failure classes. Use it when writing or reviewing a ShouldQueue job that runs on RabbitMQ, a rabbitmq connection block, a worker command or worker Deployment, or a live queue incident on this driver. Do not use it to choose between Kafka and RabbitMQ, to design event topologies or fan-out, or for Redis queues and Horizon: that is /alaa-async-messaging. Queue and vhost names are /alaa-services-contract; retry, backoff, DLQ and idempotency doctrine is /alaa-reliability-sla; broker cluster administration is /caas-arvan-kuber; chart and rollout mechanics are /alaa-k8s-helm."
---

# Purpose

Make Laravel `ShouldQueue` jobs on RabbitMQ behave predictably when things go wrong: no silently lost
message, no side effect applied twice, and a bounded outcome when the broker or worker disappears mid-flight.

**Use it** for a queued job that runs on RabbitMQ, the `rabbitmq` connection in `config/queue.php`, a worker
command line or Deployment, or a live queue incident on this driver.

**Not for** the transport decision, event topology, fan-out or event versioning: that is
`/alaa-async-messaging`. **On conflict, this skill decides the broker-specific mechanics of this Laravel
driver, and `/alaa-async-messaging` decides messaging architecture and the fleet-wide DLQ replay procedure.**

Before you act on a task that names a version, `queue:monitor`, a monitor method, a worker mode, DLX or DLQ,
quorum queues, prefetch, heartbeat, TLS or failed reroute, work the freshness triggers in
`references/source-map.md` against the installed package source. That list is the trigger. Do not substitute
your own judgement of whether verification is needed.

## Router

| You are about to… | Read |
| --- | --- |
| write or edit the `rabbitmq` block in `config/queue.php`, or any `RABBITMQ_*` variable in `.env`, a values file or a Compose file | `references/config-queue-rabbitmq.md` |
| write a worker command line, set a replica count or recycle limit, or change a worker Deployment | `references/running-workers.md` |
| diagnose a queue that is stalled, looping, storming, duplicating, or failing to publish | `references/failure-classes.md` |
| assert a driver version, call `queue:monitor`, reason about `retry_after`, or trust a flag default, a config key or the publish path | `references/driver-facts.md` |
| find a `repositories` VCS override for this package, or are about to add one | `references/fork-divergence.md` |
| decide which source wins, or hit a freshness trigger | `references/source-map.md` |
| state a rule, make a decision or edit code on ground this skill does not own: a number, a name, an observability level, messaging architecture, deployment, test design, security, code shape, complexity, the quality bar, a design pass, a generated wrapper or a plan file | `references/ownership-boundary.md` |

## Worker mode

| | `queue:work rabbitmq` | `rabbitmq:consume rabbitmq` |
| --- | --- | --- |
| Primitive | `basic_get`, a round trip per message | `basic_consume`, broker pushes |
| Queues per process | many, priority list `high,default` | exactly one |
| Prefetch | not applicable | `basic_qos`, set once before consuming |
| Unacked window | 1 | the prefetch count |
| Requeue on worker stop | yes — `close()` can requeue the in-flight job | no — the queue's current-job slot stays empty |

Use **`rabbitmq:consume`** when one Deployment serves one queue and throughput matters. Use **`queue:work`** when one
process must drain several queues in priority order, or when an unacked window of 1 is worth the round trip.
Never pass more than one queue to `rabbitmq:consume`, because its help text says it has no support for that.
A second queue means a second Deployment.

# Hard constraints

**1. Delivery is at-least-once, so every handler is idempotent.** A database uniqueness constraint on the
business key holds the guarantee. A Redis or cache dedupe key is a fast path in front of it, never a
replacement. `alaa-reliability-sla references/60-idempotency.md` owns the key contract, its scope, its
retention and the two-in-flight case.

**2. Ack and nack policy.** Each of the three outcomes has one route.

- **Ack**: the handler completed and Laravel deleted the job, or Laravel released it. Never call `ack()` from application code.
- **Reject without requeue**: Laravel marked the job failed, and this driver path reaches a dead-letter exchange. For
  a non-retryable business error, take this route deliberately with `$this->fail($e)` rather than throwing and
  burning every attempt.
- **Reject with requeue**: permitted in exactly one place, the driver's own `close()` on worker
  stop. Application code, job middleware and handlers must not call `reject($job, true)`.

To retry, call `$job->release($delay)`. A release increments the attempt count, and a requeue does not.

**3. Every quorum queue carries a broker-policy delivery limit, and every worker passes an explicit `--tries`.**
Set the limit as a quorum-queue policy, never as a queue argument. The driver emits no `x-delivery-limit` and
silently drops an invented one. The limit is required because a requeue or an unacked redelivery returns the
identical message with its attempt header unchanged. Repeated returns below `--tries` never spend that bound.
A job that dies before release can loop indefinitely, including across `--max-jobs` or `--max-time`
recycling.

Delivery limits bound only counted failures. Verify the actual return path under
`alaa-async-messaging references/40-dead-letter-and-replay.md`. Non-counting returns and classic queues need
a separately proven application bound. The derivation is in `references/driver-facts.md`, and the diagnosis is
`references/failure-classes.md` class 8. The values are in
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`, and the doctrine is in
`alaa-reliability-sla references/20-retries.md`.

**4. Two timeout relationships bound duplicate execution.** `retry_after` is not one of them, because it is
inert on this connection (`references/driver-facts.md`).

- Worker `--timeout` multiplied by the depth of the unacked window stays below the applicable broker
  acknowledgement timeout. Timeout scope, and whether the broker cancels the consumer or closes the channel,
  depend on broker version, queue type and negotiated capability. Verify recovery through
  `alaa-async-messaging references/30-consuming-ack-and-prefetch.md`. An open channel alone is not health.
- Pod `terminationGracePeriodSeconds` exceeds worker `--timeout` plus the shutdown margin. Below that, every
  rollout SIGKILLs a worker mid-job and replays the delivery with its attempt count unchanged.

The contract file above owns both values and the margin.

**5. Pass `--prefetch-count` explicitly in consume mode.** The pinned command's default is `1000`.
Verify the installed default through `references/driver-facts.md`. Before you choose the value, read
`alaa-async-messaging references/30-consuming-ack-and-prefetch/40-prefetch.md` for the measured-p99
window derivation, and report both the count and the measured duration. The contract file above owns values.

**6. Publisher confirms are a decision, not silence.** This driver never calls `confirm_select`, so a publish
reports success once the frame reaches the socket. A broker that dies before it persists the message loses it
while the application believes the publish succeeded. The decision: a request-path publish does not wait on a
confirm. Durability comes from the durable outbox row that the contract file above already requires. The
outbox drain worker is the one place where a confirm is required, because the contract file above forbids
deleting an outbox row before the broker acknowledges the publish, and `basic_publish` is not an
acknowledgement. `references/driver-facts.md` holds how to add a confirm and what it costs.

**7. Broker unreachable on the request path.** A request-path publish never blocks the user-facing response
on broker recovery and never fails the business write. The outbox above is the mechanism. The doctrine is in
`alaa-reliability-sla references/50-degradation.md`, and the values are in the contract file above.
`references/driver-facts.md` holds the driver mechanics that change the answer: a lazy connect, and one host
chosen at random per connection with no retry inside a publish call.

**8. The seam carries the trace.** The trace field travels as a constructor property inside the serialised
job payload. Set it at dispatch and read it at the top of `handle()`, because this driver exposes no AMQP
header injection point. The `correlation_id` that the driver already sets is the broker-side join key for the
same message. `/alaa-services-contract` owns the field name, and `/alaa-observability-soc` decides whether
carrying it is required. This seam uniquely produces these signals: queue depth, consumer count, unacked
count, oldest-unacked age, redelivery rate and worker restart rate. Register them rather than invent them:
`alaa-services-contract references/24-metric-registry.md` names them, and `/alaa-observability-soc` levels them.

**9. Horizon is not the control plane for these workers.** Set `'worker' => 'default'` on the connection, and
leave `RABBITMQ_WORKER` unset or `default` everywhere. Horizon is Redis-queue tooling, and its dashboard,
metrics and supervisor semantics do not observe a RabbitMQ queue. Observe these workers through broker
metrics, worker logs and application metrics. Use `queue:monitor` only as a ready-depth threshold alarm
(`references/driver-facts.md`).

**10. Dead-lettering and delivery limits come from broker policies, never queue arguments.** A queue argument
is fixed at declare time, and this driver never re-declares an existing queue, so an argument changed in
config does nothing to a queue that already exists. A policy applies to existing queues and reverts without a
deploy. Pre-create the exchange, queue and binding in infrastructure or a release job before consumers scale.

**11. Give every outbound call inside a handler a client timeout strictly below the worker `--timeout`**,
so that the handler fails and releases rather than holding the delivery until the broker kills the channel. A
300-second HTTP call inside a 60-second job violates this. The contract file above owns the values.

**12. Secrets never enter the repository.** Commit no `.env`, private key, certificate, password or token.
Every value comes from a Secret or a secret file.

**13. Redis touches inside jobs.** RabbitMQ is the transport, and Redis never carries these jobs. Job
middleware backed by Redis (`RateLimited`, `WithoutOverlapping`, `Redis::throttle` funnels) has a defined
outage behaviour, recorded in the change. `/alaa-security-review` owns the fail-closed discriminator.
`alaa-data-layer references/50-redis-laravel-octane.md`, via `/alaa-data-layer`, owns keys, TTL and the
Redis-down fallback contract. Make no cache or Redis read in a provider `register()` or `boot()`, because
otherwise a Redis outage stops workers from starting.

**14. Uniformity over local preference in job policy.** Use whichever form the repository already uses for
every job in it: attributes (`#[Tries]`, `#[Backoff]`, `#[Timeout]`, `#[FailOnTimeout]`) or properties and
methods. A repository that mixes both standardises on the attribute form and converts the rest in the same
change. Where queue or connection selection would otherwise repeat across dispatch sites, put it in central
`Queue::route(...)` rules.

# The one required test

**A redelivered message must not double-apply its side effect.** Every handler with a side effect has this
test. A change that adds such a handler without it is incomplete.

Read `alaa-async-messaging references/60-telemetry-and-proof.md`, "The two required tests", for the
redelivery assertion set. This driver adds two checks:

- Deliver the **same payload with the attempt count unchanged**, as a requeue does.
- Assert that the duplicate is acked rather than released, so that requeueing cannot masquerade as deduplication.

Keep the owner's effect, receipt and duplicate-counter proof.

`/alaa-testing-strategy` decides what makes this a test rather than a replay of the happy path, which layer it
belongs at, and whether the broker is real or faked: read
`alaa-testing-strategy references/70-failure-mode-first.md` and
`alaa-testing-strategy references/30-doubles.md`. Take Pest and PHPUnit syntax from the
repository-local `pest-testing` skill. This repository does **not** own that skill, and it can change between
runs. On conflict about what the test must prove, `/alaa-testing-strategy` wins, and this rule stands
regardless of syntax. Step 3 of `references/running-workers.md` verifies the same property on real
infrastructure.

# When NOT to use

- The decision is which broker to run at all (Kafka against RabbitMQ), or what the event topology and
  fan-out should be. Both are settled before any job exists.
- The queue runs on Redis with Horizon, or on any driver other than this RabbitMQ package.
- The work is broker cluster administration (nodes, quorum members, disk alarms, upgrades) rather than
  how a Laravel job behaves on a broker that is already running.
- The task is naming a queue, vhost or exchange, or setting a retry, backoff, DLQ or idempotency policy.
  `references/ownership-boundary.md` names each owner.

# Ownership boundary

This skill owns one thing: the behaviour of Laravel jobs on **this** RabbitMQ driver. Before you state a rule, make a decision
or edit code on any other ground, read `references/ownership-boundary.md`. It names the owner of numbers, names,
observability levels, messaging architecture, deployment, test design, security, code shape, complexity and
worker hygiene. The named owner wins on conflict.

# Output contract

Report:

- files changed
- the installed driver version and the grep that confirmed its monitor methods
- each config key changed and the behaviour it produces
- the worker mode and why
- the prefetch count with the measured p99 handler duration behind it
- the delivery limit and where its policy is set
- the redelivery test and its assertion
- the rollback step
- every assumption, monitoring limitation and unresolved risk, naming which are limits of this driver rather than of the change
