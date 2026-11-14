# Model and Effort Control Route

`routing-matrix.md` owns actual task allocation and admission for EVERY role. `/alaa-prompting-guide` owns supported capabilities, source guidance, runtime precedence and the checked model-neutral projections. Its `references/50-effort-and-thinking.md` and `references/90-model-selection.md` inform the decision. They do not assign a pair merely from role identity.

The registry is `alaa-prompting-guide assets/codex-model-policy.json`. Managed roles carry no executable model or effort pins. Before you realize task-selected controls, check three things separately: ordinary eligibility, effort support and host availability. Legacy roles named for a model or effort are authority-compatible workload identities, never default pairs. Choose review depth from the actual review scope, and allocate its pair separately. Never use a stronger or different model solely for a second lens.

## Normalize omitted controls

This file alone owns orchestration defaults for this runtime. Capability registries own supported pairs, never these defaults. Preserve ordinary allocation when both controls are selected. Before every dispatch, apply these steps:

1. Retain every explicit field and fill only missing model or effort from the default below. Fill each field independently.
2. Validate the resulting pair against the capability registry and actual host before invocation. Unsupported, inactive or unrealizable pairs still block the affected lane.
3. Record the normalized model AND effort in the plan or compact dispatch, then explicitly supply both. Inherited controls are not normalization.

Omission alone and a successfully resolved default are never blocked/degraded.

Codex default: user alias `sol-6.1-medium` resolves to `model = gpt-6.1-sol`, `effort = medium`; pass the executable model ID, never the composite alias.

Verified 2026-10-18 against the official sources below and the active invocation schema. Refresh the mapping and capability evidence when it drifts. Record an unresolved future alias mapping as `NEEDS_CONFIRMATION`, never a guessed model ID. Defaults change no role authority, tools, skills, verdicts or independent gates; managed wrappers remain neutral.

## Before every dispatch

1. Read the owner's current runtime reference. Inspect the actual host controls, the installed and session role definitions, capability and access evidence, the context mode and effective overrides.
2. Explicitly supply BOTH model AND effort, as normalized in the plan or compact dispatch, on the verified invocation surface.
3. Check that the effective configured pair matches the selected pair. Prose, requested controls or source validation alone cannot prove it.
4. If exact realization is unavailable, use only an exact verified available compatibility realization that preserves the role contract, or block the affected lane with evidence.

Never silently change the pair, install, mutate shared configuration or claim that source edits activated a session.

For Codex, inspect the currently loaded custom definition and the global and parent controls before dispatch. Custom `model` and `model_reasoning_effort` pins override caller controls. Model-neutral TOMLs omit BOTH pins; explicitly pass `model` and `reasoning_effort` to the supported spawn surface. Verify that the host permits those arguments and the requested fork or context mode. Do not imply that full-history forks accept overrides when this host rejects them. If the current host exposes fixed named-role definitions, treat their loaded controls as fixed until a verified reload; source edits alone do not prove that the registry reloaded. A fixed compatibility realization is usable only when its exact controls and authority match the selected task; otherwise block that lane. `alaa-prompting-guide references/11-codex-runtime-features.md` owns runtime precedence and current official evidence.

Keep permissions separate from model choice. Inspect the effective sandbox or permission mode, parent overrides, and native and MCP grants. When enforcement is unknown, stay within the narrower role authority. Model choice changes no tools, required skills, verdicts or independent gates. Diagnose missing context, tool failures and specification ambiguity before you attribute a shortfall to capacity. Reassess only remaining work, under the allocation boundary.

Report the configured and requested model and effort separately from the observed identity. An unknown observation stays unknown. Put the verdict or outcome first, then the metadata. /alaa-prompting-guide owns the rule-writer replacement-only contract.

## Source generation and proof

The existing projection engine renders the implementation and planner contracts into their wrappers. It neutralizes every other managed definition and preserves its authority and body. Wrapper metadata never owns model or effort. `SKILL.md` section 7 owns when to run `python3 scripts/render_agents.py --write`, the checks that follow it and their exit codes; aggregate validation checks drift. Source checks prove neither installed activation, account access nor serving identity.

## Default mapping sources

[Codex models](https://learn.chatgpt.com/docs/models) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
