---
name: gortex-rename
description: "Rename a symbol and update every reference atomically."
---
# Rename a Symbol with Gortex

1. Resolve exactly one symbol with `search({operation: "symbols", query: "<old name>"})`.
2. Enumerate references and implementations with `relations` operations `usages` and `implementations`.
3. Run `change({operation: "impact", source: {symbols: ["<id>"]}})`. For a public signature rename, also run `change({operation: "verify", source: {changes: [{symbol_id: "<id>", new_signature: "<signature with new name>"}]}})`.
4. Preview with `refactor({operation: "rename", target: {symbol: "<id>"}, new_name: "<new>", dry_run: true})`, then repeat it with `dry_run: false` to apply.
5. Require `change` operations `detect`, `guards`, and `tests`; confirm no old usages remain.

## Required behavior

- Native Gortex MCP is mandatory for this MCP-configured workflow. If its callable tools are missing, report a Gortex MCP integration failure and stop; do not start a daemon or switch to a CLI/shell fallback.
- Do not substitute shell reads, file search, or Git plumbing.
- Start task-shaped work with `explore`. For one already-known symbol, start with `search`.
- Use `change` before a mutation and again after it. Write only through `edit` or `refactor`.
- Call `capabilities({domain: "<tool>", operation: "<operation>", detail: "schema"})` only when an operation's exact arguments are unclear.
- Report graph-backed paths and symbol IDs. Never invent a result when an operation returns no match.

## Worktree and branch routing

- The session/CWD selects the view. An implicit or session-discovered checkout (including a linked worktree) is an automatic overlay; do not explicitly `track` it. Only an explicit user request to track creates a dedicated logical graph.
- **Overall** means the selected overlay plus exactly one designated primary in its Git family, never a union of incompatible branches. Unique overlay/base matches keep normal relevance order; for a duplicate logical identity the overlay wins, and deletion/tombstone masks hide the base copy.
- Freshness `exact:false` means the requested view was not served. Every fallback is read-only. Use `require_exact:true` to refuse substitution, `require_fresh:true` to await filesystem state, and absolute RFC3339 `wait_deadline` to bound it.
- Select explicitly when CWD is not the target, for example `view:{kind:"worktree",checkout_id:"…"}` or `view:{kind:"git_ref",value:"refs/heads/release",graph_id:"…"}`. Inactive ref/commit views are immutable committed structural/source snapshots: no working-copy LSP, `search.text`, or edits. Approved coordinator-backed exact worktree edits are supported; fallback and ref/commit views are not.
- Explicitly untracking a non-primary dedicated worktree demotes it to automatic only when another ready primary survives. Before primary closure, family forget, or `set-primary`, preview the effects and obtain user confirmation.
