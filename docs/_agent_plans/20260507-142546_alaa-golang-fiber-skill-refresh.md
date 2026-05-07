# Agent Plan - Alaa Golang Fiber Skill Refresh

- Task ID: `20260507-142546_alaa-golang-fiber-skill-refresh`
- Created: `2026-05-07T10:55:46Z`
- Mode: `execute`
- Status: `completed`
- Plan path: `docs/_agent_plans/20260507-142546_alaa-golang-fiber-skill-refresh.md`
- State path: `.codex/state/20260507-142546_alaa-golang-fiber-skill-refresh.json`

## Goal

### Problem statement

Upgrade `skills/sohrab/alaa-golang` into the main production Go router and create `skills/sohrab/alaa-golang-fiber` as a dedicated Fiber v3 skill. The updated vendored Go inventory has 42 skills while the current route map covers 36.

### In scope now

- Keep `alaa-golang` compact and routing-first.
- Create `alaa-golang-fiber` with Fiber v3 references.
- Route Fiber work from `alaa-golang` into `$alaa-golang-fiber`.
- Add route parity for all 42 vendored Go skills.
- Add production guidance for repository pattern, Redis cache layer, clean Go patterns, TDD, and `99.99%+` service readiness.

### Non-goals / intentionally deferred

- Do not edit `vendor/cc-skills-golang`.
- Do not create `alaa-golang-chi`.
- Do not migrate any real application between chi and Fiber.
- Do not rewrite unrelated Sohrab skills.

### Definition of done

- `alaa-golang` and `alaa-golang-fiber` validate as skills.
- Vendor route audit reports `vendor=42 routed=42 missing=0 extra=0`.
- Framework routing is deterministic: explicit choice wins, existing repo choice wins, raw small services use chi, raw large/high-concurrency services use Fiber.
- Repository pattern, Redis cache safety, clean code, design patterns, TDD, and production readiness are discoverable from references.
- `python scripts/validate_sohrab_skill_pack.py` and `git diff --check` are run, with results recorded.

### Frozen decisions

- `alaa-golang` remains the main entrypoint.
- `alaa-golang-fiber` is created beside `alaa-golang`.
- Chi remains taught inside `alaa-golang`; Fiber is taught inside `alaa-golang-fiber`.
- Redis is a cache layer, not the source of truth.
- Repository pattern is mandatory for DB-backed services.
- TDD is mandatory for behavior-changing Go work.

### Current repository snapshot

- Existing `alaa-golang` has `SKILL.md`, `agents/openai.yaml`, and references for topic map, installed skills, companions, framework choice, chi, package catalog, gap coverage, full guide, and sources.
- Vendored Go skills: 42.
- Routed Go skills: 36.
- Missing routes: `golang-google-wire`, `golang-spf13-cobra`, `golang-spf13-viper`, `golang-swagger`, `golang-uber-dig`, `golang-uber-fx`.

### What is already good

- Existing `alaa-golang` is compact and uses progressive disclosure.
- The chi guide and package catalog already provide useful foundations.
- The route map is machine-checkable through `###` headings.

### Gaps that remain

- Fiber v3 needs a focused skill.
- Framework policy needs the new size-aware rule.
- Route parity needs six new entries.
- Architecture, Redis, clean code, and TDD rules need stronger local references.

### Architecture boundaries and contract surfaces

- This changes skill behavior and documentation only.
- No application runtime code, DB schema, service API, deployment, or env contract changes.

## Assumptions

- Assumption: The current vendored Go inventory remains 42 skills.
  - Status: `verify during execution`
  - Impact: Route audit must be rerun before final validation.
- Assumption: Fiber v3 guidance should live in a separate skill for token efficiency.
  - Status: `frozen`
  - Impact: Create `skills/sohrab/alaa-golang-fiber`.
- Assumption: Existing repo framework choice should not be changed casually.
  - Status: `frozen`
  - Impact: Route to existing chi/Fiber path instead of recommending migration.

## Constraints

- User constraints: use `$skill-creator`, use `$alaa-workflow`, create `alaa-golang-fiber`, keep English simple and fluent.
- Repo / AGENTS constraints: preserve unrelated work, keep changes scoped, validate, suggest a Conventional Commit message when files change.
- Environment / approval constraints: Windows PowerShell; use `apply_patch` for manual edits; no destructive commands.
- Version / rollout constraints: Fiber v3 and Go testing claims should stay source-backed; no vendor edits.

## Closest existing patterns

- `skills/sohrab/alaa-golang/SKILL.md`
  - Why it is relevant: existing Go router surface.
  - What to reuse: compact fast path, routing sections, reference map.
  - What must stay different: Fiber detail moves to `alaa-golang-fiber`.
- `skills/sohrab/alaa-golang/references/31-chi-api-guide.md`
  - Why it is relevant: framework-specific guide style.
  - What to reuse: practical, direct guidance.
  - What must stay different: Fiber guide lives in the new skill.
- `skills/sohrab/alaa-golang/references/10-installed-golang-skills.md`
  - Why it is relevant: semantic route audit target.
  - What to reuse: one `###` heading per routed vendor skill.
  - What must stay different: update to all 42 skills.

## Phases (with dependencies)

### Phase 1 - Workflow artifacts and inventory

- Objective: create plan/state and record current vendor route status.
- Depends on: none.
- Parallel-safe: `yes`
- Exact files / modules to touch: this plan and matching state file.
- Validation commands: `git status --short`; vendor route audit.
- Acceptance criteria: current missing routes recorded.
- Risks / drift watchpoints: vendor subtree may change.
- Completion signal: plan/state created and inventory verified.

### Phase 2 - Create `alaa-golang-fiber`

- Objective: add dedicated Fiber v3 skill.
- Depends on: Phase 1.
- Parallel-safe: `yes`
- Exact files / modules to touch: `skills/sohrab/alaa-golang-fiber/**`.
- Validation commands: targeted skill validation and path checks.
- Acceptance criteria: new skill is self-contained, concise, and source-backed.
- Risks / drift watchpoints: do not overfill `SKILL.md`; use references.
- Completion signal: new Fiber skill files exist.

### Phase 3 - Update `alaa-golang` routing and framework policy

- Objective: route to `$alaa-golang-fiber`, add size-aware framework rules, and reach vendor route parity.
- Depends on: Phase 2.
- Parallel-safe: `no`
- Exact files / modules to touch: `alaa-golang/SKILL.md`, `agents/openai.yaml`, topic map, installed-skill map, framework choice, full guide, sources.
- Validation commands: route audit; search stale chi-first-only wording.
- Acceptance criteria: framework routing is deterministic and route parity is exact.
- Risks / drift watchpoints: no stale GraphQL or Fiber fallback wording.
- Completion signal: `vendor=42 routed=42 missing=0 extra=0`.

### Phase 4 - Add architecture, Redis, clean code, and TDD references

- Objective: add local production rules that vendor Go skills do not own for this stack.
- Depends on: Phase 3.
- Parallel-safe: `yes`
- Exact files / modules to touch: `60-service-architecture-patterns.md`, `61-redis-cache-layer.md`, `62-clean-code-and-patterns.md`, `63-tdd-and-testing-discipline.md`, gap/full/topic references.
- Validation commands: reference path checks; targeted grep for repository, Redis, TDD.
- Acceptance criteria: rules are discoverable and concise.
- Risks / drift watchpoints: avoid duplicating public Go skills too heavily.
- Completion signal: new references are linked from `SKILL.md` or topic map.

### Phase 5 - Validate and update state

- Objective: run required validations and make handoff clear.
- Depends on: all prior phases.
- Parallel-safe: `no`
- Exact files / modules to touch: state file.
- Validation commands: `python scripts/validate_sohrab_skill_pack.py`; `git diff --check`; route audit.
- Acceptance criteria: validation results recorded.
- Risks / drift watchpoints: distinguish unrelated pre-existing failures if any.
- Completion signal: state says completed or records blockers.

## Parallel-safe work split

### Parent agent

- Owns: workflow artifacts, integration, final route policy, validation, final report.
- Integrates: `alaa-golang`, `alaa-golang-fiber`, new references.
- Validates: route parity, skill validation, diff hygiene.

### Lane - Fiber skill

- Scope: create `alaa-golang-fiber`.
- Read scope: official Fiber docs and existing `alaa-golang` HTTP references.
- Write scope: `skills/sohrab/alaa-golang-fiber/**`.
- Depends on: Phase 1.
- Validation target: standalone skill validity.
- Merge notes: parent links it from `alaa-golang`.

### Lane - Router and production references

- Scope: update route map and local production guidance.
- Read scope: existing `alaa-golang` references and vendor skill names.
- Write scope: `skills/sohrab/alaa-golang/**`.
- Depends on: Phase 1.
- Validation target: route audit and path checks.
- Merge notes: parent keeps `SKILL.md` compact.

## Commands to run

### Discovery

```powershell
git status --short
Get-ChildItem vendor\cc-skills-golang\skills -Directory | Select-Object -ExpandProperty Name | Sort-Object
```

### Implementation support

```powershell
rg -n "fiber|Fiber|chi|Redis|repository|TDD|golang-google-wire|golang-spf13|golang-swagger|golang-uber" skills\sohrab\alaa-golang
```

### Validation

```powershell
python scripts\validate_sohrab_skill_pack.py
git diff --check
```

### Recovery / rollback (if relevant)

Use targeted `git diff -- <path>` review and targeted reverse patches only. Do not reset the whole worktree.

## Files touched (append-only log)

- 2026-05-07T10:55:46Z - Created plan file.
- 2026-05-07T10:55:46Z - Created state file.
- 2026-05-07T10:55:46Z - Verified clean worktree and current route gap.
- 2026-05-07T11:17:00Z - Created `skills/sohrab/alaa-golang-fiber` with compact `SKILL.md`, `agents/openai.yaml`, and focused Fiber v3 references.
- 2026-05-07T11:17:00Z - Updated `skills/sohrab/alaa-golang` routing, metadata, framework policy, vendor route map, chi guidance, package catalog, gap coverage, full guide, and sources.
- 2026-05-07T11:17:00Z - Added Go production references for service architecture, Redis cache layer, clean code and patterns, and TDD/testing discipline.
- 2026-05-07T11:17:00Z - Ran validation: both targeted skill validations passed, full Sohrab pack validation passed with existing body-length warnings, route audit reported `vendor=42 routed=42 missing=0 extra=0`, and `git diff --check` passed.
- 2026-05-07T11:17:00Z - Forward-tested `$alaa-golang-fiber` with a read-only subagent scenario for a high-concurrency Fiber/PostgreSQL/Redis API; tightened Fiber references with explicit DB, Redis, readiness, and platform-routing defaults.

## Validation evidence

- `python C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\sohrab\alaa-golang` passed.
- `python C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\sohrab\alaa-golang-fiber` passed.
- `python scripts\validate_sohrab_skill_pack.py` passed with pre-existing body-length warnings in unrelated skills.
- `git diff --check` passed.
- Semantic vendor route audit passed with `vendor=42 routed=42 missing=0 extra=0`.

## Done / Remaining

### Done

- Workflow artifacts created.
- Current vendor route gap verified.
- `alaa-golang-fiber` created as a focused Fiber v3 skill.
- `alaa-golang` updated as the main Go router, chi path, framework decision layer, and production policy entrypoint.
- All 42 vendored Go skills are routed from `references/10-installed-golang-skills.md`.
- Repository pattern, Redis cache-aside, clean Go design rules, TDD, and high-concurrency/SLA guidance are linked and documented.
- Required validation completed.

### Remaining now

- None.

### Deferred intentionally

- Separate chi skill.
- Vendor edits.
- Any real service migration.

### Blocked / waiting

- None.
