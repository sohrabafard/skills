---
name: alaa-code-intelligence-routing
description: "Evidence routing for CodeGraph, optional Serena, gopls, PHPantom, Pyright, Laravel Boost and native tools. Use to select an owner for discovery, call paths, impact, symbol semantics, diagnostics, semantic edits, Laravel docs/runtime facts, configuration, Markdown, generated artifacts, review, fallback or proof, including work without Serena and CLI versus LSP capability checks; also use to scope provider grants for a role. Activating this skill performs no setup. Do not use to implement domain code, author repository documentation, manage durable state, orchestrate agents or prove completion; those belong to the stack owner, /alaa-repo-docs, /alaa-workflow, the installed orchestrator and repository-native gates."
---

# Alaa Code Intelligence Routing

Select the evidence owner for each question. Native gates own proof.

## Decision procedure

1. Name each independently answerable question and its target worktree and environment.
2. Read `references/00-topic-map.md` before selecting an owner, handling results or failures, choosing grants, or advising on Serena contexts or REPL APIs.
3. Apply the routing contract: select one primary owner, reuse adequate evidence, and ask only the missing question.
4. Treat editing, runtime observation and proof as separate questions. Run the applicable authorized native gates.

## Authority

Routing grants no additional authority. Do not change MCP, hook, CodeGraph, Serena, Boost or language-server integration or configuration unless explicitly asked for setup, upgrade, repair or removal. Index lifecycle effects also need authorization. Native sandbox restrictions do not prove MCP enforcement. Apply the scoped grant owner before assigning tools.

## When NOT to use

- An exact native or domain owner is already named and no routing choice exists.
- Domain implementation, repository-document authoring, durable state or agent allocation is the task itself.
- Static evidence is meant to prove another repository, runtime behavior or completion.
- Unsupported artifacts are forced through a graph or semantic backend.

## Output

Report outcome, question, primary owner and established evidence; each fallback's gap, owner and lost guarantee; worktree and environment identity; changed artifacts; each observed native command and result; and partial or blocked claims. Emit no raw transcript.

## Stop and failure

Success requires answered questions, aligned artifacts and observed passing mandatory native gates in the same worktree. Stop a dependent step when missing facts, mismatched identity, unsupported safe operations, unauthorized effects or failed mandatory proof prevent it. Report the blocker and continue unrelated safe work. The routing contract owns fallback termination and retry budgets.
