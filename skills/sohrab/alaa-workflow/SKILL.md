---
name: alaa-workflow
description: "Use this when a task is non-trivial or long; create a phase-based plan file (or constrained-mode alternative), minimize terminal verbosity, stay safe in multi-agent same-branch workflows, follow repo guardrails, and end with Persian summary + English conventional commit suggestion."
---

# Purpose
Provide a deterministic workflow for long or multi-step tasks:
- Avoid context overflow.
- Enable safe continuation after restarts (plan as the anchor).
- Reduce merge conflicts in same-branch multi-agent usage.
- Enforce repo guardrails (minimal diffs, Laravel-first, performance/multi-tenant/event-driven correctness).
- Ensure consistent end-of-task reporting (no auto-commit).

# When to use
- Any task that spans multiple files, multiple steps, or involves architecture/ops/docs.
- Any time the user says the task is long, may not fit context, or multiple agents may work in parallel.
- Any change that affects behavior (API, DB, auth, queue/outbox, performance), even if only a few files.

# Instruction precedence (mandatory)
If instructions conflict, follow this order:
1) explicit user constraints for the current task
2) repo `AGENTS.md`
3) this skill
4) general best practices

If a higher-precedence constraint would be violated, do not apply the lower-precedence instruction.
Instead, follow the higher-precedence constraint and document the deviation.

# Repo guardrails (mandatory)

## Before you change anything
1) Find the closest existing pattern in the repo (similar endpoint/service/job/listener).
2) Read conventions:
- module/folder layout (Actions/Services/UseCases, etc.)
- error handling and logging style
- multi-tenancy propagation (headers/middleware/tenant columns/RLS)
- events/outbox/queues (idempotency, retries, ordering)
- tests and fixtures patterns
3) Identify:
- expected public API contract (request/response and error envelope)
- required invariants (tenant boundary, idempotency, ordering, audit needs)
- migration/rollout risks (if DB changes are involved)
4) In Laravel repositories, check whether `laravel/boost` is installed and usable. If it is available, use Boost first for Laravel-aware inspection and documentation lookup before making framework or ecosystem assumptions. If it is unavailable, fall back to local inspection and official documentation.

## Implementation rules
- Minimal-diff: extend existing code paths; avoid rewrites.
- Laravel-first:
    - prefer Form Requests, Policies/Gates, Resources, Jobs, Events, Transactions, Cache
    - keep controllers thin; business logic in Services/Domain Services
- Performance-first:
    - avoid N+1; select only required columns
    - prefer keyset/cursor pagination over OFFSET for large tables
    - cache derived results only with explicit TTL + invalidation strategy
- Multi-tenant correctness:
    - every read/write tenant-scoped
    - never rely on client-supplied tenant_id/project_id without server-side derivation/verification
- Event-driven correctness:
    - jobs/handlers must be idempotent (dedupe key, unique constraints, check-before-insert)
    - prefer outbox/transactional patterns when correctness matters
- OSS/free only by default:
    - do not introduce paid SaaS or proprietary dependencies unless explicitly requested

# Workflow (follow in order)

## 0) Establish a Plan (mandatory)
### Default mode (preferred)
Create or update a plan file:
- Path: `docs/_agent_plans/<YYYYMMDD-HHMMSS>_<slug>.md`

Include these headers (exact):
- `## Goal`
- `## Assumptions`
- `## Constraints`
- `## Closest existing patterns`
- `## Phases (with dependencies)`
- `## Parallel-safe work split`
- `## Commands to run`
- `## Files touched (append-only log)`
- `## Done / Remaining`

### Constrained mode (exception; still required if default mode is forbidden)
If the current task constraints forbid creating new files (read-only / “no new files” / “only one output file allowed”):
- Do NOT create `docs/_agent_plans/*`.
- Instead:
    - write the plan in chat using the same headers, OR
    - embed the plan section at the top of the single allowed output file (if exactly one file is permitted).

## 1) Phase design rules
- Each phase must state:
    - Inputs it depends on (files, decisions, prior phases).
    - Output artifacts (files/sections).
    - Validation (tests/linters/commands).
- Mark phases as:
    - `Parallel-safe` OR `Not parallel-safe`.

## 1.1) Delegated execution mode (optional; only with explicit user authorization)
Enter delegated execution mode only when the user explicitly authorizes subagents or parallel agent work, for example:
- `you can use subagent`
- `delegate this`
- `use parallel agents`
- `split this into subagents`

In delegated mode:
- keep the parent agent as the manager; the parent owns the plan, sequencing, integration, safety checks, and final synthesis
- do not pre-spawn a full team by default; spawn only the roles needed for the current phase or lane
- keep `docs/_agent_plans/<YYYYMMDD-HHMMSS>_<slug>.md` as the source of truth for sequencing and progress
- if a delegated run needs lane-specific detail, either append lane blocks to the same plan file or create child plan files under `docs/_agent_plans/`
- define lane ownership before spawning: scope, inputs, write scope, expected outputs, validation target, and merge notes
- prefer the role pattern `planner/researcher -> implementer -> reviewer` only when the task complexity justifies it
- add a verifier or remediator role only when the task needs an independent validation or remediation pass
- use browser/mobile/devtools validation only when the user explicitly requests it or the task is inherently visual/UI and repo/browser policy allows it
- do not let delegated workers broadly rewrite shared coordination artifacts; follow the shared-state safe-write protocol below

## 2) Minimal terminal verbosity
- Do not paste long outputs.
- Summarize results.
- Redirect huge outputs to a file and point to it.

## 3) User-changing-files safety
- Re-open files before editing when time has passed.
- Prefer small, localized diffs.
- If conflicts appear, stop and propose a safe merge plan.

## 3.1) Shared state safe-write protocol (mandatory in multi-agent runs)
Applies when editing shared coordination artifacts (for example: `.codex/state/*.json`, and plan progress logs in `docs/plan/*` or `docs/_agent_plans/*`).

1) Pre-write re-open + validate
- Re-open the file immediately before writing.
- For JSON state files, validate parse before patch:
  - PowerShell example: `Get-Content -Raw <state_file> | ConvertFrom-Json | Out-Null`
  - Bash example: `jq . <state_file>`

2) Patch scope
- Only edit your lane-owned block(s) and append your own progress line.
- Use minimal patching; do not reformat/reorder unrelated sections.
- Never rewrite a shared state file end-to-end during concurrent work.

3) Post-write verification
- Re-parse JSON state files after writing.
- Check file sanity (non-trivial size, expected timestamp change, no `null`/empty content).

4) Conflict handling
- If parse fails, content is truncated, or unrelated lane sections changed unexpectedly:
  - stop immediately
  - report `CONFLICT BLOCK` with:
    - `file`
    - `issue`
    - `evidence` (command output/timestamp)
    - `impact`
    - `required_unblock`
- Do not continue task execution until unblock is provided.

## 4) End-of-task report (mandatory)
Output in this exact order:
1) `Touched files:` (paths only)
2) `خلاصه فارسی:`
3) `گام بعدی:` (or verification commands)
4) `Suggested commit message:` (English Conventional Commit)

# Anti-patterns
- Dumping terminal logs.
- Auto-commit/push.
- Unscoped multi-tenant access.
- “Just in case” indexes/caches without justification.
- Rewriting shared state files with broad redirection in concurrent runs.
- Updating other lanes’ task blocks in shared state.
