# Validation And Release Gates

## Package validation

Use the package's current commands when available:

```bash
composer validate --strict
php scripts/controlled_ops_verify.php
vendor/bin/phpunit
composer audit --locked
git diff --check
```

`scripts/controlled_ops_verify.php` is the package-specific boundary check. Treat its findings as first-class evidence.

## Consuming-service validation

For adopter-service work, validate both the service and the package integration surface:

```bash
composer validate --strict
php artisan package:discover --ansi
php artisan route:list --path=api --except-vendor
php artisan ops:public-api-audit --json --no-log-scan
php artisan test --compact <focused-controlled-ops-tests>
git diff --check
```

Use the repo's actual commands when they differ.

## Proof vocabulary

Name proof strength precisely:

- static inspection
- SQLite or unit proof
- package fake-sink parity proof
- host-to-Docker smoke
- in-runtime service proof
- PostgreSQL or RabbitMQ live proof

Do not present a weaker proof as a production-equivalent validation.

## Artifact sync

When service public behavior changes, sync docs and API artifacts through `$alaa-docs-farsi` and `$alaa-postman-collections`. If the package changes only internal PHP contracts, update package docs instead of creating service-facing API claims.
