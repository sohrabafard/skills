# Breaking-Change Detection

The baseline that makes "pre-existing" checkable, the classification that splits a major bump out of a patch sweep, and the checks a test suite does not perform. Test design -- what makes a test a test, which layer a behaviour belongs at, flake versus intermittent defect -- is `/alaa-testing-strategy` (`$alaa-testing-strategy`).

## Step 1 -- capture the baseline

Before any mutating command, at the pre-sweep commit:

```bash
SCRATCH="$MANIFEST_ROOT/.upgrade-scratch"     # created in 10-rollback-and-blast-radius.md
composer install --no-interaction             # vendor/ now matches the pre-sweep lock
<the repo's test command> > "$SCRATCH/baseline.txt" 2>&1; echo "exit=$?" >> "$SCRATCH/baseline.txt"
```

Record in the state file: the exact command including any `--random-order-seed` value, the pre-sweep commit, the exit code, and every failing test identifier with the first line of its assertion message. An order-randomising runner produces a different failure set per seed, so a baseline captured under one seed and compared against another proves nothing.

If the baseline cannot run at all, report `baseline not captured: <reason>` and stop. Every later "pre-existing" claim depends on this file existing.

## The identity rule

A post-sweep failure is pre-existing only when **the same test identifier** fails with **the same first line of assertion message** in both `baseline.txt` and the post-sweep run. Same identifier with a different message is a new failure wearing an old name. A failure absent from the baseline belongs to this sweep and blocks it. Reporting one as pre-existing means quoting the baseline path and the matching line.

## Falsifying the claim when no baseline exists

```bash
git stash push -- composer.json composer.lock
composer install --no-interaction     # REQUIRED: vendor/ must match the stashed lock
<the repo's test command>             # same command and seed as the post-sweep run
git stash pop
composer install --no-interaction     # REQUIRED: return vendor/ to the new lock
```

Both installs are mandatory: stashing the lock without reinstalling tests the new `vendor/` against the old lock and reproduces neither state. Reproducing under the stash makes the failure pre-existing; not reproducing makes it this sweep's.

## Step 2 -- classify every moved package

From the `--dry-run` output, classify each package by the leftmost version component that changed.

| Resolved change | Class | Handling |
|---|---|---|
| Patch only, `1.4.2` -> `1.4.7` | patch | batched here |
| Minor, `1.4.2` -> `1.7.0` | minor | batched here |
| Major, `1.4.2` -> `2.0.0` | major | leaves this sweep |
| Any component of a `0.x`, `0.4.2` -> `0.5.0` | major | leaves this sweep |
| A package entering or leaving the lock | transitive move | batched, named in the report |

`0.x` counts as major because the leftmost non-zero component carries the breaking change under semver.

**A major bump is a separate change**: its own branch, its own restore point, one package at a time with `composer update <vendor/package> --with-dependencies`, the package's upgrade guide read first, and the higher proof level below. The reason is the revert unit -- thirty patch bumps sharing a commit range with one major means reverting the major reverts the thirty.

## Proof level per class

Name the level from `/alaa-controlled-ops` (`$alaa-controlled-ops`) `references/40-validation-and-release-gates.md`, "Proof vocabulary". Minimums:

| Class | Minimum proof |
|---|---|
| Patch or minor, `require-dev` only, absent from every container build stage | SQLite or unit proof |
| Patch or minor touching the request path, a driver, or a queue consumer | host-to-Docker smoke |
| Major, or any bump to the framework or a database, Redis or AMQP client | in-runtime service proof, plus PostgreSQL or RabbitMQ live proof when the bumped client speaks to that dependency |

A runtime that will not come up means reporting the highest strength actually reached and the blocker, never relabelling a unit proof. The runtime comes from `/service-runtime-kit-governance` (`$service-runtime-kit-governance`).

## Step 3 -- does the frontend build ship?

Three checks; one hit settles it.

1. The build output (`public/build`, `public/dist`, or `outDir` in `vite.config.*`) is tracked in git, served by a route, or exposed through a `Storage` disk.
2. A Blade or Inertia entrypoint references it: `grep -rn '@vite\|vite(\|manifest.json' resources/views app/`.
3. A container build stage runs it: `grep -rn 'npm run build\|vite build\|yarn build' Dockerfile* docker/`.

One hit makes the frontend production surface: its gates equal the Composer side's, and the repo's own build command must succeed after the npm upgrade, because `npm audit` passing does not prove the build still works. Zero hits makes it dev-only tooling, closed by `npm audit` alone. Build and delivery are `/alaa-frontend-devops` (`$alaa-frontend-devops`).

## Step 4 -- what the test suite does not check

- **Deprecations.** Run once with `--fail-on-deprecation` (PHPUnit 10 and later; Pest passes it through). A runner rejecting the flag is reported as `deprecation gate not available: <runner> <version>`, not skipped.
- **Config drift.** Diff the service's copy against the package's shipped copy -- `diff config/<name>.php vendor/<vendor>/<package>/config/<name>.php` -- rather than republishing over `config/`, which overwrites local values. Config contract: `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) `references/70-config-contract.md`.
- **Shipped migrations.** `php artisan migrate --pretend` shows migrations the upgrade brought in. Schema safety: `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md`.
- **Interface shape.** A bump changing a class, interface or contract the service extends or implements is a design change: `/alaa-system-design` (`$alaa-system-design`) requires its pass first.
- **Silent behaviour classes.** These move with no signature change and pass a happy-path suite: serialisation and JSON encoding flags, date parsing strictness, default timezone and locale, HTTP client default redirect and TLS-verification behaviour, decimal and float formatting, collection ordering, default charset or collation. For each one the bumped package touches, name the assertion that fails if it changed, and write it when it does not exist.
- **Runtime behaviour under a long-lived worker.** `50-runtime-verification.md`.
