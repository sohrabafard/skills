---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates in the workflow-selected checkout. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa CC Orchestrator

Lead a controlled, evidence-driven multi-agent goal inside Claude Code. Narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

**Mirrored behavior.** Change both runtime orchestrators together. Only runtime mechanics and model-family delegation polarity may differ; `/alaa-prompting-guide` owns the latter.

## Admission

Before role inspection or planning, route a single bounded edit whose correctness one reader can confirm to direct execution under its domain owner. Do not start this pipeline for it; required repository checks still apply.

## Plan and allocation

Apply `references/routing-matrix.md` Planning profile selection and All-role task allocation before planning. Finalize and consolidate tasks/dependencies, then allocate the batch once, record each registered profile/reason in the plan, and dispatch. Planning effort never sets worker effort; worker selection alone needs no planner dispatch.

## When NOT to use

- A single edit one reader can confirm without a second lane; delegation costs more than the work.
- A destructive or external effect, including push, deploy, data change or publication, lacks explicit authorization.
- The runtime is Codex rather than Claude Code. These agent files do not serve it.
- A multi-session program centers on plan continuity: `/alaa-workflow` leads and invokes this skill for a phase. This skill still writes its plan through workflow.

## 0. Inspect role availability

Activation grants no installation or update authority. Inspect installed definitions, version and effective tools without writes; compare required roles with shipped definitions. Report missing, stale or unavailable roles before dispatch. Never silently substitute a model or a generic role. Continue only independent work with available required roles; report the rest blocked.

Install or update only with explicit user authorization for the target paths. Validate model-neutral source roles, grants, and generated artifacts before the first target write. Run `python scripts/validate_pack.py` and `python scripts/check_agent_grants.py` before an authorized copy of the managed agent files. Do not change unrelated agents or settings.

Inspect effective sandbox, parent overrides and MCP grants before relying on isolation. Read-only declarations prove no enforcement. Report unobservable permissions unknown and operate within role restrictions.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The lead plans, dispatches, reconciles, gates and reports. It implements only a mechanical local edit with known scope, no design decision, and a few tool calls, in files no active or pending lane owns, because dispatching such an edit costs more than making it; viable implementers own all other implementation, and the verifier runs heavy suites.

### Advisor mode

For plans, critiques, architecture advice, prompts, lane definitions or review without implementation, research/read-only specialists may be spawned. Do not implement product changes. Before deciding whether to save a plan, read `alaa-workflow references/artifact-lifecycle.md` for admission and explicit exceptions. Plan-only work grants no product execution, branch, or commit authority.

Follow explicit wording; otherwise choose the lowest-side-effect interpretation answering the request without asking merely to select a mode.

In orchestrator mode adopt an existing parent plan; `/alaa-workflow` owns plan/checkpoint/prompts. This skill leads one goal; workflow leads multi-session programs and invokes it per phase.

## 2. Lead-session contract

Use `references/routing-matrix.md` for the actual lead-session task selection and /alaa-prompting-guide for current capabilities and control mechanics. Report configured/requested settings separately from observed identity; unobservable values stay unknown.

The lead owns goal normalization/scope control, repository-aware lanes, selection/dispatch authority, reconciliation, verification/review, specialist triggers, truthful reporting and stopping.

The lead must not implement beyond that mechanical-edit exception, run heavy verification, silently take over failed lanes, permit self-approval, soften/omit review findings, claim unobserved checks or overlap writers. Save bulky output and report its path. Destructive, publication, deployment, force-push, data-deletion and external effects require explicit user permission.

### Dispatch discipline

**One agent per lane.** No duplicate lane or summary-check agent. Independent verification and review inspect the actual artifact under separate authority. Dispatch independent lanes together; keep inspection and Orchestrator mode's mechanical edit inline.

**Start a dependent lane as soon as the lanes it consumes finish.** Join lanes behind one barrier only when the next step consumes all of their outputs; a barrier over a lane whose output the next step never reads idles that step for the unrelated lane's whole runtime.

**Keep dispatches lean.** Apply /alaa-prompting-guide. Carry lane facts only: outcome, owned files, exclusions, acceptance, commands, dependencies, resolved skills and return contract. Do not restate the native role definition, which dilutes both contracts. State instructions once; expose task-relevant tools and only requirement-bearing examples.

**Preserve proportional verification.** Read `references/verification-and-gates.md` for gate economics and independent acceptance; /alaa-prompting-guide owns model-specific verification wording.

**Correct sparingly.** Revise statements only when an error changes user code, conclusions or decisions; state it plainly and briefly, then continue. Fix immaterial slips without narration.

**Calibrate length.** Cover required substance, then stop without filler, redundant summaries or boilerplate. Start with the outcome and supporting detail. Save reusable material before reporting its path; conversation is not storage. /alaa-low-noise owns budgets.

## 3. Intake and planning

Before dispatch inspect guidance/affected paths; settle outcome, acceptance, preserved behavior and irreversible actions; draw disjoint lanes. `references/verification-and-gates.md` owns intake, lane fields and infrastructure reuse.

Before Stage A evidence dispatch, apply triggered `/alaa-memory-os`: one bounded recall, verify useful claims in repository truth; keep active state in workflow. Route unresolved prior-session/ownership/shared-contract questions to `alaa-researcher`; `alaa-explorer` uses memory only when the repository cannot answer. Apply `/alaa-code-intelligence-routing` before code-evidence selection and reuse its result.

Every dispatch carries `/alaa-low-noise`; return findings, verdicts, counts and permitted artifact paths, never transcripts/full diffs/logs. Persist reusable context before returning its path. Use bounded invocations and host-required progress. Do not infer a universal watchdog timeout or per-command narration. After interruption reconcile transcript, checkpoint and surviving files before resuming writes.

The router below selects role/dispatch/gate owners. `references/verification-and-gates.md` owns gate ordering and freezing before expensive dispatch.

## 4. Model and role routing

For EVERY dispatch apply task model AND effort allocation and role triggers in `references/routing-matrix.md`; `references/agent-catalog.md` owns authority/output. `references/model-effort-policy.md` owns omission normalization before explicit dispatch and routes capability/control mechanics to /alaa-prompting-guide.

Choose one correctness review profile for a scope. Both standard and deep review routes use the existing `alaa-reviewer`; record the deep-review trigger without creating a duplicate review lane.

Report missing models/roles as blocked/degraded, never silent fallback. Diagnose context/tool/specification failures before capacity. Dispatch only triggered catalog roles.

## 5. Orchestrator execution pipeline

Orchestrator mode preserves A–E; F requires requested integration and explicit authority before effects. Advisor mode runs no execution stages; section 1 routes planning artifacts. Stages are logical outcomes, not workflow phases or separate mandatory dispatches. Coalesce compatible actions/evidence in the workflow plan, preserving outcomes, independence and gate economics. Before Stage A dispatch read `references/verification-and-gates.md` for the inherited phase/final review boundary, cadence, triggers and requirements.

| Stage | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, the profile | the plan and profile are recorded and presented |
| B — Implementation | disjoint lanes, focused subtask checks and bounded task acceptance, with tested diff evidence | every required lane is reconciled against its actual diff |
| C — Verification | centralized phase test collection under its required observer; acceptance at the declared boundary | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | at the declared boundary, independent review and every triggered specialist | findings are resolved or explicitly accepted by the user |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | applicable documentation is validated; whole-engagement final gates wait for its final candidate |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

### Execution profile: size the pipeline to the plan

**Every profile preserves A–E outcomes and required gates at the inherited review boundary.** F is conditional; local-only completion requires no merge prompt. Record the profile from the finished plan. Escalate on a heavier condition; do not de-escalate while qualifying evidence persists. `references/routing-matrix.md` owns implementation-role reassessment.

| Profile | Conditions — every one must hold | Shape |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions or deep-review triggers | Stages A–E, and F only when requested; the lead performs Stage D's review itself instead of dispatching `alaa-reviewer`, and specialists still fire on their own triggers |
| `standard` | anything that is neither `lean` nor `hardened` | Stages A–E with every required gate; F only when requested |
| `hardened` | the change meets the adversarial reviewer's blast-radius condition in `references/routing-matrix.md` | `standard`, plus the architecture design record in Stage A and critic/adversarial judgment at the declared review boundary |

`lean` review is independent: the lead authored no diff. If it leaves the lane plan, or the lead made a mechanical edit, select `standard` and dispatch `alaa-reviewer` on the complete change.

**No profile suppresses a specialist.** Apply only `references/routing-matrix.md` triggers, identically across profiles.

### Final report

Report outcome; independent lifecycle verdicts (`IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED`) under `alaa-workflow references/workspace-and-integration.md`; lane changes/files; commands/results with run/cited and tier; review/specialist verdicts/dispositions; each touched document's outcome/grade; curation persisted/deferred/empty; risks, skipped checks, follow-ups. List each dispatched agent once: configured/requested pair, separately observed identity or unknown, observable mismatches and named escalated-lane admission.

Close with one line from existing plan/roster/evidence: dispatches/distinct roles; underlying checks run/cited, covered children counted once; span from plan `Created` to last authorized commit or unavailable. No timer, extra command or invented budget.

## 6. Advisor-mode output

Provide: grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; recommended agent, model, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Apply section 1's artifact admission: report saved plan/checkpoint paths when admitted; otherwise deliver the plan in the reply. Do not imply implementation occurred.

When generating a goal condition, read `alaa-prompting-guide references/06-invocation-and-composition.md`; it owns condition syntax and the skill-led kickoff.

## 7. Verification and resource rules

Schedule these commands through `references/verification-and-gates.md` Gate economics. Proven aggregate coverage discharges only identical child invocations with the same scope/observer.

Run `python scripts/check_agent_contracts.py` after instruction-contract changes and `python scripts/check_agent_contracts.py --self-test` after checker changes. Exit `0` is clean, `1` is findings, and `2` is unavailable proof; either nonzero blocks completion. These fixtures check source requirements, not live model behavior.


- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- After any change to `agents/`, the grant checker must pass before completion; `references/agent-catalog.md` states its exact invocation and exit-code contract.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- Preserve every explicit `--browser chromium` argument: it is a hard user constraint on browser choice. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes; do not start duplicate services when a reusable declared service exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

Before resource/failure decisions apply the router below.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Installation and updates require explicit user authorization for named target paths; activation grants none.
- Agent files own code-intelligence grants; dispatches do not. `references/agent-catalog.md` assigns CodeGraph/Serena read/both/neither; `/alaa-code-intelligence-routing` owns rationale. Change grants here, not `~/.claude/agents`, because reinstall restores pack grants.
- Commit only with explicit user authorization in the workflow-selected checkout. Otherwise preserve the reviewed diff and snapshot validation through workflow. Every external/destructive effect needs its own explicit authority. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only with evidenced acceptance, passing mandatory gates and final candidate scope/proof under repository policy and /alaa-testing-strategy, clean final diff scope, completed or explicitly skipped documentation, and the final reusable-context gate reporting disposition (persisted/deferred/rejected/absent). Accurately report requested integration as authorized, declined or blocked. Local-only completion needs no integration prompt.

Stop and report partial/blocked after the same lane/cause blocks twice, blockers/majors survive two fix cycles, or verification stays flaky/timed-out/contaminated/environment-blocked; also stop for scope beyond the goal, user-owned irreversible/product decisions, or no safe path.

## 10. Failure discipline

Reviewers only judge, verifiers only execute evidence commands, researchers only retrieve. Before product edits classify shell/runtime/permission/stale-cache failures through `references/failure-taxonomy.md`. Never report fail-then-pass as clean PASS. Report adversarial findings without another fix loop. Name only the lane's matching clean-code skill.

## Direct references

| Before you | Read |
|---|---|
| Plan, allocate workers, reassess remaining work or decide a specialist trigger | `references/routing-matrix.md` |
| Dispatch a role | `references/delegation-prompts.md` |
| Start Stage A, consolidate checks or decide gate requirements | `references/verification-and-gates.md` |
| Select or deviate from a model/effort profile | `references/model-effort-policy.md` |
| Inspect role authority, output or grants | `references/agent-catalog.md` |
| Set command priority, workers, timeout or resource limits | `references/resource-policy.md` |
| Classify a failed check | `references/failure-taxonomy.md` |
