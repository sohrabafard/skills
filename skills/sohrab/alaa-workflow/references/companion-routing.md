# Companion Skill Routing

Pair with the narrowest owner for every technical decision. Repository truth and closer instructions override generic skill guidance. Never copy a domain skill's rules into the workflow plan or state.

## Core companions

| Decision | Owner |
|---|---|
| Prompt design, model and effort capability, runtime feature syntax and freshness | `/alaa-prompting-guide`. Add `/openai-docs` for current OpenAI guidance |
| The task model AND effort for every role, review cadence scheduling, and per-goal orchestration of a bounded goal or single phase across parallel role lanes | `/alaa-codex-orchestrator` in Codex, `/alaa-cc-orchestrator` in Claude Code. The workflow plan owns phase gates and records the orchestrator's final report as phase evidence |
| What enters the context window and what gets printed | `/alaa-low-noise`. This skill owns what is written down durably |
| Prior-context recall when its trigger holds, and durable publication after curation | `/alaa-memory-os`. Recall supplies leads to verify against repository truth |
| Reusable-context curation at a signal-bearing phase boundary and before completion | `/alaa-extract-agent-lessons`. This workflow sets the timing and the parking location |
| Which surface answers a code question, and which surfaces a delegated lane may be granted | `/alaa-code-intelligence-routing`. Record what a lane established as a confirmed fact in the handoff package, with the owner that established it, so that the next phase does not repeat the query |
| Codex runtime and harness failures inside WSL/Linux | `/alaa-codex-runtime-ops`. Codex-only |

## Mandatory Ponytail binding

Use /alaa-ponytail for every workflow or orchestrator task unless the user explicitly opts out. Load it before planning. Resolve its level from the skill and from any user selection. Apply it within the existing scope, authority, domain rules, required checks and review cadence.

Bind every child lane explicitly, external specialists included. Pass the exact skill binding and the resolved level, or the user's opt-out and its scope. On resume, redispatch or continuation, recheck the opt-out and the level. An opt-out holds within its stated scope until the user changes it; a recorded binding cannot override it.

Before you continue a child, compare its prior Ponytail assignment with the current one. After an opt-out, tell the child to stop applying the mode. After a new binding or a changed level, send the exact current binding and level. The child applies the update before further work.

## Domain owners

- Frontend: `alaa-frontend-developer` and `alaa-vue-typescript-clean-code`.
- Laravel/PHP: `alaa-laravel-architecture` and `alaa-php-clean-code`.
- Go: `alaa-golang` or the repository's more specific Go skill.
- Public and cross-service contracts: `alaa-services-contract`; use `alaa-trust-gateway-auth` for trust boundaries.
- Queues and jobs: `alaa-async-messaging` or `alaa-laravel-job-rabbitmq`.
- Data: `alaa-data-layer`.
- Subsystem design before a phase implements it: `alaa-system-design`, when its trigger applies. It produces the design record that the later phases implement.
- Test design, execution, resources and result classification: `/alaa-testing-strategy`. Load it before you design implementation or verification. Record only the proof level and tier reached at the evidence owner.
- Security: `alaa-security-review`.
- Observability: `alaa-observability-soc`.
- Containers, Kubernetes and CI/CD: the matching Docker, Kubernetes or pipeline skill.
- Documentation: `alaa-repo-docs` when the document language or the task requires it.

## Executable skill bindings

Map skills before any implementation. A compact plan records its exact bindings in its issue or session. A design may record decision owners without an execution hierarchy.

Before execution or handoff, inventory skills from the active catalog and accessible source. Record each skill in `## Skill Bindings`, with the columns `Skill | Source | Load before | When | If unavailable`:

| Column | Value |
|---|---|
| `Skill` | The exact name from the catalog or the frontmatter |
| `Source` | The readable `SKILL.md` path, or `unavailable` |
| `Load before` | The decision or load point |
| `When` | The observable condition, or `always` when unconditional |
| `If unavailable` | The absence action |

Resolve a relative path from the target repository root or the Markdown plan directory. A consumer plan may use a portable home-relative installed path or a readable absolute POSIX path; verify the source and its frontmatter name. Keep repository-owned paths portable.

In a native plan, put shared rows in the root description and node-specific rows at their node; the closest row wins. Each phase records its exact `Required skills`. Each task or subtask records `Required skills: inherit` from its immediate parent, or a complete override list. In Markdown, keep the phase list, and `[skills: inherit]` or a complete override on each task mapping. When no skill applies, record `none (reason)`. Store names and binding details; never copy a manual.

An unavailable conditional owner records `Source: unavailable` and names its activating condition. When the condition activates, stop that work unless the recorded authorized fallback applies. Ask the user before you install the skill, and never substitute it silently. A missing unconditional owner blocks its work. A draft `NEEDS_FILL` value warns; an unresolved or absent mapping blocks executable work.

Load mapped skills before their recorded decisions on first execution, on resume and on delegated entry: phase bindings, then task overrides, then subtask overrides. Pass the exact skill names, sources, conditions and absence actions to children. Resolve the invocation form for the runtime through `/alaa-prompting-guide`. An empty installed result is unknown until you check its source.
