# Ownership boundary — what this skill does not own

Read this file before you state a rule on ground this skill does not own: a fleet contract value, retry doctrine, the pagination mechanism, complexity, collection generation, trust semantics, authorization, security, test design, observability, Laravel structure, a design pass, workflow, orchestration, or the quality bar. Where a row names an owner, the owner states the rule and this skill points at it. `SKILL.md`, "Ownership boundary", owns the rule that the owner wins on conflict.

| Not owned here | Owner |
|---|---|
| Envelopes, health and readiness shapes, trusted header names, public identifier forms, event and code names, deprecation windows, and every platform number — timeout, retry count, pool bound | `/alaa-services-contract` |
| Why a caller retries; budgets, backoff, breakers, degradation, error budgets | `/alaa-reliability-sla` |
| Pagination mechanism: ordering, index, predicate, cursor codec, page-size bound, reversal tests | `/alaa-keyset-pagination` |
| Complexity budgets, structure choice, the N+1 family, unbounded result sets | `/alaa-algorithms-data-structures` |
| Collection and environment generation, saved-example and error-coverage completeness, Insomnia portability | `/alaa-postman-collections` |
| Gateway trust boundary, JWT verification, header sanitisation, tenant derivation | `/alaa-trust-gateway-auth` |
| Object-level relationship authorization | `/openfga` |
| Threat classes, review triggers, the fail-closed discriminator | `/alaa-security-review` |
| What makes a test a test, which layer it belongs at, proof levels | `/alaa-testing-strategy` |
| Observability names | `/alaa-services-contract`; requirement levels and gates `/alaa-observability-soc` |
| Laravel structure, PHP naming, design-pattern selection | `/alaa-laravel-architecture`, `/alaa-php-clean-code` and its `references/design-patterns.md` |
| Pre-implementation design once a scope expansion changes an interface, a writer, or what a caller sees when a dependency fails | `/alaa-system-design` |
| Multi-file runs and durable handoff; risky operations and proof strength | `/alaa-workflow`, `/alaa-controlled-ops` |
| Lane planning and subagent roles; model and reasoning-effort choice | `/alaa-cc-orchestrator` (Claude Code), `/alaa-codex-orchestrator` (Codex), `/alaa-prompting-guide` |
| The ten-criterion quality bar; Farsi docs and backlog wording | `alaa-project-constitution references/quality-bar.md`, `/alaa-repo-docs` |
