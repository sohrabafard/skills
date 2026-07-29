---
name: alaa-permission-generator
description: "Register, generate, apply, and validate Alaa coarse permissions through alaa-permission-catalog. Use when adding, renaming, deprecating, or reserving a permission key or bitmap id, onboarding a Laravel config/permissions.php consumer, a Go internal/authz/permissions_gen.go consumer, or a TypeScript aggregate consumer such as the client permission-catalog.ts, syncing the auth seed, decoding a trusted X-Access bitmap, deriving unverified frontend UI capability hints, investigating catalog drift, or removing service-local permission-map duplication. Do not use for OpenFGA object-level can_* relations - use /openfga ($openfga). Do not use for gateway route authorization policy, JWT verification, or who may assert a trusted header - use /alaa-trust-gateway-auth ($alaa-trust-gateway-auth)."
---

# Alaa Permission Generator

`alaa-permission-catalog` is the only allocator of coarse permission names and global bitmap ids. Auth issues `prm`,
`prv`, and `av` at runtime. The gateway is the trusted-header boundary. OpenFGA holds a separate object-level
vocabulary. This skill owns allocation in the catalog and emission into consumers, and nothing beyond those two.

## Step 0 — locate the tool before anything else

The catalog is a repository of its own, separate from every service repository. Resolve its root in this order:

1. A path supplied in the request — a catalog-root argument, or a plain path the requester names. This wins.
2. Otherwise a directory named `alaa-permission-catalog` beside the current service checkout, because the catalog is a
   sibling of the service repositories rather than a child of any one of them.

Confirm a candidate root by the presence of `alaa-permission-catalog/scripts/permission_catalog.php`. Running it needs PHP 8.2 or newer and
nothing else: the project has zero runtime dependencies and that entrypoint carries its own autoloader, so **do not run
`composer install`** — invoke the entrypoint directly.

**Hard stop, and the most important rule here.** If no candidate root contains `alaa-permission-catalog/scripts/permission_catalog.php`, report
every path you tried, stop, and ask the requester where the catalog is. Do not hand-write, infer, reconstruct, or copy by eye a permission map, a
`bitmap_id`, an auth seed row, a `config/permissions.php`, a `permissions_gen.go`, or a `permission-catalog.ts`. A
hand-built permission map is the outcome every other rule here exists to prevent; "catalog root not found, need the
path" is the correct report.

**Second stop, the most common false alarm.** `catalog/services.json` sets `source_root` to the absolute path
`D:/Sohrab/Project`, and every command that reads an owner's source file resolves
`<source_root>/<owner_repo>/<source_path>`. With the sibling repositories absent from that path, those commands exit `2`
with `Configured source file not found: <path>`. That is a missing checkout, not a broken tool: report which
repositories are missing at which path and stop. Do not edit `source_root` to route around it.

## Authorization default

Four operations are separately reviewable: editing the catalog, applying a generated artifact into a service repository,
applying the auth seed, and assigning a permission to a user or role. **The default is deny** — perform an operation
only when the request names it.

- Editing `catalog/permissions.json` or `catalog/services.json` and running the catalog commands: authorized by any
  request to add, change, rename, deprecate, or reserve a permission.
- Applying a generated artifact into a service repository: requires the request to name applying, or to name that
  repository or that file as a place to change.
- Applying the auth seed, and assigning a permission to a user, role, or admin: each requires explicit words naming the
  seed or the assignment. A request to "add a permission" authorizes neither.
- Anything you cannot place in one of those three lines: ask. Report each unauthorized operation the change still needs
  as remaining work, named and pathed. Lane procedure and proof strength are owned by `/alaa-controlled-ops`
  (`$alaa-controlled-ops`).

## Non-negotiable contract

- `catalog/permissions.json` is the only place a `bitmap_id` is allocated. Nothing computes the next free id: read the
  current maximum from that file and allocate above it.
- `bit_index` equals `bitmap_id - 1` in every entry. The tool enforces this and `bitmap_id > 0` as fatal findings.
- Never reuse, renumber, or delete a published `bitmap_id`; deprecate or reserve it per `references/lifecycle.md`.
  **The tool will not catch a violation** — the duplicate, same-name, and same-service checks index `status: active`
  entries only, so an active entry may take a `reserved` or `deprecated` id and produce no finding at all. Before
  allocating, scan entries of every status for the id. This is a discipline you hold, not an invariant the tool holds,
  and the project's governance doc asserts the opposite.
- `aliases` is dead config: parsed, serialised, read by no code path. Writing it changes no behaviour. Use `legacy_keys`
  per `references/lifecycle.md` to carry an old name forward.
- Deprecating a permission does not retire it from Laravel: status is honoured by the Go and TypeScript emitters and
  ignored by both PHP emitters. Read `references/lifecycle.md` before any retirement.
- Six rules hold for every consumer in every language — commit at the exact source path; allow no override; the bit
  contract; ignore unknown bits and fail closed on zero known permissions; never hand-edit a generated file;
  re-validate after applying. They are stated once in `references/shared-consumer-contract.md`, with the observability
  and per-request cost rules. Read it before writing or reviewing any consumer code.
- **`MaxPermissionID()` is per-file, not per-catalog.** Each generated Go map returns the highest id in *that service's*
  map — `tusd` returns 95, `news` returns 119, `wa` returns 1 — and the generated `Decode` passes it as the decode
  bound, so an id above a service's own generated maximum is dropped by that service even while auth issues it. Apply
  the consuming service's generated map in the same change as the auth seed, because a seed-only change leaves the
  service unable to see the permission it was just granted.
- **Never freeze the scale.** No permission count, maximum id, or fingerprint goes into code, a comment, a test, or a
  report. Read them from `catalog/permissions.json`, from `generated/reports/permission-catalog-summary.md` and
  `generated/reports/permission-drift-report.json`, or from `PERMISSION_CATALOG_ACTIVE_COUNT`,
  `PERMISSION_CATALOG_MAX_BITMAP_ID`, and `PERMISSION_CATALOG_FINGERPRINT` at the end of the generated TypeScript
  artifact. **The id ranges the project's `docs/` state are not the problem; their incompleteness is.** Every range
  those documents name — `64-78`, `79-91`, `92-95`, `96-107` — was still correct on 2026-07-27, so treating all of them
  as stale makes a reader re-derive a range that was right. What no catalog document mentions is the `news` block at ids
  `108-119` or the `auth` admin and scope block at ids `120-130`, so a reader who stops at `docs/` concludes the catalog
  ends at 107. Read the current count and maximum from the sources named above, never from a document and never from
  this paragraph.

## One decoder, not one per service

`alaa-permission-catalog` allocates ids and emits maps; it holds no encoder and no decoder in any language. The bit
unpacking, the base64url handling, the error taxonomy, and the question "does this bitmap grant permission N" therefore
live outside it, and until this skill shipped them they lived in a hand-written file inside each consuming service. That
is the shape that produced the Crockford Base32 incident this repository already paid for: four implementations under
one contract, and the first run of all four together found five divergences.

**A service does not hand-write a permission-bitmap decoder.** It copies the canonical implementation for its language
from this skill, which is generated-adjacent source a service does not edit locally.

| Language | Asset | Copied into, changing only |
| --- | --- | --- |
| Go | `assets/permission-bitmap/permission_bitmap.go` | the package holding `permissions_gen.go`; the package clause |
| PHP | `assets/permission-bitmap/PermissionBitmap.php` with `PermissionBitmapException.php` | the namespace reading `config/permissions.php`; the namespace |
| TypeScript | `assets/permission-bitmap/permission-bitmap.ts` | the SDK package beside `permission-catalog.ts`; nothing |

- **Fix a defect in a canonical implementation here, then re-propagate it to every consumer**, because a fix applied
  only where the bug surfaced leaves every other service running the bug.
- **Run `scripts/bitmap-conformance.sh` before a change to any canonical implementation ships**, and record its output,
  because a change proved in one runtime is not proved in the others. It drives every implementation whose toolchain is
  present over `scripts/permission-bitmap-corpus.json`, prints `pass`, `fail`, or `skipped: <runtime> not installed` per
  runtime, and never reports a pass for a runtime it did not run. **A skipped runtime is unproved, not passing.**
- **Add a new input class to the corpus rather than to one language's test file**, because a corpus case binds all three
  implementations and a test-file case binds one. The corpus carries `corpus_sha256` over its case array; the harness
  recomputes it on every run and exits `6` on a mismatch, so a drifted copy is visible instead of silent.
- The canonical implementations carry the encoded-length cap that `references/shared-consumer-contract.md` requires, as
  a fallback bound plus an explicit-cap entry point. The value a service enforces is owned by
  `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
- **The frontend is a consumer of `assets/permission-bitmap/permission-bitmap.ts`, never the author of a second
  decoder.** A client-side permission read is a UI hint and never an authorization decision:
  `alaa-vue-typescript-clean-code references/72-frontend-security-binding.md` — `/alaa-vue-typescript-clean-code`
  (`$alaa-vue-typescript-clean-code`) — and
  `alaa-ui-ux-design-system references/25-untrusted-content-and-ui-authority.md` — `/alaa-ui-ux-design-system`
  (`$alaa-ui-ux-design-system`) — both state that framing, and the affordance rule (hide, disable-with-reason, or
  show-and-fail) is owned by the design-system skill.

The durable fix is for the catalog tool to emit the decoder beside the map, so there is one source rather than one
source plus a propagation discipline. `references/catalog-decoder-emission-proposal.md` states that change request, what
it would break, and what deciding it needs. It is a proposal, and this skill does not edit that repository.

## Which reference to read

Read `references/00-topic-map.md` and load only the file whose triggering condition matches the task in front of you.

Load `/alaa-services-contract` (`$alaa-services-contract`) and `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`)
for every implementation. Add `/alaa-golang` (`$alaa-golang`) for Go, `/alaa-laravel-architecture`
(`$alaa-laravel-architecture`) and `/alaa-php-clean-code` (`$alaa-php-clean-code`) for Laravel, or
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) and `/alaa-mono-package` (`$alaa-mono-package`)
for TypeScript. Add `/alaa-security-review` (`$alaa-security-review`) whenever a consumer reads token claims.

## When not to use

Do not use this skill to decide whether a caller may act on a resource, or what a service may believe about the header a permission arrived on — that is `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Do not use it for object-level relationship authorization, which is the vendored `openfga` skill. Do not use it for the TOTP step-up contract, which is `/alaa-services-contract` (`$alaa-services-contract`) `references/32-auth-totp-and-step-up-contract.md`. Do not use it to write the application code that consumes a decoded permission set; take that shape from the owning language skill.

## Ownership boundary

This skill owns permission-key and bitmap-id allocation, the catalog descriptors, generation, drift interpretation, the
apply boundary, and the consumer-side contract for reading the bitmap. Everything below belongs elsewhere and **the
listed owner wins on conflict**, with two refinements: `/alaa-services-contract` wins on what a signal is *called* and
`/alaa-observability-soc` wins on whether it is *required*; and every timeout, retry, pool and shed value lives in
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md` — this skill states none.

| Not owned here | Owner |
| --- | --- |
| Trusted-header assertion, JWT verification, header sanitisation, tenant derivation | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Object-level relations, `can_*`, tuples | `/openfga` (`$openfga`) |
| Log, metric, event and code **names**; request deadlines; the error envelope | `/alaa-services-contract` (`$alaa-services-contract`) |
| Whether a signal is **required**, and its gate | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Retry, backoff, circuit-breaking, degradation doctrine | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Complexity budgets, structure choice, the whole N+1 family | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| What makes a test a test, and which layer it belongs at | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Design pass when an interface, a data writer, or a consistency, ordering, idempotency, concurrency or caching property changes | `/alaa-system-design` (`$alaa-system-design`) |
| Security review triggers, threat classes, the fail-closed discriminator | `/alaa-security-review` (`$alaa-security-review`) |
| Controlled-operation procedure and proof strength for the apply lanes | `/alaa-controlled-ops` (`$alaa-controlled-ops`) |
| Long-task phasing and resumable state | `/alaa-workflow` (`$alaa-workflow`) |
| The quality bar itself | `alaa-project-constitution references/quality-bar.md` |
| Model choice and reasoning effort | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
| Per-language validation commands and design-pattern selection | `/alaa-golang`, `/alaa-vue-typescript-clean-code`, `/alaa-mono-package`, `/alaa-laravel-architecture`, `alaa-php-clean-code references/design-patterns.md` |

The test **cases** named in the three consumer references stay here: byte-boundary bit indexing and drift-code coverage
are domain facts, not generic test design.

## Completion evidence

Report the allocated keys and ids, every generated path and every applied path separately, the drift counts by severity
with the command that produced them, the target repository's tests you ran, and every auth-owned or assignment
operation left outstanding. Keep three things distinct and never merge them: catalog truth, source-repository truth, and
an unapplied generated proposal.
