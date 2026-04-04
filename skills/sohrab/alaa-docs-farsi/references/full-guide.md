# Purpose
Create repository documentation that is implementation-aligned, rich enough to be operationally useful, and deterministic to update across active Ala-style repositories in this workspace.

This guide defines a unified standard for `README.md` and `docs/BIG_PICTURE.md` so they stay:
- trustworthy for onboarding,
- practical for troubleshooting,
- complete enough for frontend and backend contract work,
- strong enough for human developers and agents to resume work safely,
- and useful as a reference baseline when building new Ala-style services.

# When to use
- Any task that touches contracts, routes, auth trust boundaries, queues/events, setup flow, deployment shape, module structure, or observability.
- Any task that updates `README.md`, `docs/BIG_PICTURE.md`, architecture docs, or operations docs.
- Any task that standardizes docs across repositories and wants better initial context for maintainers, frontend developers, agents, or new service authors.

# When NOT to use
- Pure code refactors with no documentation implications.
- Pure inline annotation work.
- Postman-only collection or environment maintenance with no Markdown doc work.
- Generic writing tasks that are unrelated to repository truth.

# Language requirements
- Write docs in simple, fluent, correct English unless the user explicitly requests another documentation language.
- The user's chat language does not change the documentation language by itself.
- Do not translate identifiers, enum names, table names, header names, route names, class names, queue names, or payload keys.
- Keep technical tokens exactly as implemented in code, config, and Postman artifacts.

# Hard constraints
- Do not patch business logic in a docs-only request.
- Every statement must be traceable to source code, config, migration, tests, current docs, or runtime artifacts.
- Never make an existing strong document weaker, shorter, or more generic unless obsolete content is being removed with proof.
- Keep edits minimal and style-preserving:
  - do not reorder useful sections unless clarity improves,
  - prefer corrections, additions, cross-links, and de-duplication over broad rewrites,
  - preserve high-signal existing sections when they are still accurate.
- If a claim is uncertain, remove ambiguity and add the verification path instead of guessing.

# Repository-safe links in generated documents
- All document links must be repo-portable: valid after clone, valid in GitHub/GitLab web viewers, and independent of the local machine path.
- Never use local filesystem absolute paths such as `D:/...`, `C:\...`, `/home/...`, or `file:///...` in generated Markdown or documentation.
- Use repository-valid Markdown links only for files inside the same repository.
- Use POSIX-style separators (`/`) only. Never use Windows backslashes (`\`) in links.
- Prefer relative links from the current document location such as `./file.md`, `../file.md`, or `../../platform/openfga/model.fga`.
- Before finalizing a document, validate every local Markdown link against the repository tree:
  - confirm the target exists in the repo,
  - confirm the relative path is correct from the current document directory.
- If a correct Markdown link cannot be guaranteed, fall back to a plain inline code path such as `platform/openfga/model.fga` instead of inventing a broken hyperlink.
- Correct examples:
  - `[OpenFGA model](../../platform/openfga/model.fga)`
  - `platform/openfga/model.fga`
- Incorrect examples:
  - `[model.fga](D:/Sohrab/Project/entitlement-platform/platform/openfga/model.fga)`
  - `[model.fga](C:\repo\platform\openfga\model.fga)`
  - `[model.fga](file:///D:/Sohrab/Project/...)`

# Standard documentation contract for README and BIG_PICTURE

## Core rule
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

- **Routes, ports, middleware, service map**
  - update `docs/BIG_PICTURE.md`, `README.md`, and source mapping files.
- **Auth/header trust boundaries**
  - update `docs/BIG_PICTURE.md`, `README.md`, and middleware/config references.
- **API contracts, payload fields, enums**
  - update `docs/BIG_PICTURE.md`, `README.md`, and Postman or API artifact references.
- **Queues, events, schedulers, notifications**
  - update `docs/BIG_PICTURE.md`, operations notes, and observability section.
- **Deployment or local-runtime assumptions**
  - update `README.md`, `docs/BIG_PICTURE.md`, and runbook/helm/docker sources.
- **Module boundaries or architecture patterns**
  - update `docs/BIG_PICTURE.md`, module maps, and any linked design docs.

If one of the paired docs changes, the other must still be reviewed in the same task.

# AGENTS alignment for active projects
- Several project AGENTS explicitly require reading `docs/BIG_PICTURE.md` and `README.md` before work.
- They also require updating those files when behavior, auth, runtime, routes, or operations shift.
- Reusable rule: always document runtime-mode differences explicitly.
- Reusable rule: when backend and gateway assumptions differ by deployment, keep both claims explicit and linked to source files.

# Workflow for producing richer docs

1. Read repository-local `AGENTS.md`.
2. Read the current `README.md` and `docs/BIG_PICTURE.md` before planning edits.
3. Identify the richest useful sections already present and preserve them.
4. Verify behavior from code, config, and source-of-truth docs before editing claims.
5. Fill coverage gaps for all four audiences:
   - maintainer,
   - frontend developer,
   - coding agent,
   - new service author.
6. Add or refresh diagrams, module maps, request variants, and contract notes where the current docs are too thin.
7. Re-check cross-links to Postman, runbooks, ADR/decision docs, and service-specific references, and validate every repo-local Markdown link against the repository tree.
8. Before finishing, confirm the new docs are richer or clearer than before, not just more standardized.

# Output checklist for doc updates
For every documentation update, report:
1. Files changed.
2. Triggered change type such as auth, runtime, API, architecture, ops, contracts, or observability.
3. Source-of-truth files verified.
4. Postman artifacts updated or intentionally kept in sync.
5. Remaining uncertain areas, if any.

# Evidence checks
- Use `rg` or equivalent heading checks for contract terms such as headers, routes, enums, queues, event names, and runtime modes.
- Check source code or config for each changed assertion.
- Verify that `README.md` and `docs/BIG_PICTURE.md` still have matching coverage for shared topics.
- Resolve each local Markdown link against the repository tree before finalizing the document.
- Verify that existing useful sections were preserved or intentionally replaced with stronger coverage.

# Anti-patterns
- Copying contract claims that cannot be verified by source artifacts.
- Mixing runtime-mode assumptions without explicit labels.
- Adding broad detail while skipping source-of-truth references.
- Inventing performance or security guarantees without proof.
- Translating or renaming technical identifiers.
- Replacing a concrete service map with vague “high-level architecture” language.
- Forcing every repo into the same shallow template when the system complexity requires more depth.
- Using machine-local absolute paths, Windows-style backslashes, or unverified relative links in generated Markdown links.
