# Model and Effort Control Route

`routing-matrix.md` *All-role task allocation* selects the model and effort for EVERY role. This file realizes that pair. The capability registry is `alaa-prompting-guide assets/claude-model-policy.json`. Managed roles carry no executable model or effort pins. Check ordinary eligibility, effort support and host availability separately.

## Normalize omitted controls

This file alone owns orchestration defaults for this runtime. Preserve ordinary allocation when both controls are selected. Before every dispatch:

1. Retain every explicit field and fill only missing model or effort from the default below. Fill each field independently.
2. Validate the resulting pair against the capability registry and actual host before invocation. Unsupported, inactive or unrealizable pairs still block the affected lane.
3. Record the normalized model AND effort in the plan or compact dispatch. Inherited controls are not normalization.

Omission alone and a successfully resolved default are never blocked/degraded.

Claude Code default: `model = claude-opus-5-5`, `effort = medium`.

Pass the family alias of the selected model on the Agent invocation; for this default, pass `opus`. Supply both parameters on every dispatch, because an omitted parameter falls through to the session's value, not to this default. Verify that the alias resolves to the selected ID on the target provider, or block the affected lane. `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns the alias and precedence facts.

Verified 2026-10-18 against the official sources below and the active invocation schema. Record an unresolved future alias mapping as `NEEDS_CONFIRMATION`, never a guessed model ID. Defaults change no role authority, tools, skills, verdicts or independent gates; managed wrappers remain neutral.

## Before every dispatch

1. Inspect the loaded role definition, the active version, the invocation controls and the effective overrides: environment, hook, force, provider and parent overrides can take precedence over the definition and the invocation.
2. Explicitly supply BOTH model AND effort, as normalized, on the verified Agent invocation surface.
3. Check that the effective configured pair matches the selected pair. Prose, requested controls or source validation alone cannot prove it.
4. If a fork, an older version or a restricted surface cannot realize both values, use only an exact verified available compatibility realization that preserves the role contract, or block the affected lane with evidence. A separate CLI session changes context and permissions, so it is not an automatic substitute.

Never silently change the pair, install, mutate shared configuration or claim that source edits activated a session. Source checks prove neither installed activation, account access nor serving identity.

Keep permissions separate from model choice. When enforcement is unknown, stay within the narrower role authority.

Report the configured and requested model and effort separately from the observed identity. An unknown observation stays unknown.

## Native Advisor consultation

After you select the executor's task pair, consider native Advisor for a named unresolved decision that consultation can help. Resolve missing facts and tool or context failures first. Read **Native Advisor** in `alaa-prompting-guide references/41-claude-code-runtime-features.md` for supported pairs, session checks and data sharing. Use Advisor only on a verified, authorized surface, and record the reason and the effective advisor control. Consultation stays optional and changes no executor pair, role authority or independent gate.

## Default mapping sources

[Claude model configuration](https://code.claude.com/docs/en/model-config) and [Claude subagents](https://code.claude.com/docs/en/sub-agents).
