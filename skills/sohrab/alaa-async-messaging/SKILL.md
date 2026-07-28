---
name: alaa-async-messaging
description: "RabbitMQ message-plane architecture for the Ala fleet: the seam between a database commit and a published message, the transactional outbox and its operational surface, publisher confirms, the acknowledgement point, prefetch and consumer concurrency, dead-letter topology, and the DLQ replay procedure. Use it when adding or reviewing a publisher, a consumer, an outbox relay, a queue or exchange declaration, a dead-letter route, a redelivery or replay decision, or a live message-plane incident, and when deciding whether a fact must survive the broker being unreachable. Do not use it for Laravel driver mechanics such as config/queue.php keys or worker commands, which are /alaa-laravel-job-rabbitmq; for retry, backoff, deadline or idempotency doctrine, which is /alaa-reliability-sla; for queue, exchange, metric and event names or any platform value, which are /alaa-services-contract; or for a service that has no broker lane."
---

# Alaa Async Messaging

RabbitMQ is the only broker this fleet runs. This skill owns the seam between a database transaction and a
message on it: how a fact leaves a committed transaction, when a consumer acknowledges, how many deliveries
it holds unacknowledged, where a failed message goes, and how it is replayed. One property holds through
every failure below — no committed fact is lost, no user-facing request waits on broker recovery, and no
redelivery produces a second business effect.

## Gate — does this service have a broker lane

Read the service's configured lanes first. `alaa-go-chi docs/CONSUMERS.md:23` runs `wa-api` with no `mqkit`
and no `outboxkit`: no configured broker connection means no message plane, so say so and stop rather than
adding a broker for a rule to apply to. `tusd` is the mirror — a broker-free upload plane that still runs an
outbox dispatched to RabbitMQ from a separate command.

## Hard constraints

1. **Every handler is safe to run twice, and the guarantee is a uniqueness constraint in the same store as
   the effect.** Delivery is at-least-once, and a check in code has a window that concurrency hits.
2. **Every consumer sets an explicit prefetch and concurrency bound at its construction site.** A library
   default holds unbounded unacknowledged deliveries, stranding the queue's working set in one process.
3. **A consumer commits its receipt row and business effect first, and acknowledges second.** A crash between
   ack and commit loses the message; the reverse order only redelivers, which rule 1 has made safe.
4. **Every declared queue declares a dead-letter target in the same change, with redelivery bounded by a
   delivery limit.** Without both, a poison message loops forever or is dropped, and both look healthy.
5. **A message is published only after the transaction that made its fact true commits, and a fact that must
   survive an unreachable broker goes to a durable outbox row inside that transaction.** Publishing inside it
   exposes a row that may roll back; publishing after commit without the row loses the fact on a crash.
6. **Every exchange, queue and routing-key name comes from `alaa-services-contract
   references/23-queue-and-exchange-registry.md`, registered before the declaring code merges.** An
   unregistered queue is one nobody drains, and it grows until the broker refuses publishes for the vhost.
7. **A message body is untrusted input: validate it against a schema, and take tenant, actor and scope from
   it only when no trusted source carries them.** The broker authenticates the connection, never the payload.

## References — read the row you match

| You are about to … | Read |
|---|---|
| choose event versus command, or name a broker object | `references/10-transport-and-topology.md` |
| publish, or tune an outbox relay | `references/20-publishing-and-the-outbox.md` |
| write a consumer, set prefetch, or place its ack | `references/30-consuming-ack-and-prefetch.md` |
| route a dead letter, or replay a DLQ | `references/40-dead-letter-and-replay.md` |
| diagnose a stall, backlog, duplicate, stuck row, or filling DLQ | `references/50-failure-classes.md` |
| instrument a publisher, consumer or relay | `references/60-telemetry-and-proof.md` |
| work a Laravel queue plane, or weigh Horizon against RabbitMQ | `references/70-laravel-redis-and-horizon.md` |
| repeat a version-sensitive claim about RabbitMQ or the kit | `references/90-source-map.md` |

`references/queues-best-practices.md` is a content-free redirect, not a ninth reference.

## When not to use this skill, and what owns each thing instead

- Retry, backoff, deadline, breaker, degradation and request-side idempotency, as doctrine carrying no Ala
  value: `/alaa-reliability-sla` (`$alaa-reliability-sla`).
- Every broker, metric, event and error-code **name**, and every platform **value**:
  `/alaa-services-contract` (`$alaa-services-contract`).
- Laravel driver mechanics — `config/queue.php`, worker commands, `queue:work` versus `rabbitmq:consume`:
  `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`); on conflict, mechanics there, architecture here.
- Event emission layer and timing: `/alaa-laravel-architecture` (`$alaa-laravel-architecture`). Outbox claim
  query: `/alaa-data-layer` (`$alaa-data-layer`). Telemetry levels: `/alaa-observability-soc`
  (`$alaa-observability-soc`). Fail-closed controls: `/alaa-security-review` (`$alaa-security-review`).
  Quality bar: `/alaa-project-constitution` (`$alaa-project-constitution`). Model and effort:
  `/alaa-prompting-guide` (`$alaa-prompting-guide`).
- A kit capability that does not exist: file
  `alaa-go-chi-development assets/templates/kit-change-request.md` and stop —
  `/alaa-go-chi-development` (`$alaa-go-chi-development`).

## Required tests

Both ship with every change to a consumer or dead-letter route; assertions in `references/60-telemetry-and-proof.md`.

- **A redelivery test** delivers one message twice to the real handler and asserts one business effect and
  one receipt row. Idempotency established by inspection is not established.
- **A dead-letter test** fails the handler past the delivery limit and asserts the message lands on
  `<queue>.dlq` with key `<live-key>.failed`. An unexercised dead-letter route is a hope.

## Gate script

```sh
sh scripts/check-consumer-bounds.sh --root .
```

Exit **0** no findings. Exit **1** findings with file and line: resolve every one before reporting the change
complete. Exit **2** could not determine — no broker lane or no recognisable declaration: run the three
checks by hand and report each, because exit 2 is never a pass. Detection is narrow like the kit's
pooled-lane analyzer, so a constant or a wrapper escapes it; `--self-test` runs the fixtures.

## What you report

Report each, or that it does not apply and why: the prefetch set and the measured handler p99 behind it; the
acknowledgement route per outcome — ack, requeue, reject-without-requeue; the dead-letter target for every
queue touched; for a replay, the precondition proving the cause was gone and the count replayed; and every
absent kit capability and what replaced it.
