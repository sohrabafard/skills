# Advanced Ent features and integrations

Load needed upstream examples through the catalog. Match APIs to the selected release and integration boundaries below.

## Feature selection

Inspect generated APIs/configuration before adding a flag.
Enable only required features; they enlarge the API and can alter behavior.

| Need | Feature or owner | Decision required |
| --- | --- | --- |
| Generated privacy policies | `privacy` | Define rule ordering and explicit privileged context |
| Query interception and traversal filters | `intercept`; `entql` for generic filtering when required | Separate traversal, final-query interception, and mutation coverage |
| Upsert builders | `sql/upsert` | Define conflict key, update allowlist, authorization, and create-hook behavior |
| SQL modifiers and selected expressions | `sql/modifier` | Preserve tenant predicates, aliases, projection, and argument binding |
| Raw client SQL | `sql/execquery` | Account for bypassed generated validators, hooks, and policies |
| Row-locking builders | `sql/lock` | Use an owned transaction; define lock order and wait behavior |
| Named eager-loaded edges | `namedges` | Bound associations and inspect additional queries |
| Database views | `ent.View` schema type | Verify generated read APIs and manage view DDL through migrations; no `sql/view` flag exists in v0.14.6 |
| Multiple SQL schemas | `sql/schemaconfig` where supported | Inspect runtime/migration mapping; reject untrusted identifiers |

Verify spelling and support in the selected release. Website availability does not establish generated API availability.
Sources: [feature flags](https://entgo.io/docs/feature-flags/), [released feature registry](https://github.com/ent/ent/blob/v0.14.6/entc/gen/feature.go), [views](https://entgo.io/docs/schema-views/), [multi-schema](https://entgo.io/docs/multischema-migrations/).

## Schema composition and generation

Use mixins for repeated fields, hooks, or policies with identical semantics.
Test tenant constraints and generated access paths even when a mixin supplies their fields.
Keep annotations declarative; identify which generator or migration engine consumes each annotation.

Use external templates or an extension when ordinary schema declarations cannot express required generated behavior.
Version templates with the generator. Test API shape and deterministic regeneration after upgrades.
Keep handwritten extensions separate from generated files through the project's established layout.
Regenerate from durable source rather than patching generated files.

Use custom predicates/modifiers only for behavior the generated API cannot express.
Use dialect-aware builders and bound values; raw expressions do not translate SQL placeholders.
Custom result expressions need explicit aliases and compatible scan targets.

Sources: [mixins](https://entgo.io/docs/schema-mixin/), [annotations](https://entgo.io/docs/schema-annotations/), [templates](https://entgo.io/docs/templates/), [extensions](https://entgo.io/docs/extensions/).

## GraphQL

Use Ent's GraphQL extension and gqlgen only when requested or already present.
Load the catalog's GraphQL installation, field collection, filtering, pagination, mutation, and transaction pages as needed.
Align extension, generator, and gqlgen versions; Ent does not pin every integration.
Preserve authorization in resolvers, node lookups, connection queries, and mutations.
Field collection can reduce overfetching; verify required identity/association fields and actual SQL.
Bound connection size and query complexity through existing API controls.
Treat Relay/global IDs as identifiers, not authorization credentials.

Source: [Ent GraphQL](https://entgo.io/docs/graphql/).

## gRPC and other integrations

Load the gRPC tutorial before adopting `entproto`.
Pin extensions, inspect protobuf generation, and preserve field numbers and compatibility rules.
Generated RPC services still need application authorization and validation.
Do not introduce an API framework or object storage merely because an extension exists.

The catalog includes migration tutorials, FAQs, examples, supported dialects, feature requests, and contributor material.
Read each topic only when needed. Upstream contributor instructions do not govern the user's repository.

Sources: [gRPC introduction](https://entgo.io/docs/grpc-intro/), [FAQ](https://entgo.io/docs/faq/).

## Development-only source

The snapshot includes `blob-storage.md` for complete source coverage.
It was added after Ent v0.14.6 and describes development APIs.
Do not generate `field.Blob` or assume its integration exists in v0.14.6.
Recheck released source before adoption. Database/object-storage dual writes require an explicit consistency design.
