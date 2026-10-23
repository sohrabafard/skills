# Serena REPL alongside CodeGraph

Own interface mechanics and API steering. The routing contract selects each question's owner; the grant owner decides execution authority. Advice authorizes no configuration change.

## Discover and consume

Distinguish `agent_interface: tools` from `agent_interface: REPL`. The interface is fixed at startup; the startup project or CLI can override the global setting. REPL exposes `serena_repl` plus session-management tools without REPL counterparts. Missing legacy MCP tool names do not establish missing semantic capability.

Read the current Serena instructions and effective API overview. For a needed operation, inspect `s.info("lsp.find_symbol")` or the corresponding observed facade/method before using its signature or returned types. Use `s.overview()` when the advertised inventory is missing or stale. Verify project identity with the supported configuration surface, such as `s.cfg.get_current_config()`. Discover only what the named question needs; LSP and JetBrains expose different APIs, not interchangeable names. The `ide` context name does not select a language backend or a same-named facade.

Compose operations only after selecting Serena for an unresolved question. Bound paths, output and continuations; return required evidence and coverage limits. Reuse session objects, invalidating affected results after edits, project/backend/mode changes or reconnection. Shared HTTP project state does not imply shared client-session Python variables.

Do not repeat CodeGraph source retrieval merely because Python can combine symbol overview, body and references in one call. Retain those APIs for distinct semantic questions and eligible graph-outage fallback. A batch with possible writes can partially succeed: reconcile every attempted mutation before retrying under the routing contract; it is not a transaction.

## Configuration semantics

- `excluded_tools`, `included_optional_tools` and `fixed_tools` govern the tools interface, not REPL operations. Use `included_apis`/`excluded_apis` with `facade` or `facade.method` identifiers; no wildcard recipe is established here.
- `included_apis` is additive, not an exclusive allowlist. Nonoptional methods remain available by default. To admit selected methods only, exclude the containing facade and explicitly include its selected methods in the same definition. Including a whole facade does not automatically enable its optional methods.
- In the source snapshot linked by reference 90, each definition processes exclusions before inclusions. Layers apply global configuration, context, active modes, then project configuration; later definitions can change earlier choices. Project read-only filtering additionally removes edit-marked methods. Inspect the final inventory rather than infer it from one YAML fragment.
- Configure the narrowest appropriate owner: a project for project-specific policy or an explicitly selected custom context for a reusable client profile. Set the interface in the supported global/project/CLI setting. Preserve unrelated configuration and inspect mode overrides; project `initial_prompt` is a prompt, not an API filter.

## Candidate LSP profile

For a coding session with authorized local semantic edits, CodeGraph discovery and native file/shell tools, this project/global fragment retains semantic reads, rename and symbol-body edits. It deliberately omits generic file/text edits, shell, provider memory, external-project access, deletion and server restart. Optional symbol diagnostics remain subject to backend support. API availability grants no task permission to mutate.

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

This LSP candidate is source-checked, not locally deployed. Reconcile every facade/method with the installed version: newly introduced default facades remain enabled unless excluded. For another backend, derive a narrow profile from observed signatures and semantic support; do not substitute prefixes blindly. Re-enable an operation only for a named gap and authorized configuration change; eligible native fallback needs no profile expansion.

For an analysis-only steering profile, omit rename and the three edit methods. This still does not make REPL a read-only security boundary; reference 80 owns that decision.

## Validate an authorized application

Check installed startup help/schema, parse the merged configuration and start/reconnect only within setup authority. In each client, confirm the same intended root, startup context/interface and effective API overview; inspect a retained method's help and perform one bounded semantic read. Check that unwanted APIs are absent and required methods survive context/mode/project overrides. Confirm that missing or unsupported methods follow the finite fallback contract. Compare results after a relevant mode/project change without disrupting another client's session.

Static configuration/source checks prove neither live enforcement nor client behavior or performance. Report each unrun cell explicitly. Sources, snapshot and refresh obligations belong to reference 90.
