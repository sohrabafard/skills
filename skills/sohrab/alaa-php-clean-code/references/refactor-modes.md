# Refactor modes and contract posture

## Contents
- Why task mode matters
- Default mode selection
- `scoped-soft`
- `scoped-hard-contract-preserving`
- `whole-project-preserve-local`
- `whole-project-normalize-alaa`
- Public-contract inventory
- Safe sequencing for whole-project work
- Anti-patterns

## Why task mode matters
This skill supports both local change sets and whole-project refactors. The agent must choose the mode before editing code because the allowed blast radius is different in each case.

Task mode controls:
- how far renames may propagate
- whether repo-local conventions win or Alaa normalization wins
- whether large structural extractions are allowed
- how aggressively weak abstractions may be removed
- how broad the documentation and test sweep must be

## Default mode selection
Use the safest matching rule:
- New code or a local cleanup with no explicit broad-refactor request -> `scoped-soft`
- Deeper internal cleanup while preserving public contracts -> `scoped-hard-contract-preserving`
- Whole-repo cleanup with no explicit normalization request -> `whole-project-preserve-local`
- Whole-repo standardization toward one Alaa convention set -> `whole-project-normalize-alaa`

If the request is ambiguous, do not silently escalate from a scoped mode to a whole-project mode.

## `scoped-soft`
### Use when
- adding a new feature slice
- cleaning a controller, request, service, repository, resource, job, listener, or DTO in one bounded area
- fixing a bug while making the touched code cleaner

### Main goal
Deliver a clean local slice with minimal collateral change.

### Required behavior
- Keep the touched slice fully aligned with `alaa-php-clean-code`.
- Refactor immediate neighbors only when needed to keep behavior safe, contracts intact, and the local design coherent.
- Reuse the repository's existing naming and folder conventions unless they directly block clarity.
- Add or update the nearest meaningful tests.
- Update only the documentation artifacts that are actually impacted.

### Allowed changes
- rename private or local symbols in the touched slice
- extract a DTO, value object, strategy, or small service where it clearly reduces confusion
- move a file inside the same local module if that reduces ambiguity and does not cause broad churn
- remove a thin helper or duplicate method in the touched slice

### Avoid
- repo-wide renames
- sweeping folder moves
- broad convention changes
- replacing one repository-wide naming system with another

## `scoped-hard-contract-preserving`
### Use when
- the user wants a serious refactor in one bounded area
- the current slice has structural debt that cannot be fixed with a tiny cleanup
- internal design needs real extraction or consolidation, but public contracts should remain stable

### Main goal
Aggressively improve the internals of the chosen slice while preserving external behavior and public contracts by default.

### Required behavior
- Inventory the public contracts touched by the slice before refactoring.
- Preserve those contracts unless the user explicitly authorizes a breaking change or a security bug forces a justified exception.
- Prefer reviewable batches: naming and extraction first, then structural cleanup, then docs and tests.
- Remove weak abstractions that add no value.
- Keep the final surface easier to maintain than what you started with.

### Allowed changes
- extract services, DTOs, value objects, strategies, repositories, resources, requests, or policies inside the affected slice
- move files within the same bounded module or feature area
- rename internal classes, methods, variables, and tests inside the slice
- replace vague helpers and managers with explicit roles
- collapse duplicate logic into a single clear owner

### Preserve by default
- HTTP routes and URLs
- request and response field names
- response envelope shape
- status codes and error semantics
- public method signatures used outside the slice
- event names and payload shapes
- queue names and payload shapes
- env var names and documented setup contracts
- externally relied-on database semantics unless an explicit migration plan is part of the task

## `whole-project-preserve-local`
### Use when
- the user wants the entire repository cleaned up
- the repo already has recognizable conventions worth keeping
- the aim is one-author consistency without imposing a foreign naming system

### Main goal
Make the whole repository internally consistent while preserving its local dialect.

### Required behavior
- Inventory the repo's existing naming and layer conventions before changing them.
- Choose one local term for each repeated concept and standardize toward that term.
- Clean duplication, weak abstractions, inconsistent type usage, and naming drift across the repo.
- Keep the repo's own preferred suffixes and folder names when they are stable and understandable.
- Use `alaa-workflow` and stage the work in reviewable phases.

### Allowed changes
- broad mechanical renames that preserve repo-local terminology
- repo-wide DTO, value-object, strict-typing, or error-handling cleanup
- removal of obviously duplicate abstractions
- standardizing one local test style, docblock style, and naming style across modules

### Avoid
- forcing Alaa naming just because it exists
- replacing a stable repo-local convention with a different one unless the user asked for normalization
- hidden contract changes during global cleanup

## `whole-project-normalize-alaa`
### Use when
- the user explicitly wants the repo standardized toward one global Alaa convention set
- the benefit of cross-project uniformity is more important than preserving local naming dialects

### Main goal
Make the whole repository look and behave like an Alaa-style Laravel codebase while preserving external contracts by default.

### Required behavior
- Read `alaa-workflow`, `alaa-laravel-architecture`, and `./consistency-and-naming.md` before broad renames or moves.
- Use the architecture skill's canonical layer flow and naming where it applies.
- Normalize duplicated concepts, generic helpers, manager classes, weak base repositories, raw-array boundaries, and inconsistent naming.
- Prefer explicit DTO boundaries, constructor injection, small focused services, value objects for real concepts, and clear request/resource/policy edges.
- Stage the transformation in reviewable passes and keep the repository runnable after each pass when practical.

### Canonical normalization targets
- Controller -> Service -> Repository -> Resource flow where the architecture skill calls for it
- `FormRequest` for meaningful write validation
- `*Service`, `*Repository`, `*Resource`, `*Policy`, `*Job`, `*Listener` for their real roles
- `*Data` and `*FilterData` for DTO shapes when following the architecture skill
- value objects for domain concepts that should stop traveling as loose strings or arrays
- one canonical business term per concept across the repo

### Allowed changes
- internal class, file, namespace, and method renames across the repo
- module-level folder cleanup to make layer intent obvious
- deleting thin wrappers that merely forward to Eloquent or the container
- replacing vague helpers/managers/processors with explicit services, strategies, or value objects
- codemod-style consistency passes across tests, docs, and docblocks

### Preserve by default
Even in normalization mode, preserve external contracts unless explicitly allowed to change them.

## Public-contract inventory
Before a hard refactor or whole-project pass, inventory the touched contracts:
- HTTP routes, verbs, URLs, request validation, and response shapes
- public identifiers and serialization shape
- events, queues, listeners, and message payloads
- configuration keys and env vars
- cron, CLI, or job entrypoints
- database migration order and externally observed semantics
- docs, Postman examples, and operational runbooks

If a change would break one of these surfaces, either preserve it or make the break explicit and intentional.

## Safe sequencing for whole-project work
Prefer this order:
1. Convention inventory and routing to companion skills
2. Naming and code-shape normalization
3. DTO / value-object / explicit-type cleanup
4. repository and persistence-boundary cleanup where justified
5. controller / request / resource / policy edge cleanup
6. test alignment
7. docs, Postman, diagrams, and final audit

## Anti-patterns
- Choosing a broad mode when a scoped mode would solve the task
- Smuggling breaking changes into a “cleanup”
- Global renames with no contract inventory
- Mixing preserve-local and normalize-to-Alaa goals in an ad hoc way
- Declaring a task complete after only code changes while docs and tests remain stale
