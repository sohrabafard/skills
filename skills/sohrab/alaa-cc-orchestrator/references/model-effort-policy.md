# Model and Effort Control Route

`routing-matrix.md` owns actual task allocation and admission for EVERY role. `/alaa-prompting-guide` owns supported capabilities, source guidance, runtime precedence and the checked model-neutral projections. Its `references/50-effort-and-thinking.md` and `references/90-model-selection.md` inform the decision. They do not assign a pair merely from role identity.

The registry is `alaa-prompting-guide assets/claude-model-policy.json`. Managed roles carry no executable model or effort pins. Before you realize task-selected controls, check three things separately: ordinary eligibility, effort support and host availability. Legacy roles named for a model or effort are authority-compatible workload identities, never default pairs. Choose review depth from the actual review scope, and allocate its pair separately. Never use a stronger or different model solely for a second lens.

## Normalize omitted controls

This file alone owns orchestration defaults for this runtime. Capability registries own supported pairs, never these defaults. Preserve ordinary allocation when both controls are selected. Before every dispatch, apply these steps:

1. Retain every explicit field and fill only missing model or effort from the default below. Fill each field independently.
2. Validate the resulting pair against the capability registry and actual host before invocation. Unsupported, inactive or unrealizable pairs still block the affected lane.
3. Record the normalized model AND effort in the plan or compact dispatch, then explicitly supply both. Inherited controls are not normalization.

Omission alone and a successfully resolved default are never blocked/degraded.

Claude Code default: `model = claude-opus-5-5`, `effort = medium`.

The Agent invocation accepts a family alias only (`sonnet`, `opus`, `haiku`, `fable`), never a full ID. Pass the alias of the selected model; for this default, pass `opus`. Verify that the alias resolves to the selected ID on the target provider. When it does not, block the affected lane. `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns this runtime fact and the advisor pair table.

Verified 2026-10-18 against the official sources below and the active invocation schema; the alias-only invocation model was verified 2026-11-14. Refresh the mapping and capability evidence when it drifts. Record an unresolved future alias mapping as `NEEDS_CONFIRMATION`, never a guessed model ID. Defaults change no role authority, tools, skills, verdicts or independent gates; managed wrappers remain neutral.

## Before every dispatch

1. Read the owner's current runtime reference. Inspect the actual host controls, the installed and session role definitions, capability and access evidence, the context mode and effective overrides.
2. Explicitly supply BOTH model AND effort, as normalized in the plan or compact dispatch, on the verified invocation surface.
3. Check that the effective configured pair matches the selected pair. Prose, requested controls or source validation alone cannot prove it.
4. If exact realization is unavailable, use only an exact verified available compatibility realization that preserves the role contract, or block the affected lane with evidence.

Never silently change the pair, install, mutate shared configuration or claim that source edits activated a session.

For Claude Code, inspect the loaded definition, the active version and the invocation controls before dispatch. Model-neutral YAML omits BOTH `model` and `effort`; explicitly pass both on the verified Agent invocation surface. Current owner evidence supports invocation effort on a non-fork invocation since version 2.1.292. Environment, hook, force and provider overrides can still take precedence: inspect their effective precedence, and do not assume that YAML or invocation controls win. If a fork, an older version or a restricted surface cannot realize both values, require an exact verified available compatibility realization that preserves role authority, or block that lane. A separate CLI session changes context and permissions, so it is not an automatic substitute. `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns runtime precedence and current official evidence.

Keep permissions separate from model choice. Inspect the effective sandbox or permission mode, parent overrides, and native and MCP grants. When enforcement is unknown, stay within the narrower role authority. Model choice changes no tools, required skills, verdicts or independent gates. Diagnose missing context, tool failures and specification ambiguity before you attribute a shortfall to capacity. Reassess only remaining work, under the allocation boundary.

Report the configured and requested model and effort separately from the observed identity. An unknown observation stays unknown. Put the verdict or outcome first, then the metadata. /alaa-prompting-guide owns the rule-writer replacement-only contract.

## Native Advisor consultation

After you select the executor's task pair, consider native Advisor for a named unresolved decision that can benefit from consultation. Resolve missing facts and tool or context failures first. Read **Native Advisor** in `alaa-prompting-guide references/41-claude-code-runtime-features.md` for supported pair candidates, session checks and data sharing. Use Advisor only on a verified, authorized surface. When you use it, record the reason and the effective advisor control. A configured advisor also reaches each subagent, which applies the pair check against its own model. A Fable 5.2 executor accepts only a Fable 5.2 advisor; Claude Code attaches no lower-ranked advisor and raises no error. The executor chooses when to consult and owns the result. Keep consultation optional. Preserve the executor pair, role authority and independent gates.

## Source generation and proof

The existing projection engine renders the implementation and planner contracts into their wrappers. It neutralizes every other managed definition and preserves its authority and body. Wrapper metadata never owns model or effort. `SKILL.md` section 7 owns when to run `python3 scripts/render_agents.py --write`, the checks that follow it and their exit codes; aggregate validation checks drift. Source checks prove neither installed activation, account access nor serving identity.

## Default mapping sources

[Claude model configuration](https://code.claude.com/docs/en/model-config) and [Claude subagents](https://code.claude.com/docs/en/sub-agents).
