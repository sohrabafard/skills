# Retest result

Overall: PARTIAL — 6 PASS, 1 PRODUCT-FAILURE. Tier: affected. All six passes establish level 1 (static) proof. The workflow unittest ran 146 tests and reached behavioral assertions; one failed. The original sandbox attempt remains separately classified ENVIRONMENT-BLOCKED and was not rerun in place. The authorized elevated execution was a distinct recovery attempt, not flake detection.

| # | Command | Duration | Exit | Classification | Tier / proof |
|---|---|---:|---:|---|---|
| 1 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py` | 0.313s | 0 | PASS | affected / 1 static |
| 2 | `python -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py` | 0.221s | 0 | PASS | affected / 1 static |
| 3 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py --self-test` | 11.914s | 0 | PASS | affected / 1 static |
| 4 | `python -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py --self-test` | 11.190s | 0 | PASS | affected / 1 static |
| 5 | `python -B scripts/check_fleet_references.py` | 3.423s | 0 | PASS | affected / 1 static |
| 6 | `git diff --check` | 0.107s | 0 | PASS | affected / 1 static |
| 7 | `python -B -m unittest discover -s skills/sohrab/alaa-workflow/tests -p test_workflow_files.py` | 94.860s | 1 | PRODUCT-FAILURE | affected / behavioral test execution; no proof claim passed |

Commands 1–5 used `PYTHONDONTWRITEBYTECODE=1`; command 6 had no override. All ran from `D:\Sohrab\Project\skills`, sequentially with one process, default priority and affinity. Command 7 used the same environment and exact command under the explicitly authorized elevated execution after the original sandbox attempt failed at temporary-directory creation. Timeouts: 120 seconds for commands 1–6; 180 seconds for command 7. No CPU-heavy command was declared.

Failure: command 7 ran 146 tests and failed only `TaskStoreCliTest.test_no_tracker_or_network_operations` at `test_workflow_files.py:1307`; expected `module.main()` to return 0, observed 2. Captured output includes `MISUSE: Approved design cannot be represented by a portable relative path from this repository.` See `07-workflow-unittest.log`. The earlier run's 231 `WinError 5` temporary child-directory errors are preserved in the parent verification folder's `11.log`; that result remains ENVIRONMENT-BLOCKED, separate from this failure.

Initial HEAD: `2ddd92880730458480207d414d53828107a06335`. The 22 pre-existing modified source paths have matching initial/final SHA-256 values; no source contamination was observed. Initial/final repository status and manifests are beside this report. The only additional untracked paths are the authorized verification artifacts.

Cumulative dispatched coverage: the original run remains 9 PASS, 2 PRODUCT-FAILURE, 1 ENVIRONMENT-BLOCKED; the two failures are the baseline `alaa-sms-provider-magfa` structural and index findings, outside this retest scope. Unchanged pack validators and lifecycle check remain cited from the original run. Retest adds 6 PASS and 1 PRODUCT-FAILURE. Do not combine the original sandbox blocker and elevated behavioral failure into a flaky result. No checks beyond the dispatches were run.

Task controls: requested `gpt-6-luna / medium`; configured role pair, observed serving identity, and effective-control match are not independently observable here.
