# Effort and Thinking: A Cross-Model Decision Procedure

This file owns cross-runtime effort evidence and control validation. Each model reference owns that model's supported levels, default and starting point. The runtime orchestrator owns the task choice.

## What each lever does

- **Model** selects judgment. **Effort** selects search depth. Choose both from the decisions the lane still has to make and the search it needs.
- A higher effort proves no equivalence with another model. A shared effort name means no shared search depth, across models or vendors.
- Effort controls no response length, deliverable length, update cadence or scope. Set each in the prompt. Lowering effort does not reliably constrain any of them.
- An effort inherited from another generation is untested. Refresh the guidance for the target model.

## Thinking

- Keep thinking on and lower the supported effort to cut cost. Then check retrieval, tool-use reliability and task quality.
- Before you change a thinking control, use the registered capability snapshot and refresh the model's API documentation. The model reference owns the thinking modes and their exceptions.
- An API thinking control is not a Claude Code setting. The Haiku 5.5 API exception that permits disabled thinking does not transfer to Claude Code.
- Carry no manual thinking budget into an adaptive model.
- Haiku 4.5 is the exception: it uses extended thinking and has no effort parameter. Give it no effort metadata, and never put it on one effort scale with an effort-enabled model.
- `adaptive` names a thinking mode, never an effort. Neither `ultra` nor `ultracode` is a Claude API effort value; a harness orchestration mode needs separate proof.
- Report an unsupported control. Never substitute another.
- Never ask the model in prose to think less; lower the effort. `references/43-fable-5-2.md` holds the Fable 5.2 evidence.

## The decision procedure

1. **Resolve missing evidence.** Retrieve or clarify absent context, capability or intent. A different model supplies no missing fact.
2. **Get the task selection from its owner.** The runtime orchestrator selects model AND effort for each authority role through its routing matrix, with `references/90-model-selection.md` as evidence. Planning and implementation are separate tasks. A role name or a vendor default allocates neither.
3. **Normalize, then validate.** Normalize omitted fields through `alaa-codex-orchestrator references/model-effort-policy.md` or its `alaa-cc-orchestrator` mirror. Check both explicit controls against the structured capability policy and the actual host: the loaded definitions, pins, fork restrictions and caps, and the overrides from force settings, the environment and the provider. Read the target runtime reference for precedence.
4. **Block what is not realized.** A control that is missing after normalization, unsupported or mismatched blocks the affected lane. A stale executable pin can defeat the caller's controls, and a source edit does not reload the current registry. Use only an available exact verified realization. Never invent a fallback, silently substitute, or change installed configuration.
5. **Keep selection separate from calibration.** A recommendation or a selected pair stays unmeasured. Selection needs no paid experiment or replay. When the configured resolution is established, an unknown observed identity is a reporting limit, not a reason for paid probing.
6. **Preserve authority.** A model control changes no scope, tool, verdict responsibility or independent gate. Main-session configuration stays external.

A supported level is a capability, not a task recommendation or a role-wide ceiling. A historical registry entry authorizes no active selection.

## Raising effort

Raise effort only when quality still falls short after you exclude prompt bloat, missing context, and tool or specification gaps. Never:

- escalate model or effort from a vague importance or sensitivity label; record the consequence and the priority through the runtime orchestrator instead;
- pin maximum effort without a measured quality benefit and a stated workload need;
- change model and effort together in a comparison.

## Caveats

Thinking constraints are vendor-stated and time-sensitive. Lean-prompt figures come from one vendor's tests on one generation and prove no local quality or cost gain. Re-read the sources before you hard-code a value.

## Sources

- [Effort parameter reference](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)
- [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model)
