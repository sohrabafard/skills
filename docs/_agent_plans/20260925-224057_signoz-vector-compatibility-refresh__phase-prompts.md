# Workflow Prompt Pack - SigNoz and Vector compatibility refresh

- Plan: `docs/_agent_plans/20260925-224057_signoz-vector-compatibility-refresh.md`
- Verification status: official role mechanics checked; canonical role selection and effective activation require execution preflight
- Verified on: 2026-09-26
- Verification sources: https://learn.chatgpt.com/docs/agent-configuration/subagents and repository alaa-prompting-guide
- Implementer runtime/model: Codex / canonical selected role; no model policy change
- Independent reviewer runtime/model: Codex / canonical independent roles; observed identity unknown
- Documenter runtime/model: not dispatched; documentation belongs to owned writers

## Implementer
**Outcome:** Complete approved two-skill refresh including latest stable Vector guidance.
**Read first:** Plan, checkpoint and applicable instructions.
**Scope:** Two disjoint skill lanes only.
**Validation:** Plan matrix and independent gates.
**Done:** Approved behavior and evidence agree.
**Blocked:** Record exact unmet requirement and recovery.

## Execution prompt

```text
$alaa-codex-orchestrator

Lead the approved SigNoz/ClickHouse and Vector skill refresh. The user selected GPT-6 Astra; do not infer serving identity. Communicate in Persian; save English artifacts with repository-relative paths.

Read AGENTS.md, skills/sohrab/AGENTS.md, applicable nested instructions, and:
- docs/_agent_plans/20260925-224057_signoz-vector-compatibility-refresh.md
- docs/agents/20260925-224057_signoz-vector-compatibility-refresh-state.md
- docs/_agent_plans/20260925-224057_signoz-vector-compatibility-refresh__phase-prompts.md
Load repository sources of alaa-prompting-guide, alaa-workflow and the orchestrator. Read both target skills completely, including affected references, scripts, fixtures and metadata, before edits.

Verify repository root, branch, HEAD, dirty state and prior execution. Planning baseline: main at 3a62cbb615e0180458ebedd4bc9a0794c17c1e60, tracked clean. Preserve unrelated work. Verify existing GPT/Claude migration evidence; do not redo migrations. Material drift blocks only affected work.

Approved source scope:
1. skills/sohrab/alaa-signoz-clickhouse-docs/**
2. skills/sohrab/vector-rust-observability-pipelines/**
The lead alone updates this workflow family and artifacts/signoz-vector-compatibility-refresh/**. All other skills, vendor, root scripts/indexes/manifests, consumers, installed copies and runtime/model configuration are excluded. Earlier waves are not reopened. service-runtime-kit-governance and alaa-permission-generator remain deferred.

Use official released documentation, release notes, upgrade guides and tag-matched source. Record dates, URLs, documented versions, observed local consumer/binary versions, latest stable, supported ranges, migration implications and unknowns. Latest upstream is not permission to drop consumer compatibility.

Vector has an explicit additional requirement: find the latest stable Vector product release at execution time and add its relevant new capabilities, breaking/default/security changes, deprecations, fixes and migration guidance to the skill. Planning observed vector.dev/releases listing 0.58.0; GitHub releases/latest instead selected vdev-v0.3.24. Exclude vdev, nightly and prereleases from the stable product selection; resolve conflicting release evidence explicitly.
Review the full latest release and intervening releases since the skill baseline. Record a coverage ledger with each relevant delta mapped to its owning instruction/example/test and each omitted item justified. Do more than update a version number. Keep version facts centralized; add verified, version-qualified examples where useful. Preserve older supported consumer paths and chart/appVersion distinctions.

For SigNoz, refresh supported schema/query/API guidance and investigate alert API lifecycle against released evidence. Preserve vendor-owned read-only schemas, bounded query rules, panel shapes, privacy/authorization assumptions and explicit unverified-schema labels. Do not mark the installed alert surface confirmed from public docs. No live discovery is authorized; keep the existing fail-closed fallback when deployment evidence is unavailable.

Preserve Vector delivery/acknowledgement semantics, retries, backpressure, disk-buffer failure behavior, VRL failure tests, routing confinement, secret handling and strict validation. Reconcile changed upstream behavior with version-qualified rules, never silently weaken security gates.

Use two disjoint owned writer lanes, one per skill, under one lead. Follow canonical role mappings without changing model policy. Shared contracts and workflow writes serialize. Obtain fresh independent instruction/correctness review and security review if secret or confinement guidance changes.

Run scoped checker self-tests and relevant fixtures, official link/version checks, native repository gates and workflow validation. Use installed exact binaries for Vector validate/test where available. Never install tools to fill a proof gap. Distinguish static/fixture results from real Vector runtime, installed SigNoz schema and runtime activation. Missing proof remains explicit.

At most one cause-specific repair and one materially different retry per failed operation; then record the blocker and recovery. No install, dependency or service upgrade, live benchmark, production/cluster/provider access, commit, merge, publication, deployment, deletion or global configuration change is authorized. Ask only for material breaking scope/compatibility decisions; continue unaffected work.

Finish with release coverage, source changes, preserved/changed behavior, independent verdicts, exact passed/failed/unrun/blocked checks and an updated checkpoint. Execute only this selected plan.
```

## Independent reviewer
**Outcome:** Judge correctness and instruction preservation independently.
**Read first:** Plan, diff and primary evidence.
**Scope:** Read-only approved surfaces.
**Validation:** Check source provenance, release coverage and proof limits.
**Done:** Findings, verdict and limitations returned.
**Blocked:** State missing evidence; never edit to obtain a pass.
