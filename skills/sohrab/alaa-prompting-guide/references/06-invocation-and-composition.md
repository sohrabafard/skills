# Skill Invocation Placement and Prompt Composition

Trigger syntax alone does not activate a skill. A generated prompt fails silently when the trigger is buried, the session role contradicts the skill's role, or the operating instructions are stuffed into a goal condition. Apply every rule here before finalizing any prompt that must activate a skill.

## Mention vs invocation

- An **invocation** activates a skill: the trigger opens the message, or the prompt explicitly instructs "invoke the `<name>` skill now, before any other action."
- A **mention** is inert: a trigger in backticks mid-sentence ("then use `/name` to…") is a reference the model may ignore. Never rely on a mention when activation is required.
- In Claude Code, use the exact installed name — plugin skills are namespaced (`/sohrab-skills:alaa-cc-orchestrator`, not `/alaa-cc-orchestrator`). In Codex, a `$name` mention can trigger, but the same placement rule applies: lead with it.
- One primary skill trigger per message. Skills the lanes must load are named inside lane dispatch text as instructions ("load `<name>` and apply it"), not as competing triggers at the top level.

## Role-consistency contract

A session holds exactly one role. The most common orchestration failure is a prompt that names an orchestrator skill but writes every imperative at the session as an implementer — the model obeys the dominant verbs, not the buried clause.

- If the prompt routes execution through `$alaa-codex-orchestrator` or `$alaa-cc-orchestrator`, the session role is **orchestrator/lead**, stated in the first sentences: plan lanes, dispatch, enforce the review gate, reconcile, run integrated validation, commit (when lanes must not). Add the explicit negative: "Do not write implementation code in this session."
- Every implementation verb (implement, edit, fix, test-first, refactor, document) moves into **lane rules** — a block the orchestrator copies into dispatches — never into the lead's own instructions.
- Verb-ownership audit before sending: read each imperative and assign it to lead or lane. A lane verb aimed at the lead, or a lead verb aimed at a lane, is a defect; rewrite it.

## Goal-condition splitting

`/goal` (in both runtimes, with their different mechanisms) carries a **completion condition**, not an operating manual.

- Keep the `/goal` text to a few sentences: the verifiable end state, the evidence that proves it, and an explicit turn or time bound. Claude Code's condition is judged by a small evaluator model from the transcript; a 3,000-character condition degrades both the evaluator and the directive.
- The operating prompt — role, intake, lane rules, gates, safety — is a separate normal message sent first, and that message is where the skill trigger lives.
- Never place a skill trigger inside `/goal` text expecting activation.

## Authorization polarity

Models in this pack under-fan-out by default. Delegation language must authorize, not merely restrict: "spawn one lane per independent slice in the same turn, without asking" beats "parallel work is authorized only for independent lanes." When an orchestrator skill is invoked, its own fan-out authorization applies — do not override it with restriction-only wording; add constraints (disjoint scopes, single writer per file) as lane rules instead.

## Pre-send checklist

1. Trigger opens the message and uses the exact installed name for the executing surface.
2. The session has one role, consistent with the invoked skill; implementation verbs live in lane rules.
3. `/goal`, if used, is a compact condition with a bound, sent separately from the operating prompt.
4. Delegation wording is positive; restrictions are expressed as lane constraints.
5. Skills needed by lanes are named inside dispatch text, not as top-level triggers.

## The failure shape to recognize

Bad: a `/goal` block opening "You are the senior implementer…", with "then use `/alaa-cc-orchestrator` to lead the lanes" buried mid-paragraph. Result: the skill never loads and the session implements everything itself.
Fix: message starts `/sohrab-skills:alaa-cc-orchestrator Orchestrator mode — <goal>`, second sentence assigns the orchestrator role with the do-not-implement negative, lane rules carry the implementation discipline, and a separate short `/goal` holds the completion condition.
