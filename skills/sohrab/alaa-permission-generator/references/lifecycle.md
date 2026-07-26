# Permission Lifecycle: Rename, Deprecate, Reserve, Withdraw

A permission withdrawn in the catalog keeps granting in a Laravel or Go consumer until that consumer's artifact is
regenerated, applied, and deployed. Treat every retirement as a security change with a deploy-length window, and follow
the deprecation windows in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## What status does, per artifact

`deprecated` and `reserved` behave identically in every code path; only intent differs. Neither is a synonym for
"revoked".

| Artifact | A `deprecated` or `reserved` entry is |
| --- | --- |
| TypeScript aggregate | **dropped** — the name stops existing in the client at the next regeneration |
| Go service map | **dropped**, and `MaxPermissionID()` shrinks if it was the highest |
| Auth seed PHP | **kept, and unmarked** — the emitter applies no status filter and emits no status column |
| Service PHP config | **kept, and unmarked**, while the entry still lists `<service>:config/permissions.php` |

So **deprecating a permission does not retire it from Laravel.** The project's `docs/typescript-consumer.md` states that
deprecated and reserved permissions are never emitted; that is true of the client and false of both PHP artifacts.

To actually retire a permission from Laravel:

1. Set `status` to `deprecated` (no longer granted) or `reserved` (id held, never to be reused).
2. **Also remove `<service>:config/permissions.php` from that entry's `generated_targets`.** Step 1 alone leaves it in
   the config, indistinguishable from an active permission.
3. Regenerate, apply the service config, and deploy the service. The permission is live until that deploy lands.
4. The auth seed cannot be made to omit it at all. Deleting the entry is the only mechanism, and deleting a published
   entry is forbidden — see "Withdrawal" below. Report the auth seed row as a known, deliberate residue.

## Proving a retirement landed

Only the TypeScript consumer produces a proof. `AGGREGATE_CONSUMER_PERMISSION_EXTRA` (fatal) fires while the client
still declares a name that is no longer active, and disappears once the regenerated artifact is applied — so **the
absence of that code after re-apply is the proof.**

There is no equivalent for Go: a stale Go map holding a now-deprecated id yields an observation whose id still resolves
in the catalog under the same name, so no finding is emitted. For the auth seed and the PHP configs there is nothing at
all, because auth observations are skipped and the entry is still emitted. **A retirement that is not visible in the
TypeScript artifact is unverifiable by this tooling** — say so in the report and name the consumer deploy as the only
remaining evidence.

## Rename is two-phase, and the mechanism is `legacy_keys`

**Phase 1 — edit the entry.** New `permission_key`, **the same `bitmap_id`**, and the old name appended to
`legacy_keys`. Change nothing else.

**Phase 2 — generate, then apply.** Regenerate, apply each affected artifact, then re-run `import` and
`check-drift --strict`.

`legacy_keys` is what suppresses re-import of the old name. Without it, the next `import` reads the old name still
present in the applied auth seed and **re-appends it as a brand-new active entry at the same bitmap id**, producing a
fatal `DUPLICATE_BITMAP_ID`. Two shipped entries in the catalog are exactly this pattern; read them before your first
rename.

**The trap.** The suppression list is built from the entries that survive the merge. An entry whose `owner_repo` is
`auth` is replaced wholesale on `import` by a row rebuilt from the auth seed, and that rebuild empties `legacy_keys`.
So renaming an auth-owned permission loses the suppression on the **first** `import`, and the **second** `import`
resurrects the old name as a duplicate. For an auth-owned rename: complete phase 2 and apply the auth seed before any
second `import`, and after the first `import` confirm `legacy_keys` still holds the old name before running another.
The same replacement also silently reverts a `deprecated` auth-owned entry to `active`.

## Reserving an id

`reserved` records the intent that an id is held and never reused. Nothing enforces it; the unenforced-invariant rule in
`SKILL.md` is the whole protection.

## Withdrawal is unsupported

There is no delete command, no tombstone, and no `removed` status. Deleting a row from `catalog/permissions.json` while
the permission still exists in the applied auth seed makes the next `import` re-add it as active. The supported
withdrawal is: `deprecated` or `reserved`, plus target removal for Laravel, plus regenerate, apply, and deploy. When a
request asks to delete a permission, do that instead and report the auth seed residue and the deploy window explicitly.

No runtime alias resolution exists anywhere in the project: two names never resolve to one permission. `legacy_keys` is
for import suppression during a rename and nothing else.
