---
name: alaa-code-intelligence-routing
description: "Evidence routing for CodeGraph, optional Serena, the Claude Code LSP tool, gopls, PHPantom, Pyright, Laravel Boost and native tools. Use to select an owner for discovery, call paths, impact, symbol semantics, diagnostics, semantic edits, Laravel docs/runtime facts, configuration, Markdown, generated artifacts, review, fallback or proof, including work without Serena and CLI versus LSP capability checks; also use to scope provider grants for a role. Activating this skill performs no setup. Do not use to implement domain code, author repository documentation, manage durable state, orchestrate agents or prove completion; those belong to the stack owner, /alaa-repo-docs, /alaa-workflow, the installed orchestrator and repository-native gates."
---

# Alaa Code Intelligence Routing

Select the evidence owner for each question. Native gates own proof.

## Decision procedure

1. Name each independently answerable question and its target worktree and environment.
2. For a source question in a repository whose root holds `.codegraph/`, apply the operation card.
3. Read `references/00-topic-map.md` before selecting an owner that the card does not name, handling results or failures, choosing grants, or advising on Serena contexts or REPL APIs.
4. Apply the routing contract: select one primary owner, reuse adequate evidence, and ask only the missing question.
5. Treat editing, runtime observation and proof as separate questions. Run the applicable authorized native gates.

## Operation card

| Question | Operation |
|---|---|
| Location of a named symbol | `codegraph query <name>`; MCP `codegraph_search` |
| Callers of a named symbol | `codegraph callers <name>`; MCP `codegraph_callers` |
| Source of one named symbol or one indexed file | `codegraph node <name>`; MCP `codegraph_node` |
| How an area works, a call path or impact, with the location unknown | `codegraph explore "<symbol names>"`; MCP `codegraph_explore` |
| Exact definition, complete references, implementations, typed callers or the type of a symbol | Claude Code: the `LSP` tool at the position that the query operation returned; load the tool by name when it is deferred. Codex: the language-service CLI in `references/45-native-tools.md` |
| Known lines of a file | The runtime's file-read tool with a line range. Use `sed -n` only where the runtime reads files through the shell |
| Literal text, Markdown, configuration, logs or a shell script | `rg` |

Explore returns one large fixed budget of source for every query, so send a narrow question to its narrow operation. Matching is lexical: query with symbol and file names, not prose. Search indexed source for a symbol name through the query operation first; use `rg` for that name only after the operation gave no adequate answer. Do not read again a file that an operation returned. Use the CLI form where the MCP tool is not exposed. Before you rename, delete or change the signature of a symbol, get its references from the language service: CodeGraph edges are name-based and can miss or add a caller.

In a linked Git worktree whose root holds no `.codegraph/codegraph.db`, run `codegraph init -y` once in that root before the first query. Run `codegraph sync` there before a query about code that the lane changed. This card grants these two effects inside the lane's own worktree only; the index is removed with the worktree. When the init fails, read `references/10-routing-contract.md` *Selection and identity*; it decides which parts of a main-checkout result you may use.

## Authority

Routing grants no additional authority. Do not change MCP, hook, CodeGraph, Serena, Boost or language-server integration or configuration unless explicitly asked for setup, upgrade, repair or removal. Index lifecycle effects also need authorization, except the lane-local index that the operation card grants. Native sandbox restrictions do not prove MCP enforcement. Apply the scoped grant owner before assigning tools.

## When NOT to use

- An exact native or domain owner is already named and no routing choice exists.
- Domain implementation, repository-document authoring, durable state or agent allocation is the task itself.
- Static evidence is meant to prove another repository, runtime behavior or completion.
- Unsupported artifacts are forced through a graph or semantic backend.

## Output

Report outcome, question, primary owner and established evidence; each fallback's gap, owner and lost guarantee; worktree and environment identity; changed artifacts; each observed native command and result; and partial or blocked claims. Emit no raw transcript.

## Stop and failure

Success requires answered questions, aligned artifacts and observed passing mandatory native gates in the same worktree. Stop a dependent step when missing facts, mismatched identity, unsupported safe operations, unauthorized effects or failed mandatory proof prevent it. Report the blocker and continue unrelated safe work. The routing contract owns fallback termination and retry budgets.
