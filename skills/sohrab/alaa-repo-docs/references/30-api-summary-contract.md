# API summary contract

## API summary purpose

For a repository that exposes HTTP APIs, `docs/api-summary.md` is the fast contract sheet for humans and agents who need the endpoint map and a few verified request examples without reading a full Postman collection, an OpenAPI document, `README.md`, or `docs/BIG_PICTURE.md`.

It complements the rest of the set: `README.md` is the onboarding and operational entrypoint, `docs/BIG_PICTURE.md` is the architecture and runtime map, `docs/data-architecture.md` is the storage and state walkthrough, and `docs/errors-events-observability.md` is the error, event, and observability map. Do not merge these roles.

## Boundary with the API contract and the Postman collection

One API surface can end up described in three artifacts. Each has exactly one owner:

| Artifact | Owner | Standing |
|---|---|---|
| The machine-readable contract, such as `<repo>/docs/contracts/<service>/openapi.yaml` | `/alaa-postman-collections` (`$alaa-postman-collections`) | Authoritative for request and response schemas, status codes, and error shapes. This skill never edits it. |
| The Postman collection, its environments, examples, tests, and request documentation blocks | `/alaa-postman-collections` (`$alaa-postman-collections`) | Sole owner. This skill never edits a collection or a request description. |
| `<repo>/docs/api-summary.md` | this skill | Derived, never authoritative. |
| README and cross-document navigation that links to any of the three | this skill | Graph rules in `references/10-language-and-links.md`. |
| `<repo>/remaining-task.md` wording for a documented-but-unimplemented endpoint | this skill | Rules in `references/80-implementation-gap-backlog.md`. |

**Precedence.** When `<repo>/docs/api-summary.md` disagrees with the canonical contract or with the code, the summary is the defect. `alaa-controlled-ops references/10-source-priority-and-boundaries.md` already ranks generated public artifacts — Postman collections, route inventories, API summaries — below repository truth, and names both skills as the repair route. Fix the summary; never adjust a claim about the code to match it.

**Should `docs/api-summary.md` exist when the repository already has an OpenAPI contract? Yes, and they coexist.** They answer different questions. The contract answers exactly what one endpoint accepts and returns, in a form a tool consumes. The summary answers which endpoints exist and how to call the few that matter, in a form a person reads in under a minute without opening a tool. Deleting the summary in favour of generated contract documentation removes the second property, which is the reason this document exists.

The one case where the summary shrinks rather than coexists: when the summary would only restate the contract field by field, cut it to the endpoint inventory plus a link to the contract for schemas. A summary that duplicates a machine-readable contract will drift from it, and the contract wins.

## When docs/api-summary.md is required

Create or refresh it when all of these are true: the repository owns or exposes HTTP API routes; those routes matter to frontend clients, external callers, internal services, operators, or future agents; and the route surface is large enough that a concise summary improves navigation.

Typical triggers: route additions, removals, renames, or version-prefix changes; new action endpoints such as `/like`, `/pin`, `/lock`, or a similar state transition; request-body or query-parameter changes; path-parameter changes; auth or caller-surface changes that affect how clients call the API; or stale examples in an existing `docs/api-summary.md`.

Skip it only when the repository truly has no meaningful HTTP API surface.

## Required structure for docs/api-summary.md

Use this exact high-level structure unless the user explicitly asks for another format:

1. `# <Service or Domain> API Summary`
2. A flat endpoint inventory as Markdown bullets using inline code, one entry per `METHOD /path`
3. `## Examples`, or `## Examples (base host: ...)` when the host is verified
4. A numbered list of representative requests
5. For any request that accepts a body: a `Body:` label and a fenced `json` block with a realistic minimal example
6. A short `See also` block when local links materially help the reader reach deeper documents

Prefer the project or service name in the title, such as `Comment API Summary` or `Gateway API Summary`.

## API summary formatting rules

- Keep the endpoint inventory concise and scannable: one bullet per canonical endpoint, route templates with placeholders such as `{comment}` or `{ticketRef}`, closely related endpoints grouped together, and a blank line between distinct route families when that improves scanning.
- Keep paths canonical: include the real version prefix such as `/api/v1/...` when it exists, keep placeholder names aligned with the actual route parameter names, and never substitute a real ID into the inventory.
- Keep examples concrete: realistic path values and query strings, minimal but valid payloads, the real request field names from validation or controllers, and `{}` only when the endpoint genuinely expects no payload. Every example obeys the redaction rules in `references/10-language-and-links.md`; a request example is a publication.
- When many endpoints share one pattern, keep the full endpoint inventory even if example coverage is abbreviated, show one full example for the repeated family, and add a short guidance line or a mini template for the siblings instead of repeating near-identical examples.
- Include `base host` in the `## Examples` heading only when that host and port are verified from repository sources such as README, env examples, Docker or Compose files, test fixtures, or existing documents.
- Exclude boilerplate operational endpoints such as health, readiness, or metrics unless the user asks for them or they are part of the main consumed API surface.
- Do not dump response bodies by default. Add a response example only when it is unusually important to calling the route correctly.
- If endpoint semantics depend on storage shape, event side effects, or a nuanced error contract, add a one-line pointer to the deeper document instead of copying the deep-dive section.

## API summary example-selection rules

Select examples so a caller can issue a correct first request without opening another artifact:

- start with the primary collection and item endpoints,
- include the most important action-style subroutes,
- include at least one read example and the key write examples,
- include one example per materially different body shape,
- prefer the examples a frontend or integration developer needs first.

For a CRUD-style API the default representative set is list or search, create, update or patch, delete, and any domain-specific action endpoints. For an action-heavy API, include the important business actions even when they are not CRUD, such as moderation, publish, approve, retry, assign, or a state toggle.

When many action endpoints are structurally repetitive, document one representative action endpoint fully, then add a compact note such as `Other action endpoints in this family follow the same path shape and accept either an empty body or one small state field.`, optionally with a template line such as `POST /api/.../{resource}/{action}`.

When an existing `docs/api-summary.md` already has useful examples, preserve the strongest ones and update only what is stale or incomplete.

## API summary coverage requirements

`docs/api-summary.md` must answer each of these from itself alone:

- Which consumer-facing endpoints exist?
- Which route parameters and path shapes are canonical?
- Which request bodies are expected for the important write paths?
- Which action endpoints exist beyond basic CRUD?
- What is the verified local example host, if the repository documents one?
- Which deeper document answers storage, event, or error questions?

Every claim in it is source-backed, and it never tries to replace the canonical contract or the Postman collection.
