# Frozen Lua package verification

- Agent: `/root/verification` (configured profile: `alaa-verifier`, gpt-6-luna / low; requested: none; observed runtime identity: unknown).
- Repository: `repository root`; HEAD `d41981b99554de2829f84a1879226582ba06dc7c`.
- Initial status: the dispatched checkout had dirty paths confined to the authorized HAProxy and HAProxy Lua packages plus plan/checkpoint/evidence artifacts. Git emitted permission warnings while scanning unrelated archived temp directories under `_to_delete`; the visible status listed those expected paths.
- Final status: same authorized package/artifact path set; no Lua package fingerprint drift. Same Git scan warnings for inaccessible archived temp directories. No unplanned tracked changes observed.
- Frozen package SHA256: 38 files excluding `__pycache__`; before and after manifests identical (`diff=0`). See `lua-manifest-before.sha256` and `lua-manifest-after.sha256`.

| Command | CWD | Limits | UTC / duration | Exit | Classification / tier / proof |
|---|---|---|---|---:|---|
| `python -B skills/sohrab/alaa-haproxy-lua/test/test_runtime_runner.py` | `repository root` | BelowNormal; affinity 1 CPU; timeout 30s; no env overrides | 2026-10-01T18:59:44.9548882Z–18:59:45.8317837Z / 0.866s | 0 | PASS; focused; level 2 unit; 4/4 tests |
| `python -B skills/sohrab/alaa-haproxy-lua/scripts/check_runtime.py --image haproxy:3.4.6-alpine` | `repository root` | BelowNormal; affinity 1 CPU; timeout 120s (script deadline 90s); Docker harness `--cpus=1`, memory 128 MiB, network none; no env overrides | 2026-10-01T19:00:12.1274575Z–19:00:15.7596331Z / 3.621s | 0 | PASS; affected; level 5 in-runtime; HAProxy 3.4.6 / Lua 5.4.8, 34/34 embedded Lua checks and all openlibs/parser/sample/token HTTP probes passed |

Runtime used cached image `haproxy:3.4.6-alpine`, dispatched image ID `sha256:7af8255207ee9964ccb4eec8ce4b7a40b777769665e3ae83897fb01b24d8a43a`; no pull, installation, or network access was requested. Runtime stdout records the unit and probe results and contains no Terminated lines; runtime stderr contains three Terminated lines. The command exited 0. These are retained termination messages; no assertion failure is inferred. Both streams are preserved verbatim in `runtime.stdout.txt` and `runtime.stderr.txt`.

Raw child stdout/stderr and manifests are retained beside this report. No failures, retries, skipped checks, or product edits. No memory files used.



