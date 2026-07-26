# Driver facts: verified, asserted, and what to check yourself

Read this when a task names a driver version, `queue:monitor`, a monitor method, `retry_after`, a package
default, or a config key you are about to trust.

## The version claim, resolved

**Verified 2026-07-26** against an installed package in a consuming repository
(`vendor/vladimir-yuldashev/laravel-queue-rabbitmq`, declared `"^15.0"`, locked `v15.0.0`, source ref
`fd685fa1a890b82011e9cf25d990e14221c395ad`): all four Laravel 13 monitor methods are defined on
`RabbitMQQueue` with the bodies quoted in `references/fork-divergence.md`; `Consumer::stop()` takes the
third stop-reason parameter; `composer.json` requires `"illuminate/queue": "^10.0|^11.0|^12.0|^13.0"`.

**Asserted, not verified — do not restate as fact:** that every release tagged `v15.0.0` or newer carries
these methods, or that they arrived in `15.0.0` rather than earlier. Nothing shipped here substantiates it.
The pinned upstream snapshot at `9b8df5d4` contains **none** of the four, its `CHANGELOG-14x.md` stops at
`14.0.0` with `[unreleased]` empty, and its `composer.json` aliases `dev-master` to `13.0-dev`. The offline
path proves the methods were absent at `9b8df5d4`; it cannot say which release added them.

**Check before relying on it**, in the repository, before changing worker or monitor behaviour:

```
grep -c 'function pendingSize\|function delayedSize\|function reservedSize\|function creationTimeOfOldestPendingJob' \
  vendor/vladimir-yuldashev/laravel-queue-rabbitmq/src/Queue/RabbitMQQueue.php
grep -n 'public function stop' vendor/vladimir-yuldashev/laravel-queue-rabbitmq/src/Consumer.php
```

Four hits and a three-parameter `stop()` means compatible. Fewer than four means `queue:monitor` fails with
a missing-method error on that connection, and the fix is a package upgrade, never a fork override.

## `retry_after` is inert on this connection

Verified in installed `v15.0.0` and Laravel 13: `retry_after` is read by the Beanstalkd, Database and Redis
connectors only. The RabbitMQ driver's `src/` never mentions it, and neither does `Illuminate\Queue\Worker`,
`WorkerOptions`, or `WorkCommand`. This driver has **no visibility timeout**: a delivery stays unacked
until `ack()`, and the broker redelivers only when the channel or connection drops. So `--timeout` below
`retry_after` protects nothing here and any duplicate-execution reasoning built on it is wrong; the two
timeout relationships that do decide it are stated once, in `SKILL.md`. Keep `retry_after` set anyway, so a
later switch of `QUEUE_CONNECTION` to `database` or `redis` is not silently unbounded.

## Why a requeue does not advance the attempt count

The derivation behind the delivery-limit constraint in `SKILL.md`. Verified against installed `v15.0.0`:

- `RabbitMQQueue::createMessage()` writes the attempt count into the AMQP header `laravel.attempts` at
  publish time. `RabbitMQJob::attempts()` returns that header plus one.
- `RabbitMQJob::release()` is the only writer: it calls `laterRaw(..., $this->attempts())` to republish a
  **new** message and then acks the original. `delete()` acks. `markAsFailed()` calls
  `reject($job)` with requeue defaulting to false, which is what lets a DLX receive it.
- `RabbitMQQueue::close()` is the single requeue site:
  `if (isset($this->currentJob) && ! $this->currentJob->isDeletedOrReleased()) { $this->reject($this->currentJob, true); }`
  and `reject()` maps straight to `basic_reject($deliveryTag, $requeue)`.
- `RabbitMQConnector` registers a `WorkerStopping` listener that calls `$queue->close()`.
  `RabbitMQQueue::$currentJob` is assigned only in `pop()`, the `basic_get` path, so this requeue fires in
  `queue:work` mode and not in consume mode, where the loop tracks its job in a local variable.
- Laravel's SIGALRM job-timeout handler calls `kill()`, which fires `WorkerStopping`. It first calls
  `markJobAsFailedIfWillExceedMaxAttempts`, which fails the job only when the count already reached
  `--tries`.

Put together: a `basic_reject(requeue: true)` and an unacked redelivery both return the identical frames,
so `laravel.attempts` is unchanged, `attempts()` returns the same number on every replay, `--tries` never
trips, and the job never reaches `failed_jobs` or the DLX. Only a broker-side `delivery-limit` counts
redeliveries, which is why it is the one thing that ends the loop.

## Monitor-method behaviour

`pendingSize()` delegates to `size()`, a passive `queue_declare` on a temporary channel returning the
broker's ready count. `delayedSize()` and `reservedSize()` return literal `0`;
`creationTimeOfOldestPendingJob()` returns literal `null`. So `queue:monitor rabbitmq:default --max=<n>` is
a ready-depth threshold alarm and nothing more — delayed, reserved and oldest-message questions are
answered from broker metrics.

## Package defaults that differ from what the flags suggest

From `src/Console/ConsumeCommand.php`:

| Flag | Default | Why it matters |
| --- | --- | --- |
| `--tries` | `1` | One attempt then failed. Always pass explicitly. |
| `--prefetch-count` | `1000` | Makes the unacked window in `SKILL.md` effectively unbounded. |
| `--prefetch-size` | `0` | No byte limit, which is the correct value. |
| `--timeout` | `60` | Two roles at once: the SIGALRM job timeout via `registerTimeoutHandler()`, and the AMQP `wait()` timeout in the consume loop. |
| `--memory` | `128` | MB; recycles the process, does not fail the job. |
| `--sleep` | `3` | Applies only to a wait cycle that consumed nothing. |
| `--max-jobs` / `--max-time` | `0` | Off; no recycling unless set. |

`--queue` help text says it outright: "there is no support for multiple queues".

## Config keys the driver actually reads

`QueueConfigFactory::make()` reads `queue`, `after_commit`, and from `options.queue` exactly `job`,
`prioritize_delayed`, `queue_max_priority`, `exchange`, `exchange_type`, `exchange_routing_key`,
`reroute_failed`, `failed_exchange`, `failed_routing_key`, `quorum`. Anything else under `options.queue` is
stored by `setOptions()` and never reaches the broker, so an invented `options.queue.x-delivery-limit` is
silently ignored.

`getQueueArguments()` emits at most four arguments: `x-max-priority` (only when `prioritize_delayed` is
true **and** `quorum` is false), `x-dead-letter-exchange` plus `x-dead-letter-routing-key` (only when
`reroute_failed` is true), and `x-queue-type: quorum`. There is no `x-delivery-limit`, no `x-message-ttl`
and no `x-max-length` on the main queue. That is the mechanical reason the DLX and delivery-limit rules in
`SKILL.md` are policy-only rather than a preference: the driver cannot express them.

`ConfigFactory::getHostFromConfig()` does `Arr::first(Arr::shuffle($config['hosts']))` — one host chosen at
random per connection, no failover inside a single publish or consume call. A multi-host `hosts[]` spreads
processes across brokers; it does not retry a failed connect.

## Publish-path mechanics

- **No publisher confirms.** `publishBasic()` calls `basic_publish` and nothing else; `confirm_select`,
  `set_ack_handler` and `wait_for_pending_acks` appear nowhere in installed `v15.0.0` `src/`. A publish
  therefore returns as soon as the frame reaches the socket. To add a confirm where `SKILL.md` requires one
  (the outbox drain worker), extend `RabbitMQQueue`, call `confirm_select` once on the channel, and wait for
  pending acks after publishing. Never edit `vendor/`. Cost: publish throughput becomes bound to the
  broker's fsync rate, which is why only the drain worker pays it.
- **Lazy connection.** With `lazy` true, which is the default, the TCP connect happens on the first publish
  in the process. A request therefore pays `connection_timeout` on a cold worker or a cold Octane worker,
  not the heartbeat interval.
- **`bulk()`** loops `bulkRaw()` then calls `publish_batch()`, so a batch is one flush and not one
  round trip per job — but it is still unconfirmed, and a failure mid-batch gives no per-message outcome.
- **Trace propagation.** `createMessage()` sets AMQP `correlation_id` from the payload `id` and sets
  `application_headers` to exactly `{laravel: {attempts: N}}`. `pushRaw()` reads `$options` only for
  `attempts`, `exchange`, `exchange_type` and `delay`. There is no AMQP header injection point, which is why
  `SKILL.md` puts the trace field in the job payload.

## Package commands that exist

Topology: `rabbitmq:exchange-declare`, `rabbitmq:queue-declare`, `rabbitmq:queue-bind`,
`rabbitmq:queue-delete`, `rabbitmq:queue-purge`. Worker: `rabbitmq:consume`.
