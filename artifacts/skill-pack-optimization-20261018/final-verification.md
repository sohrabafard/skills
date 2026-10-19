# Final verification

**Overall: FAIL.** Gate 1 failed on a missing referenced path. Gates 17 and 20 have no reliable exit evidence; neither is counted as passing. The other dispatched gates with observed exit codes passed.

Agent: `alaa-verifier`; configured controls: neutral/unpinned; requested: `gpt-6-luna` / `medium`; observed runtime identity: unknown. Effective sandbox: workspace-write. MCP enforcement evidence: unknown.

Repository: `main` at `1a0799de71254427973f1253d80b846fea9acf10`. Initial status had 385 rows; final status has 388, including this verification artifact. Frozen product inputs stayed unchanged, so the run is not contaminated.

| # | Command (full #18 path list is in the cited log artifact) | CWD | Duration | Exit | Result | Tier / proof |
|---:|---|---|---:|---:|---|---|
| 1 | `python -B scripts/validate_sohrab_skill_pack.py` | `.` | 0.344s | 1 | PRODUCT-FAILURE | affected / none |
| 2 | `python -B scripts/check_skill_index.py` | `.` | 0.228s | 0 | PASS | affected / L1 static |
| 3 | `python -B scripts/check_fleet_references.py` | `.` | 3.554s | 0 | PASS | affected / L1 static |
| 4 | `python -B scripts/check_lifecycle_contract.py` | `.` | 0.676s | 0 | PASS | affected / L1 static |
| 5 | workflow test suite via low-priority runner | `.` | 57.819s | 0 | PASS | exhaustive / L2 unit |
| 6 | `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20261018-000000_skill-pack-optimization.md` | `.` | 0.473s | 0 | PASS | affected / L1 static |
| 7-9 | Codex orchestrator contracts, self-test, pack validation | `skills/sohrab/alaa-codex-orchestrator` | recorded in JSON/logs | 0 | PASS | affected / L1 and L2 |
| 10-13 | CC orchestrator contracts, self-test, pack validation, self-test | `skills/sohrab/alaa-cc-orchestrator` | recorded in JSON/logs | 0 | PASS | affected / L1 and L2 |
| 14-15 | Docker pack validation, then self-test | `.` | 2.540s / 1.355s | 0 / 0 | PASS | affected / L1 and L2 |
| 16 | constitution validator | `.` | unavailable | 0 | PASS | affected / L1 static |
| 17 | `python -B artifacts/skill-pack-optimization-20261018/lanes/AUDIT-cli-assertion.py` | `.` | unavailable | unknown | SKIPPED: no reliable exit capture | not specified / none |
| 18 | Markdown link checker on 228 exact paths | `.` | 0.339s | 0 | PASS | affected / L1 static |
| 19 | change-notes link and line-budget check | `.` | unavailable | 0 | PASS | affected / L1 static |
| 20 | scoped `git diff --check` | `.` | unavailable | unknown | SKIPPED: wrapper failed before evidence capture | not specified / none |

Gate 1 output: `alaa-bale-provider` refers to missing `references/70-soc-evidence.md`. Gates 2-4 passed; the workflow suite passed 130 tests. The workflow-file validator emitted its expected offline-Beads warning, so it proves offline structure only. The Docker commands ran against the requested cached immutable image with network disabled.

Integrity assertions matched all 2,238 product file hashes and aggregate SHA-256; the 10 unrelated hashes and their cached index entries; three designated zero-byte reports; the Bash topic-map SHA-256; and UTF-8 without BOM with LF for 374 owned text files. Proposal coverage was 124/124 with 27 implemented, 90 adapted, and 7 rejected. No tracked skills were deleted.

The exact argv path list for gate 18, command logs, initial/final status, corrected integrity assertions, and the preserved flawed probe are under `final-verification-logs/`. No installed, live application, live Beads, or performance behavior is established by these static checks.
