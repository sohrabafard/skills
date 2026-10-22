---
name: gortex-add-test
description: "Add tests for under-tested code and coverage gaps."
---
# Add Tests with Gortex

1. Localize the behavior with `explore`.
2. Confirm the specific gap with `change({operation: "tests", source: {symbols: ["<id>"]}})`. Use repository-wide `analyze({kind: "untested"})` or path-scoped `analyze({kind: "coverage_gaps", options: {path_prefix: "<path>"}})` only for broader coverage discovery.
3. Inspect callers with `relations({operation: "callers", target: {symbol: "<id>"}})` and request targets with `change({operation: "tests", source: {symbols: ["<id>"]}})`.
4. Add the narrowest test with `edit({operation: "file", target: {file: "<existing test path>"}, ...})`; use operation `write` for a new test file.
5. Run the test, then require `change` operations `detect` and `guards`.

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
