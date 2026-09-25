---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates on its own work branch. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa CC Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system inside Claude Code. The session model leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

**One skill, two runtimes.** This pack and its counterpart for the other runtime are the same orchestrator with identical behaviour by design — same decisions, gates, triggers, and stopping conditions — so a behavioural rule added to one is added to the other in the same change. Only expression differs: each states its mechanics in its own runtime's idiom and carries the delegation polarity its own target model family needs, which `/alaa-prompting-guide` owns. Any other difference is drift.

## When NOT to use

- The change is a single edit whose correctness one reader can confirm without a second lane. Delegation
  then costs more than the work.
- The request is a destructive or externally visible action — a push, a deploy, a data change, a published
  artifact — and no explicit authorization for it exists yet.
- The runtime is Codex rather than Claude Code. The bootstrap here writes Claude Code agent files and
  does nothing useful there.
- The engagement is a multi-session program whose value is the plan and its continuity rather than one
  goal's parallel role lanes. `/alaa-workflow` leads there and invokes this skill for a
  single phase. This skill still writes its plan through that one; the question is only which of the two leads.

## 0. Inspect role availability

Activation grants no installation or update authority. Inspect the installed role definitions, version, and effective tool permissions without writing files. Compare the roles needed for this goal with the shipped definitions; report missing, stale, or unavailable roles before dispatch. Never silently substitute a model or a generic role. Continue only independent work whose required roles are available; report the rest blocked.

Install or update only with explicit user authorization for the target paths. Validate source pins, grants, and generated artifacts before the first target write. Run `python scripts/validate_pack.py` and `python scripts/check_agent_grants.py` before an authorized copy of the managed agent files. Do not change unrelated agents or settings.

Inspect the effective sandbox, parent overrides, and MCP grants before relying on isolation. A declared read-only role does not prove runtime enforcement. If effective permissions cannot be observed, report them unknown and keep operations within the role restriction.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The lead session plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available, and it does not run heavy test suites itself — the verifier does.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not edit repository files, and do not create workflow artifacts: the plan, critique, or review is the reply. Advisor mode creates a branch, a commit, or a plan file only when the user asks for one, because a request to think about the work is not authorization to change the tree.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

In orchestrator mode every goal writes its plan through `/alaa-workflow`, which owns plan files, resumable state, and phase prompt packs; this skill never recreates that machinery. When the engagement is a multi-session program rather than one goal, `/alaa-workflow` leads and invokes this skill for a single phase while keeping plan and state ownership. When one goal is the whole engagement, this skill leads and owns the plan it created there.

## 2. Lead-session contract

Read /alaa-prompting-guide for lead-session model and effort policy. Report configured/requested settings separately from observed identity; unobservable values stay unknown.

The lead owns goal normalization and scope control; repository-aware lane planning; agent selection and dispatch authorization; cross-lane reconciliation; verification and review gates; specialist-trigger decisions; and final truthfulness and stopping.

The lead must not: implement while implementation agents are viable; run CPU-heavy verification itself; silently implement a failed lane; let an implementer approve its own change; soften or omit reviewer findings; claim checks it did not observe; fan out overlapping write lanes concurrently; print bulky tool output into the conversation instead of routing it to a file and reporting the path; or run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

### Lead calibration

Four behaviors of the lead model need active counter-tuning. These are deliberate inversions of guidance that was correct for the previous generation, and getting them backwards is the most expensive mistake available in this pack.

**Delegate narrowly.** The lead delegates readily on its own and does not need encouragement to fan out. Dispatch one agent per lane and never several agents for the same lane. Do not delegate work the lead can finish in a handful of tool calls, and do not spawn duplicate summary-check lanes. Independent verification and review inspect the actual artifact under separate authority. Independent lanes still go out in the same turn — the constraint is on redundancy, not on parallelism.

**Do not add verification instructions.** The lead verifies its own work without being told, so instructions like "include a final verification step" or "re-check before responding" only burn tokens. The gates in this pack survive for a different reason and must not be confused with them: `alaa-verifier`, `alaa-reviewer`, and the specialists exist as **authority boundaries**, because no lane may approve its own change. That is a structural property of the pipeline, not a request for the model to check itself twice. Never skip a gate on the grounds that the work already looks verified.

**Correct sparingly.** Revise an earlier statement only when the error would change the user's code, conclusions, or decisions. State the correction plainly, briefly, and continue. For slips that change nothing, fix and move on without narrating.

**Calibrate length.** Reports and written deliverables run long by default. Match length to what the task needs: cover the substance, then stop. No filler sections, no redundant summaries, no boilerplate. Lead every report with the outcome — the first sentence answers "what happened" — and put supporting detail after it. Anything a later turn or another agent might need again is written to a file first and referenced by path; the conversation is not the storage medium, and `/alaa-low-noise` owns the budgets.

## 3. Intake and planning

Before any dispatch: inspect the repository's own guidance and the affected code paths; restate the outcome, the checkable acceptance criteria, the preserved behavior, and every irreversible action; then split the work into the smallest lanes with disjoint write scopes and serialize the ones that overlap. `references/verification-and-gates.md` owns the full intake list and what each lane definition must carry.

Before the first Phase A evidence dispatch, invoke `/alaa-memory-os` when its trigger list holds. The lead performs one bounded recall, verifies useful claims against repository truth, and passes only confirmed facts into lane context; active plan and handoff state stay in `/alaa-workflow`. When the unresolved question is itself about a prior session, decision, file, or shared contract, give the exact query to `alaa-researcher`, which owns that read-only memory lane. Independently invoke `/alaa-code-intelligence-routing` before choosing a code-evidence surface, then reuse the routed result rather than asking another surface for the same fact.

Every dispatch carries `/alaa-low-noise`: a child returns findings, verdicts, counts, and artifact paths, never transcripts, full diffs, or raw logs, and anything bulky is written to the permitted artifact directory and returned as a path. An unbounded child return is the most common way a lead's context is flooded, and the lead pays that cost on every remaining turn of the goal.

Every dispatched agent runs one bounded command per invocation and prints a line naming the step it is starting between them. A watchdog ends a lane on silence rather than on duration, so several commands chained into one long quiet invocation is the shape that loses the whole lane. A killed lane is resumed from its transcript, never restarted: its working tree survived the kill, so the transcript is the only record of which steps had already landed, and a restart repeats those while quietly losing the one that had not.

Read `references/routing-matrix.md` for specialist triggers and `references/delegation-prompts.md` for dispatch contracts. `references/verification-and-gates.md` owns gate economics — which gate runs before which, and what must be frozen before the expensive one is dispatched.

## 4. Model and role routing

Read `references/model-effort-policy.md` before selecting or deviating from a profile; it routes capability and pin policy to /alaa-prompting-guide. This pack owns role triggers in `references/routing-matrix.md` and authority/output contracts in `references/agent-catalog.md`.

Choose one correctness review profile for a scope. Both standard and deep review routes use the existing `alaa-reviewer`; record the deep-review trigger without creating a duplicate review lane.

Missing target models or roles are explicit blocked/degraded execution, never silent fallback. Diagnose missing context, tool failure, and specification ambiguity before attributing failure to model capacity. The catalog is a menu; dispatch only roles whose triggers hold.

## 5. Orchestrator execution pipeline

Phases A through E run in orchestrator mode; Phase F applies only to user-requested integration and requires explicit authorization before effects. Advisor mode runs none of them: Phases A, B, and F perform workspace setup, write files, and may perform explicitly authorized integration, which is exactly what section 1 forbids there. They are also the gate order; there is no second list. `references/verification-and-gates.md` owns what each phase does, its triggers, and what each gate requires — read it before dispatching Phase A.

| Phase | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, the profile | the plan and profile are recorded and presented |
| B — Implementation | one lane per disjoint write scope, focused-tier checks, a reviewable diff per completed subtask | every required lane is reconciled against its actual diff |
| C — Verification | one integrated affected-tier plan, executed by an authority that owns no lane | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | the independent review, plus every specialist whose trigger holds | findings are resolved or explicitly accepted by the user |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | the candidate has the proof required for the requested outcome |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

### Execution profile: size the pipeline to the plan

**Every profile preserves Phases A through E and their required gates.** Phase F is conditional on requested integration; local-only completion requires no merge prompt. The profile decides dispatch overhead, never whether an independent verification, review, or triggered specialist gate applies. What `lean` removes is dispatch overhead on a change that cannot justify it, where the cost lands on latency and the user's attention as much as on tokens. Choose the profile once, from the finished Phase A plan, and record it there. Escalate mid-run the moment a heavier profile's condition becomes true; never de-escalate, because the evidence that earned the heavier profile does not stop existing.

| Profile | Conditions — every one must hold | Shape |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions or deep-review triggers | Phases A–E, and F only when requested; the lead performs Phase D's review itself instead of dispatching `alaa-reviewer`, and specialists still fire on their own triggers |
| `standard` | anything that is neither `lean` nor `hardened` | Phases A–E with every required gate; F only when requested |
| `hardened` | the change meets the adversarial reviewer's blast-radius condition in `references/routing-matrix.md` | `standard`, plus the architecture critic in Phase A and the adversarial reviewer in Phase D |

`lean` drops the reviewer dispatch, never the review. The lead did not write the diff, so it remains an independent authority over it, which is what the gate exists to guarantee. The moment the diff leaves the lane plan, the profile becomes `standard` and `alaa-reviewer` is dispatched against the complete change.

**No profile suppresses a specialist.** The profile governs the reviewer dispatch and how much ceremony the phases carry; `references/routing-matrix.md` governs which specialists fire, identically at every profile. A one-lane retry change is still `lean` and still gets the observability reviewer. Any attempt to state which specialists a profile excludes would be a second copy of the trigger list, and the copy is what goes stale.

### Final report

Report in this order: the outcome, then the four completion-lifecycle states — `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` — each carrying its own verdict and none collapsed into another, with `alaa-workflow references/workspace-and-integration.md` owning what earns each state and this skill restating none of it; changes by lane and touched files; verification commands with observed results, each marked run or cited and carrying its tier; review and specialist verdicts with the resolution of each finding; documentation outcome with each touched document's grade; reusable-context curation outcome, including persisted, deferred, or empty; residual risks, skipped checks, and follow-ups; and the agent roster — every subagent dispatched this goal, one line each with agent name, configured/requested model and effort, separately observed runtime identity or unknown, flagging only observable mismatches, and for every escalated lane the named criterion that earned it.

Close with one run-accounting line: agents dispatched and how many distinct roles that was; checks run versus checks cited; and the branch span, from the plan's `Created` timestamp to the last authorized commit, or unavailable when no such commit exists. Every figure is already in hand — the roster, the evidence table, and the plan header plus Phase E's final git inspection — so the accounting costs no extra command and no bookkeeping. Never start a timer and never carry a clock across turns: a run that measures its own slowness by being slower has answered nothing. Call it the branch span rather than the duration, because it excludes planning before the first commit and every gate after the last. The three are diagnostic only together — dispatches well above distinct roles is fix-cycle churn, checks run well above checks cited is the repetition the tiers exist to prevent — and no budget is stated for any of them, because a threshold invented here would be enforced everywhere and grounded nowhere.

## 6. Advisor-mode output

Provide: grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; recommended agent, model, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Do not edit files or imply implementation occurred.

## 7. Verification and resource rules

Run `python scripts/check_agent_contracts.py` after instruction-contract changes and `python scripts/check_agent_contracts.py --self-test` after checker changes. Exit `0` is clean, `1` is findings, and `2` is unavailable proof; either nonzero blocks completion. These fixtures check source requirements, not live model behavior.


- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- After any change to `agents/`, the grant checker must pass before completion; `references/agent-catalog.md` states its exact invocation and exit-code contract.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- On the user's Windows environment, preserve every explicit `--browser chromium` argument. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes; do not start duplicate services when a reusable declared service exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

Read `references/resource-policy.md` for runner usage and ecosystem examples. Read `references/failure-taxonomy.md` when a check fails.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Installation and updates require explicit user authorization for named target paths; activation grants none.
- A lane's code-intelligence grant lives in its agent file, not in the dispatch. `references/agent-catalog.md` records which agents hold CodeGraph, the Serena read set, both, or neither; `/alaa-code-intelligence-routing` owns why. Reinstalling this pack restores those grants, so change them here rather than in `~/.claude/agents`.
- Commit only with explicit user authorization, on the run's work branch. Without it, preserve the reviewed diff and pin validation to a content snapshot under the workflow protocol. Installation, merge, push, tag, branch deletion, publication, deployment, and other external or destructive effects require their own explicit authorization. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, the final candidate passed the scope and proof levels required by repository policy and /alaa-testing-strategy, the final diff scope is clean, documentation was completed or explicitly skipped, the final reusable-context gate reported what was persisted, deferred, rejected, or absent, and any requested integration has an accurately reported authorized, declined, or blocked outcome. Local-only requests complete without an integration prompt.

Stop and report a partial or blocked state when: the same lane is blocked twice by the same cause; blocker or major findings remain after two fix cycles; verification remains flaky, timed out, contaminated, or environment-blocked; scope expands beyond the goal; an irreversible or product decision belongs to the user; or a safe execution path no longer exists.

## 10. Anti-patterns

Each of these inverts a default the lead would otherwise follow. Rules already stated above are not repeated here.

- spawning every specialist for every task, several agents for one lane, or a duplicate summary-check lane; independent artifact review is a required authority gate;
- delegating work the lead could finish in a handful of tool calls, or the lead implementing and running heavy suites while lanes are viable;
- treating the verifier and reviewer gates as redundancy and skipping them because the work already looks checked — they are authority boundaries;
- using a reviewer as a fixer, a verifier as a debugger, or a researcher as a decision-maker;
- running the full suite, the race detector, or the acceptance set again on a tree that has not changed since the last run — breadth is bought by a change in the tree, never by reaching a new phase or handing the work to a new agent;
- letting an implementation lane run the exhaustive tier on its own work, or running it before the final candidate exists;
- editing the product in response to a shell-parsing, container-runtime, permission, or stale-cache failure that was never classified;
- treating a rerun that passes after a failure as a clean pass;
- dispatching implementation before Phase A produced a written plan with the approach chosen and the alternatives rejected;
- dispatching the full reviewer and specialist set on a change whose plan meets the `lean` conditions, or staying in `lean` after the diff left the lane plan — `lean` removes dispatches, never phases;
- treating activation or phase completion as authority to install, commit, or merge;
- printing a diff, a log, or a file into the conversation instead of writing it to the artifact directory and reporting the path;
- deciding a document's size grade locally, or restating a rule this pack routes to its owner, instead of applying the owner's;
- escalating a lane's model because the goal is important or the surface is sensitive, rather than because the lane meets a named escalation criterion — importance and sensitivity are handled by gates, not tier;
- changing model or effort to mask tool failure, missing evidence, or an unresolved specification;
- routing the adversarial reviewer's findings into another fix cycle instead of reporting them;
- parallelizing migrations, generated contracts, or shared-state edits;
- instrumenting a run to explain its own cost, when the measurement costs more than the waste it would find;
- pre-loading every clean-code skill into every lane — name only the lane's matching skill.
