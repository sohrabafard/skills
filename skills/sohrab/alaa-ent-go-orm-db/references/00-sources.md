# Sources and targeted retrieval

Use local guides for established patterns; fetch official evidence for unresolved version or API decisions. Read only required pages.

## Retrieval decisions

| Observable trigger | Inspect or retrieve | Required conclusion |
| --- | --- | --- |
| Familiar schema/query pattern, unchanged pinned API, no unresolved behavior | Relevant bundled reference and project-generated code | Implement and verify locally; no repeated general research |
| Select/update Go, Ent, driver, generator, extension, or feature flag | Installed/module versions; official releases; matching API source | Supported version and configuration; avoid assuming latest-docs compatibility |
| Builder, import, annotation, SQL output, error, or lifecycle behavior is uncertain | Generated/project-pinned source, then matching Ent page below | The exact supported operation, or a bounded supported alternative |
| PostgreSQL index, constraint, locking, planner, or migration behavior changes | Target server major; that major's official manual | Applicable semantics, lock/write implications, and verification plan |
| Atlas operation or external object is introduced | Installed Atlas version/edition, Ent and Atlas integration docs | Required capabilities, ownership, and availability; do not assume paid features |
| Runtime fails or sources disagree | Exact sanitized error; selected release source; relevant maintainer issue if necessary | Cause-specific repair; distinguish a report from a supported guarantee |

Resolve API availability from project/generated source, then official versioned documentation and maintainer sources.
Check examples against the selected release; live documentation may describe unreleased APIs.
Open the official page; search its official domain when the required detail or route is missing.
Record only the URL, consulted version/date, and the decision it resolves in task evidence.
If retrieval is unavailable, continue supported work and mark the dependent decision blocked/unverified. Do not invent an API or claim freshness.

## Ent topic map

The getting-started navigation reaches the complete documentation. Follow the task's branch.

| Need | Official source |
| --- | --- |
| Setup and generator | [Getting started](https://entgo.io/docs/getting-started/), [generation](https://entgo.io/docs/code-gen/), [supported dialects](https://entgo.io/docs/dialects/) |
| Schema, fields, relationships | [Schema](https://entgo.io/docs/schema-def/), [fields](https://entgo.io/docs/schema-fields/), [edges](https://entgo.io/docs/schema-edges/) |
| Reused schema, annotations, indexes | [Mixins](https://entgo.io/docs/schema-mixin/), [annotations](https://entgo.io/docs/schema-annotations/), [indexes](https://entgo.io/docs/schema-indexes/) |
| CRUD and exact projections | [CRUD](https://entgo.io/docs/crud/), [predicates](https://entgo.io/docs/predicates/), [aggregation](https://entgo.io/docs/aggregate/) |
| Associations and paging | [Traversal](https://entgo.io/docs/traversals/), [eager loading](https://entgo.io/docs/eager-load/), [paging/ordering](https://entgo.io/docs/paging/) |
| Lifecycle and authorization | [Transactions](https://entgo.io/docs/transactions/), [hooks](https://entgo.io/docs/hooks/), [interceptors](https://entgo.io/docs/interceptors/), [privacy](https://entgo.io/docs/privacy/) |
| Schema and data changes | [Versioned migration](https://entgo.io/docs/versioned-migrations/), [migration tutorial](https://entgo.io/docs/versioned/intro/), [automatic migration](https://entgo.io/docs/migrate/), [data migrations](https://entgo.io/docs/data-migrations/) |
| PostgreSQL external objects | [Composite](https://entgo.io/docs/migration/composite-types/), [domain](https://entgo.io/docs/migration/domain-types/), [enum](https://entgo.io/docs/migration/enum-types/) types; [extensions](https://entgo.io/docs/migration/extensions/), [functional indexes](https://entgo.io/docs/migration/functional-indexes/), [RLS](https://entgo.io/docs/migration/row-level-security/), [triggers](https://entgo.io/docs/migration/triggers/) |
| Driver, tests, and build integration | [sql.DB](https://entgo.io/docs/sql-integration/), [testing](https://entgo.io/docs/testing/), [CI](https://entgo.io/docs/ci/) |
| Custom generation and advanced schema | [Templates](https://entgo.io/docs/templates/), [extensions](https://entgo.io/docs/extensions/), [feature flags](https://entgo.io/docs/feature-flags/), [views](https://entgo.io/docs/schema-views/), [multiple schemas](https://entgo.io/docs/multischema-migrations/), [schema generation](https://entgo.io/docs/generating-ent-schemas/), [global IDs](https://entgo.io/docs/globalid-migrate/) |
| Optional API integrations | [GraphQL](https://entgo.io/docs/graphql/), [GraphQL tutorial](https://entgo.io/docs/tutorial-todo-gql/), [gRPC tutorial](https://entgo.io/docs/grpc-intro/) |
| Uncovered edge case | [FAQ](https://entgo.io/docs/faq/), selected tag under [Ent source](https://github.com/ent/ent), then the relevant maintainer issue |

For PostgreSQL, start with the actual major's [manual](https://www.postgresql.org/docs/), not an assumed server version.
Use the [Go toolchain](https://go.dev/doc/toolchain), [Go modules](https://go.dev/doc/modules/managing-dependencies), [pgx](https://pkg.go.dev/github.com/jackc/pgx/v5/stdlib), and [Atlas](https://atlasgo.io/ent) sources when those integrations change.

## Verification context and attribution

Sources reviewed **2026-11-05**. Go/Ent version selection is owned by [10-go-and-generation.md](10-go-and-generation.md).
Guidance was checked against Ent **v0.14.6** and official documentation source commit `8037bc89bcab9a264099afa2672581237a3e079b`.
That documentation contains a development-only Blob page unavailable in v0.14.6. A page's presence does not prove release support.
The PostgreSQL current manual resolved to major 18; this does not select the consumer's server version.

The linked [lwx-cloud/entgo-skills](https://github.com/lwx-cloud/entgo-skills/tree/3aa257d1f4f8ee21035c93fd585389012c1416f4) pack was reviewed for coverage.
Primary-source checks replaced its unverified API, transaction, privacy, and index examples with independently authored guidance.
Its inspected tree had no LICENSE file; no community-pack text is redistributed. No upstream documentation snapshot is bundled.
Ent documentation belongs to the Ent Authors; retain upstream attribution/licenses if later copying substantial source material.

This evidence supports the written guidance, not a claim that consumer code compiles, migrations run, or host discovery works.
