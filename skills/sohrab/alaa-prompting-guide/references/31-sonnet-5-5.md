# Claude Sonnet 5.5

Use this file for current Sonnet prompting and API migration.

## Effort

- Defaults: `medium` in Claude Code (model-config, 14 November 2026) and the Claude apps; `high` on the Platform and the API. A surface default is not a task choice.
- Start at `medium` for well-specified agentic work and at `high` for a harder or longer task. Effort levels were recalibrated, so a level carried from Sonnet 5 is untested. Before you raise effort, read `references/50-effort-and-thinking.md`.
- The launch reports high-effort Sonnet near Opus on some work at similar cost. That proves no general equivalence.
- In two reported benchmark cases `max` scored below `xhigh`, because extra reviewer subagents caused timeouts or out-of-scope edits. Higher effort can change tool behavior without improving acceptance. This is no general delegation bias; for delegation wording read `references/06-invocation-and-composition.md`.

## Prompting

- Everyday coding with bounded local decisions fits this model; the patch need not be settled in advance. For a task with coupled unresolved design, `references/90-model-selection.md` names the owner of allocation.
- At `low`, state an observable done condition and the required checks, because early stops and skipped verification are documented risks.
- At `high` or `xhigh`, constrain the scope and stop after the requested outcome and checks. An extra feature or refactor is not completion.
- Do not turn the removal of thinking reminders into a ban. The prompting page permits private reasoning before a strict JSON answer when it makes structured output more reliable. Keep the JSON schema, evaluate the change on that workload, and never ask for the private reasoning itself.
- Set output length and visible progress separately from effort. Some progress narration moves into thinking, so when a person needs updates, ask for short status text at meaningful milestones. Hidden thinking does not meet a host's communication requirement.
- Before you remove verification language, apply the authority test in `references/80-subagent-authoring.md`.

## API migration boundary

These are API controls, not Claude Code configuration keys. Tool replay and provider compatibility need integration tests in the consuming client.

- Select `claude-sonnet-5-5` with adaptive thinking. Disabled or manual thinking returns an error. A per-message effort change requires adaptive mode.
- The optional `thinking: {"type": "between_tools"}` mode permits only `low`, `medium` and `high`. It accepts no `display`, `budget_tokens` or `block_binding`.
- `tool_choice` values `any` and `tool` are rejected. Use `auto` and validate required tool use in the application. Use a strict tool schema only where the provider supports it; a strict schema forces no invocation.
- Preserve returned signed thinking blocks and append-only history through tool loops. A rewritten earlier message can invalidate replay; follow the migration guide's account and binding conditions before you transform history.
- Recheck an integration that uses computer use or an advisor. The Claude API and Google use `computer_toolset_20260801`. An advisor configuration cannot carry forward a Sonnet 5 or Opus 4.7/4.8 target. Verify the tool surface of the selected provider.

## Claude Code availability

The minimum Claude Code version is v2.1.284. A `sonnet` alias can select an older generation on another provider, so use the exact ID or a verified deployment mapping. Before activation, inspect account access, allowlists, effective overrides, effort caps and observed identity through `references/41-claude-code-runtime-features.md`. Missing availability blocks selection and authorizes no fallback, installation or settings change.

## Sources

Verified 29 September 2026. Agentic effort, the structured-JSON scope, the launch defaults and the benchmark caveats were refreshed 9 October 2026 from the prompting page, the 28 September launch and the effort documentation.

- [Sonnet overview](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Sonnet migration](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)
- [Sonnet changes](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Sonnet launch](https://www.anthropic.com/claude-sonnet-5-5)
