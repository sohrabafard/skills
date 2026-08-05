# Companion Skill Routing

`alaa-workflow` owns workflow admission, plan and checkpoint continuity, delegation boundaries, handoff, and review cadence. Pair it with the narrowest owner for every technical decision. This file says which skill owns which decision and nothing more.

Triggers are runtime-specific: `/name` in Claude Code, `$name` in Codex. Both forms exist for every skill below except where a line marks one runtime-specific.

## Core companions

- Prompt design, model and effort selection, runtime feature syntax, and freshness: `$alaa-prompting-guide` / `/alaa-prompting-guide`. It owns every model name, effort level, and trigger-syntax question this skill defers on; add `$openai-docs` / `/openai-docs` for current OpenAI guidance.
- Per-goal multi-model role orchestration: `$alaa-codex-orchestrator` in Codex, `/alaa-cc-orchestrator` in Claude Code — a bounded goal or a single phase executed across parallel role lanes. The workflow plan stays authoritative and records the orchestrator's final report as phase evidence.
- Context economy and output discipline: `$alaa-low-noise` / `/alaa-low-noise`. It owns both what enters the context window and what gets printed. This skill owns what gets written down durably; the two are complementary and neither substitutes for the other.
- Reusable-context curation at signal-bearing phase boundaries and before completion: `$alaa-extract-agent-lessons` / `/alaa-extract-agent-lessons`. It owns admission and the decision-interface, judgment-rubric, and knowledge-card shapes. This workflow owns the intermediate handoff location and the final lifecycle gate; `$alaa-memory-os` / `/alaa-memory-os` owns durable publication.
- Which surface answers a phase's code question — a code graph, a semantic language server, a framework MCP, or plain read and search — and which of those a delegated lane may be granted: `$alaa-code-intelligence-routing` / `/alaa-code-intelligence-routing`. It also owns preventing the same fact from being retrieved twice. Record what a lane established as a confirmed fact in the handoff package, with the owner that established it, so the next phase consumes it instead of re-running the query.
- Codex runtime and harness failures on Windows: `$alaa-codex-runtime-ops`. Codex-only, with no Claude Code equivalent.

## Domain owners

- Frontend: `alaa-frontend-developer` and `alaa-vue-typescript-clean-code`.
- Laravel/PHP: `alaa-laravel-architecture` and `alaa-php-clean-code`.
- Go: `alaa-golang` or the repository's more specific Go skill.
- Public and cross-service contracts: `alaa-services-contract`; use `alaa-trust-gateway-auth` for trust boundaries.
- Queues and jobs: `alaa-async-messaging` or `alaa-laravel-job-rabbitmq`.
- Data: `alaa-data-layer`.
- Subsystem design before a phase implements it: `alaa-system-design`. Route a phase there first when the phase changes an interface another component calls, moves which component writes a piece of data, alters a consistency, ordering or caching property, adds or removes a dependency between components, or creates a new deployable unit. It produces the design record the later phases implement.
- What a phase's tests must prove and at which strength: `alaa-testing-strategy`. Route there when deciding which layer a behaviour is tested at, whether a double is honest, which of six proof levels a phase's validation evidence actually reached, or which scope tier a phase has earned — the plan records the level and the tier reached, never a stronger one, and cites an unchanged earlier result rather than re-running it.
- Security: `alaa-security-review`.
- Observability: `alaa-observability-soc`.
- Containers, Kubernetes, and CI/CD: the matching Docker, Kubernetes, or pipeline skill.
- Documentation: `alaa-repo-docs` when the document language or task requires it.

Repository truth and closer instructions override generic skill guidance. Do not duplicate a domain skill's rules in the workflow plan or state.
