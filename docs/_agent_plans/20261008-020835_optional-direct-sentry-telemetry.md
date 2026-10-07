# Workflow Plan - Optional direct Sentry telemetry

- Task ID: `20261008-020835_optional-direct-sentry-telemetry`
- Mode: `orchestrator`
- Profile: `resumable`
- Status: completed
- Created: `2026-10-07T22:38:35Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261008-020835_optional-direct-sentry-telemetry-state.md`
- Machine state: not created
- Base branch and commit: `main`, `aa32353c7c38cf1700077f61d2f007128186f9de`
- Work branch: current `main` checkout; user follow-up authorizes commit and push to configured `origin/main` on this same branch. Parent owns staging, commit and push; no branch creation or merge/rebase requested.
- Worktree: repository root (`.`)
- Execution profile: lean; one settled prose lane, parent correctness review, independent verifier and delegated instruction-review specialist

## Summary and Outcome

- Baseline repository truth: SOC references 10/50/60 prohibited or gated a second Sentry telemetry path; 30 gated duplicate tracing. Contract 21 defaulted application OTLP to the central Collector, contradicting SOC 50's co-located Vector topology. The frozen five-reference patch resolves those statements.
- Outcome: permit optional direct Sentry SDK logs/traces beside the preserved application -> Vector -> Collector path, including simultaneous delivery and duplicates. Sensitive-environment operators disable direct Sentry logs/traces while retaining Sentry exceptions and the platform path.
- Strategy: policy in SOC 60, topology in SOC 50, rates in SOC 30, endpoint names/values in services-contract 21; secondary statements become owner pointers. Apply draft -> compressed rewrite with behavior-equivalence review.

## Scope

- In scope: five references listed under Phase B; this plan, checkpoint, endpoint drift decision record and scoped evidence under `outputs/20261008-optional-direct-sentry-telemetry/`.
- Out of scope: service repositories, SDK integration, Vector/Collector configuration, vendor files, dependencies, installed roles, model policy, secrets, release, deployment and runtime effects. Commit/push delivery is now separately authorized for the parent; this write lane does not perform it.
- Constraints: preserve existing privacy, fail-open, exception-capture, numeric tracing/profiling defaults and ceilings. No new direct-log/trace filtering or data-inspection gate, duplication approval or backend ban. No invented Vector DNS or claim of live service conformance.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. Field semantics are in `alaa-workflow references/context-continuity.md`, which is in the skill, not in this repository.

- Confirmed facts: user ratified optional direct SDK logs/traces, duplicate delivery, sensitive-environment disablement and no new inspection/filter gate on 2026-10-08. Native reads verified five policy contradictions and endpoint drift; both affected skills contain no scripts. Parent selected native prose/file/Git evidence. Initial tracked diff empty on the base above. Intermediate curation places this decision in canonical skills; no durable memory write authorized.
- Open assumptions: live SDK support and deployment conformance unverified; neither is asserted by this prose-only change. Installed role pins/declarations match shipped source per parent inspection; observed runtime identity and enforcement remain unknown.
- Ruled out: runtime/config edits exceed scope; new filtering gates contradict user intent; a blanket Sentry backend ban contradicts permitted duplicate delivery; copied topology or policy recreates drift; inventing deployment DNS has no source.
- Read first on resume: this plan, its checkpoint, `docs/drift/20261008-optional-direct-sentry-telemetry.md`, SOC `references/60-sentry-and-profiling.md` and contract `references/21-alaa-platform-observability-directive.md`.
- Environment notes: workflow initializer requires `YYYYMMDD-HHMMSS`; date-only `20261008` returned exit 2 and wrote nothing. One cause-specific retry with the valid stem succeeded. Python available. Retired inaccessible scratch directories outside scope. Hindsight unavailable per parent; recall is not proof and no durable memory writes occur. Three workflow/drift artifacts are staged; staging actor/time/reason unknown. The writer has no recorded staging action and the initializer contains no Git/staging behavior. Preserve the index; HEAD unchanged.
- Traps: contract 21's closing deployment bullets also prescribe the central endpoint; changing only its table leaves drift. SOC 30's head/tail rule must be scoped to the platform path. SOC 10's blanket second-backend ban must route to 60. July vendor capability claims in 60 remain dated and subject to its freshness caveat.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | skills/sohrab/alaa-workflow/SKILL.md | artifact admission, state and final gate | always | block |
| alaa-prompting-guide | skills/sohrab/alaa-prompting-guide/SKILL.md | instruction edits and compression | always | block |
| alaa-low-noise | skills/sohrab/alaa-low-noise/SKILL.md | bounded retrieval and lane return | always | block |
| alaa-observability-soc | skills/sohrab/alaa-observability-soc/SKILL.md | policy and topology decisions | always | block |
| alaa-services-contract | skills/sohrab/alaa-services-contract/SKILL.md | endpoint names and values | always | block |
| alaa-codex-orchestrator | skills/sohrab/alaa-codex-orchestrator/SKILL.md | parent dispatch and gates | always | block |
| alaa-code-intelligence-routing | skills/sohrab/alaa-code-intelligence-routing/SKILL.md | parent evidence selection | parent-only | block if source absent |
| alaa-memory-os | skills/sohrab/alaa-memory-os/SKILL.md | parent recall and persistence decisions | parent-only | source absent blocks; unavailable recall fails open |
| alaa-repo-docs | skills/sohrab/alaa-repo-docs/SKILL.md | atomic-file exemption classification | parent-only | block if source absent |
| alaa-testing-strategy | skills/sohrab/alaa-testing-strategy/SKILL.md | proof-level reporting | parent-only; conditional on reporting proof levels | missing source blocks proof classification |
| alaa-extract-agent-lessons | skills/sohrab/alaa-extract-agent-lessons/SKILL.md | final curation | final closure | block final closure |

## Ordered Work

### Phase A - Ground and plan

- Status: completed
- Depends on: none
- Owned scope: planning artifacts and drift record; parent decisions
- Excluded from this phase: source edits
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-observability-soc, alaa-services-contract, alaa-codex-orchestrator
- Work:
  - [x] Inspect relevant references, owner boundaries and current checkout; record user decision provenance. [skills: inherit]
  - [x] Save scoped plan/checkpoint and endpoint drift record. [skills: inherit]
  - [x] Parent inspects and presents plan before authorizing Phase B. [skills: inherit]
- Acceptance criteria: smallest settled approach and independent gates recorded; no skill source edited yet.
- Validation commands: `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261008-020835_optional-direct-sentry-telemetry.md`
- Evidence observed: initializer retry exit 0; workflow validator above exit 0, "Validation completed without blocking errors (profile: resumable)." Parent inspected and presented the plan, then authorized Phase B.
- Snapshot: reconciled at Phase B handoff; HEAD aa32353c7c38cf1700077f61d2f007128186f9de; SHA-256 9ab91e7dec7f4d948be91caa6201ab3205528d1561179bd4398512124c307e85; paths five-source candidate in `outputs/20261008-optional-direct-sentry-telemetry/implementation-evidence.md`. Phase A itself changed planning artifacts only.

### Phase B - Implement owning references

- Status: completed
- Depends on: Phase A and parent implementation authorization
- Owned scope: one `policy_implementation` lane; SOC `references/10-signal-model.md`, `30-quantitative-budgets.md`, `50-telemetry-pipeline.md`, `60-sentry-and-profiling.md`; services-contract `references/21-alaa-platform-observability-directive.md`
- Excluded from this phase: all other source files and runtime effects
- Required skills: alaa-workflow, alaa-prompting-guide, alaa-low-noise, alaa-observability-soc, alaa-services-contract
- Work:
  - [x] Finish complete affected-skill reads before source editing: both SKILL files, every reference and metadata read; neither skill contains scripts. [skills: inherit]
  - [x] Author the smallest five-reference patch and apply draft/compression equivalence. [skills: inherit]
  - [x] Inspect actual diff, numeric-rate preservation and ownership pointers. [skills: inherit]
- Acceptance criteria: direct Sentry logs/traces optional, concurrent duplicates allowed; sensitive operators retain exceptions/platform path while disabling direct logs/traces; no added filtering/inspection or duplication approval; privacy/fail-open unchanged; default same-namespace Vector endpoint loopback HTTP, deployment-supplied co-located Vector address for Compose/Swarm, central address only the existing no-local-process exception.
- Validation commands: focused `git diff --check -- <five source paths>` and workflow validator; broad gates reserved for Phase C.
- Evidence observed: five-source `git diff --check` exit 0; Git emitted only CRLF-to-LF normalization notices. Draft/compression review retains optionality, duplicates, sensitive-environment disablement, exceptions, platform path, privacy and lack of added inspection gates. Existing touched-file dual invocation forms converted under repository rules; no policy expansion. Parent's positional-bullet finding corrected to the explicit exception-coverage requirement. Workflow reconciliation validation required a scoped snapshot; one cause-specific repair supplied this manifest, retry exit 0: "Validation completed without blocking errors (profile: resumable)."
- Snapshot: HEAD aa32353c7c38cf1700077f61d2f007128186f9de; SHA-256 9ab91e7dec7f4d948be91caa6201ab3205528d1561179bd4398512124c307e85; paths five-source candidate in `outputs/20261008-optional-direct-sentry-telemetry/implementation-evidence.md`.

### Phase C - Independent verification

- Status: completed
- Depends on: Phase B; frozen five-reference candidate
- Owned scope: independent verifier evidence, no source edits
- Excluded from this phase: runtime/config validation and repeated unchanged gates
- Required skills: alaa-workflow, alaa-low-noise, alaa-codex-orchestrator
- Work:
  - [x] Run repository skill checks on the identified candidate and record exit codes. [skills: inherit]
- Acceptance criteria: each required skill gate exit 0; nonzero results classified, never reported as pass.
- Validation commands (repo root, affected tier, serial lightweight Python): `python scripts/validate_sohrab_skill_pack.py`; `python scripts/check_skill_index.py`; `python scripts/check_fleet_references.py`; `python scripts/check_lifecycle_contract.py`; orchestrator-directory `python scripts/check_agent_contracts.py` for instruction-contract changes.
- Evidence observed: cited independent `alaa-verifier` observation, configured gpt-6-luna/low, requested override none, observed identity unknown; all five gates PASS exit 0 at proof level 1 (static), affected tier. Evidence read from `outputs/20261008-optional-direct-sentry-telemetry/verification/verification.json` and its five logs; this lane ran no broad gates. Python 3.13.14; one process, serial, default priority, no affinity limit, timeout 120s, no environment overrides. Exact command evidence follows; cwd is expressed relative to this repository under repository path rules. Start timestamps were not separately captured; recorded durations are retained. Static proof establishes skill artifact contracts, not SDK/runtime/deployment behavior.

| Command | Cwd | Observed result | Duration (seconds) | Log under scoped verification directory |
|---|---|---|---|---|
| `python scripts/validate_sohrab_skill_pack.py` | `.` | PASS, exit 0; 69 skills; advisory body-length warnings | 0.417 | `validate_sohrab_skill_pack.log` |
| `python scripts/check_skill_index.py` | `.` | PASS, exit 0; 69 directories/index entries; findings none | 0.408 | `check_skill_index.log` |
| `python scripts/check_fleet_references.py` | `.` | PASS, exit 0; 69 skills, 1125 Markdown files, 4056 citations; findings none; informational target-repository paths | 5.241 | `check_fleet_references.log` |
| `python scripts/check_lifecycle_contract.py` | `.` | PASS, exit 0; four lifecycle states; findings none | 0.918 | `check_lifecycle_contract.log` |
| `python scripts/check_agent_contracts.py` | `skills/sohrab/alaa-codex-orchestrator` | PASS, exit 0; metadata, dispatch scope and independent verification authority | 0.491 | `check_agent_contracts.log` |

- Snapshot: verifier initial and final source digest unchanged; HEAD aa32353c7c38cf1700077f61d2f007128186f9de; SHA-256 9ab91e7dec7f4d948be91caa6201ab3205528d1561179bd4398512124c307e85; paths five-source candidate in verification JSON.
- Input reconciliation: read `outputs/20261008-optional-direct-sentry-telemetry/verification/checker-input-reconciliation.json`, observed 2026-10-07T22:48:01.0494139Z. Current five checker hashes and clean checker-input diff against HEAD corroborate unchanged inputs; execution-time checker hashes and per-command start/observation times were not captured. These later hashes do not supply retroactive timestamps or execution-time measurements. No checks rerun.

### Phase D - Independent review

- Status: completed
- Depends on: Phase C
- Owned scope: delegated instruction-review specialist plus parent correctness review; no reviewer edits
- Excluded from this phase: additional runtime specialists; no runtime, SDK or config change
- Required skills: alaa-prompting-guide, alaa-observability-soc, alaa-services-contract, alaa-low-noise, alaa-codex-orchestrator
- Work:
  - [x] Review five-reference semantics, agent authority, preserved invariants, routing ownership and compression fidelity. [skills: inherit]
  - [x] Reconcile findings through the original implementation lane; reopen only affected gates. [skills: inherit]
- Acceptance criteria: no unresolved actionable findings; user-requested independent delegated review observed.
- Validation commands: read-only source/diff review; no duplicated broad check run.
- Evidence observed: parent correctness review APPROVED after the positional-bullet correction; no unresolved parent finding. Delegated `independent_instruction_review` (`alaa-instruction-reviewer`, configured gpt-6-astra/high, requested override none, observed unknown) APPROVED with no findings and matched all five hashes. Review confirmed optional direct SDK logs/traces, concurrent duplicates, sensitive selective disablement, no new filtering/inspection/duplication approval, preserved privacy/fail-open/exception coverage/scope reset/profiling/rates and single owners. Live SDK/deployment behavior and unchanged July capability claims were not assessed. Actual workspace-write exposure exceeded the reviewer's declared read-only role; only native reads were used. Verdict supplied through parent dispatch; no separate duplicate review artifact created.
- Snapshot: HEAD aa32353c7c38cf1700077f61d2f007128186f9de; SHA-256 9ab91e7dec7f4d948be91caa6201ab3205528d1561179bd4398512124c307e85; paths same five-source candidate independently checked against the manifest.

### Phase E - Reconcile and close

- Status: completed
- Depends on: Phase D
- Owned scope: delegated workflow artifact updates, parent final synthesis
- Excluded from this phase: source edits, release/deployment, durable memory writes and unrequested external actions; authorized current-branch commit/push is parent-owned delivery.
- Required skills: alaa-workflow, alaa-low-noise, alaa-prompting-guide, alaa-extract-agent-lessons, alaa-codex-orchestrator
- Work:
  - [x] Reconcile evidence, doc grades, final scope and four lifecycle verdicts. [skills: inherit]
  - [x] Record full-engagement curation after stable proof; no competing memory copy of canonical skills. [skills: inherit]
  - [x] Validate final workflow artifact family before completion. [skills: inherit]
- Acceptance criteria: implementation/review/proof agree; final gate observed; all source and workflow changes explained.
- Validation commands: independent verifier runs `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261008-020835_optional-direct-sentry-telemetry.md`; final scoped Git inspection.
- Evidence observed: independent `alaa-verifier` preclosure command `python skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261008-020835_optional-direct-sentry-telemetry.md`, cwd repository root, observed 2026-10-07T22:50:31.7845954Z, duration 0.267s, PASS exit 0: "Validation completed without blocking errors (profile: resumable)." One lightweight process, serial/default priority, no affinity limit, timeout 120s, no environment overrides; proof level 1/static. Evidence `outputs/20261008-optional-direct-sentry-telemetry/verification/workflow-preclosure.json` and `.log` recorded stable source/artifact/tool hashes and unchanged HEAD. Phase C root gates remain unchanged cited results owned by the verifier, with old per-command times unknown; none rerun. Source documents graded EXEMPT-ATOMIC under repo-docs; plan/checkpoint/drift are named-artifact exemptions. Parent's full-engagement curation under `/alaa-extract-agent-lessons` completed with no additional admitted candidates: user policy is promoted into its canonical owning skill; competing memory copy rejected as cheaply recoverable. No durable memory writes authorized or performed; Hindsight absent; no pipeline reopen.
- Snapshot: HEAD aa32353c7c38cf1700077f61d2f007128186f9de; SHA-256 9ab91e7dec7f4d948be91caa6201ab3205528d1561179bd4398512124c307e85; paths five-source candidate preserved. Immutable preclosure and final evidence in `outputs/20261008-optional-direct-sentry-telemetry/verification/` retain per-invocation artifact/tool hashes and times; this status correction does not rewrite those observations.
- Final validation observed: independent verifier ran the same workflow command at repository root, PASS exit 0 at 2026-10-07T22:51:48.5145802Z, duration 0.244s, proof level 1/static: "Validation completed without blocking errors (profile: resumable)." HEAD, source and invocation artifact hashes stayed stable. Evidence `outputs/20261008-optional-direct-sentry-telemetry/verification/workflow-final.json` and `workflow-final.log` is immutable. Completion fully observed; no validation hold remains. A later status-reconciliation check may write `workflow-stable.json`/`workflow-stable.log` in that directory; no result is asserted for it here.

Lifecycle verdicts use `/alaa-workflow`, `references/workspace-and-integration.md`:

- IMPLEMENTED: proven for the frozen source digest by focused evidence, independent static gates and approved reviews.
- MERGE_CANDIDATE: proven by completed source gates/reviews and observed independent final workflow validation exit 0.
- RELEASE_CANDIDATE: not requested; runtime/deployment proof is outside scope.
- PUBLISHED: Git delivery now authorized by the user's follow-up, but not proven in this serialized pre-delivery state. Actual commit/ref and push evidence is authoritative for the delivery outcome; no future publication is asserted and no second documentation commit is needed to mirror that evidence. Release/deployment remain unrequested.

## Delegation

- Parent leads without file edits. `policy_implementation` owns the only source write lane and workflow artifacts; independent verifier and instruction reviewer own their evidence. No overlapping concurrent writes.
- Implementer admission: precise ratified user policy and settled endpoint mapping; no unresolved substantive design. Configured `alaa-implementer` pin: gpt-6.1-sol/high; requested override none; observed identity unknown.
- Parent reports availability/version/enforcement evidence, independent verdicts and final lifecycle/accounting; lanes never approve themselves.
- Skill source documents: EXEMPT-ATOMIC per parent repo-docs owner; plan/checkpoint/drift are named-artifact exemptions. No extra documentation lane needed for prose source changes.

## Blockers and Next Action

- Blockers: none. Staging provenance remains unknown and the index is preserved.
- Next action: source work complete; parent delivers the authorized commit/push on current `main` to configured `origin/main`. Source skill checks and reviews remain unchanged. Delivery outcome is established by actual Git commit/ref evidence; this artifact does not predict it. Workflow artifacts freeze after this authority update.
