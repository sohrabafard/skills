# Source Map

Use this map when Laravel architecture, public contracts, or framework-owned behavior may be version-sensitive.

## Source order

1. Repository truth:
   - routes, controllers, Form Requests, Resources, DTOs, services, policies, tests, docs, Postman/API artifacts, and repo-local `AGENTS.md`.
   - Existing public response samples and frontend consumers when contract shape matters.
2. Official Laravel sources:
   - Laravel 13 upgrade guide: https://laravel.com/docs/13.x/upgrade
   - Routing: https://laravel.com/docs/13.x/routing
   - Controllers: https://laravel.com/docs/13.x/controllers
   - Validation and Form Requests: https://laravel.com/docs/13.x/validation
   - Eloquent API Resources: https://laravel.com/docs/13.x/eloquent-resources
   - Authorization: https://laravel.com/docs/13.x/authorization
   - Events: https://laravel.com/docs/13.x/events
   - Queues: https://laravel.com/docs/13.x/queues
   - Service container: https://laravel.com/docs/13.x/container
   - Laravel API docs: https://api.laravel.com/docs/13.x/
3. Companion skill references:
   - `alaa-php-clean-code` for class shape and naming.
   - `alaa-data-layer` for persistence and transaction choices.
   - `alaa-async-messaging` for event/outbox delivery semantics.
   - `alaa-security-review` for auth, tenant, and trust boundaries.
4. Community posts and examples:
   - Use only for troubleshooting or vocabulary discovery.
   - Confirm all contract, resource, middleware, and lifecycle claims against repo code or official Laravel docs.

## Freshness triggers

Re-check official docs and repo code when the task mentions:

- `latest`, `current`, `upgrade`, `Laravel 13`, `deprecated`, `removed`, or `security`.
- Middleware, bootstrap, route precedence, resources, API envelopes, model serialization, queue events, events/listeners, policies, or container behavior.
- Public request or response fields that frontend or external services consume.

## Small example

For public contract work, keep the model internal and serialize through a Resource:

```php
return new ProfileResource($profile);
```

Anti-pattern:

```php
return response()->json($profile);
```

Raw model serialization can leak persistence fields or relationship state that was never part of the public API contract.
