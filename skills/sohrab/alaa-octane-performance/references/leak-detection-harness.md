# Octane leak-detection harness

## The false-green trap — read this first

Laravel normally refreshes the application between test methods. Independent request tests
therefore prove no cross-request isolation in a persistent worker. The runner (`artisan test`,
Pest or PHPUnit) is not the limitation: a test must deliberately retain the relevant state.
Name which shape below supports each retention claim.

## Shape A — same-container scoped-binding test

Use this fast test for a `scoped` registration's lifetime. Keep the same application and call
`forgetScopedInstances()` between resolutions. **Never use `refreshApplication()` here:** it
recreates the application and its singletons too, allowing an incorrect singleton to pass.
Pinned framework and Octane evidence: `references/source-map.md`, "Leak-harness mechanics".

Use the production registration without rebinding it in the test. Adapt the illustrative
`TenantContext` and its setter/getter to the repository's trusted-context fixture; the setter
below seeds test state, not an HTTP identity input.

```php
public function test_tenant_context_is_forgotten_with_its_scope(): void
{
    // Defends against replacing the production scoped binding with singleton.
    $first = $this->app->make(TenantContext::class);
    $first->setId('tenant-a');
    self::assertSame('tenant-a', $first->id());

    $this->app->forgetScopedInstances();

    $second = $this->app->make(TenantContext::class);
    self::assertNull($second->id(), "previous request's tenant survived the flush");
    self::assertNotSame($first, $second, 'container retained the scoped instance');
}
```

Assert both the state and identity: static state can survive a new object; an old object can
look empty before repopulation. This tests binding lifetime, **not Octane event wiring**.
A configured `octane.flush` entry or custom reset listener is not exercised by this call.
For those, captured holders, statics or memoization, use Shape B.

## Shape B — two sequential requests against one booted worker

Use this for actual worker lifecycle and reset wiring, including `flush` configuration,
listeners, captured instances, static/vendor state, RLS connection state, SDK scopes and
Swoole tables. Use the repository's configured driver and isolated test environment.

```bash
# Swoole example; use the selected driver's equivalent in the target repository.
php artisan octane:start --server=swoole --workers=1 --max-requests=10000 --port=8123 &
curl -sS -H "$(tenant_a_trusted_headers)" localhost:8123/api/<route> > a.json
curl -sS -H "$(tenant_b_trusted_headers)" localhost:8123/api/<route> > b.json
# Assert A exercised the tenant-specific state; B succeeds with B's expected data
# and contains no identifier, name, or count belonging to A.
```

Verify readiness before sending requests and verify both reached the same surviving worker;
a restart between them invalidates the proof. Clean up the test worker afterwards. One worker
prevents load balancing from hiding retention; it does not prevent a recycle or crash.

Trusted-header construction is owned by `/alaa-trust-gateway-auth`; never hand-forge a tenant
header that the gateway would reject.

## Proving the test is real

Per `/alaa-testing-strategy`, a test that passes both ways is not a
test. Before the change is reported as covered:

1. Remove the relevant reset: mutate the production `scoped` registration to `singleton`
   for Shape A, or remove the `flush` entry/reset listener exercised by Shape B. Also verify
   Shape A fails when its `forgetScopedInstances()` call is omitted. Do not combine mutations.
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
