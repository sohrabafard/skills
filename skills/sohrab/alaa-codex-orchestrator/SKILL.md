---
name: alaa-codex-orchestrator
description: "Production-grade multi-agent coding orchestration for Codex. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates in the workflow-selected checkout. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa Codex Orchestrator

Lead a controlled, evidence-driven multi-agent goal. Narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

**Mirrored behavior.** Change both runtime orchestrators together. Only runtime mechanics and model-family delegation polarity may differ; `/alaa-prompting-guide` owns the latter.

## Admission

Before role inspection or planning, route a single bounded edit whose correctness one reader can confirm to direct execution under its domain owner. Do not start this pipeline for it. Required repository checks still apply.

## Plan and allocation

Apply `references/routing-matrix.md` Planning profile selection and All-role task allocation before planning. Finalize and consolidate tasks and dependencies. Then allocate the batch once, record each registered profile and reason in the plan, and dispatch. Planning effort never sets worker effort. Worker selection alone needs no planner dispatch.

## When NOT to use

- A single edit one reader can confirm without a second lane; delegation costs more than the work.
- A destructive or external effect, including push, deploy, data change or publication, lacks explicit authorization.
- The runtime is Claude Code rather than Codex. These TOML roles do not serve it.
- A multi-session program centers on plan continuity: `/alaa-workflow` leads and invokes this skill for a phase. This skill still writes its plan through workflow.

## 0. Inspect role availability

The separately available companion /alaa-testing-strategy is required for test design, test execution, and legacy runner forwarding. If it is unavailable, report the missing owner and block dependent work. Never auto-install it.

Activation grants no installation or update authority. Inspect installed definitions, version and effective tools without writes. Compare required roles with shipped definitions. Report missing, stale or unavailable roles before dispatch. Never silently substitute a model or a generic role. Continue only independent work with available required roles. Report the rest as blocked.

Install or update only with explicit user authorization for the target paths. Validate model-neutral source roles, grants, and generated artifacts before the first target write. Use the supported materializing installers described in `references/installation.md`. A direct TOML copy inherits parent MCP grants and is unsupported.

Inspect effective sandbox, parent overrides and MCP grants before relying on isolation. Read-only declarations prove no enforcement. Report unobservable permissions as unknown. Operate within role restrictions.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The main thread plans, dispatches, reconciles, gates and reports. It implements only a mechanical local edit with known scope, no design decision, and a few tool calls, in files no active or pending lane owns, because dispatching such an edit costs more than making it. Viable implementers own all other implementation. The verifier runs heavy suites.

### Advisor mode

For plans, critiques, architecture advice, prompts, lane definitions or review without implementation, you may spawn research or read-only specialists. Do not implement product changes. Before deciding whether to save a plan, read `alaa-workflow references/artifact-lifecycle.md` for admission and explicit exceptions. Plan-only work grants no product execution, branch, or commit authority.

Follow explicit wording. Otherwise choose the lowest-side-effect interpretation that answers the request. Do not ask merely to select a mode.

In orchestrator mode, adopt an existing parent plan. `/alaa-workflow` owns plan, checkpoint and prompts. This skill leads one goal. Workflow leads multi-session programs and invokes it per phase.

## 2. Main-thread contract

Use `references/routing-matrix.md` for the actual main-thread task selection and /alaa-prompting-guide for current capabilities and control mechanics. A requested profile is not evidence of this session's observed identity.

It owns goal normalization, scope control, repository-aware lanes, selection and dispatch authority, reconciliation, verification and review, specialist triggers, truthful reporting and stopping.

It must not implement beyond that mechanical-edit exception, run heavy verification, silently take over failed lanes, permit self-approval, soften or omit review findings, claim unobserved checks or overlap writers. Save bulky output and report its path. Destructive, publication, deployment, force-push, data-deletion and external effects require explicit user permission.

### Dispatch discipline

**One agent per lane.** No duplicate lane or summary-check agent. Independent verification and review inspect the actual artifact under separate authority. Dispatch independent lanes together. Keep inspection and Orchestrator mode's mechanical edit inline.

**Start a dependent lane as soon as the lanes it consumes finish.** Join lanes behind one barrier only when the next step consumes all of their outputs. A barrier over a lane whose output the next step never reads idles that step for the unrelated lane's whole runtime.

**Keep dispatches lean.** Apply /alaa-prompting-guide. Carry lane facts only: outcome, owned files, exclusions, acceptance, commands, dependencies, resolved skills and return contract. Do not restate the native role definition, which dilutes both contracts. State each instruction once. Expose task-relevant tools and only requirement-bearing examples.

**Preserve proportional verification.** Read `references/verification-and-gates.md` for gate economics and independent acceptance. /alaa-prompting-guide owns model-specific verification wording.

**Correct sparingly.** Revise a statement only when its error changes user code, conclusions or decisions. State the correction plainly and briefly, then continue. Fix immaterial slips without narration.

**Calibrate length.** Cover required substance, then stop without filler, redundant summaries or boilerplate. Start with the outcome and supporting detail. Save reusable material before reporting its path. Conversation is not storage. /alaa-low-noise owns budgets.

## 3. Intake and planning

Before designing implementation or verification, load /alaa-testing-strategy. Before dispatch inspect guidance and affected paths. Settle outcome, acceptance, preserved behavior and irreversible actions. Draw disjoint lanes. `references/verification-and-gates.md` owns intake, lane fields and infrastructure reuse.

Before Stage A evidence dispatch, apply triggered `/alaa-memory-os`: make one bounded recall, verify useful claims in repository truth, and keep active state in workflow. Route unresolved prior-session, ownership and shared-contract questions to `alaa-researcher`. `alaa-explorer` uses memory only when the repository cannot answer. Apply `/alaa-code-intelligence-routing` before code-evidence selection and reuse its result.

Every dispatch carries `/alaa-low-noise`. Return findings, verdicts, counts and permitted artifact paths, never transcripts, full diffs or logs. Persist reusable context before returning its path. Use bounded invocations and host-required progress. Do not infer a universal watchdog timeout or per-command narration. After an interruption, reconcile transcript, checkpoint and surviving files before resuming writes.

The router below selects role, dispatch and gate owners. `references/verification-and-gates.md` owns gate ordering and freezing before expensive dispatch.

## 4. Model and role routing

For EVERY dispatch apply task model AND effort allocation and role triggers in `references/routing-matrix.md`; `references/agent-catalog.md` owns authority and output. `references/model-effort-policy.md` owns omission normalization before explicit dispatch and routes capability and control mechanics to /alaa-prompting-guide.

Choose one correctness reviewer for a scope. Deep review changes the review task, then requires its own justified model AND effort selection. `alaa-reviewer-deep` is a compatibility identity with the same authority, never a fixed-model escalation.

Report missing models and roles as blocked or degraded, never silent fallback. Diagnose context, tool and specification failures before capacity. Dispatch only triggered catalog roles.

## 5. Orchestrator execution pipeline

Orchestrator mode preserves A–E. F requires requested integration and explicit authority before effects. Advisor mode runs no execution stages. Section 1 routes planning artifacts. Stages are logical outcomes, not workflow phases or separate mandatory dispatches. Coalesce compatible actions and evidence in the workflow plan, preserving outcomes, independence and gate economics. Before Stage A dispatch read `references/verification-and-gates.md` for the inherited phase and final review boundary, cadence, triggers and requirements.

| Stage | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, the profile | the plan and profile are recorded and presented |
| B — Implementation | disjoint lanes, focused subtask checks and bounded task acceptance, with tested diff evidence | every required lane is reconciled against its actual diff |
| C — Verification | focused phase evidence and required pre-review checks under their assigned observers | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | at the declared boundary, independent review and every triggered specialist | findings are resolved or explicitly accepted by the user |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | applicable documentation is validated; whole-engagement final gates wait for its final candidate |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

### Execution profile: size the pipeline to the plan

**Every profile preserves A–E outcomes and required gates at the inherited review boundary.** F is conditional. Local-only completion needs no integration prompt. Record the profile from the finished plan. Escalate on a heavier condition. Do not de-escalate while qualifying evidence persists. `references/routing-matrix.md` owns implementation-role reassessment.

| Profile | Conditions — every one must hold | Shape |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions or deep-review triggers | Stages A–E, and F only when requested; the main thread performs Stage D's review itself instead of dispatching `alaa-reviewer`, and specialists still fire on their own triggers |
| `standard` | anything that is neither `lean` nor `hardened` | Stages A–E with every required gate; F only when requested |
| `hardened` | the change meets the adversarial reviewer's blast-radius condition in `references/routing-matrix.md` | `standard`, plus the architecture design record in Stage A and critic/adversarial judgment at the declared review boundary |

`lean` review is independent because the lead authored no diff. If the work leaves the lane plan, or the lead made a mechanical edit, select `standard` and dispatch `alaa-reviewer` on the complete change.

**No profile suppresses a specialist.** Apply only `references/routing-matrix.md` triggers, identically across profiles.

### Final report

Report outcome; independent lifecycle verdicts (`IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED`) under `alaa-workflow references/workspace-and-integration.md`; lane changes and files; commands and results, marked run or cited, with tier; review and specialist verdicts and dispositions; each touched document's outcome and grade; curation as persisted, deferred or empty; risks, skipped checks, follow-ups. List each dispatched agent once with its configured and requested pair, separately observed identity or unknown, observable mismatches, and the exceptional-model admission for each escalated dispatch.

Close with one line from the existing plan, roster and evidence: dispatches and distinct roles; underlying checks run or cited, covered children counted once; span from plan `Created` to last authorized commit, or unavailable. Use no timer, extra command or invented budget.

## 6. Advisor-mode output

Provide grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; a recommended agent, variant, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Apply section 1's artifact admission. When a plan is admitted, report the canonical plan address and recovery reference. Otherwise deliver the plan in the reply. Do not imply implementation occurred.

When generating a goal condition, read `alaa-prompting-guide references/06-invocation-and-composition.md`; it owns condition syntax and the skill-led kickoff.

## 7. Verification and resource rules

Schedule these commands through `references/verification-and-gates.md` Gate economics. Proven aggregate coverage discharges only identical child invocations with the same scope and observer.

Run `python3 scripts/check_agent_contracts.py` after instruction-contract changes. Exit `0` is clean, `1` is findings, and `2` is unavailable proof. Either nonzero exit blocks completion. The script checks source requirements, not live model behavior.

After changing reviewer instructions, pins, agents, or version, run `python3 scripts/render_agents.py --write`, then `python3 scripts/render_agents.py --check` and `python3 scripts/validate_pack.py`. Exit `0` is clean, `1` is findings or drift, and `2` means unavailable proof. Either nonzero exit blocks completion. Review both generated wrappers against `assets/reviewer-contract.md`.

After any change to `agents/`, run `python3 scripts/check_agent_grants.py`. It verifies the transport-neutral templates. To exercise live resolution manually, run `python3 scripts/check_agent_grants.py --materialize agents <new-empty-output-directory>` and inspect only the generated scratch directory. Exit `0` is clean, exit `1` means grant findings, and exit `2` means the checker could not run. Both nonzero results fail completion. `scripts/validate_pack.py` checks the templates. Both agent installers materialize and validate the live resolved grants before writing.

Before planning or executing checks, load /alaa-testing-strategy. Read its `references/100-test-execution.md` for execution, `references/110-execution-resources.md` for resources and timing, or `references/120-result-classification.md` for result classification and diagnosis. The router below retains legacy loading paths.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Installation and updates require explicit user authorization for named target paths; activation grants none.
- Agent files own code-intelligence grants. Dispatches do not. `references/agent-catalog.md` assigns CodeGraph/Serena read/both/neither. `/alaa-code-intelligence-routing` owns rationale. Change grants here, not `~/.codex/agents`, because reinstall restores pack grants.
- Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. Do not wait for boundary review or request an already-granted permission again. Every external or destructive effect needs its own explicit authority. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only with evidenced acceptance, passing mandatory gates and final candidate scope and proof under repository policy and /alaa-testing-strategy, clean final diff scope, completed or explicitly skipped documentation, and the final reusable-context gate reporting disposition (persisted, deferred, rejected or absent). Report requested integration accurately as authorized, declined or blocked. Local-only completion needs no integration prompt.

Stop and report partial or blocked status after the same lane or cause blocks twice, blockers or majors survive two fix cycles, or verification stays flaky, timed-out, contaminated or environment-blocked. Also stop for scope beyond the goal, user-owned irreversible or product decisions, or no safe path.

## 10. Failure discipline

Reviewers only judge. Verifiers only execute evidence commands. Researchers only retrieve. Before product edits, load /alaa-testing-strategy `references/120-result-classification.md` for classification and repair eligibility. Report adversarial findings without another fix loop. Name only the lane's matching clean-code skill.

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
| Perform an explicitly authorized installation or update | `references/installation.md` |
