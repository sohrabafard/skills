---
name: alaa-laravel-job-rabbitmq
description: "Production skill for Laravel jobs on RabbitMQ via vladimir-yuldashev/laravel-queue-rabbitmq, including Laravel 13 temporary-fork compatibility, accurate config, safe worker modes, retries/DLQ/idempotency, and Kubernetes/Arvan-ready operations."
---




# Purpose
Provide production-grade guidance for Laravel queued jobs on RabbitMQ using `vladimir-yuldashev/laravel-queue-rabbitmq`, with:
- predictable throughput (queue split, prefetch/concurrency tuning),
- correctness (idempotency, `after_commit`, timeout/retry alignment),
- resilience (bounded retries, DLQ strategy, graceful restarts),
- operational safety on Kubernetes and Arvan CaaS.

This skill complements:
- `alaa-async-messaging` (architecture + generic RabbitMQ/Kafka guidance)
- `alaa-octane-performance` (Octane long-lived worker hygiene)
- `alaa-observability-soc` (logs/metrics/runbooks)
- `alaa-workflow` (plan file + phased execution)

# When to use
- You want Laravel `ShouldQueue` jobs processed by RabbitMQ (AMQP).
- You deploy web/worker/scheduler in containers and need safe rollouts.
- You need high-SLA patterns (idempotency, retries, DLQ, graceful stop).

## When NOT to use
- do not use this skill for broker-cluster administration or generic event-stream design that belongs to broader async architecture decisions
- do not assume Horizon is the control plane for RabbitMQ workers in this repository
- do not skip Laravel queue, RabbitMQ, or deployment-specific source-of-truth checks when compatibility is version-sensitive

# Non-goals
- Full broker platform engineering (cluster topology/operator lifecycle) beyond app-facing requirements.
- Event-stream architecture design (see `alaa-async-messaging` for Kafka-first decisions).

# Source-of-truth order
Use sources in this order when generating or reviewing changes.

1) Maintained Laravel 13 / PHP 8.5 fork snapshot inside this skill:
   - Root: `references/forks/sohrabafard/9c8125f133cc13d49e7c08496fde5615919439e7`
   - `src/Consumer.php`
   - `src/Queue/RabbitMQQueue.php`
   - `composer.json`
   - `.github/workflows/tests.yml`
   - `CHANGELOG-14x.md`
   - `README.md`

2) Pinned upstream snapshot inside this skill (works even when `vendor/` is empty):
   - Root: `references/upstream/vyuldashev/9b8df5d4239128ed70b857249513edb30749e63b`
   - `src/Console/ConsumeCommand.php`
   - `src/Queue/RabbitMQQueue.php`
   - `src/Queue/QueueConfigFactory.php`
   - `src/Queue/Connection/ConfigFactory.php`
   - `src/Queue/QueueFactory.php`
   - `README.md`
   - `CHANGELOG-14x.md`, `CHANGELOG-13x.md`

3) Installed package in runtime project (if present):
   - `vendor/vladimir-yuldashev/laravel-queue-rabbitmq/...`

4) Temporary clone fallback (if present):
   - `.tmp/laravel-queue-rabbitmq/...`

5) Upstream PR/issues (open + closed) for compatibility and operational edge cases:
   - PR `#652` for Laravel 13 queue monitor compatibility

6) Official docs:
   - Laravel Queue docs (`after_commit`, `retry_after`, `--timeout`)
   - RabbitMQ docs (DLX policy, prefetch, heartbeats, quorum queue behavior)

7) Repository policy:
   - `caas-arvan-kuber` is authoritative for Arvan-specific constraints.

If the repository targets Laravel 13 and upstream stable has not yet released the required compatibility, prefer a stable tag from the maintained fork over a local path repository or an untagged branch.
If local snapshot and runtime package differ, prefer the snapshot that matches the repository's declared driver source (maintained fork tag vs upstream release) and note the mismatch explicitly.

If sources conflict:
- maintained fork snapshot > older upstream snapshot for Laravel 13 / PHP 8.5 work until upstream stable catches up,
- package source code > README examples,
- official Laravel/RabbitMQ docs > community assumptions,
- Arvan policy wins for deployment defaults in this repository.

# Upstream facts you must respect
1) Worker modes:
- `queue:work` uses `basic_get` and supports multiple queues.
- `rabbitmq:consume` uses `basic_consume`, is generally faster, and does NOT support multiple queues in one process.
2) Consume command supports flags such as:
- `--prefetch-count`, `--prefetch-size`, `--max-priority`, `--json`.
3) Horizon policy in this repository:
- Even if the package offers a Horizon mode, this skill forbids Horizon for RabbitMQ workers.
- RabbitMQ workers must run with `worker=default` and be monitored via broker/app metrics instead.
4) Queue config supports:
- exchange routing keys, failed reroute settings, queue quorum flag, heartbeat, TLS options, network protocol, and lazy connection.
5) Laravel 13 queue monitor compatibility:
- `queue:monitor` expects `pendingSize`, `delayedSize`, `reservedSize`, and `creationTimeOfOldestPendingJob` on the queue driver.
- The maintained fork snapshot in this skill implements these methods.
- Current maintained behavior is broker-backed `pendingSize()` plus conservative `0`, `0`, and `null` for delayed/reserved/oldest metrics.
6) Topology commands are available:
- `rabbitmq:exchange-declare`
- `rabbitmq:queue-declare`
- `rabbitmq:queue-bind`
- `rabbitmq:queue-delete`
- `rabbitmq:queue-purge`

# Temporary fork policy for multi-service estates
- Prefer one tagged maintained fork reused across services instead of copying the driver into each Laravel app.
- Keep the Composer package name unchanged and override only the repository source while upstream stable lags.
- Once upstream ships a stable release with the same compatibility, remove the VCS override and refresh lockfiles back to upstream.

# Hard constraints
- Never commit secrets (`.env`, private certs, passwords, tokens).
- Prefer minimal, reversible diffs; avoid unrelated refactors.
- Terminal snippets and commands must be English.
- Assume at-least-once delivery; handlers MUST be idempotent.
- Keep `--timeout` lower than queue connection `retry_after`.
- Prefer broker policies (DLX, routing, limits) over hardcoded queue arguments where possible.
- Do NOT use Horizon for RabbitMQ workers in this repository.
- Do not duplicate app-local driver copies across services when one tagged maintained fork can be shared safely.
- For Arvan targets in this repo:
  - container resources are mandatory and should keep requests==limits by default,
  - secret values go in secret files or existing Secrets,
  - worker scaling is explicit (manual/HPA/KEDA by policy), not guessed.

# Laravel 13 queue-integration notes
- Keep Laravel-side queue behavior aligned with the Laravel 13 queue docs for routing, retries, timeouts, and failure handling.
- When queue or connection selection would otherwise be duplicated at dispatch sites, prefer central `Queue::route(...)` rules.
- For job-local policy, prefer declarative attributes such as `#[Tries]`, `#[Backoff]`, `#[Timeout]`, and `#[FailOnTimeout]` when they keep intent clearer than scattered properties, but preserve repository style if it already standardizes on methods or properties.
- If the repository listens to queue events, update upgrade reviews for `JobAttempted::$exception` and `QueueBusy::$connectionName`.
- If the repository uses `php artisan queue:monitor`, verify the driver source exposes Laravel 13 monitor methods before rollout.
- In the maintained fork snapshot for this skill, `pendingSize()` is meaningful while delayed/reserved/oldest monitor values remain conservative and should not replace broker metrics.

# Decision matrix
1) Use `queue:work` when:
- you need multi-queue priority lists (`high,default`),
- you want standard Laravel worker behavior,
- you prefer fewer operational differences.
2) Use `rabbitmq:consume` when:
- you run one queue per deployment/process group,
- you need stronger throughput tuning via consume prefetch options,
- you can operate separate worker fleets per queue.
3) Do not select Horizon mode for RabbitMQ:
- `RABBITMQ_WORKER` must remain `default`,
- avoid Horizon-specific assumptions in runbooks and observability.

# Step 1 — Install the driver
Install and pin intentionally:
- `composer require vladimir-yuldashev/laravel-queue-rabbitmq`
- For Laravel 13 repositories, keep the driver on the newest stable Laravel 13-compatible release and reconcile config keys against the upstream changelog and package source.
- If upstream stable has not released the needed Laravel 13 / PHP 8.5 compatibility yet, use a tagged maintained fork instead of a path repository or app-local driver copy.
- Keep the Composer package name unchanged and override only the repository source in `composer.json`:

```json
{
  "repositories": [
    {
      "type": "vcs",
      "url": "https://github.com/sohrabafard/laravel-queue-rabbitmq"
    }
  ]
}
```

- Then install a stable tag from that fork, for example:
  - `composer require vladimir-yuldashev/laravel-queue-rabbitmq:<stable-tag> --with-all-dependencies`
- Once upstream stable ships the same compatibility, remove the VCS override and update the lockfile back to upstream.
- Keep package major versions controlled during release windows.
- Ensure `ext-pcntl` is available for full worker behavior in container/runtime images.

# Step 2 — Configure `config/queue.php`
Add an explicit `rabbitmq` connection with source-accurate keys:

```php
'rabbitmq' => [
    'driver' => 'rabbitmq',
    'queue' => env('RABBITMQ_QUEUE', 'default'),
    'connection' => env('RABBITMQ_CONNECTION_TYPE', 'default'),

    'hosts' => [
        [
            'host' => env('RABBITMQ_HOST', '127.0.0.1'),
            'port' => (int) env('RABBITMQ_PORT', 5672),

            // Accept both env schemas:
            'user' => env('RABBITMQ_USER', env('RABBITMQ_USERNAME', 'guest')),
            'password' => env('RABBITMQ_PASSWORD', env('RABBITMQ_PASS', 'guest')),
            'vhost' => env('RABBITMQ_VHOST', '/'),
        ],
    ],

    // Keep default worker mode for RabbitMQ. Do NOT set horizon.
    'worker' => 'default',
    'after_commit' => (bool) env('QUEUE_AFTER_COMMIT', true),

    // Keep lazy connections enabled for CLI workers; disable only if you must:
    'lazy' => (bool) env('RABBITMQ_LAZY', true),
    'secure' => (bool) env('RABBITMQ_SECURE', false),
    'network_protocol' => env('RABBITMQ_NETWORK_PROTOCOL', 'tcp'),

    'options' => [
        'heartbeat' => (int) env('RABBITMQ_HEARTBEAT', 10),
        'connection_timeout' => (float) env('RABBITMQ_CONNECTION_TIMEOUT', 3.0),
        'read_timeout' => (float) env('RABBITMQ_READ_TIMEOUT', 3.0),
        'write_timeout' => (float) env('RABBITMQ_WRITE_TIMEOUT', 3.0),
        'channel_rpc_timeout' => (float) env('RABBITMQ_CHANNEL_RPC_TIMEOUT', 0.0),

        // TLS options (paths mounted from Kubernetes Secrets)
        'ssl_options' => [
            'cafile' => env('RABBITMQ_SSL_CAFILE'),
            'local_cert' => env('RABBITMQ_SSL_LOCALCERT'),
            'local_key' => env('RABBITMQ_SSL_LOCALKEY'),
            'verify_peer' => (bool) env('RABBITMQ_SSL_VERIFY_PEER', true),
            'passphrase' => env('RABBITMQ_SSL_PASSPHRASE'),
        ],

        // Queue/exchange behavior (driver-specific)
        'queue' => [
            // Optional delayed prioritization
            'prioritize_delayed' => (bool) env('RABBITMQ_PRIORITIZE_DELAYED', false),
            'queue_max_priority' => (int) env('RABBITMQ_QUEUE_MAX_PRIORITY', 10),

            // Optional publish to exchange with routing key
            'exchange' => env('RABBITMQ_EXCHANGE'),
            'exchange_type' => env('RABBITMQ_EXCHANGE_TYPE', 'direct'),
            'exchange_routing_key' => env('RABBITMQ_EXCHANGE_ROUTING_KEY', ''),

            // Optional: reroute failed messages (in addition to Laravel failed_jobs)
            'reroute_failed' => (bool) env('RABBITMQ_REROUTE_FAILED', false),
            'failed_exchange' => env('RABBITMQ_FAILED_EXCHANGE', 'amq.direct'),
            'failed_routing_key' => env('RABBITMQ_FAILED_ROUTING_KEY', '%s.failed'),
            'quorum' => (bool) env('RABBITMQ_QUEUE_QUORUM', false),

            // Optional custom wrapper for foreign payloads:
            // 'job' => \App\Queue\Jobs\RabbitMQJob::class,
        ],
    ],
],
```

Notes:
- Keep per-connection `retry_after` in `config/queue.php` greater than worker `--timeout`.
- If using custom payload formats from external producers, define a custom `job` wrapper class.
- Prefer one canonical env naming schema; map aliases only during migration.

# Step 3 — Write jobs for at-least-once execution
Assume duplicate delivery is possible:
- enforce idempotency via DB unique keys and dedupe keys,
- pass IDs and immutable business keys, not large mutable payloads,
- set explicit client timeouts (HTTP/DB/RPC) inside job handlers.

Typical per-job hardening:
- `$tries`, `backoff()` or `retryUntil()` for bounded retries,
- `$timeout` + `$failOnTimeout` where appropriate,
- explicit handling for non-retryable business errors.

# Step 4 — Run workers (local and production)
## Local
- `php artisan queue:work rabbitmq --queue=high,default --sleep=1 --tries=5 --timeout=60`
- `php artisan rabbitmq:consume rabbitmq --queue=high --prefetch-count=50 --timeout=60 --tries=5 --json`

## Kubernetes with platform-app-php Helm chart
Recommended:
- Run web (Octane) and worker separately.
- Set `QUEUE_CONNECTION=rabbitmq` via envConfig.
- Use `maxJobs` / `maxTime` to recycle workers and control memory drift.
- Keep `terminationGracePeriodSeconds` high enough for in-flight jobs to finish.
- For `rabbitmq:consume`, deploy one queue per worker Deployment (or one Deployment per queue profile).

See: `assets/helm/values.worker.rabbitmq.yaml.example`

# Step 5 — Topology and DLQ strategy
Prefer topology pre-creation in infra or release jobs:
- exchanges, queues, bindings, and DLX policies should exist before high-volume workers start,
- use package commands when needed:
  - `rabbitmq:exchange-declare`
  - `rabbitmq:queue-declare`
  - `rabbitmq:queue-bind`
- policy-first for DLX is preferred (avoids brittle hardcoded x-args lifecycle).

RabbitMQ reliability baseline:
- dedicated vhost and least-privilege user per environment,
- DLX + DLQ for poison messages,
- quorum queues for critical durability where appropriate,
- understand quorum caveat: repeated nack/requeue patterns can hurt log growth; delivery-limit matters.

# Step 6 — Runtime resilience
Laravel side:
- `after_commit=true` for jobs dispatched inside DB transaction flows,
- timeout discipline: `job timeout` and `queue:work --timeout` must be below `retry_after`,
- process manager required (Kubernetes/Supervisor/systemd) to restart failed workers safely.

Connection and heartbeat:
- keep heartbeat enabled (do not disable unless you intentionally rely on TCP keepalive policy),
- in Octane producer scenarios, validate long-lived connection behavior under idle periods before production rollout.

# Step 7 — Octane considerations
If your app uses Octane:
- Warm the `rabbitmq` connection as suggested by the package docs.
- Keep queue workers separate from Octane web workers (different Deployments/Pods).
- Validate idle heartbeat behavior in long-lived producer workers before production rollout.

# Step 8 — Failure handling (Laravel + RabbitMQ)
Laravel:
- Use `failed_jobs` storage (DB) and alert on increases.
- Use `queue:failed`, `queue:retry`, and incident runbooks for rapid replay and containment.

RabbitMQ (optional):
- Enable `reroute_failed` only when failed-route topology is verified.
- Ensure infra has the exchange/queue/bindings for the failed route (do not assume auto-creation).
- Validate failed routing keys and dead-letter bindings with a forced-failure test.

# Step 9 — Observability without Horizon
For RabbitMQ production observability, rely on:
- RabbitMQ broker metrics (ready/unacked/consumers/rates/alarms),
- worker logs and application metrics,
- failed job tracking and DLQ signals,
- Laravel 13 `queue:monitor` threshold alerts once the installed driver source includes the monitor methods.

Operational note for Laravel 13:
- `php artisan queue:monitor rabbitmq:default --max=100` is useful as a lightweight threshold alarm.
- Treat `queue:monitor` as a supplement, not your primary RabbitMQ telemetry.
- In the maintained fork snapshot for this skill:
  - `pendingSize()` reflects broker queue depth.
  - `delayedSize()` and `reservedSize()` currently return `0`.
  - `creationTimeOfOldestPendingJob()` currently returns `null`.
- Use broker metrics for ready, unacked, consumers, publish/ack rates, and oldest-message investigations.

# Step 10 — Verification checklist
- Dispatch a test job and confirm:
  - message appears in RabbitMQ queue
  - worker consumes and acks
  - failure path lands in `failed_jobs` and (if enabled) in the failed route
- Kill a worker pod during processing:
  - verify job is retried (at-least-once)
  - verify idempotency prevents duplicates
- Load test:
  - observe queue depth and worker CPU/memory
  - tune queue split, prefetch, and worker replicas

# Troubleshooting map (high-signal)
1) Laravel 13 `queue:monitor` failure after driver upgrade lag:
- Symptom: missing method errors around `pendingSize`, `delayedSize`, `reservedSize`, or `creationTimeOfOldestPendingJob`.
- Action: use the maintained fork tag or an upstream stable release that implements the Laravel 13 monitor surface.
2) Queue/Binding missing at worker start:
- Symptom: `NOT_FOUND` / consume startup errors.
- Action: pre-create queue+exchange+bindings before scaling consumers.
3) Accidental Horizon mode enablement:
- Symptom: `RABBITMQ_WORKER=horizon` appears in env/config for RabbitMQ workers.
- Action: remove it and force `worker=default`; redeploy workers.
4) Missed heartbeat / closed channel in long-lived producers:
- Symptom: heartbeat/channel closed exceptions after idle windows.
- Action: validate heartbeat strategy + connection lifecycle; use safe reconnect and process restart behavior.
5) Duplicate job execution:
- Symptom: same job runs twice.
- Action: enforce `timeout < retry_after`, idempotency, and bounded retry rules.
6) `queue:monitor` gives only partial queue insight:
- Symptom: delayed/reserved/oldest metrics look empty even though the broker shows activity.
- Action: remember the current maintained driver only maps pending depth richly; use broker metrics for the rest.

# Known upstream change signals (track before major rollout)
- Open pull request:
  - `#652` adds Laravel 13 + PHP 8.5 CI coverage, `Consumer::stop()` compatibility, and `RabbitMQQueue` monitor methods. Prefer a tagged maintained fork until that lands in a stable upstream release.
- Open issues:
  - `#644` worker queue/binding creation expectations mismatch.
  - `#634` maintenance-mode channel exceptions (`CONNECTION_FORCED`) need graceful handling.
  - `#615` DLQ setup confusion in real deployments.
  - `#601` quorum + delayed dead-letter safety discussion.
- Closed but informative:
  - `#603` consume command gained `--json` output support.
  - `#562` multiple queues are for `queue:work`, not `rabbitmq:consume`.
  - `#591` heartbeat behavior can break in long-lived producer contexts (especially with Octane-style lifecycles).

# Output contract
When applying this skill, output should include:
- exact files changed,
- exact driver source (`upstream stable` vs maintained fork tag) and why it was chosen,
- config diffs and why each option exists,
- deployment/runtime commands,
- verification checklist and rollback notes,
- assumptions, monitoring limitations, and unresolved risks.

# References
- Package repo: https://github.com/vyuldashev/laravel-queue-rabbitmq
- Maintained fork example: https://github.com/sohrabafard/laravel-queue-rabbitmq
- Package README: https://github.com/vyuldashev/laravel-queue-rabbitmq/blob/master/README.md
- Upstream PR #652: https://github.com/vyuldashev/laravel-queue-rabbitmq/pull/652
- Laravel Queue docs: https://laravel.com/docs/13.x/queues
- RabbitMQ DLX docs: https://www.rabbitmq.com/docs/dlx
- RabbitMQ prefetch docs: https://www.rabbitmq.com/docs/consumer-prefetch
- RabbitMQ heartbeat docs: https://www.rabbitmq.com/docs/heartbeats
- RabbitMQ quorum docs: https://www.rabbitmq.com/docs/quorum-queues
- RabbitMQ at-least-once DL: https://www.rabbitmq.com/blog/2022/03/29/at-least-once-dead-lettering
- StackOverflow timeout/retry_after rule of thumb: https://stackoverflow.com/questions/41991251/what-is-the-difference-queuework-tries-3-and-tries-3
- GitHub issues list: https://github.com/vyuldashev/laravel-queue-rabbitmq/issues

# Anti-patterns
- Using Horizon for RabbitMQ workers in this repository.
- Running `rabbitmq:consume` against multiple queues in one process.
- Leaving timeout/retry defaults unreviewed for long jobs.
- Enabling DLQ reroute without verifying broker topology.
- Treating handlers as exactly-once; ignoring idempotency.
