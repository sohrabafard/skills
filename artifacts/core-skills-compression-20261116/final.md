# Final measurement

Measured on `work/core-skills-compression` at d2e4638b, 2026-11-17, with `measure.py`. Compare with `baseline.md`.

| Skill | Frontmatter | SKILL.md body | References | Assets | Hand-written agents | Generated agents | Other | Source total |
|---|---|---|---|---|---|---|---|---|
| `alaa-testing-strategy` | 104 | 2510 | 10381 | 0 | 0 | 0 | 60 | 13055 |
| `alaa-cc-orchestrator` | 102 | 2001 | 10788 | 3455 | 10935 | 14248 | 27 | 27308 |
| `alaa-codex-orchestrator` | 101 | 1972 | 11491 | 4100 | 10237 | 18046 | 608 | 28509 |
| `alaa-workflow` | 113 | 872 | 13466 | 1788 | 0 | 0 | 31 | 16270 |
| `alaa-code-intelligence-routing` | 105 | 723 | 7056 | 0 | 0 | 0 | 47 | 7931 |
| `alaa-low-noise` | 77 | 714 | 964 | 0 | 0 | 0 | 29 | 1784 |
| `alaa-prompting-guide` | 89 | 772 | 21318 | 4316 | 0 | 0 | 49 | 26544 |

Source total, all seven skills: 121401 words. Generated agents, CHANGELOG.md and scripts are excluded from it.

| Checker | Tuple | String constants |
|---|---|---|
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `EXECUTION` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `RESOURCES` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `CLASSIFICATION` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `REQUIREMENTS` | 211 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `NORMATIVE_DUPLICATES` | 102 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `EXPECTED_NORMATIVE_INVENTORY_SHA256` | 1 |
| `alaa-testing-strategy/scripts/check_execution_contracts.py` | `CONTRADICTIONS` | 20 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `EQUIVALENT_REQUIREMENTS` | 6 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `BOUNDED_REQUIREMENTS` | 14 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `IMPLEMENTER_REQUIREMENTS` | 16 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `GATE_REQUIREMENTS` | 23 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_MODEL_CLAUSES` | 3 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_REQUIREMENTS` | 12 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `CADENCE_REQUIREMENTS` | 28 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_REQUIREMENTS` | 14 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_SEAMS` | 28 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_CONTRADICTIONS` | 11 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_REQUIREMENTS` | 29 |
| `alaa-cc-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_CONTRADICTIONS` | 7 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `EQUIVALENT_REQUIREMENTS` | 6 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `BOUNDED_REQUIREMENTS` | 14 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `IMPLEMENTER_REQUIREMENTS` | 15 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `GATE_REQUIREMENTS` | 23 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_MODEL_CLAUSES` | 4 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `DEFAULT_REQUIREMENTS` | 12 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `CADENCE_REQUIREMENTS` | 28 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_REQUIREMENTS` | 14 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_SEAMS` | 28 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `COLLECTION_CONTRADICTIONS` | 11 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_REQUIREMENTS` | 29 |
| `alaa-codex-orchestrator/scripts/check_agent_contracts.py` | `RUN_ECONOMY_CONTRADICTIONS` | 7 |
