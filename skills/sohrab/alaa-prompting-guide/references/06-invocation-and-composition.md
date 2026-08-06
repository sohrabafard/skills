# Skill Invocation and Prompt Composition

A generated prompt that names a skill has not necessarily activated it. Activation fails silently when the trigger is buried mid-paragraph, when the session role contradicts the skill's role, when a compact goal is inflated back into an operating manual, or when the wrong form is written for the surface that will execute it. Apply every rule here before finalizing any prompt that must activate a skill.

## Writing a call site

**Write `/name`.** One form, every call site, both runtimes. The pack's plugin build rewrites `$name` and `/name` alike to `/<plugin-namespace>:name` in the packaged Markdown, so a second form is redundant in the artifact that actually ships and costs characters against the description budget — `skills/sohrab/AGENTS.md` owns that budget and the rewrite cost. The one place a bare `$` is still correct is `agents/openai.yaml`, which is Codex-only interface metadata that no build rewrites.

## How a skill is actually reached

Three mechanisms, and a prompt author must know which one they are relying on.

**Selection from the host's picker.** Typing `/` opens a command palette that lists installed skills in Claude Code and in the Codex app and CLI, where `/skills` also opens a dedicated browser. Selection is deterministic: the chosen skill loads. This is a user action, so it is not available to a prompt.

**An explicit textual mention.** This is what a generated prompt has. The sigil is a property of the surface that reads the text: `/name` in Claude Code, `$name` in Codex CLI and the IDE extension, `@name` in ChatGPT. Inside this pack the build makes the question moot, but a prompt written to be pasted raw into Codex or ChatGPT outside the plugin must carry that surface's sigil or the mention will not resolve.

**An implicit description match.** Both hosts load every skill's name and description first and load the body only after deciding the skill applies. A prompt that describes the work in the description's own trigger words can activate a skill with no sigil at all — reliably enough to depend on when the description is well written, never reliably enough to be the only mechanism when activation is required.

Resolve the registered name rather than guessing it. In Claude Code the command name comes from the skill's directory or file name for personal and project skills, while a plugin skill resolves under `/plugin-name:skill-name`, where the frontmatter `name` sets only the last segment. In Codex, read the `name:` frontmatter field. Prefer the namespaced form for a plugin skill even where a bare alias also resolves, because the alias works only while no other command claims that name and is therefore the wrong thing to hard-code into a generated prompt. Claude Code merged custom commands into skills, so `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both answer to `/deploy`, and either is a valid target.

## Mention versus invocation

- An **invocation** activates a skill: the trigger opens the message, or the prompt explicitly instructs "invoke the `<name>` skill now, before any other action."
- A **mention** is inert. A trigger in backticks mid-sentence — "then use `/name` to…" — is a reference the model may ignore. Never rely on a mention when activation is required.
- One primary trigger per message. Skills that lanes must load are named inside the lane dispatch text as instructions ("load `<name>` and apply it"), never as competing triggers at the top level.

## Role-consistency contract

A session holds exactly one role. The most common orchestration failure is a prompt that names an orchestrator skill and then writes every imperative at the session as an implementer — the model obeys the dominant verbs, not the buried clause.

- When the prompt routes execution through `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator`, the session role is **orchestrator or lead**, stated in the first sentences: plan lanes, dispatch, enforce the review gate, reconcile, run integrated validation, commit when lanes must not. Add the explicit negative: "Do not write implementation code in this session."
- Every implementation verb — implement, edit, fix, test-first, refactor, document — moves into **lane rules**, a block the orchestrator copies into dispatches, and never into the lead's own instructions.
- Run a verb-ownership audit before sending: read each imperative and assign it to lead or lane. A lane verb aimed at the lead, or a lead verb aimed at a lane, is a defect.

## Single-message forms, and the optional two-message split

Two single-message shapes both work. Choose by whether you want the runtime's harness-enforced auto-continue.

**Trigger-led — deterministic activation, no harness loop.** The message leads with the exact skill trigger, assigns the role and lane rules, and closes with the completion condition and a turn or time bound inline. The skill activates reliably because its trigger leads, and the invoked skill's own drive carries the work to completion. Best when the skill is itself the completion engine.

**Goal-led — harness auto-continue, implicit activation.** The message is a single `/goal` whose text is both the directive for the first turn and the completion condition the harness re-checks each turn. Because the goal command must lead the message, the skill it needs activates only implicitly, so open the condition by naming and describing that skill's role — "Acting as the `<name>` orchestrator, lead the lanes…" — to make the description match fire, then give the operating context, lane rules, a measurable end state, and a turn or time bound. Keep it inside the runtime's limit; `references/41-claude-code-runtime-features.md` and `references/11-codex-runtime-features.md` carry the current caps. Accept that implicit activation is model judgment rather than a guaranteed trigger — that is the reliability cost of one message.

One Claude Code constraint belongs in this decision: the goal evaluator judges only what is already in the transcript, runs no tools, and reads no files. Write the condition as something the session's own output can demonstrate — "`npm test` exits 0", "`git status` is clean" — not as a state the evaluator would have to go and check.

**Two messages** are needed only to combine deterministic activation *and* harness auto-continue, since a leading skill trigger and a leading goal command cannot share one message. Send the skill-triggering operating prompt first, then a compact goal holding only the completion condition. Never inflate that compact goal back into an operating manual.

## Satisfiable completion conditions

A completion condition must be reachable, or the harness loops until the turn cap. "Zero findings from a fresh adversarial pass" is the canonical unreachable condition, because an adversarial reviewer with fresh context reliably finds new defensible items every pass. Bound convergence structurally instead: define done by a severity threshold — zero open blocker and major findings, with minors and nits reported rather than looped; cap review-fix cycles explicitly, two being the orchestrator packs' default; make the final adversarial pass a reporting pass whose findings go to the user rather than into another cycle; and pay the full gate set once after the last fix, with targeted checks per fix. Every goal-form prompt also carries an explicit turn or time cap as a safety net — the cap is the backstop, the structural bounds are the brake.

## Delegation polarity

This section owns the rule; other references point here rather than restating it.

**Match the polarity of your delegation language to the target model's default bias.** There is no single correct direction. A prompt that authorizes fan-out on a model that already over-delegates multiplies cost for nothing; a prompt that only restricts fan-out on a model that never delegates unprompted produces a single-threaded session that quietly does everything itself. Polarity defects are silent — nothing errors, and the verb-ownership audit will not catch them — so check polarity separately against the target model.

- **Claude Opus 5 — eager; cap it.** Anthropic's guide states that Opus 5 delegates to subagents more readily than prior models, that delegation multiplies cost and time when applied to small tasks, and that authors should give explicit guidance on which scenarios warrant delegation or set deterministic caps on how many agents may launch. Delegation language for Opus 5 is a ceiling rather than a permission: delegate only for large, genuinely independent, parallelizable tracks; do not delegate work finishable in a handful of tool calls; prefer one subagent over several; keep spawn counts low.
- **Claude Fable 5 — eager, and the correction is shape rather than volume.** Fable 5 dispatches parallel subagents readily, and the guidance is to use subagents frequently while giving explicit criteria for when delegation is appropriate, preferring asynchronous orchestrator-to-subagent communication over blocking on each return. Add selection criteria and non-blocking dispatch, not encouragement.
- **Claude Sonnet 5 — treat as neutral-to-eager, and verify.** The Sonnet 5 guide does not address delegation. It does state that Sonnet 5 is more agentic than its predecessor and will reach for tools and run self-verification loops more readily. Absence of a delegation note is not evidence of under-fan-out; measure on your own harness before writing polarity either way.
- **Codex and GPT-5.6 — reticent; authorize it.** The Codex documentation is explicit that Codex spawns a subagent only when asked and does not fan out on its own. This is the family where positive-authorization wording is exactly right: "spawn one lane per independent slice in the same turn, without asking" beats "parallel work is authorized only for independent lanes."

Two rules hold whichever direction you write.

**Constraints belong in lane rules, not in the delegation sentence.** Disjoint scopes, a single writer per file, the shared validation command, the review gate — these are properties of the work partition. Putting them in the delegation sentence is what turns authorization into restriction and restriction into noise.

**An invoked orchestrator skill's own fan-out policy wins.** When `/alaa-cc-orchestrator` or `/alaa-codex-orchestrator` is invoked, do not override its delegation stance from the calling prompt; add or tighten lane rules instead.

Delete carried-over verification scaffolding of the form "use a subagent to verify" or "add a final verification step" — current models verify their own work without being told, and the instruction causes over-verification. When you are about to remove such an instruction, read `references/80-subagent-authoring.md` first, because it owns the test that separates a redundant self-check from an independent gate that must survive.

## Pre-send checklist

1. The message opens with either the exact skill trigger or a goal command that names the needed skill's role, using the exact installed name for the executing surface, never a buried mid-paragraph trigger.
2. The session has one role, consistent with the invoked skill, and implementation verbs live in lane rules.
3. The single-message form is chosen deliberately: trigger-led for deterministic activation, goal-led for harness auto-continue. Two messages only to get both.
4. Delegation wording matches the target model's default bias — a cap and selection criteria for Opus 5 and Fable 5, explicit positive authorization for Codex, measured rather than assumed for Sonnet 5.
5. Skills needed by lanes are named inside dispatch text, not as top-level triggers.
6. In goal form, the completion condition is demonstrable from the transcript and carries an explicit turn or time clause.
7. If the prompt will be pasted raw into a surface outside this plugin, the mention sigil matches that surface.

## The failure shape to recognize

Bad: a goal block opening "You are the senior implementer…", with "then use `/alaa-cc-orchestrator` to lead the lanes" buried mid-paragraph. The skill never loads and the session implements everything itself.

Fix, in either single-message form. Trigger-led: start `/alaa-cc-orchestrator Orchestrator mode — <goal>`, assign the orchestrator role with the do-not-implement negative, put implementation discipline in lane rules, and state the completion condition and turn bound inline. Goal-led: start `/goal Acting as the <name> orchestrator, …` so the skill loads implicitly, with the same role, lane rules, and condition inline. Add a separate goal message only to layer the harness loop onto the trigger-led form.

For durable multi-phase work that outgrows a single goal, route to `/alaa-workflow` rather than lengthening the completion condition.

## Freshness

Verified against live documentation on 6 August 2026. Re-check before quoting: the goal-command character cap and evaluator scope in Claude Code, the Codex goal limits, and the per-model delegation-bias claims, which are the values most likely to move — polarity in particular has inverted before and is the section to re-read on every model upgrade. The Sonnet 5 position is marked unverified because its guide is silent on delegation, not because it was measured and found neutral.

## Sources

- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
- [Developer commands (OpenAI)](https://learn.chatgpt.com/docs/developer-commands)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Keep Claude working toward a goal (Claude Code)](https://code.claude.com/docs/en/goal)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
