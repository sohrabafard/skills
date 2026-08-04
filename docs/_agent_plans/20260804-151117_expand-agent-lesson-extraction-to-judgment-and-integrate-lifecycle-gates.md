# Workflow Plan - Expand agent lesson extraction to judgment and integrate lifecycle gates

- Task ID: `20260804-151117_expand-agent-lesson-extraction-to-judgment-and-integrate-lifecycle-gates`
- Mode: `plan`
- Profile: `resumable`
- Status: complete with reported out-of-scope constraints
- Created: `2026-08-04T15:11:17Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20260804-151117_expand-agent-lesson-extraction-to-judgment-and-integrate-lifecycle-gates-state.md`
- Machine state: not created

## Summary and Outcome

- Current repository truth: staged changes add `alaa-extract-agent-lessons` as a compact final curation gate, but its admission rule and only output shape require a verified surprise converted into a decision interface. That excludes explicit user or team judgment, accepted taste, non-obvious product knowledge, and reusable rubrics present in the conversation. The two orchestrators and `alaa-workflow` do not yet invoke it. Verified by the staged diff and the current skill bodies.
- Outcome: broaden the skill into a model-neutral reusable-context curator that preserves decision interfaces, judgment rubrics, and durable knowledge cards; integrate signal-driven intermediate curation and a mandatory final admission pass into both orchestrators and the durable workflow.
- Strategy: keep the always-loaded body lean, move detailed output shapes into one progressive-disclosure reference, preserve `alaa-memory-os` as the only publication and note-shape owner, and add lifecycle hooks without duplicating workflow or orchestration rules.

## Scope

- In scope: `alaa-extract-agent-lessons`; its Codex UI metadata and skill indexes; the lifecycle text of `alaa-codex-orchestrator`, `alaa-cc-orchestrator`, and `alaa-workflow`; focused tests or validators needed by those changes.
- Out of scope: memory-store writes, model pins, agent roster or grant changes, installer behavior, vendor files, commits, external publishing, and the unrelated staged crash log.
- Constraints and assumptions: preserve all pre-existing dirty work; stable skill text stays model-neutral and routes prompt/runtime questions to `alaa-prompting-guide`; intermediate workflow state stays in the plan handoff package; durable publication remains conditional on authorization and follows `alaa-memory-os`; no candidate is manufactured when admission fails.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. See `references/context-continuity.md`.

- Confirmed facts (verified, each with how it was verified): the staged skill has one eight-field decision-interface schema and admits only evidence that disproved an assumption or exposed or validated a decision; the supplied article explicitly recommends model judgment, progressive disclosure, team or product opinions and knowledge, and rubrics as reusable context; current orchestrator and workflow bodies contain no extraction hook. Verified through `git diff --cached`, the supplied X article, and complete reads of the three skill bodies.
- Open assumptions (believed but unverified, each with what would verify it): none; the new reference resolved the progressive-disclosure question and passed the pack and fleet-reference validators.
- Ruled out (approach, reason, evidence): renaming the skill, because its current name and staged index entries already describe the broader lesson-curation domain and a rename would create unnecessary routing churn; publishing at every intermediate boundary, because active knowledge first belongs in the workflow handoff and publication authority is conditional.
- Read first on resume (ordered exact paths): `skills/sohrab/AGENTS.md`; `skills/sohrab/alaa-extract-agent-lessons/SKILL.md`; this plan; its correlated checkpoint.
- Environment notes (command shapes that work here, and ones that look right but fail): run Python validation from the repository root under `BelowNormal`; X returned no body through its normal page, while the public mirror endpoint returned the linked article payload.
- Traps (looks correct, is not): treating explicit user judgment as an unverified factual claim rejects the most valuable source; forcing every reusable item into an action interface destroys taste and knowledge; publishing intermediate candidates immediately duplicates active workflow state.
- Completion-audit finding: novelty alone is not value. A retained item needs a counterfactual effect on a future decision, quality judgment, reasoning, or meaningful rediscovery cost. A final repository promotion also cannot mutate evidence after its gates have passed; it must reopen the owning lane and affected gates.

## Final Reusable-Context Curation

- Persisted in this repository: the user-provided judgment that reusable agent context must retain scoped judgment and valuable non-procedural knowledge, not only action interfaces, was promoted into the extraction skill's admission and classification contract. The contract now defines value by the harm caused when context is absent, verifies that compressed output stands alone without the originating chat, preserves high-fidelity references, and reopens proof when final curation requires a repository write. The supplied article's emphasis on judgment, team or product knowledge, rubrics, expressive interfaces, and progressive disclosure was encoded as design guidance rather than copied prose.
- Deferred: no candidate.
- Rejected: no candidate.
- Durable memory publication: not performed because the request authorized repository changes, not a memory-store write; the repository skill is now the canonical destination for this contract.

## Ordered Work

### Phase 1 - Ground the reusable-context contract

- Status: complete
- Depends on: none
- Owned scope: named skills and references, staged diff, supplied authoritative article, memory/workflow ownership boundaries.
- Excluded from this phase: repository edits beyond workflow artifacts.
- Work:
  - [x] Read repository instructions, named skills, the staged skill, and the supplied source.
  - [x] Finish required references and complete-file reads for every skill that will change.
  - [x] Define admission, classification, provenance, authority, safety, and lifecycle acceptance criteria.
- Acceptance criteria: the contract distinguishes explicit judgment from factual knowledge and procedural lessons; each form has checkable provenance and authority; workflow-local and durable destinations do not overlap.
- Validation commands: targeted reads and `git diff --cached` inspection.
- Evidence observed: staged scope and ownership gap confirmed; detailed change contract recorded above.

### Phase 2 - Implement compact skill and lifecycle integrations

- Status: complete
- Depends on: Phase 1
- Owned scope: `skills/sohrab/alaa-extract-agent-lessons/**`, the four skill-index lines, and lifecycle sections in both orchestrators and `alaa-workflow`.
- Excluded from this phase: agent definitions, model policy, memory adapters, installers, unrelated staged files.
- Work:
  - [x] Add the three reusable-context shapes behind progressive disclosure.
  - [x] Add signal-driven intermediate curation and a final admission gate to both orchestrators and workflow.
  - [x] Align UI metadata and both indexes without duplicating owned rules.
- Acceptance criteria: the skill can return zero or more evidence-backed interfaces, rubrics, and knowledge cards; both runtimes use the same portable contract; both orchestrators and workflow have explicit intermediate and final integration points; memory and workflow ownership remain intact.
- Validation commands: targeted text searches and diffs; skill-own validators where present.
- Evidence observed: three reusable-context shapes now live behind one reference; both runtime orchestrators contain signal-driven intermediate and mandatory final hooks; workflow owns handoff placement and completion timing; UI metadata and both indexes describe the broader contract.

### Phase 3 - Validate and reconcile

- Status: complete with reported constraints
- Depends on: Phase 2
- Owned scope: affected validators, final diff, workflow plan and checkpoint.
- Excluded from this phase: unrelated baseline failures and external publication.
- Work:
  - [x] Run pack structure, index, fleet-reference, workflow, and diff checks.
  - [x] Re-read every changed file from disk and reconcile final state.
- Acceptance criteria: required behavior and evidence agree; all applicable native gates pass or exact blockers are reported; unrelated staged work remains untouched.
- Validation commands: `python scripts\validate_sohrab_skill_pack.py`; `python scripts\check_skill_index.py`; `python scripts\check_fleet_references.py`; workflow validator against this plan; `git diff --check` for staged and unstaged changes.
- Evidence observed: `validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, and the Codex orchestrator pack validator passed; targeted searches confirmed all lifecycle hooks and no runtime model names in the extraction skill. The Claude orchestrator pack validator remains red only on unchanged agent-grant files, and `git diff --name-only HEAD -- skills/sohrab/alaa-cc-orchestrator/agents skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py` returned empty. The workflow unit suite ran 23 tests but all 26 reported errors occurred at its nested temporary-directory creation before assertions, with `WinError 5` under the system temp directory, `V:\cache`, and the repository artifacts directory.

### Phase 4 - Completion audit and semantic hardening

- Status: complete
- Depends on: Phase 3
- Owned scope: extraction admission and compression semantics; final-gate reopening behavior in both orchestrators and workflow; requirement-by-requirement proof.
- Excluded from this phase: memory-store writes, unrelated agent grants, installer changes, and the staged crash log.
- Work:
  - [x] Re-read the supplied source and every current lifecycle owner against the active goal.
  - [x] Add a counterfactual value test, cold-start semantic compression test, and high-fidelity reference handling.
  - [x] Prevent final curation from mutating stable repository evidence without reopening affected gates.
  - [x] Run all requirement-scoped validators and reconcile the final worktree.
- Acceptance criteria: a future agent can apply each retained item without the originating chat; novelty without decision, judgment, reasoning, or rediscovery value is rejected; both orchestrators and workflow run intermediate and final curation; any repository write discovered by the final gate reopens affected proof.
- Validation commands: pack, index, fleet-reference, both orchestrator pack, workflow artifact, targeted lifecycle and portability searches, scope-specific whitespace checks, and final diff/status inspection.
- Evidence observed: the 69-skill validator, both indexes, fleet references, Codex orchestrator pack, workflow artifact validator, lifecycle searches, portability search, description budget, and scope-specific whitespace checks passed. The Claude orchestrator pack still fails only on unchanged agent-grant catalog files; its agents and grant checker have no task diff. Full combined whitespace remains red only on the unrelated staged crash log. Generated Python caches and 26 failed workflow temporary directories were moved intact into `_to_delete/20260804-agent-lessons-validation-artifacts/`; the two cache trees retained 2 files and 48,360 bytes plus 2 files and 43,388 bytes, and the temporary tree retained all 26 immediate directories.

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: none.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.

## Blockers and Next Action

- Blockers: no in-scope blocker. The known Claude agent-grant baseline, workflow test-harness permission failure, and unrelated staged crash-log whitespace remain explicit constraints on a whole-repository green claim.
- Next action: none in the requested scope; stage the final mixed working-tree changes when ready to commit, excluding or separately deciding the unrelated crash log.
