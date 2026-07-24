# Skill Invocation Placement and Prompt Composition

Trigger syntax alone does not activate a skill. A generated prompt fails silently when the trigger is buried mid-paragraph, the session role contradicts the skill's role, or a compact two-message `/goal` is bloated back into an operating manual. Apply every rule here before finalizing any prompt that must activate a skill.

## Mention vs invocation

- An **invocation** activates a skill: the trigger opens the message, or the prompt explicitly instructs "invoke the `<name>` skill now, before any other action."
- A **mention** is inert: a trigger in backticks mid-sentence ("then use `/name` to…") is a reference the model may ignore. Never rely on a mention when activation is required.
- In Claude Code, use the exact installed name (e.g. `/alaa-cc-orchestrator`; `/plugin-name:skill-name` for plugin skills). In Codex, a `$name` mention can trigger, but the same placement rule applies: lead with it.
- One primary skill trigger per message. Skills the lanes must load are named inside lane dispatch text as instructions ("load `<name>` and apply it"), not as competing triggers at the top level.

## Role-consistency contract

A session holds exactly one role. The most common orchestration failure is a prompt that names an orchestrator skill but writes every imperative at the session as an implementer — the model obeys the dominant verbs, not the buried clause.

- If the prompt routes execution through `$alaa-codex-orchestrator` or `/alaa-cc-orchestrator`, the session role is **orchestrator/lead**, stated in the first sentences: plan lanes, dispatch, enforce the review gate, reconcile, run integrated validation, commit (when lanes must not). Add the explicit negative: "Do not write implementation code in this session."
- Every implementation verb (implement, edit, fix, test-first, refactor, document) moves into **lane rules** — a block the orchestrator copies into dispatches — never into the lead's own instructions.
- Verb-ownership audit before sending: read each imperative and assign it to lead or lane. A lane verb aimed at the lead, or a lead verb aimed at a lane, is a defect; rewrite it.

## Single-message forms, and the optional two-message split

Two single-message shapes both work; choose by whether you want the runtime's harness-enforced auto-continue.

**Trigger-led (deterministic activation, no harness loop).** The message leads with the exact skill trigger, assigns the role and lane rules, and closes with the completion condition + turn/time bound inline. The skill activates reliably because its trigger leads; the invoked skill's own drive (an orchestrator's plan -> dispatch -> review gate -> reconcile) carries the work to completion. Best when the skill is itself the completion engine and you do not need a per-turn harness check.

**`/goal`-led (harness auto-continue, implicit activation).** The message is a single `/goal` (Claude Code) or Codex Goal whose text is both the directive for the first turn and the completion condition the harness re-checks each turn — Claude Code's small fast evaluator model, Codex's durable Goal loop. Because `/goal` must lead the message, the skill it needs activates only *implicitly*, so open the condition by naming and describing that skill's role ("Acting as the `<name>` orchestrator, lead the lanes…") to make the description-match fire, then give the operating context, lane rules, a measurable end state, and a turn/time bound. Keep it within the runtime's limit (Claude Code caps `/goal` at 4,000 characters; Codex documents no fixed cap, but a bloated objective dulls both the directive and the completion check). Accept that implicit activation is model judgment, not a guaranteed trigger — that is the reliability cost of one message.

One further Claude Code constraint belongs in this decision: the `/goal` evaluator judges only what is already in the transcript. It runs no tools and reads no files. Write the condition as something the session's own output can demonstrate ("`npm test` exits 0", "`git status` is clean"), not as a state the evaluator would have to go and check.

**Two messages** are needed only to combine *both* deterministic activation *and* the harness auto-continue, since a leading skill trigger and a leading `/goal` cannot share one message: send the skill-triggering operating prompt first, then a compact `/goal` holding only the completion condition. Never inflate that compact `/goal` back into an operating manual.

## Satisfiable completion conditions

A completion condition must be reachable, or the harness loops until the turn cap. "Zero findings from a fresh adversarial pass" is the canonical unreachable condition: an adversarial reviewer with fresh context reliably finds new defensible items every pass. Bound convergence structurally instead: define DONE by severity threshold (zero open blocker/major findings; minors and nits reported, never looped), cap review-fix cycles explicitly (two is the orchestrator packs' default), make the final adversarial pass a reporting pass whose findings go to the user rather than into another cycle, and pay the full gate set once after the last fix with targeted checks per fix. Every goal-form prompt also carries an explicit turn or time cap as a safety net — the cap is the backstop, the structural bounds are the brake.

## Authorization polarity

**Match the polarity of your delegation language to the target model's default bias.** There is no longer one correct direction. A prompt that authorizes fan-out on a model that already over-delegates multiplies cost for nothing; a prompt that only restricts fan-out on a model that never delegates unprompted produces a single-threaded session that quietly does everything itself.

Where each family currently leans:

- **Claude Opus 5 — eager; cap it.** Anthropic's prompting guide states plainly that Opus 5 "delegates to subagents more readily than prior models," that delegation "multiplies cost and time when applied to small tasks," and that you should "give explicit guidance on which scenarios warrant delegation, or set deterministic caps on how many agents can be launched." Delegation language for Opus 5 is a ceiling, not a permission: delegate only for large, genuinely independent, parallelizable tracks; do not delegate work finishable in a handful of tool calls; prefer one subagent over several; keep spawn counts low.
- **Claude Fable 5 — eager, but the correction is shape rather than volume.** Fable 5 "dispatches parallel subagents more readily than prior models," and the guidance is to use subagents frequently while giving explicit criteria for when delegation is appropriate, and to prefer asynchronous orchestrator-to-subagent communication over blocking on each return. Do not add encouragement here; add selection criteria and non-blocking dispatch.
- **Claude Sonnet 5 — treat as neutral-to-eager, and verify.** The Sonnet 5 prompting guide does not address delegation directly. It does state that Sonnet 5 is more agentic than its predecessor and "will reach for tools and run self-verification loops more readily." Absence of a delegation note is not evidence of under-fan-out; measure on your own harness before writing polarity either way.
- **Codex / GPT-5.6 — reticent; authorize it.** The Codex docs are explicit that Codex "only spawns subagents when explicitly requested" and does not fan out on its own. This is the one family where the original positive-authorization wording remains exactly right: "spawn one lane per independent slice in the same turn, without asking" beats "parallel work is authorized only for independent lanes."

Two corroborating signals worth reading as evidence rather than as trivia. On the Claude Code side, the harness has grown caps in the direction of restraint — a default concurrent-subagent limit, a per-session spawn cap, a configurable workflow size guideline, and an advisory warning when a single workflow schedules an unusually large number of agents. Harnesses acquire brakes for models that accelerate. On the Codex side, subagent spawning stayed opt-in and explicit across the same period.

Two rules survive the polarity change unchanged:

- **Constraints belong in lane rules either way.** Disjoint scopes, a single writer per file, the shared validation command, the review gate — these are properties of the work partition, not of the delegation sentence. Putting them in the delegation sentence is what turns authorization into restriction and restriction into noise.
- **An invoked orchestrator skill's own fan-out policy wins.** When `$alaa-codex-orchestrator` or `/alaa-cc-orchestrator` is invoked, do not override its delegation stance from the calling prompt. Add or tighten lane rules instead.

One adjacent correction specific to the current Claude generation: delete carried-over verification scaffolding of the form "use a subagent to verify" or "add a final verification step." Opus 5 verifies its own work without being told, and those instructions cause over-verification. This applies only to redundant self-checks. A structurally independent reviewer that exists so no lane approves its own change is a governance boundary, not a quality patch — keep it. See `references/20-opus-5.md`.

## Pre-send checklist

1. The message opens with either the exact skill trigger (trigger-led form) or a `/goal` that names the needed skill's role (`/goal`-led form) — using the exact installed name for the executing surface, never a buried mid-paragraph trigger.
2. The session has one role, consistent with the invoked skill; implementation verbs live in lane rules.
3. Single message: either the trigger leads with the completion condition inline (deterministic activation, no harness loop), or one `/goal` opens by naming the needed skill's role (harness auto-continue, implicit activation) — both within the runtime's limit. Use two messages (operating prompt, then a compact separate `/goal`) only to get both at once.
4. Delegation wording matches the target model's default bias: a cap and selection criteria for Opus 5 and Fable 5, explicit positive authorization for Codex, measured rather than assumed for Sonnet 5. Restrictions on the *work partition* are expressed as lane constraints in every case.
5. Skills needed by lanes are named inside dispatch text, not as top-level triggers.
6. In Claude Code `/goal` form, the completion condition is demonstrable from the transcript and carries an explicit turn or time clause.

## The failure shape to recognize

Bad: a `/goal` block opening "You are the senior implementer…", with "then use `/alaa-cc-orchestrator` to lead the lanes" buried mid-paragraph. Result: the skill never loads and the session implements everything itself.
Fix, either single-message form: (a) trigger-led — start `/alaa-cc-orchestrator Orchestrator mode — <goal>`, assign the orchestrator role with the do-not-implement negative, put implementation discipline in lane rules, and state the completion condition + turn bound inline; or (b) `/goal`-led — start `/goal Acting as the <name> orchestrator, …` so the skill loads implicitly, with the same role, lane rules, and condition inline. Add a separate `/goal` only to layer the harness loop onto form (a).

The second failure shape, new this generation: a prompt lifted from an Opus 4.8-era pack that opens "spawn one lane per independent slice, without asking" and then runs on Opus 5 or Fable 5. Nothing errors. The session fans out across trivial slices, spends several times the tokens, and returns a correct answer at the wrong price. Polarity defects are silent — the verb-ownership audit will not catch them, so check polarity separately against the target model.

For durable multi-phase work that outgrows a single goal, route to `$alaa-workflow` / `/alaa-workflow` rather than lengthening the completion condition.

## Caveats

Verified against live documentation on 24 July 2026. Time-sensitive: the 4,000-character Claude Code `/goal` cap, the evaluator's transcript-only scope, and the Claude Code subagent and workflow caps cited as corroborating evidence are current values that move between releases — see `references/41-claude-code-runtime-features.md` for the figures and `references/11-codex-runtime-features.md` for the Codex side. The delegation-bias claims for Opus 5 and Fable 5 are quoted from Anthropic's per-model prompting guides; the Sonnet 5 position is marked unverified because the guide is silent on delegation, not because it was measured and found neutral. Re-check polarity on every model upgrade: this is the section most likely to invert again.

## Sources

- [Keep Claude working toward a goal (`/goal`)](https://code.claude.com/docs/en/goal)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Create custom subagents – Claude Code](https://code.claude.com/docs/en/sub-agents)
- [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Subagents – Codex](https://developers.openai.com/codex/subagents)
- [Follow a goal – Codex](https://developers.openai.com/codex/use-cases/follow-goals)
