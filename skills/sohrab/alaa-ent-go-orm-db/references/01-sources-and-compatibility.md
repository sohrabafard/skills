# Sources, freshness, and compatibility boundaries

## Contents

- [Verified baseline](#verified-baseline)
- [Source priority and refresh](#source-priority-and-refresh)
- [Corrections to the linked community pack](#corrections-to-the-linked-community-pack)
- [Evidence limits](#evidence-limits)

## Verified baseline

Verification date: **2026-11-05**, using primary sources and source inspection.

| Item | Observed evidence | Interpretation |
| --- | --- | --- |
| Go | [Downloads](https://go.dev/dl/) and [release history](https://go.dev/doc/devel/release) list Go 1.27.3 | Current verified stable release and this skill's minimum; refresh before selecting a newer toolchain |
| Ent | [v0.14.6 release](https://github.com/ent/ent/releases/tag/v0.14.6), published 2026-03-23 | Released API baseline; do not automatically upgrade an existing project |
| Ent module | [v0.14.6 go.mod](https://github.com/ent/ent/blob/v0.14.6/go.mod) declares Go 1.24 / toolchain go1.24.0 | Upstream's minimum is not a consumer target or proof of Go 1.27.3 compilation |
| Ent documentation | [Pinned source](https://github.com/ent/ent/tree/8037bc89bcab9a264099afa2672581237a3e079b/doc/md) | 75 complete English source files; 74 match v0.14.6, one Blob page is development-only |
| PostgreSQL documentation | [Current documentation](https://www.postgresql.org/docs/current/) resolves to major 18 | Use the actual server's major-version manual; this does not choose the user's server version |
| Community pack | [lwx-cloud/entgo-skills](https://github.com/lwx-cloud/entgo-skills/tree/3aa257d1f4f8ee21035c93fd585389012c1416f4), commit dated 2026-03-02 | Audited as inspiration and counterexamples; independently authored guidance replaces unverified snippets |

The bundled Ent source retains its original [Apache-2.0 license](ent-docs/LICENSE) and per-file [provenance manifest](ent-docs/manifest.json).
Its raw files are unchanged. Modernization instructions live in [10-go-and-generation.md](10-go-and-generation.md).
External media and linked example repositories are not bundled; the text and shared MDX includes are complete.

The community pack declares MIT in metadata, but its inspected repository tree contains no LICENSE file.
This package does not redistribute that pack's text or assume a license grant from its label.

## Source priority and refresh

Determine executable APIs from the project's pinned source and generated code.
Use official Ent documentation and source, official Go release/toolchain documentation, and the matching PostgreSQL manual for behavior.
Use maintainer documentation for pgx, Atlas, PgBouncer, GraphQL, and gRPC integrations.
Treat community examples as leads that require primary-source verification.

Refresh when changing a toolchain, dependency, feature flag, extension, migration mechanism, or version-specific database behavior.
Verify the installed version, selected release, API existence, and required configuration before adoption.
Retain exact versions and retrieval dates in the task evidence.
Do not repeatedly research stable principles during a narrow task. Use the bundled source when it matches the selected release.
When browsing is unavailable, mark volatile facts unverified and stop only decisions that depend on them.

## Corrections to the linked community pack

Apply relevant corrections; ordinary tasks need no whole-repository audit.

| Source-pack problem | Verified replacement |
| --- | --- |
| Index `.Where`, `.SchemaType`, `.Comment`, or `index.FieldIsNull` treated as available builders | Use actual `index` declarations and `entsql` annotations; express unsupported DDL through the migration owner |
| `Optional` and `Nillable` semantics reversed | Distinguish nullable/optional storage from Go pointer representation |
| `entgo.io/ent/schema/privacy` import | Use Ent's runtime privacy package or the application's generated privacy helpers as documented |
| `sql.P("...", args...)` | `sql.P` takes a builder callback; use verified predicates and dialect-aware binding |
| `sql.ExprP` assumed to rewrite `?` for PostgreSQL | Inspect placeholders; raw SQL fragments retain their SQL semantics |
| `entc.Generate` configuration omitted | Pass schema path, `*gen.Config`, then options |
| Eager loading described as a universal single JOIN | It executes association queries; project and bound each association |
| Soft-delete hook only sets a field before continuing a Delete operation | Implement and test the operation transformation; setting a field does not cancel deletion |
| Broad `privacy.DecisionContext(..., privacy.Allow)` used as include-deleted mode | Separate deletion visibility from authorization; broad allow can bypass privacy rules |
| `ent.WithTx` or nested `tx.BeginTx` assumed built-in | `WithTx` is a user helper; nested transactions/savepoints need explicit supported handling |
| Post-mutation hook treated as post-commit | Use the actual transaction commit boundary and durable delivery strategy |
| Upsert assumes update hooks run | Conflict updates use the create-hook path; enforce authorization/invariants explicitly |
| Startup auto-migration treated as production-safe | Use reviewed versioned migrations and explicit deployment authorization |

Primary checks: [index builder](https://github.com/ent/ent/blob/v0.14.6/schema/index/index.go), [SQL annotations](https://github.com/ent/ent/blob/v0.14.6/dialect/entsql/annotation.go), [fields](https://entgo.io/docs/schema-fields/), [privacy](https://entgo.io/docs/privacy/), [hooks](https://entgo.io/docs/hooks/), [transactions](https://entgo.io/docs/transactions/), [CRUD/upsert](https://entgo.io/docs/crud/), [query template](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/dialect/sql/query.tmpl), [select template](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/dialect/sql/select.tmpl).

## Evidence limits

Documentation/source review verifies described APIs and intended behavior, not the generated consumer application's runtime.
The package is model-neutral. It does not extrapolate Alaa's older model-specific prompting policy to newer model identities.
Consumers must perform the task-specific generation, compile, PostgreSQL, and performance checks in [70-runtime-testing.md](70-runtime-testing.md).
Do not infer live host compatibility from portable metadata or infer database safety from an archive validation result.
