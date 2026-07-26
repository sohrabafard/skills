# Diagnostic drills — named tools, exact commands, pass thresholds

No rule in this skill says "profile if tooling exists" or "validate with load tests". The tools
are named here; if one is absent from the environment, installing it is part of the task.

## Load test — k6

```bash
k6 run --vus 50 --duration 3m --summary-trend-stats='p(95),p(99)' loadtest.js
```

Latency and error-rate targets belong to `alaa-services-contract
references/22-failure-load-and-deprecation-contract.md` and go in the script's `thresholds`
block. Three pass criteria are owned here, because they are about the worker rather than the
response:

1. **No latency drift with worker age.** p99 over the final third of the run is within 10% of
   p99 over the first third, at flat request rate. A larger rise is accumulation, not load.
2. **Flat RSS.** Per-worker RSS over the second half of the run has no upward slope.
3. **Even distribution.** Requests served per worker are within 10% of each other; a persistent
   outlier means one worker is stuck or recycling.

Run against `--workers=1` first to make criteria 1 and 2 unambiguous, then at the production
worker count to exercise contention.

## RSS sampling

```bash
# every 10s: pid, resident KiB, process age in seconds, for the worker processes
while :; do ps -eo pid=,rss=,etimes=,args= | grep -F 'octane' | grep -vF grep; sleep 10; done
```

Read it as bytes per request served, not bytes per second — pair it with the requests-served
signal in `references/worker-observability.md`. Time-based growth under variable load proves
nothing.

## CPU profile — php-spx

`php-spx` profiles a live worker; Xdebug's profiler is unsuitable here because it changes the
timing it measures and its per-request output does not survive worker reuse cleanly.

```bash
# in the php.ini used by octane:start
# extension=spx.so
# spx.http_enabled=1
# spx.http_key="<key>"
# spx.http_ip_whitelist="127.0.0.1"
curl -sS -H 'SPX_ENABLED: 1' -H 'SPX_KEY: <key>' 'localhost:8123/api/<route>' > /dev/null
```

Pass threshold: the top frame by exclusive time must be work the endpoint exists to do. Framework
boot appearing in a profile means the driver is not reusing the worker — check
`config('octane.server')` and that the request went to the Octane port. Whether profiling may be
enabled in a given environment is owned by `/alaa-observability-soc`
(`$alaa-observability-soc`), `references/60-sentry-and-profiling.md`.

## Query count per request

```php
// in a provider boot(), non-production only
DB::listen(fn () => $count++);
Event::listen(RequestTerminated::class, fn () => logger()->debug('queries', ['n' => $count]));
```

Pass threshold: the count does not grow when the response's collection size grows. That is the
N+1 test; the budget it is held to is owned by `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`).

## Bisect — finding *which* binding leaked

1. Reproduce with Shape A in `references/leak-detection-harness.md`. Without a failing test
   there is nothing to bisect against.
2. List what the container still holds after the flush, for request 1 and request 2:

```php
Event::listen(RequestTerminated::class, function (): void {
    $p = new ReflectionProperty(Illuminate\Container\Container::class, 'instances');
    $p->setAccessible(true);
    logger()->debug('held', ['keys' => array_keys($p->getValue(app()))]);
});
```

   Any key present after both requests that should be request-scoped is a candidate.
3. Move half the candidates into the `flush` array of `config/octane.php` and re-run the test.
   The half that turns it green contains the leak. Halve again until one abstract remains, then
   fix it with the right mechanism from `references/full-guide.md` — `flush` was the bisect
   instrument, not necessarily the fix.
4. For RSS growth with no candidate binding, bisect the history instead:

```bash
git bisect start <bad> <good>
git bisect run ./scripts/octane-rss-check.sh   # starts octane --workers=1, drives k6,
                                               # exits non-zero if the RSS slope is positive
```

Report the failing test from step 1, the abstract found in step 3, and the mechanism applied.
