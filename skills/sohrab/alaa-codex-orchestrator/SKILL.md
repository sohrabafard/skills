---
name: alaa-codex-orchestrator
description: "Multi-model orchestrator/advisor mode for Codex (GPT-5.6). Use when the user states a goal and wants the Sol main thread to lead: either orchestrator mode (plan, dispatch role subagents — Terra implementers with Sol escalation, a Sol reviewer, a Luna documenter — enforce a review gate, reconcile evidence) or advisor mode (plan, produce lane prompts, and review without delegating). Trigger with $alaa-codex-orchestrator plus a goal, or whenever a Codex request names advisor or orchestrator mode. Do not use for trivial single-file edits or for Windows runtime failures (route those to $alaa-codex-runtime-ops)."
---

# Alaa Codex Orchestrator

Turn one written goal into role-separated, multi-model execution inside Codex: Sol leads, Terra role agents implement, review, and document, and nothing is reported as done without evidence.

## Requirements

- Main thread model: `gpt-5.6-sol`, reasoning effort `high`. If the session runs on another model, tell the user before proceeding.
- Role agents: definitions ship in this skill's `agents/` folder, but Codex discovers agents only in `.codex/agents/` (project) or `~/.codex/agents/` (personal) — a TOML inside the skill folder is invisible to the spawner. On activation, check whether the four role agents are available; if not, copy `agents/*.toml` from this skill's directory into `~/.codex/agents/` (or `.codex/agents/` when the user wants a repo-scoped override) before dispatching. If a freshly copied agent is not visible in this session, tell the user to restart the Codex session once; hot reload is not guaranteed. Roles and pins: `alaa-implementer` (`gpt-5.6-terra`, `high`), `alaa-implementer-sol` (`gpt-5.6-sol`, `high`, escalation lanes), `alaa-reviewer` (`gpt-5.6-sol`, `high`, read-only), `alaa-documenter` (`gpt-5.6-luna`, `high`).
- If the role TOMLs are not installed, say so, then fall back to built-in `worker` (implement) and `explorer` (read) agents using the same lane prompts from `references/delegation-prompts.md`. Note to the user that fallback agents inherit the Sol model and cost more.
- Optional: raise `[agents] max_threads` in `~/.codex/config.toml` when goals routinely need more than 6 parallel lanes.

## Mode resolution

- If the request says advise, advisor, consult, "don't implement", or asks only for direction or critique: advisor mode.
- If the request states a goal to build, fix, refactor, or migrate: orchestrator mode.
- If genuinely ambiguous, ask exactly one question offering the two modes, then proceed.

## Shared intake (both modes)

1. Restate the goal as: outcome, success criteria (checkable), constraints, out-of-scope.
2. Detect lane languages and map each lane to its clean-code skill: PHP/Laravel → `$alaa-php-clean-code`; Vue/Quasar/TypeScript → `$alaa-vue-typescript-clean-code`; Go → `$alaa-golang-clean-code-principles`. Documentation lanes in Ala-style repos → `$alaa-docs-farsi`.
3. Split the goal into independent lanes with disjoint file sets. Each lane gets: scope (files/modules), acceptance criteria, verification commands, and its clean-code skill. A goal too small to split becomes one lane.
4. If lanes cannot be made disjoint, serialize the overlapping lanes instead of parallelizing them.

## Orchestrator mode

1. Present the lane plan in one compact block, then continue without waiting unless the goal is destructive, externally visible, or ambiguous in scope.
2. Dispatch with explicit authorization — Codex never fans out on its own. Include this in the dispatch turn:

```text
Explicit authorization: spawn subagents and run independent lanes in parallel for this task without asking again.
Spawn one alaa-implementer per lane, give every lane the same constraints and a clearly scoped slice so nothing
is duplicated or dropped, wait for all of them, and reconcile the results yourself before moving on.
```

3. Build each lane prompt from `references/delegation-prompts.md` (implementer template). One lane, one implementer, one prompt. Dispatch an architecture-heavy or unusually subtle lane to `alaa-implementer-sol`; every other lane uses `alaa-implementer`.
4. Wait for all lanes. Reconcile: check lane outputs against acceptance criteria, detect cross-lane conflicts, and rerun the affected lane if two lanes touched the same behavior.
5. Review gate: spawn `alaa-reviewer` with the reviewer template covering the full change set against the lane plan. The reviewer is fresh-context and read-only.
   - `VERDICT: APPROVED` or `APPROVED-WITH-NITS` → proceed. Report nits to the user; fix them only if trivial and in scope.
   - `VERDICT: CHANGES-REQUESTED` → route blocker and major findings back to the owning implementer lanes with the fix template. Maximum two fix cycles; after the second, stop and report unresolved findings to the user with options.
6. Documentation lane: after the gate passes, spawn `alaa-documenter` only when the change alters behavior, APIs, configuration, or operations. Skip it explicitly otherwise and say so. The documenter runs on Luna: during reconciliation, spot-check its output against the change summary — accuracy, coverage of behavior/API/config changes, and links. If it falls short, send one correction dispatch with the concrete fixes; if it fails again, report it and recommend raising the documenter pin to Terra.
7. Final report, in order: verdict; what changed (per lane, touched files); verification evidence (commands and observed results); reviewer verdict and how findings were resolved; residual risks and follow-ups. Never claim success for anything that was not verified in this session.

## Advisor mode

1. Deliver: the lane plan; a ready-to-run implementer prompt per lane (from the templates) that the user can paste or hand to any worker; the top risks and the assumptions that would change the plan.
2. Do not spawn implementers or edit code. Spawning `alaa-reviewer` is allowed when the user asks for a review of work they implemented themselves; return the reviewer output with findings first, and make no fixes.
3. When the user asks "should I…" questions mid-goal, answer with a recommendation plus the strongest counter-argument, grounded in files actually inspected.

## Long-horizon goals

For a goal that will outlive this thread (multi-hour, many checkpoints), offer Codex `/goal` (requires `features.goals = true`):

```text
/goal <desired end state> verified by <specific command, test, or artifact>, while preserving <what must not regress>.
Use only <allowed files, tools, or boundaries>. Between iterations, <how to pick the next action>.
If blocked or no valid path remains, report exactly what is blocking progress and what would unblock it.
```

The lane plan from intake becomes the goal's iteration policy. Orchestrator dispatch rules above still apply inside each turn.

## Safety

- Never run destructive or externally visible actions (force push, history rewrite, deletion of data, deploys, publishing) without explicit user confirmation, in any mode or lane.
- Implementer lanes may edit only inside their declared scope. Reviewer is read-only. Documenter edits documentation files only.
- Commit only when the user asked for commits; commit messages carry no Co-Authored tag.
- A failed or incomplete lane is reported as failed. Do not silently re-implement it in the main thread; either rerun the lane or ask.

## Stop rules

- Stop when every acceptance criterion has verification evidence and the review gate passed.
- Stop and report when: a lane is blocked twice on the same cause; the review gate fails after two fix cycles; scope grows beyond the stated goal; or a required decision belongs to the user.

## Anti-patterns

- Doing lane implementation in the Sol main thread while orchestrator mode is active — Sol plans, dispatches, reconciles, and judges.
- Spawning a subagent for work the main thread can finish directly in advisor mode answers.
- Letting the reviewer fix code, or letting an implementer review its own lane.
- Reporting "done" from lane summaries without checking evidence, or paraphrasing reviewer findings into something softer.
- Merging this skill's job with durable multi-phase plan/state machinery — for that engagement shape, use the alaa-workflow process instead of recreating it here.

## Validation checklist (before the final report)

1. Every lane has evidence: commands run and observed results, not intentions.
2. Reviewer verdict is quoted, not summarized away; all blocker/major findings are resolved or explicitly open.
3. Touched files match declared lane scopes.
4. Docs lane ran or was explicitly skipped with a reason.
5. The final report opens with the outcome in one sentence.
