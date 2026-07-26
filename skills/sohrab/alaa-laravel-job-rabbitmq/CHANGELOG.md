# Changelog

## 2026-07-26

- **Version claim resolved.** Verified against an installed package in a consuming repository (locked
  `v15.0.0`, ref `fd685fa1a890b82011e9cf25d990e14221c395ad`) that the four Laravel 13 monitor methods and the
  three-parameter `Consumer::stop()` are present. `references/driver-facts.md` now records what is verified,
  what is only asserted, and the grep to run before relying on it.
- **New rules**, none of which the skill had: ack and nack policy; broker-policy delivery limit with the
  crash-loop derivation (a requeue does not advance `laravel.attempts`, so `--tries` cannot end the loop);
  publisher confirms as a stated decision with its cost; the prefetch-times-duration unacked-window rule; the
  broker-down producer contract; one required redelivery test; trace propagation and the signals this seam
  produces.
- **`references/failure-classes.md`** replaces the arrival-ordered troubleshooting list: eight failure
  classes, each with symptom, diagnosis, smallest retry and escalation.
- **Four code-versus-prose corrections.** `queue_max_priority` is inert without `prioritize_delayed` and the
  omitted default is 2, not 10; `connection` is a class name, so the variable is `RABBITMQ_CONNECTION_CLASS`;
  `retry_after` is inert on this driver, replaced by the two timeout relationships that do bound duplicate
  execution; `.github/workflows/tests.yml` and the `.tmp/` clone tier left the source order.
- **~45 KB of snapshot retired** to `_to_delete/2026-07-26-batch2/`: the fork `README.md` (byte-identical to
  upstream), fork `RabbitMQQueue.php` (one added block), fork `composer.json`, `tests.yml` and
  `CHANGELOG-14x.md`, and upstream `CHANGELOG-13x.md`. Their decision-relevant content is
  `references/fork-divergence.md`. `src/Consumer.php` and both pin files kept.
- **Restructured** into six references behind a router of observable conditions, with an ownership-boundary
  section naming the owner of every criterion this skill does not own, and a description carrying its own
  exclusions so the router can see them.
- **Helm asset fixed**: `/bin/sh -ec` instead of `-lc` plus `set -euo pipefail`, no hardcoded application
  directory, one canonical env name, and the service-specific vhost replaced by a registry placeholder.

## 2026-07-08

- Added "Redis in the async plane (boundaries and degradation)" section: fail-open defaults for Redis-backed job middleware (`RateLimited`, `WithoutOverlapping`, funnels), DB-first dedupe with optional Redis fast-path, no cache/Redis in provider `register()`/`boot()` for worker boot safety, and routing to `alaa-data-layer references/50-redis-laravel-octane.md` for key/TTL/fallback contracts.
- Added matching anti-patterns (Redis-only dedupe for critical side effects; undefined Redis-outage behavior in job middleware).

## 2026-06-23

- Updated Laravel 13 guidance to prefer official upstream `vladimir-yuldashev/laravel-queue-rabbitmq` `v15.0.0` or newer instead of the temporary `sohrabafard` fork override.
- Kept the historical fork snapshot only as archived compatibility context and corrected troubleshooting/source-map wording to point at upstream stable.

## 2026-03-21

- Added a maintained fork snapshot for Laravel 13 / PHP 8.5 compatibility under `references/forks/sohrabafard/9c8125f133cc13d49e7c08496fde5615919439e7/`.
- Updated `SKILL.md` to prefer one tagged shared fork across services instead of app-local driver copies when upstream stable lags.
- Documented Laravel 13 `queue:monitor` expectations and the current `RabbitMQQueue` monitor-method behavior exposed by the maintained fork.
- Added explicit guidance for switching back from the maintained fork to upstream stable once a compatible stable release lands.

## 2026-03-06

- Reworked `SKILL.md` into a source-validated, production-ready guide for `vladimir-yuldashev/laravel-queue-rabbitmq`.
- Added explicit source-of-truth ordering (package source, README/changelog, issues, Laravel/RabbitMQ official docs, Arvan policy).
- Added pinned upstream snapshot under `references/upstream/vyuldashev/<commit>/` for deterministic/offline behavior.
- Added path-resolution fallback order: skill snapshot -> `vendor/...` -> `.tmp/...` -> web docs.
- Corrected worker-mode guidance:
  - `queue:work` (`basic_get`) supports multiple queues.
  - `rabbitmq:consume` (`basic_consume`) is one-queue-per-process with prefetch tuning.
- Enforced repository policy: do NOT use Horizon for RabbitMQ workers; force default worker mode.
- Restored explicit Octane section: warm RabbitMQ connection and keep Octane web workers separate from queue workers.
- Added hard constraints and reliability guardrails:
  - idempotency,
  - timeout vs `retry_after` discipline,
  - topology pre-creation,
  - DLQ/policy-first operations,
  - heartbeat/runtime resilience notes.
- Added troubleshooting matrix informed by upstream issues.
- Added explicit upstream issue watchlist (open + closed signals) with actionable interpretation.
- Expanded references to official docs and package sources.
- Hardened `assets/helm/values.worker.rabbitmq.yaml.example`:
  - Arvan-safe resources (`requests == limits`),
  - richer RabbitMQ env schema and connection options,
  - explicit notes for timeout/retry alignment,
  - safer consume-mode override example with prefetch tuning.
