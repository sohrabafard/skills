---
name: alaa-php-clean-code
description: "PHP 8.5 and Laravel 13 code craft for Octane-safe services: naming, SOLID, pattern and smell diagnosis, repository-first persistence, cache-decorator caching, modern PHP and PSR/PER, size budgets, boundary error handling, Pest idiom, and refactor blast radius. Use before writing, reviewing, or refactoring a PHP or Laravel file, and for repo-wide consistency passes. Do not use for: layering and envelopes (/alaa-laravel-architecture); Octane runtime and workers (/alaa-octane-performance); schema, queries and Redis (/alaa-data-layer); trusted headers and tenancy (/alaa-trust-gateway-auth); timeout and retry values (/alaa-services-contract, /alaa-reliability-sla); test doctrine (/alaa-testing-strategy); complexity bounds and N+1 (/alaa-algorithms-data-structures); orchestration (/alaa-cc-orchestrator); or a one-line edit."
---

# Alaa PHP Clean Code

Make PHP and Laravel code written by many different agents read as if one careful author wrote it. Keep it correct inside a long-lived worker that serves many tenants.

This skill owns code shape inside files, classes, methods and local module boundaries. Inside a companion skill's boundary it stays the code-quality baseline, and it never replaces that skill. Cross-skill calls follow the single `/name` convention in the [pack instructions](../AGENTS.md).

## Quick start — do not skip a step

1. Read the repo-local `AGENTS.md`.
2. Apply `/alaa-low-noise` when the task is non-trivial.
3. Read `references/00-topic-map.md`, the only router here. It maps your situation to the local file, the claim you are about to make to the skill that owns it, the task to the sibling skills you must read first, and each concern to its owning skill.
4. Classify the task mode (below). The mode fixes the blast radius before you edit any file.
5. If the task is non-trivial, multi-file, behaviour-changing or whole-project, read `/alaa-workflow` and create or update the plan artifact it requires.
6. Work the ownership table in `references/00-topic-map.md` section 4. Read every skill whose row fires **before** you edit the code that row governs.
7. Read `references/source-map.md` when any of its freshness triggers fire. It owns the trigger list and the source order.
8. Read `references/octane-clean-code.md` for every Laravel change. Read `references/consistency-and-naming.md` before you rename any class, method, namespace, file, folder or concept.
9. Implement the smallest coherent change set the mode allows, validate it, and report against the output contract.

## Compatibility target

PHP 8.5 and Laravel 13 are the current baseline for new Alaa Laravel services. `composer.json` in the target repository is the authority for what that repository runs. Use a newer feature only where the installed runtime and toolchain support it. Do not let a Laravel 13 repository drift back to Laravel 12 conventions in new code, refactors, reviews or upgrade planning. `/alaa-laravel-upgrade-all-packages` owns dependency resolution and isolation, not framework code migration. For migration scope, follow its boundary and the official target-version upgrade guide. `references/laravel-best-practices.md` holds the surviving code-level audit points.

**Resolve runtime scope before you relax worker safety.** Read `/alaa-octane-performance` `SKILL.md`, "Scope condition", for applicability. When it applies, use Octane-safe code shape by default, including in code that a planned worker will execute.

## When NOT to use

- The edit is one line with no design choice in it: a typo, a version bump, a copy change.
- The question can only be answered by reading more than one class: which layer may call which, what an envelope carries, who derives a tenant, or what a worker retains between requests.
- The question is a value rather than a shape: a timeout, a retry count, a page size or a cardinality cap.
- The ownership table in `references/00-topic-map.md` section 4 names the owner for each of these.

## Ownership boundary — what this skill does not own

The ownership table in `references/00-topic-map.md` section 4 answers *who decides* each concern this skill does not own. Sections 1 to 3 of that file answer *when to read* a file or a skill.

Where a row's condition fires, read that skill before you edit the affected code, then apply this skill inside its boundary. **On conflict the named owner wins.** A claim that a companion skill was respected without reading it is a reporting failure.

Inside those boundaries this skill still contributes:

- the PHP mechanism that carries a contract name
- the obligation that both timeouts are set explicitly
- the code shape that makes the Octane invariants hold
- where persistence access may live
- the Laravel idiom that carries a chosen complexity answer
- the choice between Pest and PHPUnit constructs
- the job and listener shape with the run-twice proof
- the local checks run before you claim done
- docblock and artifact expectations

**Never edit anything under `vendor/`.** Those are upstream subtrees, and a local edit is either overwritten or collides. Wrap them from the owning skill.

## Task modes

Selecting a task mode is mandatory. If the user names none, infer the narrowest mode that satisfies the request. Never silently escalate from a scoped mode to a whole-project mode.

| The request is | Mode |
|---|---|
| New code, or a local cleanup with no explicit broad-refactor request | `scoped-soft` |
| A deeper internal cleanup of one bounded area, public contracts held stable | `scoped-hard-contract-preserving` |
| A repo-wide cleanup with no explicit request to standardise | `whole-project-preserve-local` |
| An explicit request to standardise the repo toward one Alaa convention set | `whole-project-normalize-alaa` |

Read `references/refactor-modes.md` whenever the task includes refactoring, a new slice design, or more than one touched file. It owns what each mode allows and forbids, the public-contract inventory that precedes the two harder modes, the persistence-naming rules that apply only in `whole-project-normalize-alaa`, and the safe sequencing for whole-project work.

## Uniformity rule

Two statements are both true, because they govern different code:

- **Inside an existing repository, that repository's own convention wins for code that already exists there.** A repository written in two dialects costs every later reader more than either dialect costs alone. Convert an existing repository to the house convention only in `whole-project-normalize-alaa`, which the user must ask for explicitly.
- **A new surface takes the house convention.** A new module, service or file family with no sibling in the repository has no local convention to preserve, so it follows `references/consistency-and-naming.md` from its first file. Uniformity across services is the standing preference. The only reason to depart from it is an existing local dialect that your change would otherwise fracture.

The observable test for "an existing convention": at least two files in the repository already do it the same way. One file is a precedent, not a convention.

Repository reality outranks every style rule stated here. An existing public contract, a pinned framework version and a repo-local rule each win. `references/consistency-and-naming.md` owns the naming rules themselves.

## Pattern decision order

Choose the simplest abstraction that fixes the real problem. When a pattern seems needed but the right one is unclear, run the symptom → pattern diagnostic at the top of `references/design-patterns.md`. Pick by observable smell, then answer its confirming question. A "no" means the pattern is wrong.

1. A plain class, a private method extraction, or a better name.
2. A service, when a controller, job, listener or command does more than orchestration.
3. A repository, before any application-layer code reads or writes persistence.
4. A DTO, when validated or transferred data crosses a layer boundary and needs a stable typed shape.
5. A value object, when a domain concept carries invariants or behaviour.
6. A strategy, when algorithms or providers vary behind one narrow contract.
7. A factory, when construction enforces invariants or hides meaningful branching.
8. An adapter, when an external provider's API must be hidden behind an internal contract.
9. A pipeline, when a workflow is a sequence of independent reorderable steps that all run.
10. A command or job, when an action must be queued, retried, delayed, audited, or run outside the HTTP request.
11. A backed enum plus one transition authority, when statuses have guarded transitions. Never scatter status `if`s.
12. An interface, only where a real seam exists: multiple implementations, a package boundary, an external integration, or a test seam that genuinely improves clarity.

Add an abstraction only when it removes a named smell. Do not stack Repository, Factory, Strategy and Interface for aesthetics. **Wrap a framework capability rather than reimplementing it.** A wrapper survives an upgrade, and a reimplementation does not.

When you diagnose what is wrong with code or decide whether to refactor it, read `references/code-smells-and-refactoring-triggers.md`. It owns the five smell families in Laravel terms with a treatment for each, the Rule of Three, when to refactor, and when not to.

## Mandatory repository policy

In Alaa Laravel code the Repository pattern is mandatory for application-layer persistence access.

- Controllers, services, jobs, listeners, commands, policies, actions, pipelines and adapters must not compose Eloquent or query-builder persistence directly. They call a repository.
- Create or reuse one repository for each aggregate, use case, read model or persistence boundary the task touches. A generic `BaseRepository` is not one.
- Repositories hold persistence and query composition only. Business rules stay in services, authorization in policies and gates, and serialization in resources.
- Repositories accept typed DTOs, filter objects, value objects or scalars, never a raw `Request` or an unvalidated array. A simple operation may have a simple repository method, but the boundary still belongs in the repository.
- **The allowed exceptions are enumerated in `references/laravel-best-practices.md` under "Repository-first persistence".** Read that list before you wrap a model relationship, scope, cast or accessor, a migration, a factory, a seeder, a test assertion, or a resource that reads an already-loaded model. Those are not violations.
- Existing direct Eloquent outside a repository is legacy debt. **When a line in your diff composes Eloquent or the query builder outside a repository, move that access behind a repository in the same change.** The trigger is a line in your diff, not a file you opened.
- Cache domain data only in a repository **decorator**: a `Cached<Domain>Repository` that implements the same interface. Never cache inside the concrete repository. Never call `Cache::` in a controller or service. A complete repository layer is the precondition. `alaa-data-layer references/50-redis-laravel-octane.md` owns its definition and the gate, "Step 0 — repository-pattern gate". `references/design-patterns.md` (Decorator) holds the decorator's shape, its stacking order, and the Redis-outage fall-through that makes it worth having.

## Non-negotiable defaults

- Put `declare(strict_types=1);` in every new PHP file, unless every existing file in the same directory omits it. Type every parameter, return value and property, unless a framework contract forbids it.
- Use no service location. `app()`, `resolve()` or an injected container inside business logic hides the dependency graph. Inject the collaborator through the constructor instead.
- Keep side effects at the edges and core logic deterministic. A method that writes, queues or calls out says so in its name and its signature.
- Catch an exception only at a boundary that can translate it. Never bury a failure behind `null`, `false` or a silent log.
- Keep public parameter names stable wherever a caller may use named arguments.
- **Merge and partial-update logic decides by key presence, never by truthiness.** `$data['count'] ?? $existing` silently discards a legitimate `0`, `false` or `''`. Where absence and empty are different facts, use `array_key_exists()`, `$request->has()` or an explicit `!== null`.
- Read `env()` only inside `config/*.php`. Application code reads `config()` or receives typed config through its constructor.
- Make event names, error codes, cache-key prefixes, queue names and metric names backed enums or class constants, never inline strings, because a typo in an inline string is a silent contract or observability hole. The canonical names come from `/alaa-services-contract`. This skill owns only the mechanism that carries them.
- Never guess an external fact: a provider payload, another service's contract, or a header's meaning. Write `NEEDS_<PROVIDER>_CONFIRMATION` or `[gap]` at the site and report it instead of inventing a plausible value.

When you use a language-level construct, read `references/php-modern-and-psr.md`. It owns the language-level rules: `readonly`, `DateTimeImmutable`, enums plus `match`, union and intersection types, the PHP 8.5 features, lazy objects, the PSR and PER baseline, and the language-level anti-patterns.

## Size and complexity budgets

These budgets are gates, not advice. A repo-local rule with stricter numbers wins.

- A class (controller, service, repository, job, listener, action or support class): **≤ 400 lines**.
- A single method: **≤ 60 lines**. A controller action stays orchestration-only regardless of length.
- One primary class per file. A second class rides along only where at least two existing files in the same directory already do that.
- A constructor that takes more than five collaborators belongs to a class doing too much. Split it by use case before you inject a sixth.

**A class or method you create or materially change is within budget when you are done.** Split along the standard seams first: validation → Form Request; business flow → one focused service per use case; persistence → repository or query object; branching by provider or algorithm → strategy; construction → factory; cross-cutting wrap → decorator.

For a file that was already over budget before your change, bring the responsibility you touched under budget in the same change. If you cannot, because the split would cross a public contract the mode preserves or needs a companion skill's decision you do not have, **stop and report the blocker with the file, its current size, and the seam you would have cut.** Growing an over-budget file is not an option this skill offers.

`alaa-project-constitution references/quality-bar.md` owns the quality bar these budgets serve.

## SOLID posture

Apply SOLID where its absence causes real pain (untestable code, shotgun changes, unstable contracts, unsafe worker state), never as a scoring system. Clarity, fewer moving parts and repo consistency beat textbook purity. When you answer a SOLID question or justify an abstraction, read `references/solid-in-practice.md`. It owns the per-principle depth, the recognition signals for each violation, and the review checklist.

## Laravel defaults

- Keep controllers thin and deterministic: receive validated input, call the service layer, return a resource.
- **Declare route posture at registration.** Put auth, permission, throttle and tenant middleware on the route or route group, visible where the route is defined, never as an ad-hoc check inside a controller body. A route whose trust posture must be inferred from its handler is a review failure.
- **Guard every relation and every count read inside an API Resource with `whenLoaded()`, `whenCounted()` or `whenAggregated()`.** An unguarded `$this->relation` fires one query per row whenever the caller did not eager-load it. A Resource cannot see what the caller loaded, so the guard is mandatory, never conditional.
- Follow the repository's existing folder structure. Where it has none and the task enters architecture territory, `/alaa-laravel-architecture` owns folder and layer decisions.
- Eager-loading strategy and large-dataset traversal carry a decision this skill does not own. When a collection grows with tenants, rows, history or fan-out, `/alaa-algorithms-data-structures` owns the bound, whether the path streams or materialises, and which N+1 resolution applies. This skill owns the Laravel idiom that carries the answer: `references/laravel-best-practices.md`.

## Octane-safe code shape

Clean code is not acceptable if it leaks request state across a long-lived worker.

- **Retain no value that belongs to one request anywhere that outlives the request.** `/alaa-octane-performance` owns the enumerated list of those values, the sites where retaining them is forbidden, the reset mechanism, and the leak regression test. Read it before you bind any service, add any static property or write any observer. Treat its wording as the invariant.
- **A service that needs a per-request value takes it as a method argument.** Constructor-injecting `Request`, the authenticated user or a tenant-context holder into a service is a review failure. A method argument removes the binding-lifetime question, because a service that holds no per-request state is safe at any lifetime.
- **Include the tenant or project identifier in every in-memory memoization key inside a long-lived object**, unless the value is explicitly global. `alaa-data-layer references/50-redis-laravel-octane.md` owns cache key design, TTL and invalidation.

When you shape a design pattern for a long-lived worker, read `references/octane-clean-code.md`. It holds how each pattern is shaped so that those invariants hold.

## Error-handling baseline

- Throw specific exceptions with clear ownership. Preserve the previous exception when you wrap a low-level failure. Translate centrally at the HTTP, CLI, queue and integration boundaries.
- **Never mask a definitive denial as success.** Validation failures, authorization failures and non-transient 4xx responses never fall through to a path that behaves like success. A swallowed 403 turns a refusal into a silent grant.
- **Set both `timeout()` and `connectTimeout()` explicitly on every outbound call**, at the call site or in the client macro that builds it. A call that sets neither inherits a default long enough to hold a worker through an SLA breach. `/alaa-reliability-sla` owns whether that call may retry, how it backs off, and what happens when the dependency is gone. `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` owns every number. This skill states no timeout and no retry count.
- Keep client-visible error messages safe and stable. Put debugging detail into structured logs, never into a user-facing string.

## Performance baseline

Measure before you micro-optimize. In hot code, avoid repeated encode and decode churn, broad object graphs, unnecessary temporary arrays, and abstractions that rely on reflection or magic. Use small immutable objects for stable data. `/alaa-data-layer` owns query shape and indexing. `/alaa-octane-performance` owns hot-path and worker behaviour. `/alaa-algorithms-data-structures` owns the complexity bound itself.

## Documentation baseline

Documentation is part of done when behaviour, contracts, setup, env vars, request or response shapes, flows or examples change. When that happens, read `references/documentation-and-artifacts.md`. It owns PHP docblocks, README and docs alignment, flow alignment, and the output language of documentation, and it routes Postman collection and environment generation to `/alaa-postman-collections`. `/alaa-repo-docs` owns the repo-wide docs workflow.

## Validation before done

Run the relevant checks. Use repo scripts and CI-pinned versions where they exist.

- Style: `vendor/bin/pint --test` or the repo's formatter.
- Static analysis: `vendor/bin/phpstan analyse` at the repo's configured level.
- Then the targeted test selector for the changed behaviour: `--filter`, or the topic's `--group`.

The affected suite is the affected tier. The authority that `/alaa-testing-strategy` assigns runs it. A session with no such authority runs it once, on the final tree.

**Report only what you observed run.** If a check could not run, state the exact blocked command and the reason. A check not observed to run has no result. `/alaa-cicd-laravel-postgres` owns pipeline-level gating.

`/alaa-testing-strategy` owns what makes a test worth having: whether it is owed at all (never for Laravel, package or vendor behaviour, only for this application's use of it), the broken implementation it defends against, the layer it belongs at, whether a double is honest, the proof level a claim reaches, and whether an intermittent failure is a product defect or a broken test. This skill owns only the PHP-side construct choice: Pest and PHPUnit idiom, the database-refresh trait decision, and the run-twice proof for re-runnable units, all in `references/laravel-best-practices.md` under "Tests".

## Output contract

State these items, concisely and auditably:

- the selected task mode
- which companion skills governed the work
- whether public contracts were preserved, and any intentional exception
- the patterns introduced or deliberately avoided where the choice is non-obvious
- each check run with its observed outcome, and the exact command and reason for any that did not run
- documentation alignment status
- remaining risk or follow-up, including every budget blocker you reported rather than resolved
