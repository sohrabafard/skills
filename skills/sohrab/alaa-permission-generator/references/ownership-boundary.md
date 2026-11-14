# Ownership boundary — what this skill does not own

Read this file before you state a rule on ground this skill does not own. `SKILL.md`, "Ownership boundary", owns
the rule that the listed owner wins on conflict and the two refinements on signal names and requirements.

| Not owned here | Owner |
| --- | --- |
| Trusted-header assertion, JWT verification, header sanitisation, tenant derivation | `/alaa-trust-gateway-auth` |
| Object-level relations, `can_*`, tuples | `/openfga` |
| Log, metric, event and code **names**; request deadlines; the error envelope | `/alaa-services-contract` |
| Whether a signal is **required**, and its gate | `/alaa-observability-soc` |
| Retry, backoff, circuit-breaking, degradation doctrine | `/alaa-reliability-sla` |
| Complexity budgets, structure choice, the whole N+1 family | `/alaa-algorithms-data-structures` |
| What makes a test a test, and which layer it belongs at | `/alaa-testing-strategy` |
| Design pass when an interface, a data writer, or a consistency, ordering, idempotency, concurrency or caching property changes | `/alaa-system-design` |
| Security review triggers, threat classes, the fail-closed discriminator | `/alaa-security-review` |
| Controlled-operation procedure and proof strength for the apply lanes | `/alaa-controlled-ops` |
| Long-task phasing and resumable state | `/alaa-workflow` |
| The quality bar itself | `alaa-project-constitution references/quality-bar.md` |
| Model choice and reasoning effort | `/alaa-prompting-guide` |
| Per-language validation commands and design-pattern selection | `/alaa-golang`, `/alaa-vue-typescript-clean-code`, `/alaa-mono-package`, `/alaa-laravel-architecture`, `alaa-php-clean-code references/design-patterns.md` |
