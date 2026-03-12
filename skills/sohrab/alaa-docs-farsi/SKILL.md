---
name: alaa-docs-farsi
description: "Persian repo documentation pass (keep domain terms English): business-friendly README intro, feature list, competitor comparison, end-to-end API+DB examples, and a docs consistency guardian (docs↔code↔Postman sync)."
---

# Purpose
Create or update repository documentation so it becomes a reliable source of truth, while remaining readable for both business stakeholders and backend engineers.

This skill includes a docs consistency guardian mode to keep:
- README/docs
- API contract examples
- Postman collection artifacts
  aligned with the current implementation.

# When to use
- “Document the repo”, “update README/docs”, “ops-grade docs”, “align docs with code”.
- Any task that changes behavior and must update docs/runbooks/changelog.
- Syncing Postman collections with the current API contract.

# When NOT to use
- Code changes or refactors (except tiny doc-adjacent fixes explicitly requested)
- Runtime config changes without doc impact
- Tasks unrelated to docs/collections

# Language requirements
- All docs written in Persian (fa-IR).
- If the user explicitly requests another language for a docs task, follow the user request.
- Do NOT translate domain/technical identifiers (keep exact English tokens used in code):
  e.g. `story`, `thread_root_id`, `reaction`, `status`, `project_id`, `commentable_type`, `commentable_id`, `pagination`, `index`, etc.

# Hard constraints
- Do not refactor application logic for a docs task.
- Every claim in docs must be verifiable from code/config/tests.
- Apply minimal, style-preserving edits:
    - keep headings and ordering
    - update only mismatched facts
- If the repo is Postgres-only, do NOT mention MongoDB/MariaDB except as “legacy” with explicit proof.

# Required deliverables (typical targets)
- `README.md`:
    - A business-friendly introduction at the very top.
    - High-level architecture summary (multi-tenancy, scale, security, realtime, moderation, analytics).
    - A complete feature list (only what exists in code).
    - A comparison table vs Coral Talk and Comentario.
    - A final “Summary / Value Proposition”.
- `docs/DESIGN.md` (or existing equivalent):
    - Terminology / Concepts (Persian explanations + English terms).
    - Domain model: story/thread/replies/moderation/reactions, etc.
    - Query patterns, indexes, rationale.
    - End-to-end examples (Request → Response → stored DB changes → rationale).
- `docs/OPERATIONS.md`:
    - Environments & env vars (including secrets handling).
    - Docker/Compose run steps (dev & prod).
    - Maintenance commands and when/why to run them.
    - Health checks and troubleshooting.

# Method (deterministic)
1) Confirm sources of truth
    - Migration docs, API contract, schema design, and the live code
2) Inventory referenced docs/artifacts
    - README links, `docs/*`, and Postman collection (if present)
3) Apply minimal, style-preserving edits
    - preserve headings/order, fix mismatched facts
    - use consistent ID formats and field names in examples (e.g., `public_id`)
4) Update Postman artifacts (if present)
    - variables (baseUrl, auth token), headers, example IDs, response bodies
    - adjust Postman tests to match response shape
5) Run consistency grep (docs + Postman)
    - search for legacy terms and mismatched identifiers
6) Record changes and leftovers
    - short report listing remaining legacy references or contradictions

# Docs consistency checklist (guardian mode)
- API examples match UUID/public_id rules (never show internal IDs)
- Counters/aggregates are documented using the current schema (avoid legacy nested counters)
- Outbox behavior described at a high level (without claiming nonexistent guarantees)
- Optional PgBouncer usage is consistent across docs (either used + documented, or clearly optional)
- Legacy tech references are removed OR explicitly labeled as legacy with boundaries

# When to stop and ask
- If docs require code changes to be accurate
- If source-of-truth docs are missing or contradictory
- If a change would alter API behavior (needs product approval)

# Output contract
When using this skill, output:
1) List of files updated and why (paths only)
2) The consistency grep patterns you used and what mismatches were fixed
3) Any intentional legacy references that remain (and why)
4) Any inconsistencies that need follow-up

# Anti-patterns
- Translating identifiers or renaming concepts that do not exist in code
- Claiming performance/scalability numbers without measurement or architecture proof
- Updating docs in a way that changes API behavior (docs must describe, not invent)
