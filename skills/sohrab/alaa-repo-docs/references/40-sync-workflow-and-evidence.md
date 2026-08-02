# Sync matrix, workflow, evidence, and failure classes

This file owns the production workflow. `SKILL.md` carries a six-step orientation and points here;
the ordered procedure exists only below, so the two cannot disagree.

## Provenance of this standard

The standard was derived from the richest documents across active Ala-style repositories in this
workspace: `auth`, `comment-service`, `gateway`, `ticket`, `vod`, `wa`, `entekhabat-front`. Those
names record provenance only. Never cite one as an example a reader is expected to open: the reader
usually has no access to it, which makes the instruction unfollowable.

## Repository sync matrix

When a change touches the left column, every document in the right column is reviewed in the same
task. Reviewing does not always mean editing, but an unreviewed paired document is an incomplete
task.

| Change | Documents that must be reviewed together |
|---|---|
| Routes, ports, middleware, or the service map | `<repo>/docs/BIG_PICTURE.md`, `<repo>/README.md`, `<repo>/docs/api-summary.md` when the repository exposes APIs, and the source mapping files |
| Auth or header trust boundaries | `<repo>/docs/BIG_PICTURE.md`, `<repo>/README.md`, `<repo>/docs/api-summary.md` when caller usage changes, and middleware or config references |
| Storage shape, tables, collections, cache rules, or request-state walkthroughs | `<repo>/docs/data-architecture.md`, `<repo>/docs/BIG_PICTURE.md`, `<repo>/README.md`, and linked schema or migration references |
| API contracts, payload fields, enums, or caller-visible errors | `<repo>/docs/BIG_PICTURE.md`, `<repo>/README.md`, `<repo>/docs/api-summary.md`, `<repo>/docs/errors-events-observability.md`, and the Postman or contract artifacts through `/alaa-postman-collections` (`$alaa-postman-collections`) |
| Queues, events, schedulers, notifications, listeners, or outbox flows | `<repo>/docs/BIG_PICTURE.md`, `<repo>/docs/errors-events-observability.md`, `<repo>/docs/data-architecture.md` when storage handoff matters, and operations notes |
| Logging, tracing, metrics, alerting, or SOC evidence | `<repo>/docs/errors-events-observability.md`, `<repo>/docs/BIG_PICTURE.md`, `<repo>/README.md`, and runtime or dashboard references |
| Deployment or local-runtime assumptions | `<repo>/README.md`, `<repo>/docs/BIG_PICTURE.md`, `<repo>/docs/api-summary.md` when the example base host changes, and runbook, Helm, or Docker sources |
| Module boundaries or architecture patterns | `<repo>/docs/BIG_PICTURE.md`, module maps, and linked design documents |
| Documentation filenames or internal links | `<repo>/README.md`, every touched deep-dive document, and the full repo-local link graph |
| A localized companion explicitly requested by the user | its explicitly named base document and the companion, per `references/10-language-and-links.md` |

## AGENTS alignment

- Several project `AGENTS.md` files require reading `docs/BIG_PICTURE.md` and `README.md` before
  work, and updating them when behavior, auth, runtime, routes, storage, or operations shift.
- Always document runtime-mode differences explicitly.
- When backend and gateway assumptions differ by deployment, keep both claims explicit and each
  linked to its source file.
- When deep-dive documents exist, keep the repository's declared documentation index as the hub;
  use `README.md` when no separate index is declared.

## Workflow for producing richer documents

1. Read the repository `AGENTS.md`.
2. Read the current `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` where they exist, before planning any edit.
3. Identify the richest useful sections already present and mark them for preservation.
4. Verify behavior from code, config, route definitions, validation rules, exception handlers, events, listeners, migrations, models, cache helpers, and source-of-truth documents before editing any claim.
5. When the repository is large or the task spans several documents, split read-only discovery per `references/70-subagent-doc-workflows.md` and wait for every track before writing.
6. Fill coverage gaps for all four audiences: maintainer, frontend developer, coding agent, and new service author.
7. For an API repository, create or refresh `docs/api-summary.md` per `references/30-api-summary-contract.md`.
8. For a stateful repository, create or refresh `docs/data-architecture.md` per `references/50-data-architecture-contract.md`.
9. For a repository with meaningful error, event, or observability surface, create or refresh `docs/errors-events-observability.md` per `references/60-errors-events-observability-contract.md`.
10. Add or refresh diagrams, module maps, flowcharts, and state snapshots where the current documents are too thin.
11. Apply the canonical-topic procedure in `references/10-language-and-links.md`: consolidate
    repeated detail into one owner, replace duplicates with summaries and links, and make every
    changed major document reachable from the repository's documentation hub; then validate every
    repo-local Markdown link.
12. Classify every created or refreshed file under
    `references/15-document-size-and-clustering.md`; preserve exempt artifacts whole, recursively
    split eligible non-green narrative clusters when comprehension permits, and run the line-budget
    gate only on eligible narrative files.
13. If a document or Postman artifact promises behavior not implemented in current code, create or refresh `remaining-task.md` using `references/80-implementation-gap-backlog.md`.
14. Preserve every existing document's language. Create or update a localized companion only when
    the user explicitly requested it, then validate that pair with
    `--localized-pair <base> <companion>`.
15. Before finishing, walk the `## Coverage requirements` list in every contract reference that applied to this task and confirm each question is answered by the document that owns it. **An unanswered coverage question is a gap to close, and that is this skill's only done criterion.** "Richer or clearer than before" is not one, because no agent can fail it.

## Output checklist for documentation updates

Report every line. An item that did not apply is reported as intentionally not needed, never omitted:

1. Files changed.
2. The change type that triggered the task: auth, runtime, API, storage, architecture, operations, errors, events, or observability.
3. Source-of-truth files verified.
4. `docs/api-summary.md` created, refreshed, or intentionally not needed.
5. `docs/data-architecture.md` created, refreshed, reused under another filename, or intentionally not needed.
6. `docs/errors-events-observability.md` created, refreshed, reused under another filename, or intentionally not needed.
7. Postman and contract artifacts updated through their owner, or intentionally unchanged.
8. `remaining-task.md` created, refreshed, or intentionally not needed.
9. Languages preserved; explicitly requested localized companions created or updated, or none
   requested.
10. Subagents used or intentionally skipped, with the track each owned.
11. Repo-local Markdown links validated, with the checker's exit code, or the reason the checker could not run.
12. Line count and green, yellow, orange, or red state for every eligible narrative document; the
    comprehension reason for each yellow or orange exception; the exact human approval for each red
    exception; and each exempt artifact with its exemption class and reason.
13. Remaining uncertain areas, if any.

## Evidence checks

- Use `rg` or an equivalent identifier search for every contract term: headers, routes, enums, queues, event names, table names, cache-key prefixes, logger names, and runtime modes.
- Check source code, migrations, schema, or config for each changed assertion.
- Verify that each document listed in the sync matrix for this change still matches current code for the topic it owns, and that `README.md` and `docs/BIG_PICTURE.md` have matching coverage on shared topics.
- Resolve each repo-local Markdown link against the repository tree. Run
  `python $SKILL_DIR/scripts/check_markdown_links.py <repo-root>` and treat exit `2` as "not
  checked", never as "clean".
- Run the line-budget command from `references/15-document-size-and-clustering.md` for every
  eligible narrative document and child; never pass exempt artifacts to that gate.
- Reconcile conflicting subagent findings against source-of-truth files before editing final documents.
- Verify that existing useful sections were preserved or intentionally replaced with stronger coverage.
- Search the documentation tree for each touched topic after editing; confirm all unique verified
  facts were merged and corrected in one canonical owner, old duplication was not reproduced, and
  every other occurrence is an audience-specific summary with an informative link.
- Confirm every changed major document is reachable from the documentation hub and links back to
  that hub.

## Failure classes for this skill's own run

| Symptom | Diagnosis | Smallest retry | Escalate when |
|---|---|---|---|
| The repository has no `AGENTS.md` | No repo-local override exists | Use this skill's defaults unchanged and say so in the report | Never; absence is a valid state |
| Two source-of-truth files disagree | Stale artifact, or genuinely divergent runtime modes | Prefer code, config, migrations, tests, and runtime artifacts over any document; if both are code, document both modes with their conditions | Neither is reachable from the repository — then state the uncertainty and its verification path instead of choosing |
| Python is unavailable, or the checker exits `2` | The check did not run | Re-run with an explicit interpreter path once | After one retry: verify the touched links by opening each target, and report the document as unvalidated, never as validated |
| A subagent fails or returns nothing | The track produced no evidence | Re-run that one track once with a narrower scope | After one retry: shrink the task to the tracks that returned, and report the missing track by name as uncovered |
| An existing document contradicts current code | The document is stale, or the code regressed | Verify from code and correct the document | The contradiction concerns a security, auth, or trust claim you cannot verify — then do not publish the claim in either direction and route to `/alaa-security-review` (`$alaa-security-review`) |
| A claim cannot be verified before the deadline | Evidence is missing, not absent | State the claim as unverified with its verification path | The claim is a security, auth, entitlement, or data-retention guarantee — publishing an unverified guarantee lets something wrong through, so it is a gate: cut the claim |

## Anti-patterns

- Copying a contract claim that no source artifact can verify.
- Mixing runtime-mode assumptions without an explicit label for each.
- Adding broad detail while skipping the source-of-truth references.
- Inventing a performance or security guarantee.
- Replacing a concrete service map with vague architecture language.
- Creating a deep-dive document full of guessed table names, payload fields, or event flows.
- Duplicating a deep-dive document verbatim into `README.md` or `docs/BIG_PICTURE.md`.
- Leaving future-looking documentation or Postman requests mixed into shipped behavior instead of implementing them or moving them into a source-backed `remaining-task.md`.
