# Agent Plan - Sohrab GPT-5.5 skill pack upgrade

- Task ID: `20260424-000739_sohrab-gpt55-skill-pack-upgrade`
- Created: `2026-04-23T20:37:39Z`
- Mode: `execute`
- Status: `completed`
- Plan path: `docs/_agent_plans/20260424-000739_sohrab-gpt55-skill-pack-upgrade.md`
- State path: `.codex/state/20260424-000739_sohrab-gpt55-skill-pack-upgrade.json`

## Goal

### Problem statement

Upgrade all 55 skills under `skills/sohrab` into a professional GPT-5.5-ready skill pack without losing existing domain behavior.

The pack is already mostly routing-first, but the current validator fails because of missing canonical `When NOT to use` headings, short `agents/openai.yaml` descriptions, and false positives where target-repo paths are treated as bundled skill resources. Several dense generator/validator skills are high-risk because a previous broad cleanup over-normalized them and removed required workflow detail.

### In scope now

- Use `$skill-creator` as the governing method in every phase.
- Create durable workflow state for resume, validation, and subagent coordination.
- Harden `scripts/validate_sohrab_skill_pack.py`.
- Normalize metadata, canonical non-use headings, source maps, model-policy wording, examples, anti-patterns, and reference navigation.
- Refresh current-knowledge pointers from official and primary sources first.
- Use subagents with disjoint write scopes for large independent lanes.

### Non-goals / intentionally deferred

- Do not install, unlink, or remove global skills from `C:\Users\CIT\.codex\skills`.
- Do not modify vendored upstream skill packs directly except through a deliberate subtree workflow.
- Do not touch pre-existing untracked archives unless explicitly scoped.
- Do not invent GPT-5.5-specific skill syntax or unverified model capabilities.

### Definition of done

- `python scripts\validate_sohrab_skill_pack.py` passes or reports only documented intentional warnings.
- `python -X utf8 C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill-dir>` passes for every changed skill.
- `git diff --check` passes.
- Changed high-risk skills have routing/forward-test evidence or recorded residual risk.
- Plan/state files list touched files, validations, remaining work, and handoff state.

### Frozen decisions

- GPT-5.5 is the preferred main model for high-risk skill authoring and review when available; fallback to GPT-5.4 must be recorded.
- `SKILL.md` stays a compact decision layer; detailed examples and source knowledge live in one-hop `references/`.
- StackOverflow/community material is troubleshooting/discovery only, never normative contract policy.
- Existing dense workflows must be preserved unless they are fully moved into references and linked back.

### Current repository snapshot

- Current untracked files before this task: `skills/sohrab/alaa-observability-soc.zip`, `skills/sohrab/alaa-signoz-clickhouse-docs/`, `skills/sohrab/signoz.tar`.
- Current validator exits `1` with heading, metadata, and path-reference failures.
- `agents/openai.yaml` exists for all inspected skills.
- Existing evaluation assets live under `docs/skill-evals/`.

### What is already good

- The pack README already defines routing-first design rules.
- Many Ala skills already use `references/00-topic-map.md`, split references, and compact top-level workflows.
- `alaa-golang`, `alaa-haproxy`, `alaa-shaka-player`, `clickhouse-performance-schema-ops`, and `vector-rust-observability-pipelines` already show good source-map patterns.
- The pack already has a custom validator and evaluation datasets.

### Gaps that remain

- Validator cannot distinguish target-repo example paths from bundled resource paths.
- Several skills miss canonical `## When NOT to use` headings.
- Some `short_description` fields are shorter than the pack validator requires.
- GPT-5.4-era wording exists in a few references and must be updated conservatively.
- Many skills lack explicit source-priority maps or freshness triggers.
- Dense generator/validator skills need surgical preservation while improving routing and references.

### Architecture boundaries and contract surfaces

- Skill identity boundary: folder name, frontmatter `name`, `agents/openai.yaml` default prompt.
- Trigger boundary: frontmatter `description` and `agents/openai.yaml`.
- Knowledge boundary: top-level `SKILL.md` vs one-hop references.
- Validator boundary: bundled skill resources vs target repository example paths.
- Pack routing boundary: `skills/sohrab/README.md` and companion routing references.

## Assumptions

- Assumption: official OpenAI/Codex and Agent Skills guidance remains the authority for skill structure.
  - Status: `frozen`
  - Impact: avoid custom GPT-5.5 skill formats.
- Assumption: version-sensitive source claims need live verification during each lane.
  - Status: `verify during execution`
  - Impact: browse official docs or primary sources before changing latest/version guidance.
- Assumption: dense line-count warnings may be acceptable when they preserve mandatory workflows.
  - Status: `frozen`
  - Impact: do not force every skill under the soft target at the cost of behavior.

## Constraints

- User constraints: implement the proposed plan exactly; use subagents; use `$skill-creator`; keep work resumable.
- Repo / AGENTS constraints: English responses and artifacts, small reviewable changes, no unrelated reverts, validate before completion.
- Environment / approval constraints: workspace-write; do not perform destructive operations; use `python -X utf8` for Windows validation when needed.
- Version / rollout constraints: no unverified GPT-5.5 capability claims; current knowledge must be source-backed.

## Closest existing patterns

- `skills/sohrab/README.md`
  - Why it is relevant: pack-level routing map and definition of done.
  - What to reuse: routing-first language and active skill map.
  - What must stay different: this plan is execution state, not user-facing catalog text.
- `skills/sohrab/alaa-golang/`
  - Why it is relevant: routing-first wrapper with source map and vendor routing checks.
  - What to reuse: source-map layout, model/version caution, semantic routing validation.
  - What must stay different: do not copy Go-specific guidance into other skills.
- `scripts/validate_sohrab_skill_pack.py`
  - Why it is relevant: pack-wide structural gate.
  - What to reuse: existing identity, metadata, heading, and topic-map checks.
  - What must stay different: path checking must distinguish bundled resources from target-repo examples.
- `docs/skill-evals/`
  - Why it is relevant: existing prompt datasets and review rubrics.
  - What to reuse: manual review and routing evaluation shape.
  - What must stay different: forward-tests must use fresh prompts and raw artifacts where possible.

## Phases (with dependencies)

### Phase 0 - Bootstrap workflow state

- Objective: create durable plan/state artifacts and baseline snapshot.
- Depends on: current repository inspection.
- Parallel-safe: `no`
- Exact files / modules to touch:
  - `docs/_agent_plans/20260424-000739_sohrab-gpt55-skill-pack-upgrade.md`
  - `.codex/state/20260424-000739_sohrab-gpt55-skill-pack-upgrade.json`
  - `docs/agents/sohrab-gpt55-skill-pack-upgrade-state.md`
- Validation commands: `git status --short`, `python scripts\validate_sohrab_skill_pack.py`
- Acceptance criteria: artifacts exist and list all phases, lanes, validators, and non-goals.
- Risks / drift watchpoints: overwriting prior state or losing the initial validator baseline.
- Completion signal: state file marks Phase 0 complete.

### Phase 1 - Validator hardening and baseline metadata

- Objective: fix structural noise before content rewrites.
- Depends on: Phase 0.
- Parallel-safe: `yes`, with disjoint scopes.
- Exact files / modules to touch:
  - `scripts/validate_sohrab_skill_pack.py`
  - affected `SKILL.md` files missing canonical non-use headings
  - affected `agents/openai.yaml` files with short descriptions below 25 chars
- Validation commands:
  - `python -m py_compile scripts\validate_sohrab_skill_pack.py`
  - `python scripts\validate_sohrab_skill_pack.py`
  - targeted `quick_validate.py`
- Acceptance criteria: validator failures are real/actionable, not target-repo path false positives.
- Risks / drift watchpoints: validator must not hide real missing bundled resource links.
- Completion signal: Phase 1 validation result recorded.

### Phase 2 - GPT-5.5 skill authoring standard rollout

- Objective: replace GPT-5.4-era wording with conservative GPT-5.5-ready workflow policy.
- Depends on: Phase 1.
- Parallel-safe: `yes`, after source-backed review.
- Exact files / modules to touch:
  - `alaa-workflow`
  - `alaa-php-clean-code`
  - `alaa-docs-farsi`
  - dense generator/validator skills when they mention model policy
- Validation commands:
  - `rg -n "gpt-5\.4|GPT-5\.4|gpt-5\.5|GPT-5\.5|reasoning_effort|model_reasoning" skills\sohrab`
  - targeted `quick_validate.py`
- Acceptance criteria: no unverified GPT-5.5-only claims; fallback and validation discipline remain explicit.
- Risks / drift watchpoints: changing model wording without current official support.
- Completion signal: model-policy diff reviewed and recorded.

### Phase 3 - Source maps and current-knowledge refresh

- Objective: add or refresh official-source and primary-source maps without bloating `SKILL.md`.
- Depends on: Phase 1; Phase 2 can run before or alongside for unrelated files.
- Parallel-safe: `yes`, by domain lane.
- Active worker lanes:
  - Core contracts: `019dbc1e-b43a-75a3-9ae1-8d8f27e066fc`
  - PHP/Laravel: `019dbc1e-b477-70f0-9573-333655ba6840`
  - Frontend/media: `019dbc1e-b4cf-7973-aa61-cf748aeb38cb`
  - Platform delivery: `019dbc1e-b522-71e3-8bc1-97c43c30cb9e`
  - CI/IaC/observability: `019dbc1e-b580-7bc1-bb22-a59334258880`
- Exact files / modules to touch: lane-owned `references/SOURCES.md`, `references/source-map.md`, `references/OFFICIAL_LINKS.md`, or existing equivalents.
- Validation commands: targeted `quick_validate.py`, `rg` checks for stale/latest wording.
- Acceptance criteria: every changed group has source priority and freshness triggers.
- Risks / drift watchpoints: community sources must not become normative.
- Completion signal: lane source-map summary recorded.

### Phase 4 - Domain-bounded skill enrichment

- Objective: enrich each skill within its own topic using examples, anti-patterns, decision tables, and reference routing.
- Depends on: Phases 1 and 3 for the same lane.
- Parallel-safe: `yes`, by disjoint skill folder.
- Exact files / modules to touch: lane-owned skill folders only.
- Validation commands: targeted `quick_validate.py`, pack validator after each lane group.
- Acceptance criteria: `SKILL.md` remains a compact decision layer; examples live in references where long.
- Risks / drift watchpoints: no cross-skill policy theft or generic super-skill merging.
- Completion signal: lane handoff lists touched files and validation.

### Phase 5 - Dense generator/validator surgical refactor

- Objective: improve dense skills without deleting mandatory workflows.
- Depends on: Phase 1 and current `HEAD` comparison.
- Parallel-safe: `yes`, by CI/IaC/query lane.
- Exact files / modules to touch:
  - `alaa-makefile`
  - `ansible-*`
  - `github-actions-*`
  - `jenkinsfile-*`
  - `logql-generator`
  - `loki-config-generator`
  - `promql-*`
  - `terraform-*`
  - `terragrunt-*`
- Validation commands: targeted `quick_validate.py`, pack validator, `git diff` review against `HEAD`.
- Acceptance criteria: no required generator/validator behavior is lost.
- Risks / drift watchpoints: prior over-normalization regression.
- Completion signal: dense-lane review says what stayed top-level and why.

### Phase 6 - Forward-testing and routing evaluation

- Objective: test skill behavior, not only file structure.
- Depends on: changed skills from Phases 2-5.
- Parallel-safe: `yes`, read-only fresh-agent tests.
- Exact files / modules to touch: state/eval notes only unless failures require fixes.
- Validation commands:
  - inspect `docs/skill-evals/datasets/*.jsonl`
  - run manual review prompts where practical
- Acceptance criteria: high-risk skills get trigger, non-trigger, sibling-confusion, realistic-task, and negative-routing checks.
- Risks / drift watchpoints: leaked context or expected-answer contamination.
- Completion signal: eval summary recorded.

### Phase 7 - Final integration, validation, and handoff

- Objective: reconcile actual work with the plan and finish cleanly.
- Depends on: all prior phases.
- Parallel-safe: `no`
- Exact files / modules to touch: plan/state files only unless final validation reveals a fix.
- Validation commands:
  - `git status --short`
  - `python scripts\validate_sohrab_skill_pack.py`
  - `git diff --check`
  - stale-name `rg`
- Acceptance criteria: final report includes touched files, validations, residual risks, and one suggested commit message.
- Risks / drift watchpoints: accepting warnings without recording why.
- Completion signal: state status `completed`.

## Parallel-safe work split

### Parent agent

- Owns: plan/state files, integration, validation, final synthesis.
- Integrates: all subagent outputs and all lane patches.
- Validates: pack validator, targeted quick validations, diff checks, final stale-name scans.

### Lane - Validator and metadata

- Scope: validator hardening, metadata length fixes, canonical non-use headings.
- Read scope: all `skills/sohrab`, `scripts/validate_sohrab_skill_pack.py`.
- Write scope: `scripts/validate_sohrab_skill_pack.py`, low-risk metadata/heading patches only.
- Depends on: Phase 0.
- Validation target: pack validator has only real failures or warnings.
- Merge notes: run first to reduce false noise.

### Lane - Core contracts

- Scope: workflow, trust, service contracts, docs, Postman, observability, security.
- Read scope: matching skill folders and official/primary sources.
- Write scope: `alaa-workflow`, `alaa-low-noise`, `alaa-services-contract`, `alaa-trust-gateway-auth`, `alaa-security-review`, `alaa-observability-soc`, `alaa-docs-farsi`, `alaa-postman-collections`, `alaa-crockford-base32-codecs`.
- Depends on: Phase 1.
- Validation target: targeted quick validation plus contract-boundary review.
- Merge notes: preserve existing service-boundary semantics.

### Lane - PHP and Laravel

- Scope: PHP/Laravel, data, messaging, runtime, MongoDB.
- Read scope: matching skill folders and official/primary sources.
- Write scope: `alaa-php-clean-code`, `alaa-laravel-architecture`, `alaa-data-layer`, `alaa-async-messaging`, `alaa-laravel-job-rabbitmq`, `alaa-octane-performance`, `alaa-cicd-laravel-postgres`, `alaa-mongodb-patterns`, `service-runtime-kit-governance`.
- Depends on: Phase 1.
- Validation target: targeted quick validation plus source-map review.
- Merge notes: do not change live Ala service contracts from generic Laravel advice.

### Lane - Frontend and media

- Scope: Vue/Quasar/Vite, frontend delivery, annotations, Shaka, upload, Jitsi.
- Read scope: matching skill folders and official/primary sources.
- Write scope: `alaa-frontend-developer`, `alaa-frontend-devops`, `alaa-frontend-doc-annotations`, `alaa-mono-package`, `quasar-skill-packe`, `alaa-shaka-player`, `tusd-upload-platform`, `jitsi-platform-architect`.
- Depends on: Phase 1.
- Validation target: targeted quick validation and routing checks.
- Merge notes: preserve ownership between frontend, Quasar, Shaka, and visual-design helpers.

### Lane - Platform delivery

- Scope: Go, Docker, GitLab CI, Kubernetes/Helm, HAProxy, Arvan, Bash, Makefile.
- Read scope: matching skill folders, vendored Go inventory, official/primary sources.
- Write scope: `alaa-golang`, `alaa-docker-production`, `alaa-gitlab-ci-cd`, `alaa-k8s-helm`, `alaa-haproxy`, `caas-arvan-kuber`, `alaa-bash-shell`, `alaa-makefile`.
- Depends on: Phase 1.
- Validation target: targeted quick validation and router/source-map checks.
- Merge notes: do not revive retired Dockerfile/Makefile split skills.

### Lane - CI/IaC/query dense skills

- Scope: artifact-specific generator/validator skills and query/logging skills.
- Read scope: current files plus `HEAD` for regression checks.
- Write scope: `ansible-*`, `azure-pipelines-*`, `github-actions-*`, `jenkinsfile-*`, `terraform-*`, `terragrunt-*`, `fluentbit-*`, `logql-generator`, `loki-config-generator`, `promql-*`.
- Depends on: Phase 1.
- Validation target: targeted quick validation, pack validator, manual workflow preservation review.
- Merge notes: preserve mandatory workflows even when top-level files stay long.

## Commands to run

### Discovery

```powershell
git status --short
Get-ChildItem skills\sohrab -Directory | Measure-Object
python scripts\validate_sohrab_skill_pack.py
rg -n "gpt-5\.4|GPT-5\.4|gpt-5\.5|GPT-5\.5|dockerfile-generator|makefile-generator" skills\sohrab
```

### Implementation support

```powershell
python -m py_compile scripts\validate_sohrab_skill_pack.py
python -X utf8 C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\sohrab\<skill>
```

### Validation

```powershell
python scripts\validate_sohrab_skill_pack.py
git diff --check
```

### Recovery / rollback (if relevant)

```powershell
git diff -- skills\sohrab\<skill>
git show HEAD:skills/sohrab/<skill>/SKILL.md
```

## Files touched (append-only log)

- 2026-04-23T20:37:39Z - Created plan and JSON state with the workflow bootstrapper.
- 2026-04-23T20:43:00Z - Replaced generated plan skeleton with the execution contract approved by the user.
- 2026-04-23T20:48:00Z - Hardened `scripts/validate_sohrab_skill_pack.py`; target-repo path false positives are cleared.
- 2026-04-23T20:54:00Z - Phase 1 passes parent validation with warnings only.
- 2026-04-23T21:00:00Z - Phase 2 stale model-policy wording updated and targeted skills validated.
- 2026-04-23T21:13:45Z - Phases 3-7 completed: source maps, domain enrichment, dense skill preservation, routing eval repairs, final validation.

## Done / Remaining

### Done

- Loaded `$skill-creator` and `$alaa-workflow`.
- Captured baseline `git status --short`.
- Captured baseline pack validator failure.
- Created parent plan and JSON state artifacts.
- Created human-readable state file.
- Hardened validator path checks.
- Completed Phase 1 metadata/heading cleanup and parent validation.
- Completed Phase 2 GPT-5.5-ready model-policy cleanup.
- Completed Phase 3 official-first source-map and freshness-trigger refresh.
- Completed Phase 4 domain-bounded enrichment.
- Completed Phase 5 dense generator/validator surgical refresh.
- Completed Phase 6 routing evaluation and repairs.
- Completed Phase 7 final integration and validation.

### Remaining now

- No required task work remains.
- Optional future cleanup: reduce dense line-count warnings only by moving mandatory workflows intact into one-hop references.

### Deferred intentionally

- Global skill installation/link changes.
- Vendored subtree updates.
- Untracked zip/tar artifacts.

### Blocked / waiting

- None.

## Completion Snapshot

- Completed phases: 0 through 7.
- Implementation lanes used:
  - Core contracts: `019dbc1e-b43a-75a3-9ae1-8d8f27e066fc`
  - PHP/Laravel: `019dbc1e-b477-70f0-9573-333655ba6840`
  - Frontend/media: `019dbc1e-b4cf-7973-aa61-cf748aeb38cb`
  - Platform delivery: `019dbc1e-b522-71e3-8bc1-97c43c30cb9e`
  - CI/IaC/observability: `019dbc1e-b580-7bc1-bb22-a59334258880`
  - Routing eval 1: `019dbc29-4039-79d3-8b64-b30a18582be6`
  - Routing eval 2: `019dbc29-4086-7420-af2e-01a73427f7f2`
- Final validation:
  - `python C:\Users\CIT\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill>` passed for every folder under `skills/sohrab`.
  - `python scripts\validate_sohrab_skill_pack.py` passed with documented line-count warnings only.
  - `git diff --check` passed.
  - All eval manifests and datasets parse as JSON/JSONL.
- Residual warnings:
  - Dense generator/validator skills still exceed the soft top-level line-count target by design; mandatory workflows were preserved.
  - Existing archive artifacts remain untracked and untouched: `skills/sohrab/alaa-observability-soc.zip`, `skills/sohrab/signoz.tar`.
