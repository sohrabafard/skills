# Model and Effort Control Route

`routing-matrix.md` owns actual task allocation and admission for EVERY role. `/alaa-prompting-guide` owns supported capabilities, source guidance, runtime precedence and checked model-neutral projections. Its `references/50-effort-and-thinking.md` and `references/90-model-selection.md` inform the decision; they do not assign a pair merely from role identity.

The registry is `alaa-prompting-guide assets/claude-model-policy.json`. Managed roles carry no executable model/effort pins. Before realizing task-selected controls, check ordinary eligibility, effort support and host availability separately. Legacy model/effort-named roles are authority-compatible workload identities, never default pairs. Choose review depth from the actual review scope and allocate its pair separately; never use a stronger or different model solely for a second lens.

## Normalize omitted controls

This file alone owns orchestration defaults for this runtime; capability registries own supported pairs, never these defaults. Preserve ordinary allocation when both controls are selected. Before every dispatch, retain every explicit field and fill only missing model or effort from the default below, independently. Validate the resulting pair against the capability registry and actual host before invocation; unsupported, inactive or unrealizable pairs still block the affected lane. Omission alone and a successfully resolved default are never blocked/degraded. Record the normalized model AND effort in the plan or compact dispatch, then explicitly supply both; inherited controls are not normalization.

Claude Code default: `model = claude-opus-5-5`, `effort = medium`.

Verified 2026-10-18 against the official sources below and the active invocation schema. Refresh mapping/capability evidence when it drifts; unresolved future alias mapping is `NEEDS_CONFIRMATION`, never a guessed model ID. Defaults change no role authority, tools, skills, verdicts or independent gates; managed wrappers remain neutral.

## Before every dispatch

Read the owner's current runtime reference and inspect actual host controls, installed/session role definitions, capability/access evidence, context mode and effective overrides. Explicitly supply BOTH model AND effort after normalization from the plan or compact dispatch on the verified invocation surface. Check the effective configured pair matches the selected pair; prose, requested controls or source validation alone cannot prove it. If exact realization is unavailable, use only an exact verified available compatibility realization preserving the role contract, or block the affected lane with evidence. Never silently change the pair, install, mutate shared configuration or claim source edits activated a session.

For Claude Code, inspect the loaded definition, active version and invocation controls before dispatch. Model-neutral YAML omits BOTH `model` and `effort`; explicitly pass both on the verified Agent invocation surface. Current owner evidence supports non-fork invocation effort since version 2.1.292, subject to environment, hook, force and provider overrides; inspect their effective precedence rather than assuming YAML or invocation controls win. If a fork, older version or restricted surface cannot realize both values, require an exact verified available compatibility realization preserving role authority or block that lane. A separate CLI session changes context and permissions and is not an automatic substitute. Runtime precedence and current official evidence are owned by `alaa-prompting-guide references/41-claude-code-runtime-features.md`.

Keep permissions separate: inspect effective sandbox/permission mode, parent overrides and native/MCP grants; remain within narrower role authority when enforcement is unknown. Model choice changes no tools, required skills, verdicts or independent gates. Diagnose missing context, tool failures and specification ambiguity before capacity; reassess only remaining work under the allocation boundary. Comparisons change one factor at a time.

Report configured and requested model/effort separately from observed identity; unknown observation remains unknown. Put verdict/outcome first, then metadata. The rule-writer replacement-only contract remains owned by /alaa-prompting-guide.

## Source generation and proof

The existing projection engine renders implementation/planner contracts and neutralizes every other managed definition while preserving its authority/body. Wrapper metadata never owns model/effort. Run `python scripts/render_agents.py --write` after managed definition, contract or version changes; aggregate validation checks drift. After renderer logic changes also run `python scripts/render_agents.py --self-test`. Exit `0` is clean, `1` findings/drift, `2` unavailable; either nonzero blocks completion. Source checks prove neither installed activation, account access nor serving identity.

## Default mapping sources

[Claude model configuration](https://code.claude.com/docs/en/model-config) and [Claude subagents](https://code.claude.com/docs/en/sub-agents).
