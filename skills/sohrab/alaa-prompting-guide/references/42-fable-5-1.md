# Claude Fable 5.1

Use for current Fable prompting. `references/40-fable-5.md` preserves the
older generation's guidance for historical comparison only. Read the structured Claude
policy before selecting a profile; availability and a vendor ranking do not prove a
workload-specific advantage. Explicit comparisons may test Fable for unresolved demanding reasoning or long-horizon work
after diagnosing the current profile's context and tools.

## Prompting

State the outcome and acceptance criteria, provide investigation tools, and keep authority
and side-effect boundaries explicit. Let the model investigate and correct its work without
carrying forward the older Fable-specific requirement for recurring verification reminders.
Focused implementer checks and independent acceptance gates survive; their ownership is
defined in `references/80-subagent-authoring.md`.

Calibrate effort on the hardest representative tasks, not easy tasks that cannot expose a
quality difference. At lower effort verify that required retrieval still occurs. Tune
response length and progress reporting separately, and support long turns within the
authorized runtime's resource limits. No measured pack speedup is claimed.

For independent workstreams, use the delegation conditions in
`references/06-invocation-and-composition.md`; asynchronous coordination requires actual
host support, not merely API documentation.

## API and safety boundaries

API clients must preserve append-only history and returned thinking blocks, including the
documented account-dependent binding behavior. Mid-conversation system messages, batching
nudges and cache controls are API features; do not invent matching Claude Code keys.

Read `references/41-claude-code-runtime-features.md` before selection: provider availability,
credits, safeguards and fallback can change the effective serving model. Never bypass a
safeguard or install a local fallback to manufacture a comparison result. Keep refusal,
fallback and unknown serving identity visible in evaluation evidence.

## Sources and limits

Verified 25 September 2026. Full system cards could not be retrieved; the release summaries
do not establish full-card review or justify weakening existing gates. Local comparisons
remain unrun.

- [Fable prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Fable migration](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide)
- [Fable model](https://platform.claude.com/docs/en/models/fable-5-1/overview)
- [Fable release](https://www.anthropic.com/claude-fable-and-mythos-5-1)
