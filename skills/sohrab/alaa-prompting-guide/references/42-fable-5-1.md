# Claude Fable 5.1

Historical reference only. `references/43-fable-5-2.md` owns current Fable prompting, and nothing here authorizes a current pin. `references/40-fable-5.md` preserves the
older generation's guidance. Read the structured Claude
policy before selecting a profile; availability and a vendor ranking do not prove a
workload-specific advantage. The runtime orchestrator chooses Fable only from actual task evidence; a difficult role title grants no automatic choice. No source claim proves local superiority.

## Prompting

State the outcome and acceptance criteria, provide investigation tools, and keep authority
and side-effect boundaries explicit. Let the model investigate and correct its work without
carrying forward the older Fable-specific requirement for recurring verification reminders.
Focused implementer checks and independent acceptance gates survive; their ownership is
defined in `references/80-subagent-authoring.md`.

Set effort for the hardest representative tasks. At lower effort verify that required retrieval still occurs. Tune
response length and progress reporting separately, and support long turns within the
authorized runtime's resource limits. No measured pack speedup is claimed.

Default effort depends on surface: Claude Code and Platform/API use high; Cowork and claude.ai use medium. All low/medium/high/xhigh/max levels are supported, subject to host controls. The launch reports low/medium improvements against Fable 5, not universal equivalence across models. Low can skip required retrieval; xhigh/max can duplicate deliverable drafting. Preserve required retrieval and artifact acceptance, and compare accepted outcomes rather than assuming higher effort is better.

For independent workstreams, use the delegation conditions in
`references/06-invocation-and-composition.md`; asynchronous coordination requires actual
host support, not merely API documentation.

## API and safety boundaries

API clients must preserve append-only history and returned thinking blocks, including the
documented account-dependent binding behavior. Mid-conversation system messages, batching
nudges and cache controls are API features; do not invent matching Claude Code keys.

Read `references/41-claude-code-runtime-features.md` before selection: provider availability,
credits, safeguards and fallback can change the effective serving model. Never bypass a
safeguard or install a local fallback. Keep refusal,
fallback and unknown serving identity visible in reports.

## Sources and limits

Verified 25 September 2026. Full system cards could not be retrieved; the release summaries
do not establish full-card review or justify weakening existing gates. Local calibration
remains unrun.

- [Fable prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Fable migration](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide)
- [Fable model](https://platform.claude.com/docs/en/models/fable-5-1/overview)
- [Fable release](https://www.anthropic.com/claude-fable-and-mythos-5-1)

Surface defaults and effort caveats refreshed 9 October 2026 from the official September launch (publication day unspecified) and effort documentation. The joint article is evidence for Fable only here; Mythos is excluded from active selection and custom profiles.
