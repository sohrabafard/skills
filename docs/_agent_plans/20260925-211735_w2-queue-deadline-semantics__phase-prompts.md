# Workflow Prompt Pack - W2 queue deadline and durable acceptance semantics

- Plan: `docs/_agent_plans/20260925-211735_w2-queue-deadline-semantics.md`
- Checkpoint: `docs/agents/20260925-211735_w2-queue-deadline-semantics-state.md`
- Verification status: documentary runtime/model mapping verified; target-host role activation and effective grants remain unknown until preflight.
- Verified on: 2026-09-26
- Verification sources: https://learn.chatgpt.com/docs/agent-configuration/subagents ; https://www.rabbitmq.com/docs/ttl
- Implementer runtime/model: Codex / gpt-6-astra, high (alaa-implementer-sol source policy; shared instruction-contract judgment).
- Independent reviewer runtime/model: Codex / gpt-6-sol, high (alaa-reviewer).
- Documenter runtime/model: not separately included; selected skill documentation belongs to the writer and independent instruction review.
- Lead: user-requested GPT-6 Astra; observed runtime identity/effort unknown.
- Before/after model-effort mappings: unchanged; no pin or agent-file edits selected.

Recheck canonical policy and installed roles at dispatch; do not silently substitute. The self-contained lead prompt exceeds the usual role-prompt length target to retain authority, semantic boundaries and source-proof limitations. Its final wording was compressed after drafting; no live model evaluation was performed.

## Complete execution prompt

```text
$alaa-codex-orchestrator

Act as lead orchestrator for the approved W2 skill correction. Use the user-selected GPT-6 Astra for the lead; report observed runtime identity separately or unknown. Communicate decisions and questions in Persian; save files in English. Delegate implementation; do not write skill changes yourself.

Read:
- docs/_agent_plans/20260925-211735_w2-queue-deadline-semantics.md
- docs/agents/20260925-211735_w2-queue-deadline-semantics-state.md

This authorizes local implementation of that plan in this new chat. Do not repeat the fleet audit or ask again to approve W2. Verify repository root, applicable AGENTS.md, current HEAD/branch, dirty state, installed roles and effective permissions before dispatch. Planning baseline: main, ba278f4ed6962e7f20251e55784129c550aa1b85. Preserve unrelated work and reconcile drift without resetting it.

Goal: remove ambiguity in alaa-reliability-sla between a synchronous caller's deadline and the lifecycle of durably accepted asynchronous work. A disconnected caller or expired HTTP request must not, by itself, cancel or discard accepted durable work. Preserve bounded capacity, per-attempt timeouts, retries, idempotency and explicit failure handling. Do not replace the ambiguity with an unlimited-retention or eventual-success promise.

Authorize one owned implementation lane in skills/sohrab/alaa-reliability-sla, covering the body and affected deadline, admission, retry and verification references. First inspect alaa-async-messaging and alaa-services-contract read-only. Amend only their directly contradictory wording or necessary owner pointers if current evidence proves the W2 correction cannot remain consistent otherwise; record that evidence and serialize those edits. Do not change wire formats, numeric budgets, retention periods, event names, broker configuration or consumer code.

The lane must distinguish:
- Waiting synchronous work: inherited request deadline, bounded resources, cancellation and early shedding.
- Durable acceptance: an explicit persisted ownership boundary, independent of whether the caller receives or keeps the receipt.
- Durable execution: bounded processing attempts and retries; job validity, cancellation and expiry outcomes come from the owning business contract.
- Broker TTL, application validity, storage retention, publisher confirms and consumer acknowledgements: distinct concepts, with mechanics delegated to their existing owners.
- An unknown acceptance outcome: reconcile by identity/idempotency; never assume either loss or success and blindly repeat a side effect.

Keep all other audit items deferred, including normalization/Arvan follow-up, service-runtime-kit-governance and alaa-permission-generator. The lead alone updates this workflow family and task evidence. No other skill modernization, service or live queue changes.

Use the plan's architecture pressure test, scenario-based acceptance matrix, independent correctness/instruction review and affected native gates. Freeze the tested scope and record HEAD plus content hashes. Text checks do not prove live broker or application behavior. Revalidate relevant official facts; stop only affected work on material drift, missing authority or unresolved product semantics.

Use BelowNormal priority, bounded concurrency and retries, and at most two review/fix cycles. Do not weaken checks or invent default TTLs. No installation, global configuration, live benchmark/model evaluation, production access, deployment, commit, merge, push, publication or destructive cleanup is authorized.

Finish with changed files, preserved versus deliberately clarified behavior, exact checks and independent verdicts, updated checkpoint, lifecycle states and remaining proof limits. Stop after the reviewed local result or a precise blocker.
```

## Implementer

**Outcome:** Correct only the approved W2 semantic boundary.
**Read first:** Plan, full selected skill contracts, ratified architecture/scenario evidence.
**Scope:** One owned writer; conditional dependency edits require recorded contradictions. No numbers, consumer code or broker changes.
**Validation:** Plan matrix; preserve deadline, durability, retry, idempotency and acceptance authority.
**Done:** Consistent reviewable source diff, exact evidence, preservation checklist.
**Blocked:** Missing business meaning, unapproved surface or failed proof; no guessing or scope expansion.

## Independent reviewer

**Outcome:** Judge actual snapshot for loss-of-work, unbounded-work and authority regressions.
**Read first:** Plan, resulting diff, all scenario evidence and affected owner contracts.
**Scope:** Read-only, independent of writer; no fixes.
**Validation:** Distinguish sync cancellation, durable ownership, validity and transport acknowledgements; reject source/runtime conflation.
**Done:** Severity-ranked findings and verdict with proof limits.
**Blocked:** Name missing source or decision and affected scope.
