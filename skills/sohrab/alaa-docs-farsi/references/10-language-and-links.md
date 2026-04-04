# Language, constraints, and repository-safe links

## Includes these full-guide sections

- `# Purpose`
- `# When to use`
- `# When NOT to use`
- `# Language requirements`
- `# Hard constraints`
- `# Repository-safe links in generated documents`

## Purpose
Create repository documentation that is implementation-aligned, rich enough to be operationally useful, and deterministic to update across active Ala-style repositories in this workspace.

This guide defines a unified standard for `README.md`, `docs/BIG_PICTURE.md`, and `docs/api-summary.md` so they stay:
- trustworthy for onboarding,
- practical for troubleshooting,
- complete enough for frontend and backend contract work,
- strong enough for human developers and agents to resume work safely,
- and useful as a reference baseline when building new Ala-style services.

## When to use
- Any task that touches contracts, routes, auth trust boundaries, queues/events, setup flow, deployment shape, module structure, or observability.
- Any task that updates `README.md`, `docs/BIG_PICTURE.md`, `docs/api-summary.md`, architecture docs, or operations docs.
- Any task that standardizes docs across repositories and wants better initial context for maintainers, frontend developers, agents, or new service authors.

## When NOT to use
- Pure code refactors with no documentation implications.
- Pure inline annotation work.
- Postman-only collection or environment maintenance with no Markdown doc work.
- Generic writing tasks that are unrelated to repository truth.

## Language requirements
- Write docs in simple, fluent, correct English unless the user explicitly requests another documentation language.
- The user's chat language does not change the documentation language by itself.
- Do not translate identifiers, enum names, table names, header names, route names, class names, queue names, or payload keys.
- Keep technical tokens exactly as implemented in code, config, and Postman artifacts.

## Hard constraints
- Do not patch business logic in a docs-only request.
- Every statement must be traceable to source code, config, migration, tests, current docs, or runtime artifacts.
- Never make an existing strong document weaker, shorter, or more generic unless obsolete content is being removed with proof.
- Keep edits minimal and style-preserving:
  - do not reorder useful sections unless clarity improves,
  - prefer corrections, additions, cross-links, and de-duplication over broad rewrites,
  - preserve high-signal existing sections when they are still accurate.
- If a claim is uncertain, remove ambiguity and add the verification path instead of guessing.

## Repository-safe links in generated documents
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
