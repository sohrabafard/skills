# Errors, events, and observability contract

Every obligation in this file binds the **document**, not the service. It states which facts
`docs/errors-events-observability.md` must record. It states no requirement level for the service
and blocks no ship: whether a signal is required and which gate blocks a release is
`/alaa-observability-soc`'s (`$alaa-observability-soc`), and the exact name or value of any field,
header, event, code, or metric is
`alaa-services-contract references/20-operational-and-observability-contract.md`'s.

## Why this document exists

`docs/errors-events-observability.md` is the concrete operations and side-effects map. It tells the reader which caller-visible errors exist, where each is generated or mapped, which events or jobs fire, what payload data moves through them, which logs, traces, or metrics are emitted, and how to verify the behavior while troubleshooting.

It is separate because `docs/BIG_PICTURE.md` should summarize the flow map, not carry every exception class, event payload, log field, and troubleshooting path.

## When docs/errors-events-observability.md is required

Create or refresh it when one or more of these is true:

- the repository exposes meaningful HTTP, RPC, CLI, or job error contracts,
- the code emits domain events, integration events, queued jobs, notifications, or scheduler-driven side effects,
- the system relies on structured logging, tracing, metrics, alerting, or SOC-style evidence,
- a change to handlers, events, listeners, logging, tracing, or failure mapping would otherwise make the documents misleading.

Skip it only for a simple library or tool with no meaningful runtime surface. When you skip it and the repository structure would make a reader expect it, say so explicitly in `README.md` or `docs/BIG_PICTURE.md`.

Filename, preservation, and role separation follow `SKILL.md` under `## Default document set` and `references/20-readme-big-picture-contract.md`. In particular: do not turn this document into a second API summary, a second data-architecture document, or a second BIG_PICTURE.

## Required structure for docs/errors-events-observability.md

Use this structure unless the repository shape clearly needs a tighter variant:

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

Error-matrix columns: surface, trigger, producer or mapper, HTTP or RPC or job outcome, stable error code or key, caller action or retry note, and observability note.

Event-inventory columns: name, producer, trigger, sync or async, transport or storage, consumers, payload fields, idempotency or ordering note, failure handling, and observability note.

## Error contract coverage rules

- Cover the failure families the repository actually implements: auth or trust, validation, not-found, conflict, business-rule violation, rate-limit or quota, dependency failure, infrastructure failure, async or job failure, and any custom domain family.
- Use the real response envelope, exception mapping, serializer, or job-failure contract from the code.
- Include an exact status code, stable error key, or enum name only when verified.
- Show a minimal example when the error shape matters to callers, under the redaction rules in `references/10-language-and-links.md`.
- State where the error is produced or mapped and what a caller or operator does next.
- Never invent an error that merely seems likely.

## Event inventory rules

- Include domain events, integration events, queued jobs, outbox rows, notifications, scheduler triggers, and any other side-effect signal that materially affects behavior.
- For each, state when it fires, who emits it, who consumes it, which payload fields matter, and what happens on failure.
- Distinguish synchronous from async dispatch, and the business trigger from the transport or storage mechanism.
- Record ordering, idempotency, retry, dead-letter, and deduplication rules only when verified in code or configuration. Whether the rule the code implements is the right one is `/alaa-async-messaging`'s (`$alaa-async-messaging`) decision; record what is there and route the doubt rather than documenting an intent the code does not hold.
- If the repository truly has no such events, say so explicitly instead of leaving the section vague.

## Observability coverage rules

- List the structured log families or major log points that let an operator verify the main flows.
- Include a correlation or context field only when it is verified in the repository, and spell it exactly as `alaa-services-contract references/20-operational-and-observability-contract.md` spells it. The canonical correlation identifiers are `X-Request-Id` and `traceparent`; a lowercase or hyphenated local variant such as `request-id` is wrong even when the surrounding prose is right, because a reader will copy the name into code. Tenant, actor, event, and job identifiers follow the same rule: the name comes from that contract, never from this skill.
- Map important traces, spans, metrics, dashboards, alerts, and SOC evidence paths when they exist.
- State where logs or traces land only when the repository or its documents verify that destination.
- Include the practical verification path: which logger, middleware, config file, or dashboard the reader inspects next.
- Record what the repository emits. Whether it emits enough, and which gate blocks a ship on the answer, is `/alaa-observability-soc`'s (`$alaa-observability-soc`) decision, not a judgement to make in this document.

## Diagram and flowchart rules

- Include at least one focused diagram for a representative error path, from request or job trigger through mapping to observability output.
- Include at least one focused diagram for event fire and consume flow when the repository has event or job behavior.
- Include a correlation-path diagram when tracing, logging, and metrics are all part of the implementation.
- Use `flowchart LR`, `flowchart TD`, or `sequenceDiagram` depending on whether topology or call order matters more.
- Keep labels canonical and short, using verified route names, error keys, event names, logger names, metric names, and queue names.
- Prefer several small diagrams over one that mixes unrelated failure families.

## Coverage requirements

`docs/errors-events-observability.md` must answer each of these from itself alone:

- Which errors exist, and how is each surfaced to a caller?
- Where is each important error produced or mapped?
- Which events or jobs fire, from where, and with what payload?
- Which logs, traces, metrics, alerts, or evidence paths does an operator inspect?
- How do I follow one failure from trigger to operational evidence without grepping the repository?
