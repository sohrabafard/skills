---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates in the workflow-selected checkout. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa CC Orchestrator

Lead a controlled, evidence-driven multi-agent goal inside Claude Code. Narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

**Mirrored behavior.** Change both runtime orchestrators together. Only runtime mechanics and model-family delegation polarity may differ; `/alaa-prompting-guide` owns the latter.

## Admission

Before role inspection or planning, route a single bounded edit whose correctness one reader can confirm to direct execution under its domain owner. Do not start this pipeline for it. Required repository checks still apply.

## Plan and allocation

1. Before planning, apply the Mandatory Ponytail binding in `alaa-workflow references/companion-routing.md`, including its user opt-out. Then apply Planning profile selection and All-role task allocation in `references/routing-matrix.md`.
2. Plan, then finalize and consolidate tasks and dependencies.
3. Allocate the batch once. Record each managed profile or admitted external role and its selection reason in the plan, then dispatch.

Planning effort never sets worker effort. Worker selection alone needs no planner dispatch.

## When NOT to use

- A single edit one reader can confirm without a second lane; delegation costs more than the work.
- A destructive or external effect, including push, deploy, data change or publication, lacks explicit authorization.
- The runtime is Codex rather than Claude Code. These agent files do not serve it.
- A multi-session program centers on plan continuity: `/alaa-workflow` leads and invokes this skill for a phase. This skill still writes its plan through workflow.

## 0. Inspect role availability

1. The separate companion /alaa-testing-strategy is required for test design, test execution, and legacy runner forwarding. If it is unavailable, report the missing owner and block dependent work. Never auto-install it.
2. Activation grants no installation or update authority. Inspect installed definitions, the version and effective tools without writes. Compare the required managed roles with the shipped definitions. For a required external companion, apply its admission in `references/agent-catalog.md`.
3. Report missing, stale or unavailable roles before dispatch. Never silently substitute a model or a generic role. Continue only the independent work whose required roles are available, and report the rest as blocked.
4. Before relying on isolation, inspect the effective sandbox, parent overrides and MCP grants. A read-only declaration proves no enforcement. Report unobservable permissions as unknown, and operate within role restrictions.

Install or update only with explicit user authorization for the target paths. Validate model-neutral source roles, grants, and generated artifacts before the first target write. Run `python3 scripts/validate_pack.py` and `python3 scripts/check_agent_grants.py` before an authorized copy of the managed agent files. Do not change unrelated agents or settings.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The lead plans, dispatches, reconciles, gates and reports. It implements only a mechanical local edit with known scope, no design decision, and a few tool calls, in files no active or pending lane owns, because dispatching such an edit costs more than making it. Viable implementers own all other implementation. The verifier runs heavy suites.

### Advisor mode

For native Claude Code Advisor consultation during execution, use the separate route in `references/model-effort-policy.md`.

For plans, critiques, architecture advice, prompts, lane definitions or review without implementation, you may spawn research or read-only specialists. Do not implement product changes. Before deciding whether to save a plan, read `alaa-workflow references/artifact-lifecycle.md` for admission and explicit exceptions. Plan-only work grants no product execution, branch, or commit authority.

Follow explicit wording. Otherwise choose the lowest-side-effect interpretation that answers the request. Do not ask merely to select a mode.

In orchestrator mode, adopt an existing parent plan. `/alaa-workflow` owns plan, checkpoint and prompts. This skill leads one goal. Workflow leads multi-session programs and invokes it per phase.

## 2. Lead-session contract

Use `references/routing-matrix.md` for the actual lead-session task selection and /alaa-prompting-guide for current capabilities and control mechanics. Report configured and requested settings separately from observed identity. Unobservable values stay unknown.

The lead owns goal normalization, scope control, repository-aware lanes, selection and dispatch authority, reconciliation, verification and review, specialist triggers, truthful reporting and stopping.

The lead must not implement beyond that mechanical-edit exception, run heavy verification, silently take over failed lanes, permit self-approval, soften or omit review findings, claim unobserved checks or overlap writers. Save bulky output and report its path.

### Dispatch discipline

**One agent per lane.** Dispatch no duplicate lane and no summary-check agent. A lane starts no subagent of its own: the lead owns every dispatch and its task allocation. Independent verification and review inspect the actual artifact under separate authority. Dispatch independent lanes together. Keep inspection and Orchestrator mode's mechanical edit inline.

**Start a dependent lane as soon as the lanes it consumes finish.** Join lanes behind one barrier only when the next step consumes all of their outputs. A barrier over a lane whose output the next step never reads idles that step for the unrelated lane's whole runtime.

**Keep dispatches lean.** Apply /alaa-prompting-guide. Carry lane facts only: outcome, owned files, exclusions, acceptance, commands, dependencies, resolved skills and return contract. Do not restate the native role definition, which dilutes both contracts. State each instruction once. Expose task-relevant tools and only requirement-bearing examples.

**Preserve proportional verification.** Read `references/verification-and-gates.md` for gate economics and independent acceptance. /alaa-prompting-guide owns model-specific verification wording.

**Correct sparingly.** Revise a statement only when its error changes user code, conclusions or decisions. State the correction plainly and briefly, then continue. Fix immaterial slips without narration.

**Calibrate length.** Cover required substance, then stop without filler, redundant summaries or boilerplate. Start with the outcome and supporting detail. Save reusable material before reporting its path. Conversation is not storage. /alaa-low-noise owns budgets.

## 3. Intake and planning

Before designing implementation or verification, load /alaa-testing-strategy. Before dispatch, inspect guidance and affected paths. Settle outcome, acceptance, preserved behavior and irreversible actions. Draw disjoint lanes. `references/verification-and-gates.md` owns intake, lane fields and infrastructure reuse.

Before Stage A evidence dispatch, apply `/alaa-memory-os` when its trigger holds: make one bounded recall, verify useful claims in repository truth, and keep active state in workflow. Route unresolved prior-session, ownership and shared-contract questions to `alaa-researcher`. `alaa-explorer` uses memory only when the repository cannot answer. Apply `/alaa-code-intelligence-routing` before code-evidence selection and reuse its result.

Every dispatch carries `/alaa-low-noise`. Every return carries findings, verdicts, counts and permitted artifact paths, never transcripts, full diffs or logs. Persist reusable context before returning its path. Use bounded invocations and the progress reporting the host requires. Do not infer a universal watchdog timeout or a need for per-command narration. After an interruption, reconcile the transcript, the checkpoint and the surviving files before resuming writes.

`references/verification-and-gates.md` owns gate ordering and freezing before expensive dispatch.

## 4. Model and role routing

For EVERY dispatch, apply the model AND effort allocation and the role triggers in `references/routing-matrix.md`. Before explicit dispatch, normalize omitted controls through `references/model-effort-policy.md`. `references/agent-catalog.md` owns role authority and output.

Choose one correctness review profile for a scope. Both standard and deep review routes use the existing `alaa-reviewer`. Record the deep-review trigger without creating a duplicate review lane.

Report a missing model or role as blocked or degraded; never fall back silently. Diagnose context, tool and specification failures before you attribute a shortfall to capacity. Dispatch only catalog roles whose trigger holds.

## 5. Orchestrator execution pipeline

Orchestrator mode keeps every Stage A–E outcome. Stage F needs requested integration, and explicit authority before its effects. Advisor mode runs no execution stage; section 1 routes its planning artifacts. Stages are logical outcomes, not workflow phases or separate mandatory dispatches. Coalesce compatible actions and evidence in the workflow plan while preserving outcomes, independence and gate economics. Before Stage A dispatch, read `references/verification-and-gates.md` for the inherited phase and final review boundary, cadence, triggers and requirements.

| Stage | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, the profile | the plan and profile are recorded and presented |
| B — Implementation | disjoint lanes, focused subtask checks and bounded task acceptance, with tested diff evidence | every required lane is reconciled against its actual diff |
| C — Verification | focused phase evidence and required pre-review checks under their assigned observers | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | at the declared boundary, independent review and every triggered specialist | required assessments are complete and findings are resolved or explicitly accepted by the user |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | applicable documentation is validated; whole-engagement final gates wait for its final candidate |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

### Execution profile: size the pipeline to the plan

**Every profile preserves A–E outcomes and required gates at the inherited review boundary.** Record the profile from the finished plan. Escalate to a heavier profile when its condition appears. Do not de-escalate while qualifying evidence persists. `references/routing-matrix.md` owns implementation-role reassessment.

| Profile | Conditions — every one must hold | Shape |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions or deep-review triggers | Stages A–E, and F only when requested; the lead performs Stage D's review itself instead of dispatching `alaa-reviewer`, and specialists still fire on their own triggers |
| `standard` | anything that is neither `lean` nor `hardened` | Stages A–E with every required gate; F only when requested |
| `hardened` | the change meets the adversarial reviewer's blast-radius condition in `references/routing-matrix.md` | `standard`, plus the architecture design record in Stage A and critic/adversarial judgment at the declared review boundary |

`lean` review is independent because the lead authored no diff. If the work leaves the lane plan, or the lead made a mechanical edit, select `standard` and dispatch `alaa-reviewer` on the complete change.

**No profile suppresses a specialist.** Apply only `references/routing-matrix.md` triggers, identically across profiles.

### Final report

Report outcome; independent lifecycle verdicts (`IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED`) under `alaa-workflow references/workspace-and-integration.md`; lane changes and files; commands and results, marked run or cited, with tier; review and specialist verdicts and dispositions; each touched document's outcome and grade; curation as persisted, deferred or empty; risks, skipped checks, follow-ups. List each dispatched agent once with its configured and requested pair, separately observed identity or unknown, observable mismatches, and the exceptional-model admission for each escalated dispatch.

Write the report for a reader who saw no tool call and no lane report. Put the outcome first, use full sentences, and define any lane label or abbreviation the run invented.

Close with one line from the existing plan, roster and evidence: dispatches and distinct roles; underlying checks run or cited, covered children counted once; span from plan `Created` to last authorized commit, or unavailable. Use no timer, extra command or invented budget.

## 6. Advisor-mode output

Provide: grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; recommended agent, model, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Apply section 1's artifact admission. When a plan is admitted, report the canonical plan address and recovery reference. Otherwise deliver the plan in the reply. Do not imply implementation occurred.

When generating a goal condition, read `alaa-prompting-guide references/06-invocation-and-composition.md`; it owns condition syntax and the skill-led kickoff.

## 7. Verification and resource rules

Before planning or executing checks, load /alaa-testing-strategy. Read its `references/100-test-execution.md` for execution, `references/110-execution-resources.md` for resources and timing, or `references/120-result-classification.md` for result classification and diagnosis. The router below retains legacy loading paths.

Schedule these pack checks through `references/verification-and-gates.md` Gate economics. Proven aggregate coverage discharges only identical child invocations with the same scope and observer.

- After instruction-contract changes, run `python3 scripts/check_agent_contracts.py`. It checks source requirements, not live model behavior.
- After changing agent instructions, a contract asset, pins, agents, or version, run `python3 scripts/render_agents.py --write`, then `python3 scripts/render_agents.py --check` and `python3 scripts/validate_pack.py`. Review the generated wrappers against `assets/implementation-contract.md` and `assets/planner-contract.md`.

For each command above, exit `0` is clean, `1` is findings or drift, and `2` means unavailable proof. Either nonzero exit blocks completion.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Installation and updates require explicit user authorization for named target paths; activation grants none.
- Agent files own code-intelligence grants; dispatches do not. `references/agent-catalog.md` assigns each role its CodeGraph and Serena grants. `/alaa-code-intelligence-routing` owns the rationale. Change grants in this pack, not in `~/.claude/agents`, because a reinstall restores the pack grants.
- Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. Do not wait for boundary review or request an already-granted permission again. Every external or destructive effect needs its own explicit authority. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when all of these hold:

- acceptance is evidenced;
- mandatory gates pass, and the final candidate's scope and proof satisfy repository policy and /alaa-testing-strategy;
- the final diff scope is clean;
- documentation is completed or explicitly skipped;
- the final reusable-context gate reports its disposition: persisted, deferred, rejected or absent.

Report requested integration accurately as authorized, declined or blocked. Local-only completion needs no integration prompt.

Stop and report partial or blocked status when any of these occurs:

- the same lane or cause blocks twice;
- blockers or majors survive two fix cycles;
- verification stays flaky, timed out, contaminated or environment-blocked;
- the work needs scope beyond the goal;
- an irreversible or product decision belongs to the user;
- no safe path remains.

## 10. Failure discipline

Reviewers only judge. Verifiers only execute evidence commands. Researchers only retrieve. Before product edits, load /alaa-testing-strategy `references/120-result-classification.md` for classification and repair eligibility. Report adversarial findings without another fix loop. Name only the lane's matching clean-code skill.

## Direct references

| Before you | Read |
|---|---|
| Plan, allocate workers, reassess remaining work or decide a specialist trigger | `references/routing-matrix.md` |
| Dispatch a role | `references/delegation-prompts.md` |
| Start Stage A, consolidate checks or decide gate requirements | `references/verification-and-gates.md` |
| Select or deviate from a model/effort profile | `references/model-effort-policy.md` |
| Inspect role authority, output or grants, or route a returned report on its first-line `VERDICT` or `STATUS` | `references/agent-catalog.md` |
| Set command priority, workers, timeout or resource limits | `references/resource-policy.md` |
| Classify a failed check | `references/failure-taxonomy.md` |
