---
name: alaa-code-intelligence-routing
description: "Evidence routing for CodeGraph, Serena, Laravel Boost and useful native tools. Use to select an owner for discovery, call paths, impact, known-symbol semantics, semantic edits, Laravel documentation or runtime facts, configuration, Markdown, generated artifacts, review, fallback or proof; also use to scope provider grants for a role. Activating this skill performs no setup. Do not use to implement domain code, author repository documentation, manage durable state, orchestrate agents or prove completion; those belong to the stack owner, /alaa-repo-docs, /alaa-workflow, the installed orchestrator and repository-native gates."
---

# Alaa Code Intelligence Routing

Route each named question to its best available evidence owner, consume the answer, and finish with native proof. This skill owns routing, not domain implementation, documentation authoring, workflow state, agent allocation or proof itself.

## Decision procedure

1. Name independently answerable questions and their intended worktree/environment.
2. Before selecting an owner, handling its result or failure, or choosing a grant, read `references/00-topic-map.md`; it selects the sole reference owning that decision.
3. Apply the routing contract: select one primary owner, reuse adequate evidence, and ask only the missing question.
4. Treat editing, runtime observation and proof as distinct questions; execute applicable authorized native gates.

## Authority

Routing grants no additional authority. Do not change MCP, hooks, CodeGraph, Serena, Boost or language-server integrations/configuration unless explicitly asked for setup, upgrade, repair or removal. Index lifecycle effects require authorization too. Native sandbox restrictions do not establish MCP enforcement; use the scoped grant owner before assigning tools.

## When NOT to use

- An exact native/domain owner is already named and no routing choice exists.
- Domain implementation, repository-document authoring, durable state or agent allocation is the task itself.
- Static evidence is being used to prove another repository, runtime behavior or completion.
- Unsupported artifacts are being forced through a graph or semantic backend.

## Output

Report outcome, question, primary owner, established evidence, fallback gaps/owners/lost guarantees, worktree/environment identity, changed artifacts, observed native command/results and partial or blocked claims. Do not emit raw transcripts.

## Stop and failure

Success requires answered questions, aligned artifacts and observed passing mandatory native gates in the same worktree. Stop a dependent step when missing facts, mismatched identity, unsupported safe operations, unauthorized effects or failed mandatory proof prevent it; report the blocker and continue unrelated safe work. The routing contract owns fallback termination and retry budgets.
