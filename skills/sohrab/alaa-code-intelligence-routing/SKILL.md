---
name: alaa-code-intelligence-routing
description: "Deterministic evidence routing for CodeGraph, Serena, Laravel Boost, native and domain owners, and repository proof in Codex and Claude Code. Use when selecting a discovery, semantic-edit, documentation, configuration, generated-artifact, review, runtime, handoff, hook, fallback, or validation surface; when preventing duplicate retrieval; or when evaluating routing economy. Do not use as the implementation, documentation-authoring, workflow-state, memory, orchestration, or proof doctrine itself; invoke the owning skill or repository-native gate."
---

# Alaa Code Intelligence Routing

## Role

Act as the routing control plane for engineering evidence. Select the owner of the current question; do not replace the implementation-domain owner, documentation author, workflow-state owner, memory store, or repository proof mechanism.

## Goal and success criteria

Move each named question through discovery, exact semantics or editing, and proof without repeating an answered question. Success requires the correct owner, same-worktree evidence, one recorded secondary gap at most, an explicit partial or blocked label when guarantees cannot be preserved, and observed repository-native proof.

## Constraints and invariants

- One current question has one primary owner.
- A secondary owner may answer only one recorded missing fact.
- Parallel work is legal only for separately named questions when neither answer can change the other's owner, query, authorization, or scope; otherwise sequence the questions.
- Discovery, exact semantics or editing, and proof are different questions, so ordered composition across owners is valid.
- Evidence already returned for a question is consumed and must not be retrieved again.
- Static, semantic, documentary, runtime, and proof evidence are not interchangeable.
- No result means unknown unless the selected owner proves its search was complete for the required scope.
- The user-level `CODEGRAPH_START` block owns the CodeGraph-first baseline for indexed supported source. Project bindings declare availability, invocation, and local exceptions; they do not restate that baseline.
- Route doctrine owned elsewhere to `/alaa-repo-docs` (`$alaa-repo-docs`), `/alaa-workflow` (`$alaa-workflow`), `/alaa-low-noise` (`$alaa-low-noise`), the stack owner, or the repository-native gate.

## Decision procedure

1. Name each independently answerable question before selecting tools.
2. Read the short project binding, when present, and verify the declared surfaces resolve to the active Git worktree.
3. Classify the current question with `references/10-routing-contract.md` and select one primary owner.
4. Consume the result. Stop retrieval when the next safe edit, proof, handoff, or blocked decision is known.
5. When a required fact is absent, record one named gap before selecting one secondary owner.
6. Treat a move from discovery to exact semantics or editing, and then to proof, as a new question; do not repeat discovery.
7. Start review from Git diff and decide completion only from repository-native gates.

## Tool usage

Use CodeGraph for unknown location and broad supported-source flow, relationships, architecture, or impact. Use Serena for a known supported-source symbol or file, exact semantics, references, hierarchy, diagnostics, and semantic edits. Use Laravel Boost for installed Laravel documentation and authorized Laravel application context. Use native or domain owners for Markdown and policy, JSON/YAML/TOML, CI, Docker/Compose/Helm semantics, generated artifacts, binaries, runtime facts, Git diff, and proof.

## Retrieval rules

Do not re-query evidence already returned by the selected owner. A CodeGraph stale or pending-file signal routes directly to a targeted live read of the named affected files; do not retry CodeGraph for freshness. An empty, unavailable, or worktree-misaligned owner receives at most one health attempt, not a second evidence query. If the fallback cannot preserve broad-flow or impact completeness, exact semantic guarantees, or required proof, label the result partial or blocked. Invoke `/alaa-low-noise` (`$alaa-low-noise`) when output volume rather than evidence ownership is the problem.

## Authority limits

Proceed only within the authority already granted by repository instructions and the user. Before every Laravel Boost call, verify the installed tool inventory and classify the intended effect: documentation, installed-package information, and application metadata may be read within existing read authority; database queries, code-execution or runtime operations exposed by the installed tool, data mutation, secrets, and production context require their normal authorization. Tool availability grants no authority. Serena activation is not onboarding and grants no permission to write memories, initialize or rebuild indexes, install prerequisites, or mutate configuration.

## Validation and failure obligation

Verify that the CodeGraph root, Serena active project, Git diff, and proof command working directory name the same worktree. Evidence from another checkout is unavailable. Run the active repository's required tests, type checks, linters, builds, generators, schema checks, and documentation checks. A blocked or unexecutable mandatory check is not a pass.

## When NOT to use

- Do not use this skill to answer a single exact fact when the repository already names its native or domain owner and no routing decision exists.
- Do not use local CodeGraph or Serena evidence to prove a cross-repository owner, consumer, compatibility, or handoff claim; start from the authoritative catalog, contract registry, hosting surface, or named repository.
- Do not force unsupported or unindexed artifacts through CodeGraph or Serena. Route them to the native or domain owner and label any lost completeness guarantee.
- Stop an owner when it has answered its named question. A later proof question does not authorize another discovery pass.
- Do not interpret an empty result as absence, or an unavailable tool as permission to make an unsupported claim.
- Do not claim one routing policy is absolutely best from prose or call counts. Use the controlled evaluation contract in `references/60-evaluation.md`.

## Output format

Report the outcome, named question, primary owner, established evidence, named secondary gap if any, worktree identity, changed artifacts, observed native proof, and remaining partial or blocked guarantee. Do not emit raw transcripts or reconstruct exact tool counts when passive instrumentation exists.

## Stop conditions

Success stop: every named question is answered, required artifacts are aligned, and applicable native proof passed in the same worktree.

Blocked stop: an unavailable fact, unsupported artifact, lost completeness or semantic guarantee, unauthorized effect, worktree mismatch, or failed mandatory gate prevents safe progress.

## Failure behavior and retry budget

For empty, unavailable, or misaligned owners, perform one health attempt and then use the recorded fallback or stop. For CodeGraph stale or pending files, skip the health attempt and read only the named live files. Retry a failed native gate once only after one cause-specific repair. Never loop among CodeGraph, Serena, Boost, native tools, runtime owners, and delegated agents.

## References

- Read `references/10-routing-contract.md` when choosing an owner or handing evidence off.
- Read `references/20-documentation-routing.md` when the current question concerns repository Markdown or source annotations.
- Read `references/30-artifact-boundaries.md` for configuration, contracts, generated files, runtime evidence, external docs, binaries, review, or cross-repository questions.
- Read `references/40-stack-bindings.md` for Laravel, Go, or Vue fast paths.
- Read `references/50-hooks.md` when configuring or diagnosing CodeGraph and Serena hooks.
- Read `references/60-evaluation.md` when evaluating routing or duplicate discovery.
- Read `references/70-project-bindings.md` when writing a short project binding, Serena language profile, or `initial_prompt`.
- Read `references/90-source-map.md` before changing a version-sensitive capability, path, command, or hook claim.
