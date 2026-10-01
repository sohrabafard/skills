# Final affected verification

Overall: FAILED due to one runtime gate reporting a lifecycle assertion failure. The two self-tests that initially ran in the wrong context passed on their one authorized elevated-host rerun. Of the two Docker gates, the examples parser passed and the runtime gate failed. No product files were edited.

Agent `/root/verification`; configured profile `alaa-verifier` (gpt-6-luna / low); requested model/effort none; observed runtime identity unknown. Repository root; PowerShell; no environment overrides. The examples parser Docker gate used a child-only PATH prepend for Git OpenSSL; the runtime gate had no environment overrides. No persistent environment change was made.

## Preflight and frozen inputs

- `python --version` returned `Python 3.13.14` before the first snapshot. Per-command timing was not captured for this preflight read.
- `docker image inspect haproxy:3.4.6-alpine --format '{{.Id}}'` ran in authorized elevated host context and returned `sha256:7af8255207ee9964ccb4eec8ce4b7a40b777769665e3ae83897fb01b24d8a43a`, matching the dispatched identity. Its isolated start/end timing was not captured.
- Prior Lua manifest: all 23 current non-Markdown files match; 0 added, changed, or removed. This covers current executable/configuration/fixture inputs. The package's Markdown was reorganized after the earlier runtime receipt, so only the unchanged non-Markdown inputs are compared.
- Before/after candidate snapshots each cover 477 files. HEAD stayed `d41981b99554de2829f84a1879226582ba06dc7c`; both `scope_sha256` values equal `5d59faf0ec9e18ef0c25bdabe46ed62bd8a9ea8d34b6788f3aac689e41270b5c`.

## Command evidence

Every row used repository root and at most a 30-second timeout. Full stdout/stderr and exact timing receipts are retained as `final-<name>.stdout.txt`, `final-<name>.stderr.txt`, and `final-commands.txt`.

| Command | UTC start–end / duration | Exit | Result, tier, proof |
|---|---|---:|---|
| `python -B scripts/validate_sohrab_skill_pack.py` | 19:40:50.3043920Z–19:40:50.6790609Z / 369 ms | 0 | PASS; affected; level 1 static; warnings only |
| `python -B scripts/check_skill_index.py` | 19:40:50.7125740Z–19:40:50.8855037Z / 172 ms | 0 | PASS; affected; level 1 static; no findings |
| `python -B scripts/check_fleet_references.py` | 19:40:50.8886681Z–19:40:54.4190444Z / 3,530 ms | 0 | PASS; affected; level 1 static; no findings, informational unmarked-path notices |
| `python -B scripts/check_lifecycle_contract.py` | 19:40:54.4268957Z–19:40:55.1514316Z / 724 ms | 0 | PASS; affected; level 1 static; no findings |
| `python -B skills/sohrab/alaa-haproxy/scripts/test_runner_contracts.py` | 19:40:55.1550952Z–19:40:55.7777823Z / 622 ms | 0 | PASS; affected; level 2 unit; 12/12 |
| `python -B skills/sohrab/alaa-haproxy/scripts/check_http_error_bytes.py --self-test` | 19:40:55.7835258Z–19:40:55.9772150Z / 193 ms | 0 | PASS; affected; level 2 unit; 8 byte fixtures, 0 failures |
| `python -B skills/sohrab/alaa-haproxy/scripts/check_defaults_scope.py --self-test` | 19:40:55.9799125Z–19:40:56.3333410Z / 353 ms | 1 | ENVIRONMENT-BLOCKED; affected; no proof; `PermissionError [Errno 13]` writing temp `crlf.cfg` |
| `python -B skills/sohrab/alaa-haproxy/scripts/check_defaults_scope.py skills/sohrab/alaa-haproxy/examples/haproxy` | 19:40:56.3374076Z–19:40:56.6161417Z / 278 ms | 0 | PASS; affected; level 1 static; 21 files, 0 findings |
| `python -B skills/sohrab/alaa-haproxy/scripts/check_examples.py --self-test` | 19:40:56.6195817Z–19:40:56.8391382Z / 219 ms | 1 | ENVIRONMENT-BLOCKED; affected; no proof; `PermissionError [Errno 13]` writing temp `contract.cfg` |
| `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan outputs/20261001-haproxy-346/20261001-120000_haproxy-346.md` | 19:40:56.8429793Z–19:40:57.0470339Z / 204 ms | 0 | PASS; affected; level 1 static; no blocking errors |
| `git diff --check -- skills/sohrab/alaa-haproxy skills/sohrab/alaa-haproxy-lua outputs/20261001-haproxy-346 outputs/README.md docs/agents/20261001-120000_haproxy-346-state.md` | 19:40:57.0496312Z–19:40:57.1402475Z / 90 ms | 0 | PASS; affected; level 1 static; CRLF/LF advisories only |
| python -B skills/sohrab/alaa-haproxy/scripts/check_examples.py --docker-image haproxy:3.4.6-alpine | not run at initial attempt | — | SKIPPED then; subsequently PASS in the authorized Docker run below |
| python -B skills/sohrab/alaa-haproxy/scripts/check_runtime_3_4.py --docker-image haproxy:3.4.6-alpine | not run at initial attempt | — | SKIPPED then; subsequently failed in the authorized Docker run below |

At the initial attempt, both self-tests ran in default PowerShell context despite the dispatched elevated host requirement; their retained stderr shows PermissionError [Errno 13] writing temp fixtures. They are classified ENVIRONMENT-BLOCKED for that initial attempt. The later elevated-host retries were explicitly authorized and passed; no further retry occurred. The Docker gates were initially skipped, then run once below. No pull or install occurred.

## Cited Lua evidence and limits

The final Lua runtime result remains applicable to the unchanged executable/configuration/fixture inputs and matching cached image ID. The independent receipt at `verification-report.md` records the focused runner suite 4/4 and the fresh HAProxy 3.4.6 / Lua 5.4.8 runtime suite 34/34 plus openlibs, parser, sample, and token HTTP probes, all exit 0. This is level 5 in-runtime evidence. The package proof register `skills/sohrab/alaa-haproxy-lua/references/sources/30-target-proof-register.md` also records the author’s Lua checker self-test 16/16 and production token example static check with zero findings; neither was rerun here. Those results do not prove live gateway behavior, egress failure, performance, task/filter lifecycle, drain, or deployment.

The initial snapshot is final-before.json; later frozen-tree checks are retry-before.json, retry-mid.json, and retry-after.json. Preflight outputs and the non-Markdown manifest comparison are in `final-preflight.txt` and `final-lua-input-check.txt`; gate outputs and stderr are retained beside this report. No silent pass is assigned to an unrun gate.


## Authorized retries and Docker results

| Command / attempt | UTC start–end / duration | Context and limits | Exit / classification / proof |
|---|---|---|---|
| python -B skills/sohrab/alaa-haproxy/scripts/check_defaults_scope.py --self-test (host-context retry) | 19:48:14.9949605Z–19:48:15.1703291Z / 175 ms | Elevated host; repository root; no overrides; 30s | 0; PASS in required context; level 2 unit; CRLF fixture and all self-test cases passed |
| python -B skills/sohrab/alaa-haproxy/scripts/check_examples.py --self-test (host-context retry) | 19:48:29.8560627Z–19:48:30.1053014Z / 249 ms | Elevated host; repository root; no overrides; 30s | 0; PASS in required context; level 2 unit; CRLF fixture and all self-test cases passed |
| python -B skills/sohrab/alaa-haproxy/scripts/check_examples.py --docker-image haproxy:3.4.6-alpine | 19:49:34.2870385Z–19:49:56.5165650Z / 22.227s | Elevated host; BelowNormal; affinity 1 CPU; timeout 180s; child PATH prepended with C:/Program Files/Git/usr/bin; harness 1 CPU, 256 MiB, network none | 0; PASS; affected; level 2 parse/validation proof only; 21 example configs, 22 parsed, 0 skipped, 0 findings |
| python -B skills/sohrab/alaa-haproxy/scripts/check_runtime_3_4.py --docker-image haproxy:3.4.6-alpine | 19:50:27.6227851Z–19:50:36.1662131Z / 8.540s | Elevated host; BelowNormal; affinity 1 CPU; timeout 180s; no overrides; harness 1 CPU, 256 MiB, network none | 1; PRODUCT-FAILURE; affected; level 5 executed, no passing proof; FAIL [active stream prevents deletion]: lifecycle assertion |

The runtime assertion is recorded exactly as a candidate gate failure; the actual HAProxy CLI reply is absent, so no HAProxy regression is established. No cause was diagnosed and no retry was made. Level 3 parity is inapplicable because this command does not compare a double with the real implementation. Raw output is in retry-defaults.stdout.txt / .stderr.txt, retry-examples.stdout.txt / .stderr.txt, final-docker-examples.stdout.txt / .stderr.txt, and final-docker-runtime.stdout.txt / .stderr.txt. Earlier failed default-context streams remain in the final-defaults-self-test.* and final-examples-self-test.* files.

Snapshots final-before.json, retry-before.json, retry-mid.json, and retry-after.json all match: HEAD d41981b99554de2829f84a1879226582ba06dc7c, 477 files, scope digest 5d59faf0ec9e18ef0c25bdabe46ed62bd8a9ea8d34b6788f3aac689e41270b5c. No candidate movement was observed.

## Parent closeout checks

- `python -B outputs/20261001-haproxy-346/capture_snapshot.py outputs/20261001-haproxy-346/verification/final-close.json`: exit 0, same 477-file scope digest and HEAD. Subsequent reconciliation touches only task receipts and workflow state.
- Updated workflow validator: first exit 1 because completed phases referenced the digest indirectly rather than using the validator's required HEAD/SHA256/paths fields. One cause-specific artifact correction and retry exited 0. This did not change package inputs.
- Broader `git diff --check HEAD -- skills/sohrab/alaa-haproxy skills/sohrab/alaa-haproxy-lua outputs/20261001-haproxy-346 outputs/README.md docs/agents/20261001-120000_haproxy-346-state.md`: exit 1. Unlike the earlier unstaged-only check, this includes newly indexed files. It flags intentional CRLF/terminal blank lines in raw HTTP fixtures, preserved raw command streams, and extra terminal blank lines in verification Markdown receipts. Raw fixture/log bytes remain preserved. This broader check is not reported as passing.
- Final visible-path inspection: 213 changed/untracked paths, 0 outside the two packages and authorized task artifacts; HEAD unchanged. Git warned about inaccessible unrelated archived temp directories. No index mutation, commit or gateway write was performed during closeout.

Final acceptance is explicitly partially validated. Source/static/unit/parser
results do not establish passing lifecycle, gateway compatibility or deployment.





