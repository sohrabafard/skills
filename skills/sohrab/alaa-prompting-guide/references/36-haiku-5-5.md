# Claude Haiku 5.5

Use Haiku 5.5 for bounded retrieval, exact procedures, admitted mechanical or bounded semantic implementation, and documentation from verified behavior. The launch names compaction, classification, queries and coding subagents. Sonnet and Opus stay the stronger candidates for complex agentic coding.

## Prompting and work boundaries

- Give one outcome, the named inputs or retrieval starts, the required evidence and checks, the allowed tools and side effects, and explicit completion and failure conditions.
- Require retrieval before a factual conclusion and an observed check before a success claim.
- Require a report on every requested item, as evidenced or unresolved, and a stop at the acceptance criteria.
- Tell the lane to return missing scope or evidence, a wider architecture judgment or an ambiguous failure to the lead. It never invents a fact or expands the task.

## Allocation limits

- Vendor guidance on bounded work is capability evidence, not a role default. `references/90-model-selection.md` names the owner of allocation, admission, triggers and independent gates.
- Admission to a registered implementation role follows the `/alaa-cc-orchestrator` routing-matrix predicates. Apply no arbitrary file-count cap and no trial ladder.
- Missing scope or evidence, or interacting design decisions, require reassessment, not an inherited Haiku choice.
- Implementation authority replaces neither the restrictions of a bounded support role nor an independent gate.
- A missing account or control capability blocks the affected dispatch. For identity reporting, read `references/80-subagent-authoring.md`.

## API and Claude Code controls

Verified 8 October 2026:

- API ID `claude-haiku-5-5`; efforts `low`, `medium`, `high`, `xhigh`, `max`; default `medium`, in Claude Code too (model-config, 14 November 2026).
- API thinking: adaptive is supported and a manual token budget is not. Disabled thinking is permitted through `high`; `xhigh` and `max` require adaptive.
- Claude Code: thinking cannot be disabled, and the minimum version is 2.1.293.

An API control establishes no Claude Code setting. Before activation, inspect the account and provider mapping, override precedence, caps and effective tools through `references/41-claude-code-runtime-features.md`.

Prompting guidance (9 October 2026) by level:

- `low`: short or simple work.
- `medium`: most work, including agentic coding. The model can skip checks at this level, so keep the declared completion and evidence requirements and independent acceptance.
- `high`: longer work, stricter instruction following, or knowledge tasks.
- `xhigh` and `max`: only with a stated benefit over Sonnet. They can produce thinking with no visible reply.

No supported level is a role default; the orchestrator justifies the task choice.

## Sources

Launch and prompting guidance were refreshed 9 October 2026 from the 7 October launch and the prompting page.

- [Launch and stated workloads](https://www.anthropic.com/claude-haiku-5-5)
- [Migration and API controls](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide)
- [Prompting Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Code model configuration](https://code.claude.com/docs/en/model-config)
- [Code subagents](https://code.claude.com/docs/en/sub-agents)
