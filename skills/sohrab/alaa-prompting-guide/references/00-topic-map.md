# Topic Map

The router for this skill. Every reference below is unread until its condition fires, and that is the point: the body of a skill is paid for on every run, while a reference is paid for only when something makes it necessary. Match your situation to a row, read that file, and do not pre-load the rest.

Rows are conditions, not headings. If your situation is not listed, no reference here owns it — say so rather than reading the nearest-looking file.

| You are about to | Read | Because |
|---|---|---|
| Decide how a generated prompt will actually activate a skill, write a call site, place a trigger, choose between a trigger-led and a goal-led message, or write a completion condition | `references/06-invocation-and-composition.md` | Syntax alone does not activate a skill; placement, role consistency, and reachability do |
| Write delegation language and need to know whether to cap fan-out or authorize it | `references/06-invocation-and-composition.md` | It owns delegation polarity, and the wrong direction fails silently on either family |
| Tune a prompt for GPT-5.6 in Codex, or choose among its variants | `references/10-gpt-5-6.md` | Variant, effort, and tool-orchestration behavior are model-specific and not inferable |
| Use Codex's goal loop, subagents, batch jobs, `AGENTS.md` discovery, or its slash commands | `references/11-codex-runtime-features.md` | These are harness features with version gates and hard limits a prompt must respect |
| Tune a prompt for Claude Opus 5 | `references/20-opus-5.md` | Its response-length, delegation, and self-correction behavior determine what to write and what to omit |
| Tune a prompt for Claude Sonnet 5 | `references/30-sonnet-5.md` | It follows instructions more literally than the flagship, which changes how a constraint must be scoped |
| Tune a prompt for Claude Fable 5, or judge whether its cost is justified | `references/40-fable-5.md` | It is an opt-in specialist, so the first question is whether to use it at all |
| Use Claude Code's `/loop`, subagents, workflows, plan mode, or `/goal` | `references/41-claude-code-runtime-features.md` | Concurrency caps, nesting defaults, and evaluator scope decide whether a prompt can work |
| Set or change an effort level, or judge whether a lane needs a higher tier | `references/50-effort-and-thinking.md` | Model and effort are separate decisions, and an effort inherited from another generation is an untested assumption |
| Write, review, or repair a skill | `references/60-skill-authoring.md` | It owns the authoring procedure, including the draft-then-compress rewrite and how to split a subject into references |
| Look up a skill discovery path, a frontmatter key surface, or a description character budget | `references/61-skill-platform-mechanics.md` | These are per-runtime lookups that go stale and must not be recalled from memory |
| Write, trim, or split an `AGENTS.md` or `CLAUDE.md` | `references/70-agent-instruction-files.md` | An instruction file is loaded unconditionally, so its economics differ from every other artifact here |
| Define a subagent, pin its model, effort, and tools, or write its dispatch text | `references/80-subagent-authoring.md` | It owns authority boundaries, output contracts, and the test separating a redundant self-check from a real gate |
| Choose a model, or compare models across runtimes | `references/90-model-selection.md` | One table beats re-deriving the comparison from four model files |
| Ground a version-sensitive claim, or judge whether a number must be re-fetched before it is quoted | `references/00-source-map.md` | It owns source priority and the freshness triggers that decide when recall is not allowed |
