# Companion skill routing checklist

## Contents
- Mandatory routing rule
- Routing checklist
- Skill-by-skill triggers
- Common combined scenarios
- Final audit requirement

## Mandatory routing rule
Companion skills are mandatory when their trigger fires.

Do not treat them as optional inspiration. The correct flow is:
1. classify the task scope
2. identify which specialist concerns are in scope
3. read the matching skill or skills
4. apply `alaa-php-clean-code` inside those boundaries

If multiple skills apply, route to all of them in the order that protects contracts first.

## Routing checklist
Run this checklist before editing non-trivial code:
- Is the task multi-file, long, behavior-changing, or whole-project? -> `alaa-workflow`
- Does it change layer boundaries, API contracts, DTO boundaries, `public_id`, or outbox behavior? -> `alaa-laravel-architecture`
- Does it touch Ala gateway trust, tenant derivation, request identity, trusted headers, or downstream auth context? -> `alaa-trust-gateway-auth`
- Does it touch migrations, queries, indexes, transactions, Redis primitives, or data concurrency? -> `alaa-data-layer`
- Does it touch jobs, events, retries, idempotency, consumers, or outbox consumption? -> `alaa-async-messaging`
- Does the async path use RabbitMQ or Laravel RabbitMQ specifics? -> `alaa-laravel-job-rabbitmq`
- Does it run under Octane, Swoole, or RoadRunner, or does it change hot-path singleton behavior? -> `alaa-octane-performance`
- Does it touch auth, authorization, files, URLs, secrets, validation, tenancy, or other trust surfaces? -> `alaa-security-review`
- Does it touch logs, traces, metrics, alerts, or Sentry? -> `alaa-observability-soc`
- Does it touch CI, Pint, PHPStan, test commands, test gating, repo quality gates, or pipelines? -> `alaa-cicd-laravel-postgres`
- Does it change README, docs, Postman, diagrams, or env docs? -> `alaa-docs-farsi`
- Is MongoDB already in the repo or explicitly requested? -> `alaa-mongodb-patterns`

## Skill-by-skill triggers

### `alaa-workflow`
Read first when the task is non-trivial, touches multiple files, changes behavior, or affects the whole project.

Mandatory outcome:
- create or update the plan artifact required by that skill
- use phased execution and explicit validation steps

### `alaa-laravel-architecture`
Read before changing:
- controller-service-repository-resource flow
- DTO boundaries
- `public_id` usage or route binding
- event emission or outbox flow
- cross-module boundaries or API contract shape

Mandatory outcome:
- architectural boundaries remain correct before clean-code polish is applied

### `alaa-trust-gateway-auth`
Read before changing:
- trusted headers
- JWT-derived identity
- tenant or project derivation from gateway claims
- step-up auth, session trust, or downstream auth propagation
- any route or middleware behind the Ala gateway that depends on trust context

Mandatory outcome:
- do not refactor away or invent gateway trust semantics

### `alaa-data-layer`
Read before changing:
- database schema or migrations
- indexes or query patterns
- transactions, locks, or concurrency
- tenant scoping in persistence
- Redis keys, invalidation, locks, or rate limiting

Mandatory outcome:
- data correctness and performance decisions are owned there, not guessed here

### `alaa-async-messaging`
Read before changing:
- queue jobs
- event consumers or producers
- idempotency, retries, DLQ, backoff, ordering, or outbox consumption
- side effects that move off the request thread

Mandatory outcome:
- async correctness comes first; only then polish code shape locally

### `alaa-laravel-job-rabbitmq`
Read when the async surface includes:
- RabbitMQ / AMQP transport
- topology or queue naming
- Laravel RabbitMQ worker behavior
- DLQ / retry transport details specific to RabbitMQ

Mandatory outcome:
- transport-specific semantics remain correct

### `alaa-octane-performance`
Read before changing:
- long-lived worker services
- singletons with mutable request state
- hot paths
- request reset rules or tenant context holders
- code that may behave differently under Octane than under FPM

Mandatory outcome:
- no cross-request leaks or unsafe singleton behavior

### `alaa-security-review`
Read before changing:
- auth, authorization, permissions, tenancy, privilege checks
- validation of untrusted input
- file uploads, file reads, URL fetching, SSRF-like paths
- secrets, tokens, credentials, or sensitive error flows

Mandatory outcome:
- do not let a cleanup weaken trust boundaries

### `alaa-observability-soc`
Read before changing:
- structured logs
- correlation IDs
- traces, metrics, alerts, or Sentry
- incident-facing runbook behavior

Mandatory outcome:
- observability fields and operational semantics remain aligned

### `alaa-cicd-laravel-postgres`
Read before changing:
- CI workflows
- linting or static-analysis config
- test commands or quality gates
- pipeline expectations for PHP/Laravel repos

Mandatory outcome:
- repo automation stays deterministic and consistent with the implementation

### `alaa-docs-farsi`
Read when changing:
- README or docs pages
- Postman collections or environment files
- operational or developer-facing setup docs
- request-flow diagrams

Mandatory outcome:
- docs workflow is followed, but the final docs content stays in English when `alaa-php-clean-code` is the governing coding skill unless the user asked otherwise

### `alaa-mongodb-patterns`
Read only when:
- MongoDB already exists in the repository, or
- the user explicitly asks for MongoDB design or changes

Mandatory outcome:
- do not introduce MongoDB by accident into a Postgres-first repository

## Common combined scenarios

### Gateway-backed HTTP endpoint with DB work
Usually requires:
- `alaa-workflow`
- `alaa-laravel-architecture`
- `alaa-trust-gateway-auth`
- `alaa-data-layer`
- `alaa-security-review`
- `alaa-docs-farsi` if the contract or examples changed

### RabbitMQ consumer or outbox listener
Usually requires:
- `alaa-workflow`
- `alaa-laravel-architecture`
- `alaa-async-messaging`
- `alaa-laravel-job-rabbitmq` when RabbitMQ transport details matter
- `alaa-observability-soc`
- `alaa-security-review` if auth or tenant boundaries are involved

### Whole-project cleanup
Always start with:
- `alaa-workflow`
- `alaa-laravel-architecture`
- `alaa-php-clean-code`

Then add:
- any other skill whose trigger is touched during the audit

## Final audit requirement
The final report should state which companion skills governed the task. This is the audit trail that shows routing actually happened.
