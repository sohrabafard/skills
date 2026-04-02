# Laravel Copy Baselines

Use these baselines when a Laravel repository needs copy-oriented implementation help.

Rules:
- Adapt namespaces and injected helpers to the target repository.
- Preserve the owned behavior and field names.
- Do not change headers, event names, code names, or envelope shapes while copying.

## RequestObservabilityMiddleware baseline

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use App\Support\Observability\MetricsEmitter;
use App\Support\Observability\ProbeNoiseDecider;
use App\Support\Observability\RequestContext;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Symfony\Component\HttpFoundation\Response;

final class RequestObservabilityMiddleware
{
    public function __construct(
        private readonly RequestContext $requestContext,
        private readonly ProbeNoiseDecider $probeNoiseDecider,
        private readonly MetricsEmitter $metricsEmitter,
    ) {
    }

    public function handle(Request $request, Closure $next): Response
    {
        $context = $this->requestContext->start($request);

        Log::shareContext($context->toLogContext());

        try {
            /** @var Response $response */
            $response = $next($request);
        } catch (\Throwable $throwable) {
            $this->requestContext->shareExceptionContext($request, $context, $throwable);
            $this->requestContext->logRequestFailure($request, $context, $throwable);

            throw $throwable;
        }

        $this->requestContext->attachHeaders($response, $context);
        $this->requestContext->recordMetrics($request, $response, $context, $this->metricsEmitter);

        if (! $this->probeNoiseDecider->shouldSuppressCompletedLog($request, $response)) {
            $this->requestContext->logRequestCompleted($request, $response, $context);
        }

        return $response;
    }
}
```

Required helper responsibilities behind this baseline:
- normalize or generate `X-Request-Id`
- normalize or generate `traceparent`
- expose `trace_id`
- capture request duration
- resolve route name or templated route
- attach `X-Request-Id` and `traceparent`
- persist request correlation context so the exception handler can attach the same headers to rendered API error responses
- emit `http.request.completed` and `http.request.failed`
- enforce bounded metric labels

## Exception-handler reminder

Do not assume the middleware can attach headers after a rethrow.

When the request pipeline throws and Laravel renders the API error later, the exception handler must read the shared request context and attach the same `X-Request-Id` and `traceparent` headers before returning the response.

## ResolveUserMiddleware baseline

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use App\Support\Auth\AuthStateSynchronizer;
use App\Support\Auth\TrustedActorContext;
use App\Support\Auth\TrustedRequestContext;
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

final class ResolveUserMiddleware
{
    public function __construct(
        private readonly TrustedRequestContext $trustedRequestContext,
        private readonly AuthStateSynchronizer $authStateSynchronizer,
    ) {
    }

    public function handle(Request $request, Closure $next): Response
    {
        $actor = $this->trustedRequestContext->fromHeaders($request);

        $request->attributes->set(TrustedActorContext::class, $actor);
        $this->authStateSynchronizer->synchronize($request, $actor);

        return $next($request);
    }
}
```

Required helper responsibilities behind this baseline:
- validate trusted headers exactly according to `$alaa-trust-gateway-auth`
- decode and map the permission bitmap
- normalize `X-Profile`
- normalize `shahr`
- expose one trusted actor object
- synchronize `$request->user()` and `Auth::user()`
- support legacy guard synchronization when the repository still needs it

## Trusted actor DTO baseline

```php
<?php

declare(strict_types=1);

namespace App\Support\Auth;

final readonly class TrustedActorContext
{
    /**
     * @param list<string> $permissions
     * @param array<string, mixed>|null $profile
     */
    public function __construct(
        public string $projectId,
        public int $userId,
        public array $permissions,
        public ?string $mobile,
        public ?array $profile,
        public ?string $role,
        public string $requestId,
        public string $traceId,
    ) {
    }
}
```

## Route and response reminder

When copying middleware baselines into a Laravel repository, also enforce:
- `GET /api/health`
- `GET /api/ready`
- `php artisan ops:ready --json`
- top-level `data` envelope for successful `/api/*` responses
- `X-Request-Id` and `traceparent` response headers
