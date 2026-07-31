---
name: alaa-laravel-job-rabbitmq
description: "Laravel queued jobs on RabbitMQ through vladimir-yuldashev/laravel-queue-rabbitmq: the queue:work versus rabbitmq:consume decision, config/queue.php driver keys, ack and nack policy, delivery limits and the crash-loop hazard, prefetch sizing, publisher confirms, worker recycling and graceful stop, and eight named failure classes. Use it when writing or reviewing a ShouldQueue job that runs on RabbitMQ, a rabbitmq connection block, a worker command or worker Deployment, or a live queue incident on this driver. Do not use it to choose between Kafka and RabbitMQ, to design event topologies or fan-out, or for Redis queues and Horizon: that is /alaa-async-messaging ($alaa-async-messaging). Queue and vhost names are /alaa-services-contract; retry, backoff, DLQ and idempotency doctrine is /alaa-reliability-sla; broker cluster administration is /caas-arvan-kuber; chart and rollout mechanics are /alaa-k8s-helm."
---

# Purpose

Make Laravel `ShouldQueue` jobs on RabbitMQ behave predictably when things go wrong: no silently lost
message, no side effect applied twice, and a bounded outcome when the broker or worker disappears mid-flight.

**Use it** for a queued job that runs on RabbitMQ, the `rabbitmq` connection in `config/queue.php`, a worker
command line or Deployment, or a live queue incident on this driver.

**Not for** the transport decision, event topology, fan-out or event versioning — that is
`/alaa-async-messaging` (`$alaa-async-messaging`). **On conflict: broker-specific mechanics of this Laravel
driver are decided here; messaging architecture and the fleet-wide DLQ replay procedure are decided there.**

Before acting on a task naming a version, `queue:monitor`, a monitor method, a worker mode, DLX/DLQ, quorum
queues, prefetch, heartbeat, TLS or failed reroute, work the freshness triggers in `references/source-map.md`
against installed package source. That list is the trigger — do not substitute your own judgement of whether
verification is needed.

## Router

| You are about to… | Read |
| --- | --- |
| write or edit the `rabbitmq` block in `config/queue.php`, or any `RABBITMQ_*` variable in `.env`, a values file or a Compose file | `references/config-queue-rabbitmq.md` |
| write a worker command line, set a replica count or recycle limit, or change a worker Deployment | `references/running-workers.md` |
| diagnose a queue that is stalled, looping, storming, duplicating, or failing to publish | `references/failure-classes.md` |
| assert a driver version, call `queue:monitor`, reason about `retry_after`, or trust a flag default, a config key or the publish path | `references/driver-facts.md` |
| find a `repositories` VCS override for this package, or are about to add one | `references/fork-divergence.md` |
| decide which source wins, or hit a freshness trigger | `references/source-map.md` |

## Worker mode

The modes use different AMQP primitives, so the difference is behavioural.

| | `queue:work rabbitmq` | `rabbitmq:consume rabbitmq` |
| --- | --- | --- |
| Primitive | `basic_get`, a round trip per message | `basic_consume`, broker pushes |
| Queues per process | many, priority list `high,default` | exactly one |
| Prefetch | not applicable | `basic_qos`, set once before consuming |
| Unacked window | 1 | the prefetch count |
| Requeue on worker stop | yes — `close()` can requeue the in-flight job | no — the queue's current-job slot stays empty |

**`rabbitmq:consume`** when one Deployment serves one queue and throughput matters. **`queue:work`** when one
process must drain several queues in priority order, or when an unacked window of 1 is worth the round trip.
Never pass more than one queue to `rabbitmq:consume`: its own help text says there is no support for it, and
a second queue means a second Deployment.

# Hard constraints

**1. Delivery is at-least-once; every handler is idempotent.** The guarantee lives in a database uniqueness
constraint on the business key; a Redis or cache dedupe key is a fast path in front of it, never a
replacement. Key contract, scope, retention, two-in-flight: `/alaa-reliability-sla`
(`$alaa-reliability-sla`) `alaa-reliability-sla references/60-idempotency.md`.

**2. Ack and nack policy.** Three outcomes, one route each. **Ack**: the handler completed and Laravel
deleted the job, or Laravel released it — never call `ack()` from application code. **Reject without
requeue**: Laravel marked the job failed, and this is the only path that reaches a dead-letter exchange; take
it deliberately for a non-retryable business error with `$this->fail($e)` rather than throwing and burning
every attempt. **Reject with requeue**: permitted in exactly one place, the driver's own `close()` on worker
stop — application code, job middleware and handlers must not call `reject($job, true)`. To retry, call
`$job->release($delay)`: release increments the attempt count, requeue does not.

**3. Every queue carries a broker-policy delivery limit; every worker passes an explicit `--tries`.** The
limit is a quorum-queue policy, never a queue argument — the driver emits no `x-delivery-limit` and silently
drops an invented one. It is required because a requeue or unacked redelivery returns the identical message
with its attempt header unchanged, so `--tries` never trips and a job that dies before Laravel can release it
replays forever; add a `--max-jobs` or `--max-time` recycle and that is a crash loop on one message.
Derivation: `references/driver-facts.md`. Diagnosis: `references/failure-classes.md` class 8. Values:
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. Doctrine:
`alaa-reliability-sla references/20-retries.md`.

**4. Two timeout relationships bound duplicate execution.** `retry_after` is not one of them; it is inert on
this connection (`references/driver-facts.md`). Worker `--timeout` times the depth of the unacked window
stays below the broker's `consumer_timeout` — past it the broker closes the channel and requeues **every**
delivery in the window, not only the slow one. Pod `terminationGracePeriodSeconds` exceeds worker
`--timeout` plus the shutdown margin — below that, every rollout SIGKILLs a worker mid-job and replays the
delivery with its attempt count unchanged. Both values and the margin: the contract file above.

**5. The prefetch rule.** Prefetch count times p99 handler duration **is** the unacked window, and all of it
redelivers at once when a channel drops. Choose the count so that window is smaller than the redelivery
burst the fleet absorbs, and state the count and the measured p99 duration in the change. Passing
`--prefetch-count` explicitly is required: the package default of `1000` leaves the window unbounded in
practice. The contract file above requires every consumer to set an explicit prefetch; tuning belongs to
`/alaa-async-messaging`.

**6. Publisher confirms — a decision, not silence.** This driver never calls `confirm_select`, so a publish
reports success once the frame reaches the socket and a broker that dies before persisting it loses the
message while the application believes it succeeded. The decision: a request-path publish does not wait on a
confirm, and durability comes from the durable outbox row the contract file above already requires. The
outbox drain worker is the one place a confirm is required, because that contract forbids deleting an outbox
row before the broker acknowledges the publish and `basic_publish` is not an acknowledgement. How to add it,
and its cost: `references/driver-facts.md`.

**7. Broker unreachable on the request path.** A request-path publish never blocks the user-facing response
on broker recovery and never fails the business write; the outbox above is the mechanism. Doctrine:
`alaa-reliability-sla references/50-degradation.md`. Values: the contract file above. Driver mechanics
that change the answer — lazy connect, and one host chosen at random per connection with no retry inside a
publish call — are in `references/driver-facts.md`.

**8. The seam carries the trace.** The trace field travels as a constructor property inside the serialised
job payload, set at dispatch and read at the top of `handle()`, because this driver exposes no AMQP header
injection point; the `correlation_id` it already sets is the broker-side join key for the same message. Field
name: `/alaa-services-contract` (`$alaa-services-contract`). Whether carrying it is required:
`/alaa-observability-soc` (`$alaa-observability-soc`). Signals this seam uniquely produces, to be registered
rather than invented — queue depth, consumer count, unacked count, oldest-unacked age, redelivery rate,
worker restart rate — are named in `alaa-services-contract references/24-metric-registry.md` and levelled by
`/alaa-observability-soc`.

**9. Horizon is not the control plane for these workers.** `'worker' => 'default'` on the connection and
`RABBITMQ_WORKER` unset or `default` everywhere. Horizon is Redis-queue tooling; its dashboard, metrics and
supervisor semantics do not observe a RabbitMQ queue. Observe these workers through broker metrics, worker
logs and application metrics, plus `queue:monitor` as a ready-depth threshold alarm and nothing more
(`references/driver-facts.md`).

**10. Dead-lettering and delivery limits come from broker policies, never queue arguments.** A queue argument
is fixed at declare time and this driver never re-declares an existing queue, so an argument changed in
config does nothing to a queue that already exists; a policy applies to existing queues and reverts without a
deploy. Pre-create exchange, queue and binding in infrastructure or a release job before consumers scale.

**11. Every outbound call inside a handler carries a client timeout strictly below the worker `--timeout`**,
so the handler fails and releases rather than holding the delivery until the broker kills the channel. A
300-second HTTP call inside a 60-second job violates this. Values: the contract file above.

**12. Secrets never enter the repository.** No `.env`, private key, certificate, password or token in a
commit; every value comes from a Secret or a secret file.

**13. Redis touches inside jobs.** RabbitMQ is the transport; Redis never carries these jobs. Job middleware
backed by Redis (`RateLimited`, `WithoutOverlapping`, `Redis::throttle` funnels) has a defined outage
behaviour recorded in the change — the fail-closed discriminator is `/alaa-security-review`
(`$alaa-security-review`), and keys, TTL and the Redis-down fallback contract are
`alaa-data-layer references/50-redis-laravel-octane.md` (`$alaa-data-layer`). No cache or Redis read in a
provider `register()` or `boot()`, or a Redis outage stops workers from starting.

**14. Uniformity over local preference in job policy.** Use whichever form the repository already uses for
every job in it — attributes (`#[Tries]`, `#[Backoff]`, `#[Timeout]`, `#[FailOnTimeout]`) or properties and
methods. A repository that mixes both standardises on the attribute form and converts the rest in the same
change. Where queue or connection selection would otherwise repeat across dispatch sites, put it in central
`Queue::route(...)` rules.

# The one required test

**A redelivered message must not double-apply its side effect.** Every handler with a side effect has this
test; a change adding such a handler without it is incomplete.

Shape: run the job to completion, then run the **same payload with the attempt count unchanged** through the
same handler again — exactly what a requeue produces — and assert the side effect happened once. The
assertion is a count or a total: rows written, outbound calls made, ledger balance. "No exception was
thrown" is not the assertion, because the duplicate path throws nothing. Assert too that the second run
acked rather than released, so the test fails if someone "fixes" duplication by requeueing.

What makes this a test rather than a replay of the happy path, which layer it belongs at, and whether the
broker is real or faked: `/alaa-testing-strategy` (`$alaa-testing-strategy`)
`alaa-testing-strategy references/70-failure-mode-first.md` and
`alaa-testing-strategy references/30-doubles.md`. Pest and PHPUnit syntax comes from the
repository-local `pest-testing` skill, which this repository does **not** own and which can change between
runs — on conflict about what the test must prove, `/alaa-testing-strategy` wins and this rule stands
regardless of syntax. Real-infrastructure verification of the same property is step 3 of
`references/running-workers.md`.

# When NOT to use

- The decision is which broker to run at all — Kafka against RabbitMQ — or what the event topology and
  fan-out should be. Both are settled before any job exists.
- The queue runs on Redis with Horizon, or on any driver other than this RabbitMQ package.
- The work is broker cluster administration — nodes, quorum members, disk alarms, upgrades — rather than
  how a Laravel job behaves on a broker that is already running.
- The task is naming a queue, vhost, or exchange, or setting a retry, backoff, DLQ, or idempotency policy.
  The ownership boundary below names each owner.

# Ownership boundary

This skill owns one thing: the behaviour of Laravel jobs on **this** RabbitMQ driver. Below is owned
elsewhere, and the named owner wins on conflict.

- **The ten-point quality bar itself** — `alaa-project-constitution references/quality-bar.md`.
- **Failure behaviour doctrine** (retries, backoff, deadlines, breakers, degradation, the idempotency
  contract, error budgets) — `/alaa-reliability-sla` (`$alaa-reliability-sla`). **Every number** it implies —
  timeout, retry count, prefetch value, delivery limit, threshold, margin —
  `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
- **Names**: queue, exchange and vhost names and event-versus-command topology in
  `alaa-services-contract references/23-queue-and-exchange-registry.md`; log, event and metric names in
  `alaa-services-contract references/24-metric-registry.md` — `/alaa-services-contract`
  (`$alaa-services-contract`).
- **Observability requirement levels, gates and alerts** — `/alaa-observability-soc`
  (`$alaa-observability-soc`).
- **Messaging architecture**: transport choice, event design, fan-out, DLQ replay procedure, prefetch tuning
  — `/alaa-async-messaging` (`$alaa-async-messaging`). Retry and DLQ **strategy** is `/alaa-reliability-sla`,
  not this skill and not `/alaa-async-messaging`; earlier versions of this file mis-routed it.
- **Deployment**: chart keys, probes, rollout strategy and autoscaler shapes — `/alaa-k8s-helm`
  (`$alaa-k8s-helm`); runtime image contents including `ext-pcntl` — `/alaa-docker-production`
  (`$alaa-docker-production`); broker cluster, vhost and permission administration and Arvan defaults —
  `/caas-arvan-kuber` (`$caas-arvan-kuber`).
- **Correctness and testability**: what makes a test a test, layers, doubles, proof strength, flake —
  `/alaa-testing-strategy` (`$alaa-testing-strategy`).
- **Security**: fail-closed versus fail-open, threat classes, untrusted input — `/alaa-security-review`
  (`$alaa-security-review`); trusted headers and tenant derivation — `/alaa-trust-gateway-auth`
  (`$alaa-trust-gateway-auth`).
- **Clean code, SOLID and design-pattern selection** — `alaa-php-clean-code references/design-patterns.md`
  (`$alaa-php-clean-code`).
- **Complexity budgets, structure choice and the N+1 family inside handlers** —
  `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).
- **Long-lived worker hygiene, cross-request state and memory drift** — `/alaa-octane-performance`
  (`$alaa-octane-performance`). **Pre-implementation design pass** — `/alaa-system-design`
  (`$alaa-system-design`). **Generated wrappers and MSYS path conversion** —
  `/service-runtime-kit-governance` (`$service-runtime-kit-governance`). **Plan files and phasing** —
  `/alaa-workflow` (`$alaa-workflow`).

# Output contract

Report: files changed; the installed driver version and the grep that confirmed its monitor methods; each
config key changed and the behaviour it produces; the worker mode and why; the prefetch count with the
measured p99 handler duration behind it; the delivery limit and where its policy is set; the redelivery test
and its assertion; the rollback step; and every assumption, monitoring limitation and unresolved risk,
naming which are limits of this driver rather than of the change.
