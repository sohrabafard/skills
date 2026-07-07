# Phase prompts: alaa-quasar-app-vite-v3-pack

Read first, always: `docs/_agent_plans/20260708-013000_alaa-quasar-app-vite-v3-pack.md`, `docs/agents/alaa-quasar-app-vite-v3-pack-state.md`, `.codex/state/20260708-013000_alaa-quasar-app-vite-v3-pack.json`. Mandatory skills: `$alaa-workflow`, `$alaa-low-noise`.

## Phase 2 — Author the new skill

### Codex /goal implementation prompt

Goal: create `skills/sohrab/alaa-quasar-app-vite-v3/` as a production-grade Agent Skill. End state: `SKILL.md` (frontmatter: `name` + `description` only; routing-first; lean), `agents/openai.yaml` (match sibling shape), `references/00-topic-map.md`, references for (a) v2->v3 migration, (b) v3 config/features, (c) service-worker excellence, (d) WebOTP + device trust, (e) modern user experience, plus `references/90-maintenance-and-live-checks.md` and `scripts/check-upstream-versions.mjs`. Posture: `@quasar/app-vite` v3 (3.0.1) is the stable production line; v2 is legacy/maintenance. Route to sibling skills instead of duplicating (quasar-skill-packe for exact shapes; alaa-app-vite-quasar for v2-era detail; alaa-indexeddb-browser-storage; alaa-frontend-developer; alaa-vue-typescript-clean-code; alaa-mono-package). Use ✅ Do / ❌ Don't pairs on high-value rules. Dual-runtime wording (Opus + Codex). Scope: only the new skill directory. Validate: markdown links resolve; version script runs; frontmatter parses. Report per checkpoint with changed-file list only.

### Opus review prompt

<task>Review skills/sohrab/alaa-quasar-app-vite-v3 as an execution contract for coding agents.</task>
<must_check>trigger quality of description; stable-v3-first accuracy (3.0.1, 2026-07-07); no duplicated sibling content where routing suffices; token-efficient progressive disclosure; migration playbook correctness vs official quasar.dev upgrade guide; SW guidance safety (update flow, no cached SW, offline fallback); WebOTP fallback chain correctness; fingerprinting bounded to weak-signal device trust with privacy constraints; Do/Don't pairs present; dual-runtime consistency.</must_check>
<verdict>APPROVE or CHANGES_REQUIRED with file:line findings.</verdict>

## Phase 3 — Upgrade alaa-frontend-developer

Codex: add `references/25-modern-css-and-motion.md` (or matching number) covering the Phase-1 Lane-D findings; wire into SKILL.md routing map, mandatory cross-topic rules, and search rules; flip stale v2/RC posture lines; add companion routing to `$alaa-quasar-app-vite-v3`. Scope: that skill directory only.
Opus review: check Baseline/browser-support claims carry versions, reduced-motion is mandatory, compositor-only perf rules present, no art-direction scope creep.

## Phase 4 — Sibling gap closure

Codex: apply Lane-E stale-posture list file by file across quasar-skill-packe, alaa-app-vite-quasar, alaa-vue-typescript-clean-code, alaa-indexeddb-browser-storage, alaa-mono-package. Flip "v3 is RC" to "v3 stable since 3.0.1 (2026-07-07); v2 = maintenance line"; refresh version snapshots; add cross-routing to the new skill; close per-skill gaps from Lane E. Keep diffs minimal and per-skill.
Opus review: verify zero remaining stale RC-posture lines (grep `rc\.|RC|pre-release|2\.6\.2` guided), routing symmetry across the trio + new skill, no broken ownership boundaries.

## Phase 5 — Validate + reconcile

Run available validators (`scripts/validate_skill_pack.py` style where present), link checks, final grep sweeps; update both state files; produce final report with one Conventional-Commit message for this repo.

## Fix loop

Feed review findings back as: "Apply these findings exactly, smallest safe diff, re-run the validation that failed, update state files." No scope widening.
