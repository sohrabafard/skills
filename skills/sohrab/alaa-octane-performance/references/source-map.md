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
5. **Companion skills**: `/alaa-data-layer` (`$alaa-data-layer`) for Redis and query behaviour,
   `/alaa-observability-soc` (`$alaa-observability-soc`) for signal requirements,
   `/alaa-reliability-sla` (`$alaa-reliability-sla`) for failure doctrine.
6. **Community posts and StackOverflow**: troubleshooting leads only. Verify every lifecycle,
   flush, or reset claim against the sources above and against the repository's own behaviour
   before acting on it.

## Freshness triggers

Verify against official docs or observed local runtime behaviour when the task mentions: latest,
current, upgrade, security, CVE, Octane, Swoole, OpenSwoole, RoadRunner, FrankenPHP, memory
leak, worker leak, singleton, scoped binding, `flush`, request context, tenant context, warm
state, `max_requests`, `max_wait_time`, `max_request_execution_time`, task workers, coroutines,
or `octane:reload`.
