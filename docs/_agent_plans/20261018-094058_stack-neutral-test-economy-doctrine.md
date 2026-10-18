# Workflow Plan - Stack-neutral test economy doctrine

- Task ID: `20261018-094058_stack-neutral-test-economy-doctrine`
- Mode: `execute`
- Profile: `resumable`
- Task store: `beads`
- Task binding: AGENTS.md#beads
- Status: completed
- Created: `2026-10-18T09:40:58Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261018-094058_stack-neutral-test-economy-doctrine-state.md`
- Machine state: not created
- Base branch and commit: `main` at `76efada12`
- Work branch: `main` (no commit authority; changes stay uncommitted)
- Worktree: none

## Summary and Outcome

- Original-entry repository truth: `alaa-testing-strategy` owns test doctrine but has no rule for when a test
  must not be written, no topic-selector rule, no setup-once rule and no build-economy rule. Several
  passages push breadth with no realism filter (`references/10-what-makes-a-test.md:7`,
  `references/60-coverage.md:25-38`, `references/30-doubles.md:53`). Stack skills tell the authoring lane
  to run whole suites (`alaa-golang/SKILL.md:60-64`, `alaa-golang-fiber/references/30-validation-testing.md:123`,
  `alaa-php-clean-code/SKILL.md:201`, `alaa-go-chi-development/references/10-consumer-development.md:92`)
  and repeat builds (`alaa-go-chi-development/assets/templates/consumer-update-prompt.md:38`,
  `alaa-cicd-laravel-postgres/references/10-gate-register.md:11-14`,
  `alaa-quasar-app-vite-v3/references/75-testing-ci-playbook.md:27,39-42`). The orchestrator pair restates
  tier and reuse rules and re-runs affected checks per fix cycle (`references/verification-and-gates.md:17,66,72-73,78,110`).
- Outcome: one stack-neutral doctrine in `alaa-testing-strategy` owns five decisions (test need, realism,
  topic selection, setup once, build once); stack skills carry short native bindings; the orchestrator
  pair, implementer contract, test strategist and reviewer contracts point to the doctrine.
- Strategy: doctrine first (it fixes the vocabulary), then stack bindings and orchestrator pair, then
  gates and independent instruction review.

## Scope

- In scope: `skills/sohrab/alaa-testing-strategy`; stack skills `alaa-golang`, `alaa-golang-fiber`,
  `alaa-golang-clean-code-principles`, `alaa-go-chi-development`, `alaa-php-clean-code`,
  `alaa-cicd-laravel-postgres`, `alaa-vue-typescript-clean-code`, `alaa-quasar-app-vite-v3`,
  `alaa-bash-shell`, `alaa-gitlab-ci-cd`, `alaa-k8s-helm`, `alaa-haproxy`, `alaa-haproxy-lua`,
  `alaa-makefile`, `alaa-docker-production`, `alaa-project-constitution` template; both orchestrators
  (references, implementation contract, test strategist agent, reviewer contract, rendered implementers).
- Out of scope: `vendor/` (read-only); a new Python skill (follow-up); `alaa-verifier`; commits and pushes.
- Constraints and assumptions: one owner per rule (`skills/sohrab/AGENTS.md`); orchestrator pair changes
  together; router moves to `references/00-topic-map.md` at 9 references; English in files; compression
  contract in `alaa-prompting-guide/references/60-skill-authoring.md`; `/name` call form only in new text.

## Handoff Package

Knowledge held only in the current agent's head disappears on compaction. Fill a field when knowledge is learned, not on a schedule; leave unused fields empty. Field semantics are in the skill's `alaa-workflow references/context-continuity.md`, not in this repository.

- Confirmed facts (verified, each with how it was verified): line references in "Current repository truth"
  were read by two Explore lanes and spot-checked by direct reads of `alaa-testing-strategy/SKILL.md`
  and a grep for `go test ./...` on 2026-10-18. Vendor `engineering/testing-strategy/SKILL.md` is 33
  lines with no realism, selection or setup rule (read directly). No Python skill exists in
  `skills/sohrab` or `skills/.curated` (Explore lane).
- Open assumptions (believed but unverified, each with what would verify it): none yet.
- Ruled out (approach, reason, evidence): adopting `/engineering:testing-strategy` as the owner — it
  pushes "edge cases" and "coverage targets" with no realism filter and covers neither selection nor
  setup economy.
- Read first on resume (ordered exact paths): this plan; the checkpoint;
  `skills/sohrab/AGENTS.md`; `skills/sohrab/alaa-testing-strategy/SKILL.md`; `references/90-test-economy.md` once it exists.
- Environment notes (command shapes that work here, and ones that look right but fail): run `bd`
  commands one at a time; `bd` prints a harmless `beads.role` warning.
- Traps (looks correct, is not): codex agent TOML `developer_instructions` is a single-line basic string; a literal newline breaks render_agents.py with `Illegal character '\n'` — write `\n`. `check_agent_contracts.py` locks exact phrases in `verification-and-gates.md`; add text beside them, never rewrite them. Implementer agent files are rendered from
  `assets/implementation-contract.md`; edit the asset and run `scripts/render_agents.py --write`.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-prompting-guide | `skills/sohrab/alaa-prompting-guide/SKILL.md` | Phase 1 | any edit to skill or agent text | stop instruction edits |
| alaa-testing-strategy | `skills/sohrab/alaa-testing-strategy/SKILL.md` | Phase 1 | doctrine authoring | read files directly |
| alaa-cc-orchestrator | `skills/sohrab/alaa-cc-orchestrator/SKILL.md` | Phase 3 | orchestrator edits and its scripts | read files directly |
| alaa-low-noise | `skills/sohrab/alaa-low-noise/SKILL.md` | Phase 4 | gate runs and reviewer output | bounded commands |
| alaa-workflow | `skills/sohrab/alaa-workflow/SKILL.md` | Phase 5 | corrective execution and evidence continuity | stop workflow mutations |
| alaa-codex-orchestrator | `skills/sohrab/alaa-codex-orchestrator/SKILL.md` | Phase 5 | scoped lanes and independent acceptance | stop dispatch |
| alaa-golang | `skills/sohrab/alaa-golang/SKILL.md` | Phase 5 | Go validation and selection corrections | stop Go changes |
| alaa-quasar-app-vite-v3 | `skills/sohrab/alaa-quasar-app-vite-v3/SKILL.md` | Phase 5 | Quasar command correction | stop Quasar changes |
| alaa-extract-agent-lessons | `skills/sohrab/alaa-extract-agent-lessons/SKILL.md` | Phase 6 | final engagement curation | stop closure |

## Ordered Work

Keep only phases with a distinct decision, authority or integration barrier. Merge compatible work while retaining each acceptance outcome and evidence mapping.

### Phase 1 - Doctrine in alaa-testing-strategy

- Status: completed
- Depends on: none
- Reasoning and selection reason: coupled judgment; defines the vocabulary every other phase cites.
- Settled/open decisions and invariants: five decisions as in Outcome; core rule, proof levels and tiers
  stay; no framework construct named in the doctrine.
- Risk and required observers: instruction text controlling agents; independent instruction reviewer in Phase 4.
- Owned scope: `skills/sohrab/alaa-testing-strategy/**`.
- Excluded from this phase: every other skill.
- Required skills: alaa-prompting-guide, alaa-testing-strategy
- Work:
  - Issue: alaa-g4q.1 [skills: inherit]
- Acceptance criteria: test-need decision, realism gate, topic selection, setup once and build once are
  stated once; conflicting passages rewritten; router moved to `references/00-topic-map.md`; output
  contract, stop conditions and anti-patterns updated.
- Validation commands: `python scripts\validate_sohrab_skill_pack.py`; `python scripts\check_fleet_references.py`.
- Evidence observed: on HEAD `76efada12` + scoped sha256 `9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf` (git diff HEAD -- skills/sohrab plus the two new references): validate_sohrab_skill_pack, check_skill_index, check_fleet_references, check_lifecycle_contract exit 0; both orchestrators check_agent_contracts, validate_pack, check_agent_grants, render_agents --check exit 0; validate_constitution --template PASS. alaa-instruction-reviewer: pass 1 CHANGES-REQUESTED (17 findings), pass 2 APPROVED-WITH-NITS; nits 1-4 fixed after pass 2 and gates re-run, not re-reviewed.
- Snapshot: HEAD 76efada12 SHA-256 9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf paths skills/sohrab (uncommitted)

### Phase 2 - Stack bindings

- Status: completed
- Depends on: Phase 1
- Reasoning and selection reason: bounded semantic edits per stack against settled vocabulary.
- Settled/open decisions and invariants: bindings name native mechanisms only and point to the doctrine;
  whole-suite runs move to verifier tiers; kit conformance harnesses stay mandatory.
- Risk and required observers: Phase 4 reviewer.
- Owned scope: the stack skills listed in Scope plus the constitution template.
- Excluded from this phase: orchestrators, `alaa-testing-strategy`.
- Required skills: alaa-prompting-guide
- Work:
  - Issue: alaa-g4q.2 [skills: inherit]
- Acceptance criteria: no lane directive runs the whole suite after an edit; no per-file test mandate;
  go-chi consumers have a test boundary; duplicate builds removed in the named passages.
- Validation commands: Phase 4 gates.
- Evidence observed: on HEAD `76efada12` + scoped sha256 `9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf` (git diff HEAD -- skills/sohrab plus the two new references): validate_sohrab_skill_pack, check_skill_index, check_fleet_references, check_lifecycle_contract exit 0; both orchestrators check_agent_contracts, validate_pack, check_agent_grants, render_agents --check exit 0; validate_constitution --template PASS. alaa-instruction-reviewer: pass 1 CHANGES-REQUESTED (17 findings), pass 2 APPROVED-WITH-NITS; nits 1-4 fixed after pass 2 and gates re-run, not re-reviewed.
- Snapshot: HEAD 76efada12 SHA-256 9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf paths skills/sohrab (uncommitted)

### Phase 3 - Orchestrator pair and agents

- Status: completed
- Depends on: Phase 1
- Reasoning and selection reason: mirrored behavioural edit in two runtimes; ordinary judgment.
- Settled/open decisions and invariants: cc and codex differ only in mechanics; `alaa-verifier` unchanged.
- Risk and required observers: orchestrator contract scripts; Phase 4 reviewer.
- Owned scope: `skills/sohrab/alaa-cc-orchestrator/**`, `skills/sohrab/alaa-codex-orchestrator/**`.
- Excluded from this phase: stack skills.
- Required skills: alaa-prompting-guide, alaa-cc-orchestrator
- Work:
  - Issue: alaa-g4q.3 [skills: inherit]
- Acceptance criteria: restated tier/reuse rules replaced by pointers; fix-cycle and build-reuse rules
  changed; strategist, implementer and reviewer contracts updated; implementers re-rendered.
- Validation commands: per orchestrator `check_agent_contracts.py`, `render_agents.py --check`,
  `validate_pack.py`, `check_agent_grants.py`.
- Evidence observed: on HEAD `76efada12` + scoped sha256 `9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf` (git diff HEAD -- skills/sohrab plus the two new references): validate_sohrab_skill_pack, check_skill_index, check_fleet_references, check_lifecycle_contract exit 0; both orchestrators check_agent_contracts, validate_pack, check_agent_grants, render_agents --check exit 0; validate_constitution --template PASS. alaa-instruction-reviewer: pass 1 CHANGES-REQUESTED (17 findings), pass 2 APPROVED-WITH-NITS; nits 1-4 fixed after pass 2 and gates re-run, not re-reviewed.
- Snapshot: HEAD 76efada12 SHA-256 9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf paths skills/sohrab (uncommitted)

### Phase 4 - Validate and review

- Status: completed
- Depends on: Phase 2, Phase 3
- Reasoning and selection reason: integration barrier.
- Settled/open decisions and invariants: exit 2 is a failed gate.
- Risk and required observers: `alaa-instruction-reviewer` (fresh context).
- Owned scope: fixes for findings only.
- Excluded from this phase: new scope.
- Required skills: alaa-low-noise
- Work:
  - Issue: alaa-g4q.4 [skills: inherit]
- Acceptance criteria: required behavior and evidence agree.
- Validation commands: `python scripts\validate_sohrab_skill_pack.py`; `python scripts\check_skill_index.py`;
  `python scripts\check_fleet_references.py`; `python scripts\check_lifecycle_contract.py`; Phase 3
  scripts; grep proofs from the approved plan.
- Evidence observed: on HEAD `76efada12` + scoped sha256 `9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf` (git diff HEAD -- skills/sohrab plus the two new references): validate_sohrab_skill_pack, check_skill_index, check_fleet_references, check_lifecycle_contract exit 0; both orchestrators check_agent_contracts, validate_pack, check_agent_grants, render_agents --check exit 0; validate_constitution --template PASS. alaa-instruction-reviewer: pass 1 CHANGES-REQUESTED (17 findings), pass 2 APPROVED-WITH-NITS; nits 1-4 fixed after pass 2 and gates re-run, not re-reviewed.
- Snapshot: HEAD 76efada12 SHA-256 9abd6bc5acbe34da348fd8cb452f7e88a38438f8b22733412e2e3ebafdcc7acf paths skills/sohrab (uncommitted)

### Phase 5 - Repair the six independently reviewed findings

- Status: completed
- Depends on: Phase 4
- Reasoning and selection reason: bounded semantic repairs with reproduced causes and settled acceptance; two independent write scopes.
- Settled/open decisions and invariants: preserve the existing test-economy change and the resolved Postgres/SQLite decision; no commits, installation, publication or unrelated edits.
- Risk and required observers: independent verification and fresh instruction-contract review in Phase 6.
- Owned scope: the three Go/Quasar files, paired orchestrator sources and generated outputs, and the two conflicting consumer-test/setup sentences in the testing owner reference listed below.
- Excluded from this phase: unrelated skill changes, vendor, global configuration, model policy and existing historical evidence.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-testing-strategy, alaa-codex-orchestrator, alaa-low-noise
- Work:
  - Issue: alaa-g4q.7 [skills: alaa-prompting-guide, alaa-testing-strategy, alaa-golang, alaa-quasar-app-vite-v3, alaa-low-noise]
  - Issue: alaa-g4q.8 [skills: alaa-prompting-guide, alaa-testing-strategy, alaa-codex-orchestrator, alaa-cc-orchestrator, alaa-low-noise]
- Acceptance criteria: all six obligations below are represented consistently in source instructions and their generated projections; focused checks pass. Task results remain in the issues.
- Validation commands: scoped `git diff --check`; both orchestrators `python -B scripts/render_agents.py --check`; syntax-check the repaired Quasar command after substituting placeholders.
- Evidence observed: focused repair results are recorded in alaa-g4q.7 and alaa-g4q.8. Both lanes froze their writes; the parent reconciled 27 corrective skill paths, with 36 other baseline skill paths byte-identical. Exact correction diff and manifest: `outputs/20261018-test-economy-review-fixes/corrections.diff` and `candidate.json`.
- Snapshot: HEAD 76efada1200041d694b42c6d7c6a53939d364a5c SHA-256 224cc863d868a04725800ee2d7f6ea3ec0fbbe2a8ea6eb5c4f7c9db8813f2b6d paths skills/sohrab (63 paths enumerated in outputs/20261018-test-economy-review-fixes/candidate-source-manifest.txt).

### Phase 6 - Verify and independently review the repaired candidate

- Status: completed
- Depends on: Phase 5
- Reasoning and selection reason: independent acceptance barrier for the combined candidate.
- Settled/open decisions and invariants: source and rendered evidence must identify the same frozen snapshot; static gates do not establish live agent compliance.
- Risk and required observers: an independent verifier and one fresh instruction reviewer; neither authored a repair.
- Owned scope: verification evidence and review verdict for the complete six-finding correction.
- Excluded from this phase: implementation outside an explicitly routed finding repair; commits and publication.
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-testing-strategy, alaa-low-noise, alaa-extract-agent-lessons
- Work:
  - Issue: alaa-g4q.9 [skills: inherit]
- Acceptance criteria: all six scenario obligations pass; required gates exit 0; independent instruction review has no unresolved findings; the workflow and issue evidence agree.
- Validation commands: four root gates (`validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, `check_lifecycle_contract.py`); both orchestrators (`check_agent_contracts.py`, `validate_pack.py`, `check_agent_grants.py`, `render_agents.py --check`); constitution-template validation; workflow-family validation; `git diff --check`. Invoke Python with `-B`; no checker logic changed, so self-tests are not owed.
- Evidence observed: independent verifier PASS (15/15 native/workflow/diff gates; Quasar syntax and mocked call order passed after the recorded sandbox startup failure). Fresh instruction reviewer APPROVED with no findings; all six scenarios, 17 generated implementers, both manifests and 36 preserved baseline skill files reconciled. Evidence: `outputs/20261018-test-economy-review-fixes/verification.md`, `verification-results.json`, and `independent-review.md`. The task result belongs to alaa-g4q.9. Sources remained frozen throughout both observers.
- Snapshot: HEAD 76efada1200041d694b42c6d7c6a53939d364a5c SHA-256 224cc863d868a04725800ee2d7f6ea3ec0fbbe2a8ea6eb5c4f7c9db8813f2b6d paths skills/sohrab (candidate-source-manifest.txt in the corrective-run evidence directory).

#### Six correction obligations

| Finding | Required outcome |
|---|---|
| 1 | Keep build-cache reuse separate from test-result reuse. Permit fresh execution when the result-validity conditions change or the required observer/final proof demands it, including affected-tier external-dependency checks. |
| 2 | Retain one build/link check for shipped Go entrypoints; tests alone do not prove the application's main entrypoint links. Reuse a matching existing shipped artifact. |
| 3 | Consolidate tagged and normal Go runs only after proving selected files/configurations cover the required normal behavior; negated/composite build constraints can exclude code and tests. |
| 4 | Exclude consumer tests that only re-prove dependencies, while retaining tests of decisions owned by the kit/package currently being developed and every always-owed test. |
| 5 | Preserve per-test setup for creation behavior and resources without safe rollback, namespace or reset; share infrastructure only at a reset-safe scope. |
| 6 | Keep the small-UI Quasar command syntactically complete and retain its build step; comments must not consume commands or leave a dangling `&&`. |

#### Corrective-run evidence and scope

- Baseline: `main`, HEAD `76efada1200041d694b42c6d7c6a53939d364a5c`; 65 pre-existing changed files. `outputs/20261018-test-economy-review-fixes/baseline.json` captures their content and hashes before repairs.
- Prior review reproduced three Go counterexamples: a cached pass after an HTTP dependency changed; `go test` passing while a main-less executable failed `go build`; and `!integration` tests omitted by the tagged selection. The original Quasar command failed `bash -n` with exit 2. These observations motivate the repairs, not proof of the repaired instructions.
- Snapshot method: sort repository-relative paths, hash each file's raw bytes with SHA-256, then hash the UTF-8 LF manifest of `path + NUL + file hash + LF`. Include tracked and untracked files in the declared scope; keep the manifest outside that scope.
- Parent integration found the same setup exception missing in the owned Go reference, and the same consumer-test/setup defects in two testing-owner sentences. The existing lanes received those bounded corrections before source freeze; no new policy was introduced.
- Verification dispatch omitted explicit tier labels. The parent assigns the final aggregate native gates to exhaustive source/artifact verification and the Quasar scenario checks to affected proof. The observed commands and independent authority did not change; this metadata correction invalidates no result.
- Native gates are static source/artifact proof. Instruction review must separately walk all six scenarios and cross-runtime projections; neither claims installed activation or live agent behavior.
- The initial Beads creation attempted parent-child and discovered-from edges to the same issue and was rejected before issue creation. Follow-ups instead retain parent `alaa-g4q` and point discovered-from to the corresponding original child. Readback confirmed both blocking edges into `alaa-g4q.9`.

## Task Allocation

After finalizing tasks, dependencies and consolidation, record the runtime orchestrator's all-role allocation.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Prompting-guide supplies capability/mechanics evidence; workflow stores decisions. Unresolved controls or availability block the affected dispatch. Material changes reassess only affected remaining tasks.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| Phases 1-3, coupled instruction authoring | main session (implementer) | P2; shared vocabulary needs one author | claude-opus-5-5 | session effort (not observable) | session runtime, 2026-10-18 | direct | available |
| Phase 4 review | alaa-instruction-reviewer | P2; independent read-only review | agent default | agent default | agent catalog, 2026-10-18 | Agent tool | available |
| Phase 5 Go/Quasar repair | alaa-implementer-low | balanced; known causes and bounded wording decisions | gpt-6-luna | medium | bounded semantic fit: three named files, reproduced defects, explicit six-obligation contract; routing-matrix and model-selection guidance, 2026-10-18 | explicit spawn controls; unpinned installed role | host supports pair; serving identity unknown |
| Phase 5 mirrored contracts | alaa-implementer-low | balanced; settled exceptions and deterministic projections | gpt-6-luna | medium | bounded semantic fit: four paired source files, two conflicting sentences in the existing testing owner, and generator-owned projections; no new policy decisions; scope refined before final freeze, 2026-10-18 | explicit spawn controls; unpinned installed role | host supports pair; serving identity unknown |
| Phase 6 verification | alaa-verifier | balanced; exact deterministic commands | gpt-6-luna | medium | finite native gate list and explicit expected results; 2026-10-18 | explicit spawn controls; unpinned installed role | host supports pair; serving identity unknown |
| Phase 6 instruction review | alaa-instruction-reviewer | balanced; coupled cross-owner semantics | gpt-6.1-sol | high | lower bounded route rejected: interactions and missing exceptions remain open judgment rather than a known repair; current model-selection research/analysis guidance, 2026-10-18 | explicit spawn controls; unpinned installed role | host supports pair; serving identity unknown |

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership: original Phases 1-4 used one author. Phase 5 has the two disjoint lanes below; the parent alone owns workflow and evidence integration.
- Dependency edges and ready sets: Beads owns issue dependencies and readiness; the plan owns phase barriers and shared-resource conflicts.
- Disjoint writes and shared-resource conflicts: the stack lane owns `alaa-golang/SKILL.md`, its `references/63-tdd-and-testing-discipline.md`, and `alaa-quasar-app-vite-v3/references/75-testing-ci-playbook.md`. The paired lane owns both orchestrators' `assets/implementation-contract.md`, `references/resource-policy.md`, and generator-owned profiles/manifests, plus only the consumer-test review check and reset-safe setup sentence in `alaa-testing-strategy/references/90-test-economy.md`. Paths are under `skills/sohrab/`. No lane writes workflow files or mutates Beads.
- Phase 5 generators run only in the paired lane. Phase 6 begins after both lanes stop writing; no CPU-heavy commands overlap. Only invalidated evidence is repeated after a review fix.
- Integration barriers and parallel/serialized rationale: Phase 1 before 2 and 3; Phase 4 after both.
- Consolidated tasks/checks and preserved outcome/evidence mappings: repository gates run once in Phase 4 on the final tree.
- Reusable evidence and invalidation conditions: a gate result is reusable until any file under `skills/sohrab/` changes.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.

## Execution Position

- Position owner: `docs/agents/20261018-094058_stack-neutral-test-economy-doctrine-state.md` (current phase, blockers, next action).

## Curation

- Final gate (2026-10-18): one knowledge card retained engagement-local (the TOML and phrase-lock traps above); not persisted to durable memory because the owning scripts report both failures directly. Rejected: the two-lane Laravel rule and the test-need decision, because the repository now owns both.

- Corrective-run final scan (2026-10-18): reviewed the six findings, reproductions, owner corrections, validation and independent verdict. Retained candidates: none. Cache validity, entrypoint linking, tag selection, test ownership and setup exceptions now belong to their canonical skills; duplicate memory rules were rejected. The Beads same-target edge rejection, Bash sandbox startup failure and verifier culture-sort mismatch remain local evidence, not fleet policy. No memory write or further promotion is required.

## Resolved decision

- 2026-10-18, user: SQLite exists only for when Postgres is unavailable; tests must not run twice. `alaa-cicd-laravel-postgres` SKILL.md and `references/10-gate-register.md` now run the suite once on Postgres, with SQLite only as the unreachable fallback.
