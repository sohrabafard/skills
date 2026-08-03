---
name: alaa-code-intelligence-routing
description: "Evidence-routing control plane for CodeGraph, Serena, Laravel Boost, language-native semantic tools, domain skills, and repository proof. Use when an agent must choose the owner of an unknown-location, call-path, caller/callee, impact, known-symbol, semantic-edit, Laravel framework-context, runtime, review, configuration, documentation, generated-artifact, fallback, or validation question, when duplicate grep/read discovery must be prevented, or when deciding which code-intelligence servers and tools a role or subagent may be granted. Do not use to implement domain code, author repository documentation, manage durable workflow state or memory, orchestrate agents, define agent rosters, or prove completion; route those to the relevant stack skill, alaa-repo-docs, alaa-workflow, the installed orchestrator, or repository-native gates."
---

# Alaa Code Intelligence Routing

## Role

Act as the evidence-routing control plane. You are not the implementation-domain owner, documentation author, workflow-state owner, memory store, orchestrator, or proof mechanism.

## Goal and success criteria

Move every named question to one evidence owner, consume that result, and continue to edit or proof without rediscovering the same fact. Success requires:

- the selected owner matches the question and active project binding;
- every evidence and proof surface resolves to the same Git worktree;
- at most one secondary owner answers one recorded missing fact;
- lost completeness, semantic safety, runtime authority, or proof is labelled partial or blocked;
- completion is decided only by observed repository-native gates.

## Constraints and invariants

- One current question has one primary owner.
- Discovery, exact semantics or editing, runtime observation, and proof are separate questions and may have different owners in sequence.
- Parallel retrieval is allowed only for independently named questions when neither answer can change the other's owner, scope, authorization, or query.
- Evidence returned for a question is consumed; do not retrieve it again for reassurance.
- An empty result means unknown unless the selected owner proves complete coverage of the required scope.
- The CodeGraph server and installer own exact CodeGraph tool guidance, MCP registration, permissions, and marker-fenced client instructions. This skill owns whether CodeGraph is selected. Interpret any CodeGraph-first text only within structural discovery, never as precedence over a known-symbol semantic owner, a native artifact owner, runtime evidence, review, or proof.
- Trust a code graph's edges according to the provenance it returns, and read its silence as a limit rather than a fact. A graph may resolve more than direct static calls — callback registration and interface-to-implementation are commonly real edges — so an empty text search never establishes that a symbol is unused. It will not resolve a dispatch computed at runtime, and where it detects such a site it reports the boundary instead of guessing an edge. Detection is best-effort, so an unexplained gap in a path is itself a boundary.
- A reported boundary is an answer, and it is the one place a second lookup is legitimate. Spend one targeted semantic, documentation, or runtime lookup on the missing dispatch fact — using whatever key the boundary exposed, when it exposed one — and do not restart structural discovery. Never report a call path as complete across a boundary that was not traversed.
- A stack skill may name a language-native semantic owner that replaces Serena for that stack. Follow the stack owner and report any binding drift.
- A code-intelligence MCP server runs outside the client's sandbox and permission model. A read-only lane stays read-only only when its semantic grant is restricted to read tools; a read-only sandbox mode, a restrictive permission mode, and a withheld native edit tool do not stop a semantic server's own edit, rename, delete, file-creation, or shell tools. Grant the read set in `references/80-agent-scoping.md` instead of the whole server.
- Route repository Markdown to `/alaa-repo-docs` in Claude Code or `$alaa-repo-docs` in Codex, durable execution state to `/alaa-workflow` or `$alaa-workflow`, output-volume policy to `/alaa-low-noise` or `$alaa-low-noise`, and lane fan-out to the installed runtime orchestrator. Do not restate their rules here.

## Decision procedure

1. Split the request into independently answerable questions.
2. Read the short repository binding and identify the Git root, CodeGraph root, active semantic project, installed Laravel Boost inventory, and native proof owner that apply.
3. Select one primary owner. Four cases cover most questions and need no reference read: an unknown
   location or a relationship between symbols goes to CodeGraph; a known file or symbol whose exact
   references, hierarchy, diagnostics, or symbol-scoped edit is needed goes to the semantic owner; the
   behaviour, current signature, or convention of an installed framework or package goes to that
   framework's documentation surface before any source read, because only it answers at the version
   installed here;
   and configuration, markup, contracts, generated output, and prose go to their native owner. Read
   `references/10-routing-contract.md` when the question does not land cleanly in one of the four, when
   two owners look equally right, or when an owner has already come back empty.
4. Ask only the smallest question that unlocks the next safe edit, proof step, handoff, or blocked decision.
5. Record what the result established and stop that owner.
6. When one required fact is absent, record the established evidence, missing fact, reason the owner cannot supply it, and the one secondary owner allowed to answer it.
7. Start review from Git diff. Return to native gates before declaring completion.

## Tool usage

- **CodeGraph:** unknown source location; related symbols; route-to-handler and downstream source flow; call paths; callers and callees; architecture relationships; likely blast radius; and the files or source regions that should be read in a healthy index of a supported language. It is a pre-built index, so ask it first for a structural question rather than arriving at the same answer through a grep-and-read loop it has already done, and consume its verbatim source instead of re-reading the same files. Prefer the installed primary exploration surface; use a narrower CodeGraph surface only when the installed server exposes it and the named question is narrower.
- **Serena:** a known file or symbol in a configured language; file or symbol outline; declaration, references, hierarchy, diagnostics, and semantic rename or symbol-scoped edits when the installed backend exposes the required operation. Select from the inventory the installed version exposes rather than a remembered tool list; names are added and retired between releases. Do not treat Serena activation as permission to edit.
- **Language-native semantic owner:** where a stack skill names its own semantic interface, that skill owns the choice and this one follows it. For Go the order is availability-based rather than fixed: a configured, healthy Serena answers known-symbol questions, and where Serena is absent or unhealthy the Go owner's language-server interface answers them instead — `/alaa-golang` in Claude Code or `$alaa-golang` in Codex, which routes onward to gopls. Structural discovery stays with CodeGraph either way, and Go build, vet, and test commands remain the proof.
- **Laravel Boost:** current documentation for installed Laravel packages and authorized Laravel application context. It does not own static source call graphs, semantic refactors, Git review, or completion proof.
- **Native or domain owner:** registered routes, plain text, Markdown, JSON, YAML, TOML, CI, containers, generated artifacts, contracts, binaries, runtime commands, Git diff, tests, builds, linters, generators, schema checks, and other repository proof.

## Retrieval rules

Do not query a second surface to confirm an answer already returned. If CodeGraph names stale or pending affected files, read only those live files and do not rerun the graph for freshness. An empty, stale, unavailable, or worktree-misaligned owner receives at most one tool-native health or freshness attempt. Then use the recorded fallback or stop; never loop through refresh and the same evidence query. A fallback may answer a narrower fact, but it must not inherit a completeness or semantic guarantee its owner cannot provide.

## Authority limits

This skill changes only evidence routing; it does not expand or restrict the selected tool's native lifecycle or the authority already granted for the task. Do not modify MCP, hook, CodeGraph, Serena, or Laravel Boost integration configuration unless the task explicitly requests setup, upgrade, repair, or removal.

## Validation and failure obligation

Verify that CodeGraph, the active semantic project, Git diff, generated state, runtime evidence, and every validation command resolve to the same worktree. Run the repository-required tests, type checks, linters, builds, generators, schema checks, and documentation checks. Report the exact command and observed result. A mandatory check that failed or could not run is not a pass.

## When NOT to use

- Do not use this skill when one exact native or domain owner is already named and no routing decision exists.
- Do not use local static evidence to prove cross-repository ownership, consumer compatibility, runtime behavior, or external framework behavior.
- Do not force unsupported, unindexed, generated, binary, configuration, or documentation artifacts through CodeGraph or Serena.
- Do not treat a later proof question as permission for another discovery pass.
- Do not infer absence from an empty result or availability from a configured-but-unhealthy tool.
- Do not claim this policy is universally best from prose, vendor benchmarks, or call counts; use `references/60-evaluation.md`.

## Output format

Report: outcome; named question; primary owner; established evidence; secondary gap and owner when used; worktree identity; changed artifacts; observed native proof; and any remaining partial or blocked guarantee. Do not emit raw tool transcripts.

## Stop conditions

**Success:** every named question is answered, required artifacts are aligned, and applicable native proof passed in the same worktree.

**Blocked:** an unavailable fact, unsupported artifact, lost completeness or semantic guarantee, unauthorized effect, worktree mismatch, or failed mandatory gate prevents safe progress.

## Failure behavior and retry budget

Perform one health attempt for an empty, unavailable, or misaligned owner, then use the recorded fallback or stop. Skip that attempt when CodeGraph already names stale files and read only those files. Retry one failed native gate once, and only after one cause-specific repair. Never loop among CodeGraph, Serena, Boost, native tools, language-native semantic owners, and delegated agents.

## References

- Read `references/10-routing-contract.md` before selecting or changing an evidence owner.
- Read `references/20-documentation-routing.md` for repository Markdown and source annotations.
- Read `references/30-artifact-boundaries.md` for configuration, contracts, generated files, runtime evidence, external facts, binaries, review, and cross-repository claims.
- Read `references/40-stack-bindings.md` for Laravel, Go, and Vue or Quasar routes.
- Read `references/50-hooks.md` before configuring or diagnosing CodeGraph and Serena hooks.
- Read `references/60-evaluation.md` before evaluating routing economy or duplicate discovery.
- Read `references/70-project-bindings.md` before writing a repository binding or Serena `initial_prompt`.
- Read `references/80-agent-scoping.md` before granting or withholding a code-intelligence server for a role, subagent, or lane.
- Read `references/90-source-map.md` before changing a capability, command, path, configuration key, or hook claim.
