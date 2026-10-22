---
name: gortex-cli
description: "Bash-only mirror of Gortex MCP tools for harnesses without MCP support."
---
# Gortex from a Bash-Only Harness

Use this skill only in a harness that has no MCP transport by design. If a Gortex MCP server is configured but its callable tools are missing, report an integration failure; do not use this skill as a fallback.

Every public MCP tool has the same name through `gortex call`:

```bash
gortex call explore --arg task='locate the authentication flow'
gortex call search --arg operation=symbols --arg query=UserStore
gortex call read --arg target='{"symbol":"internal/store.go::UserStore"}'
gortex call relations --arg operation=usages --arg target='{"symbol":"internal/store.go::UserStore"}'
gortex call change --arg operation=impact --arg target='{"symbol":"internal/store.go::UserStore"}'
gortex call edit --arg target='{"file":"internal/store.go"}' --arg match='old text' --arg replacement='new text'
gortex call change --arg operation=detect --arg source='{"scope":"all"}'
```

For an exact operation schema:

```bash
gortex call capabilities --arg domain=read --arg operation=source --arg detail=schema
```

The required order is `explore` → targeted `search/read/relations/trace` → pre-change `change` → `edit/refactor` → post-change `change`. Do not use shell file reads or search as a substitute.

## Worktree and branch routing

- The session/CWD selects the view. An implicit or session-discovered checkout (including a linked worktree) is an automatic overlay; do not explicitly `track` it. Only an explicit user request to track creates a dedicated logical graph.
- **Overall** means the selected overlay plus exactly one designated primary in its Git family, never a union of incompatible branches. Unique overlay/base matches keep normal relevance order; for a duplicate logical identity the overlay wins, and deletion/tombstone masks hide the base copy.
- Freshness `exact:false` means the requested view was not served. Every fallback is read-only. Use `require_exact:true` to refuse substitution, `require_fresh:true` to await filesystem state, and absolute RFC3339 `wait_deadline` to bound it.
- Select explicitly when CWD is not the target, for example `view:{kind:"worktree",checkout_id:"…"}` or `view:{kind:"git_ref",value:"refs/heads/release",graph_id:"…"}`. Inactive ref/commit views are immutable committed structural/source snapshots: no working-copy LSP, `search.text`, or edits. Approved coordinator-backed exact worktree edits are supported; fallback and ref/commit views are not.
- Explicitly untracking a non-primary dedicated worktree demotes it to automatic only when another ready primary survives. Before primary closure, family forget, or `set-primary`, preview the effects and obtain user confirmation.
