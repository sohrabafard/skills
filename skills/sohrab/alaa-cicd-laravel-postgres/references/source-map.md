# Source Map

Use this map when CI behavior, release gates, dependency versions, Postgres services, or current tool behavior may have changed.

## Source order

1. Repository truth:
   - CI files, Dockerfiles, lockfiles, Composer scripts, test bootstrap, `.env.example`, migration commands, runtime wrappers, and repo-local `AGENTS.md`.
2. Official Laravel and PHP sources:
   - Laravel 13 upgrade guide: https://laravel.com/docs/13.x/upgrade
   - Laravel testing: https://laravel.com/docs/13.x/testing
   - Laravel deployment: https://laravel.com/docs/13.x/deployment
   - PHP manual: https://www.php.net/manual/
   - PHP supported versions: https://www.php.net/supported-versions.php
3. CI provider and tool sources:
   - GitHub Actions PostgreSQL service containers: https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers
   - GitLab CI services: https://docs.gitlab.com/ci/services/
   - GitLab CI PostgreSQL service: https://docs.gitlab.com/ci/services/postgres/
   - Composer docs: https://getcomposer.org/doc/
   - PHPUnit docs: https://docs.phpunit.de/
   - Pest docs: https://pestphp.com/docs
4. Database and container sources:
   - PostgreSQL current docs: https://www.postgresql.org/docs/current/
   - Official Postgres Docker image: https://hub.docker.com/_/postgres
   - Docker Build CI docs: https://docs.docker.com/build/ci/
5. Community posts and StackOverflow answers:
   - Troubleshooting only. Verify command semantics, cache behavior, and service container behavior against official docs and a local/CI run.

## Freshness triggers

Verify official docs or live CI behavior when the task mentions:

- `latest`, `current`, `upgrade`, `security`, `CVE`, new PHP/Laravel/Postgres/Composer/PHPUnit/Pest versions, image tags, CI runner changes, cache misses, flaky tests, service health checks, or release gating changes.

## Small example

Pin the Postgres service major/minor to match production expectations:

```yaml
services:
  postgres:
    image: postgres:16.10
```

Anti-pattern:

```yaml
services:
  postgres:
    image: postgres:latest
```

Floating database tags make pipeline behavior change without a code review.
