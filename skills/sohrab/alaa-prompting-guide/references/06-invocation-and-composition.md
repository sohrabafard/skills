# Skill Invocation and Prompt Composition

A prompt that names a skill has not activated it. Activation fails silently when the trigger sits mid-paragraph, when the session role contradicts the skill's role, when the goal condition carries an operating manual, or when the sigil belongs to another surface.

## How a skill is reached

- **Picker.** Typing `/` opens a palette of installed skills in Claude Code and in the Codex app and CLI; `/skills` opens the Codex browser. It is a user action, never available to a prompt. The Codex palette is observed in a bug report; the documentation describes only `/skills`.
- **Explicit text.** Write the sigil of the executing surface: `/name` in Claude Code, `$name` in Codex CLI and the IDE extension, `@name` in ChatGPT.
- **Description match.** Both hosts load names and descriptions first, and a body only after they decide it applies. The description's own trigger words can activate a skill with no sigil. Never make this the only mechanism when activation is required.

In Claude Code a leading registered slash command invokes its skill directly. A slash name in mid-message grants permission to use the skill and does not load it. An instruction to load a skill is a request: require evidence of loading before you depend on the skill's contract.

## Writing a call site

- **A prompt generated for another surface** carries that surface's sigil. A prompt pack with per-runtime sections uses one sigil in each section; a paragraph that mixes forms is wrong under both runtimes.
- **This repository's own Markdown** carries `/name` at every call site. `skills/sohrab/AGENTS.md` owns that rule and its `agents/openai.yaml` exception. It governs files that pass through the plugin build, not the prompts those files tell an agent to write.
- **Resolve the registered name; never guess it.** In Claude Code a personal or project skill takes its command name from its directory or file name, and a plugin skill resolves under `/plugin-name:skill-name`, where frontmatter `name` sets only the last segment. In Codex, read the `name:` frontmatter field.
- **Hard-code only `/plugin-name:skill-name` into a generated prompt.** The bare alias is version-gated and resolves only while no other command claims the name.
- Claude Code merged custom commands into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both answer to `/deploy`.
- **Put one primary trigger in each message.** Name the skills a lane must load inside the lane dispatch as instructions ("load `<name>` and apply it"), never as competing top-level triggers.

## Compose from skill owners

- Route reusable doctrine to the narrowest canonical skill. Before you replace prompt text with a skill call, resolve the registered name, the syntax on the target surface, and a source the recipient can read. State each companion's load condition and what it decides.
- When a required source is unavailable, use an already authorized equivalent that preserves the obligation, or block the dependent work.
- State the outcome, scope, inputs, constraints, authority, acceptance criteria, required evidence and stop conditions in the prompt or in a named task record.
- For a workflow prompt, load `/alaa-workflow`, and pass exact bindings to children through `alaa-workflow references/companion-routing.md`. Carry the engagement's review cadence and cursor through the runtime orchestrator's gate contract.

## Role consistency

A session holds exactly one role. The model obeys the dominant verbs, not a buried clause: a block that opens "You are the senior implementer" and names the orchestrator mid-paragraph never loads the skill, and the session implements everything itself.

- When you invoke `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator`, state the orchestrator or lead role in the opening. Give the lead planning, dispatch, reconciliation, review gates, integrated validation and authorized integration.
- Route local commits through `alaa-workflow references/workspace-and-integration.md` and the applicable authority.
- Write implementation instructions as lane rules that the lead copies into dispatches. Assign an edit to the lead only under the orchestrator's mechanical-edit exception.
- Before you send, check that each imperative addresses the role that holds its authority.

## Kickoff and completion condition

Resolve the executing surface and its goal support. Use a skill-led kickoff for orchestrated or long work, and name any plan in it. When no goal loop was requested, send only the kickoff.

**Claude Code.** Check the Desktop tab and command support in `references/41-claude-code-runtime-features.md`.

1. Send the kickoff.
2. After the skill is active and any required plan is approved, send a separate `/goal` that holds only the completion condition. The command starts execution immediately.

For a goal that will run long on a Claude model, apply `references/41-claude-code-runtime-features.md` *Prompts for a session that may have an advisor* to the kickoff.

Apply the Desktop plain-text argument rule to both messages. Keep manuals, role rosters, lane instructions, skill mappings and model policy out of the condition. Use a single goal message only for self-contained work that needs neither skill activation nor long instructions.

**Codex.** Follow `references/11-codex-runtime-features.md` for the active host. Where verified, one leading `/goal` composer message can carry the kickoff context and a distinct completion condition, after required skill activation and approvals. A skill name inside the objective establishes no activation. When the kickoff must load skills or get planning approval, send a regular message that asks to create the goal with the available tools after those prerequisites. When that route is unavailable, separate the kickoff from goal activation.

**The condition, on either runtime:**

- Aim for one to three short sentences, normally at most 600 characters. This house target yields to required evidence, authority and stop content.
- Count the rendered condition after substitutions, including spaces and newlines. Apply only the verified limit of the target surface and input path. A static count proves neither activation nor live acceptance.
- Put extra context in the kickoff, an authorized workflow plan or the verified composer file route.
- For Claude, require transcript evidence: acceptance verdicts, commands and exit results. The evaluator can inspect no file and run no check, so a plan pointer alone proves no acceptance.
- Preserve unrelated dirty-tree work: write scoped criteria, not a clean-tree requirement.
- Keep completion reachable: unlimited fresh adversarial passes may never converge. Use the orchestrator's severity, fix-cycle and reporting rules without copying them into the goal.
- Include a task-specific turn or time bound and a blocked exit that names the cause and the next safe action. Distinguish success, blocked and incomplete. A bound proves no acceptance, a blocked or bounded exit claims no success, and a goal grants no new authority.

Example for a registered Claude Code skill. Resolve the namespace first, and substitute the task and the bound, which is task input and not a runtime default:

```text
/<registered-orchestrator> Orchestrator mode: deliver <outcome> within <scope>. Load alaa-workflow; save the execution plan with its exact phase/task skill mappings before dispatch. Preserve <invariants>. Local edits and checks only; no commit or external effects.
```

Send separately after loading and planning:

```text
/goal The scoped outcome meets the plan's acceptance criteria, with required checks passing and review disposition reported in the transcript; or a BLOCKED report names the cause and next safe action; or 25 goal evaluations end with an INCOMPLETE progress report.
```

When a command is rejected, diagnose it through the runtime preflight before you change the prompt or suggest another surface.

## Delegation polarity

This section owns the rule. **Match the polarity of the delegation language to the target model's default bias.** Authorizing fan-out on a model that already over-delegates multiplies cost. Only restricting fan-out on a model that never delegates unprompted gives a single-threaded session. Neither defect errors, and the role check above does not catch it.

| Target | Write |
|---|---|
| Claude Opus 5.5 | **Bound delegation.** It delegates readily, and a delegated small task multiplies cost and time. State observable delegation criteria or a justified task cap: independent parallel tracks must warrant isolation, and work that finishes in a handful of tool calls stays inline. Impose no universal one-agent preference |
| Claude Fable 5.2 | **State the cost and the criteria.** Delegation depends on the harness: it rarely delegates through a minimal subagent tool and readily where prompts invite it. At `xhigh` and `max` it can start subagents to review its own work. Remove a standing delegate line the task no longer needs. State what a subagent costs, when delegation is worth it, when it is not, and how to brief one. Send review to the declared independent gate, never to a self-review subagent. Check which model each subagent uses by default. The Fable 5.1 guidance to delegate frequently is historical |
| Claude Haiku 5.5 | **Bound the delegated work.** Give one concrete task, named retrieval sources, required checks, and completion and failure conditions. General fan-out polarity is unmeasured; never infer lead suitability from subagent performance. Read `references/36-haiku-5-5.md` before tuning |
| Claude Sonnet 5.5 | **General polarity is unmeasured.** Guidance describes extra reviewer delegation at higher efforts, not a general bias. Give explicit independent scopes and stop conditions, and measure fan-out in the target harness before you add broader encouragement or suppression |
| Codex | **Explicit authorization and bounded lanes.** Below `ultra`, Codex delegates only when the prompt asks. When delegation is authorized, name concrete independent scopes and their result contracts. "Use subagents as needed" hands Codex the decision of when and how to split: write it only where no orchestrator and no lane plan owns the split. At `ultra`, Codex delegates on its own: give `ultra` only to a session that may start subagents. Source: `references/12-gpt-6.md` *GPT-6.2 behavior*, 18 November 2026. `references/11-codex-runtime-features.md` owns the runtime boundary |

Three rules hold in either direction:

- **Constraints belong in lane rules, not in the delegation sentence.** Disjoint scopes, one writer per file, the shared validation command and the review gate are properties of the work partition.
- **An invoked orchestrator's own fan-out policy wins.** When `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` is invoked, never override its delegation stance from the calling prompt; add or tighten lane rules instead. It owns lane scheduling and observed capacity.
- **Before you remove verification language** for current Opus, Sonnet or Fable, read `references/80-subagent-authoring.md`. The Fable 5 explicit-verification exception does not transfer to Fable 5.2. Less checking proves no equal quality.

## Freshness

| Fact group | Verified |
|---|---|
| Claude goal, Desktop Code and slash-invocation semantics | 4 October 2026 |
| Other invocation mechanics | 6 August 2026 |
| Claude delegation guidance | 25 September 2026; Sonnet 5.5 on 29 September 2026; Fable 5.2 on 14 November 2026 |
| Codex delegation guidance | 18 November 2026 |

The Desktop composer rejection is user-observed evidence in the runtime reference; its release boundary and exact payload are unknown. Re-fetch before you rely on a cap, a surface or a bias.

## Sources

- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
- [Developer commands (OpenAI)](https://learn.chatgpt.com/docs/developer-commands)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Keep Claude working toward a goal (Claude Code)](https://code.claude.com/docs/en/goal)
- [Claude Code on desktop](https://code.claude.com/docs/en/desktop)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Subagents (Codex)](https://developers.openai.com/codex/subagents)
- [Follow a goal (Codex)](https://learn.chatgpt.com/use-cases/follow-goals)
- [Duplicate skills in the Codex slash picker (openai/codex issue 22626)](https://github.com/openai/codex/issues/22626)
