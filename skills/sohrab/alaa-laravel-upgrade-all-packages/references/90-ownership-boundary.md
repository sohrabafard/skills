# Ownership Boundary

This skill owns four things: recovery of a dependency change, the baseline that makes a "pre-existing" failure claim checkable, the mapping from an audit finding to an action inside a sweep, and the record of what shipped and how it fails. Every other question a sweep raises has an owner below, and on disagreement the owner wins. The ten-criterion quality bar itself is `alaa-project-constitution references/quality-bar.md`, restated nowhere here.

## The criteria

| Criterion | Owner |
|---|---|
| Correctness and testability | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Failure behaviour | doctrine `/alaa-reliability-sla` (`$alaa-reliability-sla`); every number `alaa-services-contract references/22-failure-load-and-deprecation-contract.md` |
| Security | `/alaa-security-review` (`$alaa-security-review`); tenant derivation and trusted headers `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); object-level relationship authorization `/openfga` (`$openfga`) |
| Observability | requirement levels and gates `/alaa-observability-soc` (`$alaa-observability-soc`); every field, metric, event and code name `/alaa-services-contract` (`$alaa-services-contract`) |
| Concurrency and load | workers, pools, cache tiers `/alaa-octane-performance` (`$alaa-octane-performance`); query, index and Redis semantics `/alaa-data-layer` (`$alaa-data-layer`), including the repository-pattern gate at `alaa-data-layer references/50-redis-laravel-octane.md` "Step 0" |
| Clean code, SOLID, design-pattern selection | `/alaa-php-clean-code` (`$alaa-php-clean-code`) `references/design-patterns.md` |
| Algorithms and data structures, N+1 included | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Configurability | `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) `references/70-config-contract.md`; contract values `/alaa-services-contract` (`$alaa-services-contract`) |
| Speed of development and debuggability | plan, phasing, state, resume `/alaa-workflow` (`$alaa-workflow`); output shape `/alaa-low-noise` (`$alaa-low-noise`); lane planning and delegation `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator`) |
| Documentation | service and API artifacts `/alaa-repo-docs` (`$alaa-repo-docs`), `/alaa-postman-collections` (`$alaa-postman-collections`) |

## Other surfaces

- Pre-implementation design, when a bump changes an interface shape; a consistency, ordering, idempotency, concurrency or caching property; a dependency between components; or what a caller sees when a dependency is degraded -- `/alaa-system-design` (`$alaa-system-design`).
- Risky-operation gating, the proof-strength vocabulary every gate here names, and ControlledOps release, tagging and Satis -- `/alaa-controlled-ops` (`$alaa-controlled-ops`) `references/40-validation-and-release-gates.md`.
- Local runtime bring-up for an in-runtime or live-dependency proof -- `/service-runtime-kit-governance` (`$service-runtime-kit-governance`).
- Image build, registry and digest mechanics for a revert target -- `/alaa-docker-production` (`$alaa-docker-production`).
- Pipeline stages and release gates in CI -- `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`), GitLab specifics `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).
- Frontend build and delivery when the build ships -- `/alaa-frontend-devops` (`$alaa-frontend-devops`).
- Windows sandbox recovery, locked files, path discipline -- `/alaa-codex-runtime-ops` (`$alaa-codex-runtime-ops`).
- Runtime names, model names, effort levels, feature and skill-trigger syntax -- `/alaa-prompting-guide` (`$alaa-prompting-guide`) `references/50-effort-and-thinking.md`. No model name appears anywhere in this skill.

## `vendor/` is never edited

Everything under `vendor/` is an upstream tree, replaced by the next install and, for vendored skills, re-pulled from upstream, so a local edit is either overwritten or collides. When a bump requires different behaviour from a vendored package, wrap it from the owning `alaa-*` skill: a wrapper survives the next upgrade, a patch does not. Where a sweep cannot proceed without an upstream change, record the blocker per `40-failure-classes.md` class 1 and report it.

## Three skills this repository does not own

A production Laravel service repository ships its own agent skills at `.agents/skills/`: `laravel-best-practices/` -- broad framework idiom, deeper than ours on subqueries, indexes, queue retry mechanics, HTTP-client timeouts, migration hygiene, scheduling flags and error-reporting plumbing, and entirely unaware of Octane -- plus `octane-development/` and `pest-testing/` (Pest syntax, datasets, browser and arch tests, runner flags). An agent working in that repository loads them alongside these, and they can be re-pulled, reworded or removed between runs.

Route to them for mechanics: Pest invocation syntax for the baseline and verification runs, framework idiom for a code change a bump forces. Never let an upstream file be the sole place a safety-critical invariant is stated -- where a rule protects cross-request state, tenant isolation or an authorization decision, the `alaa-*` skill states it outright and wins on conflict.

Two upstream rules actively wrong for these services, the `once()` memoization section in `rules/caching.md` and the tenant-from-client-header example in `rules/architecture.md`, are overridden by name in `50-runtime-verification.md`. A third is overridden here: `rules/style.md` forbids comments outside config files, which would strip the invariant docblocks and test-intent comments these skills require. Comment discipline comes from `/alaa-php-clean-code` (`$alaa-php-clean-code`) `references/documentation-and-artifacts.md`.
