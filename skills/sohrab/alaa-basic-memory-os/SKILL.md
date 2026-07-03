---
name: alaa-basic-memory-os
description: "Use when Alaa work needs Basic Memory project alaa-memory or Obsidian memory governance: creating/updating architecture, contract, operations, lesson, work-pattern, project-index, project-state, handoff, research, or inbox-capture notes; publishing Prompt 1/2 self-improvement outputs into Basic Memory; resuming work from cross-session memory; maintaining templates/schemas without duplicating alaa-workflow or alaa-low-noise. Do not use for tiny code edits or as a second task system."
---

# Alaa Basic Memory OS

## Purpose

Operate Basic Memory project `alaa-memory` as Alaa's curated cross-agent memory layer.

## Use this skill when

- A task is non-trivial, cross-service, contract-sensitive, architecture-sensitive, continuation-likely, or memory-sensitive.
- Creating or updating Basic Memory notes.
- Publishing Prompt 1/2 outputs into curated runtime memory.
- Resuming prior work using memory and repo-local state.
- Maintaining Basic Memory schemas, templates, metadata, or Obsidian conventions.
- Handling compact/handoff continuity across Claude and Codex.

## Do not use this skill for

- Tiny deterministic code edits where memory lookup adds no value.
- Active execution planning that belongs to `alaa-workflow`.
- Terminal/output discipline that belongs to `alaa-low-noise`.
- Dumping raw sessions, raw logs, full docs, source files, Postman collections, or draft skills into memory.

## Core rules

- Repository code and docs are source of truth; Basic Memory is a map, not proof.
- Skills define behavior; do not copy full installed skills into Basic Memory.
- Obsidian is the human editing/navigation surface, not runtime source of truth.
- `raw/processed` is the self-improvement evidence warehouse.
- Use `bm status --project alaa-memory --wait --timeout 60`, `bm reindex -p alaa-memory`, `bm doctor`, and `bm schema validate <type> --project alaa-memory`.
- Do not use unsupported `basic-memory sync`.

## Task-start rule

For non-trivial, cross-service, contract-sensitive, architecture-sensitive, or continuation-likely work:

1. Search Basic Memory for project, service/domain, contract names, decisions, lessons, and handoffs.
2. Use `build_context` from known memory URLs when available.
3. Inspect repo-local `AGENTS.md`, `CLAUDE.md`, README, docs, configs, closest code patterns, and validation commands.
4. Separate memory facts, repo facts, assumptions, risks, and questions.
5. Do not implement from memory alone.

## Note creation rule

Before creating any note:

1. Search for existing notes by title, permalink, project, domain, canonical source path, and synonyms.
2. Update an existing note when it covers the same topic.
3. Choose the template by content type.
4. Include frontmatter, `## Observations`, `## Relations`, stable `permalink`, `status`, and `confidence`.
5. Include `canonical_source_paths` and `last_verified` for source-derived notes.
6. Keep notes concise and agent-queryable.

See `references/note-governance.md` for full rules.

## Contract mode rule

Use Extraction Mode by default:

- Read source docs/code/contracts.
- Extract only supported existing facts.
- Mark gaps `[todo]`, `[question]`, or `[gap]`.

Use Design Mode only when explicitly asked to design, standardize, complete, or harden a contract:

- Proposed values must be `[proposal]`, `[draft_contract]`, or `[decision_needed]`.
- Keep status `draft` or `needs_review` until approved and recorded in repo truth.

## Prompt 3 publishing rule

Prompt 3 publishes only curated lessons and repeated patterns from Prompt 1/2 outputs.

Do not publish raw sessions, full work files, draft skill contents, skill-candidate notes, or installed skills.

See `references/prompt-3-publishing.md`.

## End-of-work rule

Update Basic Memory only when durable knowledge changed.

If `alaa-workflow` is active, store only a concise pointer to repo-local plan/state/handoff files. Do not duplicate active plans, phase checklists, or validation logs.

## Basic Memory skill boundaries

Recommended companions:

- `memory-notes`
- `memory-capture`
- `memory-continue`
- `memory-metadata-search`
- `memory-schema`

Gated/manual only:

- `memory-ingest`
- `memory-reflect`
- `memory-defrag`
- `memory-curate`
- `memory-lifecycle`
- `memory-research`
- `memory-tasks`
- `memory-ci-capture`

`memory-tasks` must not duplicate active `alaa-workflow` execution state.

## References

- `references/operating-model.md`
- `references/note-governance.md`
- `references/prompt-3-publishing.md`
- `references/cli-and-mcp.md`
- `references/obsidian-usage.md`
- `references/skill-boundaries.md`
- `references/compact-and-handoff.md`

## Completion checks

- Existing memory was searched before new note creation.
- Repo truth was inspected before implementation claims.
- No unsupported `basic-memory sync` command was used.
- No raw transcript/log/source/doc dump was stored.
- `alaa-workflow` state was not duplicated.
- Relevant schema validation was run or explicitly recommended.
- Final response reports notes changed, source paths, validation, and unresolved questions.
