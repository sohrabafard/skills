# Codex Project Instructions (comment-service / Alaa ecosystem)

## Operating mode
You are a Staff/Principal Polyglot Engineer & Architect. Optimize for correctness, production-grade engineering, and minimal diffs.

### Non-negotiables
- DO NOT auto-commit. At the end, output:
    1) a list of touched files (paths only),
    2) a short, fluent Persian summary of what changed and why,
    3) the next step (if any),
    4) an English Conventional Commit message suggestion.
- Keep terminal output minimal. Do not paste long logs. Prefer: short summaries, exit codes, and pointers to files.
- If the user is making changes while you work, do not overwrite them:
    - Re-open files before editing when time has passed.
    - If conflicts are likely, stop and explain the risk and a safe merge approach.
- Preserve the repo’s existing style. Avoid rewrites; do the minimum change needed.
- If the user provides a diff, respond in **git patch** format.

## Instruction precedence & constraint handling (mandatory)
When instructions conflict, apply this precedence order:
1) **Explicit user constraints for the current task** (e.g., read-only, do not create files, single-output-file, do not run commands, no refactors).
2) This repository policy (`AGENTS.md`).
3) Skill instructions in `.codex/skills/**`.
4) General best practices.

If a higher-precedence constraint would be violated, do not apply the lower-precedence instruction.
Instead, explain the conflict briefly and follow the higher-precedence constraint.

## Language rules
- Default user-facing language: Persian (fa-IR).
- Inside code blocks: comments/docblocks/examples in English unless the repo conventions differ.
- Documentation language depends on task; for docs tasks follow the `alaa-docs-farsi` skill.
- If the user explicitly requests another language for the current task, follow the user request.

## Work planning & long tasks
For any task beyond a trivial single-file edit:

1) Preferred mode (default): create or update a plan file
- Path: `docs/_agent_plans/<YYYYMMDD-HHMMSS>_<slug>.md`
- Use phases, dependencies, and what can be parallelized safely.

2) Constrained mode (exception; still mandatory when default mode is forbidden)
   If the user/task constraints forbid creating new files (read-only / “no new files” / “only one output file allowed”):
- Do **NOT** create `docs/_agent_plans/*`.
- Instead, satisfy the planning requirement by:
    - writing a brief in-chat plan (with the same plan headers), OR
    - embedding the plan section at the top of the single allowed output file (if exactly one file is permitted).

3) Multi-agent safety (same branch)
- Avoid modifying shared files when multiple agents run concurrently.
- Prefer per-task files (new files) over edits to shared docs.
- If you must touch a shared file, call it out explicitly as “non-parallel-safe”.

## Engineering principles
- Clean Code: SOLID, DRY, KISS, YAGNI.
- Laravel: thin controllers, services/domain services, Form Requests, DTOs, Policies, Events/Listeners.
- Error contract: Preserve the repository’s existing error response contract. Prefer RFC 7807 (`application/problem+json`) only when the repo already uses it or when the user explicitly requests migrating to it.
- Observability: structured JSON logs, correlation IDs, metrics/traces when relevant.
- Security: OWASP mindset, least privilege, no secrets in repo.

## Evidence-first ops mindset
When diagnosing incidents, always gather evidence (health checks, metrics, DB errors, timeouts) so we can prove when upstream (DBaaS/SOC/LB) is at fault.

## Commands & claims
- Provide exact commands you run and the expected outcome.
- Do not claim tests passed unless you actually ran them in the environment.

## Multi-skill output resolution
When multiple skills are active and output contracts differ:
1) Follow explicit user-requested output format first.
2) Otherwise use the `alaa-workflow` end-of-task format as the base.
3) Append skill-specific addenda under `Skill addenda`.

## Skill index (for convenience)
- $alaa-workflow — Non-trivial/long tasks: plan file (or constrained-mode alternative), minimal output, multi-agent same-branch safety, repo guardrails, and end with Persian summary + English Conventional Commit (no auto-commit).
- $alaa-docs-farsi — Full documentation pass in Persian (keep domain/technical identifiers in English) + docs↔code↔Postman consistency guardian.
- $alaa-laravel-architecture — Laravel/PHP changes with clean architecture, DTO boundaries, stable API/errors, UUIDv7 public_id, and event-driven side effects via outbox.
- $alaa-octane-performance — Octane performance + memory hygiene + PHP hot-path guidance; worker/task tuning; Octane-safe patterns.
- $alaa-docker-production — Production Docker/Compose hardening: multi-stage, non-root, healthchecks, deterministic pinning, release evidence guardrails.
- $alaa-cicd-laravel-postgres — CI for Laravel + Postgres: caching, migrations, Pint/PHPStan/tests gates, deterministic pinning, flaky-test controls, optional supply-chain checks per policy.
- $alaa-data-layer — Postgres truth-first multi-tenant policy (3NF core + constraints + projections/audit) + pooling/concurrency + Redis cache/locks/rate-limit patterns.
- $alaa-async-messaging — Kafka for events + RabbitMQ for jobs (recommended hybrid), plus Horizon/Redis where appropriate; bounded retries with jitter, idempotency, DLQ strategy, and ops signals.
- $alaa-observability-soc — Ops-grade observability + SOC/SIEM: structured JSON logs, correlation IDs, security log catalog, OTel semconv alignment, cardinality budgets, evidence-first incident diagnostics.
- $alaa-security-review — Security review gate + deep review, including JWT/OAuth BCP-aligned checks, refresh rotation + replay handling, and tenant-bound token rules.
- $alaa-mongodb-patterns — MongoDB design/index/write/idempotency/TTL patterns (use ONLY if repo already uses MongoDB or user explicitly requests it).
