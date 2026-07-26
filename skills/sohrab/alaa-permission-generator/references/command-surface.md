# Command Surface, Exit Codes, and Order of Operations

Every command runs from the catalog root located in `SKILL.md` Step 0. The `composer` aliases are exact 1:1 wrappers;
`composer catalog:check-drift -- --strict` is the only way to pass `--strict` through Composer.

## Exit codes — the whole contract

| Code | Meaning |
| --- | --- |
| `0` | Success, **or** findings present without `--strict` |
| `1` | `--strict` was passed **and** a finding of severity `fatal` or `error` exists. Nothing else produces `1` |
| `2` | A thrown `RuntimeException`: missing source file, malformed JSON, unsupported `input_shape`, an emitter refusal, or an underivable Go package |

`warning` and `info` findings never change the exit code. What each code obliges you to do:

- `0` **is not proof of a clean catalog.** Read the printed status line and
  `generated/reports/permission-drift-report.json` before concluding anything. A `0` from a command without `--strict`
  is consistent with fatal findings.
- `1` — apply nothing. Fix the catalog, regenerate, and re-run. Diagnose via `references/failure-modes.md`.
- `2` — the run did not complete and no artifact is trustworthy. The message names the cause; fix the cause. Never
  re-run with different flags to make a `2` disappear.

## Two traps that make a gate validate nothing

1. **An unknown command prints usage and exits `0`.** A mistyped gate — `checkdrift --strict`, `check-drift -strict`,
   `check_drift` — passes CI while validating nothing. Any flag that is not exactly `--strict` or `--key=value` is
   silently discarded, so `--strict` written with a space or a single dash is dropped. Verify a new gate by making it
   fail on purpose once.
2. **`--strict` is a silent no-op on `import` and `summary`.** Both return `0` unconditionally. A gate built on
   `import --strict` or `summary --strict` validates nothing while looking correct.

**Only `check-drift --strict` is a gate.** `validate --strict` and `generate --strict` also honour `--strict`, but the
gate that compares the *applied* consumer artifact is `check-drift`. Gate CI on `check-drift --strict` and on
`php tests/run.php`.

## What each command reads and writes

No command is read-only. `validate`, `check-drift`, `generate`, and `summary` all rewrite the four report artifacts
(`generated/catalog/permissions.normalized.json`, `generated/reports/permission-drift-report.md`, the same report as
`.json`, and `generated/reports/permission-catalog-summary.md`). Never run one on a tree whose reports you were about to
diff.

| Command | Reads | Writes | Honours `--strict` |
| --- | --- | --- | --- |
| `import` | `catalog/services.json`, every owner's `source_path`, `catalog/permissions.json`, each aggregate consumer's applied artifact | **`catalog/permissions.json`**, the four reports, `generated/reports/import-plan.json` | no |
| `validate` | same | the four reports | yes |
| `generate` | same | everything under `generated/`, plus the four reports | yes |
| `check-drift` | same | the four reports | yes — this is the gate |
| `summary` | same | the four reports | no |

Options are `--services=`, `--catalog=`, `--generated=`, each a **repository-relative** path. See the confinement trap in
`references/failure-modes.md` before passing any of them.

`generate` writes its reports from findings computed **before** generation ran. A report read immediately after
`generate` describes the previous state. Run `check-drift` to get a report that describes what is now on disk.

## `import` writes to the source of truth

`import` is not a read-only discovery step: it rewrites `catalog/permissions.json`. Any entry whose `owner_repo` is
`auth` is **replaced wholesale** by a row rebuilt from the auth seed, and that rebuild hardcodes `status: active`, a
single generated target, and empty `aliases` and `legacy_keys`. So running `import` after hand-editing an auth-owned
entry silently reverts the edit — including a deprecation, a note, and the `legacy_keys` a rename depends on.

The project's own `RUN_BOOK.md` leads its standard loop with `import` for every change, so following the runbook
literally causes this loss. The discriminator:

- **Run `import`** to discover what source repositories currently declare — onboarding a service, or reconciling after
  someone else applied an artifact.
- **Skip `import`** when a hand edit to `catalog/permissions.json` is the authoritative change. Go straight to
  `generate`.

## Canonical loop

Run only the steps the change needs, in this order. Step 3 is conditional per the discriminator above.

```bash
php scripts/permission_catalog.php import          # conditional; writes catalog/permissions.json
php scripts/permission_catalog.php validate --strict
php scripts/permission_catalog.php generate
php scripts/permission_catalog.php check-drift --strict
php scripts/permission_catalog.php summary
php tests/run.php
```

Order matters in three specific ways:

- `generate` before editing the catalog emits the old ids into every artifact, and the tree under `generated/` is
  git-tracked, so stale output gets committed as if approved. Nothing in the project checks that a committed artifact is
  fresh; `php tests/run.php` passes with a stale one.
- `check-drift` run before applying reports `AGGREGATE_CONSUMER_MANUAL_EDIT` or `_ARTIFACT_NOT_APPLIED` until you apply,
  because it reads the consumer repository, not `generated/`. That is expected, not a false positive.
- After applying any artifact, re-run `import` then `check-drift --strict` then `php tests/run.php`, so the importer
  observes the applied file and aggregate drift verifies it.
