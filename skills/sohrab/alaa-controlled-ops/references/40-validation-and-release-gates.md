# Validation And Release Gates

## Package gates

Run all five in the package repository:

```bash
composer validate --strict
php scripts/controlled_ops_verify.php
vendor/bin/phpunit
composer audit --locked
git diff --check
```

Where the repository ships its own equivalent — a wrapper script, a different PHPUnit path — run that and name which you ran. Where a gate has no equivalent, report it as a missing gate rather than substituting a weaker check.

Two gates have a precondition, so each has a false branch:

- `vendor/bin/phpunit` needs installed dependencies. If `vendor/` is absent, run `composer install`; if that fails, stop and report `tests not run: composer install failed` with the failure output. Never report the release gates clean while the test gate is unrun.
- `composer audit --locked` needs the advisory endpoint. If unreachable, retry once, then report `supply-chain audit not run: advisory endpoint unreachable` as a named gap and ask the user whether to release anyway. It is the only supply-chain control in the release path, so an unrun audit is the user's decision, not a detail to omit.

`scripts/controlled_ops_verify.php` is the package-specific boundary check. A finding it reports blocks the release: do not tag, do not push, and do not ask for publish approval until the finding is fixed or the user has been shown the exact finding and has said to proceed anyway.

## Adopter gates

In the consuming service, run the ControlledOps-specific pair:

```bash
php artisan test --compact <focused-controlled-ops-tests>
php vendor/alaa/controlled-ops/scripts/controlled_ops_verify.php
```

Generic service validation — Composer metadata, package discovery, the `route:list` inventory, and the public-API audit — belongs to `/alaa-services-contract` ($alaa-services-contract). Run its gates for those and keep no second list here.

## Proof vocabulary

Name proof strength precisely:

- static inspection
- SQLite or unit proof
- package fake-sink parity proof
- host-to-Docker smoke
- in-runtime service proof
- PostgreSQL or RabbitMQ live proof

Do not present a weaker proof as a production-equivalent validation.

The last three need a running local runtime, owned by `/service-runtime-kit-governance` ($service-runtime-kit-governance): obtain them through its render, bootstrap, and validate path. If the runtime cannot come up, report the highest strength actually reached and name the blocker; never relabel a unit proof as an in-runtime proof.

## Artifact sync

When service public behavior changes, sync docs and API artifacts through `/alaa-docs-farsi` ($alaa-docs-farsi) and `/alaa-postman-collections` ($alaa-postman-collections). If the package changes only internal PHP contracts, update package docs instead of creating service-facing API claims.
