# Skill Invocation Placement and Prompt Composition

Trigger syntax alone does not activate a skill. A generated prompt fails silently when the trigger is buried mid-paragraph, the session role contradicts the skill's role, or a compact two-message `/goal` is bloated back into an operating manual. Apply every rule here before finalizing any prompt that must activate a skill.

## Mention vs invocation

- An **invocation** activates a skill: the trigger opens the message, or the prompt explicitly instructs "invoke the `<name>` skill now, before any other action."
- A **mention** is inert: a trigger in backticks mid-sentence ("then use `/name` to…") is a reference the model may ignore. Never rely on a mention when activation is required.
- In Claude Code, use the exact installed name (e.g. `/alaa-cc-orchestrator`). In Codex, a `$name` mention can trigger, but the same placement rule applies: lead with it.
- One primary skill trigger per message. Skills the lanes must load are named inside lane dispatch text as instructions ("load `<name>` and apply it"), not as competing triggers at the top level.

## Role-consistency contract

A session holds exactly one role. The most common orchestration failure is a prompt that names an orchestrator skill but writes every imperative at the session as an implementer — the model obeys the dominant verbs, not the buried clause.

- If the prompt routes execution through `$alaa-codex-orchestrator` or `$alaa-cc-orchestrator`, the session role is **orchestrator/lead**, stated in the first sentences: plan lanes, dispatch, enforce the review gate, reconcile, run integrated validation, commit (when lanes must not). Add the explicit negative: "Do not write implementation code in this session."
- Every implementation verb (implement, edit, fix, test-first, refactor, document) moves into **lane rules** — a block the orchestrator copies into dispatches — never into the lead's own instructions.
- Verb-ownership audit before sending: read each imperative and assign it to lead or lane. A lane verb aimed at the lead, or a lead verb aimed at a lane, is a defect; rewrite it.

## Single-message forms, and the optional two-message split

Two single-message shapes both work; choose by whether you want the runtime's harness-enforced auto-continue.

**Trigger-led (deterministic activation, no harness loop).** The message leads with the exact skill trigger, assigns the role and lane rules, and closes with the completion condition + turn/time bound inline. The skill activates reliably because its trigger leads; the invoked skill's own drive (an orchestrator's plan -> dispatch -> review gate -> reconcile) carries the work to completion. Best when the skill is itself the completion engine and you do not need a per-turn harness check.

**`/goal`-led (harness auto-continue, implicit activation).** The message is a single `/goal` (Claude Code) or Codex Goal whose text is both the directive for the first turn and the completion condition the harness re-checks each turn — Claude Code's small evaluator model, Codex's durable Goal loop. Because `/goal` must lead the message, the skill it needs activates only *implicitly*, so open the condition by naming and describing that skill's role ("Acting as the `<name>` orchestrator, lead the lanes…") to make the description-match fire, then give the operating context, lane rules, a measurable end state, and a turn/time bound. Keep it within the runtime's limit (Claude Code caps `/goal` at 4,000 characters; Codex has no fixed cap but a bloated objective dulls both the directive and the completion check). Accept that implicit activation is model judgment, not a guaranteed trigger — that is the reliability cost of one message.

**Two messages** are needed only to combine *both* deterministic activation *and* the harness auto-continue, since a leading skill trigger and a leading `/goal` cannot share one message: send the skill-triggering operating prompt first, then a compact `/goal` holding only the completion condition. Never inflate that compact `/goal` back into an operating manual.

## Satisfiable completion conditions

A completion condition must be reachable, or the harness loops until the turn cap. "Zero findings from a fresh adversarial pass" is the canonical unreachable condition: an adversarial reviewer with fresh context reliably finds new defensible items every pass. Bound convergence structurally instead: define DONE by severity threshold (zero open blocker/major findings; minors and nits reported, never looped), cap review-fix cycles explicitly (two is the orchestrator packs' default), make the final adversarial pass a reporting pass whose findings go to the user rather than into another cycle, and pay the full gate set once after the last fix with targeted checks per fix. Every goal-form prompt also carries an explicit turn or time cap as a safety net — the cap is the backstop, the structural bounds are the brake.

## Authorization polarity

Models in this pack under-fan-out by default. Delegation language must authorize, not merely restrict: "spawn one lane per independent slice in the same turn, without asking" beats "parallel work is authorized only for independent lanes." When an orchestrator skill is invoked, its own fan-out authorization applies — do not override it with restriction-only wording; add constraints (disjoint scopes, single writer per file) as lane rules instead.

## Pre-send checklist

1. The message opens with either the exact skill trigger (trigger-led form) or a `/goal` that names the needed skill's role (`/goal`-led form) — using the exact installed name for the executing surface, never a buried mid-paragraph trigger.
2. The session has one role, consistent with the invoked skill; implementation verbs live in lane rules.
3. Single message: either the trigger leads with the completion condition inline (deterministic activation, no harness loop), or one `/goal` opens by naming the needed skill's role (harness auto-continue, implicit activation) — both within the runtime's limit. Use two messages (operating prompt, then a compact separate `/goal`) only to get both at once.
4. Delegation wording is positive; restrictions are expressed as lane constraints.
5. Skills needed by lanes are named inside dispatch text, not as top-level triggers.

## The failure shape to recognize

Bad: a `/goal` block opening "You are the senior implementer…", with "then use `/alaa-cc-orchestrator` to lead the lanes" buried mid-paragraph. Result: the skill never loads and the session implements everything itself.
Fix, either single-message form: (a) trigger-led — start `/alaa-cc-orchestrator Orchestrator mode — <goal>`, assign the orchestrator role with the do-not-implement negative, put implementation discipline in lane rules, and state the completion condition + turn bound inline; or (b) `/goal`-led — start `/goal Acting as the <name> orchestrator, …` so the skill loads implicitly, with the same role, lane rules, and condition inline. Add a separate `/goal` only to layer the harness loop onto form (a).
