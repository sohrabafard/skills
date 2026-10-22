---
name: gortex-pr-review-agent
description: "Coding-agent review verdict via the gortex review verb."
---
# Review a Change as a Sub-Agent

## MCP-capable harness

Native Gortex MCP is mandatory. Call `review({operation: "run", source: {scope: "<scope>"}})`, then use `change` operations `guards`, `tests`, and `contract`. When the proposed signature is known, run operation `verify` before mutation. If the configured callable tools are missing, report a Gortex MCP integration failure and stop; do not start a daemon or use the Bash path below.

## Bash-only harness

Use this path only when the harness has no MCP transport by design:

```bash
gortex review --audience agent --format json
```

In either mode, return `VERDICT: clean` or `VERDICT: findings` followed by actionable findings with severity and `file:line`. Do not replace graph-backed review with ad-hoc `git diff` inspection.

## Worktree and branch routing

- The session/CWD selects the view. An implicit or session-discovered checkout (including a linked worktree) is an automatic overlay; do not explicitly `track` it. Only an explicit user request to track creates a dedicated logical graph.
- **Overall** means the selected overlay plus exactly one designated primary in its Git family, never a union of incompatible branches. Unique overlay/base matches keep normal relevance order; for a duplicate logical identity the overlay wins, and deletion/tombstone masks hide the base copy.
- Freshness `exact:false` means the requested view was not served. Every fallback is read-only. Use `require_exact:true` to refuse substitution, `require_fresh:true` to await filesystem state, and absolute RFC3339 `wait_deadline` to bound it.
- Select explicitly when CWD is not the target, for example `view:{kind:"worktree",checkout_id:"…"}` or `view:{kind:"git_ref",value:"refs/heads/release",graph_id:"…"}`. Inactive ref/commit views are immutable committed structural/source snapshots: no working-copy LSP, `search.text`, or edits. Approved coordinator-backed exact worktree edits are supported; fallback and ref/commit views are not.
- Explicitly untracking a non-primary dedicated worktree demotes it to automatic only when another ready primary survives. Before primary closure, family forget, or `set-primary`, preview the effects and obtain user confirmation.
