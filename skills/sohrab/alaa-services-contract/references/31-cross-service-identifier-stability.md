# Cross-Service Identifier Stability

Read this file when an identifier leaves its owning service, or before you retire, re-key, re-parent, merge,
or bulk-import an entity whose id another service may hold. `25-end-to-end-flow-and-boundaries.md` owns the
user and project UUIDv7 shapes and the private-versus-public identifier boundary; this file owns what the
owner may do to an id after it is published. Conformance evidence is in `95-fleet-conformance.md`.

## When an id is published

An id is published once any of these is true:

- another service stores it;
- it rides in a token claim or a trusted header;
- it is part of an OpenFGA object id or tuple;
- it appears in an event payload or a public API.

## Rules for a published id

- Never renumber a published id, reuse it for another entity, or hard-delete its row. A consumer's stored
  copy would then name the wrong entity or nothing, and no consumer can detect that.
- Retire the entity by archiving it (soft delete). Keep the row, and keep its id reserved.
- A bulk importer or sync job matches existing rows on the stable id and never re-keys them.
- A change to an entity's meaning or structural position is a contract change for every consumer. Examples:
  moving a location under another parent, or merging two ids into one. It needs an announcement path to every
  consumer before it ships. The fleet has no defined announcement mechanism yet: `NEEDS_CONFIRMATION`.
- A display-text rename is not a contract change.
- The owning service documents its published ids. Each consumer documents which published ids it stores.

## Identifier form per layer

Verified 2026-11-11 against the cited files. Every other reference points here for an identifier's form in a
claim, a header or OpenFGA, and states none itself.

| Id | Owner storage | Token claim | Trusted header | OpenFGA | Crockford encoded by |
|---|---|---|---|---|---|
| Location: `ostan`, `shahrestan`, `bakhsh`, `shahr`, `shobe`, `school` | `auth` bigint primary key (`auth: database/migrations/2026_03_10_120500_bootstrap_postgres_schema.php:36-119`) | `loc.o`, `loc.sr`, `loc.b`, `loc.sh`, `loc.br`, `loc.sc`: JSON integer; null or non-positive becomes `0` (`auth: app/Services/Auth/TokenService.php:726-753`) | `X-Location-*`: decimal integer, sent only when positive (`gateway: charts/gateway/values.yaml:164-169`; `charts/gateway/templates/configmap.yaml:1549-1557`) | `<type>:<prefix><Crockford uint64>`; prefixes `ost_`, `shrs_`, `bkh_`, `shr_`, `shob_`, `sch_`; id `0` has no object. Ostan 39 is `ostan:ost_17` (`authz-openfga: platform/openfga/contracts/authorization-contract.yaml:296-303,391-412`) | `authz-sidecar` from the headers (`internal/decision/geography_codec.go:12-20,65-78`; `codec.go:78-94`); `entitlement-api` reflector for grant subjects (`internal/projection/rulekey.go:167`); `authz-openfga` seed generator for `child_*` edges |
| Country | none; no `auth` table | none | none | fixed `country:ctry_1` (contract `:393-394,749`) | constant in `authz-sidecar` (`internal/decision/geography.go:75-77`) |
| User | `auth` `users.uuidv7`; shape owned by reference `25` | `sub`: lowercase hyphenated UUIDv7 (`TokenService.php:680`) | `X-User-Id`: the same text | `user:<UUIDv7 text>`, never encoded (contract `:356-362`; `authz-sidecar: internal/decision/principal.go:24-36`) | nobody |
| Project | `auth` `projects.uuidv7` (`auth: database/migrations/2026_03_21_120000_create_projects_table.php:14,17`); shape owned by reference `25` | `pid`: UUIDv7 text (`TokenService.php:672,687`) | `X-Project-Id`: the same text | `project:p_<26-character Crockford of the 16 UUID bytes>`; the same `p_` segment opens every project-scoped object id (contract `:264-271,350-352`) | `gateway` Lua (`haproxy/lua/authz-sidecar.lua:282-297`); `authz-sidecar` (`encodeProjectUUID`, `internal/decision/codec.go:13-28`); `entitlement-api` reflector (`rulekey.go:201`) |
| Course, set, content | `content` `public_id` uuid, unique per project (`content: database/migrations/2026_04_15_121732_create_content_service_schema.php:77,90,98,110,150`) | none | none; arrives as UUIDv7 text in a path segment or comment target ref | resource segment: 26-character Crockford of the UUIDv7 bytes, for example `content:p_06emthamvssaf9p2rfxq1p1ay0__cnt_06emtsgw09xh1d0x3nfktfmffw` (contract `:278-291,413-436`) | `gateway` Lua (`authz-sidecar.lua:35-39,742-757`); `authz-sidecar` for comment refs (`codec.go:30-37`); `entitlement-api` reflector (`rulekey.go:201`) |

- The Crockford form exists only inside OpenFGA object ids and in `X-Authz-Canonical-Object-Id` from the
  gateway to the sidecar. Claims and identity or location headers carry the owner's text form.
- A backend service that reads trusted headers never encodes or decodes Crockford. The `entitlement-api`
  reflector encodes only to write tuples.
- Every encoder reproduces the contract golden vectors (contract `:304-328`). `/alaa-crockford-base32-codecs`
  owns shared codec assets.
- `NEEDS_CONFIRMATION`: the owner stated on 2026-11-11 that only the sidecar converts to Crockford. Current code
  also encodes in the gateway Lua and in the `entitlement-api` reflector, as the last column shows.
- `NEEDS_CONFIRMATION`: when a project has no `uuidv7` row, `pid` falls back to the internal integer
  (`auth: app/Support/Auth/TrustedProjectContext.php:46-48`; `TokenService.php:672`). The gateway and the sidecar
  then refuse it as a non-UUIDv7 project (`authz-sidecar.lua:830-833`; `internal/decision/engine.go:302-305`).

## Registry of published ids

Verified 2026-11-09 against the cited files. Add a row before a new id leaves its owner. Forms are in the table
above.

| Id | Stored or carried by | Retirement |
|---|---|---|
| Location ids | JWT `loc` and `X-Location-*`; OpenFGA geography objects and stored `child_*` edges from the versioned seed (`authz-openfga: platform/openfga/topology/country-ostan.yaml`; contract `:746-766`); stored `entitlement-api` grant principals (`entitlement-api: internal/domain/grants/validation.go:15-23,294-310`; `internal/projection/rulekey.go:51-63`) | soft delete on all six tables (migration `:44,55,69,86,98,113`; `auth: app/Models/BaseModel.php:18-22`); admin archive soft-deletes (`auth: app/Repositories/Admin/EloquentAdminCatalogRecordRepository.php:50-52`) |
| `country:ctry_1` | every geography decision; `entitlement-api` `country` principals (`validation.go:15-23`) | not applicable |
| Project UUIDv7 (`pid`) | JWT `pid`, `X-Project-Id`, OpenFGA project segment | reference `25` |
| User UUIDv7 (`sub`) | reference `25` | reference `25` |
| Course, set and content `public_id` | OpenFGA resource segment; stored `entitlement-api` grant objects with `*_public_id` context (`validation.go:330-357`); stored `wa` `content_id`, `set_id`, `course_id` as lowercase UUIDv7 (`wa: clickhouse/ddl/001_init.sql:99-100,130-135`); stored `comment-service` `target_ref` `<type>:<id>`, whose own validator accepts any identifier form (`comment-service: app/Support/Comment/CommentContextRef.php:17,72-75`) | soft delete (`content: database/migrations/2026_05_10_030818_add_soft_deletes_to_content_hierarchy.php`; `app/Models/Course.php:18`, `Set.php:18`, `Content.php:19`) |
