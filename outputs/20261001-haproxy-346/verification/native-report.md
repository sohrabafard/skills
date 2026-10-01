# Native gate evidence

- Agent: `/root/verification`; configured: gpt-6-luna / low; requested: none; observed runtime identity: unknown.
- Repository HEAD before/after: `d41981b99554de2829f84a1879226582ba06dc7c`. Frozen scope: 421 files; `scope_sha256` before and after `d1fe0f492c5dbbd7951586c77d0444e12e5833dfa8ee83ce4c334abef49b4a4b` (equal).
- Every command ran once, serially, from repository root, without environment overrides; 30s per-command timeout. No retries or product edits.

| Command | UTC start–end | Duration | Exit | Classification / tier / proof |
|---|---|---:|---:|---|
| `python -B outputs/20261001-haproxy-346/capture_snapshot.py outputs/20261001-haproxy-346/verification/native-before.json` | 19:03:22.5305601Z–19:03:22.9425442Z | 412ms | 0 | PASS; affected snapshot guard; n/a |
| `python -B scripts/validate_sohrab_skill_pack.py` | 19:03:44.0812667Z–19:03:44.4108348Z | 325ms | 0 | PASS; affected; level 1 static |
| `python -B scripts/check_skill_index.py` | 19:03:44.4226148Z–19:03:44.5650458Z | 142ms | 0 | PASS; affected; level 1 static |
| `python -B scripts/check_fleet_references.py` | 19:03:44.5670916Z–19:03:47.5535757Z | 2,986ms | 0 | PASS; affected; level 1 static |
| `python -B scripts/check_lifecycle_contract.py` | 19:03:47.5562311Z–19:03:47.9502808Z | 394ms | 0 | PASS; affected; level 1 static |
| `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan outputs/20261001-haproxy-346/20261001-120000_haproxy-346.md` | 19:03:47.9546039Z–19:03:48.1132860Z | 158ms | 0 | PASS; affected; level 1 static |
| `git diff --check -- skills/sohrab/alaa-haproxy skills/sohrab/alaa-haproxy-lua outputs/20261001-haproxy-346 docs/agents/20261001-120000_haproxy-346-state.md` | 19:03:48.1156300Z–19:03:48.1818066Z | 66ms | 0 | PASS; affected; level 1 static |
| `python -B outputs/20261001-haproxy-346/capture_snapshot.py outputs/20261001-haproxy-346/verification/native-after.json` | 19:04:07.3361364Z–19:04:07.6319021Z | 296ms | 0 | PASS; affected snapshot guard; n/a |

The validator reported body-length warnings; the fleet-reference checker reported 325 informational unmarked target paths; `git diff --check` reported CRLF-to-LF advisories. None failed its gate. Snapshot HEAD and scope digest are equal. Prior runtime checks remain valid for the identical Lua package fingerprint; parser/lifecycle runtime tests remain blocked per dispatch and were not run.

Raw output pairs, timing receipts, before/after snapshots, and final status are retained in this directory as `native-*.stdout.txt`, `native-*.stderr.txt`, `native-commands.txt`, `native-before.json`, `native-after.json`, and `native-final-status.txt`.
