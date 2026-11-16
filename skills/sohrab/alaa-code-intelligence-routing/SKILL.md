---
name: alaa-code-intelligence-routing
description: "Evidence routing for CodeGraph, optional Serena, the Claude Code LSP tool, gopls, PHPantom, Pyright, Laravel Boost and native tools. Use to select an owner for discovery, call paths, impact, symbol semantics, diagnostics, semantic edits, Laravel docs/runtime facts, configuration, Markdown, generated artifacts, review, fallback or proof, including work without Serena and CLI versus LSP capability checks; also use to scope provider grants for a role. Activating this skill performs no setup. Do not use to implement domain code, author repository documentation, manage durable state, orchestrate agents or prove completion; those belong to the stack owner, /alaa-repo-docs, /alaa-workflow, the installed orchestrator and repository-native gates."
---

# Alaa Code Intelligence Routing

Select one evidence owner for each question and reuse its answer. Native gates own proof.

## Decision procedure

1. For a source question in a repository whose root, or whose main checkout's root, holds `.codegraph/`, apply the operation card.
2. Read `references/00-topic-map.md` before you select an owner that the card does not name, handle a result gap or a failure, choose grants, or advise on Serena contexts or REPL APIs.

## Operation card

| Question | Operation |
|---|---|
| Location of a named symbol | `codegraph query <name>`; MCP `codegraph_search` |
| Callers of a named symbol | `codegraph callers <name>`; MCP `codegraph_callers` |
| Source of one named symbol or one indexed file | `codegraph node <name>`; MCP `codegraph_node` |
| How an area works, a call path or impact, with the location unknown | `codegraph explore "<symbol names>"`; MCP `codegraph_explore` |
| Exact definition, complete references, implementations, typed callers or the type of a symbol | Claude Code: the `LSP` tool at the position that the query operation returned; load the tool by name when it is deferred. Codex: the gopls CLI in `references/45-native-tools.md` for Go, or configured Serena. Where neither answers, record the missing guarantee |
| Replace or insert a whole symbol body, or rename a symbol across files | Configured Serena: `serena_repl` with `s.edit` and `s.lsp.rename_symbol`. Call `initial_instructions` once for the session id. Compose the reads and edits of one change in one call, and return only the result you need |
| Known lines of a file | The runtime's file-read tool with a line range. Use `sed -n` only where the runtime reads files through the shell |
| Literal text, Markdown, configuration, logs or a shell script | `rg` |

- Explore returns one large fixed budget of source for every query: send a narrow question to its narrow operation.
- Matching is lexical. Query with symbol and file names, not prose.
- Find a symbol name in indexed source through the query operation. Use `rg` for it only after that operation gave no adequate answer.
- Do not read again a file that an operation returned.
- Where the MCP tool is not exposed, use the CLI form.
- Before you rename, delete or change the signature of a symbol, get its references from the language service: CodeGraph edges are name-based and can miss or add a caller.

**Lane worktree.** In a linked Git worktree whose root holds no `.codegraph/codegraph.db`, run `codegraph init -y` once in that root before the first query, and `codegraph sync` there before a query about code that the lane changed. The card grants these two effects in the lane's own worktree only. The index is removed with the worktree. When the init fails, read `references/10-routing-contract.md` *Selection and identity* before you use a main-checkout result. Serena reads and edits the main checkout: in a lane worktree, edit with the native tools, never through Serena.

## Authority

Routing grants no authority. Change no MCP, hook, CodeGraph, Serena, Boost or language-server integration or configuration unless the task explicitly asks for its setup, upgrade, repair or removal. The same holds for an index lifecycle effect, except the lane-local index above. A native sandbox does not restrict an MCP server: before you assign tools to a role, apply `references/80-agent-scoping.md`.

## When NOT to use

- An exact native or domain owner is already named, so no routing choice exists.
- The task itself is domain implementation, repository-document authoring, durable state or agent allocation.
- Static evidence would have to prove another repository, runtime behavior or completion.
- An unsupported artifact would be forced through a graph or semantic backend.

## Output

Report the established evidence with its owner, each fallback with its gap and lost guarantee, the worktree and environment of the evidence, and each partial or blocked claim. Emit no raw transcript.

## Stop and failure

The work is done when each question is answered and every mandatory native gate was observed to pass in the same worktree. Stop a dependent step on a missing fact, a mismatched identity, an unsupported or unauthorized operation, or a failed mandatory gate. Report the blocker and continue unrelated safe work. `references/10-routing-contract.md` sets the fallback order and the retry budgets.
