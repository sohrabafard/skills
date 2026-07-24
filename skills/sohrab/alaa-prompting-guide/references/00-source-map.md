# Source Map

Ground version-sensitive claims here. Re-check live official docs before copying prices, limits, effort levels, feature gates, or latest/current recommendations.

## Source priority

1. Explicit user instructions for the current task.
2. The target model reference plus its runtime reference.
3. `05-trigger-syntax.md` for `$` versus `/`.
4. Live official docs:
   - GPT-5.6: `https://developers.openai.com/api/docs/guides/latest-model`, `https://developers.openai.com/api/docs/models`
   - Codex: base `https://developers.openai.com/codex/`; pages `use-cases/follow-goals`, `subagents`, `skills`, `guides/agents-md`, `config-reference`
   - Claude prompting: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` plus the model-specific Opus 5, Sonnet 5, and Fable 5 pages under that path
   - Claude facts and runtime: `https://platform.claude.com/docs/en/about-claude/models/overview`, `https://platform.claude.com/docs/en/build-with-claude/effort`, and base `https://code.claude.com/docs/en/` pages `skills`, `sub-agents`, `workflows`, `scheduled-tasks`, `permission-modes`, `ultraplan`, `goal`
5. `$openai-docs` for current OpenAI guidance; use community sources only as corroboration after official sources fail.

## Cross-agent packaging contract

- Keep one portable `SKILL.md` package for Codex and Claude Code.
- Keep agent-neutral behavior in `SKILL.md` and `references/`; `agents/openai.yaml` is Codex UI metadata only.
- Runtime and model differences affect prompt content, not package format. Note that skill *frontmatter* surfaces are asymmetric between the two runtimes even where the body is portable — see `60-skill-authoring.md`.

## Freshness triggers

Re-fetch for prices, token limits, effort or verbosity names, latest/current/model-choice claims, versions, defaults, flags, goal and loop behavior, subagent nesting and concurrency limits, or any fact newer than the reference's caveat date.

Three areas have proven especially volatile across revisions and should be re-verified rather than carried forward: harness version gates and hard limits in Claude Code, subagent spawning defaults and depth behavior, and the exact discovery paths for skills and agent definitions in both runtimes. Each of these changed in ways that silently broke prompts written against the previous documentation.

## What each reference file owns

| File | Owns |
|---|---|
| `05-trigger-syntax.md` | `$` vs `/` skill-invocation rule by runtime |
| `06-invocation-and-composition.md` | Trigger placement, role consistency, goal splitting, delegation polarity |
| `10-gpt-5-6.md` | GPT-5.6 variant selection, tuning, prompting, and tool orchestration |
| `11-codex-runtime-features.md` | Codex `/goal`, subagents, batch jobs, `AGENTS.md`, and skills |
| `20-opus-5.md` | Claude Opus 5 model-level prompting |
| `30-sonnet-5.md` | Claude Sonnet 5 model-level prompting |
| `40-fable-5.md` | Claude Fable 5 model-level prompting and its opt-in specialist role |
| `41-claude-code-runtime-features.md` | Claude Code `/loop`, agents, workflows, Ultraplan, and `/goal` |
| `50-effort-and-thinking.md` | Cross-model effort and thinking decision procedure |
| `60-skill-authoring.md` | Writing a production-grade skill for either runtime |
| `70-agent-instruction-files.md` | Writing `AGENTS.md` and `CLAUDE.md` |
| `80-subagent-authoring.md` | Defining and prompting agents and subagents |
| `90-model-selection.md` | Cross-model choice and companion routing |

## Scope changes in this revision

Claude Opus 4.8 is retired from this pack's scope. Opus 5 supersedes it at identical pricing with materially higher measured capability, so the previous Opus 4.8 reference file was replaced rather than kept alongside. Prompts and pins tuned for Opus 4.8 must be re-validated rather than carried forward, because several of that model's documented behaviors invert on Opus 5 — most consequentially its bias on subagent delegation and its need for explicit verification instructions. See `20-opus-5.md`.

## Interpretation contract

Carry caveats forward. Never convert uncertainty into a firm instruction, and never infer that something is false from an absence of evidence — say the docs do not state it. Where official sources or `$alaa-workflow` disagree with this skill, report the drift, prefer current official and runtime truth for the task at hand, and reconcile the owner file afterwards instead of silently choosing.
