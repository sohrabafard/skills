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

## Registry of published ids

Verified 2026-11-09 against the cited files. Add a row before a new id leaves its owner.

| Id | Owner and form | Published through | Retirement |
|---|---|---|---|
| Location ids: `ostan`, `shahrestan`, `bakhsh`, `shahr`, `shobe`, `schools` | `auth`; bigint primary key, no separate public id (`auth: database/migrations/2026_03_10_120500_bootstrap_postgres_schema.php:36-119`) | JWT `loc` claim `o`, `sr`, `b`, `sh`, `br`, `sc` (`auth: app/Services/Auth/TokenService.php:688,726-753`) projected to `X-Location-*` (`gateway: charts/gateway/values.yaml:164-169`); OpenFGA objects `ostan:ost_`, `shahrestan:shrs_`, `bakhsh:bkh_`, `shahr:shr_`, `shobe:shob_`, `school:sch_` plus the lowercase Crockford Base32 of the key (`authz-openfga: platform/openfga/contracts/authorization-contract.yaml:391-412`), with stored `child_*` edges from the versioned seed (`authz-openfga: platform/openfga/topology/country-ostan.yaml`; contract `:746-766`); stored `entitlement-api` grant principals (`entitlement-api: internal/domain/grants/validation.go:15-23,294-310`; `internal/projection/rulekey.go:51-63`) | soft delete on all six tables (migration `:44,55,69,86,98,113`; `auth: app/Models/BaseModel.php:18-22`); admin archive soft-deletes (`auth: app/Repositories/Admin/EloquentAdminCatalogRecordRepository.php:50-52`) |
| `country:ctry_1` | `authz-openfga`; fixed seed object, no `auth` table (contract `:749`) | country item of every geography decision (`authz-sidecar: internal/decision/geography.go:75-77`); entitlement-api `country` principals (`validation.go:15-23`) | not applicable |
| Project UUIDv7 (`pid`) | `auth`; shape owned by reference `25` | JWT `pid` (`TokenService.php:687`) projected to `X-Project-Id`; OpenFGA project segment | reference `25` |
| User UUIDv7 (`sub`) | `auth`; shape owned by reference `25` | reference `25` | reference `25` |
| Course, set and content `public_id` | `content`; `uuid`, unique per project (`content: database/migrations/2026_04_15_121732_create_content_service_schema.php:77,90,98,110,150,167`) | OpenFGA resource segment, 26-character Crockford Base32 of the UUIDv7 (contract `:278-291`; `gateway: haproxy/lua/authz-sidecar.lua:35-39`; `authz-sidecar: internal/decision/codec.go:30-37`); stored `entitlement-api` grant objects with `*_public_id` context (`validation.go:330-357`); stored `wa` `content_id`, `set_id`, `course_id` as lowercase UUIDv7 (`wa: clickhouse/ddl/001_init.sql:99-100,130-135`); stored `comment-service` `target_ref` `<type>:<id>`, whose own validator accepts any identifier form (`comment-service: app/Support/Comment/CommentContextRef.php:17,72-75`) | soft delete (`content: database/migrations/2026_05_10_030818_add_soft_deletes_to_content_hierarchy.php`; `app/Models/Course.php:18`, `Set.php:18`, `Content.php:19`) |
