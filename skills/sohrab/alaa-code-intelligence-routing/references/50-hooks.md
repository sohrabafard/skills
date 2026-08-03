# Routing-hook topology

The vendor or runtime owns executable hook syntax and lifecycle behavior. This skill owns only which routing behavior may coexist without creating duplicate discovery.

## Ownership

- The CodeGraph installer owns its MCP registration, marker-fenced instructions, permissions, and any compatible prompt hook. Do not copy a second CodeGraph hook from this pack.
- Project-local Serena hooks own activation and cleanup for the project.
- The reminder hook is a burst breaker, not a nudge. It counts recent text-search and code-file-read calls and denies the call that crosses the threshold, then resets and stays quiet for a cooldown window. Where the semantic owner is the intended destination, that is the cheapest defence there is against the grep-and-read loop.
- Its counters reset on one event only: a call to the semantic server's own symbolic tools. No other tool resets them, and the server's pattern-search, file-read, diagnostics and memory tools do not count as symbolic either. A structural-discovery server is therefore invisible to it.
- That makes the hook and a code graph mutually exclusive in the same profile. An agent following the graph correctly — one exploration call, then reads of the files it named — accumulates read counts that nothing can reset, until it is denied for doing exactly the right thing and told to use the semantic owner instead. Omit the reminder wherever a structural index is the primary discovery owner; keep it wherever the semantic owner is.
- Its matcher is client-specific and follows how that client performs searches and reads: every tool call where the client exposes separate search and read tools, and the shell tool alone where the client runs both through the shell. Copy the vendor's matcher for the client at hand rather than choosing one.
- Every hook here is opt-in per the vendor, and lifecycle activation is the one worth running everywhere: it is what restores the server's instructions after the context that held them is gone. Where the client supports it, extend activation to the clear and compact events as well as start and resume, because that is exactly when the instructions have just been lost.
- Auto-approval for the semantic server grants nothing new. It emits an allow decision only while the client already reports a permissive permission mode, and it stays silent otherwise, so it aligns the server's tools with the mode the user already chose instead of widening it. Without it, a permissive mode covers the client's own edit tools while every semantic edit still prompts — pure friction. Keep the vendor's own matcher; the authority boundary for a read-only lane belongs in that lane's tool grant, which is where `references/80-agent-scoping.md` puts it, not in a hook matcher.
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

## Recorded deviations from vendor defaults

A hook profile that differs from the vendor's published example is a claim that the vendor was wrong
for this repository, so each difference is recorded here with the evidence behind it. Anything not
listed is copied verbatim and must stay that way.

| Deviation | Where | Why |
|---|---|---|
| The reminder hook is omitted | Both `codegraph-indexed` profiles | Its counters reset only on the semantic server's symbolic tools, so structural-index calls never clear them and correct graph-driven reads eventually trip a deny that routes to the wrong owner. |
| Activation also fires on clear and compact | Codex profiles | The runtime documents all four session-start matchers, and the two the vendor omits are precisely the moments the server's instructions have just been dropped from context. |

Verify the feature flag and event names against the runtime's own documentation rather than the
server's, which can lag: a flag renamed upstream may survive only as a deprecated alias.

