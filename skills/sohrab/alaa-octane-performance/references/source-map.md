# Source map

Use this when Octane, Swoole, RoadRunner, FrankenPHP, long-lived workers, or hot-path behaviour
may be version-sensitive.

## Source order

1. **Repository truth**, before any document: `composer.json`, `config/octane.php` (driver,
   `flush` list, listeners, worker counts, `max_requests`), service providers and their
   bindings, middleware, the process-manager or container command, tests, and production logs.
2. **Official Laravel**: Octane <https://laravel.com/docs/octane>; container
   <https://laravel.com/docs/13.x/container>; deployment
   <https://laravel.com/docs/13.x/deployment>; queues <https://laravel.com/docs/13.x/queues>;
   upgrade guide <https://laravel.com/docs/13.x/upgrade>.
3. **Runtime**: OpenSwoole <https://openswoole.com/docs>; RoadRunner
   <https://docs.roadrunner.dev/>; FrankenPHP <https://frankenphp.dev/docs/> (worker mode,
   Laravel, Caddyfile, known issues); PHP manual <https://www.php.net/manual/>.
4. **Upstream skills in the service repository**, not owned here and re-pulled between runs:
   `.agents/skills/octane-development/SKILL.md` for `Octane::table()` and
   `Octane::concurrently()` syntax and driver configuration keys. On any retention rule, this
   skill wins — see the precedence rule in `SKILL.md`.
5. **Companion skills**: `/alaa-data-layer` for Redis and query behaviour,
   `/alaa-observability-soc` for signal requirements,
   `/alaa-reliability-sla` for failure doctrine.
6. **Community posts and StackOverflow**: troubleshooting leads only. Verify every lifecycle,
   flush, or reset claim against the sources above and against the repository's own behaviour
   before acting on it.

## Freshness triggers

Verify against official docs or observed local runtime behaviour when the task mentions: latest,
current, upgrade, security, CVE, Octane, Swoole, OpenSwoole, RoadRunner, FrankenPHP, memory
leak, worker leak, singleton, scoped binding, `flush`, request context, tenant context, warm
state, `max_requests`, `max_wait_time`, `max_request_execution_time`, task workers, coroutines,
or `octane:reload`.

## Leak-harness mechanics

Read before adapting Shape A or B in `references/leak-detection-harness.md`. Verified
2026-10-18 against Laravel **v13.34.0** and Octane **v2.20.0**; recheck the consuming
repository's lockfile and listener configuration on upgrades.

- [TestCase](https://github.com/laravel/framework/blob/v13.34.0/src/Illuminate/Foundation/Testing/TestCase.php):
  `refreshApplication()` assigns `createApplication()`; it replaces the application.
- [Container](https://github.com/laravel/framework/blob/v13.34.0/src/Illuminate/Container/Container.php):
  `scoped()` registers a shared binding and tracks it; `forgetScopedInstances()` removes
  tracked instances while leaving ordinary singletons intact.
- [FlushTemporaryContainerInstances](https://github.com/laravel/octane/blob/v2.20.0/src/Listeners/FlushTemporaryContainerInstances.php)
  invokes scoped cleanup and removes configured `octane.flush` instances.
- [Worker](https://github.com/laravel/octane/blob/v2.20.0/src/Worker.php) clones the booted
  application for each request and later flushes the sandbox. A same-container test does
  not reproduce this lifecycle or prove listener registration.
