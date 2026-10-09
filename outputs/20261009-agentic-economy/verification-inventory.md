# Independent candidate verification inventory

Run from the repository root, sequentially, with process-local `PYTHONDONTWRITEBYTECODE=1`.
These are lightweight Python/source checks at normal priority; one runner, no nested parallel suite.
Record exit code, duration, command, portable cwd, logs and before/after source hashes.

## Commands

1. `python -B skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py`
2. `python -B skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py`
3. `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py`
4. `python -B skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py`
5. `python -B skills/sohrab/alaa-prompting-guide/scripts/check_codex_model_policy.py --agent-root skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex`
6. `python -B skills/sohrab/alaa-prompting-guide/scripts/check_claude_model_policy.py --agent-root skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude`
7. `python -B skills/sohrab/alaa-prompting-guide/scripts/check_agent_evals.py`
8. `python -B skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py`
9. `python -B scripts/validate_sohrab_skill_pack.py`
10. `python -B scripts/check_skill_index.py`
11. `python -B scripts/check_fleet_references.py`
12. `python -B scripts/check_lifecycle_contract.py`
13. `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files <explicit changed/new Markdown files in the four skill trees>`
14. `git diff --check HEAD -- skills/sohrab/alaa-workflow skills/sohrab/alaa-prompting-guide skills/sohrab/alaa-codex-orchestrator skills/sohrab/alaa-cc-orchestrator`

## Consolidation and boundaries

- Pack aggregates cover managed policy pins, generated drift, grants and agent contracts. Their coverage does not include the normal contract checker's main/economy checks, so commands 3-4 are necessary. Separate managed grant/render reruns add no outcome and are omitted.
- Rule-writer roots are outside managed orchestrator agent roots, hence commands 5-6.
- Evaluation checks validate scenario records only; they execute no models and prove no comparative quality.
- Reuse independent workflow `verification/workflow/result.json`: 75 tests passed with 16 unchanged source hashes. Verify candidate still matches those hashes; rerun only if an input changed.
- Changed-checker discriminating fixtures were observed in writer-focused evidence. Independent correctness review inspects those changes; no duplicate full fixture cycle without new findings.
- Source instruction contracts and generated role files are atomic size-budget exemptions. Human artifact/report/index line budgets and links run after documentation completion.
- Parent closes plan validation, documentation links, final source snapshot and baseline preservation after reports stabilize. Do not label these pending checks passed here.
- No installation, deployment, Docker/application suite, paid live comparisons or performance claim.
