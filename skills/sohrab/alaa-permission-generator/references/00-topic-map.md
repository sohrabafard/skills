# Topic Map

Load the one file whose condition matches the task in front of you. Every row states a situation you can observe
before you act, not a subject heading, so you can route without reading the files first. The out-of-skill routing
table lives in `SKILL.md` under "Not owned here"; this file routes only inside the skill, so the two cannot drift.

| You are about to | Read |
|---|---|
| run a catalog command, gate CI on one, or explain an exit code a command just returned | `references/command-surface.md` |
| add or edit a permission entry, register an owner or an aggregate consumer, or interpret a drift finding | `references/catalog-workflow.md` |
| rename, deprecate, reserve, or withdraw a permission that has already shipped | `references/lifecycle.md` |
| write or review any consumer that reads the permission bitmap, in any language | `references/shared-consumer-contract.md` |
| touch `config/permissions.php`, Laravel authorization, or trusted-context middleware | `references/laravel-consumer.md` |
| touch `permissions_gen.go`, a Go decoder, or a Go authz package | `references/go-consumer.md` |
| touch `permission-catalog.ts`, the frontend SDK, or a UI capability hint | `references/typescript-consumer.md` |
| diagnose a non-zero exit, a blocking finding, or a clean result you doubt | `references/failure-modes.md` |
| stand up bitmap decoding in a service, or catch yourself about to hand-write a decoder | `assets/permission-bitmap/` |
| change any canonical decoder, or ship a decoder change of any size into any service | `scripts/bitmap-conformance.sh` |
| add an input class every decoder must handle, or explain the harness exiting `6` | `scripts/permission-bitmap-corpus.json` |
| judge whether the catalog tool should emit the decoder rather than only the map | `references/catalog-decoder-emission-proposal.md` |

## The decoder assets

A service copies the canonical implementation for its language rather than writing one. `SKILL.md` states where each
file is copied to and what may be changed on the way in; the files themselves are:

| Language | File |
|---|---|
| Go | `assets/permission-bitmap/permission_bitmap.go` |
| PHP | `assets/permission-bitmap/PermissionBitmap.php` and `assets/permission-bitmap/PermissionBitmapException.php` |
| TypeScript | `assets/permission-bitmap/permission-bitmap.ts` |

Fix a defect in one of these here first, then re-propagate it, because a fix applied only where the bug surfaced
leaves every other service running the bug. Run `scripts/bitmap-conformance.sh` before the change ships and record
its output: it drives every implementation whose toolchain is present over `scripts/permission-bitmap-corpus.json`
and prints `skipped: <runtime> not installed` for the rest. **A skipped runtime is unproved, not passing.**

## Reading order for a new permission

`references/catalog-workflow.md`, then `references/lifecycle.md` before you allocate an id, then the consumer
reference for each language that will read the bit, then `references/command-surface.md` for the commands and
`references/failure-modes.md` for whatever they return. Allocating first and reading the lifecycle rules afterwards
is the order that publishes an id you then cannot take back.
