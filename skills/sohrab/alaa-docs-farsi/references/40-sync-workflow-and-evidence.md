# Sync, workflow, and evidence rules

## Includes these full-guide sections

- `# How this standard was derived`
- `# Repository sync matrix (what must be updated together)`
- `# AGENTS alignment for active projects`
- `# Workflow for producing richer docs`
- `# Output checklist for doc updates`
- `# Evidence checks`
- `# Anti-patterns`

## How this standard was derived
This standard is grounded in the richest docs across active Ala-style projects in this workspace, especially:
- `auth`
- `comment-service`
- `gateway`
- `ticket`
- `vod`
- `wa`
- `entekhabat-front`

## Repository sync matrix (what must be updated together)

When a change touches:

- **Routes, ports, middleware, service map**
  - update `docs/BIG_PICTURE.md`, `README.md`, `docs/api-summary.md` when the repo exposes APIs, and source mapping files.
- **Auth/header trust boundaries**
  - update `docs/BIG_PICTURE.md`, `README.md`, `docs/api-summary.md` when caller usage changes, and middleware/config references.
- **API contracts, payload fields, enums**
  - update `docs/BIG_PICTURE.md`, `README.md`, `docs/api-summary.md`, and Postman or API artifact references.
- **Queues, events, schedulers, notifications**
  - update `docs/BIG_PICTURE.md`, operations notes, and observability section.
- **Deployment or local-runtime assumptions**
  - update `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md` when the example base host changes, and runbook/helm/docker sources.
- **Module boundaries or architecture patterns**
  - update `docs/BIG_PICTURE.md`, module maps, and any linked design docs.

If one of the paired docs changes, the other must still be reviewed in the same task.

## AGENTS alignment for active projects
- Several project AGENTS explicitly require reading `docs/BIG_PICTURE.md` and `README.md` before work.
- They also require updating those files when behavior, auth, runtime, routes, or operations shift.
- Reusable rule: always document runtime-mode differences explicitly.
- Reusable rule: when backend and gateway assumptions differ by deployment, keep both claims explicit and linked to source files.

## Workflow for producing richer docs

1. Read repository-local `AGENTS.md`.
2. Read the current `README.md`, `docs/BIG_PICTURE.md`, and `docs/api-summary.md` before planning edits when they exist.
3. Identify the richest useful sections already present and preserve them.
4. Verify behavior from code, config, route definitions, validation rules, and source-of-truth docs before editing claims.
5. Fill coverage gaps for all four audiences:
   - maintainer,
   - frontend developer,
   - coding agent,
   - new service author.
6. For API repositories, create or refresh `docs/api-summary.md` using the standardized endpoint inventory plus numbered request examples format.
7. Add or refresh diagrams, module maps, request variants, and contract notes where the current docs are too thin.
8. Re-check cross-links to Postman, runbooks, ADR/decision docs, and service-specific references, and validate every repo-local Markdown link against the repository tree.
9. Before finishing, confirm the new docs are richer or clearer than before, not just more standardized.

## Output checklist for doc updates
For every documentation update, report:
1. Files changed.
2. Triggered change type such as auth, runtime, API, architecture, ops, contracts, or observability.
3. Source-of-truth files verified.
4. `docs/api-summary.md` created, refreshed, or intentionally not needed.
5. Postman artifacts updated or intentionally kept in sync.
6. Remaining uncertain areas, if any.

## Evidence checks
- Use `rg` or equivalent heading checks for contract terms such as headers, routes, enums, queues, event names, and runtime modes.
- Check source code or config for each changed assertion.
- Verify that `README.md` and `docs/BIG_PICTURE.md` still have matching coverage for shared topics.
- Verify that `docs/api-summary.md` still matches the current route inventory and request shapes when the repository exposes APIs.
- Resolve each local Markdown link against the repository tree before finalizing the document.
- Verify that existing useful sections were preserved or intentionally replaced with stronger coverage.

## Anti-patterns
- Copying contract claims that cannot be verified by source artifacts.
- Mixing runtime-mode assumptions without explicit labels.
- Adding broad detail while skipping source-of-truth references.
- Inventing performance or security guarantees without proof.
- Translating or renaming technical identifiers.
- Replacing a concrete service map with vague “high-level architecture” language.
- Forcing every repo into the same shallow template when the system complexity requires more depth.
- Using machine-local absolute paths, Windows-style backslashes, or unverified relative links in generated Markdown links.
