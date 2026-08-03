# Per-role code-intelligence scoping

A role that cannot ask a server's question gains nothing from holding it, and every unused server costs
tool-description context in that role's window and widens its blast radius. Scope the grant to the
question class the role is dispatched to answer.

This file owns which grant class a question class earns and which tools each class contains. The
installed orchestrator pack owns the per-agent assignment and the agent files. The runtime owns the
syntax that expresses a grant and the behaviour of a grant that cannot resolve — route those to
`/alaa-prompting-guide` or `$alaa-prompting-guide`, which owns agent-definition syntax and runtime
capability, and verify against that runtime's current documentation rather than a remembered form.

## Grant classes

| Class | Contains | Earned by a role whose question is |
|---|---|---|
| `none` | no code-intelligence server | answerable from native read, search, and commands alone — command evidence, release state, manifests |
| `discovery` | the structural index | unknown location, related symbols, call path, callers, callees, blast radius, or which files to read |
| `discovery+semantic-read` | the above, plus the semantic read set below | exact references, declaration, hierarchy, or diagnostics for a symbol the role must judge but may not change |
| `full` | the above, plus the semantic server's edit surface | symbol-scoped edits the role is authorized to write |

A read-only role never earns `full`. A role that only runs declared commands and reports their output
earns `none` regardless of how senior its model pin is; seniority is not a question class.

Framework-context servers are scoped the same way but on their own axis, because a role's need for
framework documentation is independent of its need for structural discovery. Compose the grant from the
narrowest classes the role's question actually requires — documentation and installed versions, live
schema, URL and route resolution, application error and log surfaces, browser surfaces — rather than
issuing one bundle. A lane that judges migrations has no use for browser logs, and a lane that drives a
browser has no use for the connection inventory.

## The semantic read set

Grant these Serena tools by exact name, and no others, to a read-only role:
`find_symbol`, `get_symbols_overview`, `find_referencing_symbols`, `find_declaration`,
`find_implementations`, `get_diagnostics_for_file`.

Everything else in that server is either an edit surface, a shell surface, a memory surface, or a
duplicate of a native tool the runtime already sandboxes. Verify the names against the installed
inventory before writing them into an agent file; a name that no longer exists silently grants nothing,
and a new edit tool added upstream is not covered by a stale deny list.

Two framework tools stay out of every lane that observes or judges: one executes arbitrary application
code, and one writes durable rule files that other agents then follow. Deny them in the lane and switch
them off at the server, because the two filters are independent.

## Why an allow list rather than a deny list

A semantic MCP server is a separate process. Its file writes and shell calls do not pass through the
client's sandbox, permission mode, or withheld native tools, so a role can be sandboxed read-only and
still rename a symbol across the repository through the server. An allow list of read tools is the only
form of the restriction that holds. Where the runtime offers both, express the grant as an allow list
and use the deny list only to remove a whole server or a named tool from an otherwise inherited set.

## The routing contract must remain reachable

A grant without the contract that chooses among the granted servers recreates the problem the grant was
meant to solve. Two things have to hold together, and the second is easy to lose.

The always-loaded repository binding must reach the role. Where a runtime loads project memory into a
subagent, the binding arrives with it; where that is undocumented, treat it as unproven and confirm by
observation before relying on it.

The role must also be able to act on what the binding says. A binding that tells a role to invoke the
routing skill is inert if that role's tool grant cannot reach the skill surface at all. Any role granted
a code-intelligence server therefore keeps the ability to invoke this skill on demand. Prefer that to
preloading the whole skill into every lane: the binding is short and always present, while the skill is
only needed when a routing decision is genuinely contested, and preloading it everywhere spends context
on every dispatch to answer a question most dispatches never ask.

## Validating a grant

A definition states an intention. Only the resolved grant states a capability, so check the resolution
rather than the file:

- Confirm the effective tool list the role actually receives, and that a role granted the read class
  cannot reach an edit or shell tool.
- Confirm the role launches in each repository shape it will be installed into. A portable definition
  may name a server a given repository lacks, but that is safe only where the runtime has been observed
  to launch the role on the remaining tools; some runtimes refuse a role whose entire tool list resolves
  to nothing. Where it has not been observed, use a stack-specific overlay instead of assuming.
- Re-run the check after any change to the definitions, and treat a parse alone as insufficient — a
  well-formed file can still hand a reviewer an edit tool.

A grant lives in the agent definition, not in the dispatch. Do not ask a lane to use a server it was not
granted, and do not widen a grant inside a prompt.
