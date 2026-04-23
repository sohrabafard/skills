# Source Map

Use this map when queue, event, broker, retry, DLQ, or current runtime behavior may be version-sensitive.

## Source order

1. Repository truth:
   - `composer.json`, queue config, Horizon config, Kafka/RabbitMQ client packages, worker commands, runtime/deploy files, tests, logs, and runbooks.
2. Official Laravel sources:
   - Queues: https://laravel.com/docs/13.x/queues
   - Events: https://laravel.com/docs/13.x/events
   - Horizon: https://laravel.com/docs/13.x/horizon
   - Scheduling: https://laravel.com/docs/13.x/scheduling
3. Official broker sources:
   - RabbitMQ docs: https://www.rabbitmq.com/docs
   - RabbitMQ dead-letter exchanges: https://www.rabbitmq.com/docs/dlx
   - RabbitMQ consumer prefetch: https://www.rabbitmq.com/docs/consumer-prefetch
   - RabbitMQ heartbeats: https://www.rabbitmq.com/docs/heartbeats
   - RabbitMQ quorum queues: https://www.rabbitmq.com/docs/quorum-queues
   - Apache Kafka documentation: https://kafka.apache.org/documentation/
   - Redis docs: https://redis.io/docs/latest/
4. Package source:
   - Installed package source under `vendor/` outranks README snippets when driver behavior matters.
   - For Laravel RabbitMQ transport specifics, switch to `alaa-laravel-job-rabbitmq`.
5. Community posts, StackOverflow, and blog posts:
   - Use only for troubleshooting symptoms or locating official terms.
   - Do not use as authority for broker safety, Horizon support, retry semantics, or current version behavior.

## Freshness triggers

Verify official docs or package source before acting when the task mentions:

- `latest`, `current`, `upgrade`, `security`, `CVE`, driver compatibility, Horizon, RabbitMQ, Kafka, Redis, quorum queues, DLX/DLQ, retries, backoff, prefetch, heartbeat, or exactly-once behavior.
- New worker commands, new broker major versions, new Laravel queue attributes/events, or runtime image changes.

## Small example

For DB-coupled Laravel jobs, dispatch after commit:

```php
ProcessOrder::dispatch($order->id)->afterCommit();
```

Anti-pattern:

```php
ProcessOrder::dispatch($order->id);
```

If the job can run before the surrounding transaction commits, workers may observe missing or stale data.
