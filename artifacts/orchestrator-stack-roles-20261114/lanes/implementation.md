# Implementation lane: STATUS: COMPLETE
General-purpose subagent, requested opus/high. It worked in the main working tree, made no commit, ran no installer with apply and no Beads command.
Delivered: the optional `binding` in `alaa-prompting-guide/scripts/profile_projection.py`; four wrapper entries per runtime; registrations in both model policies (minor policy version bump, as commit 51b52edb did for an earlier profile addition); the role names in `validate_pack.py` and `check_agent_grants.py` of both orchestrators; two contract lines; routing, catalog and dispatch-template text as its last edits; VERSION 5.7.0 and CHANGELOG entries; the four role names in the Codex Persian README role list.
Deviations it reported:
- It added the four names to the hard-coded role sets in `alaa-prompting-guide/scripts/claude_model_policy.py` and `codex_model_policy.py`, outside the listed paths, because the policy loader fails without them. Accepted: data only.
- The dispatch `<skills>` field keeps the full resolved bindings and adds only "each written as a call, never as a bare mention", because `alaa-workflow references/companion-routing.md` and the common envelope require full bindings. The planned catalog sentence "the dispatch names only a skill the binding does not cover" was dropped for the same reason. Accepted.
- Codex wording follows that runtime's own routes and class names; the Codex catalog paragraph sits under the implementation table because that file has no skills section.
- No checker logic changed. `check_agent_contracts.py` needed no change in either runtime.
Gates it observed: every gate exit 0 on its final tree; render check exit 0 in both runtimes after the renderer change and before any role was added.
Not verified by the lane: the ValueError branches of the binding code (no self-tests); the Codex installer (not run).
