# Pruned rules, lane L5c-a

Scope: `SKILL.md` and `references/**` of `alaa-cc-orchestrator` and `alaa-codex-orchestrator`, and the
clauses of each pack's `scripts/check_agent_contracts.py` that bind those files. Every row applies to
both packs unless the file column names one pack. File names are relative to the pack.

Codes:

- `P1` to `P6`: the criteria of `lane-brief-2.md`.
- `OWN`: the sentence restated a rule that another skill owns. The owner column names the file that
  still states it. A pointer stays where a decision at that site needs one.
- `DUP`: the rule stays elsewhere in the same pack. A `DUP` row is listed only when a checker clause
  was deleted with it, or when the rule made an agent re-check or re-confirm.

To restore a rule, copy its text from commit `fe101a53` and, where the last column names a clause, put
that clause back in the named tuple of both checker files.

## SKILL.md

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 1 | Do not infer a universal watchdog timeout or a need for per-command narration | OWN | `alaa-low-noise` `SKILL.md` Contract; `references/delegation-prompts.md` keeps it for `<progress>` | `orchestrator_failures`: "Do not infer a universal watchdog timeout" |
| 2 | Every return carries findings, verdicts, counts and artifact paths, never transcripts, full diffs or logs; save bulky output before reporting its path; use bounded invocations | OWN | `alaa-low-noise references/workflow-integration.md` Delegated lanes; "Every dispatch carries `/alaa-low-noise`" stays | none |
| 3 | **Calibrate length**: cover required substance, then stop; start with the outcome; conversation is not storage | OWN | `alaa-low-noise` `SKILL.md` | `cadence_failures` skill tuple: "Calibrate length" |
| 4 | Concurrency facts: what counts against the limit, the refusal and its error text, the undocumented failure at the limit | OWN | `alaa-prompting-guide references/41-claude-code-runtime-features.md` (cc), `references/11-codex-runtime-features.md` (codex); the instruction to free a slot stays | none |
| 5 | The lead owns goal normalization, scope control, lanes, selection, reconciliation, verification, triggers, reporting and stopping | P1 | none | none |
| 6 | Use `routing-matrix.md` for the lead-session task selection and /alaa-prompting-guide for capabilities and control mechanics | P5 | none | none |
| 7 | In a dispatch, expose task-relevant tools and only requirement-bearing examples | OWN | `alaa-prompting-guide`; "Word each dispatch under /alaa-prompting-guide" stays | none |
| 8 | /alaa-prompting-guide owns model-specific verification wording; it owns delegation polarity | P5 | none | none |
| 9 | `verification-and-gates.md` owns intake, lane fields, infrastructure reuse, gate ordering and freezing; `agent-catalog.md` owns role authority and output and assigns the grants; `/alaa-code-intelligence-routing` owns the grant rationale | P5 | the Direct references table routes each read | none |
| 10 | After a memory recall, keep active state in workflow | OWN | `alaa-memory-os`, `alaa-workflow` | none |
| 11 | Final report: write full sentences | P1 | none | none |
| 12 | The router retains legacy loading paths; test "legacy runner forwarding" | P3 | none | none |
| 13 | Schedule the pack checks through the verification decision | P5 | none | none |
| 14 | Proven aggregate coverage discharges only identical child invocations with the same scope and observer | OWN | `alaa-testing-strategy` `SKILL.md`, *A result stays valid until something named invalidates it* | none |
| 15 | `check_agent_contracts.py` checks source requirements, not live model behavior | P6 | stated once in `references/model-effort-policy.md` | none |
| 16 | Lanes commit on the lane branch their dispatch names; the lead merges it only after the required verification accepts it | OWN | `alaa-workflow references/workspace-and-integration.md` `## Lane branches and commits`; the pointer stays | none |
| 17 | Operate within role restrictions when permissions are unobservable | P1 | none | none |
| 18 | This skill leads one goal; section 1 routes Advisor planning artifacts | P5 | none | none |

## references/verification-and-gates.md

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 19 | This orchestrator pair owns scheduling; /alaa-testing-strategy owns check necessity, breadth and proof; workflow owns validation of the mappings | P5 | none | none |
| 20 | A native plan requires its registered issue graph, with no Markdown prerequisite; follow the workflow owner's outage and existing-family rules; use the final phase's exact issue ID | OWN | `alaa-workflow references/task-tracking.md` | none |
| 21 | Never initialize a replacement Beads database | OWN | `alaa-workflow references/task-tracking.md` `## Select before tracking-dependent work` | `CADENCE_REQUIREMENTS`: "never initialize a replacement Beads database" |
| 22 | Tested issue closure advances readiness without claiming reviewed acceptance | OWN | `alaa-workflow references/task-tracking.md` (closure under a pending review) | `CADENCE_REQUIREMENTS`: "tested issue closure advances readiness without claiming reviewed acceptance" |
| 23 | Implementation and documentation lanes commit their owned paths on the named lane branch when their focused checks pass, at any phase, including before final review | OWN | `alaa-workflow references/workspace-and-integration.md` `## Lane branches and commits` and `## Record the tested state` | `CADENCE_REQUIREMENTS`: "Implementation and documentation lanes commit their owned paths …" |
| 24 | A commit is a checkpoint, not acceptance; record review status separately | OWN | same file, `## Record the tested state` | `CADENCE_REQUIREMENTS`: "A commit is a checkpoint, not acceptance; record review status separately" |
| 25 | Reuse applicable standing authority without another approval | DUP | `SKILL.md` Safety and authority: "do not wait for boundary review or request an already-granted permission again" | `CADENCE_REQUIREMENTS`: "Reuse applicable standing authority without another approval" |
| 26 | Preserve an identified snapshot when authority or validation is missing | OWN | `alaa-workflow references/workspace-and-integration.md` `## Record the tested state` | `CADENCE_REQUIREMENTS`: "Preserve an identified snapshot when authority or validation is missing" |
| 27 | The integration parent commits work that no lane owns, and work a lane returned uncommitted | OWN | same file, `## Lane branches and commits` | `CADENCE_REQUIREMENTS`: "The integration parent commits work that no lane owns, …" |
| 28 | Pending review never delays a lane's or the parent's authorized checkpoint | DUP | `SKILL.md` Safety and authority, same sentence as row 25 | `CADENCE_REQUIREMENTS`: "Pending review never delays a lane's or the parent's authorized checkpoint" |
| 29 | A fix after the final merge follows step 7 of `## Lane branches and commits`; lanes with disjoint files may share the checkout; do not create a worktree automatically | OWN | `alaa-workflow references/workspace-and-integration.md` | none |
| 30 | A focused command is the topic selector that /alaa-testing-strategy names | OWN | `alaa-testing-strategy` `SKILL.md` scope tiers | none |
| 31 | Reusable context: workflow owns scan timing, the lessons skill owns admission, the memory skill owns publication | P5 | none | none |
| 32 | `routing-matrix.md` names the three conditions that /alaa-system-design adds; use `context-continuity.md` for position and resume | P5 | none | none |
| 33 | Plan contents: ordered phases, acceptance, focused phase checks, the final gate and handoff knowledge | OWN | `alaa-workflow` | none |
| 34 | Increase parallel writers when capacity and ready work justify it; reserve capacity for the next required gate only when it is ready | P1 | "Dispatch ready independent lanes together when observed host slots and declared resource ceilings permit" stays | none |
| 35 | Lanes choose the smallest discriminating checks for the claimed behavior and for changed exported-surface, contract, type or lint properties, and return the output or mark the property not checked | OWN | `alaa-testing-strategy` focused tier; the cadence table row "Subtask end" stays | none |
| 36 | Role definitions own dispatch-conflict handling | P5 | none | `GATE_REQUIREMENTS`: "Role definitions own dispatch-conflict handling" |
| 37 | Wait for all required lanes | P2 | none | none |
| 38 | `alaa-verifier` collects missing or invalidated evidence when the planned checks require its authority | DUP | Stage C step 2 | `COLLECTION_REQUIREMENTS`: same sentence |
| 39 | When independent checks remain to run, dispatch `alaa-verifier` | DUP | merged into Stage C step 2 | `COLLECTION_REQUIREMENTS`: same sentence |
| 40 | Plan one whole-engagement broad gate stage in Stage E, after final documentation | DUP | Stage E step 3: "Collect required affected and exhaustive checks in one whole-engagement gate stage" | `COLLECTION_REQUIREMENTS`: same sentence |
| 41 | Use only host-exposed dispatch and continuation mechanisms | P1 | none | none |
| 42 | Select required final checks and proof from repository policy and /alaa-testing-strategy | DUP | Check collection | none |
| 43 | Audit every claim against an actual tool result of this session before the report; report in the order `SKILL.md` states | DUP | `SKILL.md`: the lead "reports no unverified claim as complete" and never "claims an unobserved check" | none |
| 44 | Record the last authorized commit timestamp, or record it as unavailable | P3 | the Final report close line states "or unavailable" itself | none |
| 45 | Final criteria: the declared boundary has attributable verification evidence; local checkpoints follow the main instruction rule independently of review status; task progress matches what landed (stated twice) | P3 | Stage E step 5 keeps the progress check | none |
| 46 | Codex only: route Docker socket permission failures through /alaa-codex-runtime-ops before the host fallback | OWN | `alaa-testing-strategy references/110-execution-resources.md` | none |
| 47 | The matrix reason for the test strategist, the "typo versus authentication change" reason, and the per-floor consequence clauses | reason | the rules stay; only the reason clause that restated the rule went | none |

## references/routing-matrix.md

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 48 | `SKILL.md` owns one agent per lane; /alaa-prompting-guide owns capabilities, starting guidance, precedence and projections | P5 | none | none |
| 49 | For each rejected cheaper pair, also record the decomposition you rejected and the exact source row and its date | P3 | the failed fit predicate is still recorded; the exceptional admission still records rejected alternatives | none |
| 50 | Allocation record fields: the task, the authority identity, the runtime control surface, the requested and effective configured controls, availability, unresolved limits | P3 | role, scope and class, departing priority, pair and admission stay; `<task_controls>` carries the verified controls | none |
| 51 | Realize the pair: use only an exact verified available compatibility realization, otherwise block that affected lane; no silent substitution, installation or configuration edit; source changes do not reload roles | DUP | `references/model-effort-policy.md` *Before every dispatch* | `task_allocation_failures` routing tuple: "exact verified available compatibility realization", "block that affected lane", "Source changes do not reload" |
| 52 | Supported capability is not calibrated local quality | P6 | "These routes are uncalibrated workload admissions" stays | none |
| 53 | When the mechanical branch does not fit, evaluate the remaining routes and retrieve unresolved facts; keep the assignment while the same reason applies; do not switch during a command or a progress update | P1 | none | none |
| 54 | What each specialist covers (instruction reviewer, dependency auditor, accessibility reviewer, adversarial lens) | P5 | the role definitions under `agents/` | none |
| 55 | Browser QA: preserve `--browser chromium` and existing profile settings | OWN | `alaa-testing-strategy references/110-execution-resources.md` | none |
| 56 | Read `model-effort-policy.md` before profile changes; a session started before a role was installed may not have it | P5 | none | none |

## references/agent-catalog.md

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 57 | The orchestrator is not a custom subagent; /alaa-prompting-guide owns capabilities and runtime mechanics; the role templates name each role's dispatch inputs | P5 | none | none |
| 58 | `LSP` only reads; Serena's REPL is no read-only grant; an MCP server is a separate process that a withheld `Edit` tool does not stop | OWN | `alaa-code-intelligence-routing references/80-agent-scoping.md`; the assignment sentence stays | none |
| 59 | Which skills three named roles preload (critic, profiler, test strategist) | P3 | the agent files | none |
| 60 | Schedule the grant check or its identical aggregate-covered invocation | OWN | `alaa-testing-strategy` | none |
| 61 | Codex only: section *Policy and runtime evidence* (labels are requested restrictions; inspect effective permissions) | DUP | `SKILL.md` Safety and authority | none |

## references/model-effort-policy.md

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 62 | The list of rules that `routing-matrix.md` owns; capability registries own supported pairs, never defaults; /alaa-prompting-guide owns the rule-writer contract | P5 | none | none |
| 63 | cc: the alias list, "never a full ID", its 2026-11-14 date; invocation effort since version 2.1.292 | OWN | `alaa-prompting-guide references/41-claude-code-runtime-features.md`; "pass the family alias, supply both parameters" stays | none |
| 64 | cc: an advisor reaches each subagent; a Fable 5.2 executor accepts only a Fable 5.2 advisor; no lower-ranked advisor attaches | OWN | same file, **Native Advisor** | none |
| 65 | The executor chooses when to consult and owns the result | P4 | none | none |
| 66 | Refresh the mapping and capability evidence when it drifts | P1 | none | none |
| 67 | Put the verdict or outcome first, then the metadata | P5 | each role definition states it | none |
| 68 | Section *Source generation and proof*: what the projection engine renders; `SKILL.md` owns when to run it | P5 | "Source checks prove neither installed activation…" moved up, kept once | none |

## references/delegation-prompts.md and templates

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 69 | Pass `--sandbox` on each `bd` command that can write, and `--readonly` for a read-only lane | OWN | `alaa-workflow references/task-tracking.md` `## Agent identity and ownership` and `## Beads capabilities in use` | none |
| 70 | `<task_controls>` field "availability or affected-lane blocker" | P3 | none | none |
| 71 | Workflow owns persistence; `SKILL.md` owns interrupted-lane recovery; `verification-and-gates.md` retains scheduling (in `<collection_barrier>`) | P5 | none | none |
| 72 | `20-design.md` `<doctrine>`: the enumerated test-design method | OWN | `alaa-testing-strategy` | none |
| 73 | `20-design.md` `<standard>`: the enumerated design method | OWN | `alaa-system-design` | none |
| 74 | `90-completion/10-operability-evidence.md` `<budget_owner>`: what a budget contains | OWN | `alaa-algorithms-data-structures` | none |
| 75 | `30-implementation.md`: pass the same bounded lane block; apply the same scoped repair and retest limits. `20-review-followup.md`: preserve the repair scope and retest limits below | P1 | none | none |
| 76 | `<trigger>` text in `10-`, `60-`, `70-` and `80-` restated the routing trigger | DUP | `references/routing-matrix.md`; the tag now takes the condition that holds | none |

## Pointer files and codex references/installation.md

| # | Rule removed | Code | Owner or remaining home | Checker clause deleted |
|---|---|---|---|---|
| 77 | `failure-taxonomy.md`, `resource-policy.md`: what the testing-strategy file owns; "this legacy reference remains a loading path" | P5 | none | none |
| 78 | `installation.md`: "Version 5 renames `alaa-implementer-sol`…" and "Since version 4, a report puts the verdict first…" | P3 | the retire-the-old-role rule stays in general form; `CHANGELOG.md` holds the history | none |
| 79 | `installation.md`: /alaa-prompting-guide owns discovery facts; source control owns rollback versions; record those evidence levels separately | P5 | none | none |
| 80 | `installation.md`: canonical policy registers task-selected roles; supply and verify task controls at dispatch | DUP | `references/model-effort-policy.md` | none |

## Checker clauses deleted

17 clauses, the same in both `check_agent_contracts.py` files; no clause was reworded and no logic changed.

| Tuple | Deleted | Rows |
|---|---|---|
| `orchestrator_failures` required tuple | 1 | 1 |
| `cadence_failures` skill tuple | 1 | 3 |
| `GATE_REQUIREMENTS` | 1 | 36 |
| `CADENCE_REQUIREMENTS` | 8 | 21 to 28 |
| `COLLECTION_REQUIREMENTS` | 3 | 38 to 40 |
| `task_allocation_failures` routing tuple | 3 | 51 |
