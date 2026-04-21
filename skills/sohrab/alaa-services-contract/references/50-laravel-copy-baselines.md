# Laravel Copy Baselines

Use these baselines when a Laravel repository needs copy-oriented implementation help.

Rules:
- Adapt namespaces and injected helpers to the target repository.
- Preserve the owned behavior and field names.
- Do not change headers, event names, code names, envelope shapes, or metric names while copying.

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

## MetricsEmitter baseline expectations

The request middleware metrics emitter should align to the shared metric contract.

Minimum request-middleware metrics:
- `alaa_http_requests_total`
- `alaa_http_request_duration_seconds`
- `alaa_http_requests_in_flight`
- `alaa_http_request_failures_total`

Rules:
- use route templates or stable route names, not raw paths
- do not label by `user_id`, `project_id`, request IDs, raw URLs, or exception text
- use histograms for request duration
- if the stack supports exemplars, attach trace identifiers as exemplar data rather than normal labels

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
- normalize compact trusted first and last names
- normalize compact trusted location ids into one repository-owned structure when needed
- normalize `X-Access-Token-Id` when the repository uses token-session context
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
     * @param array{
     *     ostan?: int,
     *     shahrestan?: int,
     *     bakhsh?: int,
     *     shahr?: int,
     *     shobe?: int,
     *     school?: int
     * }|null $location
     */
    public function __construct(
        public string $projectId,
        public int $userId,
        public array $permissions,
        public ?string $mobile,
        public ?string $firstName,
        public ?string $lastName,
        public ?array $location,
        public ?string $tokenId,
        public ?string $role,
        public string $requestId,
        public string $traceId,
    ) {
    }
}
```

## Snapshot baseline

- if a repo stores request-time user context, keep mutable projections separate from immutable snapshots
- prefer a repository-owned projection that preserves compact ids instead of inventing display names
- keep missing location ids explicit instead of fabricating location names

## Route and response reminder

When copying middleware baselines into a Laravel repository, also enforce:
- `GET /api/health`
- `GET /api/ready`
- `php artisan ops:ready --json`
- top-level `data` envelope for successful `/api/*` responses
- `X-Request-Id` and `traceparent` response headers
- the metric families defined by `21-alaa-platform-observability-directive.md` when the service owns an HTTP metrics boundary
