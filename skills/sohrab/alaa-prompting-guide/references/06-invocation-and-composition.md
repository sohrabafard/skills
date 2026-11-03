# Skill Invocation and Prompt Composition

A generated prompt that names a skill has not necessarily activated it. Activation fails silently when the trigger is buried mid-paragraph, when the session role contradicts the skill's role, when a compact goal is inflated back into an operating manual, or when the wrong form is written for the surface that will execute it. Apply every rule here before finalizing any prompt that must activate a skill.

## How a skill is actually reached

Three mechanisms, and a prompt author must know which one they are relying on.

**Selection from the host's picker.** Typing `/` opens a command palette listing installed skills in Claude Code and in the Codex app and CLI, where `/skills` also opens a dedicated browser. Selection is deterministic: the chosen skill loads. It is a user action, so it is never available to a prompt. Treat the Codex palette as observed behaviour rather than documented behaviour — it is evidenced by a bug report against the shipping app, while the documentation describes only `/skills`.

**An explicit textual instruction.** The sigil belongs to the executing surface: `/name` in Claude Code, `$name` in Codex CLI and the IDE extension, `@name` in ChatGPT. In Claude Code, a leading registered slash command invokes its skill directly; a mid-message slash name grants permission to use it but does not directly load it. Do not treat that permission as observed activation. A prompt aimed at Codex that carries `/name` uses the wrong textual invocation form.

**An implicit description match.** Both hosts load every skill's name and description first and load the body only after deciding the skill applies. A prompt that describes the work in the description's own trigger words can activate a skill with no sigil at all — reliably enough to depend on when the description is well written, never reliably enough to be the only mechanism when activation is required.

## Writing a call site

Two questions hide under one word here, and answering the wrong one is how a generated prompt silently activates nothing.

**In a prompt you generate for another surface to run, write that surface's sigil**, from the list above. Where a prompt pack carries per-runtime sections, apply one sigil consistently inside each section and switch it at the section boundary; a paragraph that mixes forms is wrong under both runtimes.

**In this repository's own Markdown, write `/name`** — one form, every call site. The plugin build rewrites `$name` and `/name` alike to `/<plugin-namespace>:name` in the packaged artifact, so a second form buys nothing and costs characters against the description budget. This rule governs files that pass through that build, and says nothing about the prompts those files instruct an agent to write, which follow the paragraph above. The one bare `$` that stays correct is in `agents/openai.yaml`, Codex interface metadata that no build rewrites.

Resolve the registered name rather than guessing it. In Claude Code the command name comes from the skill's directory or file name for personal and project skills, while a plugin skill resolves under `/plugin-name:skill-name`, where the frontmatter `name` sets only the last segment. In Codex, read the `name:` frontmatter field. Treat `/plugin-name:skill-name` as the only stable form to hard-code into a generated prompt: the bare alias is version-gated behaviour that has changed inside the current release line, and it resolves only while no other command claims that name. Claude Code merged custom commands into skills, so `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both answer to `/deploy`, and either is a valid target.

## Mention versus invocation

- A leading registered Claude Code skill command is a direct **invocation**. An instruction to load a skill is a request; require evidence of loading before depending on its contract.
- A mid-message Claude Code slash **mention** grants permission without direct invocation. Use a leading command when deterministic activation is required.
- One primary trigger per message. Skills that lanes must load are named inside the lane dispatch text as instructions ("load `<name>` and apply it"), never as competing triggers at the top level.

## Compose from skill owners

Route reusable doctrine to the narrowest applicable canonical skill. Before replacing prompt text with a skill call, resolve its registered name, target syntax, and source the recipient can read. Make each companion's load condition and decision explicit. If a required source is unavailable when needed, use an already authorized equivalent that preserves the obligation, or block dependent work.

State the outcome, scope, inputs, constraints, authority, acceptance criteria, required evidence and stopping conditions in the prompt or named task record. Load `/alaa-workflow` when composing workflow prompts. Resolve exact bindings and pass them to children through `alaa-workflow references/companion-routing.md`. Carry the engagement's review cadence and cursor through the runtime orchestrator's gate contract.

## Role-consistency contract

A session holds exactly one role. The most common orchestration failure is a prompt that names an orchestrator skill and then writes every imperative at the session as an implementer — the model obeys the dominant verbs, not the buried clause.

- State the **orchestrator or lead** role in the opening when invoking `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator`. Assign planning, dispatch, reconciliation, review gates, integrated validation and authorized integration to the lead. Route local commits through `alaa-workflow references/workspace-and-integration.md` and the applicable standing or explicit authority.
- Put implementation instructions in **lane rules** for the lead to copy into dispatches. Assign an edit to the lead only under the invoked orchestrator's mechanical-edit exception.
- Audit each imperative before sending. Assign it to the lead or lane according to that role's authority.

## Compose the kickoff and completion condition

Resolve the executing surface and its goal support. Use a skill-led kickoff for orchestrated or long work. Name any plan in the kickoff. Without a requested goal loop, send only the kickoff.

**Claude Code.** Check Desktop tab and command support in `references/41-claude-code-runtime-features.md`. For orchestrated or long work, send the kickoff first. After skill activation and any required planning approval, send a separate `/goal` with only the completion condition. The command starts execution immediately. Apply the Desktop plain-text argument rule to both messages. Keep manuals, role rosters, lane instructions and model policy outside the condition. Use a single Claude goal only for self-contained work that needs neither skill activation nor long instructions.

**Codex.** Follow `references/11-codex-runtime-features.md` for the active host. Where verified, one leading `/goal` composer message can carry kickoff context and a distinct completion condition after required skill activation and approvals. A skill name inside the objective does not establish activation. If the kickoff must load skills or obtain planning approval, use a regular message. Include an explicit request to create the goal with the available tools after those prerequisites. If that route is unavailable, separate the kickoff from goal activation.

Aim for one to three short sentences for the condition, normally at most 600 characters. This house target yields to required evidence, authority and stopping content. Count the rendered condition after substitutions, including spaces and newlines. Apply only the verified limit for the target surface and input path. Put extra context in the kickoff, an authorized workflow plan or the verified composer file route.

For Claude, require transcript evidence: acceptance verdicts, commands and exit results, because the evaluator cannot inspect files or run checks. A plan pointer alone proves no acceptance. Preserve unrelated dirty-tree work; use scoped criteria instead of requiring a clean tree.

Example for a registered Claude Code skill (resolve the namespace before use; substitute the task and bound):

```text
/<registered-orchestrator> Orchestrator mode: deliver <outcome> within <scope>. Load alaa-workflow; save the execution plan with its exact phase/task skill mappings before dispatch. Preserve <invariants>. Local edits and checks only; no commit or external effects.
```

Send separately after loading and planning:

```text
/goal The scoped outcome meets the plan's acceptance criteria, with required checks passing and review disposition reported in the transcript; or a BLOCKED report names the cause and next safe action; or 25 goal evaluations end with an INCOMPLETE progress report.
```

The example bound is task input, not a runtime default. A blocked or bounded exit stops continuation without claiming successful completion.

## Satisfiable completion conditions

Keep completion reachable: unlimited fresh adversarial passes may never converge. Use the orchestrator's severity, fix-cycle and reporting rules without copying them into the goal. Include a task-specific turn or time bound and a blocked exit naming the cause and next safe action. Distinguish success, blocked and incomplete; a bound proves no acceptance and a goal grants no new authority.

## Delegation polarity

This section owns the rule; other references point here rather than restating it.

**Match the polarity of your delegation language to the target model's default bias.** There is no single correct direction. A prompt that authorizes fan-out on a model that already over-delegates multiplies cost for nothing; a prompt that only restricts fan-out on a model that never delegates unprompted produces a single-threaded session that quietly does everything itself. Polarity defects are silent — nothing errors, and the verb-ownership audit will not catch them — so check polarity separately against the target model.

- **Claude Opus 5.5 — bound delegation.** Current guidance says Opus delegates readily and small-task delegation multiplies cost/time. State observable delegation criteria or a justified task cap: independent parallel tracks must warrant isolation, and work finishable in a handful of tool calls stays inline. Do not impose a universal one-agent preference; the invoked orchestrator owns lane scheduling and observed capacity.
- **Claude Fable 5.1 — constrain the work shape.** Current Fable dispatches parallel subagents readily, and the guidance is to use subagents frequently while giving explicit criteria for when delegation is appropriate, preferring asynchronous orchestrator-to-subagent communication over blocking on each return. Add selection criteria and non-blocking dispatch, not encouragement.
- **Claude Haiku 5.5 — bound delegated work explicitly.** Give one concrete task, named retrieval sources, required checks and completion/failure conditions. General fan-out polarity remains unmeasured; never infer lead suitability from subagent performance. Read `references/36-haiku-5-5.md` before tuning.
- **Claude Sonnet 5.5 — general polarity remains unmeasured.** Current guidance describes extra reviewer delegation at higher efforts, not a universal delegation bias. Give explicit independent scopes and stopping conditions; measure fan-out in the target harness before adding broader encouragement or suppression.
- **Codex — explicit authorization and bounded lanes.** Use the current host's delegation
  rules and available tools. When authorized, name concrete independent scopes and their result
  contracts. Do not infer a universal GPT-6 delegation bias from a previous generation or an API
  feature; `references/11-codex-runtime-features.md` owns the runtime boundary.

Two rules hold whichever direction you write.

**Constraints belong in lane rules, not in the delegation sentence.** Disjoint scopes, a single writer per file, the shared validation command, the review gate — these are properties of the work partition. Putting them in the delegation sentence is what turns authorization into restriction and restriction into noise.

**An invoked orchestrator skill's own fan-out policy wins.** When `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` is invoked, do not override its delegation stance from the calling prompt; add or tighten lane rules instead.

Before removing verification language for current Opus, Sonnet or Fable, read
`references/80-subagent-authoring.md`. It owns the distinction between redundant self-check
reminders and focused tests or independent acceptance gates. The Fable 5 exception in
`references/40-fable-5.md` is historical and does not transfer to Fable 5.1. Never assume that less checking
proves equal quality.

## Pre-send checklist

1. The executing surface, registered skill name and recipient-readable source are resolved. Required activation is observed before the goal starts.
2. The session has one role consistent with the invoked skill. Implementation instructions follow its role boundary.
3. The kickoff and condition follow the surface-specific composition rules above.
4. Delegation wording matches the target model's default bias — bounded selection criteria for current Opus and Fable, current authorization and bounded scopes for Codex, measured rather than assumed for Sonnet 5.5.
5. Exact phase/task skill mappings follow the workflow contract and reach dispatches; they are absent from the goal condition.
6. In goal form, the completion condition is demonstrable from the transcript and carries an explicit turn or time clause.
7. If the prompt will be pasted raw into a surface outside this plugin, the mention sigil matches that surface.
8. Count the rendered condition against any verified limit. Confirm required content survives compression. A static pass proves neither activation nor live acceptance.

## The failure shape to recognize

Bad: a goal block opening "You are the senior implementer…", with "then use `/alaa-cc-orchestrator` to lead the lanes" buried mid-paragraph. The skill never loads and the session implements everything itself.

Fix: invoke the registered orchestrator in the kickoff, route durable planning to `/alaa-workflow`, then use the goal route for the executing surface when a loop is requested. Keep task instructions in the kickoff, plan and dispatches rather than lengthening the evaluator's condition. Diagnose a rejected command through the runtime preflight before changing the prompt or suggesting another surface.

## Freshness

Claude goal, Desktop Code and slash-invocation semantics refreshed 4 October 2026. The Desktop composer rejection is user-observed evidence in the runtime reference; its release boundary and the exact rejected payload remain unknown. Other invocation mechanics retain their 6 August 2026 verification. Claude delegation guidance was refreshed 25 September 2026 and Sonnet 5.5 on 29 September; its general polarity remains unmeasured. Re-fetch before relying on a cap, surface or bias. The Codex slash picker is observed in a bug report; `/skills` is documented.

## Sources

- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
- [Developer commands (OpenAI)](https://learn.chatgpt.com/docs/developer-commands)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Keep Claude working toward a goal (Claude Code)](https://code.claude.com/docs/en/goal)
- [Claude Code on desktop](https://code.claude.com/docs/en/desktop)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Subagents (Codex)](https://developers.openai.com/codex/subagents)
- [Follow a goal (Codex)](https://learn.chatgpt.com/use-cases/follow-goals)
- [Duplicate skills in the Codex slash picker (openai/codex issue 22626)](https://github.com/openai/codex/issues/22626)
