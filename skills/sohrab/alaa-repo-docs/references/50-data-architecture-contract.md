# Data architecture, storage, and request-flow contract

## Why this document exists

`docs/data-architecture.md` is the storage and state walkthrough. It exists so a developer or agent can see where data lives, which tables, collections, or indexes matter, which cache keys and derived records exist, and how one representative request reads or mutates persisted state.

It is separate because `docs/BIG_PICTURE.md` becomes unreadable if it carries every storage detail, table inventory, cache policy, and state snapshot itself.

This document describes what the repository stores. It does not decide what the repository should store: schema shape, query shape, and index choice are `/alaa-data-layer`'s (`$alaa-data-layer`).

## When docs/data-architecture.md is required

Create or refresh it when one or more of these is true:

- the repository uses a relational database, document store, key-value store, cache, search index, object storage, outbox, or other meaningful persisted state,
- a reader must follow a request across stored records to understand the system,
- the service uses denormalized records, materialized views, sessions, tokens, cache invalidation, TTL rules, or read models,
- storage shape, table ownership, or cache behavior changed and the current documents would otherwise mislead.

Skip it only for a simple stateless tool or library. When you skip it and the repository structure would make a reader expect it, say so explicitly in `README.md` or `docs/BIG_PICTURE.md`.

Filename, preservation, and role separation follow the rules in `SKILL.md` under `## Default document set` and `references/20-readme-big-picture-contract.md`. In particular: do not turn this document into a second API summary or a second BIG_PICTURE.

## Required structure for docs/data-architecture.md

Use this structure unless the repository shape clearly needs a tighter variant:

1. `# <Service or Domain> Data Architecture`
2. `## Purpose and scope`
3. `## Source-of-truth map`
4. `## Storage topology`
5. `## Primary tables, collections, or indices`
6. `## Cache and derived-state inventory`
7. `## Key data structures and record shapes`
8. `## Representative request walkthrough`
9. `## State snapshots by step`
10. `## Concurrency and ordering behavior`
11. `## Consistency, invalidation, and lifecycle rules`
12. `## Verification notes and inspection paths`
13. `## See also`

Table or collection inventory columns: name, purpose, primary keys or canonical identifiers, important fields, writer paths, reader paths, and retention or lifecycle notes when verified.

Cache inventory columns: key pattern or namespace, value shape, writer, reader, TTL, invalidation trigger, and fallback path.

## Storage coverage rules

- Cover every meaningful durable or semi-durable store that affects behavior: primary database, replicas when behavior depends on them, cache, outbox, blob or object storage, search indexes, read models, and session stores.
- Distinguish the source of truth from derived or cached state.
- Use canonical table, collection, index, bucket, topic, and cache-key names exactly as the code and infrastructure use them.
- Call out tenant or partition keys, sharding rules, and compound identifiers when they materially shape behavior.
- Include only verified columns, fields, TTLs, and lifecycle rules. Never infer a schema detail from a name.
- When a record shape is serialized or nested, show a minimal realistic example rather than a vague paragraph, under the redaction rules in `references/10-language-and-links.md`.
- Document what the repository does. When the documented shape looks wrong — an unindexed lookup, an unbounded collection, a missing constraint — record it as a finding for `/alaa-data-layer` (`$alaa-data-layer`) rather than silently documenting it as intended design.

## Request walkthrough rules

- Pick the most instructive path, such as create and read-back, sign-in, checkout, publish, moderation, or sync.
- Name the exact route, command, job, or message that starts the flow.
- Follow the path step by step across handler, service or use case, repository or model, database or cache, and any async handoff needed to understand stored state.
- For each step, state what is read, what is written, which keys or IDs matter, and which store is touched.
- Include at least one state-snapshot table, or an equivalent, that lets a reader inspect stored data as the request progresses.
- For any step whose cost grows with rows, tenants, history, or events — a list, search, export, or fan-out — state the access pattern and the index or key that serves it. Whether that bound is acceptable is `/alaa-algorithms-data-structures`'s (`$alaa-algorithms-data-structures`) decision, and the pagination strategy for a list flow is `/alaa-keyset-pagination`'s (`$alaa-keyset-pagination`).
- If the request continues asynchronously, show the storage handoff here and link to `docs/errors-events-observability.md` for the event and observability detail.
- Prefer one excellent walkthrough over several shallow ones.

## Concurrency and ordering rules

The walkthrough must state, for the flow it describes:

- which steps are safe when the same flow runs concurrently for the same record, and which are not,
- which store enforces that safety, naming the mechanism the code actually uses: a unique constraint, a transaction and its isolation level, a row or advisory lock, an optimistic version column, or a queue that serializes the work,
- what a caller observes when two concurrent runs collide — a conflict status, a retry, a last-writer-wins overwrite, or a duplicated side effect,
- and, when nothing enforces it, that nothing enforces it. An unstated concurrency rule reads as "safe" to the next reader, which is the failure this section exists to prevent.

## Diagram rules

- Use `flowchart LR` or `flowchart TD` for storage topology and store-to-store relationships; `sequenceDiagram` when call order and mutation order matter.
- Pair diagrams with compact tables when that makes storage mutations or cache keys easier to inspect.
- Keep node labels short and exact, using verified table names, cache-key prefixes, queue names, and route names.
- Prefer several focused diagrams over one that mixes every request family.

## Coverage requirements

The `docs/data-architecture.md` cluster tree must answer each of these without opening code:

- Where does the important data live, and which component reads and writes each store?
- Which cache keys or derived records exist, and what invalidates each one?
- What happens to stored state during one representative request?
- What happens when that request runs twice at once for the same record?
- Which code, migration, or runtime inspection point verifies each claim here?
