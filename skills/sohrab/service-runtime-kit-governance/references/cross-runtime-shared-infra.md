# Cross-Runtime Shared Infrastructure

Use when a change touches shared local infrastructure — Postgres, Redis, RabbitMQ, Adminer — or when a Go service on the `alaa-go-chi` kit is in scope. A Laravel change that does not touch shared infra does not need this file.

## Two generators, one contract

Shared infra is one running instance the whole platform reuses, emitted by two generators implementing the same contract:

- **Laravel** services get it from `service-runtime-kit` via `scripts/runtime/render-runtime.sh`.
- **Go** services on the `alaa-go-chi` kit get it from that kit's own scaffold (`scaffold/templates.go`, `docs/consumer-templates/**`), not from `service-runtime-kit`.

The infra set both emit is `postgres`, `adminer`, `redis`, `rabbitmq`. Adminer is shared local infrastructure, not a service-owned application service, so a service repo does not add its own.

## Owned here, and not owned here

`alaa-services-contract` `references/15-deployment-and-runtime-contract.md` is the normative owner of the canonical shared-infra identity, the in-network endpoint aliases, the host-published port defaults, and the reuse-or-fail-fast obligation. Read the values there; they are not restated here, because the contract must hold even for a runtime that was hand-written or emitted by a third generator.

`SKILL.md` "Shared Runtime Contract Ownership" names the generator variables this skill does own.

## Reuse mechanism

Each wrapper inspects the shared project's running state with `docker compose -p <project> … ps --format json`. If every service it would provision is already running it reuses them untouched rather than recreating a peer-booted instance; otherwise it bootstraps them. On an indeterminable state it refuses to recreate rather than clobber a peer's data. No generator writes an ownership marker, which is what lets a Go service and a Laravel service boot in either order.

## Routing a change

A change to how a **Go** service generates its runtime belongs in the `alaa-go-chi` kit, never in `service-runtime-kit`.

A change to the shared *contract* — identity, reuse mechanism, image tags, infra set — is `alaa-services-contract`'s. `SKILL.md` "Working Method" holds the procedure for landing it in both generators, including what to do when the `alaa-go-chi` kit is not in the workspace.
