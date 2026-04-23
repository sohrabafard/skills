# Source Map

Use this map when Octane, Swoole, RoadRunner, long-lived workers, or hot-path behavior may be version-sensitive.

## Source order

1. Repository truth:
   - `composer.json`, `config/octane.php`, service providers, singleton bindings, middleware, runtime files, tests, logs, and production process manager config.
2. Official Laravel sources:
   - Octane: https://laravel.com/docs/octane
   - Laravel 13 upgrade guide: https://laravel.com/docs/13.x/upgrade
   - Service container: https://laravel.com/docs/13.x/container
   - Deployment: https://laravel.com/docs/13.x/deployment
   - Queues: https://laravel.com/docs/13.x/queues
3. Runtime sources:
   - Swoole docs: https://openswoole.com/docs
   - RoadRunner docs: https://docs.roadrunner.dev/
   - PHP manual: https://www.php.net/manual/
4. Companion skills:
   - `alaa-data-layer` for DB, Redis, pooling, and hot-query behavior.
   - `alaa-observability-soc` for metrics, traces, logs, alerts, and incident evidence.
5. Community posts and StackOverflow answers:
   - Troubleshooting only. Verify lifecycle and reset claims against Laravel Octane docs, runtime docs, and repo behavior.

## Freshness triggers

Verify official docs or local runtime behavior when the task mentions:

- `latest`, `current`, `upgrade`, `security`, `CVE`, Octane, Swoole, RoadRunner, memory leak, worker leak, singleton, request context, tenant context, warm state, max requests, task workers, or coroutine behavior.

## Small example

Resolve current request data at request time, not in a singleton constructor:

```php
$this->app->singleton(CurrentTenantResolver::class, fn () => new CurrentTenantResolver(
    fn () => request()->header('X-Project-Id'),
));
```

Anti-pattern:

```php
$this->app->singleton(CurrentTenantResolver::class, fn () => new CurrentTenantResolver(
    request()->header('X-Project-Id'),
));
```

The anti-pattern captures one request's state and can leak it into later requests under a long-lived worker.
