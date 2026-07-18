# alaa-go-chi-development — Uncommitted-Changes Analysis and Skill-Pack Rewrite

Date: 2026-07-18. Scope: analysis of the uncommitted edits to
`skills/sohrab/alaa-go-chi-development` (15 files, ~565 insertions / ~699 deletions vs HEAD), verification against
the live `alaa-go-chi` repository, and the merged rewrite produced from both.

## 1. What the editor changed, and why

The uncommitted edits were driven by one real event: on **2026-07-14 the platform owner ratified
`KIT_FIRST_STABILIZATION`** (`alaa-go-chi/docs/change-requests/2026-07-14-kit-first-stabilization-scope.md`,
status `implemented`), a constitutional amendment that freezes all consumer work — no inspection, edits, audits,
prompts, propagation, or compatibility claims — until explicit owner reactivation. This is anchored across the kit
repo: `CONSTITUTION.md` (v2.0.0, amended 2026-07-14), `GOVERNANCE.md`, `AGENTS.md`, `README.md`, and the live
`docs/CONSUMERS.md` (all 5 consumers `paused` / `NOT_ASSESSED_KIT_FIRST`, including `wa-api` registered
2026-07-18). The HEAD version of the skill predated this decision and actively instructed behavior the owner had
since forbidden (consumer surveys during intake, propagation prompts, cross-consumer audits).

The editor's discoverable intents — all legitimate:

1. **Sync the skill with owner-ratified repo truth** (the phase gate). Correct and necessary.
2. **Add a kit capability map** (`references/12`) so agents know what the kit offers and use it instead of
   re-coding — exactly the skill's stated purpose, and largely accurate against source (rediskit composition,
   apicontractkit/Postman constraints, Helm/Swarm hardening, gateway-proof semantics).
3. **Add a debug/upgrade/migrate/review mode** (`references/15`) — a real workflow gap in HEAD.
4. **Add an authority-order + evidence-vocabulary reference** (`references/05`).
5. **Tighten evidence honesty** (SLA claims, `implemented-unreleased`, `runner_contract_pending`).

## 2. Why the edits were still not commit-ready

1. **Volatile state baked into durable files.** The temporary, reversible phase was hard-coded into every file —
   frontmatter description, all templates, the registry template, all six evals. The day the owner reactivates
   consumers, the entire pack goes stale at once.
2. **The steady-state governance was gutted.** The skill's core purpose (two-way kit↔consumer loop: timestamped
   change requests, kit-owner intake with decision blocks, per-consumer propagation prompts, cross-consumer
   audits, registry row contract) was compressed to fragments or deleted, leaving the pack nearly empty for its
   main long-term audience.
3. **Lost operational specificity.** Decision-record block shape, propagation tracking (`updated |
   prompt-issued | pending`), audit dimensions with concrete grep targets, change-request severity ladder and
   quality bar, KIT-WRAP mechanics, migration inventory naming, docs-authoring rules, "what happens next".
4. **Factual slip:** the capability map cited `make gen-check`, which does not exist in the kit Makefile (only
   `tier2-drift`).
5. **Eval regression:** all three steady-state evals were replaced instead of merged.

## 3. What the rewrite does

- **Phase centralized, not smeared.** `references/05` owns the gate: agents determine the active phase from repo
  truth (`docs/CONSUMERS.md` banner, `AGENTS.md`/`CONSTITUTION.md`, newest scope decision) with
  `KIT_FIRST_STABILIZATION` documented as "active as of this revision"; repo wins if newer. All other files carry
  short conditional phase notes only.
- **Steady-state fully restored** as conditional behavior: decision-tree, kit-owned surface list, decision-record
  block (extended with the kit's real fields `validation_evidence`/`implementation_status`), propagation workflow
  and tracking, per-consumer + cross-consumer audit checklists, registry row contract, template guidance depth.
- **Editor's additions kept and corrected:** capability map (+ package index, CLI binary list, exact verified Make
  targets incl. `migrate-updowup`; `gen-check` removed), debug/upgrade/migrate reference, evidence vocabulary,
  phase-aware impact sections, kit-first evals.
- **Evals merged:** 8 total — 4 phase-gate/diagnostic (editor's) + steady-state change-request, kit-owner intake,
  rediskit safety, and SLA-honesty scenarios, all rewritten phase-aware.
- **Verified against the kit** (2026-07-18): module `git.alaatv.com/vk/alaa-go-chi`, Go 1.26.5, latest tag
  `v0.3.1`, breaking `v1.0.0` candidate staged; 25 packages confirmed; scaffold flags confirmed (no
  `--without-pg/--without-mq`); `alaa-go-chi gen` pin-mismatch refusal confirmed; RUNBOOK §3–§6 intake/ship/
  propagate/bootstrap procedures confirmed.

## 4. Files in the final pack

`SKILL.md` (116 lines) + `references/05,10,12,15,20,30,40,50` + 5 templates + `evals/evals.json` (8 evals).
Total 1041 lines vs HEAD's ~1175 and the editor's ~1041 — editor's economy, HEAD's completeness.

## 4b. Second pass (2026-07-18, same session): shared infra, runtime-kit centralization, permission catalog

Audited the kit against three owner concerns before editing the skill:

- **Shared infra — naming drift surfaced to owner.** `alaa-infra-share` exists nowhere (no repo, no doc, no
  compose). The implemented contract is the canonical `alaa-shared-infra` identity: generated
  `deploy/shared-infra/compose.yaml` + wrappers, `DOCKER_SHARED_INFRA_PROJECT`/`DOCKER_SHARED_NETWORK_NAME`,
  `*_PROVISION` toggles (production fail-closed), provision-implies-migrate, reuse-if-healthy gate mirroring
  `service-runtime-kit` (owner decisions 2026-07-08 CR + 2026-07-16 unification). Skill teaches this verified
  model; whether a separate `alaa-infra-share` repo should exist awaits owner clarification.
- **Runtime-kit centralization — aligned.** Strengthened into SKILL.md law 5, a kit-owner "design for the fleet"
  rule with both-generator routing, and the capability map.
- **Permission catalog — kit aligned, skill was silent; fixed.** Kit consumer templates + CONTRACTS.md already
  mandate: `servicePermissions` seam, `trustkit.DenyAllPermissions` placeholder, map generated into
  `internal/authz/permissions_gen.go` from `alaa-permission-catalog` via `alaa-permission-generator` (auth seed
  synced), never hand-written. Added to capability map (trustkit), consumer build flow + never-do list, SKILL.md
  routing/laws, and evals 9–10.

## 5. Follow-ups (not done here)

- When the owner reactivates any consumer: update `references/05` ("active as of" statement), the
  `consumers-registry.md` scope wording, and the frontmatter description sentence about the current phase.
- The kit's own `docs/consumer-templates/{AGENTS.md,CLAUDE.md}` still name this skill; no change needed there.
