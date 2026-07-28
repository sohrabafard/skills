# The Laravel queue plane: Redis, Horizon, and after-commit dispatch

Read this when working on a Laravel service's queue plane, when choosing between a Redis-backed queue and
RabbitMQ for a job, or when making a dispatch happen after a transaction commits. Driver mechanics — the
`rabbitmq` connection block in `config/queue.php`, worker command flags, the `queue:work` versus
`rabbitmq:consume` decision, and driver-level delivery limits — are `/alaa-laravel-job-rabbitmq`
(`$alaa-laravel-job-rabbitmq`), and on conflict that skill decides them.

## Horizon is a Redis tool, and it does not monitor RabbitMQ

**Laravel Horizon is designed for Redis-backed queues and depends on Redis operationally.** It stores its
metadata in Redis and reads Redis queue structures directly.

**Horizon is not a process manager or a monitor for RabbitMQ queues.** A service running RabbitMQ for jobs
and Horizon for its dashboard has no visibility into the RabbitMQ plane at all, while the dashboard makes it
look as though it does — which is worse than having no dashboard, because it answers the question wrongly
instead of not answering it.

**A service whose jobs run on RabbitMQ monitors them with broker metrics and the registered
`alaa_queue_*` family**, per `60-telemetry-and-proof.md`, and with dead-letter routing, bounded redelivery
and idempotent handlers per this skill's other references. Horizon contributes none of that.

**A service that wants Horizon's ergonomics puts the subset of jobs it wants Horizon to manage on a Redis
queue**, deliberately, and accepts that those jobs get Redis semantics rather than broker semantics.

## Running both planes at once

Running Redis-with-Horizon and RabbitMQ in the same service is allowed, and it is allowed only when the
routing is explicit.

- **Route per job or per queue, never by a single global `QUEUE_CONNECTION`.** One global connection with two
  planes present produces silent misrouting: a job lands on the wrong plane, runs, and nothing distinguishes
  it from correct behaviour until the plane it should have used is drained and empty.
- **Run separate worker fleets, one per plane.** A single fleet consuming both cannot be scaled, restarted
  or bounded independently, so a backlog on one plane starves the other.
- **State which job classes and which queues belong to which plane, in the service's own repository
  documentation.** The routing is otherwise recoverable only by reading every job class, and the reader who
  needs it is mid-incident.
- **Keep the retry, backoff and timeout policy consistent across both planes.** Two policies for one service
  means the same failure behaves differently depending on which plane the job happened to land on, and the
  difference is invisible in the code that dispatched it.

## Redis-queue timeout alignment

**On a Redis-backed queue, the worker's job timeout is set strictly less than the connection's
`retry_after`.** When the timeout is greater than or equal to `retry_after`, the queue makes the job
available to a second worker while the first is still running it, so the job executes twice with no failure
anywhere to explain it. The margin between the two values is `alaa-services-contract`'s; that timeout is the
smaller of the two is this file's rule.

**A worker sets an explicit memory limit and a maximum job or time budget before it recycles.** A long-lived
PHP worker accumulates memory across jobs, and a worker killed by the operating system's out-of-memory
handler drops its in-flight job with no graceful stop, which is the redelivery burst described in
`30-consuming-ack-and-prefetch.md`.

## After-commit dispatch

**A job or event that reads database state written by the surrounding transaction is dispatched after that
transaction commits.** Dispatched inside the transaction, the job can begin on another process before the
commit lands and will read a row that does not exist yet — or that never will, if the transaction rolls
back.

Two mechanisms express it in Laravel, and both are acceptable for a message whose loss is tolerable:

- Mark the individual dispatch as after-commit at the call site.
- Set the queue connection to dispatch after commit for every job on that connection, which makes the
  behaviour the default and removes the per-call-site decision. Use this form once the service has more than
  three dispatch sites, because a decision repeated at every site is one an author eventually forgets, and
  the forgotten one is invisible until a consumer reads a row that has not committed.

**Neither mechanism makes the message durable.** The process can die between the commit and the dispatch,
and nothing then records that the message was owed. A fact that must reach a consumer at least once goes to
a durable outbox row inside the transaction instead — `20-publishing-and-the-outbox.md`.

Which layer emits a domain event, and the emission point relative to the transaction, are
`alaa-laravel-architecture references/30-events-and-outbox-seam.md` — `/alaa-laravel-architecture`
(`$alaa-laravel-architecture`).

## Payload size

**Pass identifiers and business keys in a message, not serialized models or large documents.** A serialized
model is a snapshot that is stale by the time the handler runs, it inflates every copy the broker holds and
redelivers, and it breaks on the first change to the model's shape while old messages are still in the
queue.

## What belongs elsewhere

Redis as a cache, a lock or a rate limiter, and Redis behaviour under Octane: `/alaa-data-layer`
(`$alaa-data-layer`). Worker lifecycle under Octane, and request-state leakage across jobs:
`/alaa-octane-performance` (`$alaa-octane-performance`). Job class shape, dependency injection and
repository access inside a handler: `/alaa-php-clean-code` (`$alaa-php-clean-code`).
