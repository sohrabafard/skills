# Source Map

Ground version-sensitive claims here. Re-check live official docs before copying prices, limits, effort levels, feature gates, or latest/current recommendations.

## Source priority

1. Explicit user instructions for the current task.
2. The target model reference plus its runtime reference.
3. `05-trigger-syntax.md` for `$` versus `/`.
4. Live official docs:
   - GPT-5.6: `https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6`, `https://developers.openai.com/api/docs/models`, `https://developers.openai.com/api/docs/models/gpt-5.6-sol`
   - Codex: base `https://developers.openai.com/codex/`; pages `use-cases/follow-goals`, `subagents`, `skills`, `guides/agents-md`, `config-reference`
   - Claude prompting: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` plus the model-specific Opus 4.8, Sonnet 5, and Fable 5 pages under that path
   - Claude facts/runtime: `https://platform.claude.com/docs/en/about-claude/models/overview`, `https://platform.claude.com/docs/en/build-with-claude/effort`, and base `https://code.claude.com/docs/en/` pages `skills`, `sub-agents`, `workflows`, `scheduled-tasks`, `permission-modes`, `ultraplan`, `goal`
5. `$openai-docs` for current OpenAI guidance; use community sources only as corroboration after official sources fail.

## Cross-agent packaging contract

- Keep one portable `SKILL.md` package for Codex and Claude Code.
- Keep agent-neutral behavior in `SKILL.md` and `references/`; `agents/openai.yaml` is Codex UI metadata only.
- Runtime/model differences affect prompt content, not package format.

## Freshness triggers

Re-fetch for prices, token limits, effort/verbosity names, latest/current/model-choice claims, versions, defaults, flags, goal/loop behavior, nesting, concurrency, or facts newer than the reference's caveat date.

## What each reference file owns

| File | Owns |
|---|---|
| `05-trigger-syntax.md` | `$` vs `/` skill-invocation rule by runtime |
| `10-gpt-5-6.md` | GPT-5.6 model selection, tuning, prompting, and tool orchestration |
| `11-codex-runtime-features.md` | Codex `/goal`, subagents, batch jobs, `AGENTS.md`, and skills |
| `20-opus-4-8.md` | Claude Opus 4.8 model-level prompting |
| `30-sonnet-5.md` | Claude Sonnet 5 model-level prompting |
| `40-fable-5.md` | Claude Fable 5 model-level prompting |
| `41-claude-code-runtime-features.md` | Claude Code `/loop`, agents, workflows, Ultraplan, and `/goal` |
| `90-model-selection.md` | Cross-model choice and companion routing |

## Interpretation contract

Carry caveats forward. If official sources or `$alaa-workflow` disagree with this skill, report the drift, prefer current official/runtime truth for the task, and reconcile the owner files instead of silently choosing.
