# Model and Effort Control Route

`routing-matrix.md` *All-role task allocation* selects the model and effort for EVERY role. This file realizes that pair. The capability registry is `alaa-prompting-guide assets/codex-model-policy.json`. Managed roles carry no executable model or effort pins. Check ordinary eligibility, effort support and host availability separately.

## Normalize omitted controls

This file alone owns orchestration defaults for this runtime. Preserve ordinary allocation when both controls are selected. Before every dispatch:

1. Retain every explicit field and fill only missing model or effort from the default below. Fill each field independently.
2. Validate the resulting pair against the capability registry and actual host before invocation. Unsupported, inactive or unrealizable pairs still block the affected lane.
3. Record the normalized model AND effort in the plan or compact dispatch. Inherited controls are not normalization.

Omission alone and a successfully resolved default are never blocked/degraded.

Codex default: user alias `sol-6.2-medium` resolves to `model = gpt-6.2-sol`, `effort = medium`.

Pass the executable model ID, never the composite alias. Supply both controls on every spawn, because an unset subagent model or effort inherits the parent agent's model and reasoning effort, not this default ([Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), read 2026-11-18). `alaa-prompting-guide references/11-codex-runtime-features.md` owns the pin precedence facts.

Verified 2026-11-18 against the official sources below and the host model catalog. Record an unresolved future alias mapping as `NEEDS_CONFIRMATION`, never a guessed model ID. Defaults change no role authority, tools, skills, verdicts or independent gates; managed wrappers remain neutral.

## Before every dispatch

1. Inspect the loaded custom definition and the global and parent controls: a custom `model` or `model_reasoning_effort` pin and parent overrides take precedence over caller controls.
2. Explicitly supply BOTH model AND effort, as normalized: pass `model` and `reasoning_effort` to the supported spawn surface. Verify that the host permits those arguments and the requested fork or context mode.
3. Check that the effective configured pair matches the selected pair. Prose, requested controls or source validation alone cannot prove it.
4. If a fork or a fixed named-role definition cannot realize both values, use only an exact verified available compatibility realization that preserves the role contract, or block the affected lane with evidence. Treat the loaded controls of a fixed definition as fixed until a verified reload.

Never silently change the pair, install, mutate shared configuration or claim that source edits activated a session. Source checks prove neither installed activation, account access nor serving identity.

Keep permissions separate from model choice. When enforcement is unknown, stay within the narrower role authority.

Report each lane's model and effort from your dispatch record: a lane writes neither in its report. The serving identity stays unknown unless a lane blocked on an observed control or reported a mismatch.

## Default mapping sources

[Codex models](https://learn.chatgpt.com/docs/models) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
