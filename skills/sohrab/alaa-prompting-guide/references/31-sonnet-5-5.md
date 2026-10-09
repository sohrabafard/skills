# Claude Sonnet 5.5

Use for current Sonnet prompting and migration. `assets/claude-model-policy.json` owns
role identity, capability snapshots and availability; `references/30-sonnet-5.md` is historical.
Source checks do not prove account access, runtime activation or workload quality.

## Prompting and effort

Claude Code and Claude apps default to `medium`; Platform/API defaults to `high`. These surface defaults are not task choices. Begin comparisons at `medium` for well-specified agentic work and
`high` for harder or longer tasks. Effort levels were recalibrated: workload recommendations are
unrun hypotheses, not inherited calibration. Use `references/50-effort-and-thinking.md`
for controlled comparisons; raise effort only after excluding context, tool and specification gaps.

The launch reports high-effort Sonnet approaching Opus on some work at similar cost; it proves no universal local equivalence. Medium and high remain distinct supported task settings. In two reported benchmark cases, max underperformed xhigh because extra reviewer subagents caused timeouts or out-of-scope edits. Treat this as a workload-specific caveat, not a universal effort ranking; higher effort can change tool behavior without improving acceptance.

Everyday coding can involve bounded local decisions; it need not be transcription of a fully settled patch. Use the runtime orchestrator routing matrix for task allocation/admission and canonical policy for supported pairs. The orchestrator decides the route for materially coupled unresolved design.

Do not turn thinking-reminder removal into a blanket ban. The Sonnet prompting page specifically permits private reasoning before a strict JSON answer when that improves structured-output reliability. This is a task-specific exception, never authority to disclose private chain-of-thought. Preserve the required JSON schema and evaluate the change on that workload.

At low effort, supply an observable done condition and required checks: early stopping and
skipped verification are documented risks. At high or xhigh effort, constrain scope and stop
after the requested outcome and checks; extra features or refactors are not completion.
Preserve focused implementation checks and independent gates through the authority test in
`references/80-subagent-authoring.md`. Extra reviewer delegation at higher efforts does not
establish a general delegation bias; `references/06-invocation-and-composition.md` owns routing.

For a bounded implementation, adapt this contract without broadening its authority:

```text
Change only the named function and its focused tests. Preserve the public signature and
unrelated behavior. Run the supplied checks and report their observed results. Stop when
the acceptance criteria and checks pass; report blockers without claiming unrun checks passed.
```

Specify output length and visible progress separately from effort. Some progress narration
can move into thinking; when visible updates are needed, request concise status text at
meaningful milestones. Do not request private reasoning or assume hidden thinking satisfies
the host's communication requirements. Keep durable state through `/alaa-workflow`.

## API migration boundary

- Select `claude-sonnet-5-5` and use adaptive thinking. Disabled or manual thinking returns
  an error. The optional `thinking: {"type": "between_tools"}` mode permits only low,
  medium and high effort; it does not accept `display`, `budget_tokens` or `block_binding`.
  Per-message effort changes require adaptive mode.
- Forced `tool_choice` values `any` and `tool` are rejected. Use `auto`; validate required
  tool use in the application. Use strict tool schemas only where the provider supports
  them; strict schemas do not force invocation.
- Preserve returned signed thinking blocks and append-only history through tool loops.
  Rewriting earlier messages can invalidate replay; follow the migration guide's account
  and binding conditions before transforming history.
- Recheck integrations with computer use or an advisor. The Claude API and Google use
  `computer_toolset_20260801`; advisor configurations cannot carry forward Sonnet 5 or
  Opus 4.7/4.8 targets. Verify the selected provider's supported tool surface.

These are API controls, not new Claude Code configuration keys. Tool replay and provider
compatibility need integration tests in the consuming client; this skill performs no API calls.

## Claude Code availability

The minimum is v2.1.284. A `sonnet` alias can select older generations on other providers;
use the exact ID or a verified deployment mapping. Before activation, inspect account access,
allowlists, effective overrides, effort caps and observed identity through
`references/41-claude-code-runtime-features.md`. Missing availability blocks selection;
it does not authorize fallback, installation or a settings change.

## Sources and limits

Verified 29 September 2026. General delegation polarity, local quality and installed serving
identity remain unmeasured. Re-fetch the relevant source before reusing a version-sensitive value.

- [Sonnet overview](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Sonnet migration](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)
- [Sonnet changes](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Sonnet launch](https://www.anthropic.com/claude-sonnet-5-5)

Agentic effort and structured-JSON prompting scope refreshed 9 October 2026; API migration facts retain their 29 September snapshot. The selection guide assigns everyday coding to Sonnet without an effort; medium/high come from the separate prompting source.

Launch defaults and benchmark caveats refreshed 9 October 2026 from the official 28 September launch and effort documentation. No local comparative calibration ran.
