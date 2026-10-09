# Per-role grants

Grant only operations the role's dispatched questions require. The installed orchestrator owns role assignments/definitions; /alaa-prompting-guide owns runtime syntax and capability. A model/role name grants no extra authority.

## Classes

| Class | Needed question | Eligible grant |
|---|---|---|
| none | Native read/search/command evidence, release state or manifests | No code-intelligence server |
| discovery | Unknown location, source relationships, paths or impact | Observed structural read operations |
| discovery+semantic-read | Exact symbol facts a role may judge | Discovery plus verified backend read operations |
| full | Authorized symbol-scoped writes | Required reads plus individually supported edit operations |

A read-only role never earns full. A declared-command verifier earns none. Boost uses a separate axis: docs/versions, schema/connections, URL/routes, logs/browser observations and execution/writes are distinct grants; compose only needed groups.

## Exact allowlists

Start a semantic-read grant from observed supported equivalents of `find_symbol`, `get_symbols_overview`, `find_referencing_symbols`, `find_declaration`, `find_implementations` and `get_diagnostics_for_file`. Optional symbol diagnostics or backend-specific declaration/reference/hierarchy/inspection operations are eligible only after their exact inventory and read semantics are verified. A remembered name grants nothing.

Unknown operations are not read-safe. Exclude edits, file creation/deletion, shell, memory writes, activation/onboarding and unrestricted REPL/debug execution from a read-only grant. An advertised read query through a general execution tool is insufficient without observable restriction to that read set.

MCP executes in a separate process; native sandbox/permission modes and withheld native edit tools do not enforce its filesystem/shell effects. Use an exact read allowlist rather than a whole-server grant or stale denylist. Report enforcement unavailable when the runtime cannot demonstrate the restriction.

## Reachability and validation

The repository binding and named routing skill must reach every granted role through orchestrator-owned wiring. Do not grant general skill discovery solely to make this contract reachable. Observe loading where runtime inheritance is undocumented.

Inspect resolved effective tools, not only definition syntax. Confirm read-only roles cannot reach writes/execution, and launch behavior in each target repository shape, including absent servers. If absent-server behavior is unobserved, use a stack-specific definition rather than assume graceful startup. Recheck after definition/inventory changes; parse alone is insufficient.

The grant lives in the role definition. Dispatch prose cannot widen it; report a missing grant rather than ask the role to bypass its tools.
