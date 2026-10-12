# Allocation-only capture contract

Status: prepared; run only after independent source gates and correctness review clear the candidate. One fixed configuration per runtime, two fresh repetitions, thirty neutral case/variant decisions per invocation. This is sampled post-change allocation observation, not a worker or model-quality comparison.

Authority: verifier executes exact commands and captures artifacts only in this task's `runtime/`. No tools inside the evaluated response, workers, edits, installs, settings, commits, publication or oracle input. Inputs are the complete frozen `checker-lane/codex-allocation-request.txt` and `checker-lane/claude-code-allocation-request.txt`; verify their hashes and loaded-source hashes against matching probe manifests before every invocation. Use request bytes as stdin; do not assemble shell text from their contents.

Commands use argv, not shell interpolation, from repository root. Resolve the installed executables locally without installation. Codex's inspected PowerShell shim forwards to `node` and the sibling `node_modules/@openai/codex/bin/codex.js`; that exact launcher may be invoked directly. Resolve its directory from `Get-Command codex`, and resolve `claude` through `Get-Command claude`. Artifact metadata uses repository-relative paths or named runtime placeholders, never one machine's absolute path.

| Configuration | Exact argv after resolved launcher |
|---|---|
| `codex-sol61-high` | `exec --ignore-user-config --ephemeral --sandbox read-only --model gpt-6.1-sol --config model_reasoning_effort="high" --json --output-last-message <runtime/codex-rN-final.txt> -` |
| `claude-sonnet55-high` | `--safe-mode --tools "" --no-session-persistence --permission-mode plan --model claude-sonnet-5-5 --effort high --output-format json -p` |

For argv construction, the Codex config argument contains the literal TOML value `model_reasoning_effort="high"`; the Claude tools argument is the empty string. Paths above resolve to absolute paths only in the process invocation. No bypass flags, rule suppression, automatic model fallback or global configuration writes are authorized. Codex still loads applicable repository instructions/rules; record any resulting refusal or extra tool use rather than hiding it. Claude safe mode is the installed CLI's customization-isolation option; authentication remains in its existing session. The preflight found no configured hooks or model-force environment overrides.

Limits: sequential invocations, 600 seconds each, ordinary local process priority, no worker threads or services. Terminate only the invocation started by this lane if its timeout expires. One unavailable configuration need not block the independent runtime. No retry, credential repair, escalation or command changes without parent classification. When the first invocation proves its configuration unavailable, preserve that evidence and mark its second repetition unrun with the same blocker instead of repeating a known failure.

Capture separate stdout, stderr, final assistant response, exit, elapsed time, request hash, tool events and reported usage. Do not print raw large outputs. Unknown counters or serving identity stay unknown. Runtime configuration evidence can establish effective requested controls; self-reported identity is not serving telemetry. Any concrete mismatch blocks that configuration's live claim.

Keep responses ungraded. Parse the complete final response as the exact JSON wrapper in `checker-lane/runtime-handoff.md`; do not strip prose or invent absent fields. The independent reviewer receives frozen raw outputs plus the separate oracle and grades criteria. Only then assemble result records and run the implemented result validator. Source tests, real allocator controls, proposed workers, simulated host conditions and worker quality remain distinct evidence layers.

## First attempt and authorized recovery

The initial Codex request/source hashes matched. Its app-server initialization failed with `Access is denied. (os error 5)` before inference; stdout and final response were empty. Capture-helper PowerShell syntax then failed while saving metadata, so original exit/duration remain unknown. This is environment-blocked plus a capture defect, not a failed allocation answer.

Parent authorized one cause-specific evidence-helper repair without changing request/argv/timeout, preserving initial captures. Run independent Claude normally. Retry the exact Codex invocation once through the standard narrow sandbox-escalation review; no bypass flags, installation, credential or settings edits. If denied or still unavailable, preserve the reason and stop that runtime. A successful retry may supply repetition one, followed by one fresh second repetition under the same successful controls. Until runtime acceptance, argv records only requested controls; effective and observed controls remain unknown.
