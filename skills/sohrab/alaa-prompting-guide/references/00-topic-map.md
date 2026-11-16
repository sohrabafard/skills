# Topic Map

The router for this skill. Match your situation to a row and read that file. Preload no other reference. When no row matches, no reference here owns the situation: say so, and do not read the nearest-looking file.

| You are about to | Read | It decides |
|---|---|---|
| Activate a skill in a generated prompt, choose a kickoff and a goal condition, or prepare phase and task skill routing | `references/06-invocation-and-composition.md` | The message shape: direct invocation, session role, reachable completion |
| Write delegation language, and need to know whether to cap fan-out or authorize it | `references/06-invocation-and-composition.md` | Delegation polarity per model; the wrong direction fails silently |
| Tune GPT prompts or choose active Codex profiles | `references/12-gpt-6.md` | Model capability, runtime availability and local policy, kept apart |
| Handle an explicit user request for a legacy model | `references/90-model-selection.md` | How to record it; it restores no ordinary eligibility and passes no task-control validation |
| Use Codex's goal loop, subagents, batch jobs or slash commands, or diagnose rejected tool input or patch context | `references/11-codex-runtime-features.md` | The supported operation under the harness and the active tool contract |
| Tune current Opus prompting or migrate older Opus instructions | `references/21-opus-5-5.md` | Calibration and API boundaries |
| Tune current Sonnet prompting or migrate Sonnet API controls | `references/31-sonnet-5-5.md` | Recalibrated effort, thinking modes and tool contracts |
| Tune current Haiku prompts, or select bounded retrieval, verification or documentation | `references/36-haiku-5-5.md` | The completion, retrieval and check instructions that bounded work needs |
| Tune current Fable prompting | `references/43-fable-5-2.md` | Early-stop, approval, ownership, delegation and style behaviors |
| Use Claude Code's `/advisor`, `/loop`, subagents, workflows, plan mode or `/goal`, resolve a Desktop tab, or diagnose a rejected goal | `references/41-claude-code-runtime-features.md` | What can run: surface support, advisor pairs, limits, evaluator scope |
| Write a prompt, system prompt or dispatch for a Claude model whose session may have the advisor on | `references/41-claude-code-runtime-features.md` section *Prompts for a session that may have an advisor* | What to write about the advisor, per executor model |
| Set or change an effort level, or judge whether a lane needs a higher tier | `references/50-effort-and-thinking.md` | The effort and thinking procedure; an inherited effort is untested |
| Decide whether what you write is a prompt, an instruction file, a skill, a script or a subagent | `references/60-skill-authoring.md` | The artifact test |
| Write, review or repair a skill | `references/60-skill-authoring.md` | The authoring procedure and the split into references |
| Shorten or edit an artifact that controls another agent, or judge whether a change altered behavior | `references/60-skill-authoring.md`, with the artifact's own reference | Equivalence and compression; the artifact's reference owns its structure and content |
| Carry a prompt, skill, agent file, instruction file, memory or note written for an earlier model to a newer one | `references/60-skill-authoring.md` | The carry-over review; the target model's reference owns the evidence for each check |
| Plan an authorized comparison of instruction variants | `references/60-skill-authoring.md` | Comparable starting conditions, outcome measures and evidence limits |
| Look up a skill discovery or install path, a frontmatter key surface, a description budget, or official structure guidance for `SKILL.md` | `references/61-skill-platform-mechanics.md` | Per-runtime values that go stale; never recall them |
| Write, trim or split an `AGENTS.md` or `CLAUDE.md`, or rely on the order or the size limit of the instruction-file chain | `references/70-agent-instruction-files.md` | What an always-loaded file holds, and what each runtime loads; trimming one also needs the compression row |
| Define a model-neutral subagent and its tools, or write explicit task controls in a dispatch | `references/80-subagent-authoring.md` | Authority boundaries, output contracts, and the test that separates a redundant self-check from a real gate; shortening a definition or a dispatch also needs the compression row |
| Choose a model for either runtime | `references/90-model-selection.md` | The capability evidence and the owner of task selection |
| Ground a version-sensitive claim, or judge whether a number must be re-fetched before you quote it | `references/00-source-map.md` | Source priority and the freshness triggers that forbid recall |
