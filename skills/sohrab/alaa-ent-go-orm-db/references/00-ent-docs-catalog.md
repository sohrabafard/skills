# Complete official Ent documentation source

Use this catalog for detailed Ent evidence. Open only relevant pages.
The authored references own execution decisions, including the Go modernization overlay in [10-go-and-generation.md](10-go-and-generation.md).

## Snapshot and limits

- Retrieved: **2026-11-05**. Official source commit: `8037bc89bcab9a264099afa2672581237a3e079b`.
- Complete English `doc/md` source: **75 files**, including 3 shared MDX components.
- Coverage: 44 primary-sidebar pages, 26 tutorial-sidebar pages, 1 auxiliary page, 1 development-only page, and 3 components.
- The 74 existing files match the released Ent **v0.14.6** source. `blob-storage.md` is development-only.
- This is the full textual source, not an offline website. Original remote diagrams, avatars, and example-project links remain external.
- Every relative MDX component import is bundled. Docusaurus theme components are needed only to render the upstream website.
- The files are unmodified evidence. Historical commands, disabled TLS, destructive examples, and old version recommendations are not execution instructions.
- Original Apache-2.0 license: [ent-docs/LICENSE](ent-docs/LICENSE). Attribution: The Ent Authors.
- Per-file URLs, sizes, release status, and SHA-256: [ent-docs/manifest.json](ent-docs/manifest.json).

Verify APIs against the project's selected Ent version. Refresh upstream for version/API decisions when needed.
Do not infer released functionality from the presence of a source page.

## Navigation

- [Primary documentation](#primary-documentation)
- [Tutorials](#tutorials)
- [Auxiliary and development pages](#auxiliary-and-development-pages)
- [Shared components](#shared-components)

## Primary documentation

| Topic | Local source | Official page / source | Availability |
| --- | --- | --- | --- |
| Aggregation | [aggregate.md](ent-docs/aggregate.md) | [Official](https://entgo.io/docs/aggregate/) | v0.14.6 source |
| Continuous Integration | [ci.mdx](ent-docs/ci.mdx) | [Official](https://entgo.io/docs/ci/) | v0.14.6 source |
| Introduction | [code-gen.md](ent-docs/code-gen.md) | [Official](https://entgo.io/docs/code-gen/) | v0.14.6 source |
| Join our Community | [community.md](ent-docs/community.md) | [Official](https://entgo.io/docs/community/) | v0.14.6 source |
| Contributors | [contributors.md](ent-docs/contributors.md) | [Official](https://entgo.io/docs/contributors/) | v0.14.6 source |
| CRUD API | [crud.mdx](ent-docs/crud.mdx) | [Official](https://entgo.io/docs/crud/) | v0.14.6 source |
| Data Migrations | [data-migrations.mdx](ent-docs/data-migrations.mdx) | [Official](https://entgo.io/docs/data-migrations/) | v0.14.6 source |
| Supported Dialects | [dialects.md](ent-docs/dialects.md) | [Official](https://entgo.io/docs/dialects/) | v0.14.6 source |
| Eager Loading | [eager-load.mdx](ent-docs/eager-load.mdx) | [Official](https://entgo.io/docs/eager-load/) | v0.14.6 source |
| Extensions | [extension.md](ent-docs/extension.md) | [Official](https://entgo.io/docs/extensions/) | v0.14.6 source |
| Frequently Asked Questions (FAQ) | [faq.md](ent-docs/faq.md) | [Official](https://entgo.io/docs/faq/) | v0.14.6 source |
| Feature Flags | [features.md](ent-docs/features.md) | [Official](https://entgo.io/docs/feature-flags/) | v0.14.6 source |
| Generating Schemas | [generating-ent-schemas.md](ent-docs/generating-ent-schemas.md) | [Official](https://entgo.io/docs/generating-ent-schemas/) | v0.14.6 source |
| Quick Introduction | [getting-started.mdx](ent-docs/getting-started.mdx) | [Official](https://entgo.io/docs/getting-started/) | v0.14.6 source |
| GraphQL Integration | [graphql.md](ent-docs/graphql.md) | [Official](https://entgo.io/docs/graphql/) | v0.14.6 source |
| Hooks | [hooks.md](ent-docs/hooks.md) | [Official](https://entgo.io/docs/hooks/) | v0.14.6 source |
| Interceptors | [interceptors.mdx](ent-docs/interceptors.mdx) | [Official](https://entgo.io/docs/interceptors/) | v0.14.6 source |
| Automatic Migration | [migrate.md](ent-docs/migrate.md) | [Official](https://entgo.io/docs/migrate/) | v0.14.6 source |
| Using Composite Types in Ent Schema | [migration/composite.mdx](ent-docs/migration/composite.mdx) | [Official](https://entgo.io/docs/migration/composite-types/) | v0.14.6 source |
| Using Domain Types in Ent Schema | [migration/domain.mdx](ent-docs/migration/domain.mdx) | [Official](https://entgo.io/docs/migration/domain-types/) | v0.14.6 source |
| Using Postgres Enum Types in Ent Schema | [migration/enum.mdx](ent-docs/migration/enum.mdx) | [Official](https://entgo.io/docs/migration/enum-types/) | v0.14.6 source |
| Using Postgres Extensions in Ent Schema | [migration/extension.mdx](ent-docs/migration/extension.mdx) | [Official](https://entgo.io/docs/migration/extensions/) | v0.14.6 source |
| Using Functional Indexes in Ent Schema | [migration/functional-indexes.mdx](ent-docs/migration/functional-indexes.mdx) | [Official](https://entgo.io/docs/migration/functional-indexes/) | v0.14.6 source |
| Using Row-Level Security in Ent Schema | [migration/rls.mdx](ent-docs/migration/rls.mdx) | [Official](https://entgo.io/docs/migration/row-level-security/) | v0.14.6 source |
| Using Database Triggers in Ent Schema | [migration/trigger.mdx](ent-docs/migration/trigger.mdx) | [Official](https://entgo.io/docs/migration/triggers/) | v0.14.6 source |
| Multi-Schema Migration | [multischema-migrations.mdx](ent-docs/multischema-migrations.mdx) | [Official](https://entgo.io/docs/multischema-migrations/) | v0.14.6 source |
| Paging And Ordering | [paging.mdx](ent-docs/paging.mdx) | [Official](https://entgo.io/docs/paging/) | v0.14.6 source |
| Predicates | [predicates.md](ent-docs/predicates.md) | [Official](https://entgo.io/docs/predicates/) | v0.14.6 source |
| Privacy | [privacy.mdx](ent-docs/privacy.mdx) | [Official](https://entgo.io/docs/privacy/) | v0.14.6 source |
| Annotations | [schema-annotations.md](ent-docs/schema-annotations.md) | [Official](https://entgo.io/docs/schema-annotations/) | v0.14.6 source |
| Introduction | [schema-def.md](ent-docs/schema-def.md) | [Official](https://entgo.io/docs/schema-def/) | v0.14.6 source |
| Edges | [schema-edges.mdx](ent-docs/schema-edges.mdx) | [Official](https://entgo.io/docs/schema-edges/) | v0.14.6 source |
| Fields | [schema-fields.mdx](ent-docs/schema-fields.mdx) | [Official](https://entgo.io/docs/schema-fields/) | v0.14.6 source |
| Indexes | [schema-indexes.md](ent-docs/schema-indexes.md) | [Official](https://entgo.io/docs/schema-indexes/) | v0.14.6 source |
| Mixin | [schema-mixin.md](ent-docs/schema-mixin.md) | [Official](https://entgo.io/docs/schema-mixin/) | v0.14.6 source |
| Views | [schema-view.mdx](ent-docs/schema-view.mdx) | [Official](https://entgo.io/docs/schema-views/) | v0.14.6 source |
| sql.DB Integration | [sql-integration.md](ent-docs/sql-integration.md) | [Official](https://entgo.io/docs/sql-integration/) | v0.14.6 source |
| External Templates | [templates.md](ent-docs/templates.md) | [Official](https://entgo.io/docs/templates/) | v0.14.6 source |
| Testing | [testing.md](ent-docs/testing.md) | [Official](https://entgo.io/docs/testing/) | v0.14.6 source |
| Transactions | [transactions.md](ent-docs/transactions.md) | [Official](https://entgo.io/docs/transactions/) | v0.14.6 source |
| Translations | [translations.md](ent-docs/translations.md) | [Official](https://entgo.io/docs/translations/) | v0.14.6 source |
| Graph Traversal | [traversals.md](ent-docs/traversals.md) | [Official](https://entgo.io/docs/traversals/) | v0.14.6 source |
| Versioned Migrations | [versioned-migrations.mdx](ent-docs/versioned-migrations.mdx) | [Official](https://entgo.io/docs/versioned-migrations/) | v0.14.6 source |
| Writing Docs | [writing-docs.md](ent-docs/writing-docs.md) | [Official](https://entgo.io/docs/writing-docs/) | v0.14.6 source |

## Tutorials

| Topic | Local source | Official page / source | Availability |
| --- | --- | --- | --- |
| Working with Edges | [tutorial-grpc-edges.md](ent-docs/tutorial-grpc-edges.md) | [Official](https://entgo.io/docs/grpc-edges/) | v0.14.6 source |
| Working with External gRPC Services | [tutorial-grpc-ext-service.md](ent-docs/tutorial-grpc-ext-service.md) | [Official](https://entgo.io/docs/grpc-external-service/) | v0.14.6 source |
| Generating a gRPC Service | [tutorial-grpc-generating-a-service.md](ent-docs/tutorial-grpc-generating-a-service.md) | [Official](https://entgo.io/docs/grpc-generating-a-service/) | v0.14.6 source |
| Generating Protobufs with entproto | [tutorial-grpc-generating-proto.md](ent-docs/tutorial-grpc-generating-proto.md) | [Official](https://entgo.io/docs/grpc-generating-proto/) | v0.14.6 source |
| gRPC Introduction | [tutorial-grpc-intro.md](ent-docs/tutorial-grpc-intro.md) | [Official](https://entgo.io/docs/grpc-intro/) | v0.14.6 source |
| Optional Fields | [tutorial-grpc-optional-fields.md](ent-docs/tutorial-grpc-optional-fields.md) | [Official](https://entgo.io/docs/grpc-optional-fields/) | v0.14.6 source |
| Creating the Server and Client | [tutorial-grpc-server-and-client.md](ent-docs/tutorial-grpc-server-and-client.md) | [Official](https://entgo.io/docs/grpc-server-and-client/) | v0.14.6 source |
| Configuring Service Method Generation | [tutorial-grpc-service-generation-options.md](ent-docs/tutorial-grpc-service-generation-options.md) | [Official](https://entgo.io/docs/grpc-service-generation-options/) | v0.14.6 source |
| Setting Up | [tutorial-grpc-setting-up.md](ent-docs/tutorial-grpc-setting-up.md) | [Official](https://entgo.io/docs/grpc-setting-up/) | v0.14.6 source |
| Setting Up | [tutorial-setup.md](ent-docs/tutorial-setup.md) | [Official](https://entgo.io/docs/tutorial-setup/) | v0.14.6 source |
| Query and Mutation | [tutorial-todo-crud.md](ent-docs/tutorial-todo-crud.md) | [Official](https://entgo.io/docs/tutorial-todo-crud/) | v0.14.6 source |
| GraphQL Field Collection | [tutorial-todo-gql-field-collection.md](ent-docs/tutorial-todo-gql-field-collection.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-field-collection/) | v0.14.6 source |
| Filter Inputs | [tutorial-todo-gql-filter-input.md](ent-docs/tutorial-todo-gql-filter-input.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-filter-input/) | v0.14.6 source |
| Mutation Inputs | [tutorial-todo-gql-mutation-input.md](ent-docs/tutorial-todo-gql-mutation-input.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-mutation-input/) | v0.14.6 source |
| Relay Node Interface | [tutorial-todo-gql-node.md](ent-docs/tutorial-todo-gql-node.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-node/) | v0.14.6 source |
| Relay Cursor Connections (Pagination) | [tutorial-todo-gql-paginate.md](ent-docs/tutorial-todo-gql-paginate.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-paginate/) | v0.14.6 source |
| Schema Generator | [tutorial-todo-gql-schema-generator.md](ent-docs/tutorial-todo-gql-schema-generator.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-schema-generator/) | v0.14.6 source |
| Transactional Mutations | [tutorial-todo-gql-tx-mutation.md](ent-docs/tutorial-todo-gql-tx-mutation.md) | [Official](https://entgo.io/docs/tutorial-todo-gql-tx-mutation/) | v0.14.6 source |
| Introduction | [tutorial-todo-gql.mdx](ent-docs/tutorial-todo-gql.mdx) | [Official](https://entgo.io/docs/tutorial-todo-gql/) | v0.14.6 source |
| Introduction | [versioned/01-intro.md](ent-docs/versioned/01-intro.md) | [Official](https://entgo.io/docs/versioned/intro/) | v0.14.6 source |
| Automatic migration planning | [versioned/02-auto-plan.mdx](ent-docs/versioned/02-auto-plan.mdx) | [Official](https://entgo.io/docs/versioned/auto-plan/) | v0.14.6 source |
| Upgrading Production | [versioned/03-upgrade-prod.mdx](ent-docs/versioned/03-upgrade-prod.mdx) | [Official](https://entgo.io/docs/versioned/upgrade-prod/) | v0.14.6 source |
| Planning a Migration | [versioned/04-new-migration.mdx](ent-docs/versioned/04-new-migration.mdx) | [Official](https://entgo.io/docs/versioned/new-migration/) | v0.14.6 source |
| Custom migrations | [versioned/05-custom-migrations.md](ent-docs/versioned/05-custom-migrations.md) | [Official](https://entgo.io/docs/versioned/custom-migrations/) | v0.14.6 source |
| Verifying migration safety | [versioned/06-verifying-safety.mdx](ent-docs/versioned/06-verifying-safety.mdx) | [Official](https://entgo.io/docs/versioned/verifying-safety/) | v0.14.6 source |
| Appendix: programmatic planning | [versioned/07-programmatically.mdx](ent-docs/versioned/07-programmatically.mdx) | [Official](https://entgo.io/docs/versioned/programmatically/) | v0.14.6 source |

## Auxiliary and development pages

| Topic | Local source | Official page / source | Availability |
| --- | --- | --- | --- |
| Blob Storage | [blob-storage.md](ent-docs/blob-storage.md) | [Official](https://entgo.io/docs/blob-storage/) | Development only; not v0.14.6 |
| Migrate Globally Unique ID | [globalid.mdx](ent-docs/globalid.mdx) | [Official](https://entgo.io/docs/globalid-migrate/) | v0.14.6 source |

## Shared components

| Topic | Local source | Official page / source | Availability |
| --- | --- | --- | --- |
| components/_atlas_migrate_apply.mdx | [components/_atlas_migrate_apply.mdx](ent-docs/components/_atlas_migrate_apply.mdx) | [Official](https://raw.githubusercontent.com/ent/ent/8037bc89bcab9a264099afa2672581237a3e079b/doc/md/components/_atlas_migrate_apply.mdx) | v0.14.6 source |
| components/_atlas_migrate_diff.mdx | [components/_atlas_migrate_diff.mdx](ent-docs/components/_atlas_migrate_diff.mdx) | [Official](https://raw.githubusercontent.com/ent/ent/8037bc89bcab9a264099afa2672581237a3e079b/doc/md/components/_atlas_migrate_diff.mdx) | v0.14.6 source |
| components/_installation_instructions.mdx | [components/_installation_instructions.mdx](ent-docs/components/_installation_instructions.mdx) | [Official](https://raw.githubusercontent.com/ent/ent/8037bc89bcab9a264099afa2672581237a3e079b/doc/md/components/_installation_instructions.mdx) | v0.14.6 source |

