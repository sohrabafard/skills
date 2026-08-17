---
name: alaa-codex-orchestrator
description: "Production-grade multi-agent coding orchestration for Codex. Use when a user asks to build, fix, refactor, migrate, review, investigate, or plan non-trivial repository work with an orchestrator/advisor and specialist subagents. On activation, idempotently installs or updates this pack's managed agent TOMLs in ~/.codex/agents, then plans first, sizes the pipeline to that plan, and routes work through scoped implementation, risk-proportional verification, review, and conditional specialist gates on its own work branch. Do not use for trivial edits that need no delegation or for destructive/external actions without explicit authorization. Let $alaa-workflow lead a multi-session program; this skill writes its plan and state through it either way."
---

# Alaa Codex Orchestrator

Convert a product or engineering goal into a controlled, evidence-driven multi-agent execution system. The main thread leads; narrow subagents inspect, implement, verify, challenge, and document. No lane approves itself, and no unverified claim is reported as complete.

**One skill, two runtimes.** This pack and its counterpart for the other runtime are the same orchestrator with identical behaviour by design — same decisions, gates, triggers, and stopping conditions — so a behavioural rule added to one is added to the other in the same change. Only expression differs: each states its mechanics in its own runtime's idiom and carries the delegation polarity its own target model family needs, which `/alaa-prompting-guide` owns. Any other difference is drift.

## When NOT to use

- The change is a single edit whose correctness one reader can confirm without a second lane. Delegation
  then costs more than the work.
- The request is a destructive or externally visible action — a push, a deploy, a data change, a published
  artifact — and no explicit authorization for it exists yet.
- The runtime is Claude Code rather than Codex. The bootstrap here writes `~/.codex/agents` TOMLs and does
  nothing useful there.
- The engagement is a multi-session program whose value is the plan and its continuity rather than one
  goal's parallel role lanes. `$alaa-workflow` (`/alaa-workflow`) leads there and invokes this skill for a
  single phase. This skill still writes its plan through that one; the question is only which of the two leads.

## 0. Bootstrap: ensure managed subagents exist (cheap sentinel check first)

1. Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. From `SKILL_ROOT`, compare `~/.codex/agents/.alaa-codex-orchestrator.version` with `VERSION`, then run `python scripts/check_agent_grants.py --inventory-fingerprint` and compare its output with `~/.codex/agents/.alaa-codex-orchestrator.mcp-inventory`, and confirm every `agents/*.toml` has a same-named file in `~/.codex/agents/`. Only when all three hold are the agents current; skip the rest of this section silently. The presence check is what keeps a deleted agent file from being reported as installed for as long as the sentinels match.
2. When either sentinel is missing or differs, run the platform installer: `scripts/Install-AlaaCodexAgents.ps1` on Windows or `scripts/install-agents.sh` elsewhere. The installer resolves the live parent MCP inventory, materializes each role's exact catalog grant with complete transports, disables every unassigned server, validates the resolved grants, replaces differing same-named files outright, and writes both sentinels. It keeps no backup and no copy of a prior version: the source is under version control, so a copy in the agents home is an unmanaged second copy rather than a safety net. Do not bypass this gate with a plain file copy: the portable files under `agents/` are marked templates and intentionally contain no machine transport.
3. One attempt only. If installation fails for any reason, do not troubleshoot, retry, or read installation docs mid-goal: state the failure in one line, continue with whatever `alaa-*` agents are already installed (or built-in `worker`/`explorer` if none), clearly mark the fallback, and note that one Codex restart may be required for newly installed agents to become discoverable.
4. Never block or delay dispatch on bootstrap. Installation authority stays limited to this pack's named TOMLs and the two sentinel files under `~/.codex/agents`. Never delete or modify unrelated files or global configuration.

Read `references/installation.md` only when the user explicitly asks about installation.

## 1. Operating modes

### Orchestrator mode

Use when the user asks to build, fix, refactor, migrate, integrate, optimize, or otherwise change a repository. The main thread plans, dispatches, reconciles, gates, and reports. It should not perform normal implementation itself while viable implementation agents are available, and it does not run heavy test suites itself — the verifier does.

### Advisor mode

Use when the user asks for a plan, critique, architecture advice, prompts, lane definitions, or review without implementation. Research and read-only specialist agents may be spawned. Do not edit repository files, and do not create workflow artifacts: the plan, critique, or review is the reply. Advisor mode creates a branch, a commit, or a plan file only when the user asks for one, because a request to think about the work is not authorization to change the tree.

Resolve explicit wording first. When intent remains ambiguous, choose the lowest-side-effect interpretation that still answers the request; do not interrupt merely to ask which mode.

In orchestrator mode every goal writes its plan through `$alaa-workflow`, which owns plan files, resumable state, and phase prompt packs; this skill never recreates that machinery. When the engagement is a multi-session program rather than one goal, `$alaa-workflow` leads and invokes this skill for a single phase while keeping plan and state ownership. When one goal is the whole engagement, this skill leads and owns the plan it created there.

## 2. Main-thread contract

The main thread runs the frontier variant at `high` reasoning effort.

It owns goal normalization and scope control; repository-aware lane planning; agent selection and dispatch authorization; cross-lane reconciliation; verification and review gates; specialist-trigger decisions; and final truthfulness and stopping.

It must not: implement while implementation agents are viable; run CPU-heavy verification itself; silently implement a failed lane; let an implementer approve its own change; soften or omit reviewer findings; claim checks it did not observe; fan out overlapping write lanes concurrently; print bulky tool output into the conversation instead of routing it to a file and reporting the path; or run destructive, publishing, deployment, force-push, data-deletion, or externally visible actions without explicit user permission.

### Dispatch discipline

**One agent per lane.** Never several agents for the same lane, and never a subagent whose job is to double-check another subagent's output. Independent lanes still go out together — the constraint is on redundancy, not on parallelism. Do not delegate work the main thread can finish in a handful of tool calls.

**Keep dispatches lean.** Leaner prompts measurably outperform padded ones on this model generation while costing a fraction of the tokens, so prompt bloat here is a quality regression and not merely an expense. Dispatch text carries lane facts only: outcome, owned files, exclusions, acceptance criteria, verification commands, dependencies, and the return contract. The role already lives in the agent TOML; restating it dilutes both. State each instruction once, expose only task-relevant tools, and keep examples only where they encode a real requirement.

**Bound every return.** Each dispatch carries `$alaa-low-noise` (`/alaa-low-noise`): a child returns findings, verdicts, counts, and artifact paths, never transcripts, full diffs, or raw logs, and anything bulky is written to the permitted artifact directory and returned as a path. An unbounded child return is the most common way a main thread's context is flooded, and that cost is charged on every remaining turn of the goal. Anything a later turn or another agent might need again is written to a file first and referenced by path; the conversation is not the storage medium.

**One bounded command per invocation.** Every dispatched agent runs one bounded command per invocation and prints a line naming the step it is starting between them. A watchdog ends a lane on silence rather than on duration, so several commands chained into one long quiet invocation is the shape that loses the whole lane. A killed lane is resumed from its transcript, never restarted: its working tree survived the kill, so the transcript is the only record of which steps had already landed, and a restart repeats those while quietly losing the one that had not.

**Verification is an authority boundary, not redundancy.** `alaa-verifier`, `alaa-reviewer`, and the specialist gates exist because no lane may approve its own change. That is structural. Never skip a gate on the grounds that a lane already checked its own work, and never add a generic "double-check yourself" instruction to a dispatch in place of a real gate.

## 3. Intake and planning

Before any dispatch: inspect the repository's own guidance and the affected code paths; restate the outcome, the checkable acceptance criteria, the preserved behavior, and every irreversible action; then split the work into the smallest lanes with disjoint write scopes and serialize the ones that overlap. `references/verification-and-gates.md` owns the full intake list and what each lane definition must carry.

Before the first Phase A evidence dispatch, invoke `/alaa-memory-os` when its trigger list holds. The lead performs one bounded recall, verifies useful claims against repository truth, and passes only confirmed facts into lane context; active plan and handoff state stay in `/alaa-workflow`. When the unresolved question is itself about a prior session, decision, file, or shared contract, give the exact query to `alaa-researcher`, which owns that read-only memory lane. Independently invoke `/alaa-code-intelligence-routing` before choosing a code-evidence surface, then reuse the routed result rather than asking another surface for the same fact.

Read `references/routing-matrix.md` for specialist triggers and `references/delegation-prompts.md` for dispatch contracts. `references/verification-and-gates.md` owns gate economics — which gate runs before which, and what must be frozen before the expensive one is dispatched.

## 4. Model and role routing

Use the shipped model pins unless a variant is unavailable or the user explicitly overrides them. `references/model-effort-policy.md` owns the full ladder, the runtime capability notes, and the escalation rules; `references/agent-catalog.md` lists every role with its trigger and verdict contract.

The short form: Sol runs the main thread, review, security, architecture, and escalated implementation at `high`, spec analysis, migration safety, and contract review at `medium`, and adversarial review at `xhigh`. Terra is the implementation default at `high` and covers test strategy, research, failure analysis, performance, observability, release, dependency audit, and accessibility. Luna covers exploration, documentation, and browser evidence at `medium`, and deterministic command execution at `low`.

Three rules keep routing decidable. **Terra's ceiling is `high`** and **Luna's ceiling is `medium`** — a lane needing more does not need a higher effort on the same variant, it needs the next variant up, so change the model rather than the effort. And **escalation is earned by decision density, not surface sensitivity**: mechanically applying a ratified decision or a precise spec is Terra work on any surface, because sensitive surfaces already receive Sol-tier scrutiny at the gates. Record the named escalation criterion wherever a pin is raised. When uncertain, do not escalate.

The catalog is a menu, not a fleet. A typical goal fires one to three roles beyond the implementation lanes, because every specialist is gated on a condition. Catalog breadth costs nothing per run; imprecise triggers do.

## 5. Orchestrator execution pipeline

Six phases, in order, and orchestrator mode only. Advisor mode runs none of them: Phases A, B, and F create a branch, write files, and commit, which is exactly what section 1 forbids there. They are also the gate order; there is no second list. `references/verification-and-gates.md` owns what each phase does, its triggers, and what each gate requires — read it before dispatching Phase A.

| Phase | Owns | Ends when |
|---|---|---|
| A — Plan | workspace setup, evidence lanes, the chosen solution and its rejected alternatives, the written plan, the profile | the plan and profile are recorded and presented |
| B — Implementation | one lane per disjoint write scope, focused-tier checks, a commit per completed subtask | every required lane is reconciled against its actual diff |
| C — Verification | one integrated affected-tier plan, executed by an authority that owns no lane | every command reached `PASS`, or the phase ended blocked with the failure classified and its owner named |
| D — Review and specialist gates | the independent review, plus every specialist whose trigger holds | findings are resolved or explicitly accepted by the user |
| E — Documentation and final validation | the documentation lane and its grade, base integration, the single exhaustive run, the report | the tree that will land has been observed |
| F — Integration handshake | the user's decision, then the local merge | the work is on the base branch, or the user declined |

### Execution profile: size the pipeline to the plan

**Every profile runs all six phases.** The profile decides how many agents are dispatched inside them, not which of them happen — a phase skipped is a gate skipped, and no profile has that authority. What `lean` removes is dispatch overhead on a change that cannot justify it, where the cost lands on latency and the user's attention as much as on tokens. Choose the profile once, from the finished Phase A plan, and record it there. Escalate mid-run the moment a heavier profile's condition becomes true; never de-escalate, because the evidence that earned the heavier profile does not stop existing.

| Profile | Conditions — every one must hold | Shape |
|---|---|---|
| `lean` | one lane, one implementation phase, a diff that stays inside the lane plan, and none of the `hardened` conditions | all six phases; the main thread performs Phase D's review itself instead of dispatching `alaa-reviewer`, and specialists still fire on their own triggers |
| `standard` | anything that is neither `lean` nor `hardened` | all six phases, every gate dispatched as written |
| `hardened` | the change meets the adversarial reviewer's blast-radius condition in `references/routing-matrix.md` | `standard`, plus the architecture critic in Phase A and the adversarial reviewer in Phase D |

`lean` drops the reviewer dispatch, never the review. The main thread did not write the diff, so it remains an independent authority over it, which is what the gate exists to guarantee. The moment the diff leaves the lane plan, the profile becomes `standard` and `alaa-reviewer` is dispatched against the complete change.

**No profile suppresses a specialist.** The profile governs the reviewer dispatch and how much ceremony the phases carry; `references/routing-matrix.md` governs which specialists fire, identically at every profile. A one-lane retry change is still `lean` and still gets the observability reviewer. Any attempt to state which specialists a profile excludes would be a second copy of the trigger list, and the copy is what goes stale.

### Final report

Report in this order: the outcome, then the four completion-lifecycle states — `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` — each carrying its own verdict and none collapsed into another, with `alaa-workflow references/workspace-and-integration.md` owning what earns each state and this skill restating none of it; changes by lane and touched files; verification commands with observed results, each marked run or cited and carrying its tier; review and specialist verdicts with the resolution of each finding; documentation outcome with each touched document's grade; reusable-context curation outcome, including persisted, deferred, or empty; residual risks, skipped checks, and follow-ups; and the agent roster — every subagent dispatched this goal, one line each with agent name, pinned model and effort, its self-reported AGENT/MODEL/EFFORT identity line flagging any mismatch, and for every escalated lane the named criterion that earned it.

Close with one run-accounting line: agents dispatched and how many distinct roles that was; checks run versus checks cited; and the branch span, from the plan's `Created` timestamp to the last commit. Every figure is already in hand — the roster, the evidence table, and the plan header plus Phase E's final git inspection — so the accounting costs no extra command and no bookkeeping. Never start a timer and never carry a clock across turns: a run that measures its own slowness by being slower has answered nothing. Call it the branch span rather than the duration, because it excludes planning before the first commit and every gate after the last. The three are diagnostic only together — dispatches well above distinct roles is fix-cycle churn, checks run well above checks cited is the repetition the tiers exist to prevent — and no budget is stated for any of them, because a threshold invented here would be enforced everywhere and grounded nowhere.

## 6. Advisor-mode output

Provide grounded repository findings; a lane plan with dependencies and gates; one ready-to-run prompt per lane using the templates; a recommended agent, variant, and effort per lane; a verification plan and resource policy; and the risks, assumptions, and decisions that require the user. Do not edit files or imply implementation occurred.

## 7. Verification and resource rules

- After any change to `agents/`, run `python scripts/check_agent_grants.py`; it verifies the transport-neutral templates. To exercise live resolution manually, run `python scripts/check_agent_grants.py --materialize agents <new-empty-output-directory>` and inspect only the generated scratch directory. Exit `0` is clean, exit `1` means grant findings, and exit `2` means the checker could not run; both nonzero results fail completion. Run `python scripts/check_agent_grants.py --self-test` when changing the checker itself. `scripts/validate_pack.py` checks the templates, and both agent installers materialize and validate the live resolved grants before writing.
- Exact command semantics come from repository guidance and the dispatch. Never invent a flag merely to make a check pass.
- Lowering process priority is mandatory for declared CPU-heavy local commands; limiting runner-level parallelism is separate and must also be explicit.
- On the user's Windows environment, preserve every explicit `--browser chromium` argument. Never remove, replace, or change it without prior user approval.
- Do not kill unrelated services, dev servers, containers, or processes.
- Do not start duplicate services when a reusable declared service already exists.
- Do not update snapshots, golden files, lockfiles, generated clients, dependencies, or migrations during verification unless that change is an explicitly scoped implementation lane.

Read `references/resource-policy.md` for runner usage and ecosystem examples. Read `references/failure-taxonomy.md` when a check fails.

## 8. Safety and authority

- Repository-local, reversible edits inside declared scopes may proceed in orchestrator mode.
- Ask before destructive Git operations, force pushes, history rewrites, deployment, publishing, production access, data deletion, credential changes, shared-system configuration changes, or irreversible migrations.
- Auto-install authority is limited to this pack's named TOML files and its two sentinels under `~/.codex/agents`. It does not authorize editing `~/.codex/config.toml`, MCP configuration, other skills, or unrelated agents.
- A lane's code-intelligence grant lives in its agent file, not in the dispatch. `references/agent-catalog.md` records which agents hold CodeGraph, the Serena read set, both, or neither; `/alaa-code-intelligence-routing` owns why. Reinstalling this pack restores those grants, so change them here rather than in `~/.codex/agents`.
- Commit on the run's own work branch at each completed subtask — never on the user's base branch, and never as one commit at the end. `alaa-workflow references/workspace-and-integration.md` owns the protocol, including which agent may commit. Push, tag, force-push, history rewrite, branch deletion, and merging into the base each need explicit permission at the time it is needed. Never add Co-Authored tags.
- Never expose secrets in prompts, logs, artifacts, or reports.

## 9. Stop conditions

Stop successfully only when every acceptance criterion has evidence, mandatory gates passed, the exhaustive tier ran once on the final candidate, the final diff scope is clean, documentation was completed or explicitly skipped, the final reusable-context gate reported what was persisted, deferred, rejected, or absent, and the integration handshake was presented with the user's answer recorded.

Stop and report a partial or blocked state when: the same lane is blocked twice by the same cause; blocker or major findings remain after two fix cycles; verification remains flaky, timed out, contaminated, or environment-blocked; scope expands beyond the goal; an irreversible or product decision belongs to the user; or a safe execution path no longer exists.

## 10. Anti-patterns

Each of these inverts a default the main thread would otherwise follow. Rules already stated above are not repeated here.

- spawning every specialist for every task, several agents for one lane, or a subagent whose job is to check another subagent;
- delegating work the main thread could finish in a handful of tool calls, or the main thread implementing and running heavy suites while lanes are viable;
- treating the verifier and reviewer gates as redundancy and skipping them because the work already looks checked — they are authority boundaries;
- using a reviewer as a fixer, a verifier as a debugger, or a researcher as a decision-maker;
- running the full suite, the race detector, or the acceptance set again on a tree that has not changed since the last run — breadth is bought by a change in the tree, never by reaching a new phase or handing the work to a new agent;
- letting an implementation lane run the exhaustive tier on its own work, or running it before the final candidate exists;
- editing the product in response to a shell-parsing, container-runtime, permission, or stale-cache failure that was never classified;
- treating a rerun that passes after a failure as a clean pass;
- dispatching implementation before Phase A produced a written plan with the approach chosen and the alternatives rejected;
- dispatching the full reviewer and specialist set on a change whose plan meets the `lean` conditions, or staying in `lean` after the diff left the lane plan — `lean` removes dispatches, never phases;
- committing the whole goal as one commit at the end, committing onto the user's base branch, or merging into the base before the user confirms;
- printing a diff, a log, or a file into the conversation instead of writing it to the artifact directory and reporting the path;
- deciding a document's size grade locally, or restating a rule this pack routes to its owner, instead of applying the owner's;
- escalating a lane's variant because the goal is important or the surface is sensitive, rather than because the lane meets a named escalation criterion — importance and sensitivity are handled by gates, not tier;
- raising a Terra lane above `high` or a Luna lane above `medium` instead of changing the variant, or pinning any agent at `max`;
- routing the adversarial reviewer's findings into another fix cycle instead of reporting them;
- parallelizing migrations, generated contracts, or shared-state edits;
- instrumenting a run to explain its own cost, when the measurement costs more than the waste it would find;
- pre-loading every clean-code skill into every lane — name only the lane's matching skill.
