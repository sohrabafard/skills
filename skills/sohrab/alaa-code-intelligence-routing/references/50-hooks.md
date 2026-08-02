# Routing-hook topology

The vendor or runtime owns executable hook syntax and lifecycle behavior. This skill owns only which routing behavior may coexist without creating duplicate discovery.

## Ownership

- The CodeGraph installer owns its MCP registration, marker-fenced instructions, permissions, and any compatible prompt hook. Do not copy a second CodeGraph hook from this pack.
- Project-local Serena hooks own activation and cleanup for the project.
- A Serena reminder may be used when CodeGraph is not available. Omit it in a CodeGraph-indexed project because it cannot prove that graph discovery already answered the question and may re-trigger grep or symbol exploration.
- Serena auto-approval is not a default. It can approve semantic edit tools as well as reads; enable the optional fragment only when project permission policy explicitly authorizes that entire matched tool surface.
- One hook operation has one configuration owner. Do not rely on cross-layer replacement or deduplication; inspect effective hooks and remove semantically duplicate entries from the layer you control.

## Adoption

1. Verify CodeGraph root, Serena active project, and Git root resolve to the same worktree.
2. Inspect installed CodeGraph and Serena help and the target runtime's official hook schema.
3. Let the CodeGraph installer create or repair its own entries.
4. Merge exactly one Serena profile: `codegraph-indexed` or `no-codegraph`.
5. Parse the effective JSON or TOML and inspect the runtime's effective hook list.
6. Exercise activation, one known-symbol Serena request, cleanup, and—only in the no-CodeGraph profile—one reminder case.
7. Record the project-local delta and rollback path. Hook activation does not change evidence ownership. Do not modify hook or MCP configuration unless the task explicitly requests setup, upgrade, repair, or removal.

## Rollback

Remove only entries introduced from this pack. Preserve managed, user, plugin, vendor, and unrelated project hooks. Re-parse the effective configuration, inspect remaining hooks, and verify manual routing in the same worktree.

Passive evaluation hooks may observe events but must not alter permissions, tool output, or routing decisions.
