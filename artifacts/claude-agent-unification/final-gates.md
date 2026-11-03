# Final candidate gates

Plan: `beads:alaa-1khq`; phase: `alaa-1khq.1`; candidate HEAD: `472e2e407e9421a6130304670f1972eef391ab29`.

The candidate contained documentation edits to `install-skills.md`, `docs/install-skills/40-agent-installation.md`, and `docs/install-skills/50-rule-writer.md`. Parent review identified a misplaced restored Claude role paragraph and requested pausing doc-dependent gates until correction. Those gates remain pending; no attempt was made to verify the currently known incorrect draft. This record captures the independent root checks completed while waiting.

All commands ran from repository root, lightweight host execution, 60s timeout budget, no explicit CPU cap. Test selector: n/a for all checks.

| Command | Duration | Exit | Classification | Tier / proof | Scope/result |
|---|---:|---:|---|---|---|
| `python3 -B scripts/validate_sohrab_skill_pack.py` | 2.782s | 0 | PASS | final / static (1) | 72 skills; advisory body-length and description-budget warnings; exit contract clean |
| `python3 -B scripts/check_skill_index.py` | 2.778s | 0 | PASS | final / static (1) | 72 skill directories and 72 entries in each index; no findings |
| `python3 -B scripts/check_fleet_references.py` | 5.109s | 0 | PASS | final / static (1) | 72/72 skills, 1145 Markdown files, 4422 citations; no findings; informational unmarked paths only |
| `python3 -B scripts/check_lifecycle_contract.py` | 2.959s | 0 | PASS | final / static (1) | Lifecycle owner/states/reporters found; no findings |

## Deferred document checks, completed

After the correction was reported complete and the docs frozen, these gates ran from repository root with a 60s timeout budget and lightweight host execution:

| Command/check | Duration | Exit | Classification | Tier / proof | Scope/result |
|---|---:|---:|---|---|---|
| `python3 -B "$SKILL_DIR/scripts/check_markdown_links.py" . --files install-skills.md docs/install-skills/40-agent-installation.md docs/install-skills/50-rule-writer.md artifacts/claude-agent-unification/verification.md --line-budget` (`SKILL_DIR` resolves to the installed `alaa-repo-docs` skill.) | 2.286s | 0 | PASS | final / static (1) | Links valid; line budgets: 99 YELLOW, 66 YELLOW, 43 GREEN, verification 45 GREEN |
| `git diff --check` | 2.206s | 0 | PASS | final / static (1) | No whitespace findings |
| Compare source-root and generated vendor marker spans with `472e2e40` | 2.223s | 0 | PASS | final / static (1) | Source roots, install vendor list, and README vendor list byte-identical |
| Compare Codex fenced commands with `472e2e40` | included above | 0 | PASS | final / static (1) | Both orchestrator installer command and Codex writer copy command unchanged |
| `bash -n` for fenced shell blocks in the 3 changed docs | included above | 0 | PASS | final / static (1) | 9 blocks parsed successfully |

The final `git diff --check` was inadvertently invoked a second time with the SHA/status capture command; it also exited 0. No source changed between runs. Initial and final `git status --short` showed the same candidate docs plus this verification artifact; no additional changes or contamination were found.

## Frozen documentation SHA-256

```text
c2f45d50a27f4b2f098077768ff1ae7760eb32cb24f5e03dbc3e8d745e4417f3  install-skills.md
1dbd15316ceeeab4587103beb9e6d5cb46ee4fdbedcc49934b134fced9e6ce08  docs/install-skills/40-agent-installation.md
7c02def8c6d97df7d01403db86db1370774481b8c2e9382679c80c2fe4b5c844  docs/install-skills/50-rule-writer.md
```

Source/test/model-policy evidence remains the prior focused record in `verification.md`; parent reports no source-code changes since `472e2e40`, so that evidence is cited and not repeated.
