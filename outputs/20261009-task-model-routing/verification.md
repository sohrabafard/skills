# Independent verification

**Overall status: PASS WITH ENVIRONMENT RECOVERY.** Final-tree aggregate, preflight, and whitespace gates pass. The workflow suite passed after an authorized temp-path permission recovery; Git Bash passed after an authorized sandbox IPC recovery. Early source and citation failures are retained below as superseded-candidate evidence.

- **AGENT:** alaa-verifier
- **CONFIGURED:** gpt-6-luna / low
- **REQUESTED:** not specified
- **OBSERVED:** unknown
- **Authority:** workspace-write sandbox plus repository/cache write roots; narrow escalation accepted for the two recovery runs. Separate MCP grant enforcement is unknown.

Commands ran sequentially with `python -B` and `PYTHONDONTWRITEBYTECODE=1`; no CPU-heavy command was dispatched. PowerShell lacked `Start-Process -PriorityClass`, so lightweight checks ran at normal priority without explicit affinity or parallel workers. `CACHE_ROOT` denotes the authorized scratch root. Raw stdout/stderr and machine timestamps are retained in linked logs and JSON records.

| Command | CWD | Limits | Duration | Exit | Classification; tier; proof | Evidence |
|---|---|---|---:|---:|---|---|
| Codex `scripts\validate_pack.py` | `skills/sohrab/alaa-codex-orchestrator` | sequential, normal | .402s | 0 | PASS; affected; 1 static | `final-codex-validate-pack.*` |
| Codex `scripts\check_agent_contracts.py` | same | sequential, normal | .118s | 0 | PASS; affected; 1 static | `final-codex-check-agent-contracts.*` |
| Claude `scripts\validate_pack.py` | `skills/sohrab/alaa-cc-orchestrator` | sequential, normal | .545s | 0 | PASS; affected; 1 static | `final-claude-validate-pack.*` |
| Claude `scripts\check_agent_contracts.py` | same | sequential, normal | .121s | 0 | PASS; affected; 1 static | `final-claude-check-agent-contracts.*` |
| Prompting grants, Codex evals, Claude evals | `skills/sohrab/alaa-prompting-guide` | sequential, normal | .363/.157/.199s | 0 each | PASS; affected; 1 static | `rule-writer-grants.*`, `codex-agent-evals.*`, `claude-agent-evals.*` |
| `profile_projection.py --self-test` | same | sequential, normal | .491s | 0 | PASS; affected; 2 unit | `profile-projection-self-test.*` |
| Workflow `python -B -m unittest discover -s tests` (sandbox; temp at `CACHE_ROOT`) | `skills/sohrab/alaa-workflow` | sequential, normal | .677s | 1 | ENVIRONMENT-BLOCKED; affected; none | `workflow-suite.*` |
| Same workflow command (escalated) | same | sequential, normal | 15.572s | 0 | PASS; affected; 2 unit | `workflow-suite-escalated.*` |
| Installer preflight, PowerShell and Bash (superseded source) | `skills/sohrab/alaa-codex-orchestrator` | sequential, normal | 1.883/.365s | 2 each | PRODUCT-FAILURE; affected; proof unavailable | `install-preflight-powershell.*`, `install-preflight-bash.*` |
| Final PowerShell installer preflight | same | sequential; fresh scratch | 11.349s | 0 | PASS; affected; 4 local process smoke | `final-install-preflight-powershell.*` |
| Final Bash installer preflight (sandbox) | same | sequential; fresh scratch | .667s | 2 | ENVIRONMENT-BLOCKED; affected; none | `final-install-preflight-bash.*` |
| Same Bash preflight (escalated; fresh scratch) | same | sequential | 6.632s | 0 | PASS; affected; 4 local process smoke | `final-install-preflight-bash-escalated.*` |
| Root skill-pack validator, skill index, lifecycle contract | `.` | sequential, normal | .239/.149/.367s | 0 each | PASS; affected; 1 static | `root-validate-skill-pack.*`, `root-check-skill-index.*`, `root-check-lifecycle-contract.*` |
| Fleet references (before citation repair) | `.` | sequential, normal | 2.592s | 1 | PRODUCT-FAILURE; affected; 1 static | `root-check-fleet-references.*` |
| Fleet references (final tree) | `.` | sequential, normal | 2.633s | 0 | PASS; affected; 1 static | `final-root-fleet-references.*` |
| `git -c core.safecrlf=false diff --check -- AGENTS.md skills/sohrab` (final tree) | `.` | sequential, normal | .115s | 0 | PASS; affected; 1 static | `final-scoped-diff-check.*` |

The workflow sandbox attempt ran 81 tests but reported 92 errors from `PermissionError: [WinError 5]` creating temp directories; the escalated run passed all 81. The superseded installer runs exited 2 because the copied validator could not import `profile_projection`; the loader was repaired, and final PowerShell/Bash preflights each passed nine negative paths with synthetic destinations untouched. The final sandbox Bash attempt failed before installer invocation with `CreateFileMapping ... Win32 error 5`; the escalated run passed. The early fleet check found three workflow citations; the final check found none. Its 315 unmarked repository paths were informational.

Initial HEAD: `85532a8dd1be46eb226537377899523ddc998039` (`main`). Initial/final status captures had 139/141 entries; the difference includes this archive. Existing Git scan warnings for 26 `_to_delete/.../workflow-test-temp-artifacts` directories were captured and left untouched. Final source inventory: 138 changed paths, hash `3cfb58ae03e654fae65a158676b6df5f7f74245a928264e2f9dc12c0bba4d9c7`. The 153-file orchestrator/workflow snapshot hashes to `db68bab1fbdf4effc7562c7132fcee97df6e4ff530cc30e6e5a2ac9bdc2bd3a0`, matching the writer's freeze. No verifier source edits or contamination occurred.

No dispatched check was skipped; no live model calls, real-target installs, commits, or global setting changes occurred. Parent-owned final Markdown-link and workflow-artifact gates are not claimed here. See `source-final.json`, `verification-initial-status.txt`, `verification-final-status.txt`, and the per-command `*.record.json` files for complete inventories and timestamps.

Skills used: alaa-codex-runtime-ops; alaa-testing-strategy.
