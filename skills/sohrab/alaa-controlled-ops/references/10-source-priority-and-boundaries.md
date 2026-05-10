# Source Priority And Boundaries

## Source priority

Use current repository truth in this order:

1. Active consuming service code, tests, routes, migrations, Postman artifacts, and docs when the task is service adoption.
2. `D:\Sohrab\Project\alaa-controlled-ops` code, tests, docs, config, and verifier when the task is package behavior.
3. Current service or package plan/state files only as continuation context, not as contract truth.
4. Historical Codex sessions only as search hints.

If sources disagree, verify against live code and committed tests before editing claims or behavior.

## Package-owned surfaces

The package may own reusable:

- DTOs, enums, guards, planners, status transitions, and lifecycle decision helpers
- dry-run hash, payload hash, and idempotency primitives
- audit, structured-log, metric, progress, and lifecycle outbox value objects
- file metadata, access policy, import chunking, and adapter contracts
- service-adoption test helpers and package verification gates

## Service-owned surfaces

The consuming service owns:

- HTTP routes, controllers, FormRequests, resources, and public response envelopes
- trusted gateway context normalization, permission catalog usage, and authorization policy
- domain validation, table writes, transactions, locks, models, migrations, jobs, and outbox publication
- audit/log/metric/outbox sink implementations
- service docs, route inventory, Postman examples, and public API validation

## Hard boundary

ControlledOps package code must not directly write consuming-service domain tables, expose service HTTP routes, own raw upload bodies, or silently create public behavior just because a package helper exists.
