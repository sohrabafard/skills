# Changelog

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
