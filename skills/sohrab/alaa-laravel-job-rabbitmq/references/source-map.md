# Source Map

Use this map when Laravel RabbitMQ driver behavior, Laravel 13 compatibility, queue monitor methods, worker modes, or broker topology may have changed.

## Source order

1. Repository truth:
   - `composer.json`, `composer.lock`, `config/queue.php`, `.env.example`, worker runtime files, deployment manifests, tests, logs, and installed package source under `vendor/`.
2. Pinned package snapshots in this skill:
   - Maintained fork snapshot: `references/forks/sohrabafard/9c8125f133cc13d49e7c08496fde5615919439e7`.
   - Upstream snapshot: `references/upstream/vyuldashev/9b8df5d4239128ed70b857249513edb30749e63b`.
   - Use the snapshot that matches the repository's declared package source.
3. Primary package sources:
   - Upstream repo: https://github.com/vyuldashev/laravel-queue-rabbitmq
   - Maintained fork: https://github.com/sohrabafard/laravel-queue-rabbitmq
   - Upstream PR #652: https://github.com/vyuldashev/laravel-queue-rabbitmq/pull/652
   - Issues list: https://github.com/vyuldashev/laravel-queue-rabbitmq/issues
4. Official Laravel and RabbitMQ sources:
   - Laravel queues: https://laravel.com/docs/13.x/queues
   - Laravel Horizon: https://laravel.com/docs/13.x/horizon
   - RabbitMQ docs: https://www.rabbitmq.com/docs
   - Dead-letter exchanges: https://www.rabbitmq.com/docs/dlx
   - Consumer prefetch: https://www.rabbitmq.com/docs/consumer-prefetch
   - Heartbeats: https://www.rabbitmq.com/docs/heartbeats
   - Quorum queues: https://www.rabbitmq.com/docs/quorum-queues
   - At-least-once dead lettering: https://www.rabbitmq.com/blog/2022/03/29/at-least-once-dead-lettering
5. Platform policy:
   - `caas-arvan-kuber` owns Arvan-specific Kubernetes defaults.
6. Community and StackOverflow material:
   - Troubleshooting only. Use it to understand symptoms or find search terms.
   - Never let it override package source, official Laravel docs, official RabbitMQ docs, or repo runtime evidence.

## Freshness triggers

Verify package source and official docs before acting when the task mentions:

- `latest`, `current`, `upgrade`, `Laravel 13`, `PHP 8.5`, `security`, `CVE`, upstream release, maintained fork, PR status, issue status, or package driver compatibility.
- `queue:monitor`, `pendingSize`, `delayedSize`, `reservedSize`, `creationTimeOfOldestPendingJob`, Horizon mode, `rabbitmq:consume`, `queue:work`, DLX/DLQ, quorum queues, prefetch, heartbeat, TLS, or failed reroute behavior.

## Small example

For RabbitMQ workers in this repository, keep the driver in default worker mode:

```php
'worker' => 'default',
```

Anti-pattern:

```php
'worker' => 'horizon',
```

Even if the package exposes Horizon support, this skill treats Horizon as Redis-queue tooling and requires RabbitMQ observability through broker metrics, app metrics, failed jobs, and DLQ signals.
