# Octane leak-detection harness

## The false-green trap — read this first

The default Laravel test harness creates a fresh application for every test method. **A leak
between requests therefore cannot reproduce under `php artisan test`, `vendor/bin/pest`, or
`vendor/bin/phpunit` as normally written, and a green suite is not evidence about this bug
class at all.** A service can have a cross-tenant singleton leak in production and a fully
green suite on the same commit. Any claim that tests cover a retention change must name which
of the two shapes below was used.

## Shape A — in-process, one application, two request cycles

Use this for anything resolvable from the container: bindings, tenant holders, statics,
memoization, listeners. It is fast enough for CI and is the default.

The mechanic is `$this->refreshApplication()` between the two halves of the test: it simulates
the per-request scoped-binding flush, so a `scoped` binding yields a new instance afterwards
while a leaked `singleton` yields the same one.

```php
public function test_tenant_context_does_not_survive_the_request(): void
{
    // Test intent: proves Invariant 1 for TenantContext. This test passes only while the
    // binding is `scoped` or listed in the `flush` array of config/octane.php. Convert it
    // back to `singleton` and this test must fail — see "Proving the test is real" below.
    $this->actingAsTenant('tenant-a');
    $first = app(TenantContext::class);
    self::assertSame('tenant-a', $first->id());

    $this->refreshApplication();            // the per-request scoped flush

    $second = app(TenantContext::class);
    self::assertNotSame($first, $second, 'container returned one instance across two requests');
    self::assertNull($second->id(), "previous request's tenant survived the flush");
}
```

Assertion form, both halves required:

- **identity**: `assertNotSame($first, $second)` — proves the container really re-resolved.
- **value**: the second resolve carries nothing from the first — `assertNull(...)`, or the
  second tenant's own value, never the first tenant's.

Identity alone passes against a class that is re-created but reads from a leaked `static`.
Value alone passes against a class that is never re-created but happens to be re-populated.

## Shape B — two sequential requests against a booted server

Use this when the state is not container-resolvable: a `static` in framework or vendor code, an
RLS session variable on a connection, an SDK scope, a Swoole table.

```bash
php artisan octane:start --server=swoole --workers=1 --max-requests=10000 --port=8123 &
# --workers=1 is load-bearing: it forces both requests onto the same process, which is the
# only configuration in which the leak is deterministic rather than a coin flip.
curl -sS -H "$(tenant_a_trusted_headers)" localhost:8123/api/<route> > a.json
curl -sS -H "$(tenant_b_trusted_headers)" localhost:8123/api/<route> > b.json
# Assert: b.json contains no identifier, name, or count belonging to tenant A.
```

Trusted-header construction is owned by `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`); never hand-forge a tenant header that the gateway would reject.

## Proving the test is real

Per `/alaa-testing-strategy` (`$alaa-testing-strategy`), a test that passes both ways is not a
test. Before the change is reported as covered:

1. Remove the reset — change `scoped` back to `singleton`, or delete the abstract from `flush`,
   or comment out the `RequestTerminated` listener.
2. Run the test. **It must fail**, and the failure message must name the leaked value.
3. Restore the reset and confirm it passes.

Record step 2's failure output in the task report. A retention test whose failure has never
been observed is an assertion, not evidence.

## Ship rule

Every change to a `singleton` binding, a `scoped` binding, the `flush` array, a reset listener,
or a memoization site ships with one of the two shapes above, plus the step-2 failure output.
A change to any of those without such a test is incomplete regardless of suite colour.

Guard Swoole-only tests with `extension_loaded('swoole') || extension_loaded('openswoole')` and
skip when neither is present. When exercising `concurrently()`, tables or ticks without a real
server, assert correctness rather than parallelism: closures may run sequentially in tests.

Layer choice, doubles, proof strength and flake diagnosis are owned by
`/alaa-testing-strategy`; Pest syntax, datasets and runner flags come from upstream
`pest-testing/SKILL.md`, which is not owned by this repository. The two shapes above and their
mechanic are owned here.
