# Central verification result

Overall: PARTIAL — 9 PASS, 2 PRODUCT-FAILURE, 1 ENVIRONMENT-BLOCKED. No command was rerun. Tier: affected. Proof level for successful repository/static checks: 1 (static); no runtime compliance proof.

| # | Command | Duration | Exit | Classification | Tier / proof |
|---|---|---:|---:|---|---|
| 1 | `python -B scripts/validate_sohrab_skill_pack.py` | 1.011s | 1 | PRODUCT-FAILURE | affected / none |
| 2 | `python -B scripts/check_skill_index.py` | 0.527s | 1 | PRODUCT-FAILURE | affected / none |
| 3 | `python -B scripts/check_fleet_references.py` | 11.901s | 0 | PASS | affected / 1 static |
| 4 | `python -B scripts/check_lifecycle_contract.py` | 0.816s | 0 | PASS | affected / 1 static |
| 5 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py` | 1.427s | 0 | PASS | affected / 1 static |
| 6 | `python -B skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py` | 1.025s | 0 | PASS | affected / 1 static |
| 7 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py` | 0.481s | 0 | PASS | affected / 1 static |
| 8 | `python -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py` | 0.468s | 0 | PASS | affected / 1 static |
| 9 | `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py --self-test` | 9.413s | 0 | PASS | affected / 1 static |
| 10 | `python -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py --self-test` | 9.155s | 0 | PASS | affected / 1 static |
| 11 | `python -B -m unittest discover -s skills/sohrab/alaa-workflow/tests -p test_workflow_files.py` | 1.228s | 1 | ENVIRONMENT-BLOCKED | affected / none |
| 12 | `git diff --check` | 0.446s | 0 | PASS | affected / 1 static |

All commands ran from `D:\Sohrab\Project\skills`, sequentially, one process at a time, with default process priority and affinity. Commands 1–11 used `PYTHONDONTWRITEBYTECODE=1`; command 12 had no override. Timeout was 120 seconds except command 11 at 180 seconds. No CPU-heavy command was declared.

Failures:

- Command 1 reports `alaa-sms-provider-magfa` missing a `When not to use` / `Do not use` section and missing `agents/openai.yaml`. Command 2 reports the skill absent from both skill indexes and also missing `agents/openai.yaml`. Full output: `01.log`, `02.log`.
- Command 11 ran 146 tests and reported 231 errors. The repeated exception is `PermissionError: [WinError 5] Access is denied` while test helper `workspace_tempdir()` calls `path.mkdir()` under `C:\Users\Alaa\AppData\Local\Temp`. Classified ENVIRONMENT-BLOCKED; no rerun or workaround was authorized. Full output: `11.log`.

Repository state: initial HEAD `2ddd92880730458480207d414d53828107a06335`. The initial source manifest contains the 20 pre-existing modified source files. Their final SHA-256 values match the initial manifest; no tracked-source change or source contamination was observed. Final status additionally shows the verification artifact directory as untracked. Initial/final status: `initial-status.txt`, `final-status.txt`. Snapshots: `initial-source-manifest.json`, `final-source-manifest.json`.

Not run: no checks beyond the dispatched 12 commands. Model/effort requested by dispatch: `gpt-6-luna / medium`; configured role pair and observed serving identity are not independently observable here. Effective-control mismatch: unknown. Repository/runtime compliance, installed-skill behavior, and live behavior remain unverified.
