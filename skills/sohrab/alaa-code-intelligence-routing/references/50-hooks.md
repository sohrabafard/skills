# Routing-hook topology

The vendor or runtime owns executable hook syntax and lifecycle behavior. This skill owns only which routing behavior may coexist without duplicate discovery.

Apply Serena hook guidance only where Serena is configured and hook work is authorized. Without Serena, skip its hook profiles entirely; CodeGraph, native language operations and Boost need no Serena activation, reminder or cleanup hook.

## Ownership

- The CodeGraph installer owns its MCP registration, marker-fenced instructions, permissions and any compatible prompt hook. Do not copy a second CodeGraph hook from this pack.
- Project-local Serena hooks own activation and cleanup for the project.
- The reminder hook is a burst breaker, not a nudge. It counts recent text-search and code-file-read calls, denies the call that crosses the threshold, then resets and stays quiet for a cooldown window. Where the semantic owner is the intended destination, it is the cheapest defence against the grep-and-read loop.
- Its counters reset only on a call to the semantic server's own symbolic tools. The server's pattern-search, file-read, diagnostics and memory tools are not symbolic, so a structural-discovery server is invisible to it.
- Omit the reminder wherever a structural index is the primary discovery owner; keep it wherever the semantic owner is. Reason: an agent that follows the graph correctly, with one exploration call and then reads of the files it named, accumulates read counts that nothing resets, until it is denied and sent to the semantic owner. Recheck this against the installed version, because the conflict lives in one reset condition and disappears if that condition widens.
- Its matcher is client-specific: every tool call where the client exposes separate search and read tools, and the shell tool alone where the client runs both through the shell. Copy the vendor's matcher for the client at hand rather than choose one.
- Every hook here is opt-in per the vendor. Lifecycle activation is the one worth running everywhere, because it restores the server's instructions after the context that held them is gone. Whether to extend it beyond the vendor's events is a measurement, not a deduction; the deviation register below holds the open case.
- Auto-approval does not broaden the selected permission mode, but it suppresses per-call prompts for matched Serena operations inside that mode. It emits an allow decision only while the client already reports a permissive permission mode, and stays silent otherwise. Keep the vendor's own matcher. A read-only lane's authority boundary belongs in its tool grant, as `references/80-agent-scoping.md` states, not in a hook matcher.
- One hook operation has one configuration owner. Do not rely on cross-layer replacement or deduplication; inspect effective hooks and remove semantically duplicate entries from the layer you control.

## Adoption

1. Verify that CodeGraph root, Serena active project and Git root resolve to the same worktree.
2. Inspect installed CodeGraph and Serena help and the target runtime's official hook schema.
3. Let the CodeGraph installer create or repair its own entries.
4. Merge exactly one Serena profile: `codegraph-indexed` or `no-codegraph`.
5. Parse the effective JSON or TOML and inspect the runtime's effective hook list.
6. Exercise activation, one known-symbol Serena request, cleanup and, only in the no-CodeGraph profile, one reminder case.
7. Record the project-local delta and rollback path. Hook activation does not change evidence ownership. `SKILL.md` *Authority* owns the rule for changing hook or MCP configuration.

For REPL, verify how the installed hook classifies `serena_repl` and its composed calls. Legacy symbolic-tool matchers prove neither counter resets nor per-API approval or plan-mode enforcement. The topic map's grant owner decides execution boundaries; do not add auto-approval to compensate for missing API-level matching.

## Rollback

Remove only entries introduced from this pack. Preserve managed, user, plugin, vendor and unrelated project hooks. Re-parse the effective configuration, inspect remaining hooks, and verify manual routing in the same worktree.

Passive evaluation hooks may observe events but must not alter permissions, tool output or routing decisions.

## Recorded deviations from vendor defaults

Record here, with its evidence, each way a hook profile differs from the vendor's published example. Copy everything not listed verbatim and keep it so. A deviation not yet observed belongs in the candidate list, not the adopted one, because reasoning is not evidence.

**Adopted.**

| Deviation | Where | Evidence |
|---|---|---|
| The reminder hook is omitted | Both `codegraph-indexed` profiles | The hook's own source: its counters reset only on the semantic server's symbolic tools, so correct graph-driven reads eventually trip a deny that routes to the wrong owner. |
| The vendor prompt hook runs behind a gate that requires the prompt to name an indexed symbol or an indexed code file | The `UserPromptSubmit` entry of both runtimes | Replay of one week of typed prompts in one Laravel repository, CodeGraph 1.6.2, 2026-11-15: the vendor hook matches prompt words lexically and injected source for prompts that named no symbol; behind the gate, injected text fell from about 140,000 to about 37,000 characters. The gate fails open, and a vendor reinstall can restore the bare entry. |

**Candidate, not adopted.** Extend session-start activation to the clear and compact events on the runtime that documents all four matchers. Reason: those two events are when the server's instructions have just left context, and the same vendor already matches all events on the other runtime. It stays unadopted until observed. Adopt it only after a test shows that the instructions are lost after those events, that activation restores them, and that no duplicate activation or project switch results; then change the hook file, this register and the checker together.

Verify the feature flag and event names against the runtime's own documentation rather than the server's, which can lag: a flag renamed upstream may survive only as a deprecated alias.
