# Per-role code-intelligence scoping

A role that cannot ask a server's question gains nothing from holding it, and every unused server costs
tool-description context in that role's window and widens its blast radius. Scope the grant to the
question class the role is dispatched to answer.

This file owns which grant class a question class earns and which tools each class contains. The
installed orchestrator pack owns the per-agent assignment and the agent files; the runtime owns the
frontmatter or TOML syntax that expresses it. Do not restate the roster here.

## Grant classes

| Class | Contains | Earned by a role whose question is |
|---|---|---|
| `none` | no code-intelligence server | manifest, lockfile, markup, CI, release, browser-runtime, or command-evidence shaped — answerable from native read, search, and commands |
| `discovery` | CodeGraph only | unknown location, related symbols, call path, callers, callees, blast radius, or which files to read |
| `discovery+semantic-read` | CodeGraph plus the semantic read set below | the above, plus exact references, declaration, hierarchy, or diagnostics for a symbol the role must judge but may not change |
| `full` | the whole semantic server and CodeGraph | the above, plus symbol-scoped edits the role is authorized to write |

A read-only role never earns `full`. A role that only runs declared commands and reports their output
earns `none` regardless of how senior its model pin is; seniority is not a question class.

## The semantic read set

Grant these Serena tools by exact name, and no others, to a read-only role:
`find_symbol`, `get_symbols_overview`, `find_referencing_symbols`, `find_declaration`,
`find_implementations`, `get_diagnostics_for_file`.

Everything else in that server is either an edit surface, a shell surface, a memory surface, or a
duplicate of a native tool the runtime already sandboxes. Verify the names against the installed
inventory before writing them into an agent file; a name that no longer exists silently grants nothing,
and a new edit tool added upstream is not covered by a stale deny list.

## Why an allow list rather than a deny list

A semantic MCP server is a separate process. Its file writes and shell calls do not pass through the
client's sandbox, permission mode, or withheld native tools, so a role can be sandboxed read-only and
still rename a symbol across the repository through the server. An allow list of read tools is the only
form of the restriction that holds. Where the runtime offers both, express the grant as an allow list
and use the deny list only to remove a whole server.

## Expressing the grant

Both runtimes support server-level and exact-tool-level scoping in the agent definition, and both own
their own syntax. Before editing agent files, confirm the current keys and matching rules in the
runtime's official subagent documentation, then check the result:

- Confirm the effective tool list the role actually receives, not the list the file requests.
- Confirm that a role granted `discovery+semantic-read` cannot reach an edit or shell tool.
- Confirm that a role granted `none` still launches; some runtimes fail a role whose entire tool list
  resolves to nothing.

A grant lives in the agent definition, not in the dispatch. Do not ask a lane to use a server it was not
granted, and do not widen a grant inside a prompt.

## Degraded and absent servers

An agent file may name a server the project has not installed. That is expected in a portable pack and
is not an error to repair per project. Treat it as a capability the role uses when present: the role
still answers its question through native tools, and it labels the answer partial when the lost server
carried a completeness guarantee it cannot otherwise establish.
