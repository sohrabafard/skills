# Advanced feature and integration decisions

Own flags, views, multiple schemas, custom generation, GraphQL, and gRPC integration. Enable only required features after inspecting generated APIs/configuration. Use [source policy](00-sources.md) for unknown APIs, selected-version mismatches, or development-only examples.

## Feature map

| Need | Flag/API | Consult for behavior |
| --- | --- | --- |
| Privacy policies | `privacy`; `entql` for generic privacy filtering | [Security](60-transactions-security.md): rule order/default denial/bypass. |
| Interceptors/traversers | `intercept` | Security: path versus final-query filtering. |
| Upsert | `sql/upsert` | [Queries](30-ent-queries.md): conflict targets/update allowlists/create hooks. |
| SQL modifiers/expressions | `sql/modifier` | Queries: bindings, aliases, projections, scan types. |
| Raw client SQL | `sql/execquery` | Security: bypassed validation/hooks/policy. |
| Row locks | `sql/lock` | Security: transaction ownership/order/waits. |
| Named eager edges | `namedges` | Queries: bounded fan-out/additional statements. |
| Views | `ent.View` | Verify read APIs and migration-owned DDL; no sql/view flag exists in v0.14.6. |
| Multiple SQL schemas | `sql/schemaconfig` where supported | Verify runtime/migration mapping; reject untrusted identifiers. |

Verify unfamiliar flags against [feature docs](https://entgo.io/docs/feature-flags/) and selected-release source. The [v0.14.6 registry](https://github.com/ent/ent/blob/v0.14.6/entc/gen/feature.go) is the verified baseline. Website examples alone prove no released API. Consult [views](https://entgo.io/docs/schema-views/) or [multi-schema](https://entgo.io/docs/multischema-migrations/) before adopting them.

## Custom generation

[Schema design](20-schema-design.md) owns mixin semantics. Identify the consumer of each annotation. Use [templates](https://entgo.io/docs/templates/) or [extensions](https://entgo.io/docs/extensions/) only when ordinary declarations cannot express required generation. Version templates with the generator; test API shape/deterministic regeneration after upgrades. [Generation](10-go-and-generation.md) owns durable sources and generated-file boundaries.

Use custom predicates/modifiers only for missing generated behavior; read queries for bindings, aliases, and scan targets. [Migrations](50-migrations.md) owns external-object retention and edition dependencies.

## API integrations

Use GraphQL/gqlgen only if requested or present. Consult [Ent GraphQL](https://entgo.io/docs/graphql/) for the needed installation, field collection, filtering, pagination, mutation, or transaction workflow. Align extension/generator/gqlgen versions; Ent does not pin every integration. Preserve resolver, node, connection, and mutation authorization. Verify field collection's identity/association dependencies and actual SQL. Bound connection size/complexity using existing API controls. Relay/global IDs confer no authorization.

Before adopting entproto, read [Ent gRPC](https://entgo.io/docs/grpc-intro/). Pin extensions; inspect protobuf generation and preserve field numbers/compatibility. Generated services still require application authorization/validation. Do not add an API framework or object storage merely because an extension exists.

`field.Blob` is absent from the verified v0.14.6 release. Verify released source before adopting development-only blob APIs. Database/object-storage dual writes need an explicit consistency design. Upstream contributor instructions do not govern the consuming repository.
