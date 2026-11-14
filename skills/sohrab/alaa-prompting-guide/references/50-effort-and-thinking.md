# Effort and Thinking: A Cross-Model Decision Procedure

This file owns cross-runtime effort evidence and control validation. Each model reference owns that model's supported levels. The runtime orchestrators own the actual task choices.

## The two levers do different jobs

**Model** selects judgment, and **effort** selects search depth. Choose both from the decisions the lane still has to make and the search it requires, then verify the choice. A higher effort proves no equivalence across models.

## What effort does not control

Response length, deliverable length, update cadence and scope require explicit prompt controls. Effort can change token use and tool behavior. Lowering it is not a reliable substitute for output constraints or scope constraints. Read the target model reference for the workload-specific effects observed on that model.

## Thinking: keep it on, lower the effort instead

Before you change thinking controls, use the registered model capability snapshot and refresh the model's API documentation. The current model references own thinking modes and their exceptions. Haiku 5.5 supports effort and adaptive thinking. Its API exception that permits disabled thinking does not transfer to Claude Code. Historical Haiku 4.5 uses extended thinking without effort. These API controls are not interchangeable with Claude Code settings.

For effort-enabled models, lower the supported effort to cut cost. Check retrieval, tool-use reliability and task quality. Report unsupported controls. Never substitute them. Read `references/36-haiku-5-5.md` for current Haiku controls.

Do not carry manual thinking budgets into current adaptive models. Historical Haiku 4.5 is the extended-thinking exception. The value `adaptive` names a thinking mode, never an effort. Neither `ultra` nor `ultracode` is a Claude API effort value. A harness orchestration mode requires separate proof.

## Choosing a starting level

Read the target model's reference for its supported levels, its default and its workload starting point. A shared effort name does not imply a shared search depth. An inherited effort is untested: refresh the guidance and keep its unrun status. Selection requires no experiment.

## The decision procedure

1. **Resolve missing evidence.** Retrieve or clarify absent context, capability or intent; a different model does not supply missing facts.
2. **Obtain the task selection from its owner.** The runtime orchestrator selects model AND effort for each authority role through its routing matrix, using `references/90-model-selection.md` as evidence. Planning and implementation are separate actual tasks. Role names and vendor defaults do not allocate them.
3. **Validate capabilities and realization.** First normalize omitted fields through `alaa-codex-orchestrator references/model-effort-policy.md` or its `alaa-cc-orchestrator` mirror. Then check both explicit controls against the structured capability policy and the actual host. Inspect the loaded definitions, pins, fork restrictions and caps, and the overrides from force settings, the environment and the provider. A control that is missing after normalization, unsupported or mismatched blocks the affected lane. Use only an available exact verified compatibility realization. Never invent a fallback.
4. **Keep selection separate from calibration.** Recommendations and selected pairs stay unmeasured. Selection needs no paid experiment or replay.
5. **Preserve authority.** Model controls change no scope, tool, verdict responsibility or independent gate. Main-session configuration stays external. Source consistency does not prove installed activation or observed serving identity.


## Capability registries and realized controls

The structured Codex and Claude policies register neutral role identities and supported pairs. Supported levels are capabilities, not task recommendations or role-wide ceilings. Historical entries do not authorize active selection. The runtime orchestrator owns actual task admission, priority and deliberate departures. This skill validates controls and allocates no work.

A stale executable pin can defeat the caller's controls. Read the target runtime reference, and verify the loaded definition, the explicit pair and the effective resolution. A source edit does not reload the current registry. Use an available exact verified realization or block the affected lane. Never silently substitute or change installed configuration. When the configured resolution is established, an unknown observed identity is a reporting limit, not a requirement for paid probing.

## Effort is not the only cost lever

Before raising effort, resolve prompt bloat and missing context. Vendor lean-prompt results support shorter prompts. They prove no local quality or cost gain. Better retrieval addresses absent evidence.

## Anti-patterns

- Carrying an effort level forward from a previous model generation without revalidating current guidance and honestly retaining unrun calibration status; task selection does not require an experiment.
- Disabling thinking to control cost instead of lowering effort, then writing repair instructions for the resulting behavior.
- Treating lower effort as a reliable verbosity or scope control instead of specifying the required output and boundaries.
- Writing a prompt line that asks the model to think less instead of lowering the effort; `references/43-fable-5-2.md` holds the Fable 5.2 evidence.
- Arbitrary model or effort escalation from a vague importance or sensitivity label. Record the consequence and the priority through the runtime orchestrator, which owns allocation.
- Pinning maximum effort by habit without measured quality benefit and a stated workload need.
- Treating a supported effort as proof it is appropriate, or changing model and effort together in a comparison.
- Setting an explicit thinking budget on a generation that no longer accepts one.
- Passing `adaptive` as an effort value.
- Raising effort to compensate for a bloated prompt or a badly assembled context.
- Benchmarking by effort name across vendors, where the same word denotes different amounts of work.

## Caveats

Thinking-disable constraints and the availability of manual thinking budgets are vendor-stated and time-sensitive. This file does not restate effort level names, per-model defaults or starting-point recommendations. Read the target model's own file, which is the current source for its own numbers. The measured lean-prompt figures come from one vendor's internal testing on one generation, and they should not be generalized. Re-read the sources below before you hard-code any of these values anywhere, and distinguish orchestrator task policy from vendor capability.

## Sources

- [Effort parameter reference](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)
- [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model)
