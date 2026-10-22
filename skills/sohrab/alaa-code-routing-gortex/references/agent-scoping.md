# Managed agent grants

The server key is `gortex`, with `GORTEX_TOOLS=compact`. Source evidence: [compact MCP contract](https://github.com/zzet/gortex/blob/v0.64.8/docs/mcp.md), inspected 2026-10-22. Tool-level grants cannot restrict individual operation values inside multiplexed tools; effective schema and role authority still govern each call.

Managed role projections are owned by the existing Codex/Claude orchestrator source templates, grant checkers and renderers. This file owns their intended permission boundary; it does not install or materialize them globally.

- Read-only code evidence: explicit tools `explore`, `search`, `read`, `relations`, `trace`, `analyze`, `change`, `recall`, `workspace`, `response`, `capabilities` only. `change` is for inspection/receipt operations, not permission to mutate source; `recall` is retrieval, not permission to ingest memory. `workspace` selects/observes context, not admin registration. Inspect exposed schemas after a release change.
- Implementers add `edit` and `refactor`; `writes.md` still gates each supported operation. A grant does not authorize unrelated files, lifecycle actions, runtime/data writes or a different checkout.
- Do not grant Gortex `ask`, `review`, `pr`, `workspace_admin`, `session`, `overlay`, `remember`, or `publish_review` as routine code evidence. They bring LLM, administrative, memory, session or external effects beyond this role contract. Preserve existing Boost subsets and Hindsight role boundaries.
- Never replace a reviewer's allowlist with a whole-server wildcard. If the runtime cannot enforce a scoped grant, report it; prose is not a technical restriction. Parent tool grants must not silently expand a child.

Gortex's path tools can access the union of tracked roots. Graph workspace scope and the client's native shell sandbox do not constrain MCP to that session's worktree. A Unix socket restricts other OS accounts, not other processes under the same user; a shared HTTP bearer token similarly grants daemon access, not per-repository filesystem authorization. Use only trusted same-user sessions and coordinated ownership here; separate OS/service boundaries are needed for stronger isolation.

Keep old deny entries only where they are deliberate defense for an unmigrated existing installation; they do not install or select Serena/CodeGraph. The old routing package stays intact for unmigrated consumers, but migrated managed sources call the new owner. Global/in-project rules and integration configs remain an operator migration, so source projection checks do not prove live activation.
