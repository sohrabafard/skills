# Agent Catalog

The orchestrator is the main thread, not a custom subagent. These custom agents are auto-installed from `agents/*.toml` into `~/.codex/agents`.

## Core execution roles

| Agent | Model | Sandbox | Use | Never use for |
|---|---|---|---|---|
| `alaa-explorer` | Luna / medium | read-only | Repository ownership and execution-path mapping | External/version research or design decisions |
| `alaa-researcher` | Terra / high | read-only | Official docs, versions, standards, third-party contracts | Implementation or final decision-making |
| `alaa-test-strategist` | Terra / high | read-only | High-value test matrix before subtle work | Writing tests or running the final gate |
| `alaa-implementer` | Terra / high | workspace-write | Routine bounded implementation lanes | High-risk architecture or self-review |
| `alaa-implementer-sol` | Sol / high | workspace-write | Architecture/security/concurrency/migration-sensitive lanes | Routine low-judgment edits |
| `alaa-verifier` | Luna / medium | workspace-write artifacts only | Exact commands and reproducible evidence | Fixing, debugging, or changing commands |
| `alaa-failure-analyst` | Terra / high | read-only | Diagnose ambiguous/flaky/environment/cross-lane failures | Applying fixes |
| `alaa-reviewer` | Sol / high | read-only | Independent full-change review | Editing or reassuring |
| `alaa-documenter` | Luna / medium | docs-only write | Verified documentation updates | Executable files or intended behavior |

## Conditional specialist gates

| Agent | Trigger | Gate output |
|---|---|---|
| `alaa-architecture-critic` | Public contracts, boundaries, distributed workflow, consistency, caching, concurrency | `SOUND`, `SOUND-WITH-CONDITIONS`, `REVISE` |
| `alaa-security-reviewer` | Auth, authorization, secrets, untrusted input, uploads, queries, payments, webhooks, crypto | `PASS`, `PASS-WITH-HARDENING`, `BLOCK` |
| `alaa-migration-guardian` | Schema/data changes, backfill, index, cleanup, zero-downtime compatibility | `SAFE`, `SAFE-WITH-CONDITIONS`, `BLOCK` |
| `alaa-browser-qa` | User-visible web flow, frontend regression, navigation/form/visual behavior | `PASS`, `FAIL`, `BLOCKED`, `FLAKY` |
| `alaa-performance-profiler` | Measurable latency/throughput/CPU/memory/query regression | Verdict against declared baseline/budget |
| `alaa-observability-reviewer` | New runtime failure paths, jobs, distributed calls, retries, degraded operation | `PASS`, `PASS-WITH-GAPS`, `BLOCK` |
| `alaa-release-guardian` | CI/CD, Docker, config/env, dependencies, packaging, deploy/release | `READY`, `READY-WITH-CONDITIONS`, `NOT-READY` |

## Model escalation rules

Use Luna for bounded execution/evidence, Terra for normal engineering judgment, and Sol when the lane's correctness depends on deep architecture, security, concurrency, data safety, or independent owner-level judgment.

Do not escalate because a command is slow. The verifier remains Luna while the failure analyst or Sol implementer handles difficult reasoning.
