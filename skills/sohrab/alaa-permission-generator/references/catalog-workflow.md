# Catalog Governance, Descriptors, and Drift

## Repository surfaces

- `catalog/permissions.json` — canonical registry, the only id allocation surface.
- `catalog/services.json` — importer and generator descriptors. `services` holds permission owners;
  `aggregate_consumers` holds consumers that read the whole active catalog and own no `service_key`.
- `generated/auth/database/seeders/data/permissions.php` — proposed auth seed. This path is hardcoded in the generator.
- `generated/<owner_repo>/<path from generated_targets>` — proposed service artifact. Drift compares the applied file
  against generated output byte for byte after line-ending normalisation, so the applied path must equal the declared
  `source_path` exactly; no shortened or equivalent path is accepted.
- `generated/reports/permission-drift-report.md` — human drift review; `.json` — machine drift detail.
- `RUN_BOOK.md` — the project's operator procedure. It leads every change with `import`; see the discriminator in
  `references/command-surface.md` before following it.

## Permission entry

Every entry carries `bitmap_id`, `bit_index`, `permission_key`, `service_key`, `description`, `status`, `aliases`,
`legacy_keys`, `owner_repo`, `generated_targets`, `source_refs`, `notes`, and `display_name`. `bitmap_id`, `bit_index`,
`permission_key`, `service_key`, `status`, and `owner_repo` are read without a default and must be present.

Hard limits, each enforced by a refusal that exits `2`:

- `permission_key` must match `/^[a-z][a-z0-9_]*$/`.
- No generated TypeScript line may exceed 80 columns, which caps `permission_key` length. The widest line is in
  `BITMAP_ID_BY_PERMISSION`: 19 columns of indent and syntax, plus the upper-cased key, plus the id's digits. A key stays
  safe below roughly 55 characters; verify a longer one by generating rather than by counting.
- A Go target must end in `.go` and sit in a directory whose name matches `/^[a-z][a-z0-9_]*$/`, because the Go package
  is derived from that directory name.
- An aggregate consumer's `scope` must be `all_active` and its `input_shape` must be `typescript_permission_catalog`.

`status` is a three-value enum — `active`, `deprecated`, `reserved` — with no state machine, no transition validation,
no date, and no successor field. Anything else is a fatal `INVALID_STATUS`. What each status does per artifact, and the
migrations, are in `references/lifecycle.md`.

`notes` is load-bearing free text: two fatal-to-info downgrades depend on substrings in it. Treat it as code — see
`references/failure-modes.md` before editing a `notes` value.

## Generated targets

```json
"generated_targets": [
  "auth:database/seeders/data/permissions.php",
  "example:services/example/internal/authz/permissions_gen.go"
]
```

The prefix before `:` **must equal that entry's own `service_key`**; the remainder is the repository-relative path.
A mismatched prefix is skipped with no finding, no warning, and no error, so the artifact is silently never written.
The directory the generator writes into comes from the entry's `owner_repo`, while the importer reads
`services[].owner_repo` plus `services[].source_path`. The two files are never cross-validated: when they disagree,
drift-checking reads a file the generator never writes and every report stays clean. After adding a target, confirm the
file appeared under `generated/` before believing any clean report.

Aggregate consumers are never listed here: they own no `service_key`, and their coverage comes from `scope: all_active`,
so a new permission reaches them with no per-permission bookkeeping.

## Descriptors

A permission owner goes in `services` and needs all five keys, `generated_target` included — it is read by nothing, but
the file will not parse without it.

```json
{
  "service_key": "example",
  "owner_repo": "example",
  "source_path": "config/permissions.php",
  "input_shape": "service_config",
  "generated_target": "generated/example/config/permissions.php"
}
```

`input_shape` has exactly three values for an owner, and the choice changes behaviour:

- `auth_seed` — the **only** shape that creates catalog entries. Requires a PHP file returning a list of rows.
- `service_config` — a PHP file returning a keyed array. Contributes observations only, never catalog entries.
- `go_service_permission_map` — regex-scrapes the forward `map[int]string` block. **Uniquely tolerates a missing file**,
  which is how a Go service is registered before its map is applied: `import` skips it and reports no error. For the
  other two shapes a missing file exits `2`.

For a Go owner inside a monorepo, keep `owner_repo` as the repository name and put the full nested path in
`source_path`, `generated_target`, and the entry's `generated_targets`.
An aggregate consumer goes in the separate `aggregate_consumers` array and uses `consumer_key` instead of
`service_key`, plus `scope`:

```json
{
  "consumer_key": "client",
  "owner_repo": "client",
  "source_path": "packages/sdk-auth/src/generated/permission-catalog.ts",
  "input_shape": "typescript_permission_catalog",
  "generated_target": "generated/client/packages/sdk-auth/src/generated/permission-catalog.ts",
  "scope": "all_active"
}
```

Unlike a `services[]` entry, an aggregate consumer's `generated_target` **is** read: it determines the output path,
with a leading `generated/` stripped. Both `scope` and `input_shape` are validated in the constructor and anything else
exits `2`.

## Onboarding a Laravel owner produces nothing until the generator is edited

Only two `service_config` outputs are generated at all — `content` and `comment-service` — because the generator
hardcodes those two calls. Go and TypeScript outputs are data-driven; Laravel outputs are not. `docs/service-onboarding.md`
and `RUN_BOOK.md` both promise a generated config for any newly registered service and are wrong. When onboarding a
third Laravel service, report the generator edit as required work up front instead of predicting an output file.

Expect `CONSUMER_PERMISSION_MISSING_FROM_AUTH` (error, blocking) for every permission the new service declares that the
catalog does not yet hold. That is the signal to add those entries, not a tool failure.

## Drift severity — the machine contract

Fatal and error findings block apply. Warning and info do not. `--strict` returns `1` when any fatal or error exists.

| Code | Severity |
| --- | --- |
| `INVALID_BITMAP_ID`, `BIT_INDEX_MISMATCH`, `INVALID_STATUS` | fatal |
| `DUPLICATE_BITMAP_ID`, `SAME_SERVICE_PERMISSION_DIFFERENT_IDS`, `SAME_NAME_DIFFERENT_IDS` | fatal |
| `MALFORMED_CONSUMER_PERMISSION`, `DANGEROUS_BITMAP_COLLISION` | fatal |
| `CONSUMER_PERMISSION_MISSING_FROM_AUTH`, `CONSUMER_PERMISSION_NAME_MISSING_FROM_AUTH` | error |
| `CANDIDATE_ALIAS`, `AUTH_PERMISSION_UNUSED_BY_INSPECTED_SERVICES` | warning |
| `RESOLVED_EXTRACTION_REALLOCATION`, `RESOLVED_COMMENT_CANONICALIZATION` | info |
| `AGGREGATE_CONSUMER_ARTIFACT_NOT_APPLIED` | warning |
| `AGGREGATE_CONSUMER_STALE_METADATA`, `AGGREGATE_CONSUMER_MANUAL_EDIT` | error |
| every other `AGGREGATE_CONSUMER_*` — `_PERMISSION_MISSING`, `_PERMISSION_EXTRA`, `_BITMAP_ID_MISMATCH`, `_IDENTIFIER_COLLISION`, `_MAP_DESYNC`, `_MALFORMED`, `_GENERATION_FAILED` | fatal |

Reading this table:

- `SAME_NAME_DIFFERENT_IDS` is emitted by two different checks — one over catalog entries, one over source observations.
  Read the finding's context payload to tell which; never treat the code as a single condition.
- `AUTH_PERMISSION_UNUSED_BY_INSPECTED_SERVICES` is warning-only and expected in bulk: a clean report consists almost
  entirely of these. It is emitted for entries of every status, so deprecating a permission adds one rather than
  removing one.
- `CANDIDATE_ALIAS` is emitted only nested inside a `DANGEROUS_BITMAP_COLLISION`, and its similarity trigger matches
  almost any pair of permission names, so it carries close to no signal. Resolve the collision; do not act on the alias
  suggestion, and remember that writing `aliases` changes no behaviour.
- `DANGEROUS_BITMAP_COLLISION` means one id maps to two names. Correct ownership in `catalog/permissions.json`; never
  resolve it by remapping a consumer or by reusing an id.
- Every `AGGREGATE_CONSUMER_*` finding has one remedy: regenerate, copy the generated file over the applied file, never
  hand-edit. CRLF is normalised before comparison, so a Windows checkout reports no false drift.

## Apply boundaries

Generation writes review artifacts only; copy and apply is a separate, explicitly authorized step. Auth seed apply,
downstream service apply, and aggregate consumer apply are three separate lanes, and assigning a permission to an
admin, role, or user is a fourth, auth-owned state mutation. Do not combine lanes without explicit scope per the
authorization default in `SKILL.md`. Lane procedure, approval and proof strength are owned by `/alaa-controlled-ops`
(`$alaa-controlled-ops`).
