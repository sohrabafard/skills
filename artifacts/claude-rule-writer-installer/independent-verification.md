# Independent installer verification

- Date: 2026-11-03 UTC
- Agent: `alaa-verifier` (independent verification lane)
- Configured model/effort: unknown from available runtime evidence
- Requested model/effort: `gpt-6-luna` / `medium`
- Observed model/effort: unknown
- Worktree: `.`
- HEAD at start and end: `ff6bd5acf8a1886ea7b6648f79d5c6b8a913358c`
- Installer SHA-256 at start and end: `a48e57592c94375556b2d8c170542410fd49273a05044b6fe90a574e181b31d8`
- Initial and final source-state status, observed before writing this evidence artifact: `?? scripts/install_claude_rule_writer.py`; no other source status entries and no run contamination observed.
- Tool versions: Python `3.14.4`; Claude Code `2.1.307`.
- Host resources observed: 32 CPUs available, affinity `0-31`, cgroup CPU quota `max` and effective cpuset `0-31`; load average at start `4.53 4.90 4.24`. One serial scenario command; no extra workers. Whole-command timeout 120s and runner subprocess timeout 40s.
- Beads: `alaa-hv28` / `alaa-hv28.1` read with `--readonly`; `bd where` matched the expected shared workspace and `bd ping` succeeded. The workspace gate warned that its lock could not be opened on the read-only filesystem; reads completed ungated.

## Command evidence

| Command | Duration | Exit | Classification | Tier | Proof reached | Cases |
|---|---:|---:|---|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 "$TMP_RUNNER" ./scripts/install_claude_rule_writer.py` (disposable temporary scenario runner) | 3.95s | 0 | PASS | Focused | Local smoke (real Claude CLI validation in isolated temporary homes); isolated in-process cases also exercise unit-level behavior | 9 selected, 9 passed, 0 failed, 0 skipped, 0 not run |
| The sequential AST parse, `--help`, and `git diff --check` commands (each completed with exit 0) | 2.6s combined | 0 each | PASS | Focused | Static | n/a |

The runner-selected case list (all observed `ok`):

1. `test_rule_writer_fresh_then_unchanged_with_real_cli`
2. `test_rule_writer_held_lock`
3. `test_rule_writer_manifest_conflicts`
4. `test_rule_writer_missing_dependency`
5. `test_rule_writer_preview_default_and_explicit`
6. `test_rule_writer_replacement_failure_retains_backup`
7. `test_rule_writer_symlink_escape`
8. `test_rule_writer_update_with_real_cli`
9. `test_rule_writer_validation_failure`

The cases assert preview write-freedom; refusal and no mutation for wrong, malformed, or duplicate-name manifests; symlink escape refusal; missing dependency refusal; lock refusal; validator exits 1 and 7 before mutation; injected replacement failure retains the original and a restorable backup; fresh install and unchanged rerun with real Claude validation; and update preserving the manifest, unknown files, sibling plugin, settings, and a restorable backup.

## Result

All dispatched checks passed. No failing cases, skips, flaky outcomes, or blocked checks. No live Claude home was read or written, no live installation was performed; scenario installs and updates ran only in isolated temporary homes. The disposable runner remained outside the repository; no repository test fixture was added. Highest observed level is local smoke for the real CLI validation path; this does not establish behavior in a deployed or production runtime.
