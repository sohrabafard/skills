# Workflow Prompt Pack - Selected normalization and Arvan skill corrections

- Plan: `docs/_agent_plans/20260925-143542_normalization-arvan-selected-fixes.md`
- Checkpoint: `docs/agents/20260925-143542_normalization-arvan-selected-fixes-state.md`
- Verification status: verified documentary runtime/model mapping; target-host installed role activation and effective grants remain unknown and must be checked at execution preflight.
- Verified on: 2026-09-25
- Verification sources: https://learn.chatgpt.com/docs/agent-configuration/subagents ; https://learn.chatgpt.com/docs/build-skills ; https://github.com/laravel/framework/blob/13.x/src/Illuminate/Foundation/Http/Middleware/TransformsRequest.php
- Implementer runtime/model: Codex / gpt-6-sol, high; current alaa-implementer source pin.
- Independent reviewer runtime/model: Codex / gpt-6-sol, high; current alaa-reviewer source pin.
- Documenter runtime/model: not separately included; scoped documentation corrections belong to the implementation lanes, independently reviewed.
- Lead: GPT-6 Astra requested by user; observed runtime identity and effort unknown.
- Other gate profiles: alaa-verifier gpt-6-luna/low; alaa-instruction-reviewer gpt-6-astra/high, as inspected in source metadata. Availability/enforcement must be verified before dispatch. Never silently substitute a role or model.
- Policy changes: none. These dated values are execution metadata, not changes to canonical policy.

The corrections are bounded applications of ratified findings, so the routine implementer is the starting role. If a lane discovers an unresolved judgment requiring escalation under the canonical owner, record the criterion; do not use escalation to conceal missing evidence or scope expansion.

The user requested one self-contained orchestrator prompt. It exceeds the default 250-word role target because it must carry the two scopes, exclusions, preservation, evidence and authority across a new-chat boundary. Compression removed repeated workflow mechanics; it preserves every material boundary. No live evaluation or improved-model claim is implied.

## Complete prompt for the new Codex chat

```text
$alaa-codex-orchestrator

Act as the lead orchestrator for the approved two-skill correction plan. Use the user-selected GPT-6 Astra for the lead; do not infer observed runtime identity from that request. Communicate decisions and approval questions in Persian; save artifacts in English. Delegate implementation to owned lanes; do not implement skill content yourself.

Read and execute:
- Plan: docs/_agent_plans/20260925-143542_normalization-arvan-selected-fixes.md
- Checkpoint: docs/agents/20260925-143542_normalization-arvan-selected-fixes-state.md

The plan is approved for scoped local execution in this new chat. Do not repeat the broad audit or ask for approval of this same scope. Read applicable AGENTS.md instructions and the plan's handoff package, then verify the current repository root, branch, HEAD, dirty state, selected source files, installed roles and effective permissions. Preserve unrelated changes. The planning baseline was main at 34aeb11db38e1408b1760d9fe3f4c1fec16d0498; a different HEAD requires reconciliation, not a reset.

Authorize two disjoint implementation lanes:
1. alaa-input-normalization: correct the length claims in references/10-normalization-contract.md so they distinguish digit folding from NFC and match the canonical implementation; complete the Laravel example in references/30-backend-middleware-binding.md, which currently calls undefined fieldName. Preserve Nd-only folding, NFC, text/typed opt-in semantics, value-only traversal, normalization before validation, corpus expectations and existing failure rules. Resolve nested typed-field semantics from current evidence; do not silently broaden matching.
2. caas-arvan-kuber: correct the malformed Python invocation in SKILL.md so it resolves the real alaa-k8s-helm/scripts/check_manifests.py, quotes paths and preserves --profile arvan and exit-code handling. Preserve all existing platform, RBAC, Secret and live-discovery constraints.

Implementation writes are limited to those two skill directories and necessary focused example validation within them. The lead owns only the saved workflow family and artifacts/normalization-arvan-selected-fixes/. Other skills are read-only dependencies. service-runtime-kit-governance and alaa-permission-generator were explicitly deferred. Every other audit finding, root-file modernization, provider/version refresh, model-policy change and migration remains excluded.

Follow the plan's focused tests and independent gates. Verify the normalization reference, Unicode composition case and complete Laravel example; distinguish actual framework execution from syntax checks or stubs. Validate the repaired Arvan command with local fixtures and its existing checker, without a live cluster. Preserve independent correctness and instruction review, run the affected repository gates against a held content snapshot, and never claim skipped runtimes passed.

Revalidate time-sensitive official facts only where they control the selected work. Stop only affected work on material drift, scope expansion, missing required runtime/role or unresolved behavior. Keep independent work moving. Use the plan's bounded retry/fix cycles, BelowNormal priority and limited concurrency. Do not weaken tests, change corpus expectations or alter canonical normalization implementations to make prose fixes pass.

No installation, tool upgrade, global configuration change, consumer/cluster mutation, benchmark, live model evaluation, commit, merge, push, publication, deployment or destructive cleanup is authorized. Ask separately only if such an effect becomes necessary. Do not reopen either completed model migration.

Finish with the selected changes, exact validation and independent review results, scoped content identity, updated checkpoint, remaining blockers and clickable paths. Distinguish source validation, runtime proof, installed activation and quality evaluation; report lifecycle states accurately. Stop after the reviewed local result or an exact affected-scope blocker.
```

## Implementer dispatch contract

**Outcome:** Complete only the assigned N or A lane from the plan.
**Read first:** Applicable instructions, plan handoff facts, assigned skill's complete contract, and relevant read-only dependency.
**Scope:** Assigned skill directory only; other lane and shared workflow files excluded. No canonical normalization/corpus changes or external effects.
**Validation:** Apply the lane's focused matrix and record exact commands/results/source identity; unavailable proof is not pass.
**Done:** Ratified correction and preservation criteria hold with a reviewable diff; parent integrates.
**Blocked:** Return unresolved behavior, scope conflict, unavailable runtime or failed gate with evidence; never repair another lane.

## Independent reviewer dispatch contract

**Outcome:** Judge the frozen combined diff and its evidence independently.
**Read first:** Plan, actual diff, changed instructions, test evidence and scoped snapshot.
**Scope:** Read-only; preserve the user's two-skill selection. Separate source correctness, runtime proof and activation/quality limits.
**Validation:** Confirm complete helper semantics, NFC wording, real checker invocation, unchanged corpus and retained authority; instruction reviewer applies the compression-equivalence contract.
**Done:** Return severity-ranked findings, verdict, proof limitations and exact paths. No self-approval by implementers.
**Blocked:** Identify the smallest missing evidence; do not edit, broaden scope or require unselected benchmarking.
