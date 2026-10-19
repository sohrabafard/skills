<?php

declare(strict_types=1);

use Illuminate\Container\Container;

require '/var/www/html/vendor/autoload.php';

// In-memory fixture only; no application bootstrap, database or HTTP identity handling.
final class TenantContext
{
    private ?string $tenantId = null;

    public function setId(string $id): void
    {
        $this->tenantId = $id;
    }

    public function id(): ?string
    {
        return $this->tenantId;
    }
}

function makeProbeContainer(string $binding): Container
{
    $container = new Container();
    $container->{$binding}(TenantContext::class, fn (): TenantContext => new TenantContext());

    return $container;
}

// Each process runs the exact documented method, with one explicit mutation at most.
$case = $argv[1] ?? '';
if (! in_array($case, ['scoped', 'singleton', 'no-reset', 'rebuild-singleton'], true)) {
    fwrite(STDERR, "Usage: php octane-probe.php scoped|singleton|no-reset|rebuild-singleton\n");
    exit(2);
}

require __DIR__.'/octane-snippet.php';
$probe = new HarnessSnippet();
$probe->app = makeProbeContainer(in_array($case, ['singleton', 'rebuild-singleton'], true) ? 'singleton' : 'scoped');

try {
    match ($case) {
        'no-reset' => $probe->withoutReset(),
        'rebuild-singleton' => $probe->withRebuiltContainer(),
        default => $probe->test_tenant_context_is_forgotten_with_its_scope(),
    };
    echo $case, ': ORACLE PASS', PHP_EOL;
    exit(0);
} catch (RuntimeException $failure) {
    fwrite(STDERR, $case.': ORACLE FAIL: '.$failure->getMessage().PHP_EOL);
    exit(1);
}
