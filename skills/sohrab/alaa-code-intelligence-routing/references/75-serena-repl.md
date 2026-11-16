# Serena REPL alongside CodeGraph

This file covers interface mechanics and API steering. Its advice authorizes no configuration change. `references/80-agent-scoping.md` decides execution authority.

## Discover and consume

- `agent_interface` is `tools` or `REPL`, fixed at startup; the startup project or the CLI can override the global setting. REPL exposes `serena_repl` plus session-management tools that have no REPL counterpart. A missing legacy MCP tool name does not establish a missing semantic capability.
- Before you rely on an operation, inspect its signature and returned types with `s.info("lsp.find_symbol")` or the matching facade or method. Use `s.overview()` when the advertised inventory is missing or stale. Discover only what the question needs.
- Verify the project identity through the supported configuration surface, such as `s.cfg.get_current_config()`.
- LSP and JetBrains expose different APIs, not interchangeable names. The `ide` context name selects no language backend and no same-named facade.
- Invalidate session results after an edit, after a change of project, backend or mode, and after a reconnection. Clients of one shared HTTP server share no Python session variables.
- Do not repeat CodeGraph source retrieval because one Python call can combine symbol overview, body and references. Keep those APIs for distinct semantic questions and for the fallback during a graph outage.
- A batch with possible writes is not a transaction and can partially succeed. Reconcile every attempted mutation before a retry, under `references/10-routing-contract.md` *Mutation uncertainty*.

## Configuration semantics

- `excluded_tools`, `included_optional_tools` and `fixed_tools` govern the tools interface, not REPL operations. For REPL, use `included_apis` and `excluded_apis` with `facade` or `facade.method` identifiers. This file establishes no wildcard recipe.
- `included_apis` is additive, not an exclusive allowlist: nonoptional methods stay available by default. To admit selected methods only, exclude the containing facade and include those methods in the same definition. Including a whole facade does not enable its optional methods.
- Each definition processes exclusions before inclusions. Layers apply in this order: global configuration, context, active modes, project configuration. A later layer can change an earlier choice, and project read-only filtering also removes edit-marked methods. These facts come from the source snapshot in `references/90-source-map.md`: inspect the final inventory.
- Configure the narrowest owner: a project for project-specific policy, or an explicitly selected custom context for a reusable client profile. Preserve unrelated configuration, and inspect mode overrides. A project `initial_prompt` is a prompt, not an API filter.

## Candidate LSP profile

For a coding session with authorized local semantic edits, CodeGraph discovery and native file and shell tools, this project or global fragment keeps semantic reads, rename and symbol-body edits. It omits generic file and text edits, shell, provider memory, external-project access, deletion and server restart. Optional symbol diagnostics depend on backend support. API availability grants no task permission to mutate.

```yaml
agent_interface: REPL
excluded_apis:
  - cfg
  - fs
  - edit
  - mem
  - shell
  - ext
  - lsp
  - jb
included_apis:
  - cfg.get_current_config
  - lsp.find_symbol
  - lsp.get_symbols_overview
  - lsp.find_declaration
  - lsp.find_referencing_symbols
  - lsp.find_implementations
  - lsp.get_diagnostics_for_file
  - lsp.get_diagnostics_for_symbol
  - lsp.rename_symbol
  - edit.replace_symbol_body
  - edit.insert_before_symbol
  - edit.insert_after_symbol
```

The owner's project services run a variant of this candidate since 2026-11-15: a live probe of each service listed the facades `cfg`, `edit` and `lsp` only, with no shell, file or memory facade and without `lsp.safe_delete_symbol`.

- Reconcile every facade and method with the installed version: a newly introduced default facade stays enabled unless it is excluded.
- For another backend, derive a narrow profile from observed signatures and semantic support. Do not substitute prefixes blindly.
- Re-enable an operation only for a named gap and under an authorized configuration change. An eligible native fallback needs no profile expansion.
- For an analysis-only steering profile, omit rename and the three edit methods. That still makes REPL no read-only security boundary; `references/80-agent-scoping.md` owns that decision.

## Validate an authorized application

Start or reconnect only within setup authority, and disrupt no other client's session. In each client, confirm the intended root, the startup context and interface, and the effective API overview: unwanted APIs are absent, and required methods survive the overrides by context, mode and project. Then perform one bounded semantic read. A static check of configuration or source proves no live enforcement. Report each check that you did not run.
