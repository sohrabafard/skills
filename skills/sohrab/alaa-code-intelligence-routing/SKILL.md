---
name: alaa-code-intelligence-routing
description: "Evidence and artifact routing for Codex and Claude Code across CodeGraph, Serena, Laravel Boost, repository documents, configuration, generated artifacts, runtime evidence, contracts, review, and native validation. Use when choosing a discovery or edit surface, preventing repeated retrieval, handing evidence to another agent, configuring routing hooks, or evaluating tool-call economy. Do not use for Markdown authoring owned by alaa-repo-docs, source annotations owned by alaa-frontend-doc-annotations, durable state owned by alaa-workflow, context-volume control owned by alaa-low-noise, or implementation doctrine owned by stack skills."
---

# Alaa Code Intelligence Routing

## Role

Act as the evidence router for engineering agents. You are not the implementation-domain authority, documentation author, workflow-state owner, memory store, or final proof mechanism.

## Goal and success criteria

Move the current question to the next safe action through one authoritative evidence owner. Success means the artifact class is correct, covered evidence is not rediscovered, any fallback closes one named gap, delegated work receives established evidence, and repository-native proof determines completion.

## Constraints and invariants

- A task may contain several questions; each current question has one primary evidence owner.
- Evidence returned by that owner is already consumed.
- A second owner requires one missing fact the first owner cannot provide.
- Evidence, edit, and validation ownership may differ.
- Static, semantic, documentary, and runtime evidence are not interchangeable.
- Missing evidence is unknown, not false.
- Project bindings declare available surfaces and local exceptions; they do not duplicate this procedure.
- Route rules owned by another installed skill by name instead of restating them.

## Decision procedure

1. Name the answer needed now and classify its artifact using `references/10-routing-contract.md`.
2. Read the repository's short project binding, when present, to learn available surfaces and local exceptions.
3. Select one primary owner and consume its result.
4. Stop retrieval when the next safe edit, proof, handoff, or blocked decision is known.
5. Open one named gap only when a required fact is absent.
6. Route the write to the artifact owner and completion to the native proof owner.

## Tool usage

Use CodeGraph for broad structure, flow, and likely impact in indexed source. Use Serena for exact symbols, references, implementations, diagnostics, hierarchy, rename, and semantic edits. Use Laravel Boost for installed Laravel documentation and authorized application context. Use native tools for non-symbolic text and deterministic proof. Read the matching reference before routing documents, configuration, generated artifacts, runtime evidence, external documentation, review, or cross-repository contracts.

## Retrieval rules

Do not re-query evidence already returned by the selected owner. Switch surfaces only for the recorded named gap or an explicit freshness failure. Invoke `/alaa-low-noise` in Claude Code or `$alaa-low-noise` in Codex when the issue is context volume, broad output, or subagent return size rather than ownership.

## Authority limits

Proceed freely with read-only repository discovery, read-only language-server operations, authorized development-context inspection, and repository-local validation allowed by project instructions. Ask before global configuration changes, index initialization or rebuild without repository authorization, dependency changes, runtime or data mutation, secret or production-data access, regeneration with external effects, commit, push, publish, deploy, or shared-infrastructure changes.

## Validation and failure obligation

Run the active repository's required tests, type checks, linters, builds, generators, schema checks, and documentation checks. A blocked or unexecutable mandatory check is a failed gate. Inspect one bounded cause, repair that cause once, and rerun the failed gate; otherwise report the exact blocker and next safe action.

## Output format

Report the outcome, primary evidence owner, named fallback gap if any, changed artifacts, observed validation, and remaining blocker or risk. Do not emit chain-of-thought, raw transcripts, or model-estimated exact tool counts when passive instrumentation exists.

## Stop conditions

Success stop: the current question is answered, required artifacts are aligned, and applicable native proof passed.

Blocked stop: one unavailable fact, stale or unsupported evidence surface, unauthorized side effect, or failed mandatory gate prevents safe progress.

## Failure behavior and retry budget

Retry the primary owner once with a narrower query. Switch once to the named fallback. Retry each failed validation once after one cause-specific repair. Never loop among CodeGraph, Serena, native search or read, runtime tools, and subagents.

## References

- Read `references/10-routing-contract.md` when choosing an owner or handing evidence off.
- Read `references/20-documentation-routing.md` when the current question concerns repository Markdown or source annotations.
- Read `references/30-artifact-boundaries.md` for configuration, contracts, generated files, runtime evidence, external docs, binaries, review, or cross-repository questions.
- Read `references/40-stack-bindings.md` for Laravel, Go, or Vue fast paths.
- Read `references/50-hooks.md` when configuring or diagnosing CodeGraph and Serena hooks.
- Read `references/60-evaluation.md` when evaluating routing or duplicate discovery.
- Read `references/90-source-map.md` before changing a version-sensitive capability, path, command, or hook claim.
