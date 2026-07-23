# Companion Skill Routing

`alaa-workflow` owns workflow admission, plan/state continuity, delegation boundaries, handoff, and review cadence. Pair it with the narrowest owner for technical decisions.

- Prompt design and runtime freshness: `$alaa-prompting-guide`; add `$openai-docs` for current OpenAI guidance.
- Per-goal multi-model role orchestration: `$alaa-codex-orchestrator` (Codex) or `$alaa-cc-orchestrator` (Claude Code) for a bounded goal or single phase with parallel implementer/reviewer/documenter lanes; the workflow plan stays authoritative.
- Output discipline: `$alaa-low-noise`.
- Frontend: `$alaa-frontend-developer` and `$alaa-vue-typescript-clean-code`.
- Laravel/PHP: `$alaa-laravel-architecture` and `$alaa-php-clean-code`.
- Go: `$alaa-golang` or the repository's more specific Go skill.
- Public and cross-service contracts: `$alaa-services-contract`; use `$alaa-trust-gateway-auth` for trust boundaries.
- Queues and jobs: `$alaa-async-messaging` or `$alaa-laravel-job-rabbitmq`.
- Data: `$alaa-data-layer`.
- Security: `$alaa-security-review`.
- Observability: `$alaa-observability-soc`.
- Containers, Kubernetes, and CI/CD: use the matching Docker, Kubernetes, or pipeline skill.
- Documentation: `$alaa-docs-farsi` when the document language or task requires it.
- Windows/Codex harness failures: `$alaa-codex-runtime-ops`.

Repository truth and closer instructions override generic skill guidance. Do not duplicate a domain skill's rules in the workflow plan or state.
