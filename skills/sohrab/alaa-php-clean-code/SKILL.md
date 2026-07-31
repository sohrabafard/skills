---
name: alaa-php-clean-code
description: "PHP 8.5 / Laravel 13 code-level craft for Octane-safe services: naming and one-author consistency, SOLID, design-pattern and smell diagnosis, repository-first persistence with cache-decorator-only caching, modern PHP and PSR/PER, size budgets, boundary error handling, Pest idiom, and mode-aware refactor blast radius. Use before writing, reviewing, or refactoring any PHP or Laravel file, and for whole-repo consistency passes. Do not use for: layering and envelopes (/alaa-laravel-architecture); Octane runtime invariants and worker tuning (/alaa-octane-performance); schema, query plans and Redis (/alaa-data-layer); trusted headers and tenant derivation (/alaa-trust-gateway-auth); timeout and retry values (/alaa-services-contract, /alaa-reliability-sla); what makes a test a test (/alaa-testing-strategy); complexity bounds and the N+1 decision (/alaa-algorithms-data-structures); subagent orchestration (/alaa-cc-orchestrator); or a one-line edit with no design choice in play."
---

# Alaa PHP Clean Code

Make PHP and Laravel code written by many different agents read as if one careful author wrote it, and keep it correct inside a long-lived worker serving many tenants.

This skill owns code shape inside files, classes, methods, and local module boundaries. Inside a companion skill's boundary it stays the code-quality baseline; it never replaces that skill. Companion skills are written `/name` for Claude Code and `$name` for Codex; both forms appear at every call site.

## Quick start — do not skip a step

1. Read the repo-local `AGENTS.md`.
2. Apply `/alaa-low-noise` (`$alaa-low-noise`) when the task is non-trivial.
3. Read `references/00-topic-map.md` — the only router here. It maps your situation to the local file, the claim you are about to make to the skill that owns it, and the task to the sibling skills you must read first.
4. Classify the task mode (below). The mode fixes the blast radius before any file is edited.
5. If the task is non-trivial, multi-file, behaviour-changing, or whole-project, read `/alaa-workflow` (`$alaa-workflow`) and create or update the plan artifact it requires.
6. Work the ownership map. Read every skill whose row fires **before** editing the code that row governs.
7. Read `references/source-map.md` when any of its freshness triggers fire — it owns the trigger list and the source order.
8. Read `references/octane-clean-code.md` for every Laravel change, and `references/consistency-and-naming.md` before renaming any class, method, namespace, file, folder, or concept.
9. Implement the smallest coherent change set the mode allows, validate, and report against the output contract.

## Compatibility target

PHP 8.5 and Laravel 13 are the current baseline for new Alaa Laravel services; `composer.json` in the target repository is the authority for what that repository runs. Use a newer feature only where the installed runtime and toolchain support it, and do not let a Laravel 13 repository drift back to Laravel 12 conventions in new code, refactors, reviews, or upgrade planning. The Laravel 12 → 13 upgrade itself — dependency bumps, skeleton comparison, renamed framework classes, changed event properties — belongs to `/alaa-laravel-upgrade-all-packages` (`$alaa-laravel-upgrade-all-packages`); the code-level audit points that outlive the upgrade are in `references/laravel-best-practices.md`.

**Octane is the default runtime assumption.** Treat every Alaa Laravel service as running under Octane unless `composer.json` requires no `laravel/octane` **and** the repository has no `config/octane.php`. Both must hold before you may reason as if a worker serves one request.

## When NOT to use

- The edit is one line with no design choice in it: a typo, a version bump, a copy change.
- The question can only be answered by reading more than one class — which layer may call which, what an
  envelope carries, who derives a tenant, what a worker retains between requests.
- The question is a value rather than a shape: a timeout, a retry count, a page size, a cardinality cap.
- The ownership boundary below names the owner for each of these.

## Ownership boundary — what this skill does not own

This table answers *who decides*. `references/00-topic-map.md` answers *when to read* — it is the only router in this skill, and its third table carries the read triggers.

Where a row's condition fires, read that skill before editing the affected code, then apply this skill inside its boundary. **On conflict the named owner wins.** Claiming a companion skill was respected without reading it is a reporting failure.

| Concern | Owner |
|---|---|
| The quality bar itself — never restate it | `alaa-project-constitution references/quality-bar.md` |
| Layering, API envelopes, `public_id`, DTO boundaries, outbox shape | `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) |
| A design pass before implementation, when an interface shape, a data writer, a consistency / ordering / idempotency / concurrency / caching property, a dependency edge, a deployable unit, or degraded-path behaviour changes | `/alaa-system-design` (`$alaa-system-design`) |
| Every shared name: envelopes, error and event codes, queue and exchange names, metric names, trusted header names, request deadlines | `/alaa-services-contract` (`$alaa-services-contract`) |
| Every timeout, retry count, pool bound, acquire wait, shed threshold — every number | `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` |
| Retry, jittered backoff, retry budget, breaker, bulkhead, admission control, degradation and idempotency **doctrine** | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Octane runtime facts and every absolute worker invariant: which values may never be retained and where, the reset mechanism, worker lifecycle and reload, the leak regression test, connection and Redis lifecycle, cache tiers, worker sizing, runtime portability | `/alaa-octane-performance` (`$alaa-octane-performance`) |
| Schema, migrations, indexes, query plans, transactions, pooling, Redis primitives, cache key design, TTL, invalidation | `/alaa-data-layer` (`$alaa-data-layer`) |
| S3 or MinIO client library choice and configuration | `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) |
| The repository-pattern gate preceding any caching, and its completeness definition | `alaa-data-layer references/50-redis-laravel-octane.md`, "Step 0 — repository-pattern gate" |
| Trusted headers, JWT-derived identity, tenant and project derivation, downstream auth propagation | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Object-level relationship authorization | `/openfga` (`$openfga`) |
| Security review triggers, threat classes, fail-closed vs fail-open | `/alaa-security-review` (`$alaa-security-review`) |
| Complexity budgets, structure choice, the whole N+1 family | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| What makes a test a test, test layer placement, doubles, the six proof levels, flake classification | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Queue, broker, retry transport, DLQ, ordering, message-plane design | `/alaa-async-messaging` (`$alaa-async-messaging`), `/alaa-laravel-job-rabbitmq` (`$alaa-laravel-job-rabbitmq`) |
| Whether a signal is required, and the gate it feeds | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| CI, quality gates, Pint and PHPStan configuration, pipeline behaviour | `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) |
| Docs-alignment workflow, Postman sync, docs consistency checks | `/alaa-repo-docs` (`$alaa-repo-docs`) |
| Long-task planning, phasing, resumable state, shared plan paths such as `docs/_agent_plans/*` | `/alaa-workflow` (`$alaa-workflow`) |
| Subagent lanes, role prompts, delegation, review gates — this skill carries no subagent template | `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator` in Codex) |
| Controlled and risky operations, the proof-strength vocabulary | `/alaa-controlled-ops` (`$alaa-controlled-ops`) |
| Codex-only tools and runtime affordances, including parallel tool invocation | `/alaa-codex-runtime-ops` (`$alaa-codex-runtime-ops`) |
| Model and effort choice — name no model, ever | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
| Crockford Base32, integer, string and UUIDv7 codecs shared with JS, shell, or HAProxy Lua | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
| MongoDB design, only where the repo already uses MongoDB or the user asks | `/alaa-mongodb-patterns` (`$alaa-mongodb-patterns`) |
| Current OpenAI API, model, prompt, tool and product behaviour cited in docs | `/openai-docs` (`$openai-docs`) |

Inside those boundaries this skill still contributes: the PHP mechanism carrying a contract name; the obligation that both timeouts are set explicitly; the code shape that makes the Octane invariants hold; where persistence access may live; the Laravel idiom carrying a chosen complexity answer; Pest and PHPUnit construct choice; job and listener shape with the run-twice proof; the local checks run before claiming done; and docblock and artifact expectations. **Never edit anything under `vendor/`** — those are upstream subtrees; wrap them from the owning skill.

## Task modes

Mandatory. If the user names none, infer the narrowest one that satisfies the request, and never silently escalate from a scoped mode to a whole-project mode.

| The request is | Mode |
|---|---|
| New code, or a local cleanup with no explicit broad-refactor request | `scoped-soft` |
| A deeper internal cleanup of one bounded area, public contracts held stable | `scoped-hard-contract-preserving` |
| A repo-wide cleanup with no explicit request to standardise | `whole-project-preserve-local` |
| An explicit request to standardise the repo toward one Alaa convention set | `whole-project-normalize-alaa` |

`references/refactor-modes.md` owns what each mode allows and forbids, the public-contract inventory preceding the two harder modes, the persistence-naming rules that apply only in `whole-project-normalize-alaa`, and the safe sequencing for whole-project work. Read it whenever the task includes refactoring, a new slice design, or more than one touched file.

## Uniformity rule

Two statements are both true because they govern different code:

- **Inside an existing repository, that repository's own convention wins for code that already exists there.** A repository written in two dialects costs every later reader more than either dialect costs alone. Converting an existing repository to the house convention happens only in `whole-project-normalize-alaa`, which the user must ask for explicitly.
- **A new surface takes the house convention.** A new module, service, or file family with no sibling in the repository has no local convention to preserve, so it follows `references/consistency-and-naming.md` from its first file. Uniformity across services is the standing preference; an existing local dialect your change would otherwise fracture is the only reason to depart from it.

The observable test for "an existing convention": at least two files in the repository already do it the same way. One file is a precedent, not a convention.

Repository reality outranks every style rule stated here — an existing public contract, a pinned framework version, and a repo-local rule each win. `references/consistency-and-naming.md` owns the naming rules themselves.

## Pattern decision order

Choose the simplest abstraction that fixes the real problem. When a pattern seems needed but the right one is unclear, run the symptom → pattern diagnostic at the top of `references/design-patterns.md`: pick by observable smell, then answer its confirming question. A "no" means the pattern is wrong.

1. A plain class, a private method extraction, or a better name.
2. A service, when a controller, job, listener, or command does more than orchestration.
3. A repository, before any application-layer code reads or writes persistence.
4. A DTO, when validated or transferred data crosses a layer boundary and needs a stable typed shape.
5. A value object, when a domain concept carries invariants or behaviour.
6. A strategy, when algorithms or providers vary behind one narrow contract.
7. A factory, when construction enforces invariants or hides meaningful branching.
8. An adapter, when an external provider's API must be hidden behind an internal contract.
9. A pipeline, when a workflow is a sequence of independent reorderable steps that all run.
10. A command or job, when an action must be queued, retried, delayed, audited, or run outside the HTTP request.
11. A backed enum plus one transition authority, when statuses have guarded transitions — never scattered status `if`s.
12. An interface, only where a real seam exists: multiple implementations, a package boundary, an external integration, or a test seam that genuinely improves clarity.

Every abstraction removes a named smell or it does not go in; do not stack Repository + Factory + Strategy + Interface for aesthetics. **Wrap a framework capability rather than reimplementing it** — a wrapper survives an upgrade and a reimplementation does not.

`references/code-smells-and-refactoring-triggers.md` owns the diagnosis layer: the five smell families in Laravel terms with a treatment each, the Rule of Three, when to refactor, and when not to.

## Mandatory repository policy

In Alaa Laravel code the Repository pattern is mandatory for application-layer persistence access.

- Controllers, services, jobs, listeners, commands, policies, actions, pipelines, and adapters must not compose Eloquent or query-builder persistence directly. They call a repository.
- Create or reuse one repository per aggregate, use case, read model, or persistence boundary the task touches. A generic `BaseRepository` is not one.
- Repositories hold persistence and query composition only: business rules stay in services, authorization in policies and gates, serialization in resources.
- Repositories accept typed DTOs, filter objects, value objects, or scalars — never a raw `Request` or an unvalidated array. A simple operation may have a simple repository method; the boundary still belongs in the repository.
- **The allowed exceptions are enumerated in `references/laravel-best-practices.md` under "Repository-first persistence".** Read that list before wrapping a model relationship, scope, cast or accessor, a migration, a factory, a seeder, a test assertion, or a resource reading an already-loaded model — those are not violations.
- Existing direct Eloquent outside a repository is legacy debt. **When a line in your diff composes Eloquent or the query builder outside a repository, that access moves behind a repository in the same change.** The trigger is a line in your diff, not a file you opened.
- Caching domain data lives only in a repository **decorator** — a `Cached<Domain>Repository` implementing the same interface — never inside the concrete repository and never as a `Cache::` call in a controller or service. A complete repository layer is the precondition; its completeness definition and the gate are owned by `alaa-data-layer references/50-redis-laravel-octane.md`, "Step 0 — repository-pattern gate". The decorator's shape, stacking order, and the Redis-outage fall-through that makes it worth having are in `references/design-patterns.md` (Decorator).

## Non-negotiable defaults

- `declare(strict_types=1);` in every new PHP file, unless every existing file in the same directory omits it. Type every parameter, return value, and property unless a framework contract forbids it.
- No service location: `app()`, `resolve()`, or an injected container inside business logic hides the dependency graph. Inject the collaborator through the constructor instead.
- Side effects at the edges, core logic deterministic. A method that writes, queues, or calls out says so in its name and its signature.
- Catch an exception only at a boundary that can translate it. Never bury a failure behind `null`, `false`, or a silent log.
- Public parameter names stay stable wherever a caller may use named arguments.
- **Merge and partial-update logic decides by key presence, never by truthiness.** `$data['count'] ?? $existing` silently discards a legitimate `0`, `false`, or `''`. Where absence and empty are different facts, use `array_key_exists()`, `$request->has()`, or an explicit `!== null`.
- `env()` is read only inside `config/*.php`; application code reads `config()` or receives typed config through its constructor.
- Event names, error codes, cache-key prefixes, queue names, and metric names are backed enums or class constants, never inline strings — a typo in an inline string is a silent contract or observability hole. The canonical names come from `/alaa-services-contract` (`$alaa-services-contract`); this skill owns only the mechanism carrying them.
- Never guess an external fact — a provider payload, another service's contract, a header's meaning. Write `NEEDS_<PROVIDER>_CONFIRMATION` or `[gap]` at the site and report it instead of inventing a plausible value.

`references/php-modern-and-psr.md` owns the language-level rules: `readonly`, `DateTimeImmutable`, enums plus `match`, union and intersection types, the PHP 8.5 features, lazy objects, the PSR/PER baseline, and the language-level anti-patterns.

## Size and complexity budgets

Gates, not advice. A repo-local rule with stricter numbers wins.

- A class — controller, service, repository, job, listener, action, support class: **≤ 400 lines**.
- A single method: **≤ 60 lines**. A controller action stays orchestration-only regardless of length.
- One primary class per file. A second class rides along only where at least two existing files in the same directory already do that.
- A constructor taking more than five collaborators is a class doing too much. Split by use case before injecting a sixth.

**A class or method you create or materially change is within budget when you are done.** Split along the standard seams first: validation → Form Request; business flow → one focused service per use case; persistence → repository or query object; branching by provider or algorithm → strategy; construction → factory; cross-cutting wrap → decorator.

For a file already over budget before your change, the responsibility you touched comes under budget in the same change. If it cannot — the split would cross a public contract the mode preserves, or needs a companion skill's decision you do not have — **stop and report the blocker with the file, its current size, and the seam you would have cut.** Growing an over-budget file is not an option this skill offers.

The quality bar these budgets serve is owned by `alaa-project-constitution references/quality-bar.md`.

## SOLID posture

Apply SOLID where its absence causes real pain — untestable code, shotgun changes, unstable contracts, unsafe worker state — never as a scoring system. Clarity, fewer moving parts, and repo consistency beat textbook purity. `references/solid-in-practice.md` owns the per-principle depth, the recognition signals for each violation, and the review checklist.

## Laravel defaults

- Controllers stay thin and deterministic: receive validated input, call the service layer, return a resource.
- **Declare route posture at registration.** Auth, permission, throttle, and tenant middleware live on the route or route group, visible where the route is defined — never as an ad-hoc check inside a controller body. A route whose trust posture must be inferred from its handler is a review failure.
- **Every relation and every count read inside an API Resource is guarded by `whenLoaded()`, `whenCounted()`, or `whenAggregated()`.** An unguarded `$this->relation` fires one query per row whenever the caller did not eager-load it, and a Resource cannot see what the caller loaded — so the guard is mandatory, never conditional.
- Follow the repository's existing folder structure. Where it has none and the task enters architecture territory, folder and layer decisions belong to `/alaa-laravel-architecture` (`$alaa-laravel-architecture`).
- Eager-loading strategy and large-dataset traversal carry a decision this skill does not own: when a collection grows with tenants, rows, history, or fan-out, `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns the bound, whether the path streams or materialises, and which N+1 resolution applies. This skill owns the Laravel idiom that carries the answer — `references/laravel-best-practices.md`.

## Octane-safe code shape

Clean code is not acceptable if it leaks request state across a long-lived worker.

- **No value belonging to one request is retained anywhere that outlives the request.** `/alaa-octane-performance` (`$alaa-octane-performance`) owns the enumerated list of those values, the sites where retaining them is forbidden, the reset mechanism, and the leak regression test. Read it before binding any service, adding any static property, or writing any observer, and treat its wording as the invariant.
- **A service that needs a per-request value takes it as a method argument.** Constructor-injecting `Request`, the authenticated user, or a tenant-context holder into a service is a review failure — and it is the shape from which the binding-lifetime question disappears, because a service holding no per-request state is safe at any lifetime.
- **Every in-memory memoization key inside a long-lived object includes the tenant or project identifier**, unless the value is explicitly global. Cache key design, TTL, and invalidation belong to `alaa-data-layer references/50-redis-laravel-octane.md`.

`references/octane-clean-code.md` holds how each design pattern is shaped so those invariants hold.

## Error-handling baseline

- Throw specific exceptions with clear ownership, preserve the previous exception when wrapping a low-level failure, and translate centrally at the HTTP, CLI, queue, and integration boundaries.
- **A definitive denial is never masked as success.** Validation failures, authorization failures, and non-transient 4xx never fall through to a path that behaves like success — a swallowed 403 turns a refusal into a silent grant.
- **Every outbound call sets both `timeout()` and `connectTimeout()` explicitly**, at the call site or in the client macro that builds it. A call setting neither inherits a default long enough to hold a worker through an SLA breach. Whether that call may retry, how it backs off, and what happens when the dependency is gone belong to `/alaa-reliability-sla` (`$alaa-reliability-sla`); every number belongs to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. This skill states no timeout and no retry count.
- Client-visible error messages stay safe and stable; debugging detail goes into structured logs, never into a user-facing string.

## Performance baseline

Measure before micro-optimizing. Avoid repeated encode/decode churn, broad object graphs, unnecessary temporary arrays, and reflection- or magic-heavy abstractions in hot code; use small immutable objects for stable data. Query shape and indexing belong to `/alaa-data-layer` (`$alaa-data-layer`); hot-path and worker behaviour to `/alaa-octane-performance` (`$alaa-octane-performance`); the complexity bound itself to `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).

## Documentation baseline

Documentation is part of done when behaviour, contracts, setup, env vars, request or response shapes, flows, or examples change. `references/documentation-and-artifacts.md` owns the docblock rules, README and docs expectations, Postman collection v2.1 shape, environment artifacts, and flow diagrams; the repo-wide docs workflow belongs to `/alaa-repo-docs` (`$alaa-repo-docs`), with output in simple, fluent English unless the user asks for another language.

## Validation before done

Run the relevant checks, preferring repo scripts and CI-pinned versions: style via `vendor/bin/pint --test` or the repo's formatter; static analysis via `vendor/bin/phpstan analyse` at the repo's configured level; then the targeted test filter for the changed behaviour followed by the affected suite.

**Report only what you observed run.** If a check could not run, state the exact blocked command and the reason — a check not observed to run has no result. Pipeline-level gating belongs to `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`).

What makes a test worth having — the broken implementation it defends against, the layer it belongs at, whether a double is honest, the proof level a claim reaches, and whether an intermittent failure is a product defect or a broken test — is owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`). This skill owns only the PHP-side construct choice: Pest and PHPUnit idiom, the database-refresh trait decision, and the run-twice proof for re-runnable units, all in `references/laravel-best-practices.md` under "Tests".

## Output contract

State, concisely and auditably: the selected task mode; which companion skills governed the work; whether public contracts were preserved and any intentional exception; the patterns introduced or deliberately avoided where the choice is non-obvious; each check run with its observed outcome, and the exact command and reason for any that did not run; documentation alignment status; and remaining risk or follow-up, including every budget blocker you reported rather than resolved.
