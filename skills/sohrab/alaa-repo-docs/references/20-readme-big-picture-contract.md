# README and BIG_PICTURE contract

## Core rule

`README.md` is the onboarding and operations entrypoint.
`docs/BIG_PICTURE.md` is the operational and architecture contract map.

They must not become duplicates.
For any service or project where both exist, review both in the same task when behavior, trust, API shape, storage shape, deployment expectations, or operating assumptions change.

## Audience and outcome requirements

The documentation set must serve all of these readers at the same time:

- **Human maintainer** — repository purpose, boundaries, runtime shape, safe edit zones, and the validation path.
- **Frontend developer** — request flows, headers, auth-state assumptions, endpoint families, response and error patterns, and which document to read next.
- **Coding agent** — a fast initial mental model, a source-of-truth file map, common caveats, and the correct order for deeper inspection.
- **New service author** — the Ala conventions for trust boundaries, response contracts, data flow, observability, deployment modes, and documentation structure.

If a rewrite improves one audience while making the document less useful for the others, the rewrite is incomplete and must not ship in that state.

## Richness protection rule

When updating an existing `README.md` or `docs/BIG_PICTURE.md`:

- Preserve high-signal details already present: payload examples, enum tables, request variants, trust and header details, queue or outbox flow notes, storage and cache notes, logging and SOC flow notes, deployment-mode differences, and known caveats or operator notes.
- Standardize structure without flattening service-specific knowledge.
- If a repository already exceeds this baseline in a useful way, keep the richer coverage and map it under the standard instead of deleting it.

## Role boundaries against the deep-dive documents

- `README.md` tells the reader what to read next.
- `docs/BIG_PICTURE.md` gives the summary map and links outward.
- `docs/data-architecture.md` and `docs/errors-events-observability.md` hold the dense, topic-specific detail.

Do not copy deep-dive content into `README.md` or `docs/BIG_PICTURE.md`. Summarize and link instead.

## Required sections in README (minimum baseline)

1. **Project summary** — what the repository does and what it does not own.
2. **Ownership and runtime truth** — stack, service role, runtime modes, deployment shape, and the health or readiness model.
3. **How to run locally** — setup, install, build, lint, test, and strict prerequisites.
4. **API or client contract surface** — route families, API versions, entrypoint differences, and where deeper contracts live.
5. **Trust and authentication contract** — required headers, tokens or cookies, identity propagation, and tenant assumptions.
6. **Integration notes** — frontend flows, backend integration notes, sample request or response expectations, and practical caveats.
7. **Observability and troubleshooting** — key logs, traces, metrics, verification commands, and operational artifacts.
8. **Documentation links** — `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, `docs/errors-events-observability.md`, Postman, runbooks, decision records, and service-specific references when they exist, as repository-safe relative links.

## README coverage requirements

`README.md` must answer each of these from the file alone, for a reader with no prior repository knowledge:

- What is this repository responsible for, and what does it explicitly not own?
- What should a new developer read next?
- How do I run it locally, and which prerequisites are strict?
- Which runtime modes or environments change behavior?
- How do authentication and trust work at the boundary?
- Where are the contracts, storage notes, and operational artifacts?

`README.md` may be shorter than `docs/BIG_PICTURE.md`. It may not answer fewer of these questions.

## Required sections in docs/BIG_PICTURE.md (minimum baseline)

1. **Repository orientation** — purpose, scope, ownership boundaries, and why the repository exists.
2. **System boundary and trust model** — trusted headers, gateway or auth boundaries, tenant context, failure assumptions, and non-negotiable trust rules.
3. **Runtime and topology** — process stack, data stores, queue or storage or cache topology, runtime modes, and environment differences.
4. **Flow map** — request lifecycle and key call paths, with small Mermaid diagrams when practical.
5. **API and data contract** — public, internal, and admin surface families, common request and response contracts, important headers, and critical enums or lookups.
6. **Domain model and rulebook** — key entities, invariants, state transitions, rule boundaries, and validation expectations.
7. **Frontend integration** — bootstrap order, payload families, important user flows, auth-refresh assumptions, and error-handling expectations.
8. **Events, queues, and side effects** — jobs, listeners, outbox, notifications, schedulers, and observability hooks.
9. **Operations and safety playbooks** — local runbook, safe-change playbooks, known caveats, hotspots, and rollback or revalidation expectations.
10. **Source-of-truth map** — the exact files to check before documenting a route, behavior, auth, storage, deployment, error, event, or observability change.
11. **Related deep-dive docs** — links to `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` when they exist.

## BIG_PICTURE coverage requirements

`docs/BIG_PICTURE.md` must answer each of these without the reader opening any code:

- Which runtime components exist and how do they connect?
- Which trust-boundary rules are non-negotiable?
- Which request families exist and how do they differ?
- Which stores, caches, events, jobs, or logging pipelines matter?
- Which modules or layers own what?
- Which caveats and hotspots have caused regressions before?
- Which files and documents are the real source of truth for each topic?

This file may be long when the system is complex. Length is not the constraint; an unanswered question is.

## Diagram and flow coverage requirements

`docs/BIG_PICTURE.md` must include a diagram for every major behavioral family the repository actually implements:

1. **Request flow** — at least one diagram for the main request path, plus a variant when auth or trust behavior differs by route family or caller type.
2. **Async and event flow** — event emit, consume, or job flow when the service uses an outbox, queues, notifications, or schedulers.
3. **Error and observability flow** — the correlation path from request to logs, metrics, tracing, and SOC or monitoring handoff, when implemented. Name correlation headers exactly as `alaa-services-contract references/20-operational-and-observability-contract.md` spells them — `X-Request-Id` and `traceparent` — and never a local variant. Whether a given signal is required at all is `/alaa-observability-soc`'s (`$alaa-observability-soc`) decision.
4. **Deployment or runtime flow** — one topology diagram when route or runtime behavior differs by local Docker, shared Docker, Swarm, Helm, or Kubernetes mode.

When a deep-dive document exists, `docs/BIG_PICTURE.md` may keep the diagram small and link to the companion instead of duplicating every state snapshot or payload detail.

Diagram rules:
- Use `flowchart LR` or `flowchart TD` for request, topology, and mode mapping; `sequenceDiagram` when call order or actor handoff matters.
- Keep labels short and canonical, using the identifiers the code uses, such as `X-Project-Id`, a real route template, queue names, event class names, cache-key prefixes, and table names.
- Do not include a system that is not verified in source or config.
- Prefer several focused diagrams over one oversized diagram that hides behavior.
- When a flow differs by role, runtime mode, or trust path, add a separate diagram or an explicit labelled variant.

## Coding patterns and module map

Add a **Coding Patterns and Module Map** section when the repository has more than one layer. It is complete when it states all six of the following, each anchored to a real file or directory:

1. the layer map, such as `Http/Controller -> Service/Usecase -> Repository/Model -> DB/Queue`,
2. the boundary rule between route group, middleware, service, queue worker, and observer or listener,
3. the module decomposition the repository actually uses, such as packages, bounded domains, feature modules, or route groups,
4. where to extend an existing module before creating a new file,
5. the hard "do not" patterns observed in this codebase, such as a mixed auth path, a duplicated tenant check, or stateful singleton misuse,
6. cross-service touchpoints, each with a file anchor or a document reference.

Cover these five boundaries explicitly: request or route, authorization and trusted headers, async or event, storage or cache, and frontend-facing contract.

## Frontend integration coverage requirements

When the repository exposes frontend-consumed APIs, the documentation set must state:

- entrypoint families and path prefixes,
- required headers, cookies, and auth-refresh assumptions,
- the common success and error envelope patterns,
- the order of frontend bootstrap calls,
- the main user flows, such as sign-in, list or detail, create or update, upload, and retry or error handling,
- links to payload examples, enum references, Postman artifacts, and the deeper documents that explain storage or error side effects.

A frontend developer must not have to reverse-engineer a controller to learn a basic contract rule.

## New-service baseline extraction

When a repository is mature enough to act as a pattern source, state the conventions a new Ala-style service should copy: trust boundary and header handling, route grouping and API versioning, response envelope and serialization rules, data-flow and cache-invalidation conventions, observability and correlation conventions, deployment-mode distinctions, documentation cross-linking expectations, and safe-change expectations.

A convention that exists only implicitly in code is not documented. Surface it explicitly or leave it out.

## Shared section extensions

Add these when the system warrants them: `Deployment modes` with the explicit differences between local Docker, shared infrastructure, Helm or Kubernetes, and Swarm; `Known implementation caveats` and `High-risk hotspots`; a `Change checklist` for safe behavior edits; `Documentation and contract maintenance` with explicit refresh triggers; and `Detailed payload examples`, `enum references`, `resource shapes`, `storage tables`, `cache key inventories`, or `ops notes` when complexity justifies them.
