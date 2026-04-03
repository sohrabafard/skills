---
name: alaa-docs-farsi
description: "Use this skill when the task involves repository documentation such as README.md, docs/BIG_PICTURE.md, architecture or operations docs, or aligning docs with code and contracts in Ala-style projects. It produces rich, simple-English docs for human developers, frontend integrators, and agents. Do not use it for logic-only changes or Postman-only work."
---

# Alaa Docs Farsi

## Purpose

Use this skill when a repository needs richer, more reliable documentation that stays aligned with implementation.

Despite the historical folder name, the output language for documentation is always simple, fluent English with complete sentences unless the user explicitly asks for another documentation language.

Keep this top-level file lean. Load the reference files only as needed.

## When to use

- `README.md` updates
- `docs/BIG_PICTURE.md` updates
- architecture, operations, contract, onboarding, or troubleshooting docs
- documentation alignment after API, auth, runtime, deployment, event, or observability changes
- standardizing docs across repositories so frontend developers, backend developers, and agents can understand the system quickly

## When NOT to use

- logic changes with no doc impact
- pure inline code annotation passes
- Postman-only collection or environment maintenance with no Markdown doc work

## Quick start

1. Read the repo-local `AGENTS.md`.
2. Read the current `README.md` and `docs/BIG_PICTURE.md` if they exist.
3. Read `references/00-topic-map.md`.
4. Load only the relevant sections from `references/full-guide.md`.
5. Inspect source-of-truth files before documenting behavior.
6. Pair with the relevant companion skills when the task touches frontend, auth, architecture, observability, or Postman.

## Non-negotiables

- Keep documentation in simple, fluent English regardless of the user message language unless the user explicitly requests another doc language.
- Never weaken an existing strong document into a shorter but lower-signal version.
- Preserve service-specific richness such as caveats, diagrams, enum tables, payload examples, operational notes, and flow variants unless they are provably obsolete.
- `README.md` and `docs/BIG_PICTURE.md` serve different roles. Do not collapse them into duplicates.
- When behavior, contracts, runtime shape, auth flow, events, or observability change, review both files in the same task.
- Prefer explicit source references and concrete repo facts over generic documentation language.
- All document links must be repo-portable: valid after clone, valid in GitHub/GitLab web viewers, and independent of the local machine path.
- Never emit local absolute filesystem links in generated docs. Use repository-valid relative Markdown links with POSIX `/` separators only, and fall back to an inline code path when a correct link cannot be verified.

## Doc impact checklist

- Re-check `README.md` when install, setup, commands, onboarding, or workflow expectations changed.
- Re-check `docs/BIG_PICTURE.md` when architecture, runtime, request flow, event flow, observability, or trust boundaries changed.
- Re-check related docs when request, response, auth, headers, errors, enums, jobs, logs, or deployment behavior changed.
- Re-check Postman collections through `$alaa-postman-collections` when endpoints, examples, or auth flows changed.
- Re-check diagrams and module maps when system flow or code boundaries changed.

## Companion routing

- $alaa-frontend-doc-annotations
  - Pair when the task also touches docblocks and inline code annotations.
- $alaa-frontend-developer
  - Pair when frontend integration flows, SSR/PWA behavior, route flows, or consumer expectations must be documented accurately.
- $alaa-php-clean-code
  - Pair when backend contract terminology or implementation structure must stay aligned with docs.
- $alaa-laravel-architecture
  - Pair when service-layer boundaries, controller/service/repository structure, or module decomposition need accurate documentation.
- $alaa-services-contract
  - Pair when Ala service conventions, `/api/*` response behavior, or platform-wide service expectations are in scope.
- $alaa-trust-gateway-auth
  - Pair when trusted headers, gateway identity propagation, or downstream auth semantics are in scope.
- $alaa-observability-soc
  - Pair when logs, traces, metrics, SOC evidence paths, or operational event naming are in scope.
- $alaa-postman-collections
  - Pair when the task needs Postman collections, environments, examples, tests, or Insomnia-safe artifact sync.

## Reference navigation

- Read `references/00-topic-map.md` first for fast routing.
- Read `references/full-guide.md` for the documentation contract, audience coverage, richness guardrails, required section sets, and workflow.
- Use the active repository `AGENTS.md` as a repository-local override for sync rules and done criteria.

## Maintenance rules

- Keep this file routing-first and plain.
- Put detailed rules into `references/full-guide.md` instead of growing this file.
- Keep the topic map aligned with the actual headings in the full guide.
- Re-check companion-skill routing when ownership boundaries change.
