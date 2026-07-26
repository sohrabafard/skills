# Topic map — the situation you are in, and the one file that answers it

This is the only router in this skill. Match the situation, read that one file, and stop. Reading the whole tree means the task was never scoped.

| You are about to… | Read |
|---|---|
| add, move, rename, or split a route, Controller, Service, Repository, DTO, Resource, Policy, Observer, or Enum, or decide what a method may accept or return across a boundary | `references/10-layer-map.md` |
| decide which identifier a response exposes, a route binds on, or a filter accepts | `references/10-layer-map.md` |
| bind an interface in a service provider, add or move caching for a domain, or explain why a worker boots with a dependency down but not with it up | `references/20-composition-and-boot.md` |
| emit a domain event, add a listener, write to or publish from an outbox, or decide whether a side effect runs inside the request | `references/30-events-and-outbox-seam.md` |
| decide what a caller sees when the database, Redis, or the broker is unreachable, or write any `catch` on a dependency failure | `references/40-degraded-mode.md` |
| diagnose something already wrong in production — stale reads, a stuck outbox row, a worker that will not boot, two endpoints answering in different shapes | `references/50-failure-recovery.md` |
| add or move one of this skill's surfaces and make it visible in production: an authorization denial, a cache decorator, an outbox transition, a fallback taken | `references/60-telemetry-surfaces.md` |
| make behaviour vary by environment or scale, add a config key, or read config anywhere near bootstrap | `references/70-config-contract.md` |
| run the gate, wire it into CI, read a finding, or waive one | `references/80-acceptance-gate.md` |
| rely on framework-owned behaviour when the task says `latest`, `current`, `upgrade`, `Laravel 13`, `deprecated`, `removed`, or `security`, or when middleware, bootstrap, route precedence, resource serialization, or container behaviour is in scope | `references/source-map.md` |

## Situations that leave this skill

Some situations are not this skill's at all: writing a cache key, TTL, index, or migration; deciding whether and how a list paginates; choosing a name, a type, or a pattern inside one file; deriving tenant or user identity; and settling a boundary that does not exist yet. Each is routed by the ownership table in `SKILL.md`, which also states what wins on conflict. That table is the only list of owners in this skill.
