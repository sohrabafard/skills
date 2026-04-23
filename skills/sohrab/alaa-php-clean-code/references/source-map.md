# Source Map

Use this map when PHP, Laravel, tooling, or security behavior may have changed since this skill was last edited.

## Source order

1. Repository truth:
   - `composer.json`, `composer.lock`, `phpunit.xml`, `pint.json`, `phpstan*`, `rector*`, CI files, and repo-local `AGENTS.md`.
   - Installed vendor code and generated framework files when present.
2. Official PHP sources:
   - PHP manual: https://www.php.net/manual/
   - PHP 8.5 migration guide: https://www.php.net/manual/en/migration85.php
   - PHP supported versions: https://www.php.net/supported-versions.php
   - PHP security advisories: https://www.php.net/security/
3. Official Laravel sources:
   - Laravel 13 upgrade guide: https://laravel.com/docs/13.x/upgrade
   - Laravel 13 documentation: https://laravel.com/docs/13.x
   - Laravel API docs: https://api.laravel.com/docs/13.x/
   - Laravel Pint: https://laravel.com/docs/13.x/pint
4. Standards and first-party tools:
   - PHP-FIG PSR index: https://www.php-fig.org/psr/
   - PHP-FIG PER index: https://www.php-fig.org/per/
   - PHPUnit docs: https://docs.phpunit.de/
   - Pest docs: https://pestphp.com/docs
   - PHPStan docs: https://phpstan.org/user-guide/getting-started
5. Community posts, StackOverflow answers, blog posts, and AI summaries:
   - Use only for troubleshooting symptoms or finding keywords to verify against sources above.
   - Do not use them as authority for current PHP, Laravel, security, or release behavior.

## Freshness triggers

Verify official or repo-local sources before acting when the task mentions:

- `latest`, `current`, `new in`, `deprecated`, `removed`, `security`, `CVE`, `upgrade`, or `migration`.
- PHP, Laravel, PHPUnit, Pest, Pint, PHPStan, Rector, Composer, or Symfony version changes.
- Framework-owned behavior such as middleware names, cache serialization, queue events, container injection, route matching, resources, or test lifecycle.
- Named-argument compatibility against Laravel framework methods.

## Small examples

Prefer Laravel 13 docs over old snippets when touching CSRF middleware:

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;

$this->withoutMiddleware([PreventRequestForgery::class]);
```

Anti-pattern:

```php
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

$this->withoutMiddleware([VerifyCsrfToken::class]);
```

The second form relies on old names and should only remain when the target repo is not on Laravel 13 or the local codebase intentionally preserves the old alias.
