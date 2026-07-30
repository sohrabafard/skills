---
name: alaa-repo-docs
description: "Use this skill for repository-level documentation in Ala-style projects: README.md, remaining-task.md, the four docs/ deep-dive documents (BIG_PICTURE.md, api-summary.md, data-architecture.md, errors-events-observability.md), README navigation and repo-local Markdown links, and keeping all of them aligned with code and contracts. Every document named here is a file in the repository being worked on, not a file this skill ships. The English document is always the source of truth; a Persian mirror such as README.fa.md is produced when the repository already carries one or the user asks for one. Do not use it for logic-only changes, for comments and docblocks inside source files, which belong to alaa-frontend-doc-annotations, or for Postman collections and OpenAPI contracts, which belong to alaa-postman-collections."
---

# Alaa Repo Docs

## Purpose

Produce repository-level documentation that stays aligned with implementation and operational reality, and keep the documents that describe one system consistent with each other.

This skill owns Markdown files in a repository. Comments and docblocks inside source files belong to `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`). The folder was named `alaa-docs-farsi` until this batch; it was renamed because the old name promised a language while the skill delivers a documentation standard.

Keep this file routing-first. Load only the reference whose condition holds.

## When to use

- `README.md`, `docs/BIG_PICTURE.md`, README navigation, or repo-local Markdown links
- `docs/api-summary.md` for a repository that exposes HTTP routes
- `docs/data-architecture.md` for a storage-heavy or stateful repository
- `docs/errors-events-observability.md` for a repository with meaningful error, event, queue, log, trace, or metric surface
- documentation alignment after an API, auth, storage, cache, runtime, deployment, event, error, or observability change
- `remaining-task.md` when a document or Postman request promises behaviour the code does not implement
- a Persian mirror of any document above, under `## Documentation language`

## When NOT to use

- a logic change with no documentation impact
- a comment, docblock, or any annotation inside a source file
- Postman collection, environment, or OpenAPI contract maintenance with no Markdown work
- writing disconnected from repository truth

## Quick start

1. Read the repository `AGENTS.md`, then whichever documents from the set below already exist.
2. Read `references/00-topic-map.md` and load only the rows whose condition holds.
3. Verify behaviour from source before writing any claim: routes, validation, handlers, exception mapping, events, listeners, queue config, migrations, models, cache code, observability config, and tests.
4. For a broad or multi-document refresh, split discovery using `references/70-subagent-doc-workflows.md` before editing anything.
5. Update every paired document the change triggers, following the production workflow in `references/40-sync-workflow-and-evidence.md`, and report against its output checklist.
6. Repair README navigation and repo-local links, then run `python scripts/check_markdown_links.py <repo-root>` and resolve every finding.

## Default document set

| Document | Create or refresh when |
|---|---|
| `README.md` | onboarding, setup, runtime, operational commands, troubleshooting entrypoints, or documentation links changed |
| `docs/BIG_PICTURE.md` | architecture, request flow, trust boundaries, runtime or storage topology, events, or observability changed |
| `docs/api-summary.md` | the repository exposes meaningful HTTP routes, or route families, methods, path or query parameters, request bodies, or version prefixes changed |
| `docs/data-architecture.md` | the repository persists meaningful domain data, or tables, collections, cache keys, TTL or invalidation rules, serializer shapes, or the main request flow changed |
| `docs/errors-events-observability.md` | error envelopes, status codes, exception mapping, event names, payloads, listener or job flows, logs, traces, metrics, or alerts changed |
| `remaining-task.md` | the user asks for remaining work, or a document or Postman request describes behaviour current code does not implement |

If the repository already has a stronger equivalent document under another name, update that file instead of creating a duplicate, then repair README and cross-links so each document's role stays obvious.

## Documentation language

- The English document is the source of truth. Every other rule in this skill binds the English document first.
- Produce a Persian mirror when either condition holds: the repository already contains a `.fa` document such as `README.fa.md` or `README-fa.md`, or a `docs/fa/` directory; or the user asks for one. Both are checkable facts about the repository or the request, not judgements about the audience.
- A change to an English document leaves the documentation set **incomplete** until its mirror carries the same change in the same task. `scripts/check_markdown_links.py` asserts this and reports drift as a finding.
- Never translate an identifier, in any output language: enum, table, collection, index, header, route, class, queue, event, metric, or payload key. A Persian sentence that mixes the two starts with a Persian word.
- Several skills across the fleet route Persian deliverables to this skill. That routing is correct as of this batch, because the mirror is now this skill's output. It does not make Persian the default.
- Full rules, including the mirror's structural obligations: `references/10-language-and-links.md`.

## Non-negotiables

- Every statement is traceable to source code, config, migrations, schema, tests, current documents, or runtime artifacts. When a claim is uncertain, state the verification path instead of guessing.
- Never weaken an existing strong document into a shorter, more generic one. Preserve caveats, diagrams, enum tables, payload examples, operational notes, storage inventories, event lists, and flow variants unless they are provably obsolete.
- The documents above hold different roles. Do not collapse them into duplicates, and do not copy deep-dive content upward into `README.md` or `docs/BIG_PICTURE.md`.
- Do not patch business logic in a documentation-only request.
- Every link is repo-portable. Never emit a machine-local absolute path, a Windows backslash, or a `file://` link.
- A committed example never carries a real secret, token, API key, `.env` value, production hostname, internal IP address, or real tenant or user identifier. Use placeholder values that are obviously placeholders, and route any doubt about whether a value is safe to publish to `/alaa-security-review` (`$alaa-security-review`).
- Validate repo-local links and heading anchors before finishing.
- The repository `AGENTS.md` may rename or relocate any document above and may add required sections. It may not waive link validation, the traceability rule, the redaction rule, or the mirror rule.

## Ground this skill does not own

Route by name rather than restating. Claude Code form first, Codex form second.

| Concern | Owner |
|---|---|
| Observability field, header, event, code, and metric names and values | `alaa-services-contract references/20-operational-and-observability-contract.md` |
| Whether an observability signal is required, and which gate blocks a ship | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Storage shape, query shape, and index doctrine behind a documented store | `/alaa-data-layer` (`$alaa-data-layer`) |
| Event, queue, retry, and delivery-semantics doctrine behind a documented event | `/alaa-async-messaging` (`$alaa-async-messaging`) |
| The complexity bound behind a documented list, export, or fan-out flow | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Whether an unverifiable security or auth claim is safe to publish | `/alaa-security-review` (`$alaa-security-review`) |
| The ten-criterion quality bar this documentation is measured against | `alaa-project-constitution references/quality-bar.md` |
| Model and effort selection | `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md` |
| Context economy and the subagent fan-out budget | `/alaa-low-noise` (`$alaa-low-noise`) |
| Postman collections, request documentation blocks, and the OpenAPI contract | `/alaa-postman-collections` (`$alaa-postman-collections`) |
| Trusted headers, gateway identity propagation, downstream auth semantics | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Comments, docblocks, and annotations inside a source file | `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`) |
| Backend structure and terminology the documents describe | `/alaa-php-clean-code` (`$alaa-php-clean-code`), `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) |
| Frontend integration behaviour the documents describe | `/alaa-frontend-developer` (`$alaa-frontend-developer`) |
| Ala service conventions and `/api/*` response behaviour | `/alaa-services-contract` (`$alaa-services-contract`) |
| Whether every cross-skill path citation in `skills/sohrab/` resolves | the fleet checker `skills/scripts/check_fleet_references.py` |

## Subagent strategy

- Use parallel subagents only for read-heavy discovery on a broad refresh, and only when the runtime supports them. Claude Code spawns them with the Task tool; Codex spawns them from the parent thread. Do not write a runtime-specific mechanic into a documentation rule.
- Keep final wording, conflict resolution, and every write in the parent agent unless a delegated file is fully isolated from the others.
- The track split, the return contract, the fan-out bound, and the rule for a subagent that fails or returns nothing are in `references/70-subagent-doc-workflows.md`.

## Reference navigation

Read `references/00-topic-map.md` first. It routes each condition to exactly one file, and no other file repeats that routing.

## Maintenance rules

- Keep this file routing-first. New detail goes into the reference that owns the topic, never into a second copy of it here.
- Every rule lives in exactly one file. Do not create a combined guide: the previous one, `full-guide.md`, reproduced 96% of the references verbatim, then drifted from them, and was retired in this batch.
- Re-check the ownership table when a boundary moves.
