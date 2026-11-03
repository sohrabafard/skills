# Frozen candidate verification

Plan: `beads:alaa-1khq`; final boundary: `alaa-1khq.1`.
Candidate base: `0c37f68dfb7ae7312c4ed4b86b90a7e106aa05d7`. Commands ran on the unchanged frozen candidate; no source edits made.

## Initial repository state

`git status --short`: modified `scripts/install_claude_rule_writer.py`, `skills/sohrab/alaa-prompting-guide/SKILL.md`; untracked `_to_delete/20261103-claude-rule-writer-plugin/`, `scripts/install_claude_agents.py`, `scripts/test_install_claude_agents.py`.

## Commands

Durations are wall seconds reported by the execution tool. All commands used serial host execution; timeout budget 60s each; no explicit CPU cap. Resource class: lightweight.

| Command | cwd | duration | exit | classification | tier / proof | cases |
|---|---|---:|---:|---|---|---|
| `python3 -B -m unittest -v scripts.test_install_claude_agents` | repository root | 2.459s | 0 | PASS | focused / unit (2) | selected 17, passed 17, failed 0, skipped 0, not run 0 |
| `python3 -B -c 'import ast, pathlib; paths = ["scripts/install_claude_agents.py", "scripts/install_claude_rule_writer.py", "scripts/test_install_claude_agents.py", "_to_delete/20261103-claude-rule-writer-plugin/install_claude_rule_writer.py"]; [ast.parse(pathlib.Path(path).read_text(), filename=path) for path in paths]; print(f"AST parsed {len(paths)} Python files")'` | repository root | 2.174s | 0 | PASS | focused / static (1) | n/a |
| `git diff --check` | repository root | 1.826s | 0 | PASS | focused / static (1) | n/a |
| `python3 -B scripts/check_rule_writer_grants.py` | `skills/sohrab/alaa-prompting-guide` | 2.288s | 0 | PASS | focused / static (1) | n/a |
| `python3 -B scripts/check_codex_model_policy.py --agent-root assets/rule-writer/codex` | `skills/sohrab/alaa-prompting-guide` | 2.165s | 0 | PASS | focused / static (1) | n/a |
| `python3 -B scripts/check_claude_model_policy.py` | `skills/sohrab/alaa-prompting-guide` | 2.329s | 0 | PASS | focused / static (1) | n/a |
| `git show HEAD:scripts/install_claude_rule_writer.py \| cmp - _to_delete/20261103-claude-rule-writer-plugin/install_claude_rule_writer.py` | repository root | 2.118s | 0 | PASS | focused / static (1) | n/a |

Unit runner output named 17 tests, all `ok`; final summary `Ran 17 tests ... OK`. Grant checker: `OK: both wrappers embed the contract unchanged, hold read-only grants, and omit executable model/effort defaults`. Codex checker: `OK: model policy and 1 model-neutral agents`. Claude checker: `OK: Claude policy and 30 projections; activation and calibration unproven`.

## Frozen scoped SHA-256 manifest

```text
235a57dcfc553411b3f087c06ffd4c4dfc0fcb997ac8d5f4116d3c4814a34fb8  scripts/install_claude_agents.py
b1ac21bdc3843b56c9670855110a7bf3d0bc17260701375b3c264bb39e0d478a  scripts/install_claude_rule_writer.py
758d2606b5ccbf8cfe3a6a4bec3326053b4b698f2181f8187ceed03f72ea92ea  scripts/test_install_claude_agents.py
a48e57592c94375556b2d8c170542410fd49273a05044b6fe90a574e181b31d8  _to_delete/20261103-claude-rule-writer-plugin/install_claude_rule_writer.py
3d7cc37c16dc25cf843f17a924b95950ea76d0f8aef7ebf350ceafe3f6058686  skills/sohrab/alaa-prompting-guide/SKILL.md
```

Archived original equals `git show HEAD:scripts/install_claude_rule_writer.py` byte-for-byte (`cmp` exit 0; SHA-256 also matches).

## Outcome and limits

No failures, skips, or flaky results observed. This focused proof supports source and CLI behavior only. Installed role neutrality was checked; serving identity remains unknown. The Claude checker explicitly reports activation and calibration unproven. No home installation, live environment, or production behavior was exercised.


## Final repository state

`git status --short`: modified `scripts/install_claude_rule_writer.py`, `skills/sohrab/alaa-prompting-guide/SKILL.md`; untracked `_to_delete/20261103-claude-rule-writer-plugin/`, `artifacts/claude-agent-unification/`, `scripts/install_claude_agents.py`, `scripts/test_install_claude_agents.py`. These are the expected candidate and verification artifact paths; no additional contamination observed.
