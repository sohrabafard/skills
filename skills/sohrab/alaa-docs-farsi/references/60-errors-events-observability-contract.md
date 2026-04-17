# Errors, events, and observability contract

## Includes these full-guide sections

- `# Standard errors, events, and observability contract`
- `## Why this doc exists`
- `## When docs/errors-events-observability.md is required`
- `## Default filename and preservation rule`
- `## Separation from README, BIG_PICTURE, data-architecture, and api-summary`
- `## Required structure for docs/errors-events-observability.md`
- `## Error contract coverage rules`
- `## Event inventory rules`
- `## Observability coverage rules`
- `## Diagram and flowchart rules`
- `## Errors, events, and observability quality bar`

# Standard errors, events, and observability contract

## Why this doc exists
`docs/errors-events-observability.md` is the concrete operations and side-effects map for a repository.
It should tell the reader which caller-visible errors exist, where they are generated or mapped, which events or jobs fire, what payload data moves through them, which logs or traces or metrics are emitted, and how to verify the behavior during troubleshooting.

This doc is separate because `docs/BIG_PICTURE.md` should summarize the flow map, not carry every exception class, event payload, log field, and troubleshooting path.

## When docs/errors-events-observability.md is required
Create or refresh `docs/errors-events-observability.md` when one or more of these are true:
- the repository exposes meaningful HTTP, RPC, CLI, or job error contracts,
- the code emits domain events, integration events, queued jobs, notifications, or scheduler-driven side effects,
- the system relies on structured logging, tracing, metrics, alerting, or SOC-style evidence,
- changes to handlers, events, listeners, logging, tracing, or failure mapping would otherwise make the docs misleading.

Skip this doc only for simple libraries or tools with no meaningful runtime or operational surface.
If you skip it, keep that choice explicit in `README.md` or `docs/BIG_PICTURE.md` when the repo structure could make a reader expect it.

## Default filename and preservation rule
- Use `docs/errors-events-observability.md` for new work.
- If the repository already has a stronger equivalent doc under another verified name, update that file instead of creating a duplicate.
- When you preserve an existing filename, repair README and cross-links so the documentation graph still makes the role of the doc obvious.

## Separation from README, BIG_PICTURE, data-architecture, and api-summary
- `README.md` stays the onboarding and navigation entrypoint.
- `docs/BIG_PICTURE.md` stays the architecture and runtime summary map.
- `docs/api-summary.md` stays the concise endpoint inventory and request-example sheet.
- `docs/data-architecture.md` stays the storage and state walkthrough.
- `docs/errors-events-observability.md` holds the detailed error matrix, event inventory, payload notes, logging or tracing or metrics paths, alerts, and troubleshooting evidence.

Do not turn this doc into a second API summary, a second data-architecture doc, or a second BIG_PICTURE.

## Required structure for docs/errors-events-observability.md
Use this default structure unless the repository shape clearly needs a tighter variant:

1. `# <Service or Domain> Errors, Events, and Observability`
2. `## Purpose and scope`
3. `## Source-of-truth map`
4. `## Error contract matrix`
5. `## Representative error flows`
6. `## Event inventory`
7. `## Event payload notes`
8. `## Logging and correlation fields`
9. `## Traces, metrics, alerts, and evidence paths`
10. `## Flow diagrams`
11. `## Troubleshooting and verification notes`
12. `## See also`

Typical error-matrix columns:
- surface,
- trigger,
- producer or mapper,
- HTTP or RPC or job outcome,
- stable error code or key,
- caller action or retry note,
- observability note.

Typical event-inventory columns:
- name,
- producer,
- trigger,
- sync or async,
- transport or storage,
- consumers,
- payload fields,
- idempotency or ordering note,
- failure handling,
- observability note.

## Error contract coverage rules
- Cover the meaningful failure families that the repo actually implements: auth or trust, validation, not-found, conflict, business-rule violations, rate-limit or quota, dependency failure, infrastructure failure, async or job failure, and any custom domain error families.
- Use the real response envelope, exception mapping, serializer, or job-failure contract from the code or docs.
- Include exact status codes, stable error keys, or enum names only when verified.
- Show a minimal example when the error shape is important to callers.
- Explain where the error is produced or mapped and what a caller or operator should do next.
- Do not invent errors that merely seem likely.

## Event inventory rules
- Include domain events, integration events, queued jobs, outbox rows, notifications, scheduler triggers, and other side-effect signals that materially affect system behavior.
- For each event or job, state when it fires, who emits it, who consumes it, what payload fields matter, and what happens on failure.
- Distinguish synchronous dispatch from async dispatch.
- Distinguish the business trigger from the transport or storage mechanism.
- Note ordering, idempotency, retry, dead-letter, or deduplication rules only when verified.
- If the repo truly has no such events, say that explicitly instead of leaving the section vague.

## Observability coverage rules
- List the structured log families or major log points that help operators verify the main flows.
- Include correlation and context fields such as `request-id`, `traceparent`, tenant identifiers, actor identifiers, event identifiers, or job identifiers only when they are verified.
- Map important traces, spans, metrics, dashboards, alerts, or SOC evidence paths when they exist.
- State where logs or traces land only when the repo or docs actually verify that destination.
- Include the practical search or verification path: which logger, middleware, config, or dashboard the reader should inspect next.

## Diagram and flowchart rules
- Include at least one focused diagram for a representative error path from request or job trigger to mapping and observability output.
- Include at least one focused diagram for event fire and consume flow when the repo has event or job behavior.
- Include a correlation-path diagram when tracing and logging and metrics are part of the implementation.
- Use `flowchart LR`, `flowchart TD`, or `sequenceDiagram` depending on whether topology or call order matters more.
- Keep labels canonical and short: use verified route names, error keys, event names, logger names, metric names, and queue names.
- Prefer several small diagrams over one diagram that mixes unrelated failure families.

## Errors, events, and observability quality bar
`docs/errors-events-observability.md` is good when a developer or agent can answer these questions quickly:
- Which errors exist and how are they surfaced?
- Where is each important error produced or mapped?
- Which events or jobs fire, where, and with what payload?
- Which logs, traces, metrics, alerts, or evidence paths should I inspect?
- How do I follow one failure from trigger to operational evidence?

The doc should make failures and side effects understandable and debuggable.
A reader should not need to grep the whole repo just to learn which event fires or which log to search for a failure.
