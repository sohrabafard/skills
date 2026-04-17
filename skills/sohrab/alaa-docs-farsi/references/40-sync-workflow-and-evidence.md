# Sync, workflow, and evidence rules

## Includes these full-guide sections

- `# How this standard was derived`
- `# Repository sync matrix (what must be updated together)`
- `# AGENTS alignment for active projects`
- `# Workflow for producing richer docs`
- `# Output checklist for doc updates`
- `# Evidence checks`
- `# Anti-patterns`

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
