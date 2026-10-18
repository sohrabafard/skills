<?php

declare(strict_types=1);

// Generated from the skill's exact PHP method; assertion adapter replaces PHPUnit only.
final class HarnessSnippet
{
    public Illuminate\Container\Container $app;

    public static function assertSame(mixed $expected, mixed $actual): void
    {
        if ($expected !== $actual) {
            throw new RuntimeException('Expected seeded tenant-a state.');
        }
    }

    public static function assertNull(mixed $actual, string $message): void
    {
        if ($actual !== null) {
            throw new RuntimeException($message.': '.var_export($actual, true));
        }
    }

    public static function assertNotSame(mixed $first, mixed $second, string $message): void
    {
        if ($first === $second) {
            throw new RuntimeException($message);
        }
    }

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

    public function withoutReset(): void
    {
        // Defends against replacing the production scoped binding with singleton.
        $first = $this->app->make(TenantContext::class);
        $first->setId('tenant-a');
        self::assertSame('tenant-a', $first->id());

        // Mutation: omit scope reset.

        $second = $this->app->make(TenantContext::class);
        self::assertNull($second->id(), "previous request's tenant survived the flush");
        self::assertNotSame($first, $second, 'container retained the scoped instance');
    }

    public function withRebuiltContainer(): void
    {
        // Defends against replacing the production scoped binding with singleton.
        $first = $this->app->make(TenantContext::class);
        $first->setId('tenant-a');
        self::assertSame('tenant-a', $first->id());

        $this->app = makeProbeContainer('singleton');

        $second = $this->app->make(TenantContext::class);
        self::assertNull($second->id(), "previous request's tenant survived the flush");
        self::assertNotSame($first, $second, 'container retained the scoped instance');
    }
}
