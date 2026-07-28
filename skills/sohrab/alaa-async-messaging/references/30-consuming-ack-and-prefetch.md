# Consuming: the acknowledgement point, prefetch, and worker lifecycle

Read this before writing or changing a consumer, before choosing a prefetch or concurrency value, and before
setting a worker's stop budget. It owns where a consumer acknowledges, what each acknowledgement route
means, how the two bounds are derived, and how a consumer behaves across a restart or a dropped connection.

## The acknowledgement point

**A consumer acknowledges after its receipt row and its business effect have committed, and never before.**
This is the kit's own ordering contract for `mqkit`: receipt and business effect commit first, broker
acknowledgement second.

The reason is the crash window, and it is asymmetric:

- **Ack first, commit second.** A crash in the window loses the message. The broker has been told the work
  is done, no redelivery will occur, and nothing in the system records that the work is owed. This failure
  is silent and permanent.
- **Commit first, ack second.** A crash in the window redelivers the message. The handler runs a second
  time, the receipt row's uniqueness constraint recognises the duplicate, and the effect happens once. This
  failure is visible in the duplicate counter and is already made safe by the redelivery rule.

**Automatic acknowledgement is never enabled on a consumer that changes state.** Auto-ack acknowledges on
delivery, before the handler has run at all, so every message in flight during a crash is lost — it is the
ack-first window widened to the whole handler.

## The three routes out of a handler

Every handler outcome takes exactly one of these, and the choice is made by the failure's class rather than
by its severity.

| Outcome | Route | What the broker does | Crash window |
|---|---|---|---|
| The work succeeded, or a duplicate was recognised | **ack** | removes the message | between commit and ack: redelivery, recognised as a duplicate |
| Transient failure — dependency unreachable, lock contention, timeout | **reject with requeue**, or let the delivery limit redeliver | redelivers, counting against the delivery limit | none: nothing committed |
| Permanent failure — the message can never succeed as written: schema violation, unknown type, referenced entity absent for good | **reject without requeue** | dead-letters it | none: nothing committed |

**A permanent failure is never requeued.** Requeuing it produces an immediate redelivery to the same or
another consumer, which fails identically and requeues again, and the loop consumes the whole consumer fleet
at the broker's redelivery rate. Classification and the DLQ route are `40-dead-letter-and-replay.md`.

**A handler never acknowledges a message it did not process in order to clear a backlog.** That is deletion
with extra steps, and it is indistinguishable afterwards from successful processing.

## Consumer-side deduplication

**A consumer writes a receipt row keyed by the message's idempotency key, in the same transaction as its
business effect, and a duplicate is recognised by the uniqueness constraint rejecting that insert.** A
duplicate increments a counter and does nothing else — no second effect, no error, no dead-letter.

- **The key comes from the message envelope, not from the message body's content.** A content-derived key
  cannot distinguish an honest redelivery from a genuine second request with identical content, so it
  suppresses real work.
- **The receipt lives in the same store as the effect.** In two stores they disagree: the receipt commits
  and the effect rolls back, and the redelivery is then refused forever.
- **A `SELECT` before the `INSERT` is not deduplication.** Two concurrent redeliveries both find nothing and
  both proceed; the constraint is the only component in the path that serialises.

Request-side idempotency doctrine — who generates a key, retention, and the in-flight case — is
`alaa-reliability-sla references/60-idempotency.md` — `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Prefetch

**Prefetch count multiplied by the p99 handler duration is the unacknowledged window: the amount of work
that redelivers at once when the channel drops.** Derive the count from that product, and state both the
count and the measured p99 in the change.

The procedure:

1. **Measure the handler's p99 duration** from `alaa_queue_message_duration_seconds`. An estimate is not a
   measurement, and handlers are routinely an order of magnitude slower than their authors expect.
2. **Choose the unacknowledged window the fleet can absorb as a single redelivery burst.** This is the real
   input: when a consumer's channel drops, everything unacknowledged is redelivered together.
3. **Set the count to that window divided by the p99 duration**, and never leave it at the library default.
   Package defaults are large — the Laravel RabbitMQ driver's is `1000` — which leaves the window unbounded
   in practice.
4. **Set it lower for an ordered or high-blast-radius queue**, where a redelivery burst is more expensive
   than the throughput the higher count buys.

**Raising prefetch is not a remedy for a slow consumer.** It moves the broker's bounded, durable queue into
the consumer's unbounded, volatile memory, where a restart loses all of it, and it starves other consumers
on the same queue because the broker will not redeliver messages already dispatched.

The specific value for a queue is `alaa-services-contract`'s; the derivation above is this file's. That
every consumer sets one explicitly is required by
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## Consumer concurrency

**A consumer sets an explicit concurrency bound, and its database pool maximum is set for the worker
process rather than inherited from the HTTP default.** Concurrency times per-handler connections is the
consumer's real footprint on the database, and a consumer fleet that inherits the HTTP pool default
silently doubles the fleet's connection count during exactly the backlog it was scaled up to drain.

**Scale a lane by adding consumers, not by widening one consumer's prefetch.** More consumers spread the
unacknowledged window across processes, so a single crash loses a fraction of it rather than all of it.

## Graceful stop and rolling restarts

**A worker's graceful-stop budget must exceed the longest handler's own deadline.** When the stop budget is
shorter, a rolling restart kills handlers mid-flight, and every one of those messages is redelivered — so a
routine deploy converts in-flight work into a redelivery burst, at the exact moment fewer consumers are
running to absorb it.

Two consequences: **give the handler an explicit deadline**, since a handler with no deadline makes the
correct stop budget unknowable; and **stop accepting new deliveries first, then finish in-flight work**, so
the drain is bounded by one handler's deadline rather than by the queue's depth.

The Go kit expresses shutdown in ordered phases against a fixed budget, and Laravel workers express it
through the worker command and its process supervisor. Neither expression is this file's ground: the rule is
the ordering between the two budgets. Laravel specifics are `/alaa-laravel-job-rabbitmq`
(`$alaa-laravel-job-rabbitmq`); container and Deployment expression are `/alaa-docker-production`
(`$alaa-docker-production`) and `/alaa-k8s-helm` (`$alaa-k8s-helm`).

## Reconnect

**A consumer reconnects with exponential backoff and full jitter, and never with a fixed delay.** Every
consumer in a fleet loses its connection at the same instant when the broker restarts, so a fixed delay
makes them all reconnect in the same instant and the broker refuses the whole fleet again.

**A reconnect redeclares the consumer's topology before consuming.** A queue or binding that was lost with
the connection otherwise leaves the consumer connected, healthy-looking, and receiving nothing.

**A consumer that cannot reconnect exits non-zero rather than idling.** An idle consumer holds its place in
the supervisor and reports nothing wrong, while its queue grows unattended; a process that exits is
restarted and its restart count is visible.

**Set an explicit heartbeat on the connection.** Without one, a connection dropped by an intermediary stays
open from the client's point of view and the consumer waits forever on a socket nothing will deliver to.
The heartbeat interval is a value: `alaa-services-contract`.

## Two things this file does not decide

The Laravel worker command, its flags, and driver-level delivery limits: `/alaa-laravel-job-rabbitmq`
(`$alaa-laravel-job-rabbitmq`). Retry counts, backoff curves and budgets as doctrine:
`/alaa-reliability-sla` (`$alaa-reliability-sla`).
