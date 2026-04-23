---
name: alaa-async-messaging
description: "Async architecture for Alaa services: Kafka for events + RabbitMQ for jobs (recommended hybrid), optional Redis/Horizon for Laravel queues, with idempotency, retries, DLQ, and ops guardrails (prefetch/heartbeat/quorum poison control)."
---




# Purpose
Provide a production-ready workflow for asynchronous processing in an event-driven, multi-tenant system:

- Kafka for immutable domain/integration events (replayable event stream).
- RabbitMQ for background jobs/tasks (work-queue semantics).
- Optional Redis/Horizon when you explicitly want Horizon ergonomics for Redis-backed queues.

This skill is intentionally opinionated toward:
- Reliability (at-least-once, idempotency, bounded retries, DLQ)
- Correctness (dispatch-after-commit, outbox publishing, dedupe keys)
- Predictable throughput (queue/topic separation, concurrency sizing, backpressure)
- Operational clarity (templates + runbooks + verification)
- Security (least privilege, TLS where required, network segmentation)

# When to use
- Designing event-driven + async architecture (Kafka + RabbitMQ).
- Add / migrate / harden queue infrastructure (RabbitMQ, Redis/Horizon, hybrid).
- Tune throughput (worker counts, queue splits, prefetch/heartbeats, retries/backoff).
- Implement DLQ / failure rerouting, idempotency, outbox-consumer dedupe.
- Prepare production deployment: Supervisor / systemd / Docker / Kubernetes patterns.
- Add observability: structured logs, job tags, metrics, dashboards, runbooks.

## When NOT to use
- do not use this skill for synchronous request-response flows with no queue, event, or broker design decision
- do not use Kafka or RabbitMQ guidance here to justify bypassing the repository's data, security, or trust-boundary rules
- do not use Redis or Horizon guidance here as a substitute for RabbitMQ-specific operational controls when RabbitMQ owns the job plane

# Key split (recommended)
- Kafka: events (facts, replayable, multi-consumer).
- RabbitMQ: jobs/tasks (do work, competing consumers, ack/nack, DLQ).

Rationale:
- Don’t force Kafka to behave like a work queue for “do work once” commands.
- Don’t force RabbitMQ to behave like an append-only event log / source of truth.

# Key constraint: Horizon and RabbitMQ (important)
- Laravel Horizon is designed for **Redis-backed** queues and operationally depends on Redis.
- Horizon is NOT a process manager/monitor for RabbitMQ queues by default.
- Do not assume “Horizon replaces RabbitMQ monitoring”.

If you run RabbitMQ for jobs:
- Monitor RabbitMQ with broker metrics/management tooling and app logs/metrics.
- Use DLQ + retry policies + idempotency; do not rely on Horizon for RabbitMQ visibility.

If you want Horizon ergonomics:
- Use Redis queues for the subset of jobs you want Horizon to manage/observe.

## Hybrid: Redis/Horizon + RabbitMQ at the same time (allowed, but must be explicit)
You can run both:
- Redis + Horizon for “Horizon-managed” Laravel jobs (ergonomics + dashboard).
- RabbitMQ workers/consumers for “RabbitMQ-managed” jobs (broker semantics + DLQ).

Rules:
- Be explicit about job routing:
    - do not rely on a single global `QUEUE_CONNECTION` if you need both backends
    - route per-job/per-queue using Laravel job connection/queue settings (e.g., job `$connection` / `$queue` or dispatch options)
- Run separate worker fleets:
    - `php artisan horizon` for Redis queues
    - `php artisan queue:work rabbitmq ...` (or driver consume command) for RabbitMQ queues
- Keep retries/backoff and timeouts consistent across both planes.
- Document which classes/queues go to Redis vs RabbitMQ to avoid “silent misrouting”.

# Constraints
- Never commit secrets (`.env`, certs, passwords).
- Use least-privilege credentials, separate vhosts per environment, and network segmentation.
- Prefer minimal diffs; do not refactor unrelated app code.
- For non-trivial tasks, follow `alaa-workflow` and create/update the plan file (or constrained-mode alternative).

# Laravel 13 messaging notes
- Default Laravel target in this skill pack is Laravel 13 on PHP 8.5.
- When queue or connection selection would otherwise be repeated across dispatch sites, prefer central `Queue::route(...)` rules.
- Prefer queue and listener attributes such as `#[Tries]`, `#[Backoff]`, `#[Timeout]`, `#[FailOnTimeout]`, or `#[DeleteWhenMissingModels]` when they make retry or lifecycle policy clearer than scattered properties, while preserving repository style where it is already consistent.
- When reviewing upgrade work, update queue-event listeners and monitoring code for `JobAttempted::$exception` and `QueueBusy::$connectionName`.

# Step 1 — Repository discovery checklist
1) Identify current stack:
- Laravel version + installed packages (Horizon? RabbitMQ driver? Kafka client?)
- `config/queue.php`, `config/horizon.php` (if present)
- `.env.example` keys (QUEUE_CONNECTION, Redis/RabbitMQ/Kafka vars)
2) Identify runtime/deploy model:
- VM + Supervisor? systemd? Docker Compose? Kubernetes?
3) Identify requirements:
- Ordering requirements? duplicates acceptable?
- Peak throughput and job durations
- Failure tolerance: DLQ? replay? retention?
4) Identify constraints:
- Must-use Kafka? Must-use RabbitMQ? Optional Redis/Horizon?
- Multi-tenancy considerations (tenant must be scoped in handlers)

If unclear, assume conservative defaults and document assumptions.

# Step 2 — Choose a golden-path architecture

## Option E (recommended): Kafka for events + RabbitMQ for jobs
- Publish domain/integration events to Kafka (replayable).
- Enqueue jobs/tasks to RabbitMQ (work queues with DLQ).
- Use outbox to Kafka when correctness matters (publish after DB commit).

## Option A: Redis queue + Horizon
Pros: best Laravel ergonomics; strong dashboard.
Cons: Redis ops/HA; Horizon Redis Cluster constraints.

## Option B: RabbitMQ as Laravel queue backend
Pros: rich broker features; strong routing.
Cons: driver compatibility variability; Horizon monitoring does not apply by default.

# Step 3 — Kafka event plane (when used)

## What goes to Kafka
Immutable events (facts) that may need replay and multiple consumers.

Rules:
- Partition key should preserve ordering where it matters (tenant_id + aggregate_id/business key).
- Consumers assume at-least-once and must be idempotent.
- Prefer outbox publishing for correctness (write DB → commit → publish).
- Do not publish “do work once” commands here unless you intentionally model them as events and handle idempotency/replay accordingly.

# Step 4 — RabbitMQ job plane (when used)

## What goes to RabbitMQ
Jobs/tasks with work-queue semantics (competing consumers, bounded retries, DLQ).

## Poison-message controls (mandatory)
- Always define DLX/DLQ routing for critical queues.
- Retries must be bounded; poison messages must not loop forever.
- Prefer quorum queues for critical workloads; ensure poison-message behavior is explicitly handled (bounded redelivery + DLQ routing).
- For ordered/critical queues, prefer conservative `prefetch` (often prefetch=1) to reduce blast radius.

## Heartbeats/timeouts (mandatory)
- Set broker/client heartbeats and timeouts to detect dead connections.
- Align consumer timeouts with job timeouts to avoid duplicate work.
- Ensure graceful stop and sufficient stop timeouts in Supervisor/systemd.

# Step 5 — Implementation playbooks

## Playbook A — Redis + Horizon (baseline)
Actions:
1) Ensure Horizon is installed and configured:
- commit `config/horizon.php` changes
- ensure Redis connectivity and env vars documented

2) Configure supervisors:
- choose `balance` strategy appropriate for workload
- set `tries`, `timeout`, `backoff`
- align timeouts to prevent duplicates:
    - `timeout` MUST be a few seconds LESS than `retry_after`

3) Secure Horizon dashboard:
- restrict via auth gate / IP allowlist
- never expose publicly without protection

4) Deploy/run:
- Supervisor/systemd/K8s runs `php artisan horizon`
- on deploy, run `php artisan horizon:terminate` so workers reload code safely

Templates:
- `assets/systemd/horizon.service.example`
- `assets/supervisor/horizon.conf.example`

## Playbook B — RabbitMQ as queue backend (baseline)
Assumes a RabbitMQ queue driver integrated with Laravel queues.

Actions:
1) Verify driver in `composer.json` and driver docs.
2) Configure `config/queue.php` rabbitmq connection (driver-specific).
3) Update `.env.example` with placeholders (no secrets).
4) Choose worker command:
- Most compatible: `php artisan queue:work rabbitmq --queue=...`
- If supported and validated: `php artisan rabbitmq:consume --queue=...` (push-based, often faster)

5) Correctness:
- Ensure dispatch-after-commit for DB-coupled jobs (`after_commit=true`) so jobs cannot run before transaction commit.

6) Failure handling:
- Laravel failed_jobs storage enabled (when supported by your driver and expected by your ops).
- Broker-side DLQ routing (DLX/DLQ) for critical queues.

7) Broker hardening (baseline):
- vhost per environment
- per-app user, least privilege
- disable/restrict guest
- TLS for non-local traffic if required
- define DLX/DLQ policies for critical queues

Templates:
- systemd:
    - `assets/systemd/queue-work-rabbitmq@.service.example`
    - `assets/systemd/rabbitmq-consume@.service.example`
- supervisor:
    - `assets/supervisor/queue-work-rabbitmq.conf.example`
    - `assets/supervisor/rabbitmq-consume.conf.example`
- docker (local/dev only):
    - `assets/docker/docker-compose.rabbitmq-redis.yml.example`

# Reliability rules (mandatory)
- Every handler must be idempotent.
- Retries must use bounded attempts + jittered backoff.
- Poison messages go to DLQ with enough context to debug.
- Request path must not block on slow consumers.

# Step 6 — Shared reliability patterns (mandatory)
- At-least-once is the default (Kafka and RabbitMQ).
- Handlers must be idempotent (unique constraints, dedupe keys, upserts).
- Bounded retries + exponential backoff + jitter.
- Dispatch after commit for DB-coupled jobs/events.
- Keep payloads small: pass IDs/business keys, not huge serialized models.

# Step 7 — Verification / Definition of Done
- Architecture decision documented (Kafka events vs RabbitMQ jobs; optional Horizon).
- DLQ strategy verified (force-fail path).
- Kafka event produced and consumed end-to-end (idempotent consumer).
- RabbitMQ job processed end-to-end (force-fail lands in DLQ/failed store).
- Prefetch/heartbeat/timeout alignment reviewed.
- Tenant scoping proven in handlers.
- Runbook notes captured.

# References in this skill pack
- `references/source-map.md`
- `references/queues-best-practices.md`
- `references/rabbitmq-topology-and-policies.md`
- `references/troubleshooting.md`

Read `references/source-map.md` before relying on latest/current/version/security-sensitive queue, broker, Laravel Horizon, Kafka, RabbitMQ, Redis, retry, or DLQ behavior.

# Anti-patterns
- Using Kafka as a “do work once” job queue without careful semantics.
- Using RabbitMQ as the event log source of truth.
- Infinite retries or missing DLQ.
- Non-idempotent handlers.
- Publishing events before DB commit without outbox/after-commit discipline.
- Cross-tenant processing without explicit tenant scoping.

## Fast entry

| If the task is mainly about...                     | Start with                                        |
|----------------------------------------------------|---------------------------------------------------|
| event facts, replay, or multi-consumer fanout      | the Kafka split and outbox sections               |
| background jobs, retries, or DLQ handling          | the RabbitMQ / work-queue sections                |
| Redis + Horizon ergonomics                         | the hybrid Redis/Horizon rules                    |
| throughput, prefetch, heartbeat, or poison control | the ops guardrails and troubleshooting references |
