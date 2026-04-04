# README and BIG_PICTURE contract

## Includes these full-guide sections

- `# Standard documentation contract for README and BIG_PICTURE`
- `## Audience and outcome requirements`
- `## Richness protection rule`
- `## Required sections in README (minimum baseline)`
- `## README quality bar`
- `## Required sections in docs/BIG_PICTURE.md (minimum baseline)`
- `## BIG_PICTURE quality bar`
- `## Diagram and flow coverage requirements`
- `## Architectural patterns section`
- `## Frontend integration coverage requirements`
- `## New-service baseline extraction`
- `## Shared section extensions`

## Standard documentation contract for README and BIG_PICTURE

### Core rule
`README.md` is the onboarding and operations entrypoint.
`docs/BIG_PICTURE.md` is the operational and architecture contract map.

They must not become duplicates.
For any service or project where both exist, review both in the same task when behavior, trust, API shape, deployment expectations, or operating assumptions change.

## Audience and outcome requirements

The documentation set must serve all of these readers at the same time:

- **Human maintainer**
  - Must understand repo purpose, boundaries, runtime shape, safe edit zones, and the validation path.
- **Frontend developer**
  - Must understand request flows, headers, auth state assumptions, endpoint families, response/error patterns, and which docs to read next.
- **Coding agent**
  - Must get a fast initial mental model, source-of-truth file map, common caveats, and the correct order for deeper inspection.
- **New service author**
  - Must be able to infer Ala conventions for trust boundaries, response contracts, observability, deployment modes, and documentation structure.

If a rewrite improves one audience while making the doc less useful for the others, the rewrite is incomplete.

## Richness protection rule

When updating an existing `README.md` or `docs/BIG_PICTURE.md`:

- Preserve high-signal details already present:
  - payload examples,
  - enum tables,
  - request variants,
  - trust and header details,
  - queue or outbox flow notes,
  - logging and SOC flow notes,
  - deployment-mode differences,
  - known caveats and operator notes.
- Standardize structure without flattening service-specific knowledge.
- If a repo already exceeds the baseline in a useful way, keep the richer coverage and map it under the standard instead of deleting it.

## Required sections in README (minimum baseline)

1. **Project summary**
   - Explain what the repo does and what it does not own.
2. **Ownership and runtime truth**
   - Stack, service role, runtime modes, deployment shape, and health/readiness model.
3. **How to run locally**
   - Setup, install, build, lint, test, and strict prerequisites.
4. **API or client contract surface**
   - Route families, API versions, entrypoint differences, and where deeper contracts live.
5. **Trust and authentication contract**
   - Required headers, tokens/cookies, identity propagation, and tenant assumptions.
6. **Integration notes**
   - Frontend flows, backend integration notes, sample request/response expectations, and practical caveats.
7. **Observability and troubleshooting**
   - Key logs, traces, metrics, verification commands, and operational artifacts.
8. **Documentation links**
   - `docs/BIG_PICTURE.md`, Postman, runbooks, ADR/decision docs, and service-specific references.
   - Use repository-safe relative Markdown links for repo files. Do not use machine-local absolute paths.

## README quality bar

`README.md` should answer these questions quickly:

- What is this repo responsible for?
- What should a new developer read next?
- How do I run it locally?
- Which runtime modes or environments matter?
- How does auth and trust work at a high level?
- Where are the main contracts and operational artifacts?

`README.md` should be concise, but not shallow.
It may be shorter than `docs/BIG_PICTURE.md`, but it must still be useful without prior repo knowledge.

## Required sections in docs/BIG_PICTURE.md (minimum baseline)

1. **Repository orientation**
   - Purpose, scope, ownership boundaries, and why the repo exists.
2. **System boundary and trust model**
   - Trusted headers, gateway or auth boundaries, tenant context, failure assumptions, and non-negotiable trust rules.
3. **Runtime and topology**
   - Process stack, data stores, queue/storage/cache topology, runtime modes, and environment differences.
4. **Flow map**
   - Request lifecycle and key call paths with small Mermaid diagrams when practical.
5. **API and data contract**
   - Public/internal/admin surface families, common request/response contracts, important headers, and critical enums/lookups.
6. **Domain model and rulebook**
   - Key entities, invariants, state transitions, rule boundaries, and validation expectations.
7. **Frontend integration**
   - Bootstrap order, payload families, important user flows, auth-refresh assumptions, and error-handling expectations.
8. **Events, queues, and side effects**
   - Jobs, listeners, outbox, notifications, schedulers, and observability hooks.
9. **Operations and safety playbooks**
   - Local runbook, safe change playbooks, known caveats, hotspots, and rollback/revalidation expectations.
10. **Source-of-truth map**
   - Exact files that must be checked before documenting route, behavior, auth, deployment, or observability changes.

## BIG_PICTURE quality bar

`docs/BIG_PICTURE.md` should let a developer or agent answer these questions without deep code reading:

- What are the main runtime components and how do they connect?
- Which trust boundary rules are non-negotiable?
- Which request families exist and how do they differ?
- Which events, jobs, outbox flows, or logging pipelines matter?
- Which modules or layers are responsible for what?
- Which caveats and hotspots are likely to cause regressions?
- Which files are the real source of truth for each topic?

This file may be long when the system is complex.
Prefer high-signal depth over generic summaries.

## Diagram and flow coverage requirements

`docs/BIG_PICTURE.md` must include diagrams for all major behavioral families that exist in the repo:

1. **Request flow**
   - Include at least one diagram for the main request path.
   - Add a variant when auth/trust behavior changes by route family or caller type.
2. **Async and event flow**
   - Include event emit/consume/job flow when the service uses outbox, queues, notifications, or schedulers.
3. **Error and observability flow**
   - Include correlation path covering `request-id`, `traceparent`, logs, metrics, tracing, and SOC/monitoring handoff when implemented.
4. **Deployment/runtime flow**
   - Add one topology diagram when route or runtime behavior differs by local Docker, shared Docker, Swarm, Helm, or Kubernetes mode.

Preferred Mermaid types:
- `flowchart LR` or `flowchart TD` for request, topology, and mode mapping.
- `sequenceDiagram` when call order or actor handoff matters.

Diagram quality rules:
- Keep labels short and stable, using canonical identifiers exactly as code uses, such as `X-Project-Id`, `POST /api/...`, queue names, event class names, and table names.
- Keep a small local legend only when necessary.
- Do not include speculative systems that are not verified in source config or code.
- Prefer multiple focused diagrams over one oversized diagram that hides important behavior.
- When flow differs by role, runtime mode, or trust path, add separate diagrams or explicit variants.

## Architectural patterns section

When a repo has significant structure, add a short **Coding Patterns and Module Map** section that includes:
- layer map such as `Http/Controller -> Service/Usecase -> Repository/Model -> DB/Queue`,
- boundary rules between route group, middleware, service, queue worker, and observer/listener layers,
- module decomposition strategy used in the repo, such as `packages`, bounded domains, feature modules, or route groups,
- reuse rules explaining where to extend existing modules before creating new files,
- hard "Do Not" patterns observed in the codebase, such as mixed auth paths, duplicated tenant checks, or stateful singleton misuse,
- cross-service touchpoints with explicit file anchors or doc references.

Recommended minimum subsection list:
- `Request/route boundary`
- `Authorization and trusted headers boundary`
- `Async/event boundary`
- `Storage/cache boundary`
- `Frontend-facing contract boundary`

## Frontend integration coverage requirements

When the repo exposes frontend-consumed APIs, the docs must clearly cover:

- entrypoint families and path prefixes,
- required headers, cookies, and auth-refresh assumptions,
- common success and error envelope patterns,
- order of frontend bootstrap calls,
- main user flows such as sign-in, list/detail, create/update, upload, and retry/error handling,
- links to payload examples, enum references, and Postman artifacts.

Frontend developers should not need to infer basic contract rules by reverse-engineering controllers.

## New-service baseline extraction

When a repo is mature enough to act as a pattern source, the docs should expose the conventions a new Ala-style service should copy:

- trust boundary and header handling,
- route grouping and API versioning conventions,
- response envelope and resource serialization rules,
- observability and correlation conventions,
- deployment mode distinctions,
- documentation cross-linking expectations,
- safe change and done-means expectations.

If these conventions exist only implicitly in code, surface them explicitly in the docs.

## Shared section extensions

When relevant, add these explicitly:
- `Deployment modes` with explicit differences such as local Docker vs shared infra vs Helm/K8s vs Swarm.
- `Known implementation caveats` and `High-risk hotspots`.
- `Change checklist` for safe PR-level behavior edits.
- `Documentation and contract maintenance` with explicit "refresh this when X changes" guidance.
- `Detailed payload examples`, `enum references`, `resource shapes`, or `ops notes` when the system complexity justifies them.
