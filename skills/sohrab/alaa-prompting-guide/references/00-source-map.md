# Source Map

Use this file to ground the skill before trusting a version-sensitive claim in any other reference file here, and re-check live docs before hard-coding a number (price, context window, effort level) from this skill into another document.

## Why this skill exists and how it was built

All four v1 models postdate a typical training cutoff, so nothing here should be treated as remembered knowledge — every claim in `references/10-*` through `references/41-*` was pulled from a live fetch of an official docs page in the same research pass that produced this skill. Where a page could not be confirmed as genuinely model-specific, the relevant reference file says so explicitly in its own "Caveats" section instead of presenting a guess as fact.

## Source priority

1. Explicit user instructions for the current task.
2. This skill's model-specific reference file for the target model, plus the matching runtime-feature reference file for the agent surface it runs in.
3. `references/05-trigger-syntax.md` for which trigger character ($ or /) belongs in the prompt you are writing.
4. Official, model-specific documentation, fetched live when the task is version-sensitive:
   - OpenAI: `https://developers.openai.com/api/docs/guides/latest-model` (GPT-5.5 model page), `https://developers.openai.com/api/docs/guides/prompt-guidance` (prompt guidance, filterable by `?model=`)
   - OpenAI Codex: `https://developers.openai.com/codex/use-cases/follow-goals`, `https://developers.openai.com/codex/subagents`, `https://developers.openai.com/codex/skills`, `https://developers.openai.com/codex/guides/agents-md`, `https://developers.openai.com/codex/config-reference`
   - Anthropic Claude models: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` (family-wide), plus the model-specific pages `prompting-claude-opus-4-8`, `prompting-claude-sonnet-5`, `prompting-claude-fable-5` under the same `prompt-engineering/` path
   - Anthropic model facts: `https://platform.claude.com/docs/en/about-claude/models/overview`, `.../whats-new-claude-4-8`, `.../whats-new-sonnet-5`, `.../introducing-claude-fable-5-and-claude-mythos-5`
   - Anthropic effort parameter: `https://platform.claude.com/docs/en/build-with-claude/effort`
   - Claude Code runtime: `https://code.claude.com/docs/en/skills`, `.../sub-agents`, `.../workflows`, `.../scheduled-tasks` (this is where `/loop` is documented), `.../permission-modes`, `.../ultraplan`, `.../goal`
5. `$openai-docs` (system-level skill, Codex-side only) for the freshest GPT-5.5/Codex specifics when this skill's own references are stale.
6. Community posts, blogs, or forum threads only to corroborate a detail after the official pages above are exhausted — never as the sole source for a number that will be copied into other tooling.

## Cross-agent packaging contract

- This skill is packaged as one portable folder with `SKILL.md` frontmatter and Markdown instructions, per the pack-wide convention already used by every sibling `alaa-*` skill.
- Claude Code (Opus 4.8 / Sonnet 5 / Fable 5) reads the folder's `SKILL.md` directly when installed under a Claude skills path.
- OpenAI Codex (GPT-5.5) reads the same `SKILL.md`; `agents/openai.yaml` supplies Codex UI metadata and default prompt text only — keep all agent-neutral instructions in `SKILL.md` and `references/`.
- The one thing this skill is explicitly *about* — trigger-character differences, model differences, feature differences — must never leak into how the skill itself is packaged. The package stays one shared format for every agent that loads it.

## Freshness triggers

Re-check the live docs above (do not rely on this skill's cached numbers) when the task mentions:

- pricing, context window size, max output tokens, or a specific effort/verbosity level name
- "latest model," "current model," "which model should I use," or a model comparison
- a Codex or Claude Code version number, a config flag, or whether a feature is enabled by default
- goal mode, `/loop`, subagent nesting depth, background task limits, or workflow concurrency caps
- anything dated after this skill's own research pass (see each reference file's "Caveats" section for its research date context: session-reported "current month" was July 2026)

## What each reference file owns

| File | Owns |
|---|---|
| `05-trigger-syntax.md` | `$` vs `/` skill-invocation rule by runtime |
| `10-gpt-5-5.md` | GPT-5.5 model-level prompting (verbosity, reasoning effort, tone, persistence) |
| `11-codex-runtime-features.md` | Codex app/CLI features GPT-5.5 runs inside: `/goal`, subagents, `spawn_agents_on_csv`, `AGENTS.md`, Agent Skills |
| `20-opus-4-8.md` | Claude Opus 4.8 model-level prompting |
| `30-sonnet-5.md` | Claude Sonnet 5 model-level prompting |
| `40-fable-5.md` | Claude Fable 5 model-level prompting |
| `41-claude-code-runtime-features.md` | Claude Code features shared by Opus 4.8 / Sonnet 5 / Fable 5: `/loop`, Agent subagents, Workflow tool, plan mode / Ultraplan, Claude Code's own `/goal` |
| `90-model-selection.md` | Cross-model comparison table, decision helper, and companion routing to `$alaa-workflow` |

## Interpretation contract

When a reference file's "Caveats" section flags a claim as unverified, secondary-sourced, or time-sensitive, carry that same hedge forward into whatever prompt or document you are writing — do not launder an unverified number into a confident-sounding instruction. When two reference files disagree with `alaa-workflow`'s own capsule guidance in `references/90-source-map.md` (its "GPT-5.5 / Codex use guidance" and "Claude Opus 4.8 use guidance" sections), prefer this skill's fuller research for depth, but flag the mismatch so both files can be reconciled rather than left silently inconsistent.
