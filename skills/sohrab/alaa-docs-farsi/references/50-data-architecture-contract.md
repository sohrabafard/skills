# Data architecture, storage, and request-flow contract

## Includes these full-guide sections

- `# Standard data architecture, storage, and request-flow contract`
- `## Why this doc exists`
- `## When docs/data-architecture.md is required`
- `## Default filename and preservation rule`
- `## Separation from README, BIG_PICTURE, and api-summary`
- `## Required structure for docs/data-architecture.md`
- `## Storage coverage rules`
- `## Request walkthrough rules`
- `## Diagram rules`
- `## Data architecture quality bar`

# Standard data architecture, storage, and request-flow contract

## Why this doc exists
`docs/data-architecture.md` is the storage and state walkthrough for a repository.
It exists so a developer or agent can see where data lives, which tables or collections or indexes matter, which cache keys and derived records exist, and how one representative request reads or mutates persisted state.

This doc is separate because `docs/BIG_PICTURE.md` becomes shallow or unreadable if it tries to carry every storage detail, table inventory, cache policy, and state snapshot by itself.

## When docs/data-architecture.md is required
Create or refresh `docs/data-architecture.md` when one or more of these are true:
- the repository uses a relational database, document store, key-value store, cache, search index, object storage, outbox, or other meaningful persisted state,
- readers need to follow a request across stored records to understand the system,
- the service uses denormalized records, materialized views, sessions, tokens, cache invalidation, TTL rules, or read models,
- storage shape, table ownership, or cache behavior changed and the current docs would otherwise become misleading.

Skip this doc only for simple stateless tools or libraries with no meaningful persisted runtime state.
If you skip it, keep that choice explicit in `README.md` or `docs/BIG_PICTURE.md` when the repo structure could make a reader expect it.

## Default filename and preservation rule
- Use `docs/data-architecture.md` for new work.
- If the repository already has a stronger equivalent doc under another verified name, update that file instead of creating a duplicate.
- When you preserve an existing filename, repair README and cross-links so the documentation graph still makes the role of the doc obvious.

## Separation from README, BIG_PICTURE, and api-summary
- `README.md` stays the onboarding and navigation entrypoint.
- `docs/BIG_PICTURE.md` stays the architecture and runtime summary map.
- `docs/api-summary.md` stays the endpoint inventory plus request examples.
- `docs/data-architecture.md` holds the storage topology, table or collection inventory, cache inventory, record-shape notes, and the representative request walkthrough tied to stored state.
- `docs/errors-events-observability.md` holds the error, event, and observability deep dive.

Do not turn `docs/data-architecture.md` into a second API summary or a second BIG_PICTURE.

## Required structure for docs/data-architecture.md
Use this default structure unless the repository shape clearly needs a tighter variant:

1. `# <Service or Domain> Data Architecture`
2. `## Purpose and scope`
3. `## Source-of-truth map`
4. `## Storage topology`
5. `## Primary tables, collections, or indices`
6. `## Cache and derived-state inventory`
7. `## Key data structures and record shapes`
8. `## Representative request walkthrough`
9. `## State snapshots by step`
10. `## Consistency, invalidation, and lifecycle rules`
11. `## Verification notes and inspection paths`
12. `## See also`

Typical table or collection inventory columns:
- name,
- purpose,
- primary keys or canonical identifiers,
- important fields,
- writer paths,
- reader paths,
- retention or lifecycle notes when verified.

Typical cache inventory columns:
- key pattern or namespace,
- value shape,
- writer,
- reader,
- TTL,
- invalidation trigger,
- fallback path.

## Storage coverage rules
- Cover every meaningful durable or semi-durable store that affects system behavior: primary database, replicas when behavior depends on them, cache, outbox, blob or object storage, search indexes, read models, or session stores.
- Distinguish the source of truth from derived or cached state.
- Use canonical table, collection, index, bucket, topic, or cache-key names exactly as the code and infra use them.
- Call out tenant or partition keys, sharding rules, or compound identifiers when they materially shape behavior.
- Include only verified columns, fields, TTLs, or lifecycle rules. Do not infer schema details from naming alone.
- When a record shape is serialized or nested, show a minimal realistic example rather than a vague paragraph.

## Request walkthrough rules
- Pick the most instructive path for understanding the system, such as create and read-back, sign-in, checkout, publish, moderation, or sync.
- Name the exact route, command, job, or message that starts the flow.
- Follow the path step by step across controller or handler, service or use case, repository or model, database or cache, and any async handoff that is necessary to understand stored state.
- For each step, show what is read, what is written, what keys or IDs matter, and which store is touched.
- Include at least one state-snapshot table or equivalent that lets a reader inspect the stored data as the request progresses.
- If the request continues asynchronously, show the storage handoff here and link to `docs/errors-events-observability.md` for the deeper event and observability detail.
- Prefer one excellent walkthrough over many shallow walkthroughs.

## Diagram rules
- Use `flowchart LR` or `flowchart TD` for storage topology and store-to-store relationships.
- Use `sequenceDiagram` when call order and state mutation order matter.
- Pair diagrams with compact tables when that makes the storage mutations or cache keys easier to inspect.
- Keep node labels short and exact: use verified table names, cache-key prefixes, queue names, and route names.
- Prefer multiple focused diagrams over one oversized diagram that mixes every request family.

## Data architecture quality bar
`docs/data-architecture.md` is good when a developer or agent can answer these questions quickly:
- Where does the important data live?
- Which components read and write each store?
- Which cache keys or derived records exist, and how are they invalidated?
- What happens to stored state during one representative request?
- Which code, migrations, or runtime inspection points should I check to verify the doc?

The doc should make the system feel inspectable, not mysterious.
A reader should be able to trace one request and understand the resulting stored data without reverse-engineering the whole codebase.
