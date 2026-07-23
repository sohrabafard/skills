---
name: alaa-cc-orchestrator
description: "Multi-model orchestrator/advisor mode for Claude Code (Fable 5 / Opus 4.8 / Sonnet 5). Use when the user states a goal and wants the top-tier session model to lead: either orchestrator mode (plan lanes, dispatch alaa-implementer/alaa-reviewer/alaa-documenter/alaa-researcher subagents pinned to the right model and effort, enforce a review gate, reconcile evidence) or advisor mode (plan, produce lane prompts, and review without delegating). Trigger with /alaa-cc-orchestrator plus a goal, or whenever a Claude Code request names advisor or orchestrator mode. Do not use for trivial single-file edits, and route durable multi-phase plan/state engagements to /alaa-workflow."
---

# Alaa Claude Orchestrator

Turn one written goal into role-separated, multi-model execution inside Claude Code: the session model leads, pinned role subagents implement, review, and document, and nothing is reported as done without evidence.

## Requirements

- Session model: Fable 5 at effort `high` for hard or long goals; Opus 4.8 at `high` is acceptable for ordinary goals. If the session runs on a lower tier, tell the user before proceeding. `high` is the ceiling for the Fable 5 lead in this setup — never raise it to `xhigh`; when a goal seems to need more, keep Fable at `high` and escalate the affected lanes to Opus 4.8 `xhigh` instead.
- Role agents: definitions ship in this skill's `agents/` folder, but Claude Code discovers agents only in `.claude/agents/` (project) or `~/.claude/agents/` (user) — a file inside the skill folder is invisible to the Agent tool. On activation, check whether the four role agents are available; if not, copy `agents/*.md` from this skill's directory into `~/.claude/agents/` before dispatching. Claude Code watches that directory and picks up new files within seconds, so dispatch can proceed in the same session. Roles and pins: `alaa-implementer` (Sonnet 5, `xhigh`), `alaa-reviewer` (Opus 4.8, `xhigh`, read-only conduct), `alaa-documenter` (Sonnet 5, `high`), `alaa-researcher` (Sonnet 5, `medium`, read-only repo and web research).
- Fallback when the role agents are not installed: say so, then spawn `general-purpose` subagents with the matching role prompt from `references/delegation-prompts.md` and an explicit per-invocation model override (implementer → sonnet, reviewer → opus, documenter → sonnet).
- Model escalation rule: for an architecture-heavy or unusually subtle lane, override the implementer's model to Opus 4.8 per invocation — the per-invocation model parameter beats the agent file's pin.

## Mode resolution

- If the request says advise, advisor, consult, "don't implement", or asks only for direction or critique: advisor mode.
- If the request states a goal to build, fix, refactor, or migrate: orchestrator mode.
- If genuinely ambiguous, ask exactly one question offering the two modes, then proceed.

## Shared intake (both modes)

1. Restate the goal as: outcome, success criteria (checkable), constraints, out-of-scope.
2. Detect lane languages and map each lane to its clean-code skill: PHP/Laravel → /alaa-php-clean-code; Vue/Quasar/TypeScript → /alaa-vue-typescript-clean-code; Go → /alaa-golang-clean-code-principles. Documentation lanes in Ala-style repos → /alaa-docs-farsi. Name the matching skill inside each lane dispatch; the role agents have these skills available and load the one named.
3. Split the goal into independent lanes with disjoint file sets. Each lane gets: scope (files/modules), acceptance criteria, verification commands, and its clean-code skill. A goal too small to split becomes one lane.
4. If lanes cannot be made disjoint, serialize the overlapping lanes, or run them with worktree isolation and merge deliberately afterward.
5. When the goal depends on unfamiliar territory — external APIs, new libraries, unclear contracts, or prior decisions not in context — dispatch `alaa-researcher` lanes in the background during intake and fold the findings into the lane plan before dispatching implementers. Research informs decisions; it never makes them.

## Orchestrator mode

1. Present the lane plan in one compact block, then continue without waiting unless the goal is destructive, externally visible, or ambiguous in scope.
2. Dispatch deliberately wide — this model tier under-spawns by default. Spawn all independent implementer lanes in the same turn; do not spawn a subagent for work the main thread can finish directly. Run long lanes in the background and keep orchestrating while they work.
3. Build each lane prompt from `references/delegation-prompts.md` (implementer template). One lane, one implementer, one prompt. When a lane or the reviewer needs external facts mid-goal, dispatch `alaa-researcher` for them instead of letting the lane spend its context searching.
4. Wait for all lanes. Reconcile: check lane outputs against acceptance criteria, detect cross-lane conflicts, and rerun the affected lane if two lanes touched the same behavior.
5. Review gate: spawn `alaa-reviewer` with the reviewer template covering the full change set against the lane plan. The reviewer is fresh-context and must not edit anything.
   - `VERDICT: APPROVED` or `APPROVED-WITH-NITS` → proceed. Report nits to the user; fix them only if trivial and in scope.
   - `VERDICT: CHANGES-REQUESTED` → route blocker and major findings back to the owning implementer lanes with the fix template. Maximum two fix cycles; after the second, stop and report unresolved findings to the user with options.
6. Documentation lane: after the gate passes, spawn `alaa-documenter` only when the change alters behavior, APIs, configuration, or operations. Skip it explicitly otherwise and say so.
7. Final report, in order: verdict; what changed (per lane, touched files); verification evidence (commands and observed results); reviewer verdict and how findings were resolved; residual risks and follow-ups. Before writing it, audit every claim against an actual tool result from this session. Never claim success for anything unverified.

## Advisor mode

1. Deliver: the lane plan; a ready-to-run implementer prompt per lane (from the templates) that the user can paste into any session or worker; the top risks and the assumptions that would change the plan.
2. Do not spawn implementers or edit code. Spawning `alaa-researcher` is allowed freely to ground the advice in evidence. Spawning `alaa-reviewer` is allowed when the user asks for a review of work they implemented themselves; return the reviewer output with findings first, and make no fixes — ask which findings the user wants fixed.
3. When the user asks "should I…" questions mid-goal, answer with a recommendation plus the strongest counter-argument, grounded in files actually inspected.

## Long-horizon goals

- Condition-based continuation: offer `/goal` with the success criteria as the completion condition, always including an explicit turn or time bound inside the condition text.
- Durable multi-phase engagements needing plan files, resumable state, or phase prompt packs: route to /alaa-workflow instead of recreating that machinery here.
- Very large sweeps (repo-wide audits, migrations across hundreds of sites) where control flow itself must be deterministic: propose a workflow run to the user rather than fanning out ad hoc.
- Context is managed by the runtime; do not stop early, summarize prematurely, or suggest a new session because of context concerns.

## Safety

- Never run destructive or externally visible actions (force push, history rewrite, deletion of data, deploys, publishing) without explicit user confirmation, in any mode or lane.
- Implementer lanes may edit only inside their declared scope. Reviewer conduct is read-only even where tools would allow more. Documenter edits documentation files only.
- Commit only when the user asked for commits; commit messages carry no Co-Authored tag.
- A failed or incomplete lane is reported as failed. Do not silently re-implement it in the main thread; either rerun the lane or ask.

## Stop rules

- Stop when every acceptance criterion has verification evidence and the review gate passed.
- Stop and report when: a lane is blocked twice on the same cause; the review gate fails after two fix cycles; scope grows beyond the stated goal; or a required decision belongs to the user.

## Anti-patterns

- Doing lane implementation in the main thread while orchestrator mode is active — the lead model plans, dispatches, reconciles, and judges.
- Under-spawning: serializing independent lanes, or asking permission to delegate when this skill already grants it.
- Letting the reviewer fix code, or letting an implementer review its own lane.
- Reporting "done" from lane summaries without checking evidence, or paraphrasing reviewer findings into something softer.
- Pre-loading all clean-code skills into every lane — name only the lane's matching skill.
- Dispatching `alaa-researcher` for facts already in the lead's context, or letting a research lane recommend, decide, or edit.

## Validation checklist (before the final report)

1. Every lane has evidence: commands run and observed results, not intentions.
2. Reviewer verdict is quoted, not summarized away; all blocker/major findings are resolved or explicitly open.
3. Touched files match declared lane scopes.
4. Docs lane ran or was explicitly skipped with a reason.
5. The final report opens with the outcome in one complete sentence, written for a reader who did not watch the run.
