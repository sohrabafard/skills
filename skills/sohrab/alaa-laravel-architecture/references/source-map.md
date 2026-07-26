# Source map — what to trust when framework-owned behaviour may have changed

Read this file when the task says `latest`, `current`, `upgrade`, `Laravel 13`, `deprecated`, `removed`, or `security`, or when the change touches middleware, bootstrap, route precedence, resource serialization, model serialization, queue events, events and listeners, policies, or container behaviour — and when a public request or response field a frontend or another service consumes is in scope.

## Order of authority

1. **The repository.** Routes, Controllers, FormRequests, Resources, DTOs, Services, Policies, providers, tests, the API collection, saved response examples, and the repo-local `AGENTS.md`. A live consumer's expectation beats a documented intention.
2. **Official Laravel sources**, for framework-owned behaviour only:
   - upgrade guide: https://laravel.com/docs/13.x/upgrade
   - routing: https://laravel.com/docs/13.x/routing
   - controllers: https://laravel.com/docs/13.x/controllers
   - validation and Form Requests: https://laravel.com/docs/13.x/validation
   - Eloquent API resources: https://laravel.com/docs/13.x/eloquent-resources
   - authorization: https://laravel.com/docs/13.x/authorization
   - events: https://laravel.com/docs/13.x/events
   - queues: https://laravel.com/docs/13.x/queues
   - service container: https://laravel.com/docs/13.x/container
   - API reference: https://api.laravel.com/docs/13.x/
3. **The owning skill**, for anything that is not framework-owned. The ownership table in `SKILL.md` names each owner and what wins on conflict; that table is the only list of owners in this skill.
4. **A repository-local upstream skill**, for framework mechanics only — see `references/10-layer-map.md`, "Upstream rules this skill overrides". It is not owned by this repository, it can change between runs, and it never settles a rule about layering, tenant identity, cross-request state, or an authorization decision.
5. **Community posts**, for vocabulary and troubleshooting leads only. Confirm every contract, middleware, resource, and lifecycle claim against repository code or an official source above before acting on it.

## Which Laravel version this assumes

Laravel 13 on PHP 8.5, unless the repository is pinned lower. The dependency bumps, the framework-owned file comparisons, and the per-symbol upgrade audit points for a 12 → 13 move are held in one place: `alaa-php-clean-code references/laravel-best-practices.md`, its Laravel 13 audit points. This skill states none of them, because they are per-file framework-API policy and that file names the symbols being replaced.

What this skill contributes to an upgrade is the boundary question only: if the upgrade changes a public request or response shape, a route's precedence, or a serialization result a consumer reads, it is a contract change and runs through the deprecation procedure in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` rather than shipping as an upgrade side effect.
