# Alaa Docs Farsi Full Guide

Use this file when the task spans multiple topics, when you need the complete documentation contract in one place, or when you are updating the split reference files themselves.
Prefer the narrower reference files for normal work so you only load the rules you need.

## Table of contents

- [Purpose](#purpose)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Language requirements](#language-requirements)
- [Hard constraints](#hard-constraints)
- [Repository-safe links in generated documents](#repository-safe-links-in-generated-documents)
- [Documentation graph and internal linking rules](#documentation-graph-and-internal-linking-rules)
- [Link validation workflow](#link-validation-workflow)
- [Standard documentation contract for README and BIG_PICTURE](#standard-documentation-contract-for-readme-and-bigpicture)
- [Standard API summary contract](#standard-api-summary-contract)
- [Standard data architecture, storage, and request-flow contract](#standard-data-architecture-storage-and-request-flow-contract)
- [Standard errors, events, and observability contract](#standard-errors-events-and-observability-contract)
- [Standard subagent workflow for documentation tasks](#standard-subagent-workflow-for-documentation-tasks)
- [How this standard was derived](#how-this-standard-was-derived)
- [Repository sync matrix (what must be updated together)](#repository-sync-matrix-what-must-be-updated-together)
- [AGENTS alignment for active projects](#agents-alignment-for-active-projects)
- [Workflow for producing richer docs](#workflow-for-producing-richer-docs)
- [Output checklist for doc updates](#output-checklist-for-doc-updates)
- [Evidence checks](#evidence-checks)
- [Anti-patterns](#anti-patterns)

# Purpose
Create repository documentation that is implementation-aligned, rich enough to be operationally useful, and deterministic to update across active Ala-style repositories in this workspace.

This guide defines a unified standard for `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` so they stay:
- trustworthy for onboarding,
- practical for troubleshooting,
- complete enough for frontend and backend contract work,
- strong enough for human developers and agents to resume work safely,
- and useful as a reference baseline when building new Ala-style services.

# When to use
- Any task that touches contracts, routes, auth trust boundaries, storage topology, cache behavior, queues or events, setup flow, deployment shape, module structure, errors, or observability.
- Any task that updates `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, `docs/errors-events-observability.md`, architecture docs, or operations docs.
- Any task that standardizes docs across repositories and wants better initial context for maintainers, frontend developers, operators, agents, or new service authors.

# When NOT to use
- Pure code refactors with no documentation implications.
- Pure inline annotation work.
- Postman-only collection or environment maintenance with no Markdown doc work.
- Generic writing tasks that are unrelated to repository truth.

# Language requirements
- Write docs in simple, fluent, correct English unless the user explicitly requests another documentation language.
- The user's chat language does not change the documentation language by itself.
- Do not translate identifiers, enum names, table names, cache-key prefixes, header names, route names, class names, queue names, event names, or payload keys.
- Keep technical tokens exactly as implemented in code, config, migrations, and Postman artifacts.

# Hard constraints
- Do not patch business logic in a docs-only request.
- Every statement must be traceable to source code, config, migrations, schema, tests, current docs, or runtime artifacts.
- Never make an existing strong document weaker, shorter, or more generic unless obsolete content is being removed with proof.
- Keep edits minimal and style-preserving:
  - do not reorder useful sections unless clarity improves,
  - prefer corrections, additions, cross-links, and de-duplication over broad rewrites,
  - preserve high-signal existing sections when they are still accurate.
- If a claim is uncertain, remove ambiguity and add the verification path instead of guessing.
- If you add or refresh any deep-dive doc, also repair README navigation and related doc links in the same task.

# Repository-safe links in generated documents
- All document links must be repo-portable: valid after clone, valid in GitHub or GitLab web viewers, and independent of the local machine path.
- Never use local filesystem absolute paths such as `D:/...`, `C:\...`, `/home/...`, or `file:///...` in generated Markdown or documentation.
- Use repository-valid Markdown links only for files inside the same repository.
- Use POSIX-style separators (`/`) only. Never use Windows backslashes (`\`) in links.
- Prefer relative links from the current document location such as `./file.md`, `../file.md`, or `../../platform/openfga/model.fga`.
- Before finalizing a document, validate every local Markdown link against the repository tree:
  - confirm the target exists in the repo,
  - confirm the relative path is correct from the current document directory,
  - confirm any heading anchor points at a real heading.
- If a correct Markdown link cannot be guaranteed, fall back to a plain inline code path such as `platform/openfga/model.fga` instead of inventing a broken hyperlink.
- Correct examples:
  - `OpenFGA model -> ../../platform/openfga/model.fga`
  - `Data architecture -> ./data-architecture.md#representative-request-walkthrough`
  - `platform/openfga/model.fga`
- Incorrect examples:
  - `model.fga -> D:/repo/platform/openfga/model.fga`
  - `model.fga -> C:epo\platform\openfga\model.fga`
  - `model.fga -> file:///D:/repo/...`

# Documentation graph and internal linking rules
- `README.md` is the navigation hub. It should link to every major doc a new maintainer must read next.
- `docs/BIG_PICTURE.md` is the architecture and runtime map. It should summarize and point to deeper docs rather than copy every table, cache key, event, or error matrix.
- `docs/api-summary.md` should link back to `README.md` and `docs/BIG_PICTURE.md`, and optionally to the deep-dive docs when those links materially help a caller understand side effects, storage, or error behavior.
- `docs/data-architecture.md` should link to `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md` when API requests drive the walkthrough, and `docs/errors-events-observability.md` when async handoff or correlation matters.
- `docs/errors-events-observability.md` should link to `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md` when error contracts are caller-visible, and `docs/data-architecture.md` when event payloads or failures depend on stored state.
- Prefer a small `Related docs` or `See also` block near the top or end of each doc rather than repeating long navigation paragraphs.
- When two docs overlap, keep the summary in the broader doc and the full detail in the narrower doc.

# Link validation workflow
- Resolve every local Markdown link before finishing.
- Validate same-file heading anchors as well as cross-file heading anchors when they are used.
- When Python is available, run `python scripts/check_markdown_links.py <repo-root> --files ...` against the touched docs.
- If Python is not available, verify the path and heading manually before keeping the link.
- If a link target is intentionally missing because the repo does not have that doc yet, create the doc or remove the link. Do not leave aspirational broken links in committed documentation.

# Standard documentation contract for README and BIG_PICTURE
## Audience and outcome requirements
The documentation set must serve all of these readers at the same time:

- **Human maintainer**
  - Must understand repo purpose, boundaries, runtime shape, safe edit zones, and the validation path.
- **Frontend developer**
  - Must understand request flows, headers, auth state assumptions, endpoint families, response or error patterns, and which docs to read next.
- **Coding agent**
  - Must get a fast initial mental model, source-of-truth file map, common caveats, and the correct order for deeper inspection.
- **New service author**
  - Must be able to infer Ala conventions for trust boundaries, response contracts, data flow, observability, deployment modes, and documentation structure.

If a rewrite improves one audience while making the doc less useful for the others, the rewrite is incomplete.

## Richness protection rule
When updating an existing `README.md` or `docs/BIG_PICTURE.md`:

- Preserve high-signal details already present:
  - payload examples,
  - enum tables,
  - request variants,
  - trust and header details,
  - queue or outbox flow notes,
  - storage and cache notes,
  - logging and SOC flow notes,
  - deployment-mode differences,
  - known caveats and operator notes.
- Standardize structure without flattening service-specific knowledge.
- If a repo already exceeds the baseline in a useful way, keep the richer coverage and map it under the standard instead of deleting it.

## Deep-dive companion docs
When the repository warrants them, the documentation set uses separate deep-dive docs alongside `README.md` and `docs/BIG_PICTURE.md`:

- `docs/data-architecture.md`
  - storage topology, tables or collections, cache inventory, data-structure notes, and one representative request walkthrough tied to persisted state.
- `docs/errors-events-observability.md`
  - error contracts, event inventory, payload notes, logging, tracing, metrics, alerts, and troubleshooting evidence.

Role boundaries:
- `README.md` tells the reader what to read next.
- `docs/BIG_PICTURE.md` gives the summary map and links outward.
- Deep-dive docs hold the dense, topic-specific detail.

Do not copy the full deep-dive content into `README.md` or `docs/BIG_PICTURE.md`. Summarize and link instead.

## Required sections in README (minimum baseline)
1. **Project summary**
   - Explain what the repo does and what it does not own.
2. **Ownership and runtime truth**
   - Stack, service role, runtime modes, deployment shape, and health or readiness model.
3. **How to run locally**
   - Setup, install, build, lint, test, and strict prerequisites.
4. **API or client contract surface**
   - Route families, API versions, entrypoint differences, and where deeper contracts live.
5. **Trust and authentication contract**
   - Required headers, tokens or cookies, identity propagation, and tenant assumptions.
6. **Integration notes**
   - Frontend flows, backend integration notes, sample request or response expectations, and practical caveats.
7. **Observability and troubleshooting**
   - Key logs, traces, metrics, verification commands, and operational artifacts.
8. **Documentation links**
   - `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, `docs/errors-events-observability.md`, Postman, runbooks, ADR or decision docs, and service-specific references when they exist.
   - Use repository-safe relative Markdown links for repo files. Do not use machine-local absolute paths.

## README quality bar
`README.md` should answer these questions quickly:

- What is this repo responsible for?
- What should a new developer read next?
- How do I run it locally?
- Which runtime modes or environments matter?
- How do auth and trust work at a high level?
- Where are the main contracts, storage notes, and operational artifacts?

`README.md` should be concise, but not shallow.
It may be shorter than `docs/BIG_PICTURE.md`, but it must still be useful without prior repo knowledge.

## Required sections in docs/BIG_PICTURE.md (minimum baseline)
1. **Repository orientation**
   - Purpose, scope, ownership boundaries, and why the repo exists.
2. **System boundary and trust model**
   - Trusted headers, gateway or auth boundaries, tenant context, failure assumptions, and non-negotiable trust rules.
3. **Runtime and topology**
   - Process stack, data stores, queue or storage or cache topology, runtime modes, and environment differences.
4. **Flow map**
   - Request lifecycle and key call paths with small Mermaid diagrams when practical.
5. **API and data contract**
   - Public or internal or admin surface families, common request or response contracts, important headers, and critical enums or lookups.
6. **Domain model and rulebook**
   - Key entities, invariants, state transitions, rule boundaries, and validation expectations.
7. **Frontend integration**
   - Bootstrap order, payload families, important user flows, auth-refresh assumptions, and error-handling expectations.
8. **Events, queues, and side effects**
   - Jobs, listeners, outbox, notifications, schedulers, and observability hooks.
9. **Operations and safety playbooks**
   - Local runbook, safe change playbooks, known caveats, hotspots, and rollback or revalidation expectations.
10. **Source-of-truth map**
   - Exact files that must be checked before documenting route, behavior, auth, storage, deployment, error, event, or observability changes.
11. **Related deep-dive docs**
   - Link to `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` when they exist.

## BIG_PICTURE quality bar
`docs/BIG_PICTURE.md` should let a developer or agent answer these questions without deep code reading:

- What are the main runtime components and how do they connect?
- Which trust-boundary rules are non-negotiable?
- Which request families exist and how do they differ?
- Which stores, caches, events, jobs, or logging pipelines matter?
- Which modules or layers are responsible for what?
- Which caveats and hotspots are likely to cause regressions?
- Which files and docs are the real sources of truth for each topic?

This file may be long when the system is complex.
Prefer high-signal depth over generic summaries.

## Diagram and flow coverage requirements
`docs/BIG_PICTURE.md` must include diagrams for all major behavioral families that exist in the repo:

1. **Request flow**
   - Include at least one diagram for the main request path.
   - Add a variant when auth or trust behavior changes by route family or caller type.
2. **Async and event flow**
   - Include event emit or consume or job flow when the service uses outbox, queues, notifications, or schedulers.
3. **Error and observability flow**
   - Include correlation path covering `request-id`, `traceparent`, logs, metrics, tracing, and SOC or monitoring handoff when implemented.
4. **Deployment or runtime flow**
   - Add one topology diagram when route or runtime behavior differs by local Docker, shared Docker, Swarm, Helm, or Kubernetes mode.

If a deep-dive doc exists, `docs/BIG_PICTURE.md` may keep the diagram small and link to the detailed companion doc instead of duplicating every storage state snapshot or event payload detail.

Preferred Mermaid types:
- `flowchart LR` or `flowchart TD` for request, topology, and mode mapping.
- `sequenceDiagram` when call order or actor handoff matters.

Diagram quality rules:
- Keep labels short and stable, using canonical identifiers exactly as code uses, such as `X-Project-Id`, `POST /api/...`, queue names, event class names, cache-key prefixes, and table names.
- Keep a small local legend only when necessary.
- Do not include speculative systems that are not verified in source config or code.
- Prefer multiple focused diagrams over one oversized diagram that hides important behavior.
- When flow differs by role, runtime mode, or trust path, add separate diagrams or explicit variants.

## Architectural patterns section
When a repo has significant structure, add a short **Coding Patterns and Module Map** section that includes:
- layer map such as `Http/Controller -> Service/Usecase -> Repository/Model -> DB/Queue`,
- boundary rules between route group, middleware, service, queue worker, and observer or listener layers,
- module decomposition strategy used in the repo, such as `packages`, bounded domains, feature modules, or route groups,
- reuse rules explaining where to extend existing modules before creating new files,
- hard `Do Not` patterns observed in the codebase, such as mixed auth paths, duplicated tenant checks, or stateful singleton misuse,
- cross-service touchpoints with explicit file anchors or doc references.

Recommended minimum subsection list:
- `Request or route boundary`
- `Authorization and trusted headers boundary`
- `Async or event boundary`
- `Storage or cache boundary`
- `Frontend-facing contract boundary`

## Frontend integration coverage requirements
When the repo exposes frontend-consumed APIs, the docs must clearly cover:

- entrypoint families and path prefixes,
- required headers, cookies, and auth-refresh assumptions,
- common success and error envelope patterns,
- order of frontend bootstrap calls,
- main user flows such as sign-in, list or detail, create or update, upload, and retry or error handling,
- links to payload examples, enum references, Postman artifacts, and the deeper docs that explain storage or error side effects.

Frontend developers should not need to infer basic contract rules by reverse-engineering controllers.

## New-service baseline extraction
When a repo is mature enough to act as a pattern source, the docs should expose the conventions a new Ala-style service should copy:

- trust boundary and header handling,
- route grouping and API versioning conventions,
- response envelope and resource-serialization rules,
- data-flow and cache-invalidation conventions,
- observability and correlation conventions,
- deployment mode distinctions,
- documentation cross-linking expectations,
- safe-change and done-means expectations.

If these conventions exist only implicitly in code, surface them explicitly in the docs.

## Shared section extensions
When relevant, add these explicitly:
- `Deployment modes` with explicit differences such as local Docker vs shared infra vs Helm or Kubernetes vs Swarm.
- `Known implementation caveats` and `High-risk hotspots`.
- `Change checklist` for safe PR-level behavior edits.
- `Documentation and contract maintenance` with explicit refresh triggers.
- `Detailed payload examples`, `enum references`, `resource shapes`, `storage tables`, `cache key inventories`, or `ops notes` when the system complexity justifies them.

# Standard API summary contract
## API summary purpose
For repositories that expose HTTP APIs, `docs/api-summary.md` is the fast contract sheet for humans and agents who need the endpoint map and a few verified request examples without reading a full Postman collection, OpenAPI document, `README.md`, or `docs/BIG_PICTURE.md`.

This file complements the broader docs set:
- `README.md` remains the onboarding and operational entrypoint.
- `docs/BIG_PICTURE.md` remains the architecture and runtime contract map.
- `docs/data-architecture.md` remains the storage and state walkthrough when the repo has meaningful persistence.
- `docs/errors-events-observability.md` remains the concrete error, event, and observability map when the repo has that surface.
- `docs/api-summary.md` remains the concise endpoint-and-request example sheet.

Do not merge these roles together.

## When docs/api-summary.md is required
Create or refresh `docs/api-summary.md` when all of the following are true:
- the repository owns or exposes HTTP API routes,
- those routes matter to frontend clients, external callers, internal services, operators, or future agents,
- and the route surface is large enough that a concise summary improves navigation and maintenance.

Typical triggers:
- route additions, removals, renames, or version-prefix changes,
- new action endpoints such as `/like`, `/pin`, `/lock`, `/flags`, or similar state transitions,
- request-body or query-parameter changes,
- path-parameter changes,
- auth or caller-surface changes that affect how clients call the API,
- stale examples in an existing `docs/api-summary.md`.

Skip `docs/api-summary.md` only when the repository truly has no meaningful HTTP API surface.

## Required structure for docs/api-summary.md
Use this exact high-level structure unless the user explicitly asks for another format:

1. `# <Service or Domain> API Summary`
2. A flat endpoint inventory as Markdown bullets using inline code, one entry per `METHOD /path`
3. `## Examples` or `## Examples (base host: \`...\`)`
4. A numbered list of representative requests
5. For any request that accepts a body:
   - a `Body:` label
   - a fenced `json` block with a realistic minimal example
6. A short `See also` block when local links materially help the reader navigate to deeper docs

Prefer the project or service name for the title, such as `Comment API Summary`, `Gateway API Summary`, or `Ticket API Summary`.

## API summary formatting rules
- Keep the endpoint inventory concise and scannable:
  - one bullet per canonical endpoint,
  - use route templates with placeholders such as `{comment}` or `{ticketRef}`,
  - group closely related endpoints together,
  - insert a blank line between distinct route families when that improves scanning.
- Keep paths canonical in the inventory:
  - include the real version prefix such as `/api/v1/...` when it exists,
  - keep placeholder names aligned with the actual route names,
  - do not substitute real IDs into the inventory list.
- Keep examples concrete:
  - show realistic path values and query strings,
  - keep example payloads minimal but valid,
  - use the real request field names from validation or controllers,
  - use empty `{}` only when the endpoint genuinely expects no payload.
- Prefer concise coverage when many endpoints share one pattern:
  - keep the full endpoint inventory even if example coverage is abbreviated,
  - show one full example for a repeated action family when that example teaches the calling pattern,
  - add a short guidance line or mini-template for the sibling endpoints instead of repeating near-identical examples.
- Include `base host` in the `## Examples` heading only when that host and port are verified from repo sources such as README, env examples, Docker or Compose, test fixtures, or existing docs.
- Exclude boilerplate operational endpoints such as health, readiness, or metrics unless the user explicitly asks to include them or they are part of the main consumed API surface.
- Do not dump response bodies by default. Add response examples only when they are unusually important to using the route correctly.
- If endpoint semantics depend on storage shape, event side effects, or a nuanced error contract, add a one-line note that points to the deeper doc instead of copying the whole deep-dive section.

## API summary example-selection rules
Model `docs/api-summary.md` after the same pattern as the comment-service example:
- start with the primary collection and item endpoints,
- include the most important action-style subroutes,
- include at least one read example and the key write examples,
- include one example per materially different body shape,
- prefer examples that help a frontend or integration developer understand how to call the API immediately.
- When many action endpoints are structurally repetitive, it is acceptable and often better to:
  - document one representative action endpoint fully,
  - then add a compact note such as `Other action endpoints in this family follow the same path shape and usually accept either an empty body or one small state field.`,
  - and optionally list a tiny template like ``POST /api/.../{resource}/{action}`` under that note.

For CRUD-style APIs, the default representative set is:
- list or search,
- create,
- update or patch,
- delete,
- and any domain-specific action endpoints.

For action-heavy APIs, include the important business actions even if they are not CRUD, such as moderation, publish, approve, retry, assign, or state toggles.

When an existing `docs/api-summary.md` already has useful examples, preserve the strongest ones and update only what is stale or incomplete.

## API summary quality bar
`docs/api-summary.md` is good when a developer or agent can answer these questions quickly:
- Which consumer-facing endpoints exist?
- Which route parameters and path shapes are canonical?
- Which request bodies are expected for the important write paths?
- Which action endpoints exist beyond basic CRUD?
- What is the verified local example host, if the repo documents one?
- Which deeper doc should I read next when I need storage, event, or error detail?

The file should feel compact, current, and source-backed.
It should not read like generated sludge, and it should not try to replace richer docs or Postman collections.

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

# Standard errors, events, and observability contract
## Why this doc exists
`docs/errors-events-observability.md` is the concrete operations and side-effects map for a repository.
It should tell the reader which caller-visible errors exist, where they are generated or mapped, which events or jobs fire, what payload data moves through them, which logs or traces or metrics are emitted, and how to verify the behavior during troubleshooting.

This doc is separate because `docs/BIG_PICTURE.md` should summarize the flow map, not carry every exception class, event payload, log field, and troubleshooting path.

## When docs/errors-events-observability.md is required
Create or refresh `docs/errors-events-observability.md` when one or more of these are true:
- the repository exposes meaningful HTTP, RPC, CLI, or job error contracts,
- the code emits domain events, integration events, queued jobs, notifications, or scheduler-driven side effects,
- the system relies on structured logging, tracing, metrics, alerting, or SOC-style evidence,
- changes to handlers, events, listeners, logging, tracing, or failure mapping would otherwise make the docs misleading.

Skip this doc only for simple libraries or tools with no meaningful runtime or operational surface.
If you skip it, keep that choice explicit in `README.md` or `docs/BIG_PICTURE.md` when the repo structure could make a reader expect it.

## Default filename and preservation rule
- Use `docs/errors-events-observability.md` for new work.
- If the repository already has a stronger equivalent doc under another verified name, update that file instead of creating a duplicate.
- When you preserve an existing filename, repair README and cross-links so the documentation graph still makes the role of the doc obvious.

## Separation from README, BIG_PICTURE, data-architecture, and api-summary
- `README.md` stays the onboarding and navigation entrypoint.
- `docs/BIG_PICTURE.md` stays the architecture and runtime summary map.
- `docs/api-summary.md` stays the concise endpoint inventory and request-example sheet.
- `docs/data-architecture.md` stays the storage and state walkthrough.
- `docs/errors-events-observability.md` holds the detailed error matrix, event inventory, payload notes, logging or tracing or metrics paths, alerts, and troubleshooting evidence.

Do not turn this doc into a second API summary, a second data-architecture doc, or a second BIG_PICTURE.

## Required structure for docs/errors-events-observability.md
Use this default structure unless the repository shape clearly needs a tighter variant:

1. `# <Service or Domain> Errors, Events, and Observability`
2. `## Purpose and scope`
3. `## Source-of-truth map`
4. `## Error contract matrix`
5. `## Representative error flows`
6. `## Event inventory`
7. `## Event payload notes`
8. `## Logging and correlation fields`
9. `## Traces, metrics, alerts, and evidence paths`
10. `## Flow diagrams`
11. `## Troubleshooting and verification notes`
12. `## See also`

Typical error-matrix columns:
- surface,
- trigger,
- producer or mapper,
- HTTP or RPC or job outcome,
- stable error code or key,
- caller action or retry note,
- observability note.

Typical event-inventory columns:
- name,
- producer,
- trigger,
- sync or async,
- transport or storage,
- consumers,
- payload fields,
- idempotency or ordering note,
- failure handling,
- observability note.

## Error contract coverage rules
- Cover the meaningful failure families that the repo actually implements: auth or trust, validation, not-found, conflict, business-rule violations, rate-limit or quota, dependency failure, infrastructure failure, async or job failure, and any custom domain error families.
- Use the real response envelope, exception mapping, serializer, or job-failure contract from the code or docs.
- Include exact status codes, stable error keys, or enum names only when verified.
- Show a minimal example when the error shape is important to callers.
- Explain where the error is produced or mapped and what a caller or operator should do next.
- Do not invent errors that merely seem likely.

## Event inventory rules
- Include domain events, integration events, queued jobs, outbox rows, notifications, scheduler triggers, and other side-effect signals that materially affect system behavior.
- For each event or job, state when it fires, who emits it, who consumes it, what payload fields matter, and what happens on failure.
- Distinguish synchronous dispatch from async dispatch.
- Distinguish the business trigger from the transport or storage mechanism.
- Note ordering, idempotency, retry, dead-letter, or deduplication rules only when verified.
- If the repo truly has no such events, say that explicitly instead of leaving the section vague.

## Observability coverage rules
- List the structured log families or major log points that help operators verify the main flows.
- Include correlation and context fields such as `request-id`, `traceparent`, tenant identifiers, actor identifiers, event identifiers, or job identifiers only when they are verified.
- Map important traces, spans, metrics, dashboards, alerts, or SOC evidence paths when they exist.
- State where logs or traces land only when the repo or docs actually verify that destination.
- Include the practical search or verification path: which logger, middleware, config, or dashboard the reader should inspect next.

## Diagram and flowchart rules
- Include at least one focused diagram for a representative error path from request or job trigger to mapping and observability output.
- Include at least one focused diagram for event fire and consume flow when the repo has event or job behavior.
- Include a correlation-path diagram when tracing and logging and metrics are part of the implementation.
- Use `flowchart LR`, `flowchart TD`, or `sequenceDiagram` depending on whether topology or call order matters more.
- Keep labels canonical and short: use verified route names, error keys, event names, logger names, metric names, and queue names.
- Prefer several small diagrams over one diagram that mixes unrelated failure families.

## Errors, events, and observability quality bar
`docs/errors-events-observability.md` is good when a developer or agent can answer these questions quickly:
- Which errors exist and how are they surfaced?
- Where is each important error produced or mapped?
- Which events or jobs fire, where, and with what payload?
- Which logs, traces, metrics, alerts, or evidence paths should I inspect?
- How do I follow one failure from trigger to operational evidence?

The doc should make failures and side effects understandable and debuggable.
A reader should not need to grep the whole repo just to learn which event fires or which log to search for a failure.

# Standard subagent workflow for documentation tasks
## Why subagents help this skill
Documentation-alignment work is usually broad, read-heavy, and naturally separable: one track explores routes and caller contracts, another inspects storage and cache behavior, another traces errors and events and logs, and another checks the document graph.

Subagents help by keeping each discovery track bounded, reducing context pollution in the parent thread, and letting the parent agent receive distilled findings instead of raw repo noise. Use them to gather context faster, not to create uncontrolled parallel edits.

## When to use subagents
Use explicit parallel subagents when one or more of these are true:
- the repository is large enough that one agent would spend too long exploring before writing,
- the task spans several docs such as `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md`,
- the relevant source-of-truth files are spread across independent surfaces such as routes, storage, and observability,
- you need a broader fact base before deciding the final wording or document split.

## When NOT to use subagents
Avoid subagents when:
- the task is a small single-file touch-up,
- the next step depends tightly on the previous result and parallel work would just idle or conflict,
- the work is write-heavy and multiple agents would likely edit the same file,
- the environment does not support explicit subagent spawning.

## Parent-agent responsibilities
The parent agent owns the workflow and final output. It must:
- decide which docs are in scope,
- decide whether the task is large enough for subagents,
- explicitly ask Codex to spawn the subagents,
- define the work split, whether Codex should wait for all results, and what each subagent must return,
- reconcile conflicting findings,
- write the final docs or assign isolated follow-up edits with a clear merge owner,
- run final validation.

## Recommended subagent split
For a broad repository-doc refresh, start with four read-heavy tracks:

1. **Doc graph and entrypoints**
   - Scope: current `README.md`, `docs/BIG_PICTURE.md`, existing deep-dive docs, and internal link graph.
   - Output: navigation gaps, broken links, duplicated sections, and required README or BIG_PICTURE updates.

2. **API surface and caller contracts**
   - Scope: routes, validation, controllers, serializers, auth middleware, and Postman or OpenAPI artifacts.
   - Output: canonical endpoint inventory, request-shape changes, caller-visible headers, and `docs/api-summary.md` recommendations.

3. **Storage and request flow**
   - Scope: migrations, schema, models or entities, repositories, cache helpers, outbox or read models, and one representative request path.
   - Output: store inventory, key tables or collections, cache namespaces, lifecycle or invalidation rules, and `docs/data-architecture.md` recommendations.

4. **Errors, events, and observability**
   - Scope: exception handlers, error resources, event classes, listeners, jobs, schedulers, logging, tracing, metrics, alerts, and dashboards or runbooks when available.
   - Output: error matrix candidates, event inventory, payload notes, log or trace fields, and `docs/errors-events-observability.md` recommendations.

Add a fifth subagent for final cross-checking or link validation only when the repo is especially large or the doc graph is messy.

## Return contract for each subagent
Each subagent should return a compact, source-backed handoff with:
- source-of-truth files checked,
- concrete findings and verified claims,
- exact docs and sections that should change,
- minimal proposed headings, bullets, or examples to add,
- uncertainties that still need direct verification,
- file references for the parent agent.

Default rule: subagents should not edit files. They should gather evidence and propose updates unless the parent agent delegates one isolated file with no overlap risk.

## Merge and conflict-resolution rules
- The parent agent is the merge owner for final wording.
- When two subagents disagree, prefer code, config, migrations, tests, and runtime artifacts over stale docs.
- If the disagreement remains unresolved, keep the doc precise about the uncertainty and include the verification path instead of guessing.
- Do not let multiple subagents edit the same Markdown file concurrently.
- If you do delegate writing, split ownership by file, not by overlapping sections of the same file.

## Example parent prompts
Use prompts like these from the parent thread when the environment supports subagents:

```text
Use parallel subagents for this documentation refresh. Spawn four read-only subagents and wait for all results before writing.
1) Doc graph and README/BIG_PICTURE gaps
2) API surface and caller contracts
3) Storage, tables, cache, and one representative request flow
4) Errors, events, logs, traces, and observability
Each subagent must return: source-of-truth files checked, verified findings, exact docs or sections that should change, and unresolved questions. Do not edit files. I will consolidate and write the final docs in the parent thread.
```

```text
Use one explorer subagent per documentation surface. Wait for all of them, then merge the findings into `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` as needed. Keep all writes in the parent thread unless a delegated file is fully isolated.
```

## Custom-agent guidance
If the project or user has custom agents under `.codex/agents/` or `~/.codex/agents/`, prefer the one whose description best matches the track, such as a doc explorer, API cartographer, storage mapper, or observability reviewer.

If no custom agent fits, start with built-in roles this way:
- `explorer` for read-heavy discovery and evidence gathering,
- `default` for general follow-up when no sharper role exists,
- `worker` for isolated deterministic validation or implementation follow-up after the evidence is already gathered.

## Validation after subagent work
After all subagents return:
1. Reconcile overlaps and contradictions in the parent thread.
2. Write or update the docs serially with one clear merge owner per file.
3. Re-open the changed docs and verify the links between them.
4. Run `scripts/check_markdown_links.py` when Python is available.
5. Re-check the output checklist in `references/40-sync-workflow-and-evidence.md`.

# How this standard was derived
This standard is grounded in the richest docs across active Ala-style projects in this workspace, especially:
- `auth`
- `comment-service`
- `gateway`
- `ticket`
- `vod`
- `wa`
- `entekhabat-front`

# Repository sync matrix (what must be updated together)
When a change touches:

- **Routes, ports, middleware, or service map**
  - update `docs/BIG_PICTURE.md`, `README.md`, `docs/api-summary.md` when the repo exposes APIs, and source mapping files.
- **Auth or header trust boundaries**
  - update `docs/BIG_PICTURE.md`, `README.md`, `docs/api-summary.md` when caller usage changes, and middleware or config references.
- **Storage shape, tables, collections, cache rules, or request-state walkthroughs**
  - update `docs/data-architecture.md`, `docs/BIG_PICTURE.md`, `README.md`, and any linked schema or migration references.
- **API contracts, payload fields, enums, or caller-visible errors**
  - update `docs/BIG_PICTURE.md`, `README.md`, `docs/api-summary.md`, `docs/errors-events-observability.md`, and Postman or API artifact references.
- **Queues, events, schedulers, notifications, listeners, or outbox flows**
  - update `docs/BIG_PICTURE.md`, `docs/errors-events-observability.md`, `docs/data-architecture.md` when storage handoff matters, and any operations notes.
- **Logging, tracing, metrics, alerting, or SOC evidence**
  - update `docs/errors-events-observability.md`, `docs/BIG_PICTURE.md`, `README.md`, and runtime or dashboard references.
- **Deployment or local-runtime assumptions**
  - update `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md` when the example base host changes, and runbook or Helm or Docker sources.
- **Module boundaries or architecture patterns**
  - update `docs/BIG_PICTURE.md`, module maps, and any linked design docs.
- **Documentation filenames or internal links**
  - update `README.md`, every touched deep-dive doc, and validate the full local Markdown link graph.

If one of the paired docs changes, the other affected docs must still be reviewed in the same task.

# AGENTS alignment for active projects
- Several project `AGENTS.md` files explicitly require reading `docs/BIG_PICTURE.md` and `README.md` before work.
- They also require updating those files when behavior, auth, runtime, routes, storage, or operations shift.
- Reusable rule: always document runtime-mode differences explicitly.
- Reusable rule: when backend and gateway assumptions differ by deployment, keep both claims explicit and linked to source files.
- Reusable rule: when deep-dive docs exist, `README.md` should still remain the navigation hub.

# Workflow for producing richer docs
1. Read repository-local `AGENTS.md`.
2. Read the current `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` before planning edits when they exist.
3. Identify the richest useful sections already present and preserve them.
4. Verify behavior from code, config, route definitions, validation rules, exception handlers, events, listeners, migrations, models, cache helpers, and source-of-truth docs before editing claims.
5. Fill coverage gaps for all four audiences:
   - maintainer,
   - frontend developer,
   - coding agent,
   - new service author.
6. When the repository is large or the task spans several docs, explicitly spawn parallel, mostly read-only subagents for the independent tracks described in `references/70-subagent-doc-workflows.md`, then wait for all results before writing.
7. For API repositories, create or refresh `docs/api-summary.md` using the standardized endpoint inventory plus numbered request-examples format.
8. For stateful repositories, create or refresh `docs/data-architecture.md` with storage topology, inventory tables, cache notes, and one representative request walkthrough tied to stored state.
9. For repos with meaningful error, event, or observability surface, create or refresh `docs/errors-events-observability.md` with error matrices, event inventory, payload notes, and troubleshooting evidence.
10. Add or refresh diagrams, module maps, flowcharts, and state snapshots where the current docs are too thin.
11. Re-check cross-links to Postman, runbooks, ADR or decision docs, and service-specific references, and validate every repo-local Markdown link against the repository tree.
12. Before finishing, confirm the new docs are richer or clearer than before, not just more standardized.

# Output checklist for doc updates
For every documentation update, report:
1. Files changed.
2. Triggered change type such as auth, runtime, API, storage, architecture, ops, errors, events, or observability.
3. Source-of-truth files verified.
4. `docs/api-summary.md` created, refreshed, or intentionally not needed.
5. `docs/data-architecture.md` created, refreshed, reused under another filename, or intentionally not needed.
6. `docs/errors-events-observability.md` created, refreshed, reused under another filename, or intentionally not needed.
7. Postman artifacts updated or intentionally kept in sync.
8. Subagents used or intentionally skipped, with owned tracks.
9. Internal Markdown links validated.
10. Remaining uncertain areas, if any.

# Evidence checks
- Use `rg` or equivalent heading and identifier checks for contract terms such as headers, routes, enums, queues, event names, table names, cache-key prefixes, logger names, and runtime modes.
- Check source code, migrations, schema, or config for each changed assertion.
- Verify that `README.md` and `docs/BIG_PICTURE.md` still have matching coverage for shared topics.
- Verify that `docs/api-summary.md` still matches the current route inventory and request shapes when the repository exposes APIs.
- Verify that `docs/data-architecture.md` still matches the current stores, table or collection names, cache behavior, and representative request flow when the repository has meaningful persisted state.
- Verify that `docs/errors-events-observability.md` still matches the current error handlers, event inventory, payload notes, and observability paths when the repository has that surface.
- Resolve each local Markdown link against the repository tree before finalizing the document. Use `scripts/check_markdown_links.py` when available.
- Reconcile conflicting subagent findings against source-of-truth files before editing final docs.
- Verify that existing useful sections were preserved or intentionally replaced with stronger coverage.

# Anti-patterns
- Copying contract claims that cannot be verified by source artifacts.
- Mixing runtime-mode assumptions without explicit labels.
- Adding broad detail while skipping source-of-truth references.
- Inventing performance or security guarantees without proof.
- Translating or renaming technical identifiers.
- Replacing a concrete service map with vague high-level architecture language.
- Creating a deep-dive doc full of guessed table names, payload fields, or event flows.
- Duplicating `docs/api-summary.md`, `docs/data-architecture.md`, or `docs/errors-events-observability.md` verbatim into `README.md` or `docs/BIG_PICTURE.md`.
- Letting multiple subagents edit the same documentation file concurrently without a clear merge owner.
- Using machine-local absolute paths, Windows-style backslashes, or unverified relative links in generated Markdown links.
