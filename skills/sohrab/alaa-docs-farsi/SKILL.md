---
name: alaa-docs-farsi
description: "Use this skill when the task involves repository documentation such as README.md, docs/BIG_PICTURE.md, docs/api-summary.md, storage or data-architecture docs, error or event or observability docs, or aligning docs with code and contracts in Ala-style projects. It produces rich, simple-English docs for maintainers, frontend integrators, operators, and agents. For API-bearing or stateful repos it must also create or refresh separate docs for storage and request flow and for errors and events and observability, repair repo-local Markdown links and README navigation, and use explicit parallel subagents for broad read-heavy doc refreshes when the Codex surface supports them. Do not use it for logic-only changes or Postman-only work."
---

# Alaa Docs Farsi

## Purpose

Use this skill when a repository needs richer, more reliable documentation that stays aligned with implementation and operational reality.

Despite the historical folder name, documentation output is always simple, fluent English with complete sentences unless the user explicitly asks for another documentation language.

Keep this top-level file lean. Load only the reference files you need.

## When to use

- `README.md` updates
- `docs/BIG_PICTURE.md` updates
- `docs/api-summary.md` creation or refresh for API-bearing repositories
- `docs/data-architecture.md` creation or refresh for storage-heavy or stateful repositories
- `docs/errors-events-observability.md` creation or refresh for repos with meaningful error, event, queue, logging, tracing, or metrics surface
- architecture, operations, contract, onboarding, troubleshooting, and documentation-alignment work
- documentation alignment after API, auth, storage, cache, runtime, deployment, event, error, or observability changes
- standardizing docs so frontend developers, backend developers, operators, and agents can understand the system quickly

## When NOT to use

- logic changes with no documentation impact
- pure inline code annotation passes
- Postman-only collection or environment maintenance with no Markdown doc work
- generic writing work disconnected from repository truth

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read the current `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` if they exist.
3. Read `references/00-topic-map.md`.
4. If the task spans multiple docs or a large repository, read `references/70-subagent-doc-workflows.md` and split discovery with explicit parallel subagents before editing.
5. Load the topic reference files that match the current doc surface.
6. Inspect source-of-truth files before documenting behavior, especially routes, validation, controllers or actions, exception handling, events and listeners, queue config, migrations or schema files, models or entities, cache code, observability config, tests, and current docs.
7. Update every paired doc that the change triggers. Do not update only one file when the docs contract says two or more files must move together.
8. Repair README navigation and repo-local Markdown links before finishing.
9. Pair with the relevant companion skills when the task touches frontend, auth, architecture, observability, or Postman artifacts.

## Default doc set and trigger rules

- `README.md`
  - Review whenever onboarding, setup, runtime, operational commands, troubleshooting entrypoints, or documentation links changed.
- `docs/BIG_PICTURE.md`
  - Review whenever architecture, request flow, trust boundaries, runtime topology, storage topology, events, or observability changed.
- `docs/api-summary.md`
  - Create or refresh when the repository exposes meaningful HTTP APIs.
- `docs/data-architecture.md`
  - Create or refresh when the repository persists meaningful domain data, uses database, cache, outbox, search index, or object storage, or the reader needs a request walkthrough tied to stored state to understand how the system works.
- `docs/errors-events-observability.md`
  - Create or refresh when the repository has non-trivial error contracts, emitted or consumed events, jobs, logs, traces, metrics, alerts, or SOC-style operational evidence.
- If a repository already has stronger equivalent deep-dive docs under different names, update those instead of creating duplicates, then repair README and cross-links so the doc graph stays obvious.

## Non-negotiables

- Keep documentation in simple, fluent English regardless of the user message language unless the user explicitly requests another documentation language.
- Never weaken an existing strong document into a shorter but lower-signal version.
- Preserve service-specific richness such as caveats, diagrams, enum tables, payload examples, operational notes, storage inventories, event lists, and flow variants unless they are provably obsolete.
- `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` serve different roles. Do not collapse them into duplicates.
- Prefer explicit source-backed claims and concrete repo facts over generic documentation language.
- All document links must be repo-portable. Never emit local absolute filesystem links.
- Before finishing, validate local Markdown links and anchor targets. Use `scripts/check_markdown_links.py` when Python is available.

## Doc impact checklist

- Re-check `README.md` when install, setup, commands, onboarding, troubleshooting entrypoints, or documentation links changed.
- Re-check `docs/BIG_PICTURE.md` when architecture, runtime, request flow, storage topology, trust boundaries, events, or observability changed.
- Re-check `docs/api-summary.md` when route families, HTTP methods, path parameters, query parameters, request bodies, version prefixes, or caller-visible action endpoints changed.
- Re-check `docs/data-architecture.md` when tables, collections, cache keys, TTL or invalidation rules, serializers or resource shapes, outbox records, or the main request flow changed.
- Re-check `docs/errors-events-observability.md` when error envelopes, status codes, exception mapping, event names, payloads, listener or job flows, logs, traces, metrics, alerts, or operational evidence paths changed.
- Re-check Postman artifacts through `$alaa-postman-collections` when endpoints, examples, or auth flows changed.
- Re-check diagrams and module maps when code boundaries or system flows changed.

## Companion routing

- `$alaa-frontend-doc-annotations`
  - Pair when the task also touches docblocks and inline code annotations.
- `$alaa-frontend-developer`
  - Pair when frontend integration flows, SSR or PWA behavior, route flows, or consumer expectations must be documented accurately.
- `$alaa-php-clean-code`
  - Pair when backend contract terminology or implementation structure must stay aligned with docs.
- `$alaa-laravel-architecture`
  - Pair when service-layer boundaries, controller or service or repository structure, or module decomposition need accurate documentation.
- `$alaa-services-contract`
  - Pair when Ala service conventions, `/api/*` response behavior, or platform-wide service expectations are in scope.
- `$alaa-trust-gateway-auth`
  - Pair when trusted headers, gateway identity propagation, or downstream auth semantics are in scope.
- `$alaa-observability-soc`
  - Pair when logs, traces, metrics, SOC evidence paths, or operational event naming are in scope.
- `$alaa-postman-collections`
  - Pair when the task needs Postman collections, environments, examples, tests, or Insomnia-safe artifact sync.

## Subagent Strategy

- Use subagents only when the active Codex surface supports them and the task is broad enough to benefit. Subagents must be explicitly requested from the parent thread.
- For large repositories or broad doc refreshes, read `references/70-subagent-doc-workflows.md` and split discovery across focused, mostly read-only tracks: doc graph and README or BIG_PICTURE, API surface, storage and request flow, errors and events and observability, and link validation.
- Prefer `explorer` or another read-heavy custom agent for discovery. Keep final wording, final edits, and conflict resolution in the parent agent unless two output files are clearly disjoint.
- Ask each subagent to return source-of-truth files, concrete findings, proposed section changes, and unresolved questions, then consolidate centrally before writing.
- Use `worker` only for isolated validation or deterministic follow-up tasks that do not create edit collisions with other agents.

## Reference navigation

- Read `references/00-topic-map.md` first for fast routing.
- Read `references/10-language-and-links.md` for language, hard constraints, and internal doc graph rules.
- Read `references/20-readme-big-picture-contract.md` for `README.md` and `docs/BIG_PICTURE.md` separation and navigation.
- Read `references/30-api-summary-contract.md` for `docs/api-summary.md`.
- Read `references/50-data-architecture-contract.md` for storage topology, tables and cache inventory, and request-walkthrough docs.
- Read `references/60-errors-events-observability-contract.md` for error contracts, event inventory, logs, and observability docs.
- Read `references/70-subagent-doc-workflows.md` for concrete parallel delegation patterns, return contracts, and parent-agent merge rules.
- Read `references/40-sync-workflow-and-evidence.md` for paired-doc rules, workflow, link validation, and done criteria.
- Read `references/90-source-map.md` for official-first source maps, freshness triggers, and community-source limits.
- Read `references/full-guide.md` when multiple topics overlap heavily or when updating the reference pack itself.
- Use the active repository `AGENTS.md` as a repo-local override for sync rules and done criteria.

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the split topic references in `references/` aligned with `references/full-guide.md`.
- Keep the topic map aligned with the actual headings in the full guide.
- Re-check companion-skill routing when ownership boundaries change.
