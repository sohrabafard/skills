# Evidence register

Retrieved/reviewed: 2026-11-02. Model-routing recommendations in this package are our engineering hypotheses, not OpenAI per-language benchmark results. URLs can change. For implementation, verify the installed framework/runtime version.

## O1 — OpenAI Model selection
https://developers.openai.com/api/docs/guides/model-selection

Use: Terra is explicitly mentioned for scoped code fixes; general model/effort guidance.

## O2 — GPT-6.1 Terra
https://developers.openai.com/api/docs/models/gpt-6.1-terra

Use: Visual/computer-use/writing positioning, model ID, reasoning settings and price.

## O3 — GPT-6.1 Sol
https://developers.openai.com/api/docs/models/gpt-6.1-sol

Use: Complex coding positioning, model ID, reasoning settings and price.

## O4 — GPT-6 Astra
https://developers.openai.com/api/docs/models/gpt-6-astra

Use: Most demanding reasoning/coding positioning, settings and price.

## O5 — GPT-6 Luna
https://developers.openai.com/api/docs/models/gpt-6-luna

Use: Focused high-volume tasks, settings and price.

## O6 — Code generation
https://developers.openai.com/api/docs/guides/code-generation

Use: Codex general-purpose model guidance and API coding recommendation.

## O7 — Using GPT-6
https://developers.openai.com/api/docs/guides/latest-model

Use: Family positioning and model/effort distinction.

## O8 — Subagents
https://learn.chatgpt.com/docs/agent-configuration/subagents

Use: Standalone custom-agent TOML schema, delegation, permissions inheritance.

## O9 — Configuration reference
https://learn.chatgpt.com/docs/config-file/config-reference

Use: Current config key names and agent concurrency controls.

## O10 — Evaluation best practices
https://developers.openai.com/api/docs/guides/evaluation-best-practices

Use: Task-specific empirical evaluation; this package uses no hosted Evals dependency.

## O11 — Reasoning models
https://developers.openai.com/api/docs/guides/reasoning

Use: Reasoning effort is model-dependent; increased effort requires evaluation.

## T1 — Laravel 12 Octane
https://laravel.com/docs/12.x/octane

Use: Long-lived workers, dependency injection and request state.

## T2 — Vue SSR
https://vuejs.org/guide/scaling-up/ssr

Use: Cross-request state pollution and SSR concerns.

## T3 — RabbitMQ confirms
https://www.rabbitmq.com/docs/confirms

Use: Publisher confirms and consumer acknowledgements are separate.

## T4 — Vector remap
https://vector.dev/docs/reference/configuration/transforms/remap/

Use: Vector transformation uses VRL.

## T5 — PostgreSQL 18 EXPLAIN
https://www.postgresql.org/docs/18/sql-explain.html

Use: EXPLAIN ANALYZE executes statements.

## T6 — Redis distributed locks
https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/

Use: Lock and failover assumptions require explicit treatment.

## T7 — Go race detector
https://go.dev/doc/articles/race_detector

Use: Race detection is a useful runtime check, limited to executed paths.

## T8 — ClickHouse merge behavior
https://clickhouse.com/resources/engineering/clickhouse-optimize-table-final

Use: Background deduplication and query-time correctness differ.
