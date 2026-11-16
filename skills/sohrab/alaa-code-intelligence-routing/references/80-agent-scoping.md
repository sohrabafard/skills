# Per-role grants

Grant only the operations that the role's dispatched questions require. A model name or a role name grants nothing. For the runtime syntax of a grant, read /alaa-prompting-guide.

## Classes

| Class | Needed question | Eligible grant |
|---|---|---|
| none | Native read, search or command evidence, release state or manifests | No code-intelligence server |
| discovery | Unknown location, source relationships, paths or impact | Observed structural read operations |
| discovery+semantic-read | Exact symbol facts that a role may judge | Discovery plus verified backend read operations |
| full | Authorized symbol-scoped writes | Required reads plus individually supported edit operations |

A read-only role never gets full. A declared-command verifier gets none. Boost is a separate axis with distinct grants: docs and versions; schema and connections; URLs and routes; logs and browser observations; execution and writes. Compose only the groups that the role needs.

## Exact allowlists

In Claude Code, the semantic-read grant is the built-in `LSP` tool. It reads only and runs no second process. Where the Serena tools interface is active instead, start from the observed supported equivalents of `find_symbol`, `get_symbols_overview`, `find_referencing_symbols`, `find_declaration`, `find_implementations` and `get_diagnostics_for_file`. Optional symbol diagnostics and backend-specific declaration, reference, hierarchy or inspection operations become eligible only after you verify their exact inventory and read semantics. A remembered name grants nothing.

An unknown operation is not read-safe. A read-only grant excludes edits, file creation and deletion, shell, memory writes, activation, onboarding, and unrestricted REPL or debug execution. A read query through a general execution tool needs an observable restriction to that read set.

API filters, project `read_only` and the removal of `shell` do not make `serena_repl` a semantic-read grant. They only steer the exposed methods; Python keeps the Serena process's permissions. For a strictly read-only role, grant individually exposed read tools of the tools interface, or use separately verified process isolation that enforces the boundary. With neither, withhold REPL and report the missing semantic surface. Approval of one call covers every operation composed inside it, so authorize the actual code and its effects, not the tool name.

MCP runs in a separate process. A native sandbox, a permission mode or a withheld native edit tool does not restrict its filesystem or shell effects. Grant an exact read allowlist, never a whole server or a stale denylist. When the runtime cannot demonstrate the restriction, report enforcement unavailable.

## Reachability and validation

- The repository binding and this skill must reach every granted role through orchestrator-owned wiring. Do not grant general skill discovery for that purpose. Where runtime inheritance is undocumented, observe the loading.
- After each change to a definition or to the inventory, inspect the resolved effective tools; a parse of the definition is insufficient. Confirm that a read-only role reaches no write and no execution.
- Confirm launch behavior in each target repository shape, including an absent server. Where absent-server behavior is unobserved, use a stack-specific definition.
- The grant lives in the role definition. Dispatch prose cannot widen it: report a missing grant, and never ask the role to bypass its tools.
