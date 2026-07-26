# Source map

Read this when deciding which source wins, or when a freshness trigger below fires.

## Source order, highest first

1. **Repository truth.** `composer.json`, `composer.lock`, `config/queue.php`, `.env.example`, worker
   runtime files, deployment manifests, tests, logs, and the installed package source under
   `vendor/vladimir-yuldashev/laravel-queue-rabbitmq/`. This is the only source that describes what is
   actually running.
2. **Pinned snapshots in this skill**, for when `vendor/` is empty or unreachable:
   `references/upstream/vyuldashev/9b8df5d4239128ed70b857249513edb30749e63b/` for the driver, publish path,
   config factories and the package's own `config/rabbitmq.php`;
   `references/forks/sohrabafard/9c8125f133cc13d49e7c08496fde5615919439e7/src/Consumer.php` for the consume
   loop. Pins: `references/upstream/UPSTREAM_COMMIT.txt`, `references/forks/FORK_COMMIT.txt`. A snapshot
   describes the pinned commit and nothing later, so a snapshot never settles a question about the installed
   version — `references/driver-facts.md` records what the snapshots can and cannot prove.
3. **Package source code over README examples**, when the two disagree. The README lags the code.
4. **Official Laravel and RabbitMQ documentation** over community material.
5. **Platform policy.** `/caas-arvan-kuber` (`$caas-arvan-kuber`) for Arvan Kubernetes defaults;
   `alaa-services-contract references/23-queue-and-exchange-registry.md` for every queue, exchange and vhost
   name.
6. **Community and StackOverflow material — troubleshooting only.** Use it to recognise a symptom or find
   search terms. It never overrides package source, official docs, or repository evidence.

There is no temporary-clone tier. A `.tmp/` clone inside the repository is not a source: it fails on a
read-only mount, it is invisible to review, and it has no pin. When `vendor/` is empty and the snapshots do
not answer the question, say so and check the installed version in an environment where `vendor/` exists.

## Freshness triggers

Verify against installed package source and official docs before acting when the task mentions any of:

- `latest`, `current`, `upgrade`, a Laravel or PHP version, `security`, `CVE`, an upstream release, a PR or
  issue status, or package driver compatibility.
- `queue:monitor`, `pendingSize`, `delayedSize`, `reservedSize`, `creationTimeOfOldestPendingJob`, Horizon
  mode, `rabbitmq:consume`, `queue:work`, DLX/DLQ, quorum queues, `x-delivery-limit`, prefetch, heartbeat,
  `consumer_timeout`, TLS, or failed reroute behaviour.

### Upstream signals to re-check when a trigger fires

This list rots. Treat every entry as a question to re-ask against the current issue tracker, never as a
current fact, and check the dates before quoting any of it.

- `#652` — Laravel 13 and PHP 8.5 CI coverage, `Consumer::stop()` compatibility, and the `RabbitMQQueue`
  monitor methods. The four methods are present in installed `v15.0.0`; see `references/driver-facts.md`.
- `#661` — `Worker::$currentJob` became public in Laravel 13.7 and `runJob()` may reset it, which starved
  throughput in the consume loop. Installed `v15.0.0` tracks the job in a local variable instead; the
  pinned fork snapshot still has the property form.
- `#644` — worker queue and binding creation expectations mismatch.
- `#634` — maintenance-mode channel exceptions (`CONNECTION_FORCED`); see failure class 4.
- `#615` — DLQ setup confusion in real deployments.
- `#601` — quorum plus delayed dead-letter safety.
- `#603` — closed; the consume command gained `--json`.
- `#562` — closed; multiple queues are for `queue:work`, not `rabbitmq:consume`.
- `#591` — closed; heartbeat behaviour in long-lived producer contexts.

## URLs

The single canonical list for this skill; no other file repeats it.

- Package: https://github.com/vyuldashev/laravel-queue-rabbitmq
- Package README: https://github.com/vyuldashev/laravel-queue-rabbitmq/blob/master/README.md
- Issues: https://github.com/vyuldashev/laravel-queue-rabbitmq/issues
- PR 652: https://github.com/vyuldashev/laravel-queue-rabbitmq/pull/652
- Laravel queues: https://laravel.com/docs/13.x/queues
- RabbitMQ docs: https://www.rabbitmq.com/docs
- Dead-letter exchanges: https://www.rabbitmq.com/docs/dlx
- Consumer prefetch: https://www.rabbitmq.com/docs/consumer-prefetch
- Heartbeats: https://www.rabbitmq.com/docs/heartbeats
- Quorum queues, including `delivery-limit`: https://www.rabbitmq.com/docs/quorum-queues
- At-least-once dead lettering: https://www.rabbitmq.com/blog/2022/03/29/at-least-once-dead-lettering
- Consumer acknowledgement timeout: https://www.rabbitmq.com/docs/consumers
