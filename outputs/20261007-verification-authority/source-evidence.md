# Verification authority: decision evidence

Read-only specification, test-strategy and official-guidance lanes completed on 2026-10-07.
This is a task decision/evidence record, not runtime instructions or live-compliance proof.

## Repository findings

- All four implementer variants combine dispatched checks with a broad-suite prohibition but lack a conflicting-dispatch response. Codex default/difficult lines 33/25; Claude default/difficult lines 39/42 at the initial HEAD.
- Both verification references already reserve focused checks for implementers, affected checks for independent verification, and required exhaustive checks for the final candidate.
- Claude's escalation template lacks the focused tier/exclusions carried by its normal template.
- Whole-skill implementation reads also found both review fix-cycle templates dispatching focused plus affected checks to the implementer; these are part of the same repair.
- Existing contract checkers cover metadata, authority and skill bindings, but do not detect these omissions.
- Prompting-guide already preserves focused checks, independent gates and removal of unjustified repeats. No policy/pin or prompting-guide change is warranted by this incident.

## Official guidance

Accessed by the independent researcher on 2026-10-07; claims below retain their model scope.

| Source | Supported implication and limitation |
|---|---|
| [OpenAI: rethinking Astra skills](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Concise descriptions, conditional reads, fewer redundant reminders. Testing-reminder guidance is Astra-specific, not permission to drop local independent gates. |
| [OpenAI: latest model](https://developers.openai.com/api/docs/guides/latest-model) | State instructions once and compare changes against the same evaluations. Adjacent older-model wording does not prove GPT-6.1 behavior. |
| [Anthropic: prompting practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Explicit scope and desired behavior; generic self-check advice has model-specific exceptions. |
| [Anthropic: Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Prior prompts are a starting point; workload measurements remain necessary. |
| [Anthropic: Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) | Verification behavior varies with effort; explicit required checks and stopping scope remain justified. |
| [Anthropic: Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | Keep tests/changes within requested scope and preserve constraints through compaction. |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Agent definitions carry behavioral contracts; task dispatch is a distinct input. |
| [OpenAI: evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Include adversarial conflicting instructions and handoffs in evaluation. |

Independent acceptance and scope-tier ownership are repository policy, not vendor mandates.

## Acceptance scenarios

| Scenario | Required result |
|---|---|
| Separate focused and full/race/e2e/cross-lane commands | Run only established focused commands; report exclusions/conflict. |
| Indivisible mixed command | Leave it unrun; invent no split, substitute or flag. |
| Only prohibited or ambiguous commands | Report validation not run and request a valid focused command. |
| Broad command labeled focused | Decide from actual coverage; reject the mislabeled command. |
| Broad PASS supplied by the author | Do not count it as independent acceptance; required independent verifier still runs. |
| Valid independent affected PASS with unchanged inputs | Cite it, preserving the four validity conditions; keep exhaustive freshness separate. |
| Focused-only control | Execute supplied checks and report observed evidence without self-approval. |

Structural mutation fixtures and independent source walkthroughs can establish source coverage.
Live before/after trials would need isolated command traces, fixed environments and two runs per configuration in each runtime; none are implied by source checks. Installed activation, universal compliance and latency improvement remain unproven.

## Curation candidate

The user's incident supplies a reusable decision interface: dispatch cannot widen lane validation authority. Its authorized destination is the paired orchestrator contract being repaired. Avoid a duplicate memory rule; final curation must confirm the promotion and any remaining gap.
