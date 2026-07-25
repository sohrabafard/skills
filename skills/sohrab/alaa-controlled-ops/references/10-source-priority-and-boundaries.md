# Source Priority And Boundaries

## Source priority

This is the only source ranking in this skill. Higher rank wins on conflict.

Ranks 1 and 2 are the same two repositories in either order, by task class: package work puts `alaa/controlled-ops` first and the adopter second; adopter work reverses them. Below them, for both classes:

3. Committed docs in the repository that owns the surface under discussion.
4. `composer.lock`, plus Satis and Composer dist metadata for the resolved version.
5. Generated public artifacts — Postman collections, route inventories, API summaries. When one disagrees with rank 1 or 2 the code is correct and the artifact is the defect: fix it through `/alaa-postman-collections` ($alaa-postman-collections) or `/alaa-docs-farsi` ($alaa-docs-farsi), never your claim.
6. Plan and state files, as continuation context only, never as contract truth.
7. Historical Codex or Claude Code sessions, as search hints only. A fact from a session is unverified until read out of rank 1 or 2.

When the two repositories disagree, the owner of the surface is correct: on package behaviour the package wins and the adopter has drifted; on service behaviour the service wins. Report the drift; never edit the winner to match the loser.

## Package-owned surfaces

The package may own reusable:

- DTOs, enums, guards, planners, status transitions, and lifecycle decision helpers
- dry-run hash, payload hash, and idempotency primitives, canonicalised per `references/30-lifecycle-idempotency-validation.md`
- audit, structured-log, metric, progress, and lifecycle outbox value objects
- file metadata, access policy, import chunking, and adapter contracts
- service-adoption test helpers and package verification gates

The package owns the shape of those observability value objects, not their contract; `/alaa-observability-soc` ($alaa-observability-soc) owns that, under the condition stated in `references/90-source-map.md`.

## Service-owned surfaces

The consuming service owns:

- HTTP routes, controllers, FormRequests, resources, and public response envelopes
- trusted gateway context normalization, permission catalog usage, and authorization policy
- domain validation, table writes, transactions, locks, models, migrations, jobs, and outbox publication
- audit/log/metric/outbox sink implementations
- service docs, route inventory, Postman examples, and public API validation

## Hard boundary

ControlledOps package code must not directly write consuming-service domain tables, expose service HTTP routes, own raw upload bodies, or silently create public behavior just because a package helper exists.
