# Workflow Plan - Selected normalization and Arvan skill corrections

- Task ID: `20260925-143542_normalization-arvan-selected-fixes`
- Mode: `execute`
- Profile: `resumable`
- Status: completed
- Created: `2026-09-25T14:35:42Z`
- Parent plan: not created
- Prompt pack: `docs/_agent_plans/20260925-143542_normalization-arvan-selected-fixes__phase-prompts.md`
- Checkpoint: `docs/agents/20260925-143542_normalization-arvan-selected-fixes-state.md`
- Machine state: not created
- Base branch and commit: `main`, `34aeb11db38e1408b1760d9fe3f4c1fec16d0498`
- Work branch: main retained; disjoint ownership is clear and integration is not requested. No commit authority.
- Worktree: repository root; no separate checkout created.

## Summary and Outcome

Correct only the approved F01 invocation and F11 normalization documentation/example defects. The execution prompt has been submitted and scoped local implementation is authorized. Installation and external effects remain excluded.

The current three defects remain visible: caas-arvan-kuber/SKILL.md:76 uses an invalid Python script path; input-normalization contract lines 52-56 and property 4 at line 107 incorrectly imply length preservation through NFC; the Laravel middleware example calls an undefined fieldName method at line 47. Line numbers are discovery aids; re-find the actual text before editing.

The tracked tree was clean at planning intake. HEAD and branch differ from the historical audit. Both migration checkpoints now report local source completion; Claude activation, account availability and calibration are still unproven. No migration is reopened by this plan.

## Selection and authority

- Approved for this plan: F01, only the Arvan checker invocation; F11, only NFC length wording and the incomplete Laravel middleware example.
- Explicitly not selected for now: F02 service-runtime-kit-governance and F04 alaa-permission-generator. This is a scope decision, not a finding reversal.
- Deferred: every other audit item and wave, including queue semantics, provider evidence refresh, router consolidation, version ledgers and installed-role remediation.
- No model/effort policy or agent definition changes are selected. Before/after model-effort mapping: not applicable.
- No benchmarks or live model evaluations are selected; no quality, speed or cost gain is claimed.

## Scope

Implementation write roots are exclusively:
1. `skills/sohrab/alaa-input-normalization/`: primarily `references/10-normalization-contract.md` and `references/30-backend-middleware-binding.md`.
2. `skills/sohrab/caas-arvan-kuber/`: primarily `SKILL.md`.

Narrow supporting example fixtures or tests inside the same selected roots are allowed only if needed to prove the repaired example. Do not change canonical normalization implementations, existing corpus expectations or checksums just to fix prose. If a true runtime defect would require such changes, stop that affected scope for a new decision; do not silently expand.

The lead alone may update this workflow family and retain task evidence under `artifacts/normalization-arvan-selected-fixes/`. These are workflow/evidence companions, not additional skills selected for modernization.

Read-only dependencies include alaa-k8s-helm's checker, prompting-guide, testing-strategy and relevant Laravel/Unicode sources. No changes to those skills, root instructions/indexes/scripts/install docs, vendor, generated agent metadata, dependencies, application consumers, global configuration or installed copies. Do not access a live cluster or provider for a documentation command repair.

Commit, stage unrelated work, merge, push, tag, publication, deployment, installation, tool upgrade, destructive cleanup, credential work and global changes are not authorized. No memory write is selected. Preserve unrelated files and existing indexes.

## Handoff Package

- Confirmed facts (verified, each with how it was verified): targeted source reads at current HEAD confirmed all three defects. alaa-k8s-helm/scripts/check_manifests.py accepts --profile arvan and --self-test; its self-test needs no cluster/network. The existing normalization corpus has an NFC composition case, and the Python reference checks length relative to NFC(input). Historical agent-observed Python self-test passed 145 cases times two modes; it is not current integrated or four-runtime proof. Current Claude checkpoint reports completed source work, not activation.
- Open assumptions (believed but unverified, each with what would verify it): installed PHP/framework/autoload and all four normalization runtimes are not proven; inspect available tools without installing. Effective role grants/activation remain unknown until the target host exposes evidence. Exact nested typed-field interpretation must be derived from the current skill/corpus/framework; do not broaden leaf-name matching by guess.
- Ruled out (approach, reason, evidence): removing NFC to preserve length changes behavior; loosening/regenerating corpus destroys evidence; editing alaa-k8s-helm merely to compensate for a wrong caller command expands scope; copying framework traversal into an ad hoc implementation duplicates responsibility; updating an entire skill or version ledger goes beyond selection.
- Read first on resume (ordered exact paths): this plan, its checkpoint, applicable AGENTS.md, selected SKILL.md files and all their references/scripts as required by repository instructions, then the exact read-only dependency relevant to the chosen correction. Treat Arvan OpenAPI as machine-readable: use its authorized summarizer only; do not dump/read the large JSON directly.
- Environment notes (command shapes that work here, and ones that look right but fail): PowerShell is available; set process priority BelowNormal and use python -B. The historical Python reference command was run from repository root. The invalid Arvan form gives Python a skill-name token instead of a script file. Resolve a skill root and quote the full script path, without embedding a machine path or assuming an undocumented cwd.
- Traps (looks correct, is not): NFC can change code-point length, in both directions for some Unicode inputs; distinguish the digit-fold operation from the complete text pipeline. A passing Python test does not prove other languages or middleware integration. A stub PHP base class or php -l alone cannot prove Laravel traversal. A passing Arvan fixture is not live-cluster compatibility. Historical audit line numbers have shifted.

## Acceptance criteria

1. NFC remains enabled; Nd-only folding, text/typed split, value-only traversal, total/idempotent behavior, before-validation placement and corpus authority survive.
2. Every affected length assertion describes the existing canonical implementation accurately, relative to the appropriate normalized baseline. Do not introduce an unproved blanket NFC length claim.
3. The Laravel example has no unresolved helper and clearly handles its documented typed-field opt-in semantics, nested arrays and non-string preservation using the actual TransformsRequest contract. Preserve query/form/JSON behavior; define supported example assumptions. Any ambiguity that changes which fields use typed mode is a material decision, not an excuse for scope expansion.
4. The Arvan command resolves the real read-only alaa-k8s-helm checker, quotes paths safely, preserves rendered.yaml and --profile arvan, and preserves exit 0/1/2 semantics. A missing dependency gives an explicit stop, never an invented path or false pass.
5. Arvan live-discovery precedence, RBAC, resource parity, Secret handling and deployment authority stay unchanged.
6. No excluded skill or unrelated artifact changes. All prose saved in English; one repository call form where applicable, without opening unrelated files to sweep legacy forms.
7. Required native checks and independent review are recorded against a held content snapshot. Any unavailable runtime proof is explicitly blocked/unproven rather than a pass.

## Ordered Work

### Phase 1 - Revalidate and dispatch

- Status: completed
- Depends on: none
- Owned scope: lead-owned workflow and evidence only.
- Excluded from this phase: implementation and external effects.
- Work:
  - [x] Re-read instructions, plan and checkpoint; inspect branch, HEAD, tracked and untracked state; preserve unrelated work.
  - [x] Confirm selected defects still exist; if already fixed, record no-change evidence instead of redoing.
  - [x] Inspect installed roles and effective permissions, revalidate official runtime/skill syntax and Laravel facts only where they control a selected decision.
  - [x] Read selected skills under their full-contract rule; finalize focused proof and disjoint dispatches.
- Acceptance criteria: current identity, scope and necessary roles/evidence are known; only affected work pauses on material drift.
- Validation commands: git status --short; git rev-parse HEAD; targeted native source/config reads.
- Evidence observed: execution preflight recorded in artifacts/normalization-arvan-selected-fixes/preflight.md; baseline.json pins the pre-write selected content.
- Snapshot: HEAD 34aeb11db38e1408b1760d9fe3f4c1fec16d0498; SHA-256 0177491480002b3bcf9e5bb1083926ed73d7a169aa7b5fa707eb78a459ed6695; paths skills/sohrab/alaa-input-normalization/ and skills/sohrab/caas-arvan-kuber/; baseline.json records the pre-write manifest.

### Phase 2 - Implement two bounded lanes

- Status: completed
- Depends on: Phase 1
- Owned scope: lane N owns alaa-input-normalization; lane A owns caas-arvan-kuber.
- Excluded from this phase: all other skills; shared workflow writes by children.
- Work:
  - [x] Lane N corrects the length prose and complete Laravel example, with minimal relevant validation.
  - [x] Lane A corrects only the checker invocation and its immediate path-resolution explanation.
  - [x] Each lane applies prompting-guide draft-then-compress equivalence; report intentional wording corrections and preserved behavior.
- Acceptance criteria: criteria 1-6 satisfied; only owned files change.
- Validation commands: commands in Validation Matrix, focused subset per lane.
- Evidence observed: completed; exact commands, proof levels and results are indexed in artifacts/normalization-arvan-selected-fixes/result.md.
- Snapshot: HEAD 34aeb11db38e1408b1760d9fe3f4c1fec16d0498; SHA-256 a2d7a00ab1420afbbfc8fd36bd1504a83a22929a53252c343a384d14c66982ff; paths selected skill roots and checker/script inputs listed in held-snapshot-v1.json; canonical assets/corpus unchanged.

### Phase 3 - Independently verify, review and hand off

- Status: completed
- Depends on: Phase 2
- Owned scope: independent verification/review; lead serializes workflow and evidence.
- Excluded from this phase: reviewer fixes, scope expansion, installation, commit/integration.
- Work:
  - [x] Freeze selected files; independent verifier runs the integrated affected checks once.
  - [x] Independent correctness and instruction review inspect the real combined diff, preserved exceptions and runtime-proof limits.
  - [x] Reconcile findings through the owning lane, with bounded fix cycles; rerun only checks whose inputs changed.
  - [x] Align affected documentation in the selected files, record its grade through the owner, complete final scope and snapshot inspection, and update this workflow.
- Acceptance criteria: no unresolved blocker/major findings; checks and evidence meet acceptance criteria; minor/out-of-scope findings reported without automatic expansion.
- Validation commands: complete Validation Matrix and final scope/snapshot checks.
- Evidence observed: completed; exact commands, proof levels and results are indexed in artifacts/normalization-arvan-selected-fixes/result.md.
- Snapshot: HEAD 34aeb11db38e1408b1760d9fe3f4c1fec16d0498; SHA-256 93adc14f11bf9daf79881014dc5803437f21ca88c9d3dbd3c17cc38b6e56a5b9; paths selected skill roots and checker/script inputs listed in held-snapshot.json; uncommitted content included.

## Validation Matrix

All commands below run from repository root; inspect exact --help/requirements before execution. Exit 2 means unavailable proof.

- Lane N focused: `python -B skills/sohrab/alaa-input-normalization/assets/input-normalization/normalize_reference.py --self-test`. Include the existing decomposed-accent corpus case and verify the corrected prose against the implementation's normalized-baseline assertion; do not alter its expectations.
- Laravel example: syntax-check the complete extracted snippet using installed PHP. Exercise it against an already available real supported Laravel TransformsRequest/autoload using top-level and nested typed/text fields, JSON/form/query input, non-strings, digit folding and NFC composition. Record exact framework version and commands in evidence. A hand-made parent stub, syntax-only check or source inspection is a lower proof level and cannot be labelled runtime integration. If a real framework environment is unavailable, stop that affected proof; request no installation until the blocker and concrete target are known.
- Four-runtime harness: `bash skills/sohrab/alaa-input-normalization/scripts/normalization-conformance.sh` only when needed by the selected change or governing skill; inspect its invocation and runtime discovery first. With no canonical implementation/corpus changes, do not claim fresh four-runtime parity from a documentation repair; cite existing bound evidence or label it unrun. Any skipped runtime stays unproved. Canonical implementation changes are outside this plan.
- Lane A focused: `python -B skills/sohrab/alaa-k8s-helm/scripts/check_manifests.py --self-test`. Also execute the repaired invocation against safe local valid and invalid fixtures with --profile arvan; demonstrate dispatch/path correctness and rejection without contacting a cluster or editing the checker.
- Integrated source: `python -B scripts/validate_sohrab_skill_pack.py`; `python -B scripts/check_skill_index.py`; `python -B scripts/check_fleet_references.py`; `python -B scripts/check_lifecycle_contract.py`; `git diff --check`.
- Workflow: `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-143542_normalization-arvan-selected-fixes.md`.
- Review proof: read-only independent artifact review and instruction-equivalence review. Trigger further specialists only for an actual new risk; do not substitute review for runtime evidence.

Source conformance, runtime example execution, installed activation and measured quality are separate evidence levels. No installation/activation claim or live quality/cost comparison is required or authorized. Preservation scenarios above evaluate instruction fidelity; they are not model benchmarks.

## Delegation and resources

Use standard orchestration: two disjoint implementation lanes, independent verifier, one correctness reviewer, and instruction reviewer because skills are executable instructions. The exact policy-selected profiles and current availability are resolved in the prompt pack and rechecked at dispatch; no agent definitions are changed.

The lead does not implement skill content. Both implementation lanes may run concurrently only within the host capacity; reserve independent gates for the frozen result. Shared workflow files, evidence index and final reconciliation are lead-only and serialized. No overlapping writes; reviewers never fix and implementers never approve their own work.

Use BelowNormal on Windows, bounded commands/output, at most two active implementation workers and one CPU-heavy check at a time. Preserve explicit browser settings if any relevant check uses them; no browser task is required here.

## Stop conditions and recovery

For a failed operation: at most one cause-specific repair and one materially different retry. At most two review/fix cycles. Preserve the failed result and diagnose environment versus product cause; never weaken a gate, regenerate a corpus for green, install a dependency or change unrelated code as recovery.

Stop only the affected lane for overlapping dirty changes, unavailable necessary role/runtime, material framework/contract drift, unresolved field-selection semantics, required broader implementation, failed mandatory proof or missing authority. Continue independent work where safe. Retain reversible uncommitted edits and exact next action; no automatic reset, stash, cleanup, branch deletion or commit.

Completion requires requested source corrections and proportional proof, independent verdicts, accurate workflow/evidence and explicit residual limits. Report the four lifecycle states through alaa-workflow; release and publication remain not requested.

## Blockers and Next Action

- Blockers: none in selected local correction scope. Literal-dot key adoption limit, excluded matrix/OpenAPI drift and activation/proof limits are recorded in the final result.
- Next action: inspect the reviewed local diff and evidence; no further action is authorized or required for this selected scope.

## Execution evidence

Preflight: `artifacts/normalization-arvan-selected-fixes/preflight.md`. Required role definitions match source; stale installation sentinel and unknown effective MCP isolation are recorded there. No installation or activation quality claim follows. Lanes N and A completed their scoped source/runtime work.

Initial held state before review fixes (superseded by the final snapshot below). Focused evidence: `artifacts/normalization-arvan-selected-fixes/normalization-evidence.md` and `artifacts/normalization-arvan-selected-fixes/arvan-evidence.md`. Held source/tool-input snapshot: `held-snapshot-v1.json`, digest `a2d7a00ab1420afbbfc8fd36bd1504a83a22929a53252c343a384d14c66982ff`. Literal Arvan shell passed outside sandbox after MSYS startup failure. An incidental unchanged matrix/OpenAPI mismatch is deferred, not passed. Real Laravel 13.23.0 middleware example executed; consumer installation and four-runtime parity remain unrun.

Correctness review cycle 1 requested three scoped normalization fixes; see `artifacts/normalization-arvan-selected-fixes/correctness-review-1.md`. Instruction review approved the original snapshot, but correctness found a framework dotted-key ambiguity and two minor contract issues. Evidence resolves the difference; original owner resolved them without broader traversal or rejection policy. Affected proof and both review verdicts were refreshed on the final hold.

## Final result

Completed reviewed local result: `artifacts/normalization-arvan-selected-fixes/result.md`. Independent correctness and instruction verdicts APPROVED after one scoped fix cycle; affected gates passed. IMPLEMENTED and MERGE_CANDIDATE proven for this pipeline; RELEASE_CANDIDATE and PUBLISHED not requested. No commit or installation. Final curation: no admitted durable candidate, no memory write.
