# Companion Skill Routing

`alaa-workflow` owns workflow admission, hierarchy, plan and checkpoint continuity, delegation boundaries and handoff. The mirrored runtime orchestrators own review cadence scheduling. Pair with the narrowest owner for every technical decision.

## Core companions

- Prompt design, supported model/effort capabilities and source guidance, runtime feature syntax, and freshness: `/alaa-prompting-guide`. It owns capability and trigger-syntax evidence; actual task allocation belongs to the runtime orchestrator; add `/openai-docs` for current OpenAI guidance.
- Actual task model AND effort allocation for every role and per-goal orchestration: `/alaa-codex-orchestrator` in Codex, `/alaa-cc-orchestrator` in Claude Code — a bounded goal or single phase across parallel role lanes. The workflow plan owns phase gates and records the orchestrator's final report as phase evidence.
- Context economy and output discipline: `/alaa-low-noise`. It owns both what enters the context window and what gets printed. This skill owns what gets written down durably; the two are complementary and neither substitutes for the other.
- Prior-context recall when `/alaa-memory-os`'s trigger holds, and durable publication after curation: `/alaa-memory-os`. Recall supplies leads that must be verified against repository truth; this workflow still owns active plans, checkpoints, evidence, and handoffs.
- Reusable-context curation at signal-bearing phase boundaries and before completion: `/alaa-extract-agent-lessons`. It owns admission and the decision-interface, judgment-rubric, and knowledge-card shapes. This workflow owns the intermediate handoff location and the final lifecycle gate; `/alaa-memory-os` owns durable publication.
- Which surface answers a phase's code question — a code graph, a semantic language server, a framework MCP, or plain read and search — and which of those a delegated lane may be granted: `/alaa-code-intelligence-routing`. Invoke it before the first non-trivial code-evidence choice and consume that result instead of retrieving the same fact twice. Record what a lane established as a confirmed fact in the handoff package, with the owner that established it, so the next phase consumes it instead of re-running the query.
- Codex runtime and harness failures inside WSL/Linux: `/alaa-codex-runtime-ops`. Codex-only, with no Claude Code equivalent.

## Optional Ponytail binding

When the current task invokes or retains active /alaa-ponytail, resolve its level and stop state from the skill before planning. Apply it within existing scope, authority, domain rules, required checks and review cadence.

Map it only to work where the active mode applies. Pass the exact skill binding and resolved level in the dispatch only for child lanes explicitly assigned that mode. On resume or redispatch, recheck activation before using any recorded binding. A recorded binding alone cannot activate the mode.

## Domain owners

- Frontend: `alaa-frontend-developer` and `alaa-vue-typescript-clean-code`.
- Laravel/PHP: `alaa-laravel-architecture` and `alaa-php-clean-code`.
- Go: `alaa-golang` or the repository's more specific Go skill.
- Public and cross-service contracts: `alaa-services-contract`; use `alaa-trust-gateway-auth` for trust boundaries.
- Queues and jobs: `alaa-async-messaging` or `alaa-laravel-job-rabbitmq`.
- Data: `alaa-data-layer`.
- Subsystem design before a phase implements it: `alaa-system-design`. Route a phase there first when the phase changes an interface another component calls, moves which component writes a piece of data, alters a consistency, ordering or caching property, adds or removes a dependency between components, or creates a new deployable unit. It produces the design record the later phases implement.
- Before designing implementation or verification, load `/alaa-testing-strategy`. It owns test necessity, layers, doubles, selectors and proof. Before planning or running checks read its `references/100-test-execution.md`; before resources or timing, its `references/110-execution-resources.md`; before result classification or diagnosis, its `references/120-result-classification.md`. Record only the level and tier reached at the evidence owner.
- Security: `alaa-security-review`.
- Observability: `alaa-observability-soc`.
- Containers, Kubernetes, and CI/CD: the matching Docker, Kubernetes, or pipeline skill.
- Documentation: `alaa-repo-docs` when the document language or task requires it.

Repository truth and closer instructions override generic skill guidance. Do not duplicate a domain skill's rules in the workflow plan or state.

## Executable skill bindings

Map skills before any implementation. A compact plan records its exact bindings in its issue or session. Design may record decision owners without an execution hierarchy.

Before execution or handoff, inventory skills from the active catalog and accessible source. Use `Skill | Source | Load before | When | If unavailable` in `## Skill Bindings`. Record the exact catalog/frontmatter name, readable `SKILL.md` path, decision or load point, observable condition (`always` when unconditional), and absence action. Resolve relative paths from the target repository root or Markdown plan directory. Consumer plans may use portable home-relative installed paths or a readable absolute POSIX path. Expand home and verify source/frontmatter. Keep repository-owned paths portable.

In a native plan, put shared rows in the root description and node-specific rows at their node. Each phase records its exact `Required skills`. Each task or subtask records `Required skills: inherit` from its immediate parent or a complete override list. Resolve each selected name to its applicable binding row; the closest row wins. For Markdown, keep the phase list and `[skills: inherit]` or complete override on each task mapping. If no skill applies, record `none (reason)`. Store names and binding details without copying manuals.

An unavailable conditional owner records `Source: unavailable` in its table cell and names the condition that activates it; stop that work when it activates unless the recorded authorized fallback applies. Never install or silently substitute it. A missing unconditional owner blocks its work. Draft `NEEDS_FILL` values remain visible warnings; unresolved or absent mappings block executable work. Existing active execution plans add these fields before continuing; completed legacy history remains readable without migration.

Load mapped skills before their recorded decisions on first execution, resume, and delegated entry. Read phase bindings, task overrides and then subtask overrides under the hierarchy contract; pass exact skill names, sources, conditions, and absence actions to children. Resolve runtime-correct invocation through `/alaa-prompting-guide`; an empty installed result is unknown until its source is checked.
