# Laravel Copy Baselines

Use these baselines when a Laravel repository needs copy-oriented implementation help.

Rules:
- Adapt namespaces and injected helpers to the target repository.
- Preserve the owned behavior and field names.
- Do not change headers, event names, code names, envelope shapes, or metric names while copying.

## Public project selector baseline

Use this baseline whenever a Laravel service accepts public `project_id` input. Keep the names aligned unless the target repository already has an equivalent helper with the same semantics.

### `MappedProjectUuidV7` validation rule

```php
<?php

declare(strict_types=1);

namespace App\Rules;

use App\Support\Auth\TrustedProjectContext;
use Closure;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Translation\PotentiallyTranslatedString;

final class MappedProjectUuidV7 implements ValidationRule
{
    private const string CANONICAL_UUIDV7_PATTERN = '/^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/';

    /**
     * @param Closure(string, ?string=): PotentiallyTranslatedString $fail
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! is_string($value) || preg_match(self::CANONICAL_UUIDV7_PATTERN, $value) !== 1) {
            $fail('The :attribute must be a canonical UUIDv7 project id.');

            return;
        }

        if (TrustedProjectContext::resolveInternalProjectId($value) === null) {
            $fail('The selected :attribute is invalid.');
        }
    }
}
```

### Public FormRequest usage

```php
use App\Rules\MappedProjectUuidV7;
use App\Support\Auth\TrustedProjectContext;

public function rules(): array
{
    return [
        'project_id' => ['bail', 'required', 'string', new MappedProjectUuidV7],
    ];
}

protected function passedValidation(): void
{
    $projectId = TrustedProjectContext::resolveInternalProjectId(
        (string) $this->validated('project_id')
    );

    if ($projectId !== null) {
        $this->attributes->set('project_id', $projectId);
        $this->attributes->set('project_public_id', TrustedProjectContext::resolvePublicProjectId($projectId));
    }
}
```

### Controller or action usage

```php
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

private function resolveProjectId(Request $request): int
{
    $projectId = $request->attributes->get('project_id');

    if ((is_int($projectId) || is_string($projectId)) && (int) $projectId > 0) {
        return (int) $projectId;
    }

    throw ValidationException::withMessages([
        'project_id' => ['The selected project id is invalid.'],
    ]);
}
```

Usage rules:
- public FormRequests use `MappedProjectUuidV7`
- trusted-header middleware may use a separate trusted normalizer when compatibility requires it
- never convert public `project_id` to an integer in `prepareForValidation()`
- put the resolved internal id in request attributes or a typed DTO, not back into public input
- add tests that reject integer `1`, string `"1"`, malformed UUIDs, and unmapped UUIDv7 values
- keep Postman examples on a public UUIDv7 variable such as `authProjectId`, separate from trusted-header variables such as `gatewayProjectId`

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

The request middleware metrics emitter uses the exact `alaa_*` family names in `24-metric-registry.md`; a local family name is contract drift.

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
- authorize with exact catalog-owned permissions; do not derive access from user roles
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
        public string $requestId,
        public string $traceId,
    ) {
    }
}
```

Do not add a role or role-derived tier to this baseline while the provisional freeze in
`28-backend-permission-authorization-and-role-freeze.md` is active. If an existing service has a documented
observability or future-migration requirement, keep normalized `userRoles` in a separate optional passive-
metadata extension that no policy, Gate, query scope, response shaper, route, validator, feature, or workflow reads.

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
- the metric families registered in `24-metric-registry.md` when the service owns an HTTP metrics boundary
