# Centralized phase test collection

The three requested skill sources now schedule centralized phase collection, one serialized repair lane, retesting, then Review. The same execution contract is mirrored across Codex and Claude; workflow owns planning fields and routes scheduling to that pair.

## Behavior and scope

- Complete safe independent checks after ordinary failures; retain exact failures and blocked checks.
- Treat fail-fast aggregate output as partial coverage and run uncovered required checks.
- Permit minimal early repair only when a failure blocks all or most remaining checks; resume collection without intermediate Review.
- Preserve focused feedback, independent evidence, retry budgets, safety limits, inherited final-only review and final-candidate proof.
- Update 22 source files: eight per orchestrator and six workflow files. See [source manifest](source-snapshot.json).
- Added source-contract regressions justify the checker growth. The draft was compressed by the implementation lane; review found no unintended weakening. These fixtures do not simulate live scheduling.

## Verification and review

See the [initial batch](verification/verification-report.md), [repair retest](verification/retest/retest-report.md), and [environment recovery](verification/retest/focused-selector-report.md).

Both pack validators, both standalone contract checks, lifecycle, fleet references and whitespace checks passed. Final checker self-tests passed 796 Codex and 739 Claude structural fixtures. Changed sources are UTF-8 without BOM and LF.

Workflow: initial sandbox invocation was blocked by temporary-directory permissions. The elevated full run reached 146 tests: 145 passed and one failed because the unchanged test used a C-drive fixture from the D-drive repository. Its focused same-drive TEMP/TMP retry passed. One intervening malformed selector ran zero tests and is recorded as failed invocation. No clean first-pass full-suite claim is made.

Global structure and index checks still report pre-existing Magfa metadata/index defects. Its tracked baseline file was verified; no Magfa edits were made. Follow-up: `alaa-xrc`. These global results are not passes and do not establish whole-pack readiness.

Independent instruction review: APPROVED, no findings. It inspected all changed policy/template seams against HEAD and confirmed mirrored behavior and compression fidelity. Parent correctness review of the checker additions found no actionable defect: required-source clauses, contradiction rejection, mutation isolation, invocation and error handling remain consistent with the existing checker. Separate documentation work is inapplicable because skill text is the changed product; source structure/reference checks and instruction review cover it.

## Identity and limits

HEAD: `2ddd92880730458480207d414d53828107a06335`. Scoped SHA-256: `e00ecfd229ad93e80eb91a424c85e9fec02b07cdd91f4e35ed1140ee18512563`. Source scope was frozen during verification and review; no installation or live scheduling compliance was tested.

- IMPLEMENTED: proven for the scoped local source change.
- MERGE_CANDIDATE: not proven for the entire pack; global Magfa checks remain failed.
- RELEASE_CANDIDATE: not requested.
- PUBLISHED: not requested.

The work is uncommitted. Commit, push, installation and remote sync were not authorized or performed. Beads task `alaa-3l0` owns task status; workspace-gate access warnings occurred, successful mutations were read back, and exclusive filesystem locking was not established.

Curation: no additional admitted memory candidate. The user's requested behavior now resides in its canonical skills; copying it into memory would duplicate that owner. No memory write was performed.

## Lane accounting

Three agents were dispatched: batch_contract (alaa-implementer, gpt-6.1-sol/medium), central_verification (alaa-verifier, gpt-6-luna/medium), instruction_review (alaa-instruction-reviewer, gpt-6.1-sol/medium). These are requested controls; observed serving identities and session token totals are unknown. Follow-ups reused the same lanes. Plan-created-to-authorized-commit span: unavailable (issue-only work, no commit).
