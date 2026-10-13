# Workflow Plan - Dual task-store workflow

- Task ID: `20261013-000000_dual-task-store-workflow`
- Mode: execute
- Profile: resumable
- Status: completed
- Created: 2026-10-13
- Parent plan: none
- Prompt pack: not created
- Checkpoint: outputs/20261013-workflow-task-stores/docs/agents/20261013-000000_dual-task-store-workflow-state.md
- Machine state: not created
- Base branch and commit: main, 1207d2e8c17d74ea77920ea9cb285b6c73554c7d
- Work branch: main; no branch, commit, merge or push requested
- Worktree: repository root; clear ownership permits the current checkout

## Summary and Outcome

- Current repository truth: seven workflow references, four profiles, Markdown task syntax and schema-2 JSON. The validator checks task skill bindings/phase evidence, not a task graph. Source and prior advisor/explorer evidence were inspected.
- Outcome: one workflow supports local tracking and explicitly configured Beads without duplicate mutable task state, weaker continuity or a Beads dependency in local mode.
- Strategy: one task-tracking reference, explicit portable metadata, mode-aware templates/helpers, backward compatibility and independent proof.
- Authority: on 2026-10-13 the user lifted the no-file limit and authorized saving and executing this plan, restricted to workflow and directly related files. No other project, installation, live hub mutation, hook/config change, commit or push.

## Scope

- In scope: skills/sohrab/alaa-workflow/**; this artifact directory; narrowly related workflow-specific fixtures or references only for a verified consumer conflict.
- Verified consumer correction: both skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md and skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md mandate universal plan checkboxes at Phase A.9/B.6/E.6 and final success. Replace only these task-authority assumptions and the adjacent dependency-source pointer with workflow-owned selected-store/cursor references. Preserve mirrored behavior, all gates, role/model allocation and Git authority. This is the related-file allowance above, not a general orchestrator refactor.
- Out of scope: client/hub projects, upstream Beads, installed skills/agents, global configuration, vendor, unrelated skill changes, live tasks, remote sync and publication.
- Constraints and assumptions: English portable files; no deletion or unrelated cleanup; completed legacy history stays readable. Static source proof is not live agent-compliance, integration or token-savings proof.

## Ratified Design Contract

### Selection

Task store and artifact profile are independent. Existing families keep their recorded task authority until explicit migration. New work uses Beads only through explicit project adoption/binding, including an external hub without a local .beads directory. CLI/skill presence alone selects nothing. Without adoption use local; resolve conflicting/incomplete binding before tracking-dependent work. Configured but unavailable/mismatched Beads never silently falls back or initializes another database.

The project binding owns workspace, project scope and authority. Workflow records its portable reference, not machine paths or copied settings. Load upstream Beads separately; use binding-owned workspace checks and reuse fresh hook context. No copied CLI manual, hook installation or alternative Beads client.

### Ownership

Local plan tasks own progress and dependencies. Beads owns issue identity/status/priority/assignee, issue edges and native readiness. Beads plans reference issue IDs with phase/skill associations and contain no parallel task checkboxes or mutable issue register.

Plans own goal/scope, phase design/acceptance, evidence, skill mappings, resource conflicts and integration barriers. Existing task acceptance stays in its canonical plan section and issues link it; new issue-only work may own acceptance in its issue. Never keep editable copies of the same acceptance or evidence.

The plan header owns overall workflow status. Checkpoint/JSON statuses are attributable snapshots checked against it. Checkpoint owns execution position/blockers/next action; new checkpoint-bearing plans point there instead of duplicating these fields. Direct-profile position stays in its sole plan. JSON stays compact schema 2, optional for real consumers, with no task table/graph. Its position fields derive from the checkpoint when present, otherwise the direct plan; never edit them independently. Reconcile torn updates from canonical owners before execution or completion. Detailed handoff remains one six-field plan section; small Beads-only work may use issue notes without forcing workflow files.

Phase barriers/acceptance differ from issue dependencies/status. Native readiness does not prove scope, deliverable availability, authority, file/environment independence or acceptance. All issues closed proves none of the four workflow lifecycle states. Claims do not lock files/resources or independently synced PC databases. Cross-PC transfer requires designated ownership and available source/evidence; source Git sync and Dolt task sync are separate authorized actions.

### Recovery and failure

Persist at material progress, decisions, blockers, validation, expensive learning and handoff. On resume/compaction resolve family/store, read the current issue when applicable, plan/handoff when present and checkpoint when admitted, then reconcile actual worktree/evidence. Reuse attributable unchanged proof; invalidate affected proof only. Hooks/prime supply guidance, not task-state authority.

During outages preserve evidence and continue independent authorized analysis; stop tracking-dependent implementation/closure. Reconcile uncertain mutations from actual state before retrying. Never report an unsaved update as saved. Preserve memory/curation, allocation, evidence and lifecycle ownership.

### Executable interface

- Initializer adds --task-store {local,beads}, default local for compatibility, and --beads-binding <portable-reference>, required only for Beads. The caller resolves adoption before invocation; the helper never guesses from PATH, environment or directory existence.
- New metadata: Task store and Task binding. Local binding is not applicable; Beads binding references the project instruction/configuration owner. Helpers never invoke bd, start services or access the network.
- Either new metadata header marks the family; require exactly one of each, a supported store and valid pairing, even under the legacy profile. Both absent retain compatibility. New correlated companion paths must resolve to this exact plan, not merely the same basename.
- New local task: "- [ ] T1: <outcome> [depends: none] [skills: inherit]". IDs are unique/stable; prerequisites name local IDs. Validate missing/duplicate IDs, missing/cyclic edges and completed tasks with incomplete prerequisites. Draft placeholders warn; unresolved executable records fail. Unmarked old artifacts retain compatibility.
- Beads task: "- Issue: <issue-id> [skills: inherit]" or a complete explicit skill override. IDs are opaque, not prefix-pinned. Require unique mappings to phases. Reject authoritative local task checkboxes in Beads work sections. Draft template markers may warn; executable entries may not.
- Extend skill-binding parsing for both shapes; preserve phase skills/availability/acceptance/evidence gates. Offline validation checks structure, not live issue existence, scope or readiness, and reports that limit.
- New checkpoint-bearing plans link position instead of duplicating blockers/next action. Direct remains self-contained. Validate correlated checkpoint/JSON snapshot status for marked families without rewriting/tightening completed unmarked legacy history.
- For marked schema-2 families, current_phase copies the canonical cursor exactly; next_actions/blockers each project the corresponding scalar cursor field into one array entry. Empty/none sentinels project to an empty array; never split punctuation. Trim outer whitespace/code wrapping only. Generated checkpoint and JSON text must match, including casing/punctuation. Normal JSON profiles include a checkpoint; a legitimately admitted direct-plan cursor remains the fallback owner.
- Preserve profiles/schema2. Reject Beads with deprecated standalone --state-only rather than emitting state without a bound plan. Local aliases stay compatible. Invalid combinations exit 2 before writing; collisions exit 1 without partial writes.
- Extend existing tools, not a new scheduler/service/cache/framework. A small internal shared parser is allowed only for demonstrated reuse.
- Template/helper seam: the plan template uses task_store, task_binding, phase_1_work, phase_2_work, task_delegation and position_section render values. Local defaults use T1-T4 with the sequential chain T1->T2->T3->T4; Beads defaults use distinct unresolved issue placeholders. The prose lane owns template placement and explanatory prose; the Python lane owns mode-dependent rendered values, following this contract. Their default cursor strings must match. Neither lane edits the other's files.

### Compatibility cutover and reversal

Install compatible workflow instructions, templates and helpers together before executing a newly marked family. Older consumers cannot safely execute marked families: they may skip issue mappings or their gates. On rollback, freeze these families until compatible consumers return; preserve task truth/evidence and never convert Beads issues to checkboxes or silently select local. Existing unmarked local families continue under their original compatible contract. This delivery changes source only; installation and live activation require a later authorized step.

### Candidate comparison

| Candidate | Ownership and consistency | Benefit/cost | Decision and reviving condition |
|---|---|---|---|
| Selected: one task owner plus phase/acceptance plan | Local plan or Beads owns task truth; references connect independently owned phase evidence | Avoids divergent status and enables native task queries; requires explicit binding and compatible consumers | Adopt for both modes; no mirrored editable task tables |
| Alternative: copy issue state into plan/JSON | Multiple editable owners require reconciliation and conflict handling | Easier standalone reading, but stale copies can authorize duplicate work or false completion | Reject; reconsider only as a generated read-only view if a measured consumer need requires offline visibility and automatic generation/drift checks exist |

Local graph validation uses O(V+E) time/space. Offline structure gates do not prove live workspace identity, issue existence, project scope or readiness.

## Acceptance and Verification Matrix

| ID | Required result | Decisive evidence |
|---|---|---|
| A1 | Local works without bd/network across profiles | Native tests for defaults/explicit local/profile matrix and no bd subprocess |
| A2 | Beads selection is explicit and external-hub compatible | CLI/metadata tests and binding scenario review |
| A3 | No duplicate authoritative task state | Mixed-syntax rejection tests and source/template review |
| A4 | Local graph and skills are usable | Missing/duplicate IDs, missing/cyclic edges, incomplete prerequisites and skill negative cases |
| A5 | Existing profiles/schema2/history remain supported | Existing suite and legacy fixtures |
| A6 | Cursor/status owners are unambiguous | Generated direct/resumable artifacts, snapshot consistency tests and review |
| A7 | Failure never invents fallback/success | Wrong hub/project, outage, uncertain write, closed issue/failed gate scenarios |
| A8 | Resume restores current facts | Cold-start both modes, stale PC2 evidence, shared resources and unchanged proof scenarios |
| A9 | Compressed text preserves behavior | Draft/final record, parent equivalence check, independent instruction review |
| A10 | Existing permission/evidence/lifecycle/curation survive | Pack gates and whole-diff review |
| A11 | Scope/authority holds | Final scoped diff; no other repo/config/live task/install/commit/push |

Fixture proof and independent scenario review are distinct from live runtime compliance. Do not claim unrun Claude/Codex activation, distributed ownership or measured savings.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): source HEAD/branch above; full workflow references/templates read; explorer mapped scripts/tests. Current client binding was inspected read-only during advisory work. User now explicitly authorizes this scoped implementation.
- Open assumptions (believed but unverified, each with what would verify it): installed/live runtime integration is outside source delivery and would require a later authorized pilot.
- Ruled out (approach, reason, evidence): directory-only detection misses hubs; copied Beads manuals drift; automatic fallback forks task truth; automatic migration violates old authority; JSON task tables duplicate trackers; persistent ready caches drift.
- Read first on resume (ordered exact paths): this plan; its checkpoint; workflow references/task-tracking.md once created; review and verification records in this artifact directory.
- Environment notes (command shapes that work here, and ones that look right but fail): Windows PowerShell, Python -B, bounded sequential tests, no service startup. Initial Git status had no changes but warned on pre-existing inaccessible retired temp directories under _to_delete; leave them alone. Hindsight tools unavailable; source truth used. The initial apply_patch replacement failed before writing because Delete/Add targeted one path; repaired using an Update operation.
- Traps (looks correct, is not): existing task parsing proves skills, not graph progress. A local claim proves no cross-PC exclusivity. PC1 uncommitted code is not available on PC2 merely because its task synced. Planning warnings are not executable acceptance.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | artifacts/execution/resume | always | stop affected workflow |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | instruction decisions/compression | always | stop instruction work |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | allocation/dispatch | delegated work | stop affected dispatch |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | source evidence selection | source questions | stop unresolved dependent step |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | retrieval/lane returns | always | keep native output bounded |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | test design/proof | validation | stop affected proof |
| alaa-system-design | skills/sohrab/alaa-system-design/SKILL.md | design pressure-test | ownership/format seam | stop dependent change |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | final curation | completion | stop closure |
| alaa-memory-os | skills/sohrab/alaa-memory-os/SKILL.md | durable publication | authorized publication | defer and retain candidate in handoff |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | verified report | narrative docs | stop affected docs gate |

## Ordered Work

### Phase 1 - Ratify contracts and failure matrix

- Status: completed
- Depends on: none
- Reasoning and selection reason: advisory decisions grounded; independent pressure-test resolves format/ownership gaps.
- Settled/open decisions and invariants: design above is ratified subject to specific evidenced findings.
- Risk and required observers: compatibility and agent instructions; architecture critic and test strategist.
- Owned scope: plan/checkpoint and read-only source analysis.
- Excluded from this phase: source implementation and live operations.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise, alaa-system-design, alaa-testing-strategy
- Work:
  - [x] Inspect source and authority; save the concrete plan. [skills: inherit]
  - [x] Reconcile architecture and failure-matrix advice before writers. [skills: inherit]
- Acceptance criteria: A1-A11 have owners and proof; no unresolved load-bearing choice.
- Validation commands: workflow artifact validator and bounded design review.
- Evidence observed: independent architecture/test advice reconciled in design-gates.md; plan validator exited 0. Its draft-marker warning came from a literal marker named in the design prose; that literal was replaced with descriptive wording.
- Snapshot: HEAD 1207d2e8c17d74ea77920ea9cb285b6c73554c7d; SHA-256 578ba56e3c0b8834f7a899fd8018e0dca3bc78546308da6f1b1602650651f3d7; paths outputs/20261013-workflow-task-stores/design-gates.md. Current design-record identity captured 2026-10-13T00:38:12Z using the source-snapshot.md manifest method; design-manifest.sha256 stores the one-file manifest. The evolving plan/checkpoint receive their own final artifact validation.

### Phase 2 - Implement both task-store paths

- Status: completed
- Depends on: Phase 1
- Reasoning and selection reason: two disjoint lanes implement one settled interface; parser/profile interactions need engineering judgment.
- Settled/open decisions and invariants: metadata/task syntax/compatibility above; no upstream reimplementation.
- Risk and required observers: no-file/collision behavior, local independence and history; focused then independent proof.
- Owned scope: Markdown/templates/metadata lane; separate Python/tests lane.
- Excluded from this phase: parent state, other projects, installed/upstream skills, live tasks and Git effects.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-code-intelligence-routing, alaa-low-noise, alaa-testing-strategy
- Work:
  - [x] Implement policy/reference and conditional templates. [skills: inherit]
  - [x] Implement helpers and discriminating focused tests. [skills: inherit]
  - [x] Reconcile actual diffs and interface evidence. [skills: inherit]
- Acceptance criteria: A1-A8/A10 implemented with focused evidence and no scope drift.
- Validation commands: named lane-specific unittest methods; scoped git diff --check.
- Evidence observed: 22 focused methods passed outside sandbox after the host fixture failure and precise formatting-oracle repair; prose template seam/diff checks passed. See code-lane.md and prose-lane.md. Generated readiness wording changed afterward and requires final independent validation.
- Snapshot: HEAD 1207d2e8c17d74ea77920ea9cb285b6c73554c7d; SHA-256 b67537a006084689f21addcf517fbe6df90aab74a90162c11f625be291f52bc9; paths skills/sohrab/alaa-workflow and both orchestrator gate references. Final source-snapshot.md supersedes lane snapshots for integrated proof; independent suite passed 106 tests on it.

### Phase 3 - Compress and independently review

- Status: completed
- Depends on: Phase 2
- Reasoning and selection reason: wording-only compression followed by independent integrated judgment.
- Settled/open decisions and invariants: no behavior changes disguised as compression; no self-approval.
- Risk and required observers: lost conditions/parser regressions; correctness reviewer and instruction reviewer.
- Owned scope: writer applies rule-writer output; read-only gates inspect source/scenarios.
- Excluded from this phase: broad suites during writes, live integration and scope expansion.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-codex-orchestrator, alaa-low-noise
- Work:
  - [x] Compress controlling text with rule-writer and preserve draft/final evidence. [skills: inherit]
  - [x] Resolve independent correctness/instruction findings through owning writers. [skills: inherit]
- Acceptance criteria: A9/A10 verified; no unresolved blocking/major findings.
- Validation commands: diff/contract review and focused regressions for fixes.
- Evidence observed: selective rule-writer compression and repair drafts checked for equivalence. Three code regressions reproduced six failing subcases before green fixes. Independent correctness and instruction reviewers both returned APPROVED, including issue-only handling and five mirrored consumer corrections. See review-round-1.md, prose-lane.md and code-lane.md.
- Snapshot: HEAD 1207d2e8c17d74ea77920ea9cb285b6c73554c7d; SHA-256 b67537a006084689f21addcf517fbe6df90aab74a90162c11f625be291f52bc9; paths skills/sohrab/alaa-workflow and both orchestrator gate references. Review-round-1.md records approved initial fixes and the subsequent four-fixture-only closure, preserving prior production and instruction approvals.

### Phase 4 - Verify, document and close

- Status: completed
- Depends on: Phase 3
- Reasoning and selection reason: fixed-command independent proof on frozen source; docs follow observed behavior.
- Settled/open decisions and invariants: reuse unchanged covered evidence; no unrun pass.
- Risk and required observers: final compatibility/scope; verifier and narrow documenter.
- Owned scope: test outputs/final report in this directory; narrowly related archive navigation if warranted.
- Excluded from this phase: install, live tasks, other projects, commit/push/release.
- Required skills: alaa-workflow, alaa-codex-orchestrator, alaa-testing-strategy, alaa-low-noise, alaa-extract-agent-lessons, alaa-repo-docs
- Work:
  - [x] Freeze identity; run the affected workflow suite and pack gates. [skills: inherit]
  - [x] Write verified source-only usage/report and check documentation. [skills: inherit]
  - [x] Reconcile acceptance, curation, lifecycle verdicts and final scope. [skills: inherit]
- Acceptance criteria: A1-A11 proved at declared levels; mandatory gates pass; no commit/push.
- Validation commands: python -B -m unittest discover -s skills/sohrab/alaa-workflow/tests -p test_workflow_files.py; python -B scripts/validate_sohrab_skill_pack.py; python -B scripts/check_skill_index.py; python -B scripts/check_fleet_references.py; python -B scripts/check_lifecycle_contract.py; python -B skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py; python -B skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py; workflow artifact validator; scoped diff check.
- Evidence observed: independent final suite passed all 106 tests after reviewed fixture reconciliation. Index, fleet references, lifecycle, both orchestrator validators and source diff checks passed; unchanged skill-pack structure pass reused. Saved-plan validation found missing exact snapshot evidence fields in phases 1-3; the parent supplied observed scoped identities without changing validation. Final artifact closure results are owned by verification.md. Report/index documentation checks are owned by doc-checks.md. No source changes followed the frozen successful source gates.
- Acceptance reconciliation: A1-A6 have 106-test unit/CLI proof; A7-A8 have independent failure/resume scenario review (not live runtime proof); A9-A10 have compression evidence, independent correctness/instruction approval and pack/consumer gates; A11 has the final scoped inventory with unchanged branch/HEAD and no out-of-scope tracked/untracked files. Remaining installation/live activation is outside requested delivery, not an unfinished implementation gate.
- Final curation: scanned design, compression, two repair boundaries, environment failure, validation and documentation. Task-store authority, recovery and issue-only distinctions are already promoted to their canonical workflow references; no competing memory entry is admitted. The one-off Windows fixture restriction stays in task evidence. Rejected duplicate/volatile candidates; no remaining admitted candidates, no memory publication, no pipeline reopen required.
- Lifecycle disposition: IMPLEMENTED and MERGE_CANDIDATE depend on the final artifact closure recorded in verification.md as well as the already-passed source proof/reviews. RELEASE_CANDIDATE and PUBLISHED were not requested. Source is uncommitted and not remotely recoverable from this task's Git operations.
- Snapshot: HEAD 1207d2e8c17d74ea77920ea9cb285b6c73554c7d; SHA-256 b67537a006084689f21addcf517fbe6df90aab74a90162c11f625be291f52bc9; paths skills/sohrab/alaa-workflow and both orchestrator gate references. Source remains frozen; docs/artifact-only changes require only their affected gates.

## Task Allocation

Task choices follow current orchestrator routing, never role defaults. Current spawn supports explicit pair with fork_turns=none; installed roles are neutral. Serving identity and server-side read-only enforcement remain unknown; narrow role authority still binds. Main effective controls are unobservable.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Architecture pressure-test | alaa-architecture-critic | balanced; coupled ownership | gpt-6.1-sol | medium | 2026-10-13; Luna lacks settled cross-boundary decisions | explicit spawn; neutral role | available; observed identity unknown |
| Failure matrix | alaa-test-strategist | balanced; compatibility oracles | gpt-6.1-sol | medium | 2026-10-13; integrated format/failure judgment | explicit spawn; neutral role | available; read-only |
| Markdown/templates | alaa-implementer | balanced; multi-owner consistency | gpt-6.1-sol | medium | 2026-10-13; not a mechanical rewrite across references/templates | explicit spawn; neutral role | available; source only |
| Python/helpers/tests | alaa-implementer | balanced; parser/profile compatibility | gpt-6.1-sol | high | 2026-10-13; sustained coupled parser/legacy/test reasoning warrants high | explicit spawn; neutral role | available; focused proof only |
| Settled wording | alaa-rule-writer | balanced; bounded equivalence | gpt-6-luna | medium | 2026-10-13; finite draft and settled invariants | explicit spawn/reuse; neutral role | available; output only |
| Integrated correctness | alaa-reviewer | balanced; compatibility | gpt-6.1-sol | medium | 2026-10-13; coupled candidate judgment, no model diversity requirement | explicit spawn; neutral role | available; read-only |
| Instruction review | alaa-instruction-reviewer | balanced; authority/continuity | gpt-6.1-sol | medium | 2026-10-13; cross-reference behavior across modes | explicit spawn; neutral role | available; read-only |
| Exact-command proof | alaa-verifier | balanced; finite commands/oracles | gpt-6-luna | medium | 2026-10-13; bounded execution, no design | explicit spawn; neutral role | available; no fixes |
| Temp fixture access failure | alaa-failure-analyst | balanced; bounded traced host error | gpt-6-luna | medium | 2026-10-13; fixed log/helper path, no broad diagnosis or retries | explicit spawn; neutral role | available; read-only classification |
| Verified report | alaa-documenter | balanced; finite prose | gpt-6-luna | medium | 2026-10-13; grounded inputs and limited scope | explicit spawn; neutral role | available; docs only |

## Delegation

- Dependency edges and ready sets: design gates first; disjoint prose/templates and Python/tests next; reconcile interface, compress, review; resolve findings before frozen suite and final docs.
- Disjoint writes and shared-resource conflicts: parent owns plan/checkpoint; prose writer owns workflow Markdown/assets/openai metadata; code writer owns Python/tests. No source writes during final gates; one test process at a time.
- Integration barriers and parallel/serialized rationale: settle syntax before writers; focused code tests wait for required templates. No services or installation.
- Consolidated tasks/checks and preserved outcome/evidence mappings: one affected suite and relevant pack gates on unchanged candidate; focused writer results never replace independent acceptance.
- Reusable evidence and invalidation conditions: HEAD plus scoped SHA-256 manifest, covered inputs and observer; rerun affected invalidated checks only.
- Interrupted lane progress paths: writers keep bounded lane records in this directory; reconcile surviving files before redispatch.
- Documentation: controlling Markdown is implementation source; documenter owns only verified usage/report and navigation.

## Blockers and Next Action

- Blockers: none; scoped edit authority is explicit. Retired-directory access warnings are outside scope.
- Next action: none within the authorized source delivery after the final artifact closure recorded in verification.md; installation or live pilot requires a separate request.
