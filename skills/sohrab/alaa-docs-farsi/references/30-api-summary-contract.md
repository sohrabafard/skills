# API summary contract

## Includes these full-guide sections

- `# Standard API summary contract`
- `## API summary purpose`
- `## When docs/api-summary.md is required`
- `## Required structure for docs/api-summary.md`
- `## API summary formatting rules`
- `## API summary example-selection rules`
- `## API summary quality bar`

## Standard API summary contract

## API summary purpose
For repositories that expose HTTP APIs, `docs/api-summary.md` is the fast contract sheet for humans and agents who need the endpoint map and a few verified request examples without reading a full Postman collection, OpenAPI document, `README.md`, or `docs/BIG_PICTURE.md`.

This file complements the broader docs set:
- `README.md` remains the onboarding and operational entrypoint.
- `docs/BIG_PICTURE.md` remains the architecture and runtime contract map.
- `docs/data-architecture.md` remains the storage and state walkthrough when the repo has meaningful persistence.
- `docs/errors-events-observability.md` remains the concrete error, event, and observability map when the repo has that surface.
- `docs/api-summary.md` remains the concise endpoint-and-request example sheet.

Do not merge these roles together.

## When docs/api-summary.md is required
Create or refresh `docs/api-summary.md` when all of the following are true:
- the repository owns or exposes HTTP API routes,
- those routes matter to frontend clients, external callers, internal services, operators, or future agents,
- and the route surface is large enough that a concise summary improves navigation and maintenance.

Typical triggers:
- route additions, removals, renames, or version-prefix changes,
- new action endpoints such as `/like`, `/pin`, `/lock`, `/flags`, or similar state transitions,
- request-body or query-parameter changes,
- path-parameter changes,
- auth or caller-surface changes that affect how clients call the API,
- stale examples in an existing `docs/api-summary.md`.

Skip `docs/api-summary.md` only when the repository truly has no meaningful HTTP API surface.

## Required structure for docs/api-summary.md
Use this exact high-level structure unless the user explicitly asks for another format:

1. `# <Service or Domain> API Summary`
2. A flat endpoint inventory as Markdown bullets using inline code, one entry per `METHOD /path`
3. `## Examples` or `## Examples (base host: \`...\`)`
4. A numbered list of representative requests
5. For any request that accepts a body:
   - a `Body:` label
   - a fenced `json` block with a realistic minimal example
6. A short `See also` block when local links materially help the reader navigate to deeper docs

Prefer the project or service name for the title, such as `Comment API Summary`, `Gateway API Summary`, or `Ticket API Summary`.

## API summary formatting rules
- Keep the endpoint inventory concise and scannable:
  - one bullet per canonical endpoint,
  - use route templates with placeholders such as `{comment}` or `{ticketRef}`,
  - group closely related endpoints together,
  - insert a blank line between distinct route families when that improves scanning.
- Keep paths canonical in the inventory:
  - include the real version prefix such as `/api/v1/...` when it exists,
  - keep placeholder names aligned with the actual route names,
  - do not substitute real IDs into the inventory list.
- Keep examples concrete:
  - show realistic path values and query strings,
  - keep example payloads minimal but valid,
  - use the real request field names from validation or controllers,
  - use empty `{}` only when the endpoint genuinely expects no payload.
- Prefer concise coverage when many endpoints share one pattern:
  - keep the full endpoint inventory even if example coverage is abbreviated,
  - show one full example for a repeated action family when that example teaches the calling pattern,
  - add a short guidance line or mini-template for the sibling endpoints instead of repeating near-identical examples.
- Include `base host` in the `## Examples` heading only when that host and port are verified from repo sources such as README, env examples, Docker or Compose, test fixtures, or existing docs.
- Exclude boilerplate operational endpoints such as health, readiness, or metrics unless the user explicitly asks to include them or they are part of the main consumed API surface.
- Do not dump response bodies by default. Add response examples only when they are unusually important to using the route correctly.
- If endpoint semantics depend on storage shape, event side effects, or a nuanced error contract, add a one-line note that points to the deeper doc instead of copying the whole deep-dive section.

## API summary example-selection rules
Model `docs/api-summary.md` after the same pattern as the comment-service example:
- start with the primary collection and item endpoints,
- include the most important action-style subroutes,
- include at least one read example and the key write examples,
- include one example per materially different body shape,
- prefer examples that help a frontend or integration developer understand how to call the API immediately.
- When many action endpoints are structurally repetitive, it is acceptable and often better to:
  - document one representative action endpoint fully,
  - then add a compact note such as `Other action endpoints in this family follow the same path shape and usually accept either an empty body or one small state field.`,
  - and optionally list a tiny template like ``POST /api/.../{resource}/{action}`` under that note.

For CRUD-style APIs, the default representative set is:
- list or search,
- create,
- update or patch,
- delete,
- and any domain-specific action endpoints.

For action-heavy APIs, include the important business actions even if they are not CRUD, such as moderation, publish, approve, retry, assign, or state toggles.

When an existing `docs/api-summary.md` already has useful examples, preserve the strongest ones and update only what is stale or incomplete.

## API summary quality bar
`docs/api-summary.md` is good when a developer or agent can answer these questions quickly:
- Which consumer-facing endpoints exist?
- Which route parameters and path shapes are canonical?
- Which request bodies are expected for the important write paths?
- Which action endpoints exist beyond basic CRUD?
- What is the verified local example host, if the repo documents one?
- Which deeper doc should I read next when I need storage, event, or error detail?

The file should feel compact, current, and source-backed.
It should not read like generated sludge, and it should not try to replace richer docs or Postman collections.
