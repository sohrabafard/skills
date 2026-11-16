---
name: alaa-cc-orchestrator
description: "Production-grade multi-agent coding orchestration for Claude Code. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. Activation only inspects installed roles; installation requires explicit authorization. It plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates in the workflow-selected checkout. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let /alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa CC Orchestrator

Lead an evidence-driven multi-agent goal inside Claude Code. Narrow subagents inspect, implement, verify, challenge and document. The lead is the main session: it decides how much verification each change needs and reports no unverified claim as complete.

**Mirrored behavior.** Change both runtime orchestrators together. Only runtime mechanics and model-family delegation polarity may differ.

## Admission

Before role inspection or planning, route a single bounded edit whose correctness one reader can confirm to direct execution under its domain owner. Do not start this pipeline for it. Required repository checks still apply.

## When NOT to use

- A single edit one reader can confirm without a second lane.
- A destructive or external effect, including push, deploy, data change or publication, lacks explicit authorization.
- The runtime is Codex rather than Claude Code. These agent files do not serve it.
- A multi-session program centers on plan continuity: `/alaa-workflow` leads and invokes this skill per phase. This skill still writes its plan through workflow.

## Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes or irreversible migrations. Every external or destructive effect needs its own explicit authority.
- Activation grants no installation or update authority. Installation and updates require explicit user authorization for named target paths.
- Plan-only work grants no product execution, branch, or commit authority.
- Local commits follow the main instruction file's local-commit rule through `alaa-workflow references/workspace-and-integration.md`. Its `## Lane branches and commits` governs lane commits and the lane-branch merge. For a commit, do not wait for boundary review or request an already-granted permission again. Never add Co-Authored tags.
- Agent files own code-intelligence grants; dispatches do not. Change grants in this pack, not in `~/.claude/agents`, because a reinstall restores the pack grants.
- Before relying on isolation, inspect the effective sandbox, parent overrides and MCP grants. A read-only declaration proves no enforcement. Report unobservable permissions as unknown.
- Never expose secrets in prompts, logs, artifacts or reports.

## Operating modes

Follow explicit wording. Otherwise choose the lowest-side-effect interpretation that answers the request. Do not ask merely to select a mode.

**Orchestrator mode** applies when the user asks to build, fix, refactor, migrate, integrate, optimize or otherwise change a repository. The lead plans, dispatches, reconciles, verifies as it decides, and reports. It makes its own corrections only under Who fixes in `references/verification-and-gates.md`; implementers own all other implementation. It never silently takes over a failed lane, softens or omits a review finding, claims an unobserved check or overlaps writers. Adopt an existing parent plan; `/alaa-workflow` owns plan, checkpoint and prompts.

**Advisor mode** applies to plans, critiques, architecture advice, prompts, lane definitions or review without implementation. You may spawn research or read-only specialists. Do not implement product changes. Before deciding whether to save a plan, read `alaa-workflow references/artifact-lifecycle.md`. Deliver:

- grounded repository findings;
- a lane plan with dependencies and gates;
- one ready-to-run prompt per lane from the templates, with its agent, model and effort;
- a verification plan and resource policy;
- the risks, assumptions and decisions that require the user.

When a plan is admitted, report the canonical plan address and recovery reference. Otherwise deliver the plan in the reply. Do not imply implementation occurred. When generating a goal condition, read `alaa-prompting-guide references/06-invocation-and-composition.md`.

For native Claude Code Advisor consultation during execution, use the separate route in `references/model-effort-policy.md`.

## Role availability

1. Test design and test execution need the separate companion /alaa-testing-strategy. If it is unavailable, report the missing owner and block dependent work. Never auto-install it.
2. Inspect the installed role definitions, the version and effective tools without writes, and compare the required managed roles with the shipped definitions. For a required external companion, apply its admission in `references/agent-catalog.md`.
3. Before dispatch, report each missing, stale or unavailable model or role as blocked or degraded. Never silently substitute a model or a generic role. Continue only the independent work whose required roles are available.

For an authorized install or update, run `python3 scripts/validate_pack.py` and `python3 scripts/check_agent_grants.py` before you copy the managed agent files. After the copy, compare the SHA-256 of each installed managed file with its entry in `assets/manifest.json`, and report each missing or different file. A copy removes no file: in the same update, move the installed file of a renamed or removed managed role out of the agent discovery directory, under that update's target-path authority. Verify the new role and the absence of the retired role before claiming activation. Change no unrelated agent or setting.

## Plan, allocate, dispatch

1. Before planning, apply the Mandatory Ponytail binding in `alaa-workflow references/companion-routing.md`, including its user opt-out.
2. Inspect guidance and affected paths. Settle outcome, acceptance, preserved behavior and irreversible actions.
3. Before Stage A evidence dispatch, apply `/alaa-memory-os` when its trigger holds: make one bounded recall and verify useful claims in repository truth. Route unresolved prior-session, ownership and shared-contract questions to `alaa-researcher`. `alaa-explorer` uses memory only when the repository cannot answer. Apply `/alaa-code-intelligence-routing` before code-evidence selection and reuse its result.
4. Plan through Planning profile selection in `references/routing-matrix.md`, then finalize and consolidate tasks and dependencies. Planning effort never sets worker effort. Worker selection alone needs no planner dispatch.
5. Allocate the batch once through Batch allocation in that file, and record each role and its selection reason in the plan. For EVERY dispatch, apply its model AND effort allocation and its role triggers, and realize the pair through `references/model-effort-policy.md`. Dispatch only catalog roles whose trigger holds.

### Dispatch discipline

- **One agent per lane.** Dispatch no duplicate lane and no summary-check agent. A lane starts no subagent of its own. Independent verification and review inspect the actual artifact under separate authority. Keep inspection and the lead's own small correction inline.
- **Run independent lanes together.** Start a dependent lane as soon as the lanes it consumes finish. Join lanes behind one barrier only when the next step consumes all of their outputs.
- **Count live lanes before each spawn or follow-up.** At the runtime's concurrency limit, wait for a running lane to finish before you start the next one. After a limit error, free a slot; never resend the same call unchanged. `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns the limit values.
- **After an interruption or a usage-limit error,** record the lane's last evidence in the plan or compact dispatch, and reconcile the transcript, the checkpoint and the surviving files before resuming writes. Apply the stopped-writer recovery in `alaa-workflow references/workspace-and-integration.md`, then dispatch only the remaining scope.
- **Keep dispatches lean.** Word each dispatch under /alaa-prompting-guide. Carry lane facts only: outcome, owned files, exclusions, acceptance, commands, dependencies, resolved skills and return contract. Do not restate the native role definition. State each instruction once. Every dispatch carries `/alaa-low-noise`.
- **Decide verification per change.** Read `references/verification-and-gates.md` for the verification decision, the floors and who fixes.
- **Correct sparingly.** Correct a statement only when its error changes user code, conclusions or decisions. State the correction once, then continue.

## Pipeline

Orchestrator mode keeps Stages A, B and E. Stages C and D run as the verification decision and the floors in `references/verification-and-gates.md` require. Stage F needs requested integration, and explicit authority before its effects. Advisor mode runs no execution stage. Stages are logical outcomes, not workflow phases or separate mandatory dispatches. Coalesce compatible actions and evidence in the workflow plan while preserving outcomes and floors. Before Stage A dispatch, read `references/verification-and-gates.md`.

| Stage | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, each task's verification decision | the plan and decisions are recorded and presented |
| B — Implementation | disjoint lanes, focused subtask checks and bounded task acceptance, with tested diff evidence | every required lane is reconciled against its actual diff |
| C — Verification | the checks that the decisions and the floors require, under the observers they name | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | at the declared boundary, the independent review and specialist gates that the decisions and the floors require | required assessments are complete and every finding has a recorded disposition |
| E — Documentation and final validation | documentation and its grade, required final gates, the report; base integration only when requested and authorized | applicable documentation is validated; whole-engagement final gates wait for its final candidate |
| F — Requested integration | reviewable integration details and explicit authority, then the local merge | authorized integration is complete, or its declined/blocked status is reported; not applicable to local-only work |

## Final report

Report outcome; independent lifecycle verdicts (`IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED`) under `alaa-workflow references/workspace-and-integration.md`; lane changes and files; commands and results, marked run or cited, with tier; review and specialist verdicts and dispositions; each touched document's outcome and grade; curation as persisted, deferred or empty; risks, skipped checks, follow-ups. List each dispatched agent once with its configured and requested pair, separately observed identity or unknown, observable mismatches, and the exceptional-model admission for each escalated dispatch.

Write for a reader who saw no tool call and no lane report: outcome first, and a definition for each lane label or abbreviation the run invented.

Close with one line from the existing plan, roster and evidence: dispatches and distinct roles; underlying checks run or cited, covered children counted once; span from plan `Created` to last authorized commit, or unavailable. Use no timer, extra command or invented budget.

## Verification and resource rules

Before designing implementation or verification, and before planning or executing checks, load /alaa-testing-strategy. Read its `references/100-test-execution.md` for execution, `references/110-execution-resources.md` for resources and timing, and `references/120-result-classification.md` for result classification and diagnosis, and before product edits for repair eligibility.

After a change to this pack, run from the pack directory:

- after an instruction-contract change, `python3 scripts/check_agent_contracts.py`;
- after a change to agent instructions, a contract asset, pins, agents or the version, `python3 scripts/render_agents.py --write`, then `python3 scripts/render_agents.py --check` and `python3 scripts/validate_pack.py`; review the generated wrappers against `assets/implementation-contract.md` and `assets/planner-contract.md`;
- after any change to `agents/`, `python3 scripts/check_agent_grants.py`.

Each command exits `0` when clean, `1` on findings, drift or grant findings, and `2` on unavailable proof. Either nonzero exit blocks completion.

## Stop conditions

Stop successfully only when all of these hold:

- acceptance is evidenced;
- mandatory gates pass, and the final candidate's scope and proof satisfy repository policy and /alaa-testing-strategy;
- the final diff scope is clean, and final touched files match authorized scopes;
- documentation ran, or was explicitly skipped for a grounded reason;
- the final reusable-context gate reports its disposition: persisted, deferred, rejected or absent;
- requested integration is complete, or reported as declined or blocked. Local-only completion needs no integration prompt.

Stop and report partial or blocked status when any of these occurs:

- the same lane or cause blocks twice;
- blocking findings of one kind return after the approach was reconsidered under After a fix in `references/verification-and-gates.md`;
- verification stays flaky, timed out, contaminated or environment-blocked;
- the work needs scope beyond the goal;
- an irreversible or product decision belongs to the user;
- no safe path remains.

## Direct references

| Before you | Read |
|---|---|
| Plan, allocate workers, reassess remaining work, choose review depth or decide a specialist trigger | `references/routing-matrix.md` |
| Dispatch a role | `references/delegation-prompts.md` |
| Start Stage A, decide a task's verification, consolidate checks, triage a finding or choose who fixes | `references/verification-and-gates.md` |
| Realize a model and effort pair, or consult native Advisor | `references/model-effort-policy.md` |
| Inspect role authority, output or grants, or route a returned report on its first-line `VERDICT` or `STATUS` | `references/agent-catalog.md` |
| Set command priority, workers, timeout or resource limits | `references/resource-policy.md` |
| Classify a failed check | `references/failure-taxonomy.md` |
