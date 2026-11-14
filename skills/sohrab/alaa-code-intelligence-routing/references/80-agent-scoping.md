# Per-role grants

Grant only the operations that the role's dispatched questions require. The installed orchestrator owns role assignments and definitions. /alaa-prompting-guide owns runtime syntax and capability. A model name or role name grants no extra authority.

## Classes

| Class | Needed question | Eligible grant |
|---|---|---|
| none | Native read, search or command evidence, release state or manifests | No code-intelligence server |
| discovery | Unknown location, source relationships, paths or impact | Observed structural read operations |
| discovery+semantic-read | Exact symbol facts a role may judge | Discovery plus verified backend read operations |
| full | Authorized symbol-scoped writes | Required reads plus individually supported edit operations |

A read-only role never earns full. A declared-command verifier earns none. Boost uses a separate axis: docs/versions, schema/connections, URL/routes, logs/browser observations and execution/writes are distinct grants. Compose only the needed groups.

## Exact allowlists

Start a semantic-read grant from observed supported equivalents of `find_symbol`, `get_symbols_overview`, `find_referencing_symbols`, `find_declaration`, `find_implementations` and `get_diagnostics_for_file`. Optional symbol diagnostics or backend-specific declaration, reference, hierarchy or inspection operations are eligible only after their exact inventory and read semantics are verified. A remembered name grants nothing.

Unknown operations are not read-safe. Exclude from a read-only grant: edits, file creation and deletion, shell, memory writes, activation and onboarding, and unrestricted REPL or debug execution. An advertised read query through a general execution tool is insufficient without observable restriction to that read set.

Serena REPL API filters and project `read_only` steer the exposed methods. Python can still exercise the Serena process's permissions. Neither an API allowlist nor removing `shell` makes `serena_repl` a semantic-read grant. For a strictly read-only role, use individually exposed read tools in the tools interface or separately verified process isolation that enforces the required boundary. If neither is available, withhold REPL and report the missing semantic surface. Whole-call approval also covers any operations composed inside that call. Authorize the actual code and its effects, not the tool name alone.

MCP executes in a separate process. Native sandbox or permission modes and withheld native edit tools do not restrict its filesystem or shell effects. Use an exact read allowlist rather than a whole-server grant or stale denylist. Report enforcement unavailable when the runtime cannot demonstrate the restriction.

## Reachability and validation

The repository binding and named routing skill must reach every granted role through orchestrator-owned wiring. Do not grant general skill discovery solely to make this contract reachable. Observe loading where runtime inheritance is undocumented.

Inspect resolved effective tools, not only definition syntax. Confirm that read-only roles cannot reach writes or execution. Confirm the launch behavior in each target repository shape, including absent servers. If absent-server behavior is unobserved, use a stack-specific definition rather than assume graceful startup. Recheck after a change to a definition or the inventory. A parse alone is insufficient.

The grant lives in the role definition. Dispatch prose cannot widen it; report a missing grant rather than ask the role to bypass its tools.
