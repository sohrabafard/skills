# Query Language Routing

Use this file when the user is asking about SigNoz search behavior, Query Builder behavior, field ambiguity, data types, or dashboard variables.

## Pick the right page

| Topic | Best page | Use it when |
|---|---|---|
| Search syntax | `https://signoz.io/docs/userguide/search-syntax/` | The user wants filter syntax for logs, traces, or metrics |
| Operators | `https://signoz.io/docs/userguide/operators-reference/` | The user asks about operators such as `IN`, `EXISTS`, `HAS`, comparisons, or boolean logic |
| Functions | `https://signoz.io/docs/userguide/functions-reference/` | The user needs functions, especially JSON body or array operations |
| Field ambiguity and data types | `https://signoz.io/docs/userguide/field-context-data-types/` | The user sees ambiguous keys like `service.name` or has type issues |
| Query Builder v5 | `https://signoz.io/docs/userguide/query-builder-v5/` | The user asks about the current structured query interface |
| Logs Query Builder | `https://signoz.io/docs/userguide/logs_query_builder/` | The question is specifically about log filters, grouping, body search, or log query UI behavior |
| Dashboard variables | `https://signoz.io/docs/userguide/manage-variables/` | The user wants reusable dashboard filters or templates |

## Routing rules

- If the user asks for SigNoz filter syntax, answer with SigNoz search syntax, not ClickHouse SQL.
- If the user asks for dashboard panel SQL, use the ClickHouse references instead.
- If the user sees an ambiguity warning for fields like `service.name`, route to the field-context page and explain the likely instrumentation problem.
- If the user wants a reusable dashboard, pair the answer with the variables page.

## Practical guidance

### Field ambiguity

When the docs mention ambiguity, the important point is this:

- resource identity fields such as `service.name`, `deployment.environment`, `k8s.namespace.name`, and `host.name` should usually live in resource context
- if the same key appears as both a resource field and a normal attribute, the long-term fix is to correct instrumentation, not just to patch the query

### Data types

If a comparison behaves strangely, tell the user to check the field type and use explicit typing only when needed.

### Dashboard variables

Use variables when the user wants the same panel or dashboard to work across many services, environments, or teams.
