# Routing-hook topology

The vendor or runtime owns hook syntax and lifecycle behavior. This file decides only which routing hooks may coexist without duplicate discovery.

Apply Serena hook guidance only where Serena is configured and hook work is authorized. Without Serena, skip its hook profiles: CodeGraph, native language operations and Boost need no Serena activation, reminder or cleanup hook.

## Ownership

- **CodeGraph.** Its installer owns its MCP registration, marker-fenced instructions, permissions and any compatible prompt hook. Copy no second CodeGraph hook from this pack.
- **Serena activation and cleanup.** Project-local Serena hooks own them. Every hook here is opt-in per the vendor. Lifecycle activation is the one hook worth running everywhere: it restores the server's instructions after the context that held them is gone.
- **Reminder hook.** Omit it where a structural index is the primary discovery owner. Keep it where the semantic owner is: there it is the cheapest defence against the grep-and-read loop. The register below holds the reason. Recheck it against the installed version. The matcher differs per client: copy the vendor's matcher for the client at hand.
- **Auto-approval.** It suppresses per-call prompts for matched Serena operations, and only while the client already reports a permissive permission mode. It does not broaden that mode. Keep the vendor's matcher. A read-only lane's boundary belongs in its tool grant, as `references/80-agent-scoping.md` states, not in a hook matcher.
- **One configuration owner per hook operation.** Do not rely on cross-layer replacement or deduplication. Inspect the effective hooks, and remove semantically duplicate entries from the layer you control.
- **Passive evaluation hooks** may observe events. They must not alter permissions, tool output or routing decisions.

## Adoption

`SKILL.md` *Authority* decides whether you may change hook or MCP configuration.

1. Verify that the CodeGraph root, the Serena active project and the Git root resolve to the same worktree.
2. Read the installed CodeGraph and Serena help and the target runtime's official hook schema.
3. Let the CodeGraph installer create or repair its own entries.
4. Merge exactly one Serena profile: `codegraph-indexed` or `no-codegraph`.
5. Parse the effective JSON or TOML, and inspect the runtime's effective hook list.
6. Exercise activation, one known-symbol Serena request and cleanup. In the no-CodeGraph profile only, exercise one reminder case.
7. Record the project-local delta and the rollback path.

Hook activation changes no evidence ownership.

For REPL, verify how the installed hook classifies `serena_repl` and its composed calls. A legacy symbolic-tool matcher proves no counter reset, no per-API approval and no plan-mode enforcement. `references/80-agent-scoping.md` decides execution boundaries. Never add auto-approval to make up for missing API-level matching.

## Rollback

Remove only the entries that came from this pack. Preserve managed, user, plugin, vendor and unrelated project hooks. Parse the effective configuration again, inspect the remaining hooks, and verify manual routing in the same worktree.

## Recorded deviations from vendor defaults

Record here, with its evidence, each difference between a hook profile and the vendor's published example. Copy everything that is not listed verbatim. A deviation that was not observed stays a candidate, because reasoning is not evidence.

**Adopted.**

| Deviation | Where | Evidence |
|---|---|---|
| The reminder hook is omitted | Both `codegraph-indexed` profiles | The hook's own source. It counts recent text-search and code-file-read calls, denies the call that crosses the threshold, then stays quiet for a cooldown window. Its counters reset only on the semantic server's symbolic tools, not on its pattern-search, file-read, diagnostics or memory tools, and never on a structural-discovery server. One exploration call and reads of the files it named therefore add counts that nothing resets, until a deny routes to the wrong owner. The conflict lives in that one reset condition and disappears if it widens |
| The vendor prompt hook runs behind a gate that requires the prompt to name an indexed symbol or an indexed code file | The `UserPromptSubmit` entry of both runtimes | Replay of one week of typed prompts in one Laravel repository, CodeGraph 1.6.2, 2026-11-15: the vendor hook matches prompt words lexically and injected source for prompts that named no symbol. Behind the gate, injected text fell from about 140,000 to about 37,000 characters. The gate fails open, and a vendor reinstall can restore the bare entry |

**Candidate, not adopted.** Extend session-start activation to the clear and compact events on the runtime that documents all four matchers. Reason: after those two events the server's instructions have just left context, and the same vendor already matches all events on the other runtime. Adopt it only after a test shows that the instructions are lost after those events, that activation restores them, and that no duplicate activation or project switch results. Then change the hook file and this register together.

Verify the feature flag and event names against the runtime's own documentation, not the server's, which can lag: a flag renamed upstream can survive only as a deprecated alias.
