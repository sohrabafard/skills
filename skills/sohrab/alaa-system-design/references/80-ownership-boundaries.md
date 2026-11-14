# Ownership Boundaries

`SKILL.md` *What this skill does not own* owns the conflict rule. This file names the owner of each ground below.

| Not owned here | Owner |
|---|---|
| Project policy, archetype and quality-bar obligations, and the intent model and counterfactuals that `SKILL.md` *What this skill consumes* reads | `/alaa-project-constitution` |
| Envelopes, correlation and trusted gateway headers, the public identifier boundary, the trust boundary, event, code and permission names, and the deprecation procedure | `/alaa-services-contract` |
| Every Ala timeout, retry, pool, acquire-wait, and shed value, with the wire behaviour carrying it | `/alaa-services-contract`'s `references/22-failure-load-and-deprecation-contract.md` |
| Failure doctrine: gate-versus-contributor discrimination, deadlines, retries, breakers, bulkheads, admission and shedding, degradation, idempotency, error budgets, and their evidence | `/alaa-reliability-sla` |
| Trust-boundary review, authn and authz decisions, tenant isolation, fail-closed doctrine, every security verdict | `/alaa-security-review` |
| Signal selection, instrumentation requirement levels, cardinality and sampling budgets, alerting, retention, SOC evidence | `/alaa-observability-soc` |
| Schema, constraints, indexes, migrations, isolation semantics, pooling mechanics, projections, Redis behaviour | `/alaa-data-layer` |
| Broker prefetch, acknowledgement, consumer concurrency, dead-letter mechanics | `/alaa-async-messaging` |
| Dispatch, task model and effort allocation, review and commit cadence, and the `alaa-architecture-critic` role and verdicts | `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` |
| Plan files, resumable state, and phase prompt packs for a design spanning sessions | `/alaa-workflow` |
| What proves a design's behaviour: the layer a behaviour is tested at, whether a double is honest, the six proof levels, and what evidence a review accepts | `/alaa-testing-strategy` |
| The complexity budget on a path this design creates, the real bound on a growing input dimension, structure choice from the access pattern, and the N+1 family | `/alaa-algorithms-data-structures` |
| Language idiom, patterns, and refactoring inside a component | the per-language clean-code skills, named per stack |
| Model and effort capability evidence, prompting, and skill or agent authoring | `/alaa-prompting-guide` |
