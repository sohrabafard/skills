# Language, constraints, and repository-safe links

## Includes these full-guide sections

- `# Purpose`
- `# When to use`
- `# When NOT to use`
- `# Language requirements`
- `# Hard constraints`
- `# Repository-safe links in generated documents`
- `# Documentation graph and internal linking rules`
- `# Link validation workflow`

## Purpose
Create repository documentation that is implementation-aligned, rich enough to be operationally useful, and deterministic to update across active Ala-style repositories in this workspace.

This guide defines a unified standard for `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, and `docs/errors-events-observability.md` so they stay:
- trustworthy for onboarding,
- practical for troubleshooting,
- complete enough for frontend and backend contract work,
- strong enough for human developers and agents to resume work safely,
- and useful as a reference baseline when building new Ala-style services.

## When to use
- Any task that touches contracts, routes, auth trust boundaries, storage topology, cache behavior, queues or events, setup flow, deployment shape, module structure, errors, or observability.
- Any task that updates `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, `docs/data-architecture.md`, `docs/errors-events-observability.md`, architecture docs, or operations docs.
- Any task that standardizes docs across repositories and wants better initial context for maintainers, frontend developers, operators, agents, or new service authors.

## When NOT to use
- Pure code refactors with no documentation implications.
- Pure inline annotation work.
- Postman-only collection or environment maintenance with no Markdown doc work.
- Generic writing tasks that are unrelated to repository truth.

## Language requirements
- Write docs in simple, fluent, correct English unless the user explicitly requests another documentation language.
- The user's chat language does not change the documentation language by itself.
- Do not translate identifiers, enum names, table names, cache-key prefixes, header names, route names, class names, queue names, event names, or payload keys.
- Keep technical tokens exactly as implemented in code, config, migrations, and Postman artifacts.

## Hard constraints
- Do not patch business logic in a docs-only request.
- Every statement must be traceable to source code, config, migrations, schema, tests, current docs, or runtime artifacts.
- Never make an existing strong document weaker, shorter, or more generic unless obsolete content is being removed with proof.
- Keep edits minimal and style-preserving:
  - do not reorder useful sections unless clarity improves,
  - prefer corrections, additions, cross-links, and de-duplication over broad rewrites,
  - preserve high-signal existing sections when they are still accurate.
- If a claim is uncertain, remove ambiguity and add the verification path instead of guessing.
- If you add or refresh any deep-dive doc, also repair README navigation and related doc links in the same task.

## Repository-safe links in generated documents
- All document links must be repo-portable: valid after clone, valid in GitHub or GitLab web viewers, and independent of the local machine path.
- Never use local filesystem absolute paths such as `D:/...`, `C:\...`, `/home/...`, or `file:///...` in generated Markdown or documentation.
- Use repository-valid Markdown links only for files inside the same repository.
- Use POSIX-style separators (`/`) only. Never use Windows backslashes (`\`) in links.
- Prefer relative links from the current document location such as `./file.md`, `../file.md`, or `../../platform/openfga/model.fga`.
- Before finalizing a document, validate every local Markdown link against the repository tree:
  - confirm the target exists in the repo,
  - confirm the relative path is correct from the current document directory,
  - confirm any heading anchor points at a real heading.
- If a correct Markdown link cannot be guaranteed, fall back to a plain inline code path such as `platform/openfga/model.fga` instead of inventing a broken hyperlink.
- Correct examples:
  - `OpenFGA model -> ../../platform/openfga/model.fga`
  - `Data architecture -> ./data-architecture.md#representative-request-walkthrough`
  - `platform/openfga/model.fga`
- Incorrect examples:
  - `model.fga -> D:/repo/platform/openfga/model.fga`
  - `model.fga -> C:epo\platform\openfga\model.fga`
  - `model.fga -> file:///D:/repo/...`

## Documentation graph and internal linking rules
- `README.md` is the navigation hub. It should link to every major doc a new maintainer must read next.
- `docs/BIG_PICTURE.md` is the architecture and runtime map. It should summarize and point to deeper docs rather than copy every table, cache key, event, or error matrix.
- `docs/api-summary.md` should link back to `README.md` and `docs/BIG_PICTURE.md`, and optionally to the deep-dive docs when those links materially help a caller understand side effects, storage, or error behavior.
- `docs/data-architecture.md` should link to `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md` when API requests drive the walkthrough, and `docs/errors-events-observability.md` when async handoff or correlation matters.
- `docs/errors-events-observability.md` should link to `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md` when error contracts are caller-visible, and `docs/data-architecture.md` when event payloads or failures depend on stored state.
- Prefer a small `Related docs` or `See also` block near the top or end of each doc rather than repeating long navigation paragraphs.
- When two docs overlap, keep the summary in the broader doc and the full detail in the narrower doc.

## Link validation workflow
- Resolve every local Markdown link before finishing.
- Validate same-file heading anchors as well as cross-file heading anchors when they are used.
- When Python is available, run `python scripts/check_markdown_links.py <repo-root> --files ...` against the touched docs.
- If Python is not available, verify the path and heading manually before keeping the link.
- If a link target is intentionally missing because the repo does not have that doc yet, create the doc or remove the link. Do not leave aspirational broken links in committed documentation.
