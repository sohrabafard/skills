# Effort and Thinking: A Cross-Model Decision Procedure

Owns cross-runtime effort evidence and control validation. Model references own supported levels; runtime orchestrators own actual task choices.

## The two levers do different jobs

**Model** selects judgment; **effort** selects search depth. Choose from the lane's remaining decisions and required search, then verify. Higher effort proves no cross-model equivalence: comparisons vary one factor against the same task and acceptance.

## What effort does not control

Response length, deliverable length, update cadence and scope require explicit prompt controls. Effort can change tokens and tool behavior; lowering it is not a reliable substitute for output/scope constraints. Read the target model reference for observed workload-specific effects.

## Thinking: keep it on, lower the effort instead

Use the registered model capability snapshot and refresh its API documentation before changing
thinking controls. Current model references own modes and exceptions. Haiku 5.5 supports effort and adaptive thinking; its API disabled-thinking exception does not transfer to Claude Code. Historical Haiku 4.5 uses extended thinking without effort. These API controls are not interchangeable Claude Code settings.

For effort-enabled models, compare lower supported effort as a cost lever. Measure retrieval,
tool-use reliability and task quality; report unsupported controls instead of substituting
them. Read `references/36-haiku-5-5.md` for current Haiku controls.

Do not carry manual thinking budgets into current adaptive models. Historical Haiku 4.5 is the extended-thinking exception. The value `adaptive` names a thinking mode, never an effort. Neither `ultra` nor
`ultracode` is a Claude API effort value; harness orchestration modes require separate proof.

## Choosing a starting level

Read the target's reference for supported levels, default and workload starting point; shared effort names do not imply shared search depth. An inherited effort is untested: refresh guidance and retain unrun status. Selection requires no experiment.

## The decision procedure

1. **Resolve missing evidence.** Retrieve or clarify absent context, capability or intent; a different model does not supply missing facts.
2. **Obtain the task selection from its owner.** The runtime orchestrator selects model AND effort for each authority role through its routing matrix, using `references/90-model-selection.md` as evidence. Planning and implementation are separate actual tasks; role names and vendor defaults do not allocate them.
3. **Validate capabilities and realization.** Check both explicit controls against the structured capability policy and actual host. Inspect loaded definitions, pins, fork restrictions, force/environment/provider overrides and caps. Missing, unsupported or mismatched controls block the affected lane; use only an available exact verified compatibility realization, never invented fallback.
4. **Separate selection from calibration.** Comparisons hold task/context/tools/authority/acceptance constant and vary one factor. Compare cost only among passing outcomes. Recommendations and selected pairs remain unmeasured until task-specific evidence exists; selection requires no paid experiment or replay.
5. **Preserve authority.** Model controls change neither scope, tools, verdict responsibilities nor independent gates. Main-session configuration stays external. Source consistency does not prove installed activation or observed serving identity.


## Capability registries and realized controls

The structured Codex/Claude policies register neutral role identities and supported pairs. Supported levels are capabilities, not task recommendations or role-wide ceilings. Historical entries do not authorize active selection. The runtime orchestrator owns actual task admission, priority and deliberate departures; this skill validates controls without allocating work.

Stale executable pins can defeat caller controls. Read the target runtime reference and verify the loaded definition, explicit pair and effective resolution. A source edit does not reload the current registry. Use an available exact verified realization or block the affected lane; never silently substitute or change installed configuration. Unknown observed identity is a reporting limit when configured resolution is established, not a requirement for paid probing.

Task comparisons stay separate evidence through `references/92-agent-evaluation.md` or `references/93-claude-evaluation.md`. They calibrate only the recorded task/pair; no role-default model/effort or automatic selection follows.

## Effort is not the only cost lever

Before raising effort, resolve prompt bloat and missing context. Vendor lean-prompt results support evaluating shorter prompts; they prove no local quality or cost gain. Better retrieval addresses absent evidence.

## Anti-patterns

- Carrying an effort level forward from a previous model generation without revalidating current guidance and honestly retaining unrun calibration status; task selection does not require an experiment.
- Disabling thinking to control cost instead of lowering effort, then writing repair instructions for the resulting behavior.
- Treating lower effort as a reliable verbosity or scope control instead of specifying the required output and boundaries.
- Arbitrary model/effort escalation from a vague importance or sensitivity label; record consequence and priority through the runtime orchestrator allocation owner.
- Pinning maximum effort by habit without measured quality benefit and a stated workload need.
- Treating a supported effort as proof it is appropriate, or changing model and effort together in a comparison.
- Setting an explicit thinking budget on a generation that no longer accepts one.
- Passing `adaptive` as an effort value.
- Raising effort to compensate for a bloated prompt or a badly assembled context.
- Benchmarking by effort name across vendors, where the same word denotes different amounts of work.

## Caveats

Thinking-disable constraints and the availability of manual thinking budgets are vendor-stated and time-sensitive; effort level names, per-model defaults, and starting-point recommendations are not restated here — read the target model's own file, which is the current source for its own numbers. The measured lean-prompt figures are from a specific vendor's internal testing on a specific generation and should not be generalized. Re-read the sources below before hard-coding any of these anywhere, and distinguish orchestrator task policy from vendor capability.

## Sources

- [Effort parameter reference](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model)
